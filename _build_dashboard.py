# -*- coding: utf-8 -*-
import json
data=json.load(open('_clients.json'))
DATA=json.dumps(data,ensure_ascii=False)
HTML=r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Meridante — Outreach Dashboard</title>
<meta name="robots" content="noindex,nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,400&family=Archivo:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{--navy:#0c1322;--navy2:#11192b;--panel:#141d31;--brass:#c2974a;--ivory:#f3eee4;--mut:#9aa3b4;--line:rgba(243,238,228,.12);--ok:#3f9d6d;--okbg:#15241c}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--navy);color:var(--ivory);font:14px/1.5 Archivo,sans-serif;-webkit-font-smoothing:antialiased}
a{color:inherit}
.bar{position:sticky;top:0;z-index:30;background:rgba(12,19,34,.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.bar .in{max-width:1280px;margin:0 auto;padding:14px 24px;display:flex;align-items:center;gap:18px;flex-wrap:wrap}
.brand{font-family:Fraunces,serif;font-size:20px}.brand b{color:var(--brass);font-weight:600}
.kpis{display:flex;gap:18px;margin-left:auto;flex-wrap:wrap}
.kpi{text-align:center}.kpi b{font-family:Fraunces,serif;font-size:20px;display:block;line-height:1}.kpi span{font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--mut)}
.me{display:flex;align-items:center;gap:8px}
.me input{background:var(--panel);border:1px solid var(--line);border-radius:8px;color:var(--ivory);padding:8px 11px;font:13px Archivo;width:150px}
.me input:focus{outline:none;border-color:var(--brass)}
.sync{font-size:11px;color:var(--mut);display:flex;align-items:center;gap:6px}.dot{width:8px;height:8px;border-radius:50%;background:#b5763f}.dot.on{background:var(--ok)}
.tools{max-width:1280px;margin:0 auto;padding:16px 24px 4px;display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.tools input.q{flex:1;min-width:220px;background:var(--navy2);border:1px solid var(--line);border-radius:10px;color:var(--ivory);padding:10px 13px;font:14px Archivo}
.tools input.q:focus{outline:none;border-color:var(--brass)}
.seg{display:flex;border:1px solid var(--line);border-radius:10px;overflow:hidden}
.seg button{background:none;border:0;color:var(--mut);font:13px Archivo;padding:9px 14px;cursor:pointer}
.seg button.on{background:var(--brass);color:var(--navy);font-weight:600}
.chips{display:flex;gap:7px;flex-wrap:wrap}
.chip{font-size:12px;color:var(--mut);border:1px solid var(--line);border-radius:999px;padding:7px 12px;cursor:pointer;user-select:none}
.chip.on{border-color:var(--brass);color:var(--brass)}
.toggle{font-size:12.5px;color:var(--mut);display:flex;align-items:center;gap:7px;cursor:pointer}
main{max-width:1280px;margin:0 auto;padding:14px 24px 80px}
h2.country{font-family:Fraunces,serif;font-weight:400;font-size:24px;margin:26px 0 12px;display:flex;align-items:center;gap:12px;border-bottom:2px solid var(--brass);padding-bottom:8px}
h2.country .n{font-size:13px;color:var(--mut);font-family:Archivo}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:16px}
.card{background:var(--navy2);border:1px solid var(--line);border-radius:14px;padding:18px;display:flex;flex-direction:column;gap:11px;transition:.2s}
.card.sent{background:var(--okbg);border-color:rgba(63,157,109,.4)}
.card .top{display:flex;justify-content:space-between;align-items:flex-start;gap:8px}
.card h3{font-family:Fraunces,serif;font-weight:500;font-size:18px;line-height:1.15}
.meta{font-size:12px;color:var(--mut);margin-top:2px}
.status{font:700 9px ui-monospace,monospace;color:#fff;padding:3px 7px;border-radius:5px;white-space:nowrap}
.links{display:flex;gap:8px;flex-wrap:wrap}
.lk{font-size:12px;text-decoration:none;border:1px solid var(--line);border-radius:7px;padding:6px 10px;color:var(--ivory)}
.lk:hover{border-color:var(--brass);color:var(--brass)}
.lk.demo{background:var(--brass);color:var(--navy);border-color:var(--brass);font-weight:600}
.field{display:flex;align-items:center;gap:8px;background:var(--panel);border:1px solid var(--line);border-radius:9px;padding:8px 11px}
.field .v{flex:1;font:12.5px ui-monospace,monospace;color:#d8d2c6;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.cp{background:none;border:1px solid var(--line);border-radius:6px;color:var(--mut);font:11px Archivo;padding:5px 9px;cursor:pointer;white-space:nowrap}
.cp:hover{border-color:var(--brass);color:var(--brass)}
details summary{cursor:pointer;font-size:12.5px;color:var(--brass);list-style:none}
details summary::-webkit-details-marker{display:none}
textarea{width:100%;height:150px;margin-top:8px;background:var(--panel);border:1px solid var(--line);border-radius:9px;color:#e7e2d6;padding:10px;font:12px/1.5 ui-monospace,monospace;resize:vertical}
.draftbtns{display:flex;gap:8px;margin-top:8px}
.btn{font:12.5px Archivo;padding:8px 12px;border-radius:8px;border:1px solid var(--line);color:var(--ivory);text-decoration:none;cursor:pointer;background:none}
.btn.p{background:var(--brass);color:var(--navy);border-color:var(--brass);font-weight:600}.btn:hover{border-color:var(--brass)}
.sent-row{display:flex;align-items:center;gap:10px;margin-top:2px;padding-top:11px;border-top:1px solid var(--line)}
.sw{position:relative;width:44px;height:24px;flex:none}
.sw input{opacity:0;width:0;height:0}
.sw label{position:absolute;inset:0;background:#2a3346;border-radius:999px;cursor:pointer;transition:.2s}
.sw label::after{content:"";position:absolute;top:3px;left:3px;width:18px;height:18px;background:#fff;border-radius:50%;transition:.2s}
.sw input:checked + label{background:var(--ok)}.sw input:checked + label::after{transform:translateX(20px)}
.sent-info{font-size:12px;color:var(--mut)}.sent-info b{color:var(--ok)}
.empty{color:var(--mut);text-align:center;padding:50px;font-size:14px}
.note{max-width:1280px;margin:0 auto;padding:0 24px;color:#69728a;font-size:11.5px}
@media(max-width:640px){.kpis{order:3;width:100%;justify-content:space-between}.me input{width:120px}}
</style></head><body>
<div class="bar"><div class="in">
  <div class="brand"><b>Meridante</b> · Outreach</div>
  <div class="me"><span class="sync"><span class="dot" id="dot"></span><span id="syncTxt">local</span></span>
    <input id="me" placeholder="Your name" title="Your name (stamped when you mark Sent)"></div>
  <div class="kpis">
    <div class="kpi"><b id="kTotal">0</b><span>Clients</span></div>
    <div class="kpi"><b id="kSent" style="color:var(--ok)">0</b><span>Sent</span></div>
    <div class="kpi"><b id="kLeft">0</b><span>To send</span></div>
  </div>
</div></div>
<div class="tools">
  <input class="q" id="q" placeholder="Search company, city, sector, email…">
  <div class="seg" id="cseg"><button data-c="" class="on">All</button><button data-c="Luxembourg">🇱🇺 LU</button><button data-c="Portugal">🇵🇹 PT</button></div>
  <div class="chips" id="status"></div>
  <label class="toggle"><input type="checkbox" id="unsent"> Unsent only</label>
</div>
<p class="note" id="modeNote"></p>
<main id="main"></main>
<script>
(function(){var P="meridante2026";if(sessionStorage.getItem('mok')==='1')return;var e=prompt('Meridante — team passphrase:');if(e!==P){document.documentElement.innerHTML='<body style="font-family:sans-serif;background:#0c1322;color:#9aa3b4;padding:50px">Access restricted — Meridante team only.</body>';throw 'locked';}sessionStorage.setItem('mok','1');})();
const CONFIG={ENDPOINT:""}; // ← set to the Apps Script Web App URL for team sync
const CLIENTS=__DATA__;
const SC={'BROKEN':'#c0392b','NO-SITE':'#2c3e50','NOT-MOBILE':'#d35400','OUTDATED':'#b8860b','DATED-BUILDER':'#9a7d0a','TEMPLATE-BASIC':'#7d3c98','OUTDATED / DATED-BUILDER':'#9a7d0a','NOT-MOBILE / OUTDATED':'#d35400'};
let STATE={}, filterC="", filterS="", q="", unsentOnly=false;
const esc=s=>(s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const me=()=>document.getElementById('me').value.trim();
function persist(id){ const st=STATE[id]||{};
  if(CONFIG.ENDPOINT){ fetch(CONFIG.ENDPOINT,{method:'POST',body:JSON.stringify({id,...st})}).catch(()=>{}); }
  localStorage.setItem('meridante_state',JSON.stringify(STATE)); }
async function loadState(){
  if(CONFIG.ENDPOINT){ try{ const r=await fetch(CONFIG.ENDPOINT+'?t='+Date.now()); STATE=await r.json()||{};
      document.getElementById('dot').classList.add('on'); document.getElementById('syncTxt').textContent='team synced'; }
    catch(e){ STATE=JSON.parse(localStorage.getItem('meridante_state')||'{}'); } }
  else STATE=JSON.parse(localStorage.getItem('meridante_state')||'{}');
  document.getElementById('me').value=localStorage.getItem('meridante_me')||'';
}
function toggle(id,checked){ if(checked){ if(!me()){alert('Enter your name (top bar) first — so the team knows who sent it.');render();return;} STATE[id]={sent:true,by:me(),date:new Date().toISOString().slice(0,10)};}
  else STATE[id]={sent:false,by:'',date:''}; persist(id); render(); }
function copy(t,btn){ navigator.clipboard.writeText(t).then(()=>{const o=btn.textContent;btn.textContent='Copied ✓';setTimeout(()=>btn.textContent=o,1100);}); }
function card(c){ const st=STATE[c.id]||{}; const sent=st.sent;
  const site=(c.website&&!/^none/i.test(c.website))?`<a class=lk href="${/^http/.test(c.website)?esc(c.website):'https://'+esc(c.website)}" target=_blank>Current site ↗</a>`:`<span class=lk style="color:#b0392b">no website</span>`;
  const demo=c.demo?`<a class="lk demo" href="${esc(c.demo)}" target=_blank>Live demo ↗</a>`:'';
  return `<div class="card${sent?' sent':''}">
   <div class=top><div><h3>${esc(c.company)}</h3><div class=meta>${esc(c.sector)} · ${esc(c.city)} · <span style="opacity:.7">${esc(c.batch)}</span></div></div>
     <span class=status style="background:${SC[c.status]||'#555'}">${esc(c.status)}</span></div>
   <div class=links>${site}${demo}</div>
   <div class=field><span class=v>${esc(c.email)}</span><button class=cp onclick='copy(${JSON.stringify(c.email)},this)'>Copy email</button></div>
   <details><summary>✉ Email draft — view / copy</summary>
     <textarea readonly>${esc('Subject: '+c.subject+'\n\n'+c.body)}</textarea>
     <div class=draftbtns><button class="btn p" onclick='copy(${JSON.stringify("Subject: "+c.subject+"\n\n"+c.body)},this)'>Copy draft</button>
       <a class=btn href="${esc(c.gmail)}" target=_blank>Open in Gmail ↗</a></div></details>
   <div class=sent-row><span class=sw><input type=checkbox id="s_${c.id}" ${sent?'checked':''} onchange="toggle('${c.id}',this.checked)"><label for="s_${c.id}"></label></span>
     <span class=sent-info>${sent?`<b>✓ Sent</b> by ${esc(st.by||'?')} · ${esc(st.date||'')}`:'Not sent'}</span></div>
  </div>`; }
function render(){
  const list=CLIENTS.filter(c=>{
    if(filterC&&c.country!==filterC)return false;
    if(filterS&&c.status!==filterS)return false;
    if(unsentOnly&&(STATE[c.id]||{}).sent)return false;
    if(q){const h=(c.company+' '+c.city+' '+c.sector+' '+c.email).toLowerCase();if(!h.includes(q))return false;}
    return true;});
  const sentN=CLIENTS.filter(c=>(STATE[c.id]||{}).sent).length;
  document.getElementById('kTotal').textContent=CLIENTS.length;
  document.getElementById('kSent').textContent=sentN;
  document.getElementById('kLeft').textContent=CLIENTS.length-sentN;
  const m=document.getElementById('main'); m.innerHTML='';
  const countries=[['Luxembourg','🇱🇺 Luxembourg'],['Portugal','🇵🇹 Portugal']];
  let any=false;
  countries.forEach(([code,label])=>{
    const rows=list.filter(c=>c.country===code); if(!rows.length)return; any=true;
    const s=rows.filter(c=>(STATE[c.id]||{}).sent).length;
    m.innerHTML+=`<h2 class=country>${label} <span class=n>${rows.length} clients · ${s} sent</span></h2><div class=grid>${rows.map(card).join('')}</div>`;
  });
  if(!any)m.innerHTML='<div class=empty>No clients match these filters.</div>';
}
function buildStatusChips(){ const sts=[...new Set(CLIENTS.map(c=>c.status))].sort();
  const el=document.getElementById('status'); 
  el.innerHTML=`<span class="chip on" data-s="">All status</span>`+sts.map(s=>`<span class=chip data-s="${esc(s)}">${esc(s)}</span>`).join('');
  el.querySelectorAll('.chip').forEach(ch=>ch.onclick=()=>{filterS=ch.dataset.s;el.querySelectorAll('.chip').forEach(x=>x.classList.toggle('on',x===ch));render();}); }
document.getElementById('cseg').querySelectorAll('button').forEach(b=>b.onclick=()=>{filterC=b.dataset.c;document.querySelectorAll('#cseg button').forEach(x=>x.classList.toggle('on',x===b));render();});
document.getElementById('q').oninput=e=>{q=e.target.value.toLowerCase();render();};
document.getElementById('unsent').onchange=e=>{unsentOnly=e.target.checked;render();};
document.getElementById('me').oninput=e=>localStorage.setItem('meridante_me',e.target.value);
document.getElementById('modeNote').textContent=CONFIG.ENDPOINT?'Team-synced via shared Google Sheet.':'Local mode — sent-status saves on this device only. Connect the team sheet to sync across everyone (ask João).';
buildStatusChips();
loadState().then(()=>{render(); if(CONFIG.ENDPOINT)setInterval(()=>loadState().then(render),20000);});
</script></body></html>'''
open('index.html','w').write(HTML.replace('__DATA__',DATA))
print('dashboard index.html written;', len(data),'clients embedded;', len(open("index.html").read())//1024,'KB')
