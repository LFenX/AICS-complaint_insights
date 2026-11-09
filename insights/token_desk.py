"""Intranet HTTPS documentation portal and authenticated owner-only token desk."""
from __future__ import annotations
import asyncio
from dataclasses import dataclass
import hashlib
from html import escape
from ipaddress import ip_address, ip_network
import json
import logging
from pathlib import Path
import secrets
import ssl
import time
import uuid
from urllib.parse import parse_qs

from starlette.applications import Starlette
from starlette.concurrency import run_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse, Response
from starlette.routing import Route

from .config import ROOT
from .mcp_http import MCPSettings
from .mcp_tokens import (SERVER_PATH, REGISTRY_PATH, IDENTITY, issue_token, revoke_token,
                         token_inventory, read_object, write_object)

PORT = 3029
ADMIN_PATH = ROOT / '.secrets/token-desk-admin.json'
PUBLIC_PATH = ROOT / '.runtime/mcp-portal-public'
COOKIE = '__Host-insights-admin'
PREAUTH = '__Host-insights-login'
ITERATIONS = 600000
logger = logging.getLogger('insights.token_desk')


@dataclass(frozen=True)
class DeskSettings:
    host: str
    port: int = PORT
    allowed_networks: tuple[str, ...] = ('10.8.0.0/16',)

    @property
    def origin(self):
        return f'https://{self.host}:{self.port}'


def configure_admin(username: str, password: str, path: Path = ADMIN_PATH) -> None:
    if not IDENTITY.fullmatch(username) or not 16 <= len(password) <= 256:
        raise ValueError('管理员名称格式无效，或口令长度不在16至256字符范围')
    salt = secrets.token_bytes(32)
    digest = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, ITERATIONS)
    write_object(path, {'username': username, 'salt': salt.hex(), 'digest': digest.hex(),
                        'iterations': ITERATIONS, 'algorithm': 'pbkdf2-sha256'})


def _admin(path: Path) -> tuple[dict, str]:
    data = read_object(path)
    if (data.get('algorithm') != 'pbkdf2-sha256' or data.get('iterations') != ITERATIONS
            or not isinstance(data.get('username'), str) or not IDENTITY.fullmatch(data['username'])
            or len(bytes.fromhex(data['salt'])) != 32 or len(bytes.fromhex(data['digest'])) != 32):
        raise ValueError('invalid admin credential store')
    # Bind the verified credentials and session version to the same read. An
    # atomic credential replacement between two reads must not bless old data.
    snapshot = json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')
    return data, hashlib.sha256(snapshot).hexdigest()


def _password_ok(data: dict, username: str, password: str) -> bool:
    value = hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(data['salt']), ITERATIONS)
    return (secrets.compare_digest(value.hex(), data['digest'])
            & secrets.compare_digest(username.encode(), data['username'].encode()))


NAVIGATION = (('/', '接入中心', 'home'), ('/guide', '使用指南', 'guide'),
              ('/guide#tools', '工具参考', 'tools'), ('/admin', '令牌管理', 'admin'))
TOOL_GROUPS = (
    ('先了解', '首次接入先调用，确认口径与数据时效。',
     (('get_data_guide', '数据口径与工具选择'), ('get_sync_status', '来源与同步状态'), ('get_capabilities', '能力与权限目录'))),
    ('看统计', '按日期与三级分类取完整汇总。',
     (('list_taxonomy', '分类目录'), ('query_daily_statistics', '按日、按分类统计'))),
    ('查邮件', '按需分页读取邮件、正文与 AI 证据。',
     (('list_mails', '邮件列表与 AI 摘要'), ('get_mail_detail', '单封邮件原文与证据'), ('get_report_context', '周期报告上下文'))),
    ('追源头', '十四类源表的原始副本，用于对账与追溯。',
     (('list_source_tables', '源表目录'), ('list_source_records', '分页源记录'), ('get_source_record', '单条源记录'))),
)


