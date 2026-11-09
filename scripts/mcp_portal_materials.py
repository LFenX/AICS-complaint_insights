"""Build public, allowlisted MCP materials without reading any credential file."""
from datetime import datetime, timezone
import hashlib
from html import escape
import json
from pathlib import Path
import re
import ssl
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from insights.datasets import dataset_catalog
from insights.mcp_server import DEFAULT_TOOL_CALLS_PER_MINUTE, TOOL_RATE_WINDOW_SECONDS
from insights.token_desk import _shell

TASK = 'T-INSIGHTS-MCP-PORTAL-20261030-01'
DOCS = ROOT / 'LG_project_docs/requirements' / TASK
PUBLIC = ROOT / '.runtime/mcp-portal-public'
NOTES = {
    'get_data_guide':'无参数。返回timezone、workflow、counting、fields、limits、tool_rate_limit、boundaries、source_tables及服务器default_source。tool_rate_limit是当前进程实际生效的每身份调用配额。用于选工具，不含客诉正文。',
    'get_sync_status':'返回source对象、seconds_since_last_success、latest_run、schedule和consistency。source包含data_version、快照及最近同步时间；不是来源列表或实时采集健康探测。',
    'get_capabilities':'返回source_id、permissions父链及capabilities动作/风险/审计/enabled/disabled_reason。它是说明目录，不能授权或执行token.issue/revoke；MCP没有这两个工具。',
    'list_taxonomy':'返回meta、items、next_cursor。status没有封闭枚举，按源状态字符串精确匹配；省略时保留全部状态。level=1/2/3对应三级分类层次，分类ID和父链以items为准。',
    'query_daily_statistics':'start/end必填且start<end。返回meta、date_range、scope、items、next_cursor和counting_note；items含日期、分类ID/名称/状态、mail_count、issue_count和pending_mail_count。空数组是有效结果。',
    'list_mails':'返回meta、items、next_cursor。默认不加载正文和完整源行，items含mail_pk、主题、AI摘要及投影字段；日期可省略。默认direction=ALL，与统计和报告不同。分类过滤用ID，level_one/level_two最多100字符，issue_type_id最多200字符。',
    'get_mail_detail':'mail_pk须来自同一source_id的list_mails，数值须在1..9223372036854775807内。返回meta、mail、attachments和issue_bindings；mail含正文/译文及AI投影。include_raw=true才附raw_record/ai_record/raw_payload。附件只含元数据，没有附件文件下载。',
    'get_report_context':'start/end必填且start<end。返回meta、days、next_cursor、date_range和note；days按日期、二级（无二级时一级）分类组织当前页邮件，并非三级聚合总表。include_body=true才加载正文。无mailbox参数，周期总数另查统计。',
    'list_source_tables':'返回meta、items和note。items给出14个table枚举、domain、key_field及用途，供确定后续原始记录查询键。无业务分页。',
    'list_source_records':'table必填。返回meta、items、next_cursor、note；默认items只有source_id/source_domain/source_table/record_key/synced_at/deleted_at，include_payload=true才有payload。删除记录默认排除，按record_key文本排序；不接受日期/分类/任意SQL过滤。',
    'get_source_record':'table与record_key必填，record_key用list_source_records返回值。返回meta和record（含payload）。没有当前行时RECORD_NOT_FOUND；include_deleted=true才允许追溯保留的删除副本。',
}


def _schema(schema, root):
    if '$ref' in schema:
        return root['$defs'][schema['$ref'].split('/')[-1]]
    return schema


def parameter(schema, root):
    value = _schema(schema, root)
    variants = [_schema(item,root) for item in value.get('anyOf',[value])]
    types = '/'.join(item.get('type','object') for item in variants)
    constraints = []
    for item in variants:
        for key, label in [('enum','枚举'),('format','格式'),('minimum','最小值'),('maximum','最大值'),('minLength','最短'),('maxLength','最长'),('pattern','正则')]:
            if key in item:
                constraints.append(label + ': ' + json.dumps(item[key],ensure_ascii=False))
    if value.get('description'):
        constraints.append(value['description'])
    return types, '；'.join(constraints) or '无额外Schema限制'


def tool_reference(catalog):
    blocks=[]
    for tool in catalog['tools']:
        name=tool['name']
        schema=tool['inputSchema']
        blocks += ['### '+name+' · '+tool.get('title',name), '', tool.get('description',''), '', NOTES[name], '']
        if not schema.get('properties'):
            blocks += ['参数：无；arguments传 `{}`。', '']
        else:
            blocks += ['|参数|必填|类型|默认值|枚举、限制与说明|','|---|---|---|---|---|']
            for key,value in schema['properties'].items():
                types, constraints=parameter(value,schema)
                required=key in schema.get('required',[])
                default=json.dumps(value['default'],ensure_ascii=False) if 'default' in value else '无'
                row=[key,'是' if required else '否',types,default,constraints]
                blocks += ['|'+'|'.join(item.replace('|','&#124;').replace('\n',' ') for item in row)+'|']
            blocks += ['']
        blocks += ['完整inputSchema：','```json',json.dumps(schema,ensure_ascii=False,indent=2),'```','']
    return '\n'.join(blocks)


