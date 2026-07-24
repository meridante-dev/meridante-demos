#!/usr/bin/env python3
"""
WhatsApp lead sweep — find local businesses with a WEAK/absent website AND a
VERIFIED public WhatsApp (or mobile) number, so they can be contacted directly.
Focus: Dutch (NL/BE) + Portuguese markets. Appends to the cockpit as batch
"WhatsApp" with a ready wa.me link. Reuses the autopilot pipeline (run.py).

Usage: python3 autopilot/wa_leads.py [--target 18] [--langs NL,PT] [--budget 300]
"""
import os, sys, json, time, datetime, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import run, wa   # reuse the whole pipeline + the WhatsApp toolkit

CLIENTS = os.path.join(ROOT, "_clients.json")
# WhatsApp-friendly niches (small local businesses that live on WhatsApp + often have weak sites)
WA_NICHES = ["hairdresser", "beauty", "restaurant", "cafe", "car_repair", "gym", "guesthouse"]

def existing_index():
    data = json.load(open(CLIENTS))
    waset = {(x.get("whatsapp") or "").lstrip("+") for x in data if x.get("whatsapp")}
    names = {run.norm_name(x.get("company", "")) for x in data}
    return data, waset, names

def main():
    a = sys.argv[1:]
    target = int(a[a.index("--target") + 1]) if "--target" in a else 18
    langs = (a[a.index("--langs") + 1] if "--langs" in a else "NL,PT").split(",")
    budget = int(a[a.index("--budget") + 1]) if "--budget" in a else 300

    areas = [x for x in run.CFG["areas"] if x["lang"] in langs]
    niches = {n["key"]: n for n in run.CFG["niches"]}
    order = [(ar, niches[k]) for k in WA_NICHES if k in niches for ar in areas]
    # rotate territory by day + hour so each cron run scans fresh ground (dedup handles overlap)
    if order:
        now = datetime.datetime.utcnow()
        off = (now.timetuple().tm_yday * 7 + now.hour) % len(order)
        order = order[off:] + order[:off]

    data, wa_seen, name_seen = existing_index()
    seen = run.load_seen()
    found, fetches, t0 = [], 0, time.time()

    print(f"WA sweep · langs={langs} · target={target}")
    # collect candidate elements across all slices first (cheap: Overpass only), then process
    pool = []   # (area, niche, sector, el)
    for area, niche in order:
        if time.time() - t0 > budget * 0.72:   # PASS 1 is fetch-free, so give collection most of the budget
            break
        sector = niche["sector"].get(area["lang"], niche["key"])
        els = run.overpass(area, niche)
        print(f"  {area['city']}/{niche['key']} :: {len(els)} candidates")
        for el in els:
            pool.append((area, niche, sector, el))
        time.sleep(1)

    def add(area, niche, sector, el, number, src, html):
        tags = el["tags"]
        name = tags.get("name")
        website = tags.get("website") or tags.get("contact:website") or ""
        dom = run.domain_of(website)
        status = el.get("_status") or ("NO-SITE" if not website else "TEMPLATE-BASIC")
        email = run.find_email(tags, html, dom)
        lang = area["lang"]
        subj = body = gmail = ""
        if email:
            try:
                _, subj, body = run.write_email(name, tags.get("addr:city") or area["city"], sector, lang, status, run.html_to_text(html)[:1200])
                gmail = run.gmail_link(email, subj, body)
            except Exception:
                pass
        lead = {
            "id": (run.norm_name(name)[:40] or "lead") + "-wa" + str(abs(hash(number)) % 9999),
            "batch": "WhatsApp", "country": area["country"], "company": name, "sector": sector,
            "niche": niche["key"], "city": tags.get("addr:city") or area["city"], "status": status,
            "website": website, "email": email, "lang": lang,
            "whatsapp": "+" + number, "wa": wa.wa_link(number, lang, name), "wa_src": src,
            "subject": subj, "body": body, "gmail": gmail,
        }
        found.append(lead)
        wa_seen.add(number); name_seen.add(run.norm_name(name))
        seen["names"].add(run.norm_name(name))
        if email: seen["emails"].add(email.lower())
        print(f"    + {name}  |  {status}  |  +{number} ({src})  |  {email or 'no email'}")

    def dup(el, number):
        nm = el["tags"].get("name")
        return (not nm) or run.norm_name(nm) in name_seen or number in wa_seen

    def has_site(el):
        return bool(el["tags"].get("website") or el["tags"].get("contact:website"))

    # PASS 1 — WhatsApp/mobile straight from OSM tags (NO fetch). No-site "potato" businesses first.
    pool.sort(key=lambda t: has_site(t[3]))
    for area, niche, sector, el in pool:
        if len(found) >= target:
            break
        hit = wa.wa_from(el["tags"], "", area["country"])   # tags only, no HTML
        if not hit or dup(el, hit[0]):
            continue
        number, src = hit
        html = ""
        if has_site(el) and fetches < 45 and time.time() - t0 < budget:
            website = el["tags"].get("website") or el["tags"].get("contact:website")
            fetches += 1
            resp, html = run.fetch(website)
            st = run.classify_site(resp, html)
            if st == "MODERN":        # good site → not a potato, skip
                continue
            el["_status"] = st
        add(area, niche, sector, el, number, src, html)

    # PASS 2 — still short: scrape sites for a wa.me click-to-chat link (costs a fetch each).
    for area, niche, sector, el in pool:
        if len(found) >= target or fetches >= 75 or time.time() - t0 > budget:
            break
        if not has_site(el) or wa.wa_from(el["tags"], "", area["country"]):
            continue
        nm = el["tags"].get("name")
        if not nm or run.norm_name(nm) in name_seen:
            continue
        website = el["tags"].get("website") or el["tags"].get("contact:website")
        fetches += 1
        resp, html = run.fetch(website)
        st = run.classify_site(resp, html)
        if st == "MODERN":
            continue
        hit = wa.wa_from(el["tags"], html, area["country"])
        if not hit or dup(el, hit[0]):
            continue
        el["_status"] = st
        add(area, niche, sector, el, hit[0], hit[1], html)

    if found:
        data = json.load(open(CLIENTS))
        data += found
        json.dump(data, open(CLIENTS, "w"), ensure_ascii=False, indent=0)
        run.save_seen(seen)
        # feed the daily digest: append IDs to today's ledger (so they get a mockup + email too)
        led = os.path.join(HERE, "logs", f"{datetime.date.today()}-ids.txt")
        os.makedirs(os.path.dirname(led), exist_ok=True)
        with open(led, "a") as fh:
            for l in found:
                fh.write(l["id"] + "\n")
        import subprocess
        if os.path.exists(os.path.join(ROOT, "_build_dashboard.py")):
            subprocess.run([sys.executable, "_build_dashboard.py"], cwd=ROOT, check=False)
    print(f"\nDONE — {len(found)} WhatsApp leads added (batch 'WhatsApp').")
    for l in found:
        print(f"  {l['company'][:34]:34} {l['country'][:11]:11} {l['status']:14} {l['whatsapp']}")

if __name__ == "__main__":
    main()
