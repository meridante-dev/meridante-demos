#!/usr/bin/env python3
"""
Autopilot DAILY DIGEST — one email per weekday with everything the funnel produced.

Delivery (first available wins):
  1. Gmail SMTP  — if GMAIL_USER + GMAIL_APP_PASSWORD env/secrets are set:
     sends a branded HTML email to DIGEST_TO (default meridante.pt@gmail.com).
  2. GitHub inbox — if DIGEST_TOKEN (+ DIGEST_REPO) are set: files the digest as
     an issue in the private inbox repo; GitHub notifications email it to the
     account's registered address. Zero credentials beyond a repo token.
  3. stdout — prints the digest (local runs / debugging).

Run daily after the last batch:  python3 digest.py
"""
import os, sys, json, ssl, smtplib, datetime, urllib.request, html as H
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)   # so `import mockup, render` works from any cwd
ROOT = os.path.dirname(HERE)
TODAY = str(datetime.date.today())
CONSOLE = "https://meridante-dev.github.io/meridante-demos/"

def todays_leads():
    ids_path = os.path.join(HERE, "logs", f"{TODAY}-ids.txt")
    ids = []
    if os.path.exists(ids_path):
        ids = [x.strip() for x in open(ids_path) if x.strip()]
    if not ids:
        return []
    data = json.load(open(os.path.join(ROOT, "_clients.json")))
    by_id = {x.get("id"): x for x in data}
    return [by_id[i] for i in ids if i in by_id]

def day_log():
    p = os.path.join(HERE, "logs", f"{TODAY}.md")
    return open(p).read().strip() if os.path.exists(p) else ""

def totals():
    data = json.load(open(os.path.join(ROOT, "_clients.json")))
    ap = [x for x in data if x.get("batch") == "Autopilot"]
    return len(data), len(ap)

STATUS_HINT = {
    "NO-SITE": "no website at all", "BROKEN": "website is down/broken",
    "OUTDATED": "visibly outdated site", "NOT-MOBILE": "not mobile-friendly",
    "DATED-BUILDER": "old site-builder", "TEMPLATE-BASIC": "bare template site",
}

def gen_mockups(leads, cap=12):
    """Generate a world-class website-mockup hero image per lead → {id: jpg_path}.
    Runs the mockup generator + headless-Chrome render (works on GitHub runners,
    which ship Chrome). Kept private: images are only ever attached to the digest,
    never committed/published. Capped to bound render time."""
    import mockup, render
    out = {}
    picks = [l for l in leads if l.get("id")][:cap]
    if not picks:
        return out
    folders = []
    for idx, l in enumerate(picks):
        d = os.path.join(HERE, "_mockups", l["id"])
        try:
            mockup.build_html(l, d, idx=idx); folders.append((l, d))
        except Exception as e:
            print("mockup build skipped", l.get("id"), e)
    if not folders:
        return out
    try:
        render.render([os.path.abspath(d) for _, d in folders])
    except Exception as e:
        print("render failed:", e); return out
    for l, d in folders:
        hero = os.path.join(d, "hero.png")
        if not os.path.exists(hero):
            continue
        try:
            from PIL import Image
            im = Image.open(hero).convert("RGB"); im.thumbnail((900, 900))
            jpg = os.path.join(d, "hero-email.jpg")
            im.save(jpg, "JPEG", quality=72, optimize=True)
            out[l["id"]] = jpg
        except Exception:
            out[l["id"]] = hero   # PIL missing → attach full PNG
    print(f"mockups generated: {len(out)}/{len(picks)}")
    return out

