#!/usr/bin/env python3
"""
WhatsApp contact extraction — VERIFIED public numbers only (never invented).

Priority of trust:
  1. a wa.me / api.whatsapp.com click-to-chat link on the business's own site  → definitely WhatsApp
  2. an OSM `contact:whatsapp` tag                                              → definitely WhatsApp
  3. an OSM `contact:mobile` / `mobile` tag that is a real mobile number        → almost certainly WhatsApp
  4. an OSM `phone` / `contact:phone` that is a MOBILE number                   → likely WhatsApp
Landlines are rejected (they are not WhatsApp). Everything is normalised to an
international, digits-only number so a wa.me/<number> link works directly.
"""
import re, urllib.parse

# country name -> calling code (the markets the autopilot covers)
CC = {"Netherlands": "31", "Belgium": "32", "Portugal": "351", "Luxembourg": "352",
      "Spain": "34", "France": "33"}
# international mobile prefixes (NL 06→316, BE 04→324, PT 9→3519, LU 6→3526, ES 6/7→346/347, FR 6/7→336/337)
MOBILE_PREFIX = ("316", "324", "3519", "3526", "346", "347", "336", "337")

WA_LINK_RE = re.compile(
    r'(?:wa\.me/|api\.whatsapp\.com/send\?phone=|whatsapp://send\?phone=|chat\.whatsapp\.com/send\?phone=)'
    r'(\+?\d[\d\s().\-]{6,}\d)', re.I)

def norm_wa(raw, cc):
    """Best-effort normalise a raw phone string to international digits. '' if implausible."""
    if not raw:
        return ""
    raw = str(raw).split(";")[0].split(",")[0].strip()
    intl = raw.startswith("+") or raw.startswith("00")
    d = re.sub(r"\D", "", raw)
    if raw.startswith("00"):
        d = d[2:]
    if not d or len(d) < 6:
        return ""
    if intl:
        n = d
    elif d.startswith("0"):
        n = (cc + d[1:]) if cc else d
    elif cc and d.startswith(cc):
        n = d
    elif cc:
        n = cc + d
    else:
        n = d
    return n if 9 <= len(n) <= 14 else ""

def is_mobile(intl):
    return intl.startswith(MOBILE_PREFIX)

def wa_from(tags, html, country):
    """Return (intl_number, source) or None. tags = OSM tag dict, html = site HTML."""
    cc = CC.get(country, "")
    tags = tags or {}
    # 1) explicit OSM whatsapp
    for k in ("contact:whatsapp", "whatsapp"):
        n = norm_wa(tags.get(k, ""), cc)
        if n:
            return n, "osm:whatsapp"
    # 2) wa.me / api link on their site
    if html:
        for m in WA_LINK_RE.findall(html):
            n = norm_wa(m, cc)
            if n:
                return n, "site:wa.me"
    # 3) OSM mobile
    for k in ("contact:mobile", "mobile"):
        n = norm_wa(tags.get(k, ""), cc)
        if n and is_mobile(n):
            return n, "osm:mobile"
    # 4) OSM phone if it is a mobile
    for k in ("phone", "contact:phone"):
        n = norm_wa(tags.get(k, ""), cc)
        if n and is_mobile(n):
            return n, "osm:phone"
    return None

WA_MSG = {
    "NL": ("Hoi, ik ben João van Meridante. Ik help lokale ondernemers aan een sterkere, modernere website. "
           "Mag ik u vrijblijvend een klein voorbeeld laten zien van hoe die van {company} eruit zou kunnen zien?"),
    "PT": ("Olá, sou o João da Meridante. Ajudo negócios locais a terem um site mais forte e moderno. "
           "Posso mostrar-lhe, sem compromisso, um exemplo de como poderia ficar o site da {company}?"),
    "FR": ("Bonjour, je suis João de Meridante. J'aide les commerces locaux à avoir un site plus moderne. "
           "Puis-je vous montrer, sans engagement, un exemple de ce que pourrait être le site de {company} ?"),
    "EN": ("Hi, I'm João from Meridante. I help local businesses with a stronger, more modern website. "
           "May I show you a quick, no-obligation example of what {company}'s site could look like?"),
}

def wa_link(intl, lang, company):
    msg = WA_MSG.get(lang, WA_MSG["EN"]).format(company=company)
    return "https://wa.me/" + intl + "?text=" + urllib.parse.quote(msg)
