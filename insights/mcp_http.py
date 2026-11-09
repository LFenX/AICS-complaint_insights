"""HTTPS-only, network-bounded bearer gateway around the MCP protocol app."""
from dataclasses import dataclass
import hmac
from ipaddress import ip_address, ip_network
import json
import logging
from pathlib import Path
import ssl
import time
import uuid

from mcp.server.transport_security import TransportSecuritySettings
from starlette.responses import JSONResponse

from .config import ROOT
from .mcp_server import (DEFAULT_TOOL_CALLS_PER_MINUTE, ReadAPI, create_server, decode_wire_json,
                         normalize_wire_request, principal, validate_tool_rate_limit, wire_arguments)
from .mcp_tokens import read_object, validated_tokens

logger = logging.getLogger('insights.mcp.http')
PRIVATE_NETWORKS = tuple(ip_network(value) for value in ['10.0.0.0/8','172.16.0.0/12','192.168.0.0/16'])


@dataclass(frozen=True, repr=False)
class MCPSettings:
    host: str
    port: int
    allowed_networks: tuple[str, ...]
    tokens: dict[str, str]
    certificate: Path
    private_key: Path
    api_credentials: Path
    token_path: Path | None = None
    tool_calls_per_minute: int = DEFAULT_TOOL_CALLS_PER_MINUTE

    def current_tokens(self) -> dict[str, str]:
        if self.token_path is None:
            return self.tokens
        try:
            return validated_tokens(read_object(self.token_path))
        except (OSError, UnicodeError, json.JSONDecodeError, TypeError, ValueError):
            # Never resurrect a revoked startup credential on disk corruption.
            return {}

    def validate(self):
        validate_tool_rate_limit(self.tool_calls_per_minute)
        address = ip_address(self.host)
        if address.version != 4 or not any(address in network for network in PRIVATE_NETWORKS):
            raise ValueError('remote MCP host must be one specific RFC1918 IPv4 address')
        if not 1024 <= self.port <= 65535:
            raise ValueError('invalid MCP port')
        networks = tuple(ip_network(value,strict=True) for value in self.allowed_networks)
        if not networks or any(not any(network.subnet_of(private) for private in PRIVATE_NETWORKS) for network in networks):
            raise ValueError('MCP clients must be restricted to explicit private networks')
        if not any(address in network for network in networks):
            raise ValueError('MCP listen address must belong to an allowed network')
        validated_tokens({'tokens': self.tokens})
        for path in [self.certificate,self.private_key,self.api_credentials]:
            path.resolve().relative_to((ROOT/'.secrets').resolve())
            if not path.is_file():
                raise ValueError('MCP private asset missing')

    @classmethod
    def load(cls,path:Path | None = None):
        filename = path or ROOT/'.secrets/mcp-server.json'
        data = read_object(filename)
        for key in ['certificate','private_key','api_credentials']:
            data[key] = Path(data[key])
        data['allowed_networks'] = tuple(data['allowed_networks'])
        data['token_path'] = filename
        settings = cls(**data)
        settings.validate()
        return settings


class MCPAccessMiddleware:
    def __init__(self,app,settings:MCPSettings,post_only:bool=False):
        self.app = app
        self.settings = settings
        self.networks = tuple(ip_network(value) for value in settings.allowed_networks)
        self.post_only = post_only

    async def __call__(self,scope,receive,send):
        if scope['type'] != 'http':
            await self.app(scope,receive,send)
            return
        request_id = uuid.uuid4().hex
        started = time.monotonic()
        headers = dict(scope.get('headers',[]))
        client_ip = (scope.get('client') or ('',0))[0]
        identity = None
        try:
            allowed = any(ip_address(client_ip) in network for network in self.networks)
        except ValueError:
            allowed = False
        code = 403
        if scope.get('scheme') != 'https':
            response = JSONResponse({'error':'HTTPS_REQUIRED'},status_code=403)
        elif not allowed:
            response = JSONResponse({'error':'NETWORK_DENIED'},status_code=403)
        elif headers.get(b'host') != f'{self.settings.host}:{self.settings.port}'.encode():
            code = 421
            response = JSONResponse({'error':'INVALID_HOST'},status_code=421)
        elif headers.get(b'origin') not in (None, f'https://{self.settings.host}:{self.settings.port}'.encode()):
            response = JSONResponse({'error':'INVALID_ORIGIN'},status_code=403)
        else:
            auth = headers.get(b'authorization',b'').split(None,1)
            presented = auth[1] if len(auth)==2 and auth[0].lower()==b'bearer' else b''
            for candidate,token in self.settings.current_tokens().items():
                if hmac.compare_digest(presented,token.encode()):
                    identity = candidate
            if identity is None:
                code = 401
                response = JSONResponse({'error':'VALID_MCP_BEARER_REQUIRED'},status_code=401,
                                        headers={'WWW-Authenticate':'Bearer realm="complaint-insights"'})
            else:
                response = None
        async def audited_send(message):
            nonlocal code
            if message['type']=='http.response.start':
                code = message['status']
                message['headers'] = list(message.get('headers',[]))+[(b'x-request-id',request_id.encode()),(b'cache-control',b'no-store')]
            await send(message)
        token = principal.set(identity or 'unauthorized')
        try:
            if response is not None:
                await response(scope,receive,audited_send)
            elif scope.get('path') == '/health':
                await JSONResponse({'status':'ok','service':'complaint-insights-mcp'})(scope,receive,audited_send)
            elif self.post_only and scope.get('path') in {'/mcp','/mcp/'} and scope.get('method') in {'GET','DELETE'}:
                # An explicit 405 is the 2025-11-25 transport contract when this
                # stateless JSON server offers no standalone notification stream.
                await JSONResponse({'error':'METHOD_NOT_ALLOWED'},status_code=405,headers={'Allow':'POST'})(scope,receive,audited_send)
            else:
                await self.app(scope,receive,audited_send)
        finally:
            principal.reset(token)
            logger.info(json.dumps({'request_id':request_id,'identity':identity,'client_ip':client_ip,
                                    'method':scope.get('method'),'status':code,'duration_ms':round((time.monotonic()-started)*1000)}))


