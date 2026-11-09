"""Read-only daily report with explicit local/LAN boundaries; never a source DB."""
from __future__ import annotations

from contextlib import ExitStack
from collections import OrderedDict
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from hashlib import sha256
from ipaddress import IPv4Address, IPv4Network, ip_address, ip_network
import json
import logging
import os
from pathlib import Path
import re
import socket
import time
from urllib.parse import urlsplit

from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse, PlainTextResponse
from starlette.routing import Route

from .config import ROOT
from .capabilities import CAPABILITIES
from .time_rules import SHANGHAI

HOST = '127.0.0.1'
PORT = 3030
ANALYSIS = ROOT / '.runtime/daily-reports/2026-10-29/report.json'
REPORTS = ROOT / '.runtime/daily-reports'
ASSETS = {name: ROOT / 'assets' / name for name in ('daily-board.html', 'daily-board.css', 'daily-board.js', 'echarts.min.js')}
logger = logging.getLogger('insights.daily_board')
LOCAL_OPERATOR_PERMISSIONS = frozenset({'insights.daily_report.read', 'insights.attachments.read',
                                        'insights.attachments.logs.export'})
PRIVATE_NETWORKS = tuple(ip_network(value) for value in ('10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16'))
DOCUMENT_CSP = ("default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data:; media-src 'self'; frame-src 'self'; object-src 'none'; base-uri 'none'")
FILE_CSP = "default-src 'none'; sandbox"
_DNS_HOST = re.compile(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*')


def canonicalize_frame_ancestor(value: str) -> str:
    """Serialize one browser origin. Default ports fold; every other port stays exact."""
    if not isinstance(value, str) or not value or any(character.isspace() for character in value) or '*' in value:
        raise ValueError(f'invalid frame ancestor origin: {value!r}; expected an exact http or https origin with no wildcard')
    try:
        parts = urlsplit(value)
        port = parts.port
    except ValueError as error:
        raise ValueError(f'invalid frame ancestor origin: {value!r}; expected an exact http or https origin') from error
    if (parts.scheme not in {'http', 'https'} or parts.username or parts.password or parts.path
            or parts.query or parts.fragment or not parts.hostname or parts.hostname.endswith('.')):
        raise ValueError(f'invalid frame ancestor origin: {value!r}; path, query, fragment, userinfo, and wildcards are not allowed')
    try:
        parsed = ip_address(parts.hostname)
    except ValueError:
        if _DNS_HOST.fullmatch(parts.hostname) is None:
            raise ValueError(f'invalid frame ancestor origin: {value!r}; host must be an exact IPv4 address or DNS name') from None
        host = parts.hostname.lower()
    else:
        if not isinstance(parsed, IPv4Address):
            raise ValueError(f'invalid frame ancestor origin: {value!r}; host must be an exact IPv4 address or DNS name')
        host = str(parsed)
    default = 443 if parts.scheme == 'https' else 80
    if port is None:
        port = default
    if not 1 <= port <= 65535:
        raise ValueError(f'invalid frame ancestor origin: {value!r}; port must be an exact integer from 1 to 65535')
    if port == default:
        return f'{parts.scheme}://{host}'
    return f'{parts.scheme}://{host}:{port}'


@dataclass(frozen=True)
class BoardNetwork:
    """An explicit NIC address and trusted read-only audience; no proxy identity."""
    lan_host: str | None = None
    allowed_networks: tuple[str, ...] = ()
    frame_ancestor_origins: tuple[str, ...] = ()

    def __post_init__(self):
        if not isinstance(self.allowed_networks, tuple):
            raise ValueError('allowed_networks must be an immutable tuple')
        if not isinstance(self.frame_ancestor_origins, tuple):
            raise ValueError('frame_ancestor_origins must be an immutable tuple')
        canonical = tuple(canonicalize_frame_ancestor(value) for value in self.frame_ancestor_origins)
        if len(set(canonical)) != len(canonical):
            raise ValueError('frame ancestor origins must be unique')
        object.__setattr__(self, 'frame_ancestor_origins', canonical)
        if self.lan_host is None:
            if self.allowed_networks:
                raise ValueError('LAN networks require a LAN bind address')
            return
        host = ip_address(self.lan_host)
        if not isinstance(host, IPv4Address) or not any(host in net for net in PRIVATE_NETWORKS):
            raise ValueError('lan_host must be an explicit RFC1918 IPv4 address')
        if str(host) != self.lan_host or not self.allowed_networks:
            raise ValueError('LAN address and audience must be explicit')
        networks = self.networks
        if len(set(networks)) != len(networks) or not any(host in net for net in networks):
            raise ValueError('LAN audience must contain the bind address and have no duplicates')

    @property
    def networks(self):
        networks = tuple(ip_network(value, strict=True) for value in self.allowed_networks)
        if any(not isinstance(net, IPv4Network) or not any(net.subnet_of(block) for block in PRIVATE_NETWORKS)
               for net in networks):
            raise ValueError('LAN audience must stay within RFC1918 IPv4 ranges')
        return networks

    @property
    def bind_hosts(self):
        return (HOST, self.lan_host) if self.lan_host else (HOST,)

    def identity(self, peer: str, host: str, origin: str | None):
        local_hosts = {f'{HOST}:{PORT}', f'localhost:{PORT}'}
        lan_host = f'{self.lan_host}:{PORT}' if self.lan_host else None
        if host not in local_hosts | ({lan_host} if lan_host else set()):
            return None
        if not self.origin_permitted(host, origin):
            return None
        try:
            address = ip_address(peer)
        except ValueError:
            return None
        if peer in {HOST, '::1'}:
            return 'local-operator'
        if (lan_host and host == lan_host and isinstance(address, IPv4Address)
                and any(address in net for net in self.networks)):
            return 'lan-reader'
        return None

    def origin_permitted(self, host: str, origin: str | None) -> bool:
        if origin is None or origin == 'http://' + host:
            return True
        try:
            return canonicalize_frame_ancestor(origin) in self.frame_ancestor_origins
        except ValueError:
            return False

    def document_csp(self) -> str:
        ancestors = ' '.join(self.frame_ancestor_origins) if self.frame_ancestor_origins else "'none'"
        return f'{DOCUMENT_CSP}; frame-ancestors {ancestors}'

    @classmethod
    def load(cls, path: Path | None = None):
        path = path if path is not None else ROOT / '.secrets/daily-board.json'
        if not path.exists():
            return cls()
        value = json.loads(path.read_text('utf-8'))
        allowed = {'lan_host', 'allowed_networks', 'frame_ancestor_origins'}
        if not isinstance(value, dict) or not {'lan_host', 'allowed_networks'} <= set(value) <= allowed:
            raise ValueError('daily-board.json accepts lan_host, allowed_networks, and optional frame_ancestor_origins')
        networks = value['allowed_networks']
        origins = value.get('frame_ancestor_origins', [])
        if (not isinstance(value['lan_host'], str) or not isinstance(networks, list)
                or not all(isinstance(net, str) for net in networks)
                or not isinstance(origins, list) or not all(isinstance(origin, str) for origin in origins)):
            raise ValueError('daily-board.json has invalid address types')
        return cls(value['lan_host'], tuple(networks), tuple(origins))


def archive_feature():
    if CAPABILITIES['daily_log_archive']['permission'] not in LOCAL_OPERATOR_PERMISSIONS:
        return {'enabled': False, 'disabled_reason': '本机操作者未获日志批量下载权限'}
    enabled = os.environ.get('INSIGHTS_DAILY_LOG_ARCHIVE_ENABLED', '1') == '1'
    return {'enabled': enabled, 'disabled_reason': '' if enabled else '日志批量下载已由管理员关闭'}


class ReportStore:
    def __init__(self, path: Path):
        self.path, self.stamp, self.report, self.index = path, None, None, {}
        self.version = ''

    def load(self):
        stat = self.path.stat()
        stamp = (stat.st_mtime_ns, stat.st_size)
        if stamp != self.stamp:
            raw = self.path.read_bytes()
            report = json.loads(raw)
            records = report['records']
            if report['coverage']['expected'] != len(records) or any(not r.get('summary') for r in records):
                raise ValueError('report coverage is incomplete')
            if len({r['id'] for r in records}) != len(records):
                raise ValueError('duplicate report mail')
            self.report = report
            self.index = {r['id']: r for r in records}
            self.version = sha256(raw).hexdigest()
            self.stamp = stamp
        return self.report

    def overview(self):
        report = self.load()
        return {**report, 'report_sha256': self.version, 'records': [
            {**{k: v for k, v in record.items() if k not in {'body', 'body_zh', 'source_summary', 'metadata', 'uid'}},
             'uid': {k: v for k, v in record.get('uid', {}).items() if k in {'value', 'state', 'uid_roles'}}}
            for record in report['records']]}


def business_today():
    return datetime.now(SHANGHAI).date().isoformat()


def default_report_date():
    return (date.fromisoformat(business_today()) - timedelta(days=1)).isoformat()


def checked_date(value: str):
    if not isinstance(value, str) or re.fullmatch(r'\d{4}-\d{2}-\d{2}', value) is None:
        raise HTTPException(400, 'INVALID_REPORT_DATE')
    try:
        date.fromisoformat(value)
    except ValueError:
        raise HTTPException(400, 'INVALID_REPORT_DATE') from None
    return value


class ReportCatalog:
    """Date-scoped, bounded file cache. No live query or latest-report fallback."""
    def __init__(self, root: Path, fixed_path: Path | None = None):
        self.root, self.fixed_path = root.resolve(), fixed_path
        self.stores = OrderedDict()

    def available_dates(self):
        if self.fixed_path is not None:
            return [self.fixed_path.parent.name] if re.fullmatch(r'\d{4}-\d{2}-\d{2}', self.fixed_path.parent.name) else []
        if not self.root.is_dir():
            return []
        result = []
        for folder in self.root.iterdir():
            if re.fullmatch(r'\d{4}-\d{2}-\d{2}', folder.name) and folder.is_dir():
                try:
                    checked_date(folder.name)
                    path = folder / 'report.json'
                    if path.is_file() and path.resolve().parent == self.root / folder.name:
                        result.append(folder.name)
                except HTTPException:
                    continue
        return sorted(result, reverse=True)

    def select(self, request: Request):
        values = request.query_params.getlist('date')
        if len(values) > 1:
            raise HTTPException(400, 'INVALID_REPORT_DATE')
        default = self.fixed_path.parent.name if self.fixed_path and re.fullmatch(r'\d{4}-\d{2}-\d{2}', self.fixed_path.parent.name) else default_report_date()
        day = checked_date(values[0] if values else default)
        path = self.fixed_path if self.fixed_path is not None else self.root / day / 'report.json'
        if self.fixed_path is None and path.resolve().parent != self.root / day:
            raise HTTPException(400, 'INVALID_REPORT_DATE')
        if not path.is_file():
            if self.fixed_path is not None:
                raise FileNotFoundError('explicit report path is unavailable')
            return day, None
        store = self.stores.pop(day, None) or ReportStore(path)
        self.stores[day] = store
        while len(self.stores) > 3:
            self.stores.popitem(last=False)
        report = store.load()
        if report.get('business_date') not in (None, day) or self.fixed_path is None and report.get('business_date') != day:
            raise ValueError('report date does not match its namespace')
        return day, store


def create_app(report_path: Path | None = None, *, network: BoardNetwork | None = None,
               reports_root: Path = REPORTS) -> Starlette:
    network = network if network is not None else BoardNetwork()
    catalog = ReportCatalog(reports_root, report_path)

    def ready_store(request):
        _, store = catalog.select(request)
        if store is None:
            raise HTTPException(404, 'REPORT_NOT_GENERATED')
        version = request.query_params.get('v')
        if version is not None and version != store.version:
            raise HTTPException(409, 'REPORT_UPDATED')
        return store

    async def homepage(request: Request):
        return FileResponse(ASSETS['daily-board.html'], media_type='text/html')

    async def overview(request: Request):
        day, store = catalog.select(request)
        meta = {'business_date': day, 'today': business_today(), 'default_date': default_report_date(), 'timezone': 'Asia/Shanghai',
                'available_dates': catalog.available_dates()}
        if store is None:
            return JSONResponse({**meta, 'report_status': 'not_generated'})
        return JSONResponse({**store.overview(), **meta, 'report_status': 'generated',
                             'features': {'daily_log_archive': archive_feature()}})

    async def mail(request: Request):
        store = ready_store(request)
        record = store.index.get(request.path_params['mail_pk'])
        if not record:
            return JSONResponse({'error': 'MAIL_NOT_IN_REPORT'}, status_code=404)
        return JSONResponse({**record, 'report_sha256': store.version})

    async def asset(request: Request):
        name = request.path_params['name']
        path = ASSETS.get(name)
        if path is None or not path.is_file():
            return PlainTextResponse('NOT_FOUND', status_code=404)
        return FileResponse(path, media_type='text/javascript' if name.endswith('.js') else 'text/css')

    async def deliver(request: Request, *, preview=False):
        store = ready_store(request)
        report = store.load()
        directory = store.path.parent / 'attachments'
        key = request.path_params['file_id']
        item = next((f for r in report['records'] for f in r['files'] if f['id'] == key), None)
        if not key.isdigit() or item is None or not item['ready']:
            return JSONResponse({'error': 'FILE_NOT_AVAILABLE'}, status_code=404)
        original = directory / (key + '.bin')
        if not original.is_file():
            return JSONResponse({'error': 'FILE_NOT_AVAILABLE'}, status_code=404)
        if preview:
            if item['preview_type'] == 'image':
                path, media = directory / (key + '.jpg'), 'image/jpeg'
            elif item['preview_type'] == 'pdf' and item.get('preview_image'):
                path, media = directory / (key + '.pdf.jpg'), 'image/jpeg'
            elif item['preview_type'] == 'text':
                path, media = directory / (key + '.txt'), 'text/plain; charset=utf-8'
            else:
                return JSONResponse({'error': 'PREVIEW_FORMAT_UNSUPPORTED'}, status_code=415)
            if not path.is_file():
                return JSONResponse({'error': 'PREVIEW_NOT_AVAILABLE'}, status_code=404)
            return FileResponse(path, media_type=media)
        inline = item['preview_type'] in {'video', 'pdf'} and request.query_params.get('download') != '1'
        media = (item.get('detected_content_type') or item['content_type']) if inline else 'application/octet-stream'
        response = FileResponse(original, media_type=media, filename=item['name'], content_disposition_type='inline' if inline else 'attachment')
        response.headers['Content-Security-Policy'] = FILE_CSP
        return response

    async def attachment(request: Request):
        return await deliver(request)

    async def file_preview(request: Request):
        return await deliver(request, preview=True)

    async def log_archive(request: Request):
        if os.environ.get('INSIGHTS_DAILY_LOG_ARCHIVE_ENABLED', '1') != '1':
            return JSONResponse({'error': 'FEATURE_DISABLED', 'message': '日志批量下载已关闭'}, status_code=503)
        store = ready_store(request)
        report = store.load()
        if request.query_params.get('v') != store.version:
            return JSONResponse({'error': 'REPORT_UPDATED', 'message': '请刷新日报后重新下载日志'}, status_code=409)
        key = request.path_params['archive_id']
        item = (report.get('log_archives') or {}).get(key)
        if re.fullmatch('[a-f0-9]{64}', key) is None or not item or item.get('status') != 'ready':
            return JSONResponse({'error': 'LOG_ARCHIVE_NOT_IN_REPORT'}, status_code=404)
        folder = store.path.parent / 'archives'
        path = folder / (key + '.zip')
        if not path.is_file() or path.resolve().parent != folder.resolve():
            return JSONResponse({'error': 'LOG_ARCHIVE_NOT_AVAILABLE'}, status_code=404)
        response = FileResponse(path, media_type='application/zip', filename=item['filename'])
        response.headers['X-Log-Count'] = str(item['file_count'])
        return response

    async def request_error(request, exception):
        return JSONResponse({'error': exception.detail}, status_code=exception.status_code)

    app = Starlette(exception_handlers={HTTPException: request_error}, routes=[Route('/', homepage), Route('/data.json', overview),
        Route('/mail/{mail_pk}', mail), Route('/assets/{name}', asset),
        Route('/log-archive/{archive_id}', log_archive),
        Route('/file/{file_id}/preview', file_preview), Route('/file/{file_id}', attachment)])

    async def boundary(request: Request, call_next):
        started = time.monotonic()
        client = request.client.host if request.client else ''
        host = request.headers.get('host', '').lower()
        origin = request.headers.get('origin')
        identity = network.identity(client, host, origin)
        allowed = identity is not None
        if not allowed:
            response = JSONResponse({'error': 'NETWORK_ACCESS_DENIED'}, status_code=403)
        elif request.method not in {'GET', 'HEAD'}:
            response = JSONResponse({'error': 'READ_ONLY'}, status_code=405)
        elif os.environ.get('INSIGHTS_DAILY_BOARD_ENABLED', '1') != '1':
            response = JSONResponse({'error': 'FEATURE_DISABLED'}, status_code=503)
        elif CAPABILITIES['daily_board']['permission'] not in LOCAL_OPERATOR_PERMISSIONS:
            response = JSONResponse({'error': 'PERMISSION_DENIED'}, status_code=403)
        elif request.url.path.startswith('/file/') and CAPABILITIES['attachment_preview']['permission'] not in LOCAL_OPERATOR_PERMISSIONS:
            response = JSONResponse({'error': 'PERMISSION_DENIED'}, status_code=403)
        elif request.url.path.startswith('/log-archive/') and CAPABILITIES['daily_log_archive']['permission'] not in LOCAL_OPERATOR_PERMISSIONS:
            response = JSONResponse({'error': 'PERMISSION_DENIED'}, status_code=403)
        else:
            try:
                response = await call_next(request)
            except (OSError, ValueError, KeyError):
                response = JSONResponse({'error': 'REPORT_UNAVAILABLE', 'message': '日报读取模型尚未生成或校验失败，请检查本地报告。'}, status_code=503)
        response.headers['Cache-Control'] = 'no-store'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Referrer-Policy'] = 'no-referrer'
        # Framing is decided only by frame-ancestors. CORP stays same-origin, and no
        # CORS header is added: a listed parent may display the document, not read it.
        response.headers['Cross-Origin-Resource-Policy'] = 'same-origin'
        response.headers.setdefault('Content-Security-Policy', network.document_csp())
        archive_request = request.url.path.startswith('/log-archive/')
        action = 'log-archive.read' if archive_request else 'attachment.read' if request.url.path.startswith('/file/') else 'daily-report.read'
        resource = request.url.path.rsplit('/', 1)[-1] if archive_request else None
        day = request.query_params.get('date')
        logger.info(json.dumps({'action': action, 'business_date': day if day and re.fullmatch(r'\d{4}-\d{2}-\d{2}', day) else None, 'resource': resource if resource and re.fullmatch('[a-f0-9]{64}', resource) else None, 'identity': identity or 'unauthorized', 'peer': client,
                                'status': response.status_code, 'duration_ms': round((time.monotonic() - started) * 1000)}))
        return response

    app.add_middleware(BaseHTTPMiddleware, dispatch=boundary)
    return app


def serve_board():
    import uvicorn
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    network = BoardNetwork.load()
    # Bind every requested address before serving any request. A partial failure
    # closes all sockets, so an unintended subset cannot silently stay online.
    with ExitStack() as stack:
        sockets = []
        for host in network.bind_hosts:
            listener = stack.enter_context(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
            if hasattr(socket, 'SO_EXCLUSIVEADDRUSE'):
                listener.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
            else:
                listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind((host, PORT))
            listener.listen(128)
            sockets.append(listener)
        logger.info(json.dumps({'event': 'daily-board.listening', 'hosts': list(network.bind_hosts),
                                'port': PORT, 'allowed_networks': list(network.allowed_networks),
                                'frame_ancestor_origins': list(network.frame_ancestor_origins)}))
        config = uvicorn.Config(create_app(network=network), access_log=False, proxy_headers=False)
        uvicorn.Server(config).run(sockets=sockets)
