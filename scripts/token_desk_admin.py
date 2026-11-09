"""Provision/reset the one portal owner from the protected server OS account."""
import argparse
import getpass
import json
from pathlib import Path
import secrets
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from insights.cli import protect_directory
from insights.mcp_tokens import write_object
from insights.token_desk import ADMIN_PATH, configure_admin


def main():
    parser = argparse.ArgumentParser(description='配置唯一令牌发放管理员；口令不会打印')
    parser.add_argument('--username', default='owner')
    parser.add_argument('--reset', action='store_true', help='替换凭据并使旧管理会话失效')
    parser.add_argument('--interactive', action='store_true', help='交互输入至少16字符口令')
    args = parser.parse_args()
    if ADMIN_PATH.exists() and not args.reset:
        parser.error('管理员已存在；只有需要更换凭据时才显式使用 --reset')
    protect_directory(ROOT/'.secrets')
    initial = ROOT/'.secrets/token-desk-initial.json'
    password = getpass.getpass('管理员新口令（不回显）: ') if args.interactive else secrets.token_urlsafe(32)
    configure_admin(args.username, password)
    if args.interactive:
        initial.unlink(missing_ok=True)
    else:
        write_object(initial, {'username': args.username, 'password': password,
            'usage': '仅供所有者读取。可用本脚本 --reset --interactive 换成自定口令；不向MCP接收人分发。'})
    print(json.dumps({'status':'CONFIGURED','username':args.username,'initial_credential_file':str(initial) if not args.interactive else None,'password_printed':False},ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