def build(leads, mockups=None):
    mockups = mockups or {}
    n = len(leads)
    total, ap_total = totals()
    subject = f"Meridante Autopilot — {TODAY}: {n} new verified lead{'s' if n != 1 else ''}"

    # ---------- markdown (issue / fallback) ----------
    md = [f"## {n} new verified lead{'s' if n != 1 else ''} — {TODAY}", ""]
    if leads:
        md += ["| Company | Sector | City | Weakness | Email |", "|---|---|---|---|---|"]
        for l in leads:
            md.append(f"| **{l['company']}** | {l.get('sector','')} | {l.get('city','')}, {l.get('country','')} "
                      f"| `{l.get('status','')}` | {l.get('email','')} |")
        md += ["", "**Draft emails are ready** — open the console, review, send:"]
        md.append(f"➡️ [Outreach console]({CONSOLE}) (batch *Autopilot*)")
    else:
        md.append("_No new qualified leads today — the pipeline ran, dedupe + quality gates filtered everything out. Normal on quiet slices._")
    md += ["", f"Pipeline: **{ap_total}** autopilot leads · **{total}** total in the cockpit.", "", "<details><summary>Run log</summary>", "", day_log(), "", "</details>"]
    md_text = "\n".join(md)

    # ---------- branded HTML (SMTP path) — one card per lead, mockup embedded inline ----------
    rows = ""
    for l in leads:
        gm = l.get("gmail", "")
        hint = STATUS_HINT.get(l.get("status",""), l.get("status",""))
        mid = l.get("id")
        img = (f'<img src="cid:mock-{mid}" alt="Concept homepage for {H.escape(l.get("company",""))}" '
               f'style="width:100%;border-radius:10px;border:1px solid #e8dfcf;margin-top:14px;display:block;">'
               if mid in mockups else '')
        draft = (f' &nbsp;·&nbsp; <a href="{H.escape(gm)}" style="color:#8a5a2a;">open Gmail draft →</a>' if gm else '')
        rows += f"""
        <div style="padding:20px 0;border-bottom:1px solid #eee6d8;">
          <div style="font-family:Georgia,serif;font-size:18px;color:#0a1020;">{H.escape(l['company'])}</div>
          <div style="font-size:12px;color:#6c7790;margin-top:3px;">{H.escape(l.get('sector',''))} · {H.escape(l.get('city',''))}, {H.escape(l.get('country',''))} &nbsp;·&nbsp; <span style="color:#8a5a2a;letter-spacing:.06em;">{H.escape(hint)}</span></div>
          <div style="font-size:12px;color:#0a1020;margin-top:7px;">{H.escape(l.get('email',''))}{draft}</div>
          {img}
        </div>"""
    empty = """<div style="padding:26px 0;color:#6c7790;font-size:13px;">No new qualified leads today —
      the pipeline ran; dedupe and quality gates filtered everything out. Normal on quiet slices.</div>"""
    html_body = f"""
<div style="background:#f4efe6;padding:28px 12px;font-family:'Helvetica Neue',Arial,sans-serif;">
 <div style="max-width:640px;margin:0 auto;background:#fffdf9;border:1px solid #e8dfcf;">
  <div style="background:#0a1020;padding:22px 26px;">
    <div style="font-family:Georgia,serif;color:#f4efe6;font-size:19px;letter-spacing:.14em;">MERIDANTE</div>
    <div style="color:#cba75a;font-size:10px;letter-spacing:.32em;margin-top:4px;">LEADS ON AUTOPILOT · DAILY DIGEST</div>
  </div>
  <div style="padding:26px;">
    <div style="font-family:Georgia,serif;font-size:22px;color:#0a1020;">{n} new verified lead{'s' if n != 1 else ''}</div>
    <div style="font-size:12px;color:#6c7790;margin-top:4px;">{TODAY} · pipeline total: {ap_total} autopilot / {total} overall</div>
    <div style="margin-top:18px;">{rows or empty}</div>
    <a href="{CONSOLE}" style="display:inline-block;margin-top:22px;background:#0a1020;color:#f4efe6;
       font-size:11px;letter-spacing:.22em;padding:12px 22px;text-decoration:none;">OPEN OUTREACH CONSOLE →</a>
    <div style="font-size:10px;color:#9aa6bd;margin-top:22px;line-height:1.6;">Each card shows a concept homepage mockup — a free preview of the site we could build them.
      Verified email + truthful first-touch draft included, all from the free cloud pipeline (GitHub Actions · OpenStreetMap · Groq).</div>
  </div>
 </div>
</div>"""
    return subject, md_text, html_body

def send_smtp(subject, html_body, md_text, mockups=None, leads=None):
    user = os.environ.get("GMAIL_USER"); pw = os.environ.get("GMAIL_APP_PASSWORD")
    if not (user and pw):
        return False
    mockups = mockups or {}
    by_id = {l.get("id"): l for l in (leads or [])}
    to = os.environ.get("DIGEST_TO", "meridante.pt@gmail.com")
    # 'related' wraps the HTML + inline images so they render in-body (cid:) and download.
    root = MIMEMultipart("related")
    root["Subject"] = subject; root["From"] = f"Meridante Autopilot <{user}>"; root["To"] = to
    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(md_text, "plain", "utf-8"))
    alt.attach(MIMEText(html_body, "html", "utf-8"))
    root.attach(alt)
    for lid, path in mockups.items():
        try:
            data = open(path, "rb").read()
            subtype = "png" if path.lower().endswith(".png") else "jpeg"
            img = MIMEImage(data, _subtype=subtype)
            img.add_header("Content-ID", f"<mock-{lid}>")
            comp = (by_id.get(lid, {}).get("company") or lid)
            safe = "".join(c for c in comp if c.isalnum() or c in " -_").strip()[:40] or lid
            img.add_header("Content-Disposition", "inline", filename=f"{safe} — concept.{ 'png' if subtype=='png' else 'jpg' }")
            root.attach(img)
        except Exception as e:
            print("attach skipped", lid, e)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as s:
        s.login(user, pw)
        s.sendmail(user, [to], root.as_string())
    print(f"digest sent via Gmail SMTP → {to}  ({len(mockups)} mockups attached)")
    return True

def send_issue(subject, md_text):
    tok = os.environ.get("DIGEST_TOKEN"); repo = os.environ.get("DIGEST_REPO")
    if not (tok and repo):
        return False
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/issues",
        data=json.dumps({"title": subject, "body": md_text, "labels": ["digest"]}).encode(),
        headers={"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json",
                 "User-Agent": "meridante-autopilot"})
    r = json.load(urllib.request.urlopen(req, timeout=20))
    print(f"digest filed as issue → {r.get('html_url')} (GitHub emails the notification)")
    return True

def main():
    leads = todays_leads()
    preview = "--preview" in sys.argv          # local: render mockups + write HTML to a file, no send
    smtp_ready = bool(os.environ.get("GMAIL_USER") and os.environ.get("GMAIL_APP_PASSWORD"))
    # only spend render time when we can actually deliver the images privately (SMTP) or previewing
    mockups = gen_mockups(leads) if (leads and (smtp_ready or preview)) else {}
    subject, md_text, html_body = build(leads, mockups)
    if preview:
        out = os.path.join(HERE, "_digest_preview.html")
        # inline the images as data URIs so the preview file is self-contained
        import base64
        for lid, path in mockups.items():
            b64 = base64.b64encode(open(path, "rb").read()).decode()
            html_body = html_body.replace(f"cid:mock-{lid}", f"data:image/jpeg;base64,{b64}")
        open(out, "w").write(html_body)
        print(f"preview written → {out}  ({len(mockups)} mockups)")
        return
    if send_smtp(subject, html_body, md_text, mockups, leads):
        return
    if send_issue(subject, md_text):
        return
    print(subject); print(); print(md_text)

if __name__ == "__main__":
    main()