def _shell(title: str, body: str, active: str = '') -> str:
    links = ''.join('<a href="' + href + '"' + (' aria-current="page"' if key == active else '') + '>' + label + '</a>'
                    for href, label, key in NAVIGATION)
    return '''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark"><title>''' + escape(title) + ''' · 客诉 MCP</title>
<link rel="stylesheet" href="/assets/token-desk.css"><script src="/assets/token-desk.js" defer></script></head>
<body><a class="skip" href="#main">跳到正文</a><header class="topbar"><div class="topbar-inner"><a class="brand" href="/"><span class="brand-mark">CI</span>客诉 MCP <small>接入中心</small></a>
<nav class="nav" aria-label="主导航">''' + links + '''</nav></div></header>
<main id="main">''' + body + '''</main><footer><div class="footer-inner"><span>Complaint Insights · 只读查询服务</span><span>内网 HTTPS · 令牌按人发放</span></div></footer></body></html>'''


def _hidden(csrf: str) -> str:
    return '<input type="hidden" name="csrf" value="' + escape(csrf) + '">'


def _alert(tone: str, title: str, text: str = '', role: str = 'status') -> str:
    return ('<div class="alert ' + tone + '" role="' + role + '"><div><strong>' + escape(title) + '</strong>'
            + ('<p>' + escape(text) + '</p>' if text else '') + '</div></div>')


def _status_page(title: str, text: str, status: int, *, action: tuple[str, str] = ('/', '返回接入中心'),
                 headers: dict | None = None, active: str = '') -> HTMLResponse:
    body = ('<div class="narrow wide"><section class="card status-page"><div class="code">HTTP ' + str(status) + '</div><h1>'
            + escape(title) + '</h1><p>' + escape(text) + '</p><div class="actions"><a class="button secondary" href="'
            + action[0] + '">' + escape(action[1]) + '</a></div></section></div>')
    return HTMLResponse(_shell(title, body, active), status_code=status, headers=headers)


