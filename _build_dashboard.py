# -*- coding: utf-8 -*-
import json
data=json.load(open('_clients.json'))
DATA=json.dumps(data,ensure_ascii=False)
HTML=r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Meridante — Outreach Console</title>
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#0a1020">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ccircle cx='16' cy='16' r='15' fill='%230a1020' stroke='%23cba75a' stroke-width='2'/%3E%3Cpath d='M16 3a13 13 0 0 0 0 26M3 16h26' fill='none' stroke='%23cba75a' stroke-width='1.4' opacity='.7'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400&family=Archivo:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#080d1a;--bg2:#0b1222;--surf:#101a2e;--surf2:#142036;--panel:#16223a;
  --brass:#cba75a;--brass2:#e7cd86;--ivory:#f4efe6;--mut:#9aa6bd;--mut2:#6c7790;
  --line:rgba(244,239,230,.10);--line2:rgba(244,239,230,.16);
  --ok:#48bd84;--okbg:rgba(72,189,132,.10);--okline:rgba(72,189,132,.38);
  --shadow:0 18px 50px -20px rgba(0,0,0,.7);
}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%}
body{
  background:
    radial-gradient(1200px 600px at 80% -10%,rgba(203,167,90,.10),transparent 60%),
    radial-gradient(900px 500px at 0% 0%,rgba(72,120,200,.07),transparent 55%),
    var(--bg);
  color:var(--ivory);font:14px/1.55 Archivo,system-ui,sans-serif;-webkit-font-smoothing:antialiased;
  min-height:100vh;
}
a{color:inherit;text-decoration:none}
::selection{background:rgba(203,167,90,.3)}
.wrap{max-width:1320px;margin:0 auto;padding:0 clamp(14px,3vw,28px)}

