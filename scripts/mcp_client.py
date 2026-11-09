"""Portable SDK client with explicit source selection and version-safe pagination."""
import argparse
import asyncio
import csv
import getpass
import json
import os
from pathlib import Path
import re
import ssl
import subprocess
import sys
from urllib.parse import urlsplit


def configure(config_path: Path):
    if config_path.exists():
        raise ValueError('配置已存在，请使用新的受限文件路径，避免覆盖原凭据')
    token = getpass.getpass('请输入管理员发给你本人的 MCP token（不回显）: ').strip()
    if len(token) < 32 or not token.isascii() or any(char.isspace() for char in token):
        raise ValueError('令牌格式无效')
    template = json.loads((Path(__file__).parent/'mcp-client.example.json').read_text(encoding='utf-8'))
    template['bearer_token'] = token
    config_path.parent.mkdir(parents=True, exist_ok=True)
    # Protect the empty new file before the first credential byte is written.
    descriptor = os.open(config_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    stream = None
    try:
        stream = os.fdopen(descriptor, 'w', encoding='utf-8')
        with stream:
            if os.name == 'nt':
                record = subprocess.check_output(['whoami','/user','/fo','csv','/nh'],text=True).strip()
                sid = next(csv.reader([record]))[-1]
                subprocess.run(['icacls',str(config_path),'/inheritance:r','/grant:r',f'*{sid}:F','*S-1-5-18:F'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            else:
                config_path.chmod(0o600)
            json.dump(template, stream, ensure_ascii=False, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
    except BaseException:
        if stream is None:
            os.close(descriptor)
        config_path.unlink(missing_ok=True)
        raise
    return {'status':'CONFIGURED','source_id':template['source_id'],'credential_printed':False}


async def query(config_path: Path, tool: str, arguments: dict, list_tools: bool = False,
                all_pages: bool = False, max_pages: int = 10000):
    import httpx2
    from mcp import Client
    from mcp.client.streamable_http import streamable_http_client
    config = json.loads(config_path.read_text(encoding='utf-8-sig'))
    parsed = urlsplit(config['url'])
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or parsed.path != '/mcp' or parsed.query or parsed.fragment:
        raise ValueError('HTTPS /mcp URL without embedded credentials/query is required')
    token = config['bearer_token']
    if not isinstance(token, str) or len(token) < 32 or token.startswith('REPLACE_'):
        raise ValueError('请先配置本人令牌')
    arguments = dict(arguments)
    if tool != 'get_data_guide' and not list_tools:
        source = arguments.get('source_id') or config.get('source_id', 'production-ai-customer')
        if not re.fullmatch(r'[a-z][a-z0-9_-]{1,63}', source):
            raise ValueError('无效来源')
        arguments['source_id'] = source
    if all_pages and tool not in {'list_taxonomy','query_daily_statistics','list_mails','get_report_context','list_source_records'}:
        raise ValueError('--all-pages仅用于分页工具')
    ca_path = Path(config['ca_file'])
    if not ca_path.is_absolute():
        ca_path = config_path.parent / ca_path
    context = ssl.create_default_context(cafile=str(ca_path))
    async with httpx2.AsyncClient(verify=context, headers={'Authorization':'Bearer '+token}, trust_env=False,
                                follow_redirects=False, timeout=35) as http:
        async with Client(streamable_http_client(config['url'], http_client=http), read_timeout_seconds=40) as client:
            if list_tools:
                result = await client.list_tools()
                return {'tools':[item.model_dump(mode='json',by_alias=True,exclude_none=True) for item in result.tools]}
            pages, seen = [], set()
            version = None
            for _ in range(max_pages if all_pages else 1):
                result = await client.call_tool(tool, arguments)
                if result.is_error:
                    return {'is_error':True, 'content':[item.model_dump(mode='json',by_alias=True) for item in result.content]}
                data = result.structured_content
                if not all_pages:
                    return data
                current = (data.get('meta') or {}).get('data_version')
                if version is not None and current != version:
                    raise RuntimeError('分页数据版本变化，结果已丢弃，请从首页重新查询')
                version = current
                pages.append(data)
                cursor = data.get('next_cursor')
                if cursor is None:
                    return {'pages':pages,'page_count':len(pages),'data_version':version,'complete':True}
                if cursor in seen:
                    raise RuntimeError('服务返回重复游标，结果已丢弃')
                seen.add(cursor)
                arguments['cursor'] = cursor
            raise RuntimeError('超过max-pages，未输出不完整汇总；缩小范围或提高页数上限')


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description='内网HTTPS MCP客诉只读查询')
    parser.add_argument('tool', nargs='?', default='get_sync_status')
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--configure', action='store_true', help='交互保存本人令牌，不回显')
    parser.add_argument('--arguments-file', type=Path)
    parser.add_argument('--list-tools', action='store_true')
    parser.add_argument('--all-pages', action='store_true', help='遍历next_cursor直到null，输出完整pages')
    parser.add_argument('--max-pages', type=int, default=10000)
    args = parser.parse_args()
    try:
        if not 1 <= args.max_pages <= 100000:
            raise ValueError('max-pages必须在1至100000之间')
        arguments = json.loads(args.arguments_file.read_text(encoding='utf-8-sig')) if args.arguments_file else {}
        result = configure(args.config.resolve()) if args.configure else asyncio.run(query(args.config.resolve(), args.tool, arguments, args.list_tools, args.all_pages, args.max_pages))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result.get('is_error') else 0
    except Exception as error:
        print(json.dumps({'status':'MCP_CONNECTION_FAILED','error_type':type(error).__name__,
            'check':'检查内网地址、CA文件、本人令牌、参数和服务状态；不关闭证书校验。'},ensure_ascii=False),file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