def _homepage(settings: DeskSettings) -> str:
    endpoint = escape(f'https://{settings.host}:3037/mcp')
    groups = ''.join('<article class="tool-group"><h3>' + name + ' <small>' + str(len(tools)) + '</small></h3><p>' + text + '</p><ul>'
                     + ''.join('<li><code>' + tool + '</code><span>' + label + '</span></li>' for tool, label in tools)
                     + '</ul></article>' for name, text, tools in TOOL_GROUPS)
    return _shell('接入中心', '''<section class="hero-band"><div class="hero"><div>
<span class="pill"><span class="dot"></span>MCP 2025-11-25 · 11 个只读工具</span>
<h1>客诉数据，<br><span>一个 MCP 入口。</span></h1>
<p class="lead">在任意 MCP 客户端中查询分类统计、追溯邮件原文与 AI 证据。信任 CA、领取本人令牌，几分钟即可接入。</p>
<div class="actions"><a class="button" href="/guide#quickstart">开始接入</a><a class="button secondary" href="/downloads/mcp-client-kit.zip">下载客户端包</a></div>
<p class="hero-note">拿到链接不等于获得数据权限：查询需要管理员发给你本人的令牌，本页只提供说明与接入材料。</p></div>
<div class="window" role="group" aria-label="MCP 服务地址与客户端配置"><div class="window-bar"><i></i><i></i><i></i><span>mcp-client.json</span>
<button type="button" class="ghost" data-copy="''' + endpoint + '''">复制地址</button></div>
<pre class="snippet"><code>{
  <span class="k">"url"</span>: <span class="s">"''' + endpoint + '''"</span>,
  <span class="k">"ca_file"</span>: <span class="s">"mcp-ca.crt"</span>,
  <span class="k">"bearer_token"</span>: <span class="s">"REPLACE_WITH_YOUR_MCP_TOKEN"</span>,
  <span class="k">"source_id"</span>: <span class="s">"production-ai-customer"</span>
}</code></pre>
<dl><div><dt>传输</dt><dd>HTTPS · JSON-RPC</dd></div><div><dt>认证</dt><dd>按人发放 Bearer</dd></div><div><dt>数据</dt><dd>历史副本 · 已停采</dd></div></dl></div></div></section>
<section class="section"><div class="section-head"><div><span class="kicker">接入流程</span><h2>四步完成接入</h2><p>按顺序完成，每一步都对应指南中的一个章节。</p></div></div><ol class="timeline">
<li><h3>确认信任</h3><p>向管理员取得 CA 公钥并核对指纹，在本机信任该 CA，全程保持证书校验。</p><a href="/guide#tls">TLS 与证书 →</a></li>
<li><h3>领取本人令牌</h3><p>联系发放管理员取得独立令牌。不要共享，也不要用管理员口令调用 MCP。</p><a href="/guide#identity">身份与权限 →</a></li>
<li><h3>配置客户端</h3><p>下载不含凭据的客户端包，运行 configure 交互输入令牌，再列出工具。</p><a href="/guide#quickstart">快速开始 →</a></li>
<li><h3>选源并查询</h3><p>显式指定来源，先查同步状态，再按需求选择统计或明细工具。</p><a href="/guide#selection">工具选择 →</a></li></ol></section>
<section class="section"><div class="section-head"><div><span class="kicker">工具</span><h2>覆盖从统计到原文的全链路</h2><p>全部只读：无写入、无任意 SQL、无邮件发送。参数与返回结构见工具参考。</p></div><a class="button secondary small" href="/guide#tools">工具参考</a></div>
<div class="bento">''' + groups + '''</div></section>
<section class="section"><div class="section-head"><div><span class="kicker">下载</span><h2>接入材料</h2><p>同一份材料可发给所有接收人，均不含令牌。</p></div></div><div class="downloads">
<a class="download" href="/downloads/mcp-client-kit.zip"><span class="ext">ZIP</span><div><strong>客户端包</strong><span>Python 客户端、查询示例与离线指南</span></div></a>
<a class="download" href="/downloads/mcp-ca.crt"><span class="ext">CRT</span><div><strong>CA 公钥</strong><span>首次使用前请向管理员核对指纹</span></div></a>
<a class="download" href="/downloads/tools-schema.json"><span class="ext">JSON</span><div><strong>工具 Schema</strong><span>来自实际 tools/list 的原始定义</span></div></a>
<a class="download" href="/downloads/client-guide.md"><span class="ext">MD</span><div><strong>完整指南</strong><span>与在线使用指南内容一致</span></div></a></div></section>''', 'home')