/* ===== Header ===== */
.bar{position:sticky;top:0;z-index:40;background:rgba(8,13,26,.82);backdrop-filter:blur(16px) saturate(140%);-webkit-backdrop-filter:blur(16px) saturate(140%);border-bottom:1px solid var(--line)}
.bar .in{display:flex;align-items:center;gap:16px;padding:13px 0}
.brand{display:flex;align-items:center;gap:12px;min-width:0}
.logo{width:34px;height:34px;border-radius:50%;flex:none;background:radial-gradient(circle at 35% 30%,var(--brass2),var(--brass) 55%,#8a6f33);box-shadow:0 0 0 1px rgba(231,205,134,.4),0 6px 16px -6px rgba(203,167,90,.6);position:relative}
.logo::after{content:"";position:absolute;inset:6px;border-radius:50%;border:1px solid rgba(8,13,26,.55);border-top-color:transparent;border-left-color:transparent}
.brand .t{line-height:1.05;min-width:0}
.brand b{font-family:Fraunces,serif;font-weight:600;font-size:19px;letter-spacing:.01em;display:block}
.brand small{font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--mut2)}
.grow{flex:1}
.me{display:flex;align-items:center;gap:10px;flex:none}
.me input{background:var(--surf);border:1px solid var(--line2);border-radius:10px;color:var(--ivory);padding:9px 12px;font:13px Archivo;width:150px;transition:.2s}
.me input::placeholder{color:var(--mut2)}
.me input:focus{outline:none;border-color:var(--brass);background:var(--surf2)}
.me select{background:var(--surf) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M1 1l4 4 4-4' fill='none' stroke='%23cba75a' stroke-width='1.6'/%3E%3C/svg%3E") no-repeat right 12px center;border:1px solid var(--line2);border-radius:10px;color:var(--ivory);padding:9px 30px 9px 12px;font:13px Archivo;min-width:150px;transition:.2s;-webkit-appearance:none;appearance:none;cursor:pointer}
.me select:focus{outline:none;border-color:var(--brass);background-color:var(--surf2)}
.me select option{background:#101a2e;color:var(--ivory)}
.sync{display:flex;align-items:center;gap:7px;font-size:11px;color:var(--mut);white-space:nowrap}
.guidebtn{background:linear-gradient(180deg,var(--brass2),var(--brass));color:#1a1305;border:0;font:600 12.5px Archivo;padding:9px 14px;border-radius:10px;cursor:pointer;white-space:nowrap;box-shadow:0 4px 12px -4px rgba(203,167,90,.55);transition:.18s}
.guidebtn:hover{filter:brightness(1.06);transform:translateY(-1px)}
.modal{position:fixed;inset:0;z-index:100;background:rgba(4,7,14,.72);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);display:none;align-items:flex-start;justify-content:center;padding:5vh 16px;overflow-y:auto}
.modal.open{display:flex}
.sheet{background:linear-gradient(165deg,var(--surf),var(--bg2));border:1px solid var(--line2);border-radius:20px;max-width:820px;width:100%;padding:26px clamp(18px,3vw,32px) 22px;position:relative;box-shadow:var(--shadow);animation:pop .25s cubic-bezier(.2,.8,.3,1)}
@keyframes pop{from{opacity:0;transform:translateY(14px) scale(.98)}to{opacity:1;transform:none}}
.sheet .x{position:absolute;top:16px;right:16px;background:var(--surf2);border:1px solid var(--line2);color:var(--mut);width:34px;height:34px;border-radius:50%;cursor:pointer;font-size:14px;transition:.18s}
.sheet .x:hover{color:var(--ivory);border-color:var(--brass)}
.ghead{display:flex;align-items:center;gap:13px;padding-bottom:16px;border-bottom:1px solid var(--line)}
.ghead b{font-family:Fraunces,serif;font-weight:600;font-size:20px;display:block}
.ghead small{color:var(--mut2);font-size:11.5px}
.gbody{display:grid;gap:13px;margin-top:18px}
.gcard{background:var(--surf);border:1px solid var(--line);border-radius:14px;padding:16px 18px}
.gcard.hi{border-color:var(--brass);background:rgba(203,167,90,.06);box-shadow:0 12px 30px -20px rgba(203,167,90,.5)}
.gcard h4{font-family:Fraunces,serif;font-weight:600;font-size:15.5px;color:var(--brass2);margin-bottom:9px}
.gcard.hi h4{color:var(--brass2)}
.gcard p{color:var(--mut);font-size:13px;margin:6px 0}
.gcard ol,.gcard ul{margin:6px 0 0 18px;display:flex;flex-direction:column;gap:6px}
.gcard li{font-size:13px;color:var(--ivory);line-height:1.5}
.gcard b{color:var(--ivory)}.gcard i{color:var(--brass2);font-style:normal}
.gcard code{background:var(--bg);border:1px solid var(--line2);border-radius:6px;padding:1px 6px;font:12px ui-monospace,monospace;color:var(--brass2)}
.ptab{width:100%;border-collapse:collapse;margin-top:10px;font-size:12.5px}
.ptab th,.ptab td{text-align:left;padding:7px 9px;border-bottom:1px solid var(--line)}
.ptab th{color:var(--mut2);font-size:10.5px;font-weight:600;letter-spacing:.04em}
.ptab th span{color:var(--mut2);font-weight:400;font-size:9px;letter-spacing:.02em}
.ptab td:first-child{color:var(--ivory)}
.ptab td:not(:first-child){font-family:Fraunces,serif;color:var(--ivory);font-size:14px}
.ptab tr.star td{color:var(--brass2)}.ptab tr.star td:not(:first-child){color:var(--brass2)}
.fine{font-size:11.5px;color:var(--mut2) !important;margin-top:9px !important}
.gfoot{margin-top:16px;padding-top:14px;border-top:1px solid var(--line);font-size:11px;color:var(--mut2);text-align:center}
.gfoot code{font:11px ui-monospace,monospace;color:var(--mut)}
.dot{width:8px;height:8px;border-radius:50%;background:#c08a3e;box-shadow:0 0 0 3px rgba(192,138,62,.16)}
.dot.on{background:var(--ok);box-shadow:0 0 0 3px rgba(72,189,132,.18)}
/* progress line under header */
.gprog{height:3px;background:rgba(244,239,230,.07)}
.gprog i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--brass),var(--brass2));box-shadow:0 0 12px rgba(203,167,90,.6);transition:width .6s cubic-bezier(.4,0,.2,1)}

/* ===== Stat strip ===== */
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:22px 0 6px}
.stat{background:linear-gradient(160deg,var(--surf),var(--bg2));border:1px solid var(--line);border-radius:16px;padding:15px 17px;position:relative;overflow:hidden}
.stat::before{content:"";position:absolute;inset:0 auto 0 0;width:3px;background:var(--brass);opacity:.0;transition:.3s}
.stat.acc::before{opacity:.9}
.stat .lab{font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;color:var(--mut2);margin-bottom:7px}
.stat .num{font-family:Fraunces,serif;font-weight:600;font-size:clamp(26px,4vw,34px);line-height:1;letter-spacing:-.01em}
.stat.s-sent .num{color:var(--ok)}
.stat.s-pct .num{color:var(--brass2)}
.ring{position:absolute;right:14px;top:50%;transform:translateY(-50%);width:46px;height:46px}

