"""Python 3.11+ standard-library MCP 2025-11-25 JSON-response client."""
import argparse
import json
from pathlib import Path
import ssl
import sys
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, HTTPSHandler, ProxyHandler, Request, build_opener


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class ProtocolClient:
    def __init__(self, config_path):
        self.path = Path(config_path).resolve()
        self.config = json.loads(self.path.read_text(encoding='utf-8-sig'))
        parsed = urlsplit(self.config['url'])
        if (parsed.scheme != 'https' or not parsed.hostname or parsed.path != '/mcp'
                or parsed.username or parsed.password or parsed.query or parsed.fragment):
            raise ValueError('HTTPS /mcp URL required; no embedded credentials or query')
        token = self.config['bearer_token']
        if not isinstance(token, str) or len(token) < 32 or token.startswith('REPLACE_'):
            raise ValueError('configure your own issued bearer token first')
        ca = Path(self.config['ca_file'])
        if not ca.is_absolute():
            ca = self.path.parent / ca
        context = ssl.create_default_context(cafile=str(ca))
        self.opener = build_opener(ProxyHandler({}), NoRedirect(), HTTPSHandler(context=context))
        self.headers = {'Authorization':'Bearer ' + token, 'Content-Type':'application/json',
                        'Accept':'application/json, text/event-stream'}
        self.sequence = 0

    def rpc(self, method, params=None, notification=False):
        self.sequence += 1
        message = {'jsonrpc':'2.0', 'method':method}
        if not notification:
            message['id'] = self.sequence
        if params is not None:
            message['params'] = params
        request = Request(self.config['url'], data=json.dumps(message).encode(), headers=self.headers)
        with self.opener.open(request, timeout=35) as response:
            if notification:
                if response.status != 202:
                    raise RuntimeError('notification must be accepted with HTTP 202')
                return None
            if response.headers.get_content_type() != 'application/json':
                raise RuntimeError('this example requires the server JSON response mode')
            data = json.load(response)
        if data.get('id') != self.sequence or data.get('jsonrpc') != '2.0':
            raise RuntimeError('invalid JSON-RPC response envelope')
        if 'error' in data:
            raise RuntimeError('JSON-RPC error code: ' + str(data['error'].get('code')))
        return data['result']

    def initialize(self):
        result = self.rpc('initialize', {'protocolVersion':'2025-11-25','capabilities':{},
            'clientInfo':{'name':'complaint-insights-stdlib','version':'1.0.0'}})
        if result['protocolVersion'] != '2025-11-25':
            raise RuntimeError('unsupported negotiated version')
        self.headers['MCP-Protocol-Version'] = result['protocolVersion']
        self.rpc('notifications/initialized', notification=True)
        return result

    def call(self, name, arguments=None):
        arguments = dict(arguments or {})
        if name != 'get_data_guide':
            arguments.setdefault('source_id', self.config.get('source_id', 'production-ai-customer'))
        result = self.rpc('tools/call', {'name':name, 'arguments':arguments})
        if result.get('isError'):
            raise RuntimeError('MCP tool returned isError=true; inspect tool arguments and request ID')
        if 'structuredContent' in result:
            return result['structuredContent']
        return json.loads(next(item['text'] for item in result['content'] if item['type'] == 'text'))


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description='零额外依赖的原生MCP协议示例')
    parser.add_argument('tool', nargs='?', default='get_sync_status')
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--arguments-file', type=Path)
    parser.add_argument('--list-tools', action='store_true')
    args = parser.parse_args()
    try:
        client = ProtocolClient(args.config)
        client.initialize()
        arguments = json.loads(args.arguments_file.read_text(encoding='utf-8-sig')) if args.arguments_file else {}
        result = client.rpc('tools/list', {}) if args.list_tools else client.call(args.tool, arguments)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as error:
        print(json.dumps({'status':'MCP_REQUEST_FAILED','error_type':type(error).__name__,
            'check':'核对内网、CA、本人令牌、参数和服务状态；不关闭证书校验。'},ensure_ascii=False),file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