def create_app(server_path: Path = SERVER_PATH, registry_path: Path = REGISTRY_PATH,
               admin_path: Path = ADMIN_PATH, *, settings: DeskSettings | None = None,
               public_path: Path = PUBLIC_PATH, clock=time.monotonic) -> Starlette:
    if settings is None:
        remote = MCPSettings.load(server_path)
        settings = DeskSettings(remote.host, allowed_networks=remote.allowed_networks)
    networks = tuple(ip_network(value, strict=True) for value in settings.allowed_networks)
    sessions: dict[str, dict] = {}
    challenges: dict[str, dict] = {}
    challenge_issues: dict[str, list[float]] = {}
    failures: dict[str, list[float]] = {}
    login_gate = asyncio.Semaphore(2)

    def audit(request: Request, action: str, status: str, identity: str | None = None):
        logger.info(json.dumps({'request_id': request.state.request_id, 'action': action,
            'admin': getattr(request.state, 'admin', None), 'target_identity': identity,
            'client_ip': request.client.host if request.client else None, 'status': status}, ensure_ascii=False))

    def session(request: Request):
        key = hashlib.sha256(request.cookies.get(COOKIE, '').encode()).hexdigest()
        item = sessions.get(key)
        if item is None:
            return None
        try:
            _, version = _admin(admin_path)
        except (OSError, ValueError, TypeError, KeyError, UnicodeError):
            version = ''
        now = clock()
        if now - item['last'] > 1200 or now - item['created'] > 28800 or version != item['version']:
            sessions.pop(key, None)
            return None
        item['last'] = now
        request.state.admin = item['username']
        return item

    async def form(request: Request):
        if request.headers.get('origin') != settings.origin:
            return None
        if request.headers.get('content-type', '').split(';', 1)[0] != 'application/x-www-form-urlencoded':
            return None
        body = bytearray()
        async for chunk in request.stream():
            body.extend(chunk)
            if len(body) > 4096:
                return None
        try:
            fields = parse_qs(body.decode('utf-8'), keep_blank_values=True, max_num_fields=8)
        except (ValueError, UnicodeError):
            return None
        if any(len(values) != 1 for values in fields.values()):
            return None
        return {key: values[0] for key, values in fields.items()}

    def csrf_ok(fields, expected):
        return fields is not None and secrets.compare_digest(fields.get('csrf', '').encode(), expected.encode())

    def expired():
        response = RedirectResponse('/admin/login', status_code=303)
        response.delete_cookie(COOKIE, path='/', secure=True, httponly=True, samesite='strict')
        return response

    def management(item, message='', token='', status=200, tone='error', draft=''):
        try:
            rows, metadata_available = token_inventory(server_path, registry_path)
        except (OSError, ValueError, UnicodeError):
            return _status_page('令牌配置不可用', '配置丢失或损坏，管理已停止。请服务器维护者检查受限配置，不能覆盖为新文件。', 503, active='admin')
        if not message and 'flash' in item:
            # Post/redirect/get feedback: shown on the next page view only.
            tone, message = item.pop('flash')
        hidden = _hidden(item['csrf'])
        historic = sum(row['created_at'] == '历史发放，时间未记录' for row in rows)
        body = ('<div class="page-head"><div><span class="eyebrow">管理控制台</span><h1>访问令牌</h1>'
                '<p>每位接收人一个身份、一枚令牌，所有令牌拥有相同的只读数据范围。撤销对后续请求立即生效。</p></div>'
                '<div class="session"><span class="avatar" aria-hidden="true">' + escape(item['username'][:1]) + '</span><span><b>'
                + escape(item['username']) + '</b><br>发放管理员</span><form method="post" action="/admin/logout">'
                + hidden + '<button class="secondary small" type="submit">退出</button></form></div></div>')
        if message:
            body += _alert(tone, message, role='alert' if tone == 'error' else 'status')
        if token:
            body += ('<section class="card reveal" aria-labelledby="reveal-title"><h2 id="reveal-title">令牌已生成，只显示这一次</h2>'
                     '<p>请现在复制并通过受控渠道交给对应接收人。离开或刷新此页后无法再次查看，遗失只能撤销后重新发放。</p>'
                     '<label for="issued-token">新令牌</label><textarea id="issued-token" readonly rows="2" autocomplete="off" spellcheck="false">'
                     + escape(token) + '</textarea><div class="reveal-actions"><button type="button" id="copy-token">复制令牌</button>'
                     '<a class="button secondary" href="/admin">已安全交付，关闭</a><span id="copy-result" role="status"></span></div></section>')
        body += ('<div class="card stats"><div class="stat"><span>有效令牌</span><b>' + str(len(rows))
                 + '</b></div><div class="stat"><span><i class="dot' + ('' if rows else ' off') + '"></i>MCP 访问</span><b>'
                 + ('已开放' if rows else '全部拒绝') + '</b></div><div class="stat"><span>发放时间未记录</span><b>' + str(historic) + '</b></div></div>')
        body += '<div class="admin-grid"><section class="card panel" aria-labelledby="issue-title"><h2 id="issue-title">发放新令牌</h2>'
        if metadata_available:
            body += ('<p>为一位接收人生成专属令牌。</p><form method="post" action="/issue">' + hidden
                     + '<label for="identity">接收人身份名称</label><input id="identity" name="identity" maxlength="64" required placeholder="例如 analyst-wang" autocomplete="off" value="'
                     + escape(draft) + '"><p class="hint">字母、数字、点、下划线或连字符，最多 64 字符。同名身份需先撤销。</p>'
                     '<button type="submit">生成专属令牌</button></form>')
        else:
            body += _alert('warn', '发放元数据不可用', '新令牌发放已停止，右侧仍可撤销有效身份。请维护者检查受限元数据文件，不能直接覆盖原文件。', 'alert')
        body += '</section><section class="card table-card" aria-labelledby="list-title"><div class="table-tools"><h2 id="list-title">已发放身份<span>' + str(len(rows)) + '</span></h2>'
        if len(rows) > 5:
            body += '<input id="identity-filter" type="search" placeholder="筛选身份" aria-label="筛选身份" autocomplete="off">'
        body += '</div><div class="table-wrap"><table><thead><tr><th>身份</th><th>令牌前缀</th><th>创建时间（UTC）</th><th><span class="muted">操作</span></th></tr></thead><tbody>'
        for row in rows:
            identity = escape(row['identity'])
            body += ('<tr data-identity="' + identity + '"><td class="identity">' + identity + '</td><td class="prefix">' + escape(row['prefix'])
                     + '…</td><td class="muted">' + escape(row['created_at']) + '</td><td class="actions-cell"><details class="revoke"><summary>撤销</summary>'
                     '<form method="post" action="/revoke">' + hidden + '<input type="hidden" name="identity" value="' + identity
                     + '"><label><input type="checkbox" name="confirm" value="yes" required>确认撤销 ' + identity
                     + '</label><button class="danger small" type="submit">立即撤销</button></form></details></td></tr>')
        if not rows:
            body += '<tr class="empty"><td colspan="4">尚无有效令牌，MCP 当前拒绝全部访问。</td></tr>'
        body += ('</tbody></table></div><div class="table-foot" id="filter-empty" hidden>没有匹配的身份。</div>'
                 '<div class="table-foot">可撤销最后一枚令牌。撤销不取消已在执行的查询，后续请求立即失去权限。</div></section></div>')
        return HTMLResponse(_shell('令牌管理', body, 'admin'), status_code=status)

    def login_form(nonce, error='', username='', status=200):
        body = ('<div class="narrow"><section class="card login"><span class="brand-mark" aria-hidden="true">CI</span><h1>管理员登录</h1>'
                '<p>仅限令牌发放管理员。MCP 接收人的 Bearer 令牌不能登录此页。</p>'
                + (_alert('error', error, role='alert') if error else '')
                + '<form method="post" action="/admin/login">' + _hidden(nonce)
                + '<label for="username">管理员名称</label><input id="username" name="username" required maxlength="64" autocomplete="username" value="'
                + escape(username) + '"' + ('' if username else ' autofocus') + '>'
                '<label for="password">管理员口令</label><input id="password" name="password" type="password" required maxlength="256" autocomplete="current-password"'
                + (' autofocus' if username else '') + '><button type="submit">登录</button></form>'
                '<p class="hint">空闲 20 分钟或登录 8 小时后会话失效；同一来源 15 分钟内连续失败 5 次将暂停登录。</p></section></div>')
        response = HTMLResponse(_shell('管理员登录', body, 'admin'), status_code=status)
        response.set_cookie(PREAUTH, nonce, max_age=600, secure=True, httponly=True, samesite='strict', path='/')
        return response

    def challenge_for(request):
        """Reuse this browser's live challenge or issue a bounded new one; None when over limit."""
        now = clock()
        peer = request.client.host if request.client else ''
        for key, challenge in list(challenges.items()):
            if challenge['expires'] <= now:
                challenges.pop(key, None)
        for address, times in list(challenge_issues.items()):
            recent = [stamp for stamp in times if now - stamp < 60]
            if recent:
                challenge_issues[address] = recent
            else:
                challenge_issues.pop(address, None)
        nonce = request.cookies.get(PREAUTH, '')
        existing = challenges.get(hashlib.sha256(nonce.encode()).hexdigest())
        if not existing or existing['peer'] != peer:
            # Reloading a valid browser form reuses its challenge. Clearing cookies
            # is bounded per TCP peer, independently of the global memory bound.
            active = sum(challenge['peer'] == peer for challenge in challenges.values())
            recent = challenge_issues.get(peer, [])
            if active >= 8 or len(recent) >= 30 or len(challenges) >= 512 or len(challenge_issues) >= 1024:
                return None
            nonce = secrets.token_urlsafe(32)
            challenges[hashlib.sha256(nonce.encode()).hexdigest()] = {'expires':now + 600, 'peer':peer}
            challenge_issues[peer] = recent + [now]
        return nonce

    def too_many_challenges():
        return _status_page('登录请求过多', '该来源短时间内打开登录页过多，请 10 分钟后重试。', 429,
                            headers={'Retry-After': '600'}, active='admin')

    async def homepage(request):
        return HTMLResponse(_homepage(settings))

    async def login_page(request):
        if session(request):
            return RedirectResponse('/admin', status_code=303)
        try:
            _admin(admin_path)
        except (OSError, ValueError, TypeError, KeyError, UnicodeError):
            return _status_page('管理员登录暂不可用', '请维护者在服务器受限环境配置唯一管理员凭据。访客仍可阅读指南和下载客户端。', 503, active='admin')
        nonce = challenge_for(request)
        return login_form(nonce) if nonce else too_many_challenges()

    async def login(request):
        fields = await form(request)
        nonce = request.cookies.get(PREAUTH, '')
        key = hashlib.sha256(nonce.encode()).hexdigest()
        challenge = challenges.pop(key, None)
        peer = request.client.host if request.client else ''
        if (not challenge or challenge['expires'] <= clock() or challenge['peer'] != peer
                or not csrf_ok(fields, nonce) or not nonce):
            audit(request, 'admin.login', 'csrf_denied')
            return _status_page('登录页已失效', '登录表单已过期或已使用，请重新打开登录页后再试。', 403,
                                action=('/admin/login', '重新打开登录页'), active='admin')
        now = clock()
        for address, times in list(failures.items()):
            if not any(now - stamp < 900 for stamp in times):
                failures.pop(address, None)
        times = [stamp for stamp in failures.get(peer, []) if now - stamp < 900]
        if len(times) >= 5 or len(failures) >= 1024:
            audit(request, 'admin.login', 'rate_limited')
            return _status_page('登录已暂停', '认证失败次数超过限制，请在 15 分钟后重试。', 429,
                                headers={'Retry-After': '900'}, active='admin')
        failures[peer] = times + [now]
        try:
            data, version = _admin(admin_path)
            if len(fields.get('username', '')) > 64 or len(fields.get('password', '')) > 256:
                valid = False
            else:
                async with login_gate:
                    valid = await run_in_threadpool(_password_ok, data, fields.get('username', ''), fields.get('password', ''))
        except (OSError, ValueError, TypeError, KeyError, UnicodeError):
            valid = False
        if not valid:
            audit(request, 'admin.login', 'denied')
            retry = challenge_for(request)
            if not retry:
                return too_many_challenges()
            # Another login from this peer may succeed while the KDF runs and
            # clear the failure window. Read its current state after the await.
            left = max(0, 5 - len(failures.get(peer, [])))
            error = '管理员名称或口令错误' + ('，还可尝试 ' + str(left) + ' 次' if left else '，登录已暂停 15 分钟')
            return login_form(retry, error, fields.get('username', '')[:64], status=401)
        failures.pop(peer, None)
        for old, item in list(sessions.items()):
            if now - item['last'] > 1200 or now - item['created'] > 28800:
                sessions.pop(old, None)
        if len(sessions) >= 128:
            return _status_page('管理员会话过多', '当前活动会话已达上限，请稍后重试。', 429, active='admin')
        raw = secrets.token_urlsafe(32)
        sessions[hashlib.sha256(raw.encode()).hexdigest()] = {'username': data['username'], 'csrf': secrets.token_urlsafe(32), 'created': now, 'last': now, 'version': version}
        request.state.admin = data['username']
        response = RedirectResponse('/admin', status_code=303)
        response.set_cookie(COOKIE, raw, max_age=28800, secure=True, httponly=True, samesite='strict', path='/')
        response.delete_cookie(PREAUTH, secure=True, httponly=True, samesite='strict', path='/')
        audit(request, 'admin.login', 'succeeded')
        return response

    async def admin(request):
        item = session(request)
        return management(item) if item else expired()

    async def mutate(request):
        item = session(request)
        if not item:
            audit(request, 'token.manage', 'unauthorized')
            return _status_page('需要管理员登录', '会话已失效或尚未登录，请登录后重新操作。', 401,
                                action=('/admin/login', '前往登录'), active='admin')
        fields = await form(request)
        if not csrf_ok(fields, item['csrf']):
            audit(request, 'token.manage', 'csrf_denied')
            return _status_page('请求校验失败', '同源或 CSRF 校验未通过，请重新打开管理页后再操作。', 403,
                                action=('/admin', '返回令牌管理'), active='admin')
        action = 'token.issue' if request.url.path == '/issue' else 'token.revoke'
        identity = fields.get('identity', '').strip()
        draft = identity[:64] if action == 'token.issue' else ''
        if not IDENTITY.fullmatch(identity):
            audit(request, action, 'invalid_identity')
            return management(item, '身份名称格式无效：只能使用字母、数字、点、下划线或连字符，最多 64 字符', status=400, draft=draft)
        if action == 'token.revoke' and fields.get('confirm') != 'yes':
            return management(item, '请先勾选“确认撤销 ' + identity + '”再提交', status=400)
        try:
            if action == 'token.issue':
                token = await run_in_threadpool(issue_token, identity, server_path, registry_path)
                audit(request, action, 'succeeded', identity)
                return management(item, '已为 ' + identity + ' 生成令牌', token, tone='ok')
            await run_in_threadpool(revoke_token, identity, server_path, registry_path)
            audit(request, action, 'succeeded', identity)
            item['flash'] = ('ok', '已撤销 ' + identity + '，其后续 MCP 请求将被拒绝')
            return RedirectResponse('/admin', status_code=303)
        except ValueError:
            audit(request, action, 'rejected', identity)
            try:
                known = {row['identity'] for row in token_inventory(server_path, registry_path)[0]}
            except (OSError, ValueError, UnicodeError):
                known = None
            if known is not None and action == 'token.issue' and identity in known:
                message = '身份 ' + identity + ' 已有有效令牌；如需重新发放，请先在列表中撤销'
            elif known is not None and action == 'token.revoke' and identity not in known:
                message = '身份 ' + identity + ' 不存在或已被撤销'
            else:
                message = '操作未完成：令牌配置或发放元数据无效，请联系服务器维护者'
            return management(item, message, status=400, draft=draft)
        except OSError:
            audit(request, action, 'storage_unavailable', identity)
            return _status_page('令牌存储不可用', '无法读写令牌存储，请联系服务器维护者。', 503,
                                action=('/admin', '返回令牌管理'), active='admin')

    async def logout(request):
        item = session(request)
        if not item or not csrf_ok(await form(request), item['csrf']):
            return _status_page('退出校验失败', '会话已失效或请求校验未通过。', 403,
                                action=('/admin', '返回令牌管理'), active='admin')
        sessions.pop(hashlib.sha256(request.cookies.get(COOKIE, '').encode()).hexdigest(), None)
        audit(request, 'admin.logout', 'succeeded')
        return expired()

    downloads = {'mcp-client-kit.zip', 'mcp-ca.crt', 'tools-schema.json', 'client-guide.md',
                 'mcp-client.example.json', 'mcp-endpoint.json', 'SHA256SUMS.txt'}

    async def download(request):
        name = request.path_params['name']
        path = public_path / name
        if name not in downloads or not path.is_file() or path.resolve().parent != public_path.resolve():
            return Response('文件不存在', status_code=404)
        audit(request, 'download.read', 'succeeded')
        return FileResponse(path, filename=name, media_type='application/zip' if name.endswith('.zip') else 'application/octet-stream')

    async def guide(request):
        path = public_path / 'client-guide.html'
        if not path.is_file():
            return _status_page('使用指南尚未构建', '服务器尚未生成在线指南，请联系维护者；接入材料仍可在首页下载。', 503, active='guide')
        return FileResponse(path, media_type='text/html')

    async def asset(request):
        name = request.path_params['name']
        if name not in {'token-desk.css', 'token-desk.js'}:
            return Response(status_code=404)
        return FileResponse(ROOT/'assets'/name, media_type='text/css' if name.endswith('.css') else 'text/javascript')

    async def health(request):
        return JSONResponse({'status':'ok','service':'complaint-insights-portal'})

    app = Starlette(routes=[Route('/', homepage), Route('/guide', guide), Route('/downloads/{name}', download),
        Route('/assets/{name}', asset), Route('/admin', admin), Route('/admin/login', login_page),
        Route('/admin/login', login, methods=['POST']), Route('/admin/logout', logout, methods=['POST']),
        Route('/issue', mutate, methods=['POST']), Route('/revoke', mutate, methods=['POST']), Route('/health', health)])

    async def boundary(request: Request, call_next):
        request.state.request_id = uuid.uuid4().hex
        started = clock()
        peer = request.client.host if request.client else ''
        try:
            allowed = any(ip_address(peer) in network for network in networks)
        except ValueError:
            allowed = False
        if request.url.scheme != 'https' or not allowed:
            response = Response('需要HTTPS及授权内网地址', status_code=403)
        elif request.headers.get('host') != f'{settings.host}:{settings.port}':
            response = Response('Host不被允许', status_code=421)
        elif request.headers.get('origin') and request.headers['origin'] != settings.origin:
            response = Response('Origin不被允许', status_code=403)
        else:
            response = await call_next(request)
        # Native form POSTs need their same-origin Origin header. no-referrer
        # changes that header to "null", which our strict origin guard rejects.
        response.headers.update({'Cache-Control':'no-store', 'Pragma':'no-cache', 'Referrer-Policy':'same-origin',
            'X-Content-Type-Options':'nosniff', 'X-Frame-Options':'DENY',
            'Content-Security-Policy':"default-src 'none'; style-src 'self'; script-src 'self'; connect-src 'self'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'",
            'Permissions-Policy':'camera=(), microphone=(), geolocation=()', 'X-Request-ID':request.state.request_id})
        logger.info(json.dumps({'request_id':request.state.request_id,'action':'http','status':response.status_code,
            'client_ip':peer,'method':request.method,'duration_ms':round((clock()-started)*1000)}))
        return response

    app.add_middleware(BaseHTTPMiddleware, dispatch=boundary)
    return app


def serve_desk() -> None:
    import uvicorn
    remote = MCPSettings.load()
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    uvicorn.run(create_app(settings=DeskSettings(remote.host, allowed_networks=remote.allowed_networks)),
        host=remote.host, port=PORT, ssl_certfile=str(remote.certificate), ssl_keyfile=str(remote.private_key),
        ssl_version=ssl.PROTOCOL_TLS_SERVER, proxy_headers=False, access_log=False, limit_concurrency=16)
