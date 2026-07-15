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
import os, json, ssl, smtplib, datetime, urllib.request, html as H
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

HERE = os.path.dirname(os.path.abspath(__file__))
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

def build(leads):
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

    # ---------- branded HTML (SMTP path) ----------
    rows = ""
    for l in leads:
        gm = l.get("gmail", "")
        hint = STATUS_HINT.get(l.get("status",""), l.get("status",""))
        rows += f"""
        <tr>
          <td style="padding:14px 16px;border-bottom:1px solid #eee6d8;">
            <div style="font-family:Georgia,serif;font-size:16px;color:#0a1020;">{H.escape(l['company'])}</div>
            <div style="font-size:12px;color:#6c7790;">{H.escape(l.get('sector',''))} · {H.escape(l.get('city',''))}, {H.escape(l.get('country',''))}</div>
          </td>
          <td style="padding:14px 16px;border-bottom:1px solid #eee6d8;font-size:11px;letter-spacing:.08em;color:#8a5a2a;white-space:nowrap;">{H.escape(hint)}</td>
          <td style="padding:14px 16px;border-bottom:1px solid #eee6d8;font-size:12px;color:#0a1020;">{H.escape(l.get('email',''))}<br>
            {f'<a href="{H.escape(gm)}" style="color:#8a5a2a;font-size:11px;">open Gmail draft →</a>' if gm else ''}</td>
        </tr>"""
    empty = """<tr><td style="padding:26px 16px;color:#6c7790;font-size:13px;">No new qualified leads today —
      the pipeline ran; dedupe and quality gates filtered everything out. Normal on quiet slices.</td></tr>"""
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
    <table style="width:100%;border-collapse:collapse;margin-top:18px;">{rows or empty}</table>
    <a href="{CONSOLE}" style="display:inline-block;margin-top:22px;background:#0a1020;color:#f4efe6;
       font-size:11px;letter-spacing:.22em;padding:12px 22px;text-decoration:none;">OPEN OUTREACH CONSOLE →</a>
    <div style="font-size:10px;color:#9aa6bd;margin-top:22px;line-height:1.6;">Every lead has a verified public email and a
      truthful first-touch draft, generated by the free cloud pipeline (GitHub Actions · OpenStreetMap · Groq).</div>
  </div>
 </div>
</div>"""
    return subject, md_text, html_body

def send_smtp(subject, html_body, md_text):
    user = os.environ.get("GMAIL_USER"); pw = os.environ.get("GMAIL_APP_PASSWORD")
    if not (user and pw):
        return False
    to = os.environ.get("DIGEST_TO", "meridante.pt@gmail.com")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject; msg["From"] = f"Meridante Autopilot <{user}>"; msg["To"] = to
    msg.attach(MIMEText(md_text, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as s:
        s.login(user, pw)
        s.sendmail(user, [to], msg.as_string())
    print(f"digest sent via Gmail SMTP → {to}")
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
    subject, md_text, html_body = build(leads)
    if send_smtp(subject, html_body, md_text):
        return
    if send_issue(subject, md_text):
        return
    print(subject); print(); print(md_text)

if __name__ == "__main__":
    main()
