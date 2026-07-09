# -*- coding: utf-8 -*-
"""
Meridante — Leads on Autopilot (free, decentralized).
Implements the 6 GTM shifts with zero paid tools, on a GitHub Actions cron:

  1. Company sourcing   -> OpenStreetMap Overpass (free "Google Maps" for local businesses)
  2. Contact finding    -> fetch site + HTML->text, extract a VERIFIED PUBLIC email + owner name
  3. Agentic cron       -> GitHub Actions schedule (runs in the cloud, off your machine)
  4. Goal mode          -> loop until N new *qualified* (weak/no-site + real email) leads found
  5. Auto research       -> Groq (free LLM) writes a truthful hook + first-touch email + a run digest
  6. Open-source tech    -> requests + BeautifulSoup (HTML->text) + tech-signature detection; no BuiltWith/ZenRows

New leads are appended to ../_clients.json (the cockpit) and the dashboard is rebuilt.
Strict rule kept from the outreach standard: ONLY verified public emails (never guessed).
"""
import os, re, json, time, subprocess, datetime, urllib.parse, sys
import requests
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                      # the cockpit repo root (holds _clients.json)
CFG  = json.load(open(os.path.join(HERE, "config.json")))
SEEN_PATH = os.path.join(HERE, "_seen.json")
CLIENTS   = os.path.join(ROOT, "_clients.json")
FROM = "meridante.pt@gmail.com"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
GROQ_KEY = os.environ.get("GROQ_API_KEY", "").strip()

BAD_EMAIL = re.compile(r"(noreply|no-reply|wixpress|sentry|example\.|@sentry|@wix|@2x|\.png|\.jpg|\.gif|@example|your@|email@|@domain)", re.I)
EMAIL_RE  = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
YEAR_RE   = re.compile(r"(?:©|&copy;|copyright)\s*\D{0,6}(20\d{2})", re.I)

def norm_name(s): return re.sub(r"[^a-z0-9]", "", (s or "").lower())
def domain_of(url):
    try: return urllib.parse.urlparse(url if "://" in url else "http://"+url).netloc.replace("www.", "").lower()
    except Exception: return ""

# ---------- history ----------
def load_seen():
    seen = {"emails": set(), "domains": set(), "names": set()}
    if os.path.exists(SEEN_PATH):
        j = json.load(open(SEEN_PATH))
        for k in seen: seen[k] = set(j.get(k, []))
    # also seed from the live cockpit so we never re-add an existing lead
    try:
        for c in json.load(open(CLIENTS)):
            if c.get("email"): seen["emails"].add(c["email"].lower())
            if c.get("website"): seen["domains"].add(domain_of(c["website"]))
            if c.get("company"): seen["names"].add(norm_name(c["company"]))
    except Exception: pass
    return seen

def save_seen(seen):
    json.dump({k: sorted(v) for k, v in seen.items()}, open(SEEN_PATH, "w"), ensure_ascii=False, indent=0)

# ---------- 1. company sourcing (Overpass) ----------
def overpass(area, niche):
    q = f"""[out:json][timeout:60];
(
  nwr{niche['filter']}(around:9000,{area['lat']},{area['lon']});
);
out center tags 160;"""
    for ep in CFG["overpass_endpoints"]:
        try:
            r = requests.post(ep, data={"data": q}, headers={"User-Agent": UA}, timeout=90)
            if r.status_code == 200:
                return r.json().get("elements", [])
        except Exception as e:
            print("overpass err", ep, e)
    return []

# ---------- 6. open-source tech: fetch + HTML->text + weakness ----------
def fetch(url):
    if not url: return None, ""
    if "://" not in url: url = "http://" + url
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=14, allow_redirects=True)
        return r, r.text or ""
    except Exception:
        return None, ""

