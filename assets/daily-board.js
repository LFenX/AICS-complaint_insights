/* Local read model only. Mail HTML and reference sample scripts never execute. */
(() => {
  'use strict';
  const $=s=>document.querySelector(s);
  const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const pct=n=>n==null?'—':`${n>0?'+':''}${n.toFixed(1)}%`;
  const number=n=>new Intl.NumberFormat('zh-CN',{maximumFractionDigits:1}).format(n??0);
  const scopeNames={complaint:'客诉相关来信',non_complaint:'咨询 / 回访 / 其他',unclear:'尚无问题线索'};
  const statusNames={new_issue:'本封描述问题',follow_up:'工单跟进',materials:'补交材料',resolved:'已解决 / 致谢',inquiry:'咨询 / 服务申请',unidentified:'无有效问题线索',feedback:'问题反馈',suggestion:'纯建议',notice:'商务 / 通知',support_copy:'客服说明副本'};
  const uidNames={verified_mail:'本封原文支持',verified_thread:'会话原文支持',conflict:'多账号 / 冲突',unverified:'待核验',not_found:'未找到文本证据'};
  const roleNames={primary_or_keep_account:'主账号',wrong_or_empty_account:'误建账号',original_account:'原账号',current_account:'现账号',historical_account:'历史账号',self_reported:'自报账号'};
  const roleText=r=>r.uid.state==='conflict'?(r.uid.uid_roles||[]).map(v=>`<div class="mail-class">${esc((v.roles||[]).map(x=>roleNames[x]||x).join('/'))}<br><span class="uid">${esc(v.value)}</span></div>`).join(''):'';
  const state={domain:'all',group:'all',sub:'all',scope:'all',hour:null,search:'',page:1,pageSize:25,sort:'uid',subject:'translated',body:'translated'};
  const charts=[],detailCache=new Map();
  let DATA,themes,domains,drawerMail,activeFile,drawerGeneration=0,focusBefore;
  let selectedDate='',availableDates=[],defaultDate='',loadGeneration=0,loadController,calendarView=null;
  let drawerSubject='translated',drawerBody='translated';
  const parseDate=v=>new Date(String(v).replace(' ','T'));
  const timestamp=v=>{const d=parseDate(v);return Number.isNaN(d.getTime())?'未记录':new Intl.DateTimeFormat('zh-CN',{timeZone:'Asia/Shanghai',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hour12:false}).format(d);};
  const timeOnly=v=>timestamp(v).split(' ').pop();
  const headerAddress=v=>typeof v==='string'?v:(v.name?`${v.name} <${v.mail_address||v.address||''}>`:(v.mail_address||v.address||''));
  const size=n=>n>=1048576?`${(n/1048576).toFixed(1)} MB`:n>=1024?`${(n/1024).toFixed(1)} KB`:`${n} B`;
  const themeButton=(id,text)=>`<button class="text-link" data-rank-theme="${esc(id)}">${esc(text)}</button>`;
  const switcher=(which,mode)=>`<span class="switch" aria-label="${which.toLowerCase().includes('subject')?'主题':'正文'}语言"><button data-mode="${which}:original" class="${mode==='original'?'active':''}" aria-pressed="${mode==='original'}">原文</button><button data-mode="${which}:translated" class="${mode==='translated'?'active':''}" aria-pressed="${mode==='translated'}">译文</button></span>`;
  const domainColor=id=>domains.get(id)?.color||'#8793a1';
  async function getJSON(url,options={}){const response=await fetch(url,{...options,cache:'no-store'});if(!response.ok)throw new Error(response.status===409?'报告已更新，请重新载入':`读取失败（${response.status}）`);return response.json();}
  const shanghaiToday=()=>new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Shanghai',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
  const shanghaiYesterday=()=>{const day=new Date(shanghaiToday()+'T00:00:00Z');day.setUTCDate(day.getUTCDate()-1);return day.toISOString().slice(0,10);};
  const validDate=day=>/^\d{4}-\d{2}-\d{2}$/.test(day)&&!Number.isNaN(Date.parse(day+'T00:00:00Z'))&&new Date(day+'T00:00:00Z').toISOString().slice(0,10)===day;
  function reportURL(path,params={}){const url=new URL(path,location.origin);url.searchParams.set('date',DATA.business_date);url.searchParams.set('v',DATA.report_sha256);for(const [key,value] of Object.entries(params))url.searchParams.set(key,value);return url.pathname+url.search;}
  function hero(ready=false){
    const subtitle=ready?`北京时间全天 · 根据每封摘要与正文重新归类 · 来源 ${esc(DATA.source_id)} · 快照截至 ${esc(timestamp(DATA.source_snapshot_at))}`:'按北京时间查看每日客诉日报';
    const shown=selectedDate?selectedDate.replaceAll('-','/'):'选择日期';
    return `<header class="hero"><div><div class="hero-title"><div class="ios-date"><button type="button" id="report-date" class="ios-date-trigger" data-cal-toggle aria-haspopup="dialog" aria-expanded="false" aria-label="日报日期 ${esc(selectedDate)}"><span>${esc(shown)}</span><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="5" width="17" height="15" rx="3"></rect><path d="M3.5 9.5h17M8 3.5v4M16 3.5v4"></path></svg></button><div id="ios-cal" class="ios-cal" role="dialog" aria-label="选择日报日期" hidden></div></div><h1>客诉日报</h1></div><p class="subtitle">${subtitle}</p></div><div class="hero-right"><div class="date-actions">${availableDates.length?`<label><span class="sr-only">已生成日报</span><select id="report-history" aria-label="已生成日报"><option value=""${availableDates.includes(selectedDate)?'':' selected'}>已生成日报</option>${availableDates.map(day=>`<option value="${esc(day)}"${day===selectedDate?' selected':''}>${esc(day)}</option>`).join('')}</select></label>`:''}</div>${ready?`<div class="hero-meta"><span class="status-pill">${DATA.production_isolated?'本地快照 · 生产采集已隔离':'本地快照'}</span><button class="subtle-button" data-method>统计口径与覆盖 ↗</button></div>`:'<span class="date-zone">北京时间 · 每日 00:30 生成前一天日报</span>'}</div></header>`;
  }
  function renderStatus(kind,message=''){
    const title=kind==='loading'?'正在载入日报':kind==='missing'?'日报未生成':'日报读取失败';
    $('#app').innerHTML=`<main class="workspace status-workspace">${hero()}<section class="report-status" role="status" aria-live="polite"><span class="status-mark">CI</span><h2>${title}</h2><p>${kind==='missing'?`${esc(selectedDate)} 的客诉日报尚未生成，可切换查看已生成的日期。`:esc(message||'正在读取所选日期的日报')}</p>${kind==='error'?'<button class="date-today" data-retry>重新载入</button>':''}</section><p class="board-credit">FunPlus-Nueva Games-X Publish-AI与数据应用</p></main>`;
  }
  async function loadReport(day=null,historyMode=null){
    const generation=++loadGeneration;
    loadController?.abort();loadController=new AbortController();
    calendarView=null;selectedDate=day||defaultDate||shanghaiYesterday();
    closeDrawer();charts.splice(0).forEach(chart=>chart.dispose());detailCache.clear();DATA=null;
    Object.assign(state,{domain:'all',group:'all',sub:'all',scope:'all',hour:null,search:'',page:1,pageSize:25,sort:'uid'});
    if(historyMode){const url=new URL(location.href);if(day)url.searchParams.set('date',day);else url.searchParams.delete('date');history[historyMode+'State']({},'',url.pathname+url.search+url.hash);}
    renderStatus('loading');
    try{
      if(day&&!validDate(day))throw new Error('日期格式无效，请重新选择日期');
      const data=await getJSON('/data.json'+(day?'?date='+encodeURIComponent(day):''),{signal:loadController.signal});
      if(generation!==loadGeneration)return;
      defaultDate=data.default_date;selectedDate=data.business_date;availableDates=data.available_dates||[];
      document.title=`${selectedDate} 客诉日报`;
      if(data.report_status==='not_generated'){renderStatus('missing');return;}
      DATA=data;themes=new Map(DATA.themes.map(t=>[t.id,t]));domains=new Map(DATA.domains.map(d=>[d.id,d]));shell();
    }catch(error){if(generation===loadGeneration&&error.name!=='AbortError')renderStatus('error',error.message);}
  }
  function shell(){
    const s=DATA.statistics,c=DATA.coverage,top=themes.get(DATA.top_ten[0]);
    const leading=DATA.top_ten.slice(0,3).map(id=>themes.get(id)),leadingCount=leading.reduce((n,t)=>n+t.rank_count,0);
    const uidCount=(c.uid_states.verified_mail||0)+(c.uid_states.verified_thread||0);
    const identified=c.identified_count;
    const late=s.hours.slice(15).reduce((a,n)=>a+n,0),peak=s.hours.indexOf(Math.max(...s.hours));
    const lead=top?`客诉主类中，${themeButton(top.id,top.name)}最多，共 <b>${top.rank_count}</b> 封（${top.rank_share.toFixed(1)}%）。`:'全部邮件已完成逐封复核。';
    $('#app').innerHTML=`<main class="workspace" data-report="${esc(DATA.report_sha256)}">
      ${hero(true)}
      <section class="insight" aria-label="日报结论"><p>全天 <b>${s.total}</b> 封，较前一日 <b>${pct(s.growth_previous)}</b>，较前 7 日日均 <b>${pct(s.growth_seven)}</b>；15:00 后收到 <b>${late}</b> 封（${(s.total?late/s.total*100:0).toFixed(1)}%）。${lead}</p>
        <p class="insight-note">${DATA.editorial?.summary?esc(DATA.editorial.summary):`前三类合计 <b>${leadingCount} 封（${(s.total?leadingCount/s.total*100:0).toFixed(1)}%）</b>：${leading.map(t=>`${themeButton(t.id,t.name)} ${t.rank_count}封`).join("；")}。同一会话的跟进逐封保留，封数不等于玩家数或新增故障数。`}</p>
        <p class="insight-note"><b>处理关注：</b>${esc(DATA.editorial?.attention||'客户端阻断按提示和发生阶段分别复现；原角色问题核对登录渠道与历史角色；付费和赛季奖励逐笔核对权益、截止时间与凭据。当前邮件不足以认定后台根因。')}</p></section>
      <section class="kpis" aria-label="核心指标">
        <div class="kpi"><div class="kpi-value">${number(s.total)}</div><div class="kpi-label">当日来信（封）</div><div class="kpi-foot">逐封复核 ${c.reviewed}/${c.expected}</div></div>
        <div class="kpi"><div class="kpi-value up">${pct(s.growth_previous)}</div><div class="kpi-label">较前一日（${s.previous==null?'无可比数据':s.previous+' 封'}）</div><div class="kpi-foot">同一 RECEIVED 口径</div></div>
        <div class="kpi"><div class="kpi-value up">${pct(s.growth_seven)}</div><div class="kpi-label">较前 7 日平均来信</div><div class="kpi-foot">${s.previous_seven_average==null?'前7日数据不足':`前 7 日日均 ${number(s.previous_seven_average)} 封`}</div></div>
      </section>
      <section class="section-card" aria-label="问题排行"><div class="section-head"><div><h2>Top 10 客诉问题类型</h2><p>主层按业务问题汇总，具体故障保留子类；点击排行查看对应客诉来信</p></div><button class="subtle-button" data-all-groups>查看全部 ${DATA.themes.length} 个主类 ↓</button></div><div id="domain-overview"></div><div class="rank-head"><span>问题类型 / 领域</span><span>客诉相关来信</span><span>占全部</span><span>最集中的具体表现</span></div><div id="rank-rows"></div><p class="rank-note">一封计一个主类；能定位原问题的跟进与补件计入相关客诉。咨询、已解决、商务和无问题线索邮件另列。排行不代表新增事故，系统原三级分类只供复查。</p></section>
      <section class="section-card" id="evidence" aria-label="原信明细">
        <div class="evidence-head"><div class="evidence-title">原信明细<small id="result-count"></small></div><div class="coverage-tag">全部 ${c.reviewed} 封均有摘要 · 原系统缺摘要 ${c.source_empty_summaries} 封已补齐<br>真实附件已校验 ${c.attachments_ready}/${c.attachments_expected} 个${c.attachments_unavailable_authorized?` · ${c.attachments_unavailable_authorized} 个原件未取得，按用户决定保留元数据`:''}</div></div>
        <p class="subtitle">主题和正文分别切换原文 / 译文；点击图片、日志或其他文件，在右侧查看该邮件的全部附件。</p>
        <div class="domain-tabs" id="domain-tabs" aria-label="业务领域"></div><div class="theme-list" id="theme-list" aria-label="重新归纳的主问题"></div><div class="subtheme-toolbar" id="subtheme-toolbar" hidden></div><div class="subtheme-list" id="subtheme-list" aria-label="具体子问题"></div>
        <div class="filters" role="group" aria-label="邮件搜索与筛选">
          <label class="filter-field search-field"><span class="filter-label">搜索邮件</span><input id="search" type="search" aria-label="搜索邮件证据" placeholder="主题、正文、摘要、邮箱、UID 或邮件编号"></label>
          <label class="filter-field"><span class="filter-label">来信口径</span><select id="scope-filter" aria-label="邮件口径"><option value="all">全部来信口径</option><option value="complaint">客诉相关来信</option><option value="non_complaint">咨询 / 回访 / 其他</option><option value="unclear">尚无问题线索</option></select></label>
          <label class="filter-field"><span class="filter-label">主问题</span><select id="group-filter" aria-label="问题组"></select></label>
          <label class="filter-field"><span class="filter-label">优先排序</span><select id="evidence-sort" aria-label="优先排序"><option value="uid">有 UID 优先</option><option value="log">有日志优先</option><option value="image">有图片优先</option><option value="document">有其他文件优先</option></select></label>
          <button class="reset" data-reset>重置筛选</button>
        </div><div id="active-filter"></div>
        <div class="table-scroll"><table class="mail-table"><thead><tr><th>游戏 UID / 依据</th><th>发件 / 送达邮箱</th><th>主题 / 逐封摘要<br><span id="subject-switch"></span></th><th>正文<br><span id="body-switch"></span></th><th>图片</th><th>日志 / 文本</th><th>其他文件</th><th>主问题 / 原三级分类</th><th>详情</th></tr></thead><tbody id="mail-rows"></tbody></table><div id="empty-result" class="empty" hidden>没有符合条件的邮件，请重置筛选或更换关键词。</div></div>
        <div class="pagination"><span id="page-range"></span><div class="page-actions"><label>每页 <select id="page-size" aria-label="每页邮件数量"><option>25</option><option>50</option><option>100</option></select></label><button data-page="prev" aria-label="上一页">←</button><span id="page-label"></span><button data-page="next" aria-label="下一页">→</button></div></div>
      </section>
      <section class="kpis" aria-label="补充指标">
        <div class="kpi"><div class="kpi-value">${identified}<small> / ${s.total}</small></div><div class="kpi-label">已归类来信（封）</div><div class="kpi-foot">仅 ${c.unidentified_count} 封暂无有效问题线索</div></div>
        <div class="kpi"><div class="kpi-value">${s.total?String(peak).padStart(2,'0')+':00':'—'}</div><div class="kpi-label">当日收件高峰</div><div class="kpi-foot">${s.total?'该小时 '+s.hours[peak]+' 封':'当日无来信'}</div></div>
        <div class="kpi"><div class="kpi-value green">${uidCount}</div><div class="kpi-label">有单一 UID 文本证据（封）</div><div class="kpi-foot">多账号 / 冲突 ${c.uid_states.conflict||0} 封另列</div></div>
      </section>
      <section class="charts" aria-label="来信趋势与时段">
        <article class="panel"><div class="panel-head"><div><h2 class="panel-title">近 15 日收件量</h2><p>${s.previous_seven_average==null?'前7日基线数据不足':`虚线为前 7 个完整自然日日均 ${number(s.previous_seven_average)} 封`}</p></div><span class="unit">封 / 日</span></div><div class="chart" id="trend-chart" role="img" aria-label="近十五日收件量柱状图"></div><div class="chart-foot">增长率比较全部来信；同时参照前 7 日均值，避免仅由单日低基数判断故障增长。</div></article>
        <article class="panel"><div class="panel-head"><div><h2 class="panel-title">当日分时段收件</h2><p>15:00 后 ${late} 封（${(s.total?late/s.total*100:0).toFixed(1)}%） · 点击小时筛选原信</p></div><span class="unit">北京时间</span></div><div class="chart" id="hours-chart" role="img" aria-label="当日二十四小时收件量柱状图"></div><div class="chart-foot">每个小时对应真实收件时间；24 个时段合计 ${s.total} 封，包含咨询、跟进及信息不足来信。</div></article>
      </section>
      <p class="board-credit">FunPlus-Nueva Games-X Publish-AI与数据应用</p>
    </main>`;
    renderRank();renderThemes();renderTable();drawCharts();
  }
  function renderRank(){
    $('#domain-overview').innerHTML=`<div class="domain-strip" aria-label="全部来信的业务领域占比">${DATA.domains.map(d=>`<button class="domain-segment" data-domain="${esc(d.id)}" style="width:${d.share}%;--c:${domainColor(d.id)}" aria-label="${esc(d.name)} ${d.count}封，占${d.share.toFixed(1)}%"></button>`).join('')}</div><div class="domain-legend">${DATA.domains.map(d=>`<button data-domain="${esc(d.id)}"><i class="color-square" style="--c:${domainColor(d.id)}"></i><b>${esc(d.name)}</b> ${d.count} 封 · ${d.share.toFixed(1)}%</button>`).join('')}</div>`;
    const list=DATA.top_ten.map(id=>themes.get(id)),max=Math.max(...list.map(t=>t.rank_count),1);
    $('#rank-rows').innerHTML=list.map((t,i)=>{const sub=DATA.subthemes.filter(s=>s.parent_id===t.id).sort((a,b)=>b.complaint_count-a.complaint_count)[0];const kind=t.brief?`<em class="theme-kind">：${esc(t.brief)}</em>`:'';return `<button class="rank-row" data-rank-theme="${esc(t.id)}" style="--c:${domainColor(t.domain_id)}" aria-label="第${i+1}名，${esc(t.name)}${t.brief?'：'+esc(t.brief):''}，${t.rank_count}封"><span class="rank-name"><span class="rank-index">${String(i+1).padStart(2,'0')}</span><span class="rank-title">${esc(t.name)}${kind}<small>${esc(t.domain_name)}</small></span></span><span class="rank-bar"><span class="rank-track"><i style="width:${t.rank_count/max*100}%"></i></span><b>${t.rank_count}</b></span><span class="rank-share">${t.rank_share.toFixed(1)}%</span><span class="rank-sub">${esc(sub?.name||t.name)} · ${sub?.complaint_count||t.rank_count} 封</span></button>`;}).join('');
  }
  function renderThemes(){
    const domain=domains.get(state.domain),color=domain?.color||'#8793a1';
    $('#domain-tabs').innerHTML=`<button class="domain-tab ${state.domain==='all'?'active':''}" data-domain="all" aria-pressed="${state.domain==='all'}" style="--c:var(--gray)">全部来信 <b>${DATA.statistics.total}</b></button>`+DATA.domains.map(d=>`<button class="domain-tab ${state.domain===d.id?'active':''}" data-domain="${esc(d.id)}" aria-pressed="${state.domain===d.id}" style="--c:${domainColor(d.id)}"><span>${esc(d.name)}</span><b>${d.count}</b></button>`).join('');
    const available=DATA.themes.filter(t=>state.domain==='all'||t.domain_id===state.domain);
    $('#theme-list').style.setProperty('--c',color);
    $('#theme-list').innerHTML=`<button class="theme-chip ${state.group==='all'?'active':''}" data-theme="all" aria-pressed="${state.group==='all'}">${domain?'该领域全部问题':'全部主问题'}<span>${domain?.count||DATA.statistics.total}</span></button>`+available.map(t=>{const kind=t.brief?`<em class="theme-kind">：${esc(t.brief)}</em>`:'';return `<button class="theme-chip ${state.group===t.id?'active':''} ${t.scope!=='complaint'?'muted':''}" data-theme="${esc(t.id)}" aria-pressed="${state.group===t.id}" title="${esc(t.name+(t.brief?'：'+t.brief:''))}"><span class="theme-label">${esc(t.name)}${kind}</span><span>${t.count}</span></button>`;}).join('');
    $('#group-filter').innerHTML='<option value="all">全部主问题</option>'+available.map(t=>`<option value="${esc(t.id)}">${esc(t.name)} · ${t.count}</option>`).join('');
    $('#group-filter').value=state.group;
    const children=state.group==='all'?[]:DATA.subthemes.filter(s=>s.parent_id===state.group).map(s=>({...s,count:state.scope==='all'?s.count:(s.scope_counts[state.scope]||0)})).filter(s=>s.count>0);
    $('#subtheme-list').innerHTML=children.length>0?`<button class="subtheme-chip ${state.sub==='all'?'active':''}" data-subtheme="all" aria-pressed="${state.sub==='all'}">全部具体子问题</button>`+children.map(s=>`<button class="subtheme-chip ${state.sub===s.id?'active':''}" data-subtheme="${esc(s.id)}" aria-pressed="${state.sub===s.id}">${esc(s.name)} · ${s.count}</button>`).join(''):'';
    renderArchiveControl();
  }
  function renderArchiveControl(){
    const holder=$('#subtheme-toolbar'),selected=DATA.subthemes.find(s=>s.id===state.sub),archive=selected?.log_archive;
    holder.hidden=state.group==='all';
    const feature=DATA.features?.daily_log_archive,enabled=feature?.enabled!==false;
    const ready=enabled&&archive?.status==='ready';
    const reason=!enabled?feature.disabled_reason:!selected?'先选择子问题':archive?.disabled_reason||'该子问题暂无日志';
    holder.innerHTML=`<span>具体子问题${ready?` · ${archive.file_count} 个日志 / ${archive.mail_count} 封来信`:''}</span>${ready?`<a class="archive-download" href="${esc(reportURL('/log-archive/'+archive.id))}" download title="下载该子组全部来信的原始日志，不限当前页、搜索或小时筛选">下载该子组全部日志（${archive.file_count} 个） ↓ ZIP</a>`:`<button class="archive-download" disabled title="${esc(reason)}">${esc(reason)}</button>`}`;
  }
  function selectTheme(id,scroll=true,rank=false){
    state.group=id;state.sub='all';state.page=1;
    if(id!=='all'){state.domain=themes.get(id).domain_id;state.scope=rank?'complaint':'all';$('#scope-filter').value=state.scope;}
    if(rank){state.hour=null;state.search='';$('#search').value='';}
    renderThemes();renderTable();if(scroll)$('#evidence').scrollIntoView({behavior:'smooth',block:'start'});
  }
  function selectDomain(id,scroll=true){state.domain=id;state.group='all';state.sub='all';state.scope='all';state.page=1;$('#scope-filter').value='all';renderThemes();renderTable();if(scroll)$('#evidence').scrollIntoView({behavior:'smooth',block:'start'});}
  function compareEvidence(a,b){
    const priority=[...new Set([state.sort,'uid','log','image','document'])];
    for(const key of priority){const delta=Number(!!b.evidence_presence?.[key])-Number(!!a.evidence_presence?.[key]);if(delta)return delta;}
    return parseDate(b.at)-parseDate(a.at)||Number(b.id)-Number(a.id);
  }
  function filtered(){
    const q=state.search.trim().toLowerCase(),idQuery=q.replace(/^#/,''),exactId=DATA.records.some(r=>r.id===idQuery)?idQuery:null;
    return DATA.records.filter(r=>(state.domain==='all'||r.domain_id===state.domain)&&(state.group==='all'||r.theme_id===state.group)&&(state.sub==='all'||r.subtheme_id===state.sub)&&(state.scope==='all'||r.scope===state.scope)&&(state.hour===null||r.hour===state.hour)&&(!q||(exactId?r.id===exactId:(r.search_text||[r.id,r.from,r.mailbox,r.uid.value,r.subject,r.subject_zh,r.summary].join(' ')).toLowerCase().includes(q)))).sort(compareEvidence);
  }
  function filePeek(r,kind){
    const list=r.files.filter(f=>f.kind===kind);if(!list.length)return '<span class="muted">—</span>';
    const f=list[0];let preview;
    if(f.ready&&(f.preview_type==='image'||f.preview_type==='pdf'&&f.preview_image))preview=`<img loading="lazy" src="${esc(reportURL('/file/'+f.id+'/preview'))}" alt="${esc(f.name)}">`;
    else if(f.ready&&f.preview_type==='text')preview=`<pre>${esc(f.preview_head)}</pre>`;
    else preview=`<div class="doc-icon"><strong>${esc((f.name.split('.').pop()||'FILE').slice(0,5).toUpperCase())}</strong>${f.ready?size(f.size):f.availability_exception?'原件未取得':'文件待获取'}</div>`;
    return `<button class="file-peek" data-mail="${r.id}" data-file="${f.id}" aria-label="查看${esc(f.name)}及全部附件"><span class="file-name">${esc(f.name)}</span>${preview}${list.length>1?`<span class="more-files">+${list.length-1}</span>`:''}</button>`;
  }
  function renderTable(){
    $('#evidence-sort').value=state.sort;
    const rows=filtered(),pages=Math.max(1,Math.ceil(rows.length/state.pageSize));state.page=Math.min(state.page,pages);
    const start=(state.page-1)*state.pageSize,shown=rows.slice(start,start+state.pageSize);
    $('#subject-switch').innerHTML=switcher('subject',state.subject);$('#body-switch').innerHTML=switcher('body',state.body);
    $('#result-count').textContent=`筛选 ${rows.length} / 全部 ${DATA.records.length} 封 · ${state.group==='all'?(domains.get(state.domain)?.name||'全部主问题'):themes.get(state.group).name}`;
    const notes=[];
    if(state.sub!=='all')notes.push('子问题：'+(DATA.subthemes.find(s=>s.id===state.sub)?.name||''));
    if(state.hour!==null)notes.push(`小时筛选：${String(state.hour).padStart(2,'0')}:00–${String(state.hour+1).padStart(2,'0')}:00`);
    $('#active-filter').innerHTML=notes.length?`<div class="download-gap">${esc(notes.join(' · '))}</div>`:'';
    $('#mail-rows').innerHTML=shown.map(r=>`<tr data-row="${r.id}"><td><button class="uid" data-mail="${r.id}" aria-label="查看邮件${r.id}的UID依据">${esc(r.uid.value||'—')}</button><br><span class="badge ${['conflict','unverified'].includes(r.uid.state)?'warn':r.uid.value?'teal':''}">${uidNames[r.uid.state]}</span>${roleText(r)}</td><td><div class="email-stack"><div><i>发</i>${esc(r.from||'未记录')}</div><div><i>达</i>${esc(r.mailbox||'未记录')}</div></div></td><td><div class="mail-subject clamp">${esc(state.subject==='original'?(r.subject||'（无主题）'):(r.subject_zh||'未提供主题译文'))}</div><div class="mail-summary">${esc(r.summary)}</div></td><td><div class="clamp mail-body-text">${esc(state.body==='original'?(r.body_preview||'（无正文）'):(r.body_zh_preview||'无正文译文，请查看原文'))}</div><button class="detail-link" data-mail="${r.id}">展开全文 ↗</button></td><td>${filePeek(r,'image')}</td><td>${filePeek(r,'log')}</td><td>${filePeek(r,'document')}</td><td><div class="clamp">${esc(r.theme_name)}</div>${r.subtheme_name!==r.theme_name?`<div class="mail-class">细分：${esc(r.subtheme_name)}</div>`:""}<div class="mail-class"><span class="field-label">系统</span>${esc(r.original_classification.issue_type_name||r.original_classification.issue_type_id||'原三级分类未完成')}</div><span class="badge">${scopeNames[r.scope]}</span><br><span class="badge">${esc(statusNames[r.mail_status]||r.mail_status)}</span></td><td><button class="detail-link" data-mail="${r.id}">详情 ↗</button></td></tr>`).join('');
    $('#empty-result').hidden=rows.length>0;$('#page-range').textContent=rows.length?`第 ${start+1}–${Math.min(start+state.pageSize,rows.length)} 封 · 共 ${rows.length} 封`:'共 0 封';
    $('#page-label').textContent=`${state.page} / ${pages}`;$('[data-page="prev"]').disabled=state.page===1;$('[data-page="next"]').disabled=state.page===pages;
  }
  function drawCharts(){
    charts.splice(0).forEach(c=>c.dispose());
    const css=getComputedStyle(document.documentElement),surface=css.getPropertyValue('--sf').trim(),ink=css.getPropertyValue('--ink').trim(),muted=css.getPropertyValue('--muted').trim(),line=css.getPropertyValue('--line').trim(),blue=css.getPropertyValue('--blue').trim(),red=css.getPropertyValue('--red').trim();
    const draw=(id,labels,values,hourly=false)=>{
      const c=echarts.init($(id),null,{renderer:'svg'});charts.push(c);
      const peak=Math.max(...values),days=Object.keys(DATA.statistics.daily);
      c.setOption({animation:false,textStyle:{fontFamily:'Microsoft YaHei,system-ui,sans-serif'},grid:{left:42,right:24,top:34,bottom:34},tooltip:{trigger:'axis',renderMode:'richText',axisPointer:{type:'shadow'}},xAxis:{type:'category',data:labels,axisLine:{lineStyle:{color:line}},axisTick:{show:false},axisLabel:{color:muted,fontSize:10,interval:hourly?2:1}},yAxis:{type:'value',splitNumber:3,axisLabel:{color:muted,fontSize:10},splitLine:{lineStyle:{color:line}}},series:[{name:'收件量',type:'bar',barMaxWidth:hourly?20:32,data:values.map((n,i)=>({value:n,hour:i,itemStyle:{color:hourly?(i>=15?red:blue):(i===values.length-1?red:blue),opacity:hourly?(i>=15?1:.55):(i===values.length-1?1:.55),borderRadius:[2,2,0,0]}})),label:{show:true,position:'top',fontSize:10,color:ink,formatter:p=>(p.value===peak||(!hourly&&p.dataIndex===values.length-1))?String(p.value):''},markLine:hourly?undefined:{silent:true,symbol:['none','none'],lineStyle:{color:ink,type:'dashed',opacity:.7,width:1},label:{formatter:`前7日日均 ${number(DATA.statistics.previous_seven_average)}`,position:'insideStartTop',fontSize:10,color:muted,backgroundColor:surface,padding:[2,4],borderRadius:3},data:DATA.statistics.previous_seven_average==null?[]:[{yAxis:DATA.statistics.previous_seven_average}]}}]});
      if(hourly)c.on('click',p=>{state.hour=p.data.hour;state.page=1;renderTable();$('#evidence').scrollIntoView({behavior:'smooth'});});
      return c;
    };
    draw('#trend-chart',Object.keys(DATA.statistics.daily).map(d=>d.slice(5)),Object.values(DATA.statistics.daily));
    draw('#hours-chart',DATA.statistics.hours.map((_,i)=>String(i).padStart(2,'0')),DATA.statistics.hours,true);
  }
  function closeDrawer(){drawerGeneration++;$('#overlay').innerHTML='';document.body.style.overflow='';drawerMail=null;if(focusBefore?.isConnected)focusBefore.focus({preventScroll:true});}
  function openOverlay(content){focusBefore=document.activeElement;$('#overlay').innerHTML=`<div class="overlay-bg" data-close></div><aside class="drawer" role="dialog" aria-modal="true" aria-labelledby="drawer-title">${content}</aside>`;document.body.style.overflow='hidden';$('.drawer [data-close]')?.focus();}
  async function openMail(id,fileId){
    const generation=++drawerGeneration;activeFile=fileId||null;drawerSubject=state.subject;drawerBody=state.body;
    openOverlay(`<div class="drawer-head"><h2 id="drawer-title">正在读取邮件 #${esc(id)}</h2><button class="close" data-close>关闭 ✕</button></div><div class="drawer-body"><p class="evidence-note">读取完整原文与全部附件…</p></div>`);
    try{const r=detailCache.get(id)||await getJSON(reportURL(`/mail/${id}`));if(generation!==drawerGeneration)return;if(r.report_sha256!==DATA?.report_sha256)throw new Error('报告已更新，请重新载入页面');detailCache.set(id,r);drawerMail=r;renderMail();$('.drawer [data-close]')?.focus({preventScroll:true});if(fileId){const pane=$('.drawer-body'),section=$('#attachment-section');pane.scrollTop+=section.getBoundingClientRect().top-pane.getBoundingClientRect().top;}}
    catch(error){if(generation===drawerGeneration)$('.drawer-body').innerHTML=`<div class="empty">${esc(error.message)}，请关闭后重试。</div>`;}
  }
  function renderMail(){
    const r=drawerMail;if(!r)return;
    const file=r.files.find(f=>f.id===activeFile)||r.files[0];activeFile=file?.id||null;
    $('.drawer').innerHTML=`<div class="drawer-head"><div><div class="eyebrow">MAIL EVIDENCE / #${r.id}</div><h2 id="drawer-title">${esc(r.theme_name)}</h2></div><button class="close" data-close>关闭 ✕</button></div><div class="drawer-body">
      <dl class="mail-meta"><div><dt>发件邮箱</dt><dd>${esc(r.from||'未记录')}</dd></div><div><dt>送达邮箱（实际采集邮箱）</dt><dd>${esc(r.mailbox||'未记录')}</dd></div><div><dt>原始 To</dt><dd>${esc((r.recipients_original||r.to).map(headerAddress).join('；')||'未记录')}</dd></div><div><dt>原始 Cc</dt><dd>${esc(r.cc.map(headerAddress).join('；')||'未记录')}</dd></div><div><dt>收件时间 · 北京时间</dt><dd>${esc(timestamp(r.at))}</dd></div><div><dt>游戏 UID · 仅文本证据支持</dt><dd><span class="uid">${esc(r.uid.value||'未确认单一值')}</span><br><span class="badge ${r.uid.state==='conflict'?'warn':''}">${uidNames[r.uid.state]}</span>${roleText(r)}</dd></div><div><dt>本次主问题 / 具体子问题</dt><dd>${esc(r.theme_name)}<br>${esc(r.subtheme_name)}</dd></div><div><dt>来信口径 / 系统原三级分类</dt><dd>${esc(scopeNames[r.scope])} · ${esc(statusNames[r.mail_status]||r.mail_status)}<br>${esc(r.original_classification.issue_type_name||r.original_classification.issue_type_id||'原系统未完成')}</dd></div></dl>
      <section class="drawer-section"><h3>本次逐封摘要</h3><p>${esc(r.summary)}</p><p class="evidence-note">归组依据：${esc(r.basis)}</p>${r.secondary_themes.length?`<p class="evidence-note">同封次问题：${esc(r.secondary_themes.map(t=>typeof t==='string'?t:t.name||t.theme_name||t.id).join('；'))}</p>`:''}${r.review_notes?`<p class="evidence-note">复核记录：${esc(typeof r.review_notes==='string'?r.review_notes:JSON.stringify(r.review_notes))}</p>`:''}</section>
      <section class="drawer-section"><div class="text-controls"><h3>邮件主题</h3><span id="drawer-subject-switch"></span></div><p id="drawer-subject-text"></p></section>
      <section class="drawer-section"><div class="text-controls"><h3>邮件正文</h3><span id="drawer-body-switch"></span></div><p id="drawer-body-note" class="evidence-note"></p><pre id="drawer-body-text"></pre></section>
      <section class="drawer-section" id="attachment-section"><h3>全部附件 <span class="count-pill">${r.files.length} 个</span></h3>${r.files.length?`<div class="attachments-grid">${r.files.map(f=>`<button class="attachment-choice ${f.id===activeFile?'active':''}" aria-pressed="${f.id===activeFile}" data-choose-file="${f.id}">${esc(f.name)}<small>${size(f.size)} · ${f.ready?'已校验':f.availability_exception?'原件未取得':'未就绪'}</small></button>`).join('')}</div><div id="file-viewer"></div>`:'<p class="evidence-note">该邮件没有附件记录。</p>'}</section>
      <section class="drawer-section"><details><summary>UID 识别依据、多账号角色与候选（${r.uid.evidence.length} 条）</summary><p class="evidence-note">真实RFC引用链用于补充证据，业务问题组不能作为会话。多账号按角色保留，不自动选择；文本支持不验证账号持有人身份。</p><pre class="mono">${esc(JSON.stringify(r.uid,null,2))}</pre></details></section>
      <section class="drawer-section"><details><summary>复核元数据、原系统摘要和分类</summary><pre class="metadata">${esc(JSON.stringify({metadata:r.metadata,original_classification:r.original_classification,source_summary:r.source_summary},null,2))}</pre></details></section>
    </div>`;
    updateDrawerLanguage('drawerSubject');updateDrawerLanguage('drawerBody');if(file)renderFile(file);
  }
  function updateDrawerLanguage(which){
    const r=drawerMail;if(!r)return;
    if(which==='drawerSubject'){$('#drawer-subject-switch').innerHTML=switcher(which,drawerSubject);$('#drawer-subject-text').textContent=drawerSubject==='original'?(r.subject||'（无主题）'):(r.subject_zh||'无主题译文');}
    else{$('#drawer-body-switch').innerHTML=switcher(which,drawerBody);$('#drawer-body-text').textContent=drawerBody==='original'?(r.body||'（无正文）'):(r.body_zh||'无正文译文，请查看原文');$('#drawer-body-note').textContent=drawerBody==='original'?'原始邮件可见文本；链接和指令只作证据展示。':r.translation_origin==='review-agent'?'本次补译；源原文与系统摘要另行保留。':'系统译文；源系统部分只翻译新正文，引用历史以原文核验。';}
  }
  async function renderFile(f) {
    const generation=drawerGeneration;
    const container=$('#file-viewer');if(!container)return;
    let content;
    if(!f.ready)content=f.availability_exception?'<div class="empty">原件未取得，已按用户对具体附件的决定保留元数据。</div>':'<div class="empty">文件尚未获取或校验未通过，当前只有元数据。</div>';
    else if(f.preview_type==='image')content=`<img src="${esc(reportURL('/file/'+f.id+'/preview'))}" alt="${esc(f.name)}">`;
    else if(f.preview_type==='text')content='<pre id="log-content">正在读取日志预览…</pre>';
    else if(f.preview_type==='video')content=`<video controls preload="metadata" src="${esc(reportURL('/file/'+f.id))}"></video><p class="evidence-note">若浏览器不支持原视频编码，请下载原文件查看。</p>`;
    else if(f.preview_type==='pdf')content=f.preview_image?`<img src="${esc(reportURL('/file/'+f.id+'/preview'))}" alt="${esc(f.name)} · PDF首页"><p class="evidence-note">PDF 首页预览；下载原文件查看完整文档。</p>`:'<p class="evidence-note">PDF 首页预览未生成，请下载原文件查看。</p>';
    else content=`<div class="empty">${esc(f.content_type)}<br>此格式提供元数据与原文件下载，不执行附件内容。</div>`;
    container.innerHTML=`<div class="file-viewer">${content}</div><div class="file-toolbar"><span>${esc(f.name)} · ${size(f.size)}</span>${f.ready?`<a href="${esc(reportURL('/file/'+f.id,{download:'1'}))}" download>下载原文件 ↓</a>`:''}</div><p class="evidence-note method-break">${f.sha256?'SHA-256 · '+esc(f.sha256):'文件尚未校验'}${f.error?' · '+esc(f.error):''}</p>`;
    if(f.ready&&f.preview_type==='text') {
      try{const response=await fetch(reportURL(`/file/${f.id}/preview`));if(!response.ok)throw new Error('日志不可用');const text=await response.text();if(generation===drawerGeneration&&activeFile===f.id&&$('#log-content'))$('#log-content').textContent=text;}
      catch(error){if(generation===drawerGeneration&&activeFile===f.id&&$('#log-content'))$('#log-content').textContent=error.message;}
    }
  }
  function showMethod(){
    const c=DATA.coverage;
    openOverlay(`<div class="drawer-head"><h2 id="drawer-title">统计口径与覆盖</h2><button class="close" data-close>关闭 ✕</button></div><div class="drawer-body"><dl class="method-list">
      <dt>时间与范围</dt><dd>${esc(DATA.business_date)} 00:00–24:00，Asia/Shanghai，RECEIVED；共 ${DATA.statistics.total} 封。24个小时收件数与全量一致。</dd>
      <dt>逐封覆盖与摘要</dt><dd>${c.reviewed}/${c.expected} 封已逐封复核；${c.source_empty_summaries} 封原系统缺摘要，本次已全部补齐。客诉相关来信 ${c.scope_counts.complaint||0}、咨询/回访/其他 ${c.scope_counts.non_complaint||0}、尚无有效线索 ${c.unidentified_count} 封。${c.previous_unclassified_count?`初次待定位 ${c.previous_unclassified_count} 封，经复核恢复 ${c.recovered_count} 封。`:''}</dd>
      <dt>重新归纳的主问题</dt><dd>${esc(DATA.method.grouping)}<br>${esc(DATA.method.count_unit)}<br>原系统三级分类只作线索与复查字段；主问题、子问题、逐封依据和归组修订均保留。</dd>
      <dt>数量及增长率</dt><dd>问题占比以全部 ${DATA.statistics.total} 封为分母。增长率=（当日封数−基准封数）÷基准封数。前7日均值使用未舍入原数计算，展示1位小数；基准为0或缺失时不计算。</dd>
      <dt>UID与邮箱</dt><dd>${esc(DATA.method.uid)}<br>会话核对范围包含本地 ${DATA.uid_review.context_mails} 封邮件头；UID引用的历史原文与真实会话路径均保留证据。发件邮箱、实际送达邮箱、原始To与Cc分别保留。UID识别限制：<br>${DATA.uid_review.limits.map(x=>esc(x)).join('<br>')}</dd>
      <dt>翻译</dt><dd>${esc(DATA.method.translation)}<br>正文译文可用 ${c.body_translations}/${c.expected} 封。空正文与缺译文均保留状态，不能用参考文件的示例正文补齐。</dd>
      <dt>附件</dt><dd>${c.attachments_ready}/${c.attachments_expected} 个原文件通过来源身份与内容校验。${c.attachments_unavailable_authorized?`另有 ${c.attachments_unavailable_authorized} 个原件未取得，已按用户的具体决定保留元数据；涉及缺失日志的子组不提供不完整ZIP。`:''}图片预览从本地原件生成，日志预览有大小上限；已校验原件可下载。格式不支持时说明，不执行附件内容。</dd>
      <dt>数据边界</dt><dd>${esc(DATA.method.limitation)}<br>快照截至 ${esc(timestamp(DATA.source_snapshot_at))}，源 ${esc(DATA.source_id)}，版本 ${DATA.data_version}。</dd>
      <dt>报告指纹</dt><dd class="method-break">${esc(DATA.report_sha256)}</dd></dl></div>`);
  }
  function dateParts(day){const [y,m,d]=day.split('-').map(Number);return {y,m,d};}
  function isoDate(y,m,d){return `${y}-${String(m).padStart(2,'0')}-${String(d).padStart(2,'0')}`;}
  function shiftMonth(y,m,delta){const date=new Date(Date.UTC(y,m-1+delta,1));return {y:date.getUTCFullYear(),m:date.getUTCMonth()+1};}
  function monthLength(y,m){return new Date(Date.UTC(y,m,0)).getUTCDate();}
  function mondayIndex(y,m,d){return (new Date(Date.UTC(y,m-1,d)).getUTCDay()+6)%7;}
  function calendarMarkup(view){
    const ready=new Set(availableDates),today=shanghaiToday(),{y,m}=view,lead=mondayIndex(y,m,1),count=monthLength(y,m);
    const prev=shiftMonth(y,m,-1),prevCount=monthLength(prev.y,prev.m),next=shiftMonth(y,m,1),cells=[];
    for(let i=0;i<42;i++){
      let cy=y,cm=m,cd=i-lead+1,outside=false;
      if(i<lead){cy=prev.y;cm=prev.m;cd=prevCount-lead+1+i;outside=true;}
      else if(cd>count){cy=next.y;cm=next.m;cd=i-lead-count+1;outside=true;}
      const iso=isoDate(cy,cm,cd),has=ready.has(iso),selected=iso===selectedDate,isToday=iso===today;
      cells.push(`<button type="button" class="ios-day${outside?' is-outside':''}${selected?' is-selected':''}${isToday?' is-today':''}" data-cal-day="${iso}" aria-pressed="${selected}" aria-label="${cy}年${cm}月${cd}日${has?'，已生成日报':''}${isToday?'，今天':''}"><span class="ios-day-num">${cd}</span>${has?'<span class="ios-dot"></span>':''}</button>`);
    }
    return `<div class="ios-cal-head"><button type="button" class="ios-cal-nav" data-cal-shift="-1" aria-label="上个月"><svg viewBox="0 0 12 20"><path d="M10 2 2 10l8 8"></path></svg></button><div class="ios-cal-title">${y}年${m}月</div><button type="button" class="ios-cal-nav" data-cal-shift="1" aria-label="下个月"><svg viewBox="0 0 12 20"><path d="M2 2l8 8-8 8"></path></svg></button></div><div class="ios-weekdays">${'一二三四五六日'.split('').map(day=>`<span>${day}</span>`).join('')}</div><div class="ios-grid">${cells.join('')}</div><p class="ios-cal-note"><i class="ios-dot"></i>已生成日报</p>`;
  }
  function closeCalendar(){calendarView=null;const pop=$('#ios-cal'),trigger=$('#report-date');if(pop)pop.hidden=true;if(trigger)trigger.setAttribute('aria-expanded','false');}
  function openCalendar(){const base=dateParts(validDate(selectedDate)?selectedDate:shanghaiToday());calendarView={y:base.y,m:base.m};const pop=$('#ios-cal');if(!pop)return;pop.innerHTML=calendarMarkup(calendarView);pop.hidden=false;$('#report-date')?.setAttribute('aria-expanded','true');}
  document.addEventListener('click',event=>{
    const b=event.target.closest('button,[data-close]');
    if(b?.hasAttribute('data-cal-toggle')){if(calendarView)closeCalendar();else openCalendar();return;}
    if(b?.hasAttribute('data-cal-shift')){if(!calendarView)return;calendarView=shiftMonth(calendarView.y,calendarView.m,Number(b.dataset.calShift));const pop=$('#ios-cal');if(pop)pop.innerHTML=calendarMarkup(calendarView);return;}
    if(b?.hasAttribute('data-cal-day'))return loadReport(b.dataset.calDay,'push');
    if(calendarView&&!event.target.closest('.ios-date'))closeCalendar();
    if(!b)return;
    if(b.hasAttribute('data-close'))return closeDrawer();
    if(b.hasAttribute('data-default'))return loadReport(null,'push');
    if(b.hasAttribute('data-method'))return showMethod();
    if(b.hasAttribute('data-all-groups'))return selectDomain('all');
    if(b.hasAttribute('data-domain'))return selectDomain(b.dataset.domain);
    if(b.hasAttribute('data-rank-theme'))return selectTheme(b.dataset.rankTheme,true,true);
    if(b.hasAttribute('data-theme'))return selectTheme(b.dataset.theme);
    if(b.hasAttribute('data-subtheme')){state.sub=b.dataset.subtheme;state.page=1;renderThemes();renderTable();return;}
    if(b.hasAttribute('data-mail'))return openMail(b.dataset.mail,b.dataset.file);
    if(b.hasAttribute('data-mode')){
      const [which,mode]=b.dataset.mode.split(':');
      if(which==='drawerSubject'){drawerSubject=mode;updateDrawerLanguage(which);}
      else if(which==='drawerBody'){drawerBody=mode;updateDrawerLanguage(which);}
      else{state[which]=mode;renderTable();}
      document.querySelector(`[data-mode="${which}:${mode}"]`)?.focus({preventScroll:true});return;
    }
    if(b.hasAttribute('data-choose-file')){
      const f=drawerMail?.files.find(f=>f.id===b.dataset.chooseFile);if(!f)return;activeFile=f.id;
      document.querySelectorAll('.attachment-choice').forEach(n=>{n.classList.toggle('active',n.dataset.chooseFile===f.id);n.setAttribute('aria-pressed',String(n.dataset.chooseFile===f.id));});
      renderFile(f);return;
    }
    if(b.hasAttribute('data-reset')){Object.assign(state,{domain:'all',group:'all',sub:'all',scope:'all',hour:null,search:'',page:1,sort:'uid'});$('#search').value='';$('#scope-filter').value='all';renderThemes();renderTable();return;}
    if(b.hasAttribute('data-page')){state.page+=b.dataset.page==='next'?1:-1;renderTable();$('.table-scroll').scrollTop=0;return;}
    if(b.hasAttribute('data-retry'))loadReport(new URL(location.href).searchParams.get('date'));
  });
  document.addEventListener('input',event=>{if(event.target.id==='search'){state.search=event.target.value;state.page=1;renderTable();}});
  document.addEventListener('change',event=>{const t=event.target;if(t.id==='report-history'){if(t.value)loadReport(t.value,'push');return;}if(t.id==='evidence-sort'){state.sort=t.value;state.page=1;renderTable();}if(t.id==='scope-filter'){state.scope=t.value;state.sub='all';state.page=1;renderThemes();renderTable();}if(t.id==='group-filter')selectTheme(t.value,false);if(t.id==='page-size'){state.pageSize=Number(t.value);state.page=1;renderTable();}});
  document.addEventListener('keydown',event=>{
    if(event.key==='Escape'&&calendarView){closeCalendar();return;}
    const drawer=$('.drawer');if(!drawer)return;if(event.key==='Escape'){closeDrawer();return;}
    if(event.key==='Tab'){const all=[...drawer.querySelectorAll('button,a[href],select,summary,iframe')].filter(x=>!x.disabled),first=all[0],last=all.at(-1);if(event.shiftKey&&document.activeElement===first){last?.focus();event.preventDefault();}else if(!event.shiftKey&&document.activeElement===last){first?.focus();event.preventDefault();}else if(!drawer.contains(document.activeElement)){first?.focus();event.preventDefault();}}
  });
  window.addEventListener('resize',()=>charts.forEach(c=>c.resize()));
  window.addEventListener('popstate',()=>loadReport(new URL(location.href).searchParams.get('date')));
  loadReport(new URL(location.href).searchParams.get('date'));
})();