/* ===== Toolbar ===== */
.tools{position:sticky;top:53px;z-index:30;background:rgba(8,13,26,.72);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);padding:12px 0;margin-top:14px;border-bottom:1px solid var(--line)}
.tools .row1{display:flex;gap:10px;align-items:center}
.search{position:relative;flex:1;min-width:0}
.search svg{position:absolute;left:13px;top:50%;transform:translateY(-50%);width:16px;height:16px;color:var(--mut2);pointer-events:none}
.search input{width:100%;background:var(--surf);border:1px solid var(--line2);border-radius:12px;color:var(--ivory);padding:11px 14px 11px 38px;font:14px Archivo;transition:.2s}
.search input::placeholder{color:var(--mut2)}
.search input:focus{outline:none;border-color:var(--brass);background:var(--surf2);box-shadow:0 0 0 3px rgba(203,167,90,.12)}
.seg{display:flex;background:var(--surf);border:1px solid var(--line2);border-radius:12px;padding:3px;flex:none}
.seg button{background:none;border:0;color:var(--mut);font:13px Archivo;padding:8px 14px;cursor:pointer;border-radius:9px;transition:.18s;white-space:nowrap}
.seg button.on{background:linear-gradient(180deg,var(--brass2),var(--brass));color:#1a1305;font-weight:600;box-shadow:0 4px 12px -4px rgba(203,167,90,.6)}
.row2{display:flex;gap:8px;align-items:center;margin-top:11px;overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch;padding-bottom:2px}
.row2::-webkit-scrollbar{display:none}
.chip{font-size:12px;color:var(--mut);background:var(--surf);border:1px solid var(--line);border-radius:999px;padding:7px 13px;cursor:pointer;user-select:none;white-space:nowrap;flex:none;transition:.18s}
.chip:hover{border-color:var(--line2);color:var(--ivory)}
.chip.on{border-color:var(--brass);color:var(--brass2);background:rgba(203,167,90,.10)}
.toggle{display:flex;align-items:center;gap:8px;font-size:12.5px;color:var(--mut);cursor:pointer;white-space:nowrap;flex:none;margin-left:auto;padding:7px 4px}
.toggle input{accent-color:var(--brass);width:15px;height:15px}
.note{color:var(--mut2);font-size:11.5px;margin:12px 0 0}

/* ===== Sections ===== */
main{padding:8px 0 90px}
.country{display:flex;align-items:center;gap:14px;margin:30px 0 16px}
.country h2{font-family:Fraunces,serif;font-weight:500;font-size:clamp(20px,3.4vw,26px);display:flex;align-items:center;gap:10px;white-space:nowrap}
.country .cbar{flex:1;height:5px;border-radius:999px;background:rgba(244,239,230,.08);overflow:hidden;max-width:340px}
.country .cbar i{display:block;height:100%;background:linear-gradient(90deg,var(--ok),#6fe0a8);transition:width .6s}
.country .cn{font-size:12.5px;color:var(--mut);font-family:Archivo;white-space:nowrap}
.country .cn b{color:var(--ivory)}

.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:18px}

/* ===== Card ===== */
.card{background:linear-gradient(170deg,var(--surf),var(--bg2));border:1px solid var(--line);border-radius:18px;overflow:hidden;display:flex;flex-direction:column;transition:transform .25s cubic-bezier(.2,.7,.3,1),box-shadow .25s,border-color .25s}
.card:hover{transform:translateY(-4px);box-shadow:var(--shadow);border-color:var(--line2)}
.card.sent{border-color:var(--okline)}
.card.sent .thumb::after{opacity:1}

.thumb{display:block;position:relative;aspect-ratio:16/9;background:linear-gradient(135deg,var(--panel),#0a1020);overflow:hidden}
.thumb .ph{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-family:Fraunces,serif;font-size:54px;color:rgba(203,167,90,.32)}
.thumb img{position:relative;width:100%;height:100%;object-fit:cover;object-position:top;display:block;transition:transform .5s cubic-bezier(.2,.7,.3,1)}
.card:hover .thumb img{transform:scale(1.06)}
.thumb::before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,13,26,.05),rgba(8,13,26,.55));z-index:1}
.thumb::after{content:"";position:absolute;inset:0;box-shadow:inset 0 0 0 2px var(--okline);opacity:0;transition:.3s;z-index:2;pointer-events:none}
.badge{position:absolute;top:11px;left:11px;z-index:3;font:600 9.5px/1 ui-monospace,monospace;letter-spacing:.04em;color:#fff;padding:5px 8px;border-radius:6px;background:rgba(8,13,26,.5);backdrop-filter:blur(4px);border:1px solid rgba(255,255,255,.14);box-shadow:0 2px 8px rgba(0,0,0,.4)}
.badge i{display:inline-block;width:6px;height:6px;border-radius:50%;background:var(--c,#888);margin-right:5px;vertical-align:middle}
.flag{position:absolute;top:11px;right:11px;z-index:3;font:600 10px Archivo;color:#062013;background:linear-gradient(180deg,#6fe0a8,var(--ok));padding:5px 9px;border-radius:999px;box-shadow:0 4px 12px -3px rgba(72,189,132,.7)}
.live{position:absolute;bottom:11px;right:11px;z-index:3;font:600 11px Archivo;color:#1a1305;background:linear-gradient(180deg,var(--brass2),var(--brass));padding:6px 11px;border-radius:8px;box-shadow:0 4px 12px -4px rgba(203,167,90,.7);opacity:.96}

.body{padding:15px 16px 16px;display:flex;flex-direction:column;gap:11px;flex:1}
.body h3{font-family:Fraunces,serif;font-weight:500;font-size:18.5px;line-height:1.18}
.meta{font-size:12px;color:var(--mut);margin-top:3px}
.meta .b{color:var(--mut2)}
.cursite{font-size:12px;color:var(--mut);display:inline-flex;align-items:center;gap:5px}
.cursite a{border-bottom:1px solid var(--line2);color:var(--ivory);transition:.2s}
.cursite a:hover{color:var(--brass2);border-color:var(--brass)}
.cursite .no{color:#d2705f}

.email{display:flex;align-items:center;gap:8px;background:var(--bg);border:1px solid var(--line);border-radius:11px;padding:5px 5px 5px 12px}
.email .v{flex:1;font:12.5px ui-monospace,monospace;color:#d8d2c6;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.cp{background:var(--surf);border:1px solid var(--line2);border-radius:8px;color:var(--mut);font:11.5px Archivo;padding:7px 11px;cursor:pointer;white-space:nowrap;transition:.18s;flex:none}
.cp:hover{border-color:var(--brass);color:var(--brass2)}

.actions{display:flex;gap:9px}
.btn{flex:1;display:inline-flex;align-items:center;justify-content:center;gap:7px;font:600 13px Archivo;padding:11px 12px;border-radius:11px;border:1px solid var(--line2);color:var(--ivory);cursor:pointer;background:var(--surf);transition:.18s;text-align:center;min-height:42px}
.btn:hover{border-color:var(--brass);color:var(--brass2)}
.btn.primary{background:linear-gradient(180deg,var(--brass2),var(--brass));color:#1a1305;border-color:var(--brass);box-shadow:0 6px 16px -6px rgba(203,167,90,.6)}
.btn.primary:hover{filter:brightness(1.06);color:#1a1305;transform:translateY(-1px)}
.btn svg{width:15px;height:15px}

details{border-top:1px solid var(--line);padding-top:11px}
summary{cursor:pointer;font-size:12.5px;color:var(--mut);list-style:none;display:flex;align-items:center;gap:6px;transition:.2s}
summary:hover{color:var(--brass2)}
summary::-webkit-details-marker{display:none}
summary .ar{transition:.2s;font-size:10px}
details[open] summary .ar{transform:rotate(90deg)}
textarea{width:100%;height:160px;margin-top:10px;background:var(--bg);border:1px solid var(--line);border-radius:11px;color:#e7e2d6;padding:12px;font:12px/1.55 ui-monospace,monospace;resize:vertical}

.foot{display:flex;align-items:center;gap:11px;margin-top:auto;padding-top:13px;border-top:1px solid var(--line)}
.sw{position:relative;width:46px;height:26px;flex:none}
.sw input{opacity:0;width:0;height:0;position:absolute}
.sw label{position:absolute;inset:0;background:#2a3550;border-radius:999px;cursor:pointer;transition:.22s;border:1px solid var(--line2)}
.sw label::after{content:"";position:absolute;top:3px;left:3px;width:18px;height:18px;background:#fff;border-radius:50%;transition:.22s;box-shadow:0 2px 5px rgba(0,0,0,.4)}
.sw input:checked + label{background:linear-gradient(180deg,#6fe0a8,var(--ok));border-color:transparent}
.sw input:checked + label::after{transform:translateX(20px)}
.sinfo{font-size:12px;color:var(--mut)}
.sinfo b{color:var(--ok)}
.sinfo .who{color:var(--ivory)}

.empty{text-align:center;padding:70px 20px;color:var(--mut)}
.empty .big{font-family:Fraunces,serif;font-size:22px;color:var(--ivory);margin-bottom:6px}

footer{text-align:center;color:var(--mut2);font-size:11.5px;padding:30px 0 40px}

/* ===== Responsive ===== */
@media(max-width:760px){
  .stats{grid-template-columns:repeat(2,1fr);gap:10px}
  .stat{padding:13px 14px;border-radius:14px}
  .tools{top:52px}
  .row1{flex-wrap:wrap}
  .seg{width:100%}.seg button{flex:1;text-align:center}
  .grid{grid-template-columns:1fr;gap:14px}
  .me input,.me select{width:120px}
}
@media(max-width:480px){
  .bar .in{flex-wrap:wrap;gap:10px}
  .me{width:100%;justify-content:space-between}
  .me input,.me select{flex:1}
}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
</style></head><body>

<header class="bar">
  <div class="wrap in">
    <div class="brand"><span class="logo"></span><div class="t"><b>Meridante</b><small>Outreach Console</small></div></div>
    <div class="grow"></div>
    <div class="me">
      <span class="sync"><span class="dot" id="dot"></span><span id="syncTxt">local</span></span>
      <button class="guidebtn" onclick="document.getElementById('guide').classList.add('open')" title="How to use the cockpit — the full playbook">◆ Playbook</button><a class="guidebtn" href="pipeline.html" title="Command Cockpit — full funnel + money" style="text-decoration:none;display:inline-flex;align-items:center;margin-left:8px">◆ Command Cockpit</a>
      <select id="me" title="Select your name — stamped when you mark a lead as Sent">
        <option value="">Who are you?</option>
        <option>Sajid</option><option>Lucas</option><option>João</option>
      </select>
    </div>
  </div>
  <div class="gprog"><i id="gprog"></i></div>
</header>

<div class="modal" id="guide" onclick="if(event.target===this)this.classList.remove('open')">
 <div class="sheet">
  <button class="x" onclick="document.getElementById('guide').classList.remove('open')">✕</button>
  <div class="ghead"><span class="logo"></span><div><b>Meridante — Team Playbook</b><small>How the whole machine works · read once, keep open</small></div></div>
  <div class="gbody">
   <div class="gcard">
    <h4>1 · Your daily 20 minutes</h4>
    <ol>
     <li>Pick your name (top right) so your sends are logged for the team.</li>
     <li>Toggle <b>Unsent only</b>, work top to bottom.</li>
     <li>On a card: read the draft, hit <b>✉ Open in Gmail</b> (opens a ready draft as meridante.pt@gmail.com with the mockup attached), glance it over, <b>Send</b>.</li>
     <li>Flip the <b>Sent</b> switch. Everyone sees it instantly — nobody double-touches a lead.</li>
    </ol>
   </div>
   <div class="gcard">
    <h4>2 · The follow-ups (Relances)</h4>
    <p>Most replies come from the <i>chase</i>, not the first email. Each card has a <b>Relances · J+3 · J+10 · J+17</b> panel — three ready messages.</p>
    <ol>
     <li>No reply after ~3 days → send <b>J+3</b>. Still nothing at day 10 → <b>J+10</b>. Day 17 → <b>J+17</b> (the graceful exit).</li>
     <li>Each has its own <b>✉ Gmail</b> + <b>Copy</b> button. Warm, never pushy. Stop the moment they reply.</li>
    </ol>
   </div>
   <div class="gcard hi">
    <h4>3 · When a lead REPLIES — this is where the money is</h4>
    <p>A positive reply is the trigger. Tell João (or run it yourself in Claude Code):</p>
    <ol>
     <li><b>Build their real preview</b> — <code>/meridante-preview &lt;company&gt;</code>. Deep-scans their business and builds a full Kiné-level multi-page site, deployed live, plus a design PDF + page images. (Reference: the live Kiné site.)</li>
     <li><b>Send the preview email</b> — the card flips to <b>REPLIED</b> with the delivery email ready; it offers a 15-min call.</li>
     <li><b>Close it</b> — <code>/meridante-close &lt;company&gt;</code>. Preps the call, builds the 3-tier proposal PDF, drafts the close email with the deposit + booking links.</li>
    </ol>
   </div>
   <div class="gcard">
    <h4>4 · The offer & pricing (what you're selling)</h4>
    <p>Always show <b>three</b> options. Open on BEST, land on BETTER (⭐ most people pick it).</p>
    <table class="ptab"><tr><th></th><th>Premium<br><span>LU·BE·NL·FR</span></th><th>Value<br><span>ES·PT</span></th><th>Care</th></tr>
     <tr><td>GOOD — Présence</td><td>€890</td><td>€490</td><td>+€39/mo</td></tr>
     <tr class="star"><td>BETTER — Croissance ⭐</td><td>€1 900</td><td>€990</td><td>+€99/mo</td></tr>
     <tr><td>BEST — Performance</td><td>€3 400</td><td>€1 790</td><td>+€199/mo</td></tr></table>
    <p class="fine">50% deposit to start. The domain always stays in the client's name. The monthly Care plan is the real asset — attach it every time.</p>
   </div>
   <div class="gcard">
    <h4>The rules that never change</h4>
    <ul>
     <li>Every email sends from <b>meridante.pt@gmail.com</b>. We only draft — you review and send.</li>
     <li>100% truthful. Never claim we "visited" their site. Only real, verified info.</li>
     <li>Only the hero image is ever public. Full live sites happen only after a lead says yes.</li>
    </ul>
   </div>
  </div>
  <div class="gfoot">Full funnel doc: <code>~/web-agency/funnel/PITCH-TO-SALE-FUNNEL.md</code> · Questions → João</div>
 </div>
</div>

<div class="wrap">
  <div class="stats">
    <div class="stat"><div class="lab">Total leads</div><div class="num" id="kTotal">0</div></div>
    <div class="stat s-sent acc"><div class="lab">Sent</div><div class="num" id="kSent">0</div></div>
    <div class="stat"><div class="lab">To send</div><div class="num" id="kLeft">0</div></div>
    <div class="stat s-pct"><div class="lab">Progress</div><div class="num" id="kPct">0%</div></div>
  </div>
</div>

<div class="tools">
  <div class="wrap">
    <div class="row1">
      <div class="search">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
        <input id="q" placeholder="Search company, city, sector, email…">
      </div>
      <div class="seg" id="cseg"><button data-c="" class="on">All</button><button data-c="Luxembourg">🇱🇺 LU</button><button data-c="Portugal">🇵🇹 PT</button><button data-c="Belgium">🇧🇪 BE</button><button data-c="Netherlands">🇳🇱 NL</button><button data-c="France">🇫🇷 FR</button><button data-c="Spain">🇪🇸 ES</button></div>
    </div>
    <div class="row2">
      <div class="chips" id="status" style="display:contents"></div>
      <label class="toggle"><input type="checkbox" id="unsent"> Unsent only</label>
    </div>
  </div>
</div>

<div class="wrap"><p class="note" id="modeNote"></p></div>
<main class="wrap" id="main"></main>
<footer>Meridante · internal outreach console — confidential. Mark leads sent so the team never doubles up.</footer>

<script>
(function(){var P="meridante2026";if(sessionStorage.getItem('mok')==='1')return;var e=prompt('Meridante — team passphrase:');if(e!==P){document.documentElement.innerHTML='<body style="font-family:sans-serif;background:#080d1a;color:#9aa6bd;padding:50px">Access restricted — Meridante team only.</body>';throw 'locked';}sessionStorage.setItem('mok','1');})();
const CONFIG={ENDPOINT:"https://script.google.com/macros/s/AKfycbwPxJUxo3ybuYaAmyhRYfQHtRjur2-b9-shyCQTsx_wGhMoyWaTGpaBVwu56QSzJoQz/exec",DRAFT_ENDPOINT:"https://script.google.com/macros/s/AKfycbyBos7cRe9x4MPzxhpb-iRZZKnM0b0wZQ-LoiA1onf0I55kafZd-I4ReRpG_T61XCiU/exec"}; // ENDPOINT = team-sync sheet · DRAFT_ENDPOINT = Gmail draft maker
const ASSET="https://raw.githubusercontent.com/meridante-dev/meridante-assets/master";
const CLIENTS=__DATA__;
const SC={'BROKEN':'#e05a45','NO-SITE':'#5b6b85','NOT-MOBILE':'#e08a3c','OUTDATED':'#d4a83a','DATED-BUILDER':'#c79a36','TEMPLATE-BASIC':'#b07ad0','OUTDATED / DATED-BUILDER':'#c79a36','NOT-MOBILE / OUTDATED':'#e08a3c'};
let STATE={}, filterC="", filterS="", q="", unsentOnly=false;
const FROM="meridante.pt@gmail.com";
const byId={}; CLIENTS.forEach(c=>byId[c.id]=c);
const shotUrl=id=>ASSET+'/shots/'+id+'.jpg';
const draftsUrl='https://mail.google.com/mail/?authuser='+encodeURIComponent(FROM)+'#drafts';
function previewText(c){const L=(c.lang||'').toLowerCase();
  const T={fr:['Aperçu de votre nouvelle maquette de site','Voici un aperçu de la maquette que nous avons préparée pour vous :'],
           es:['Vista previa de la maqueta de su nuevo sitio web','Aquí tiene una vista previa de la propuesta que hemos preparado para usted:'],
           pt:['Pré-visualização da maqueta do seu site','Aqui está uma pré-visualização da proposta que preparámos para si:'],
           nl:['Voorbeeld van uw nieuwe website-ontwerp','Hier is een voorbeeld van het voorstel dat we voor u hebben gemaakt:']};
  const t=T[L]||T.pt;
  return '\n\n'+t[0]+'\n'+t[1]+'\n'+shotUrl(c.id);}
function composeUrl(c){return 'https://mail.google.com/mail/?view=cm&fs=1&to='+encodeURIComponent(c.email)+'&su='+encodeURIComponent(c.subject)+'&body='+encodeURIComponent(c.body+previewText(c))+'&authuser='+encodeURIComponent(FROM);}
function gmail(id){const c=byId[id]; if(!c)return;
  if(CONFIG.DRAFT_ENDPOINT){ const w=window.open('about:blank');
    fetch(CONFIG.DRAFT_ENDPOINT,{method:'POST',headers:{'Content-Type':'text/plain;charset=utf-8'},body:JSON.stringify({to:c.email,subject:c.subject,body:c.body,lang:c.lang,company:c.company,image:shotUrl(c.id)})})
      .then(r=>r.json()).then(()=>{try{w.location.href=draftsUrl;}catch(e){}})
      .catch(()=>{try{w.location.href=draftsUrl;}catch(e){}});
  } else { window.open(composeUrl(c),'_blank'); } }
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
function copy(t,btn){ navigator.clipboard.writeText(t).then(()=>{const o=btn.innerHTML;btn.innerHTML='Copied ✓';btn.style.color='var(--ok)';setTimeout(()=>{btn.innerHTML=o;btn.style.color='';},1100);}); }
const MAIL='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>';
const DL='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3v12m0 0 4-4m-4 4-4-4"/><path d="M5 21h14"/></svg>';
function card(c){ const st=STATE[c.id]||{}; const sent=st.sent;
  const init=esc((c.company.trim()[0]||'M').toUpperCase());
  const hasSite=c.website&&!/^none/i.test(c.website);
  const cur=hasSite?`<span class=cursite>Current site · <a href="${/^http/.test(c.website)?esc(c.website):'https://'+esc(c.website)}" target=_blank rel=noopener>${esc(c.website.replace(/^https?:\/\//,'').replace(/\/$/,''))} ↗</a></span>`:`<span class=cursite><span class=no>● No website yet</span></span>`;
  const draft="Subject: "+c.subject+"\n\n"+c.body;
  const thumbInner=`<span class=ph>${init}</span><img loading=lazy src="${ASSET}/thumbs/${c.id}.jpg" alt="" onerror="this.style.display='none'"><span class=badge style="--c:${SC[c.status]||'#7a869c'}"><i></i>${esc(c.status)}</span>${sent?'<span class=flag>✓ Sent</span>':''}${c.demo?'<span class=live>View live ↗</span>':''}`;
  const thumb=c.demo?`<a class=thumb href="${esc(c.demo)}" target=_blank rel=noopener>${thumbInner}</a>`:`<div class=thumb>${thumbInner}</div>`;
  return `<article class="card${sent?' sent':''}">
   ${thumb}
   <div class=body>
     <div><h3>${esc(c.company)}</h3><div class=meta>${esc(c.sector)} · ${esc(c.city)} <span class=b>· ${esc(c.batch)}</span></div></div>
     ${cur}
     <div class=email><span class=v>${esc(c.email)}</span><button class=cp onclick='copy(${JSON.stringify(c.email)},this)'>Copy</button></div>
     <div class=actions>
       <button class="btn primary" onclick="gmail('${c.id}')" title="Creates a Gmail draft (meridante.pt@gmail.com) — email + mockup shown inline and attached, ready to review &amp; send">${MAIL} Open in Gmail</button>
     </div>
     <div class=actions>
       <button class=btn onclick='copy(${JSON.stringify(draft)},this)'>Copy draft</button>
       <a class=btn href="${ASSET}/shots/${c.id}.jpg" download="${c.id}-meridante-mockup.jpg" target=_blank rel=noopener title="Open / download the website mockup image">${DL} Save PNG</a>
     </div>
     <details><summary><span class=ar>▸</span> View / edit draft</summary><textarea readonly>${esc(draft)}</textarea></details>
     ${(c.fu&&c.fu.length)?`<details><summary><span class=ar>▸</span> Relances · J+3 · J+10 · J+17</summary><div class=fus>${c.fu.map((f,i)=>`<div class=furow><span class=fud>J+${[3,10,17][i]}</span><a class="btn fub" href="${f.gmail+'&authuser='+encodeURIComponent(FROM)}" target=_blank>✉ Gmail</a><button class="cp" onclick='copy(${JSON.stringify("Subject: "+f.subject+"\n\n"+f.body)},this)'>Copy</button></div>`).join('')}</div></details>`:''}
     <div class=foot>
       <span class=sw><input type=checkbox id="s_${c.id}" ${sent?'checked':''} onchange="toggle('${c.id}',this.checked)"><label for="s_${c.id}"></label></span>
       <span class=sinfo>${sent?`<b>✓ Sent</b> · <span class=who>${esc(st.by||'?')}</span> · ${esc((st.date||'').slice(0,10))}`:'Mark as sent'}</span>
     </div>
   </div>
  </article>`; }
function render(){
  const list=CLIENTS.filter(c=>{
    if(filterC&&c.country!==filterC)return false;
    if(filterS&&c.status!==filterS)return false;
    if(unsentOnly&&(STATE[c.id]||{}).sent)return false;
    if(q){const h=(c.company+' '+c.city+' '+c.sector+' '+c.email).toLowerCase();if(!h.includes(q))return false;}
    return true;});
  const total=CLIENTS.length, sentN=CLIENTS.filter(c=>(STATE[c.id]||{}).sent).length;
  const pct=total?Math.round(sentN/total*100):0;
  document.getElementById('kTotal').textContent=total;
  document.getElementById('kSent').textContent=sentN;
  document.getElementById('kLeft').textContent=total-sentN;
  document.getElementById('kPct').textContent=pct+'%';
  document.getElementById('gprog').style.width=pct+'%';
  const m=document.getElementById('main'); m.innerHTML='';
  const FLAG={Luxembourg:'🇱🇺',Portugal:'🇵🇹',Belgium:'🇧🇪',Netherlands:'🇳🇱',France:'🇫🇷',Spain:'🇪🇸'};
  const ORDER=['Luxembourg','Belgium','Netherlands','France','Portugal','Spain'];
  const present=[...new Set(CLIENTS.map(c=>c.country))];
  const countries=present.sort((a,b)=>{const ia=ORDER.indexOf(a),ib=ORDER.indexOf(b);return (ia<0?99:ia)-(ib<0?99:ib)||a.localeCompare(b);})
    .map(c=>[c,(FLAG[c]?FLAG[c]+' ':'')+c]);
  let any=false;
  countries.forEach(([code,label])=>{
    const rows=list.filter(c=>c.country===code); if(!rows.length)return; any=true;
    const s=rows.filter(c=>(STATE[c.id]||{}).sent).length;
    const p=rows.length?Math.round(s/rows.length*100):0;
    m.innerHTML+=`<div class=country><h2>${label}</h2><div class=cbar><i style="width:${p}%"></i></div><span class=cn><b>${s}</b>/${rows.length} sent</span></div><div class=grid>${rows.map(card).join('')}</div>`;
  });
  if(!any)m.innerHTML='<div class=empty><div class=big>No leads match these filters</div><div>Try clearing the search or status chips.</div></div>';
}
function buildStatusChips(){ const sts=[...new Set(CLIENTS.map(c=>c.status))].sort();
  const el=document.getElementById('status');
  el.innerHTML=`<span class="chip on" data-s="">All status</span>`+sts.map(s=>`<span class=chip data-s="${esc(s)}">${esc(s)}</span>`).join('');
  el.querySelectorAll('.chip').forEach(ch=>ch.onclick=()=>{filterS=ch.dataset.s;el.querySelectorAll('.chip').forEach(x=>x.classList.toggle('on',x===ch));render();}); }
document.getElementById('cseg').querySelectorAll('button').forEach(b=>b.onclick=()=>{filterC=b.dataset.c;document.querySelectorAll('#cseg button').forEach(x=>x.classList.toggle('on',x===b));render();});
document.getElementById('q').oninput=e=>{q=e.target.value.toLowerCase();render();};
document.getElementById('unsent').onchange=e=>{unsentOnly=e.target.checked;render();};
document.getElementById('me').onchange=e=>{localStorage.setItem('meridante_me',e.target.value);render();};
document.getElementById('modeNote').textContent=CONFIG.ENDPOINT?'Team-synced via shared Google Sheet — everyone sees the same status live.':'Local mode — sent-status saves on this device only. Connect the team sheet to sync across everyone (ask João).';
buildStatusChips();
loadState().then(()=>{render(); if(CONFIG.ENDPOINT)setInterval(()=>loadState().then(render),20000);});
</script></body></html>'''
open('index.html','w').write(HTML.replace('__DATA__',DATA))
print('dashboard index.html written;', len(data),'clients embedded;', len(open("index.html").read())//1024,'KB')