def html_to_text(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        for t in soup(["script", "style", "noscript"]): t.extract()
        return re.sub(r"\s+", " ", soup.get_text(" ")).strip()
    except Exception:
        return re.sub(r"<[^>]+>", " ", html)

def classify_site(resp, html):
    """Return a weakness status matching the cockpit vocabulary, or 'MODERN' (skip)."""
    if resp is None: return "BROKEN"
    if resp.status_code >= 400: return "BROKEN"
    low = html.lower()
    text = html_to_text(html)
    if len(text) < 350 or any(s in low for s in ("under construction", "coming soon", "domain for sale", "site en construction", "em construção")):
        return "BROKEN"
    if any(s in low for s in ("wixsite.com", "_wixcssstate", "squarespace.com/config", "godaddysites", "business.site", ".jimdofree", "webnode")):
        return "DATED-BUILDER"
    if 'name="viewport"' not in low and "name='viewport'" not in low:
        return "NOT-MOBILE"
    yrs = [int(y) for y in YEAR_RE.findall(html)]
    if yrs and max(yrs) <= datetime.date.today().year - 3:
        return "OUTDATED"
    if len(text) < 1200:            # thin, template-ish single page
        return "TEMPLATE-BASIC"
    return "MODERN"

# ---------- 2. contact finding: verified public email + owner ----------
def find_email(osm_tags, homepage_html, dom):
    cand = []
    for k in ("email", "contact:email"):
        if osm_tags.get(k): cand += [e.strip() for e in re.split(r"[;, ]", osm_tags[k]) if "@" in e]
    if homepage_html:
        for m in re.findall(r'mailto:([^"\'?>]+)', homepage_html): cand.append(urllib.parse.unquote(m))
        cand += EMAIL_RE.findall(html_to_text(homepage_html))
    seen, out = set(), []
    for e in cand:
        e = e.strip().strip(".").lower()
        if not EMAIL_RE.fullmatch(e) or BAD_EMAIL.search(e) or e in seen: continue
        seen.add(e); out.append(e)
    if not out: return ""
    # prefer an address on the business's own domain, else the first clean public one
    for e in out:
        if dom and dom.split(".")[0] in e.split("@")[-1]: return e
    return out[0]

# ---------- 5. auto research: Groq writes hook + email (truthful) ----------
def groq_json(system, user, model):
    if not GROQ_KEY: return None
    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": "Bearer " + GROQ_KEY, "Content-Type": "application/json"},
            json={"model": model, "temperature": 0.5, "response_format": {"type": "json_object"},
                  "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]},
            timeout=45)
        if r.status_code == 200:
            return json.loads(r.json()["choices"][0]["message"]["content"])
        print("groq", r.status_code, r.text[:120])
    except Exception as e:
        print("groq err", e)
    return None

VOICE = {
 "PT": ("Escreve em português de Portugal.", "Com os melhores cumprimentos", "Olá"),
 "FR": ("Écris en français.", "Bien cordialement", "Bonjour"),
 "NL": ("Schrijf in het Nederlands.", "Met vriendelijke groet", "Hallo"),
 "ES": ("Escribe en español.", "Un cordial saludo", "Hola"),
}
GENERIC_HOOK = {"PT":"o vosso site atual não faz justiça ao vosso trabalho","FR":"votre site actuel ne rend pas justice à votre travail","NL":"jullie huidige site doet jullie werk geen recht aan","ES":"vuestra web actual no hace justicia a vuestro trabajo"}

def write_email(company, city, sector, lang, status, site_text):
    lang = lang if lang in VOICE else "FR"
    lg, signoff, hello = VOICE[lang]
    weak = {"NO-SITE":"não têm site / n'ont pas de site / geen website / sin web",
            "BROKEN":"site em baixo","OUTDATED":"site desatualizado","NOT-MOBILE":"site não adaptado ao telemóvel",
            "DATED-BUILDER":"site num construtor básico","TEMPLATE-BASIC":"site muito genérico"}.get(status,"site a melhorar")
    sys_p = ("You are João, founder of the Meridante web studio. Write warm, human, 100% TRUTHFUL B2B outreach. "
             + lg + " STRICT RULES: never claim you 'visited', 'opened' or 'looked at their phone'; do not invent facts; "
             "no em-dashes (—); ~110-140 words; one specific, grounded observation; soft single CTA (a free mockup, a simple yes). "
             'Return JSON: {"owner":"first name if clearly in the text else empty","hook":"one truthful sentence","subject":"short subject","body":"the email, plain text, signed \\"João · Meridante\\""}.')
    usr = f"Company: {company}\nCity: {city}\nSector: {sector}\nTheir website status: {status} ({weak}).\nWebsite text (may be empty): {site_text[:1400]}"
    j = groq_json(sys_p, usr, CFG["groq_model"])
    if j and j.get("subject") and j.get("body"):
        return j.get("owner","").strip(), j["subject"].strip(), j["body"].strip()
    # template fallback (still truthful, no fabricated specifics)
    hook = GENERIC_HOOK.get(lang, GENERIC_HOOK["FR"])
    subj = {"PT":f"Uma ideia para {company}","FR":f"Une idée pour {company}","NL":f"Een idee voor {company}","ES":f"Una idea para {company}"}[lang]
    intro = {"PT":"Chamo-me João, do estúdio Meridante. Desenhamos sites e ferramentas online para negócios locais.",
             "FR":"Je m'appelle João, du studio Meridante. Nous concevons des sites et des outils en ligne pour les entreprises locales.",
             "NL":"Ik ben João, van studio Meridante. Wij maken websites en online tools voor lokale bedrijven.",
             "ES":"Me llamo João, del estudio Meridante. Diseñamos webs y herramientas online para negocios locales."}[lang]
    offer = {"PT":"Se quiser, preparo-lhe uma pequena maquete do que poderia ser, sem qualquer compromisso.",
             "FR":"Si vous le souhaitez, je vous prépare une petite maquette de ce que cela pourrait donner, sans engagement.",
             "NL":"Als u wilt, maak ik een kleine mockup van hoe het eruit zou kunnen zien, vrijblijvend.",
             "ES":"Si le apetece, le preparo una pequeña maqueta de cómo podría quedar, sin compromiso."}[lang]
    body = f"{hello},\n\n{intro}\n\n{hook.capitalize()}. {offer}\n\n{signoff},\nJoão · Meridante\n{FROM}"
    return "", subj, body

def gmail_link(to, su, body):
    return "https://mail.google.com/mail/?" + urllib.parse.urlencode({"view":"cm","fs":"1","to":to,"su":su,"body":body,"authuser":FROM})

# ---------- main (goal mode: loop until N new leads) ----------
def main():
    doy = datetime.date.today().timetuple().tm_yday
    areas, niches = CFG["areas"], CFG["niches"]
    area = areas[doy % len(areas)]
    niche = niches[(doy // len(areas)) % len(niches)]
    sector = niche["sector"].get(area["lang"], niche["key"])
    print(f"AUTOPILOT {datetime.date.today()} :: {area['city']} ({area['country']}) / {niche['key']}")

    seen = load_seen()
    elements = overpass(area, niche)
    print("overpass candidates:", len(elements))
    new_leads, fetches = [], 0
    for el in elements:
        if len(new_leads) >= CFG["target_new_per_run"] or fetches >= CFG["fetch_cap"]:
            break
        tags = el.get("tags", {})
        name = (tags.get("name") or "").strip()
        if not name or norm_name(name) in seen["names"]:
            continue
        website = tags.get("website") or tags.get("contact:website") or ""
        dom = domain_of(website)
        if dom and dom in seen["domains"]:
            continue
        # fetch the site (or none)
        html, status, site_text = "", "NO-SITE", ""
        if website:
            fetches += 1
            resp, html = fetch(website)
            status = classify_site(resp, html)
            if status == "MODERN":     # already has a good site -> not our prospect
                continue
            site_text = html_to_text(html)
        # verified public email (from site or OSM) — strict, never invented
        email = find_email(tags, html, dom)
        if not email or email in seen["emails"]:
            continue
        # write the outreach (Groq, truthful; template fallback)
        owner, subj, body = write_email(name, tags.get("addr:city") or area["city"], sector, area["lang"], status, site_text)
        lead = {
            "id": (norm_name(name)[:40] or "lead") + "-ap" + str(abs(hash(email)) % 9999),
            "batch": "Autopilot", "country": area["country"], "company": name, "sector": sector,
            "city": tags.get("addr:city") or area["city"], "status": status,
            "website": website, "email": email, "lang": area["lang"],
            "subject": subj, "body": body, "gmail": gmail_link(email, subj, body),
        }
        new_leads.append(lead)
        seen["emails"].add(email.lower()); seen["names"].add(norm_name(name))
        if dom: seen["domains"].add(dom)
        print("  + lead:", name, "|", status, "|", email)
        time.sleep(0.4)

    # append to the cockpit
    if new_leads:
        data = json.load(open(CLIENTS))
        data += new_leads
        json.dump(data, open(CLIENTS, "w"), ensure_ascii=False, indent=0)
        save_seen(seen)
        # rebuild the dashboard so the console shows the new leads
        if os.path.exists(os.path.join(ROOT, "_build_dashboard.py")):
            subprocess.run([sys.executable, "_build_dashboard.py"], cwd=ROOT, check=False)

    # run digest / log (shift 5)
    os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
    log = [f"# Autopilot run — {datetime.date.today()}",
           f"- Slice: **{area['city']}, {area['country']}** / {niche['key']} ({sector})",
           f"- Overpass candidates scanned: {len(elements)} · sites fetched: {fetches}",
           f"- New qualified leads: **{len(new_leads)}**", "",
           "| Company | Status | Email |", "|---|---|---|"]
    for l in new_leads:
        log.append(f"| {l['company']} | {l['status']} | {l['email']} |")
    open(os.path.join(HERE, "logs", f"{datetime.date.today()}.md"), "w").write("\n".join(log) + "\n")
    print(f"DONE — {len(new_leads)} new leads appended.")

if __name__ == "__main__":
    main()