def inline(value):
    value=escape(value)
    value=re.sub(r'`([^`]+)`',lambda m:'<code>'+m[1]+'</code>',value)
    value=re.sub(r'\[([^\]]+)\]\((https://[^)]+|/[^)]+|#[^)]+)\)',lambda m:'<a href="'+m[2]+'">'+m[1]+'</a>',value)
    return value


def render_markdown(markdown):
    # Deliberately small, escaped renderer for this controlled document syntax.
    lines=markdown.splitlines(); output=[]; headings=[]; i=0
    while i<len(lines):
        line=lines[i]
        if line.startswith('```'):
            i+=1; code=[]
            while i<len(lines) and not lines[i].startswith('```'):
                code.append(lines[i]); i+=1
            block='<pre><code>'+escape('\n'.join(code))+'</code></pre>'
            if output and output[-1]=='<p>完整inputSchema：</p>':
                # Long per-tool schemas stay available but collapsed in the HTML guide.
                output[-1]='<details><summary>完整 inputSchema</summary>'+block+'</details>'
            else:
                output.append(block)
        elif line.startswith('#'):
            match=re.match(r'^(#{1,3}) (.*?)(?: \{#([a-z0-9_-]+)\})?$',line)
            if match:
                level=len(match[1]); title=match[2]; anchor=match[3]
                if anchor:
                    headings.append((anchor,title))
                output.append(f'<h{level}'+(' id="'+anchor+'"' if anchor else '')+'>'+inline(title)+f'</h{level}>')
        elif line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                if not re.fullmatch(r'[|:\- ]+',lines[i]):
                    rows.append([part.strip() for part in lines[i].strip('|').split('|')])
                i+=1
            output.append('<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+inline(cell)+'</th>' for cell in rows[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+inline(cell)+'</td>' for cell in row)+'</tr>' for row in rows[1:])+'</tbody></table></div>')
            continue
        elif re.match(r'^(\d+\. |\- )',line):
            numbered=bool(re.match(r'^\d+\. ',line)); tag='ol' if numbered else 'ul'; items=[]
            pattern=r'^\d+\. ' if numbered else r'^\- '
            while i<len(lines) and re.match(pattern,lines[i]):
                items.append('<li>'+inline(re.sub(pattern,'',lines[i]))+'</li>'); i+=1
            output.append('<'+tag+'>'+''.join(items)+'</'+tag+'>'); continue
        elif line.strip():
            output.append('<p>'+inline(line)+'</p>')
        i+=1
    navigation='<aside class="doc-nav" aria-label="指南目录">'+''.join('<a href="#'+anchor+'">'+escape(title)+'</a>' for anchor,title in headings)+'</aside>'
    return _shell('完整使用指南','<div class="doc-layout">'+navigation+'<article class="doc-content">'+''.join(output)+'</article></div>','guide')


def build(catalog):
    names=[tool['name'] for tool in catalog['tools']]
    if set(names)!=set(NOTES) or len(names)!=11:
        raise ValueError('expected all eleven known tools from real tools/list')
    endpoint=json.loads((ROOT/'config/mcp-endpoint.json').read_text(encoding='utf-8'))
    endpoint={key:value for key,value in endpoint.items() if key in {'url','transport','allowed_networks','ca_certificate','ca_sha256','server_certificate_sha256','server_certificate_expires_at'}}
    endpoint.update({'portal_url':endpoint['url'].replace(':3037/mcp',':3029/'),'default_source':'production-ai-customer','verified_protocol_version':'2025-11-25','authentication':'individually-issued-bearer; no OAuth discovery'})
    ca=(ROOT/'config/mcp-ca.crt').read_bytes()
    file_sha=hashlib.sha256(ca).hexdigest()
    certificate_sha=hashlib.sha256(ssl.PEM_cert_to_DER_cert(ca.decode('ascii'))).hexdigest()
    if endpoint['ca_sha256'] not in {file_sha,certificate_sha} or b'PRIVATE KEY' in ca:
        raise ValueError('CA identity mismatch or unexpected private material')
    endpoint.update({'ca_file_sha256':file_sha,'ca_certificate_der_sha256':certificate_sha})
    template=(DOCS/'release/client-guide.template.md').read_text(encoding='utf-8')
    tables='|table枚举|domain|key_field|用途|\n|---|---|---|---|\n'+'\n'.join('|'+ '|'.join(str(row[key]) for key in ['table','domain','key_field','description'])+'|' for row in dataset_catalog())
    rate_note = (f'每个身份的全部工具合计默认 {DEFAULT_TOOL_CALLS_PER_MINUTE} 次 / {TOOL_RATE_WINDOW_SECONDS} 秒滑动窗口，HTTP与stdio均执行限频。'
        '实际配额见 get_data_guide 的 tool_rate_limit。达到上限返回 isError=true，内容含 TOOL_RATE_LIMITED 和 retry_after_seconds；等待指定秒数后重试。'
        '下载客户端遇到工具错误会停止，不输出半页合计。重新运行完整分页时从首页开始；自行续页须保持筛选与版本一致，版本冲突丢弃旧页并重查。\n\n')
    replacements={'@@PORTAL@@':endpoint['portal_url'],'@@ENDPOINT@@':endpoint['url'],'@@NETWORKS@@':', '.join(endpoint['allowed_networks']),'@@CA_SHA@@':file_sha,'@@CERT_EXPIRY@@':endpoint['server_certificate_expires_at'],'@@TOOLS@@':rate_note+tool_reference(catalog),'@@TABLES@@':tables}
    for key,value in replacements.items(): template=template.replace(key,value)
    if '@@' in template: raise ValueError('unexpanded guide field')
    guide=render_markdown(template)
    files={'client-guide.md':template.encode(),'client-guide.html':guide.encode(),'tools-schema.json':json.dumps(catalog,ensure_ascii=False,indent=2).encode(),
           'mcp-ca.crt':ca,'mcp-endpoint.json':json.dumps(endpoint,ensure_ascii=False,indent=2).encode(),
           'mcp-client.example.json':json.dumps({'url':endpoint['url'],'ca_file':'mcp-ca.crt','bearer_token':'REPLACE_WITH_YOUR_OWN_ISSUED_TOKEN','source_id':'production-ai-customer'},ensure_ascii=False,indent=2).encode(),
           'mcp-client-config.example.json':(ROOT/'config/mcp-client.example.json').read_bytes()}
    for filename in ['mcp_client.py','mcp_protocol_client.py','mcp_workflow.py']:
        files[filename]=(ROOT/'scripts'/filename).read_bytes()
    files['client-dependencies.txt']=(ROOT/'client-dependencies.txt').read_bytes()
    files['token-desk.css']=(ROOT/'assets/token-desk.css').read_bytes()
    files['token-desk.js']=(ROOT/'assets/token-desk.js').read_bytes()
    query_defaults={'daily.json':{'start':'2026-10-29','end':'2026-10-30','level':3,'scope':'primary','direction':'RECEIVED','limit':200},
        'mails.json':{'start':'2026-10-29','end':'2026-10-30','direction':'RECEIVED','limit':30},
        'context.json':{'start':'2026-10-29','end':'2026-10-30','include_body':False,'limit':20},
        'ai-records.json':{'table':'MailAiArtifact','include_payload':True,'limit':20},
        'status.json':{},'taxonomy.json':{'level':3,'limit':100},'tables.json':{},'source-records.json':{'table':'messages','limit':20}}
    for name,args in query_defaults.items():
        args['source_id']='production-ai-customer'
        files['queries/'+name]=json.dumps(args,ensure_ascii=False,indent=2).encode()
        # Existing public query examples must not retain the obsolete development source.
        (ROOT/'config/mcp-queries'/name).write_bytes(files['queries/'+name])
    PUBLIC.mkdir(parents=True,exist_ok=True)
    for name in ['client-guide.md','client-guide.html','tools-schema.json','mcp-ca.crt','mcp-endpoint.json','mcp-client.example.json']:
        (PUBLIC/name).write_bytes(files[name])
    (DOCS/'release/client-guide.md').write_bytes(files['client-guide.md'])
    (DOCS/'release/tools-schema.json').write_bytes(files['tools-schema.json'])
    offline=guide.replace('/assets/token-desk','token-desk').replace('href="/guide','href="client-guide.html').replace('href="/admin"','href="'+endpoint['portal_url']+'admin"').replace('href="/"','href="client-guide.html"')
    files['client-guide.html']=offline.encode()
    files['README.txt']=('先阅读 client-guide.html 或 client-guide.md。\n通用包不含可用令牌；先向管理员领取本人令牌和核对CA。\n推荐来源 production-ai-customer 为历史本地副本。\n').encode('utf-8')
    sums='\n'.join(hashlib.sha256(data).hexdigest()+'  '+name for name,data in sorted(files.items()))+'\n'
    files['SHA256SUMS.txt']=sums.encode()
    destination=PUBLIC/'mcp-client-kit.zip'
    with zipfile.ZipFile(destination,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name,data in sorted(files.items()):
            if b'PRIVATE KEY' in data or b'postgresql://' in data:
                raise ValueError('private material in public whitelist')
            archive.writestr(name,data)
    with zipfile.ZipFile(destination) as archive:
        if archive.testzip() is not None or set(archive.namelist())!=set(files):
            raise ValueError('public kit integrity failed')
    outer=sums+hashlib.sha256(destination.read_bytes()).hexdigest()+'  mcp-client-kit.zip\n'
    (PUBLIC/'SHA256SUMS.txt').write_text(outer,encoding='utf-8')
    return {'status':'BUILT','archive':str(destination),'file_count':len(files),'tool_count':len(names),
        'sha256':hashlib.sha256(destination.read_bytes()).hexdigest(),'contains_credential':False,
        'built_at':datetime.now(timezone.utc).isoformat()}