class MCPProtocolErrors:
    """Preserve request identity before SDK union parsing; redact bad envelopes."""

    MAX_BODY = 131072

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            await self.app(scope,receive,send)
            return
        exact_arguments = None
        if scope.get('method') == 'POST' and scope.get('path') in {'/mcp','/mcp/'}:
            raw = bytearray()
            while True:
                message = await receive()
                if message['type'] == 'http.disconnect':
                    return
                raw.extend(message.get('body', b''))
                if len(raw) > self.MAX_BODY:
                    await JSONResponse({'error':'REQUEST_TOO_LARGE'},status_code=413)(scope,receive,send)
                    return
                if not message.get('more_body',False):
                    break
            try:
                data, exact_data = decode_wire_json(raw)
            except (ArithmeticError,ValueError,UnicodeError,RecursionError):
                await self.error(scope,receive,send,-32700,'Parse error')
                return
            if isinstance(exact_data,dict) and exact_data.get('method') == 'tools/call':
                params = exact_data.get('params')
                if isinstance(params,dict) and isinstance(params.get('name'),str):
                    exact_arguments = (params['name'],params.get('arguments',{}))
            if isinstance(data,dict) and 'method' in data and 'id' in data:
                try:
                    normalized = normalize_wire_request(data,exact_data)
                except ValueError:
                    await self.error(scope,receive,send,-32600,'Invalid Request')
                    return
                if normalized:
                    raw = json.dumps(data,ensure_ascii=False,separators=(',',':')).encode('utf-8','backslashreplace')
                    if len(raw) > self.MAX_BODY:
                        await JSONResponse({'error':'REQUEST_TOO_LARGE'},status_code=413)(scope,receive,send)
                        return
                    scope = {**scope,'headers':[(key,value) for key,value in scope.get('headers',[]) if key.lower() != b'content-length']
                        + [(b'content-length',str(len(raw)).encode())]}
            original_receive = receive
            delivered = False
            async def replay_receive():
                nonlocal delivered
                if not delivered:
                    delivered = True
                    return {'type':'http.request','body':bytes(raw),'more_body':False}
                return await original_receive()
            receive = replay_receive
        pending = None
        body = bytearray()
        overflow = False

        async def checked_send(message):
            nonlocal pending, overflow
            if message['type'] == 'http.response.start' and message['status'] == 400:
                pending = message
                return
            if pending is None or message['type'] != 'http.response.body':
                await send(message)
                return
            if not overflow:
                chunk = message.get('body',b'')
                if len(body) + len(chunk) > self.MAX_BODY:
                    body.clear()
                    overflow = True
                else:
                    body.extend(chunk)
            if message.get('more_body',False):
                return
            invalid_envelope = overflow
            if not overflow:
                try:
                    data = json.loads(body)
                    invalid_envelope = (isinstance(data,dict) and isinstance(data.get('error'),dict)
                        and data['error'].get('code') == -32602)
                except (ValueError,UnicodeError):
                    pass
            if invalid_envelope:
                # This SDK uses -32602 only for raw envelope validation at HTTP400.
                # Do not echo its ValidationError, which contains request values.
                await JSONResponse({'jsonrpc':'2.0','id':None,'error':{'code':-32600,'message':'Invalid Request'}},
                    status_code=400)(scope,receive,send)
            else:
                await send(pending)
                await send({'type':'http.response.body','body':bytes(body),'more_body':False})

        token = wire_arguments.set(exact_arguments)
        try:
            await self.app(scope,receive,checked_send)
        finally:
            wire_arguments.reset(token)

    @staticmethod
    async def error(scope,receive,send,code,message):
        await JSONResponse({'jsonrpc':'2.0','id':None,'error':{'code':code,'message':message}},
            status_code=400)(scope,receive,send)


def create_http_app(settings:MCPSettings,api:ReadAPI | None = None, *, clock=time.monotonic):
    settings.validate()
    server = create_server(api or ReadAPI.load(settings.api_credentials),
        tool_calls_per_minute=settings.tool_calls_per_minute,clock=clock)
    app = server.streamable_http_app(stateless_http=True,json_response=True,max_request_body_size=131072,
        transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=True,
            allowed_hosts=[f'{settings.host}:{settings.port}'],allowed_origins=[f'https://{settings.host}:{settings.port}']),host=settings.host)
    return MCPAccessMiddleware(MCPProtocolErrors(app),settings,post_only=True)


def serve_remote():
    import uvicorn
    settings = MCPSettings.load()
    logging.basicConfig(level=logging.INFO,format='%(message)s')
    # No proxy headers: the gateway authorizes the actual TCP peer and TLS scheme.
    uvicorn.run(create_http_app(settings),host=settings.host,port=settings.port,
                ssl_certfile=str(settings.certificate),ssl_keyfile=str(settings.private_key),ssl_version=ssl.PROTOCOL_TLS_SERVER,
                proxy_headers=False,access_log=False,limit_concurrency=16)
