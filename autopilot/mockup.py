#!/usr/bin/env python3
"""
Meridante — per-lead website MOCKUP generator.

Given a lead {company, sector, city, country, lang, status}, produces a
world-class, self-contained single-page website mockup (index.html) themed to
the sector, with REAL stock photography (keyless via Openverse; Pexels if a key
is present) and context-specific copy (Groq if a key is present; graceful
templated fallback otherwise). The render step (render.py) turns it into PNGs.

This is a CONCEPT mockup — a picture of the prospect's *future* site. Copy is
aspirational-but-truthful: no invented dates, awards, numbers, or testimonials.
Images are clearly placeholders (flagged in CREDITS.txt per mockup folder).
"""
import os, re, json, html, urllib.request, urllib.parse, hashlib, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 " \
     "(KHTML, like Gecko) Chrome/122 Safari/537.36"

# ---------------------------------------------------------------- keys (optional)
def _load_env(path):
    d = {}
    try:
        for line in open(os.path.expanduser(path)):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1); d[k.strip()] = v.strip()
    except Exception:
        pass
    return d

_ENV = {}
for p in ("~/.config/watch/.env", "/Volumes/Ultra Touch/Broll-Studio/config/.env"):
    _ENV.update(_load_env(p))
GROQ_KEY = os.environ.get("GROQ_API_KEY") or _ENV.get("GROQ_API_KEY", "")
PEXELS_KEY = os.environ.get("PEXELS_API_KEY") or _ENV.get("PEXELS_API_KEY", "")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

# ---------------------------------------------------------------- sector themes
# Each theme: distinctive font pairing + a restrained premium palette (never the
# purple/blue "AI gradient"), image search seeds, and sector-specific labels.
NEUTRAL = {
    "fonts": ("Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600", "Outfit:wght@300;400;500;600",
              "'Fraunces',Georgia,serif", "'Outfit',system-ui,sans-serif"),
    "vars": {"bg": "#f5f1ea", "bg2": "#efe9dd", "ink": "#1b2530", "ink2": "#54606d",
             "accent": "#b07d3c", "accent2": "#caa063", "dark": "#141b22", "line": "rgba(27,37,48,.12)"},
    "hero": ["elegant business interior", "modern architecture detail"],
    "gallery": ["premium interior design", "warm workspace", "craftsmanship detail"],
    "services": [("Serviço", ""), ("Serviço", ""), ("Serviço", "")],
    "sector": "Empresa local",
}
SECTORS = {
    "dental": {
        "fonts": ("Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600", "Hanken+Grotesk:wght@300;400;500;600",
                  "'Fraunces',Georgia,serif", "'Hanken Grotesk',system-ui,sans-serif"),
        "vars": {"bg": "#f4f7f6", "bg2": "#e8f0ee", "ink": "#0f2b2b", "ink2": "#4c6663",
                 "accent": "#2f7d78", "accent2": "#57a7a0", "dark": "#0c1f1f", "line": "rgba(15,43,43,.10)"},
        "hero": ["modern dental clinic interior bright", "dentist treating patient in chair",
                 "dental reception waiting room", "dentist examining patient teeth"],
        "gallery": ["dental treatment room equipment", "dentist and patient smiling",
                    "dental x-ray tools clean", "bright modern clinic corridor"],
        "labels": {"EN": [("Implants", "Fixed, natural-feeling replacements that last."),
                          ("Orthodontics", "Discreet aligners and braces for every age."),
                          ("Whitening & Hygiene", "Gentle care that keeps smiles bright.")],
                   "ES": [("Implantes", "Reemplazos fijos y naturales que duran."),
                          ("Ortodoncia", "Alineadores y brackets discretos para toda edad."),
                          ("Estética e Higiene", "Cuidado suave que mantiene tu sonrisa radiante.")],
                   "PT": [("Implantes", "Substituições fixas e naturais que duram."),
                          ("Ortodontia", "Alinhadores e aparelhos discretos para todas as idades."),
                          ("Estética e Higiene", "Cuidado suave que mantém o sorriso radiante.")],
                   "FR": [("Implants", "Des remplacements fixes et naturels qui durent."),
                          ("Orthodontie", "Aligneurs et bagues discrets, à tout âge."),
                          ("Esthétique & Hygiène", "Des soins doux qui gardent le sourire éclatant.")],
                   "NL": [("Implantaten", "Vaste, natuurlijke oplossingen die blijven."),
                          ("Orthodontie", "Discrete beugels en aligners, elke leeftijd."),
                          ("Esthetiek & Hygiëne", "Zachte zorg voor een stralende lach.")]},
        "sector": {"EN": "Dental Clinic", "ES": "Clínica Dental", "PT": "Clínica Dentária", "FR": "Cabinet Dentaire", "NL": "Tandartspraktijk"},
    },
    "restaurant": {
        "fonts": ("Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600", "Jost:wght@300;400;500;600",
                  "'Fraunces',Georgia,serif", "'Jost',system-ui,sans-serif"),
        "vars": {"bg": "#14100d", "bg2": "#1c1712", "ink": "#f3ece1", "ink2": "#b7a894",
                 "accent": "#c9713d", "accent2": "#e0a06a", "dark": "#0c0906", "line": "rgba(243,236,225,.14)"},
        "hero": ["fine dining plated dish", "cozy restaurant interior warm light"],
        "gallery": ["gourmet food plating", "restaurant table setting candle", "chef cooking kitchen"],
        "labels": {"EN": [("The Kitchen", "Seasonal plates from what the market gives us."),
                          ("The Cellar", "A short, considered list to match every dish."),
                          ("The Room", "Warm service, unhurried, made for the table.")],
                   "ES": [("La Cocina", "Platos de temporada con lo que da el mercado."),
                          ("La Bodega", "Una carta breve y pensada para cada plato."),
                          ("La Sala", "Servicio cálido, sin prisas, hecho para la mesa.")],
                   "PT": [("A Cozinha", "Pratos de época com o que o mercado dá."),
                          ("A Garrafeira", "Uma carta breve e pensada para cada prato."),
                          ("A Sala", "Serviço caloroso, sem pressas, feito para a mesa.")]},
        "sector": {"EN": "Restaurant", "ES": "Restaurante", "PT": "Restaurante", "FR": "Restaurant"},
    },
    "hair": {
        "fonts": ("Bodoni+Moda:opsz,wght@6..96,400;6..96,500", "Jost:wght@300;400;500;600",
                  "'Bodoni Moda',Georgia,serif", "'Jost',system-ui,sans-serif"),
        "vars": {"bg": "#f6f2ef", "bg2": "#ece3dd", "ink": "#241d1b", "ink2": "#6a5e58",
                 "accent": "#a86b52", "accent2": "#c99277", "dark": "#1a1412", "line": "rgba(36,29,27,.12)"},
        "hero": ["modern hair salon interior", "hairstylist cutting hair studio"],
        "gallery": ["elegant hairstyle woman", "salon styling chair", "hair color treatment"],
        "labels": {"EN": [("Cut & Style", "Shapes tailored to you, not the trend."),
                          ("Colour", "Dimensional, low-damage, luminous."),
                          ("Care Rituals", "Treatments that leave hair alive.")],
                   "ES": [("Corte y Peinado", "Formas a tu medida, no a la moda."),
                          ("Color", "Con dimensión, luminoso y cuidado."),
                          ("Rituales de Cuidado", "Tratamientos que dejan el cabello vivo.")],
                   "PT": [("Corte e Styling", "Formas à tua medida, não à moda."),
                          ("Cor", "Com dimensão, luminosa e cuidada."),
                          ("Rituais de Cuidado", "Tratamentos que deixam o cabelo vivo.")]},
        "sector": {"EN": "Hair Studio", "ES": "Peluquería", "PT": "Cabeleireiro", "FR": "Salon de Coiffure"},
    },
    "estate": {
        "fonts": ("Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600", "Outfit:wght@300;400;500;600",
                  "'Fraunces',Georgia,serif", "'Outfit',system-ui,sans-serif"),
        "vars": {"bg": "#f4efe6", "bg2": "#ece4d6", "ink": "#16202e", "ink2": "#5c6b7a",
                 "accent": "#c2974e", "accent2": "#d9b97e", "dark": "#111926", "line": "rgba(22,32,46,.12)"},
        "hero": ["luxury villa exterior sunset", "modern living room large windows"],
        "gallery": ["luxury home interior", "coastal property view", "modern kitchen design"],
        "labels": {"EN": [("Buy", "A shortlist that fits your life, not the whole market."),
                          ("Sell", "Priced right, staged well, sold with care."),
                          ("Guidance", "One person, start to keys.")],
                   "ES": [("Comprar", "Una selección a tu vida, no todo el mercado."),
                          ("Vender", "Bien tasado, bien presentado, vendido con cuidado."),
                          ("Acompañamiento", "Una sola persona, del inicio a las llaves.")],
                   "PT": [("Comprar", "Uma seleção à sua vida, não o mercado inteiro."),
                          ("Vender", "Bem avaliado, bem apresentado, vendido com cuidado."),
                          ("Acompanhamento", "Uma só pessoa, do início às chaves.")]},
        "sector": {"EN": "Real Estate", "ES": "Inmobiliaria", "PT": "Imobiliária", "FR": "Immobilier"},
    },
    "beauty": {
        "fonts": ("Bodoni+Moda:opsz,wght@6..96,400;6..96,500", "Hanken+Grotesk:wght@300;400;500;600",
                  "'Bodoni Moda',Georgia,serif", "'Hanken Grotesk',system-ui,sans-serif"),
        "vars": {"bg": "#f7f1ef", "bg2": "#efe1de", "ink": "#2a1f22", "ink2": "#6f5c60",
                 "accent": "#b06a72", "accent2": "#cf9299", "dark": "#1c1416", "line": "rgba(42,31,34,.12)"},
        "hero": ["luxury spa treatment room", "facial skincare woman relaxed"],
        "gallery": ["spa candles stones", "beauty skincare products", "manicure hands elegant"],
        "labels": {"EN": [("Skin", "Facials read to your skin, not a menu."),
                          ("Body", "Massage and rituals that reset you."),
                          ("Details", "Nails, brows, the finishing touches.")],
                   "ES": [("Piel", "Faciales a tu piel, no a un menú."),
                          ("Cuerpo", "Masajes y rituales que te reinician."),
                          ("Detalles", "Uñas, cejas, los toques finales.")],
                   "PT": [("Pele", "Faciais à tua pele, não a um menu."),
                          ("Corpo", "Massagens e rituais que te renovam."),
                          ("Detalhes", "Unhas, sobrancelhas, os toques finais.")]},
        "sector": {"EN": "Beauty & Spa", "ES": "Centro de Belleza", "PT": "Estética & Spa", "FR": "Institut de Beauté"},
    },
    "guesthouse": {
        "fonts": ("Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600", "Outfit:wght@300;400;500;600",
                  "'Fraunces',Georgia,serif", "'Outfit',system-ui,sans-serif"),
        "vars": {"bg": "#f3efe7", "bg2": "#e7ddcd", "ink": "#20261f", "ink2": "#5e6857",
                 "accent": "#7d8a4e", "accent2": "#a3ad78", "dark": "#161a12", "line": "rgba(32,38,31,.12)"},
        "hero": ["boutique guesthouse room natural light", "coastal countryside landscape"],
        "gallery": ["cozy bedroom linen", "breakfast table outdoors", "garden terrace view"],
        "labels": {"EN": [("Rooms", "Quiet, light-filled, made to slow down in."),
                          ("Table", "Local breakfast, honest and generous."),
                          ("Place", "The good spots, from people who live here.")],
                   "ES": [("Habitaciones", "Tranquilas, luminosas, para bajar el ritmo."),
                          ("Mesa", "Desayuno local, honesto y generoso."),
                          ("El Lugar", "Los buenos rincones, de quien vive aquí.")],
                   "PT": [("Quartos", "Tranquilos, luminosos, para abrandar."),
                          ("Mesa", "Pequeno-almoço local, honesto e generoso."),
                          ("O Lugar", "Os bons recantos, de quem vive aqui.")]},
        "sector": {"EN": "Guesthouse", "ES": "Casa de Huéspedes", "PT": "Alojamento", "FR": "Maison d'Hôtes", "NL": "Gastenverblijf"},
    },
    "lawyer": {
        "fonts": ("Cormorant+Garamond:wght@500;600", "Jost:wght@300;400;500",
                  "'Cormorant Garamond',Georgia,serif", "'Jost',system-ui,sans-serif"),
        "vars": {"bg": "#f4f4f2", "bg2": "#e9e9e4", "ink": "#1c2530", "ink2": "#586170",
                 "accent": "#8a6d3b", "accent2": "#b08d55", "dark": "#141b24", "line": "rgba(28,37,48,.12)"},
        "hero": ["law office interior professional", "lawyer meeting handshake office"],
        "gallery": ["law books library shelves", "modern office desk minimal", "classical columns building"],
        "labels": {"EN": [("Counsel", "Clear advice, in plain language."),
                          ("Representation", "Steady, prepared, in your corner."),
                          ("Discretion", "Your matter, handled with care.")],
                   "FR": [("Conseil", "Un avis clair, en langage simple."),
                          ("Représentation", "Solide, préparé, à vos côtés."),
                          ("Discrétion", "Votre dossier, traité avec soin.")],
                   "NL": [("Advies", "Helder advies, in gewone taal."),
                          ("Vertegenwoordiging", "Vast, voorbereid, aan uw zijde."),
                          ("Discretie", "Uw zaak, met zorg behandeld.")],
                   "PT": [("Aconselhamento", "Conselho claro, em linguagem simples."),
                          ("Representação", "Firme, preparado, ao seu lado."),
                          ("Discrição", "O seu caso, tratado com cuidado.")]},
        "sector": {"EN": "Law Firm", "FR": "Cabinet d'Avocats", "NL": "Advocatenkantoor", "PT": "Escritório de Advocacia", "ES": "Bufete de Abogados"},
    },
    "gym": {
        "fonts": ("Archivo:wght@600;700;800", "Jost:wght@300;400;500",
                  "'Archivo',system-ui,sans-serif", "'Jost',system-ui,sans-serif"),
        "vars": {"bg": "#14161a", "bg2": "#1d2026", "ink": "#f2f1ee", "ink2": "#a7abb3",
                 "accent": "#c7642f", "accent2": "#e08a4f", "dark": "#0d0f12", "line": "rgba(242,241,238,.12)"},
        "hero": ["modern gym interior dark", "athlete training weights gym"],
        "gallery": ["dumbbells rack gym", "fitness group class", "person stretching workout"],
        "labels": {"EN": [("Train", "Coaching that meets you where you are."),
                          ("Strength", "Programmes built for real progress."),
                          ("Community", "People who show up for each other.")],
                   "FR": [("S'entraîner", "Un coaching adapté à votre niveau."),
                          ("Force", "Des programmes pour de vrais progrès."),
                          ("Communauté", "Des gens présents les uns pour les autres.")],
                   "NL": [("Trainen", "Coaching op jouw niveau."),
                          ("Kracht", "Programma's voor echte vooruitgang."),
                          ("Community", "Mensen die er voor elkaar zijn.")],
                   "PT": [("Treinar", "Treino adaptado ao seu nível."),
                          ("Força", "Programas para progresso real."),
                          ("Comunidade", "Pessoas presentes umas para as outras.")]},
        "sector": {"EN": "Fitness Studio", "FR": "Salle de Sport", "NL": "Sportschool", "PT": "Ginásio", "ES": "Gimnasio"},
    },
}
# keyword -> sector key (multilingual-ish, matched against the lead 'sector' text)
# canonical niche key (from the autopilot config, stored on the lead) → theme. EXACT, language-proof.
NICHE2THEME = {
    "restaurant": "restaurant", "cafe": "restaurant", "hairdresser": "hair", "beauty": "beauty",
    "estate": "estate", "dentist": "dental", "guesthouse": "guesthouse",
    "lawyer": "lawyer", "gym": "gym", "car_repair": "neutral",
}
# fallback keyword map for LEGACY leads (no niche field) — multilingual EN/ES/PT/FR/NL.
KEYMAP = [
    ("dental", "dental"), ("dentist", "dental"), ("dentária", "dental"), ("dentaria", "dental"),
    ("odont", "dental"), ("clínica dental", "dental"),
    ("dentaire", "dental"), ("tandarts", "dental"), ("tandheelkun", "dental"), ("tandheelkundig", "dental"),
    ("ortho", "dental"), ("orthodont", "dental"), ("parodont", "dental"), ("kaakchirurg", "dental"), ("implantol", "dental"),
    ("restaur", "restaurant"), ("tasca", "restaurant"), ("bistro", "restaurant"), ("marisq", "restaurant"),
    ("brasserie", "restaurant"), ("eetcaf", "restaurant"), ("trattoria", "restaurant"), ("pizz", "restaurant"),
    ("cafe", "restaurant"), ("café", "restaurant"), ("cervej", "restaurant"),
    ("cabelei", "hair"), ("peluqu", "hair"), ("hair", "hair"), ("coiff", "hair"), ("barb", "hair"),
    ("kapper", "hair"), ("kapsalon", "hair"), ("kapster", "hair"), ("friseur", "hair"),
    ("imobil", "estate"), ("inmobil", "estate"), ("estate", "estate"), ("immo", "estate"),
    ("makelaar", "estate"), ("makelaardij", "estate"), ("vastgoed", "estate"),
    ("beaut", "beauty"), ("belleza", "beauty"), ("beauté", "beauty"), ("estét", "beauty"), ("estet", "beauty"),
    ("esthé", "beauty"), ("esthe", "beauty"), ("schoonheid", "beauty"), ("kosmet", "beauty"), ("spa", "beauty"), ("wellness", "beauty"),
    ("guest", "guesthouse"), ("aloj", "guesthouse"), ("huésp", "guesthouse"), ("hotel", "guesthouse"),
    ("hostel", "guesthouse"), ("hôtes", "guesthouse"), ("gasten", "guesthouse"), ("logies", "guesthouse"),
    ("advoca", "lawyer"), ("avocat", "lawyer"), ("abogad", "lawyer"), ("lawyer", "lawyer"), ("law firm", "lawyer"),
    ("notari", "lawyer"), ("juridi", "lawyer"), ("advogad", "lawyer"),
    ("gym", "gym"), ("fitness", "gym"), ("ginás", "gym"), ("sportschool", "gym"), ("salle de sport", "gym"),
    ("gimnas", "gym"), ("crossfit", "gym"), ("pilates", "gym"), ("yoga", "gym"),
]

def theme_for(lead):
    # 1) exact niche from the pipeline (preferred — never mis-guesses on a foreign-language name)
    nk = str(lead.get("niche", "")).lower().strip()
    if nk in NICHE2THEME:
        key = NICHE2THEME[nk]
        return key, SECTORS.get(key, NEUTRAL)
    # 2) legacy fallback: keyword-match sector + company
    s = (str(lead.get("sector", "")) + " " + str(lead.get("company", ""))).lower()
    for kw, key in KEYMAP:
        if kw in s:
            return key, SECTORS.get(key, NEUTRAL)
    return "neutral", NEUTRAL

# ---------------------------------------------------------------- images
def _slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")[:60] or "x"

def _get(url, timeout=20, headers=None):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=timeout)

def _pexels_search(query, n):
    if not PEXELS_KEY:
        return []
    try:
        u = "https://api.pexels.com/v1/search?" + urllib.parse.urlencode(
            {"query": query, "per_page": n, "orientation": "landscape", "size": "large"})
        req = urllib.request.Request(u, headers={"User-Agent": UA, "Authorization": PEXELS_KEY})
        d = json.load(urllib.request.urlopen(req, timeout=20))
        return [p["src"]["large2x"] for p in d.get("photos", [])]
    except Exception:
        return []

def _openverse_search(query, n):
    out = []
    try:
        u = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(
            {"q": query, "license": "cc0,pdm,by", "page_size": max(n, 6),
             "mature": "false", "aspect_ratio": "wide"})
        d = json.load(_get(u, timeout=12, headers={"User-Agent": "MeridanteMockup/1.0"}))
        for r in d.get("results", []):
            url = r.get("url")
            if url and (r.get("width") or 0) >= 900:
                out.append(url)
    except Exception:
        pass
    return out[:max(n, 6)]

def fetch_images(queries, outdir, want=4, seed=0):
    """Download up to `want` distinct stock photos for the given search seeds.
    A per-lead `seed` rotates the candidate pool so different leads in the same
    sector get visually DIFFERENT photography (no two mockups look identical).
    Returns list of local relative filenames actually saved (may be < want)."""
    os.makedirs(outdir, exist_ok=True)
    # build a de-duplicated candidate pool across seed queries; stop early once
    # the pool is deep enough to give variety (keeps runs fast).
    pool, seen = [], set()
    for q in queries:
        for url in (_pexels_search(q, 6) + _openverse_search(q, 8)):
            h = hashlib.md5(url.encode()).hexdigest()[:8]
            if h not in seen:
                seen.add(h); pool.append((h, url))
        if len(pool) >= want + 12:
            break
    # rotate by seed so lead A and lead B start at different photos
    if pool:
        off = seed % len(pool)
        pool = pool[off:] + pool[:off]
    saved = []
    for h, url in pool:
        if len(saved) >= want:
            break
        name = f"img-{len(saved)+1}-{h}.jpg"
        try:
            data = _get(url, timeout=25, headers={"User-Agent": UA}).read()
            if len(data) < 6000:  # too small / error page
                continue
            with open(os.path.join(outdir, name), "wb") as fh:
                fh.write(data)
            saved.append(name)
        except Exception:
            continue
    return saved

# ---------------------------------------------------------------- copy (Groq)
def _groq_copy(lead, theme_key, lang):
    if not GROQ_KEY:
        return None
    sector = _sector_label(theme_key, lang)
    sys = ("You write concise, premium website copy for a small local business. "
           "Output STRICT JSON only. Be aspirational but truthful: invent NO dates, "
           "numbers, awards, prices, or testimonials. No em-dashes. Write in the target language.")
    usr = json.dumps({
        "business": lead.get("company"), "sector": sector,
        "city": lead.get("city") or lead.get("country"), "language": lang,
        "want": {"eyebrow": "2-4 words", "headline": "6-11 words, no business name",
                 "sub": "1 sentence under 22 words", "cta": "2-3 words",
                 "why_title": "3-6 words", "why": "3 short benefit bullets, max 7 words each",
                 "promise": "1 warm sentence under 18 words"}}, ensure_ascii=False)
    try:
        body = json.dumps({"model": GROQ_MODEL, "temperature": 0.7,
                           "response_format": {"type": "json_object"},
                           "messages": [{"role": "system", "content": sys},
                                        {"role": "user", "content": usr}]}).encode()
        req = urllib.request.Request("https://api.groq.com/openai/v1/chat/completions", data=body,
                                     headers={"Authorization": f"Bearer {GROQ_KEY}",
                                              "Content-Type": "application/json", "User-Agent": UA})
        d = json.load(urllib.request.urlopen(req, timeout=30))
        c = json.loads(d["choices"][0]["message"]["content"])
        if c.get("headline") and c.get("sub"):
            return c
    except Exception:
        return None
    return None

FALLBACK = {
    "EN": {"eyebrow": "Welcome", "headline": "Work worth being seen properly",
           "sub": "A calmer, clearer home for {city} customers to find you and choose you.",
           "cta": "Get in touch", "why_title": "Why people stay",
           "why": ["Care in every detail", "Clear, honest guidance", "Made for real people"],
           "promise": "The same care you give your work, now in how you are found online."},
    "ES": {"eyebrow": "Bienvenido", "headline": "Un trabajo que merece verse bien",
           "sub": "Un hogar online más claro para que en {city} te encuentren y te elijan.",
           "cta": "Contactar", "why_title": "Por qué se quedan",
           "why": ["Cuidado en cada detalle", "Orientación clara y honesta", "Hecho para personas reales"],
           "promise": "El mismo cuidado que pones en tu trabajo, ahora en cómo te encuentran."},
    "PT": {"eyebrow": "Bem-vindo", "headline": "Um trabalho que merece ser bem visto",
           "sub": "Uma casa online mais clara para que em {city} o encontrem e o escolham.",
           "cta": "Contactar", "why_title": "Porque ficam",
           "why": ["Cuidado em cada detalhe", "Orientação clara e honesta", "Feito para pessoas reais"],
           "promise": "O mesmo cuidado que põe no seu trabalho, agora em como o encontram online."},
    "FR": {"eyebrow": "Bienvenue", "headline": "Un travail qui mérite d'être bien vu",
           "sub": "Un espace en ligne plus clair pour qu'à {city} on vous trouve et vous choisisse.",
           "cta": "Nous contacter", "why_title": "Pourquoi ils restent",
           "why": ["Du soin dans chaque détail", "Un accompagnement clair", "Fait pour de vraies personnes"],
           "promise": "Le même soin que dans votre travail, désormais dans votre présence en ligne."},
}

def _sector_label(theme_key, lang):
    if theme_key == "neutral":
        return {"EN": "Local Business", "ES": "Negocio Local", "PT": "Negócio Local", "FR": "Entreprise Locale"}.get(lang, "Local Business")
    sec = SECTORS[theme_key]["sector"]
    return sec.get(lang, sec.get("EN"))

def get_copy(lead, theme_key, lang):
    city = lead.get("city") or lead.get("country") or ""
    c = _groq_copy(lead, theme_key, lang) or {}
    fb = FALLBACK.get(lang, FALLBACK["EN"])
    out = {}
    out["eyebrow"] = c.get("eyebrow") or fb["eyebrow"]
    out["headline"] = c.get("headline") or fb["headline"]
    out["sub"] = c.get("sub") or fb["sub"].format(city=city)
    out["cta"] = c.get("cta") or fb["cta"]
    out["why_title"] = c.get("why_title") or fb["why_title"]
    why = c.get("why") if isinstance(c.get("why"), list) and len(c.get("why")) >= 3 else fb["why"]
    out["why"] = why[:3]
    out["promise"] = c.get("promise") or fb["promise"]
    # services: sector labels (localized), fall back to neutral
    theme = SECTORS.get(theme_key, NEUTRAL)
    labels = theme.get("labels", {}).get(lang) or theme.get("labels", {}).get("EN")
    if not labels:
        labels = [(out["why_title"], out["promise"])] * 3
    out["services"] = labels[:3]
    out["sector_label"] = _sector_label(theme_key, lang)
    return out

# ---------------------------------------------------------------- template
TEMPLATE = r"""<!-- CONCEPT MOCKUP for {{BRAND}} — Meridante. Placeholder stock imagery, flagged in CREDITS.txt. -->
<!DOCTYPE html>
<html lang="{{LANG}}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{BRAND}} — {{SECTOR}} · {{CITY}}</title>
<meta name="description" content="{{SUB}}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family={{FONT1}}&family={{FONT2}}&display=swap" rel="stylesheet">
<style>
:root{
  --bg:{{BG}}; --bg2:{{BG2}}; --ink:{{INK}}; --ink2:{{INK2}};
  --accent:{{ACCENT}}; --accent2:{{ACCENT2}}; --dark:{{DARK}}; --line:{{LINE}};
  --serif:{{SERIF}}; --sans:{{SANS}}; --maxw:1240px;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:var(--sans);background:var(--bg);color:var(--ink);line-height:1.6;
  -webkit-font-smoothing:antialiased;overflow-x:hidden}
h1,h2,h3{font-family:var(--serif);font-weight:500;line-height:1.06;letter-spacing:-.015em}
a{color:inherit;text-decoration:none}
img{max-width:100%;display:block}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 clamp(20px,5vw,56px)}
.eyebrow{font-family:var(--sans);font-size:.72rem;font-weight:600;letter-spacing:.26em;
  text-transform:uppercase;color:var(--accent);display:inline-flex;align-items:center;gap:.7em}
.eyebrow::before{content:"";width:26px;height:1px;background:var(--accent);opacity:.8}
.btn{display:inline-flex;align-items:center;gap:.55em;font-family:var(--sans);font-weight:600;
  font-size:.9rem;letter-spacing:.01em;padding:.9em 1.6em;border-radius:3px;cursor:pointer;
  border:1px solid transparent;transition:transform .35s cubic-bezier(.2,.8,.2,1),box-shadow .35s,background .35s,color .35s}
.btn-a{background:var(--accent);color:#fff;box-shadow:0 14px 34px -16px var(--accent)}
.btn-a:hover{transform:translateY(-2px);background:var(--accent2)}
.btn-line{border-color:currentColor;opacity:.9}
.btn-line:hover{color:var(--accent);border-color:var(--accent)}
/* header */
header{position:absolute;top:0;left:0;right:0;z-index:30}
.nav{display:flex;align-items:center;justify-content:space-between;padding:26px 0}
.brand{font-family:var(--serif);font-size:1.4rem;font-weight:600;color:#fff;display:flex;align-items:center;gap:.55em}
.brand .dot{width:11px;height:11px;border-radius:50%;background:var(--accent);box-shadow:0 0 0 4px rgba(255,255,255,.14)}
.navlinks{display:flex;gap:34px;font-size:.9rem;font-weight:500;color:rgba(255,255,255,.86)}
.navlinks a{position:relative;padding:4px 0}
.navlinks a::after{content:"";position:absolute;left:0;bottom:-2px;width:0;height:1px;background:var(--accent);transition:width .3s}
.navlinks a:hover::after{width:100%}
.nav .btn-a{padding:.7em 1.3em}
/* hero */
.hero{position:relative;min-height:100vh;display:flex;align-items:center;color:#fff;overflow:hidden}
.hero-bg{position:absolute;inset:0;z-index:0}
.hero-bg img{width:100%;height:100%;object-fit:cover;transform:scale(1.04)}
.hero-bg::after{content:"";position:absolute;inset:0;
  background:linear-gradient(105deg,rgba(8,12,16,.86) 0%,rgba(8,12,16,.55) 46%,rgba(8,12,16,.2) 100%),
             linear-gradient(0deg,rgba(8,12,16,.6),transparent 40%)}
.hero-inner{position:relative;z-index:2;max-width:660px;padding-block:120px}
.hero h1{font-size:clamp(2.6rem,5.6vw,4.5rem);margin:.3em 0 .5em;color:#fff}
.hero p.lead{font-size:clamp(1.05rem,1.5vw,1.28rem);color:rgba(255,255,255,.9);max-width:34em;font-weight:300}
.hero .cta{display:flex;gap:14px;margin-top:2.4em;flex-wrap:wrap}
.stats{display:flex;gap:38px;margin-top:3.2em;flex-wrap:wrap}
.stat .n{font-family:var(--serif);font-size:1.9rem;color:#fff;line-height:1}
.stat .l{font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:rgba(255,255,255,.66);margin-top:.5em}
.scrollcue{position:absolute;bottom:34px;left:50%;transform:translateX(-50%);z-index:2;
  font-size:.68rem;letter-spacing:.24em;text-transform:uppercase;color:rgba(255,255,255,.6)}
/* sections */
section{position:relative}
.section{padding:clamp(70px,10vw,130px) 0}
.shead{max-width:640px;margin-bottom:56px}
.shead h2{font-size:clamp(1.9rem,3.4vw,3rem);margin:.35em 0}
.shead p{color:var(--ink2);font-size:1.05rem;max-width:36em}
/* services */
.svcs{display:grid;grid-template-columns:repeat(3,1fr);gap:26px}
.svc{background:#fff;border:1px solid var(--line);border-radius:14px;padding:38px 32px;
  box-shadow:0 24px 50px -34px rgba(20,27,34,.35);transition:transform .4s cubic-bezier(.2,.8,.2,1),box-shadow .4s}
.svc:hover{transform:translateY(-6px);box-shadow:0 34px 60px -34px rgba(20,27,34,.5)}
.svc .ic{width:46px;height:46px;border-radius:11px;display:grid;place-items:center;margin-bottom:22px;
  background:var(--bg2);color:var(--accent)}
.svc h3{font-size:1.4rem;margin-bottom:.4em}
.svc p{color:var(--ink2);font-size:.98rem}
.dark-svc .svc{background:rgba(255,255,255,.03);border-color:var(--line);box-shadow:none;backdrop-filter:blur(6px)}
/* feature split */
.split{display:grid;grid-template-columns:1.05fr .95fr;gap:clamp(30px,5vw,72px);align-items:center}
.split .media{border-radius:16px;overflow:hidden;aspect-ratio:4/5;box-shadow:0 40px 80px -40px rgba(20,27,34,.55)}
.split .media img{width:100%;height:100%;object-fit:cover}
.why{list-style:none;margin-top:26px;display:grid;gap:16px}
.why li{display:flex;gap:14px;align-items:flex-start;font-size:1.06rem}
.why .ck{flex:0 0 auto;width:26px;height:26px;border-radius:50%;background:var(--accent);color:#fff;
  display:grid;place-items:center;margin-top:2px;font-size:.8rem}
/* gallery */
.gal{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.gal .g{border-radius:12px;overflow:hidden;aspect-ratio:1/1}
.gal .g:first-child{grid-row:span 2;aspect-ratio:auto}
.gal img{width:100%;height:100%;object-fit:cover;transition:transform .6s}
.gal .g:hover img{transform:scale(1.05)}
/* cta band */
.band{background:var(--dark);color:#fff;border-radius:20px;padding:clamp(48px,7vw,88px);
  text-align:center;position:relative;overflow:hidden}
.band::before{content:"";position:absolute;inset:0;
  background:radial-gradient(120% 120% at 80% -10%,var(--accent) 0%,transparent 55%);opacity:.28}
.band h2{position:relative;font-size:clamp(2rem,4vw,3.2rem);color:#fff;max-width:16em;margin:0 auto .6em}
.band p{position:relative;color:rgba(255,255,255,.78);max-width:30em;margin:0 auto 2em}
.band .btn-a{position:relative;background:#fff;color:var(--dark)}
.band .btn-a:hover{background:var(--accent);color:#fff}
/* footer */
footer{background:var(--bg2);color:var(--ink2);padding:70px 0 40px;font-size:.92rem}
.foot{display:flex;justify-content:space-between;gap:40px;flex-wrap:wrap;border-bottom:1px solid var(--line);padding-bottom:36px}
.foot .brand{color:var(--ink);font-size:1.3rem}
.foot-cols{display:flex;gap:64px;flex-wrap:wrap}
.foot-cols h4{font-family:var(--sans);font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:var(--ink);margin-bottom:14px}
.foot-cols a,.foot-cols span{display:block;margin-bottom:9px;color:var(--ink2)}
.copy{padding-top:26px;font-size:.8rem;color:var(--ink2);display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px}
.ribbon{display:inline-flex;align-items:center;gap:.5em;font-size:.72rem;letter-spacing:.1em;color:var(--accent)}
@media(max-width:860px){
  .svcs,.gal{grid-template-columns:1fr}.split{grid-template-columns:1fr}
  .navlinks{display:none}.gal .g:first-child{grid-row:auto}
}
</style>
</head>
<body>
<header><div class="wrap nav">
  <div class="brand"><span class="dot"></span>{{BRAND}}</div>
  <nav class="navlinks">{{NAVLINKS}}</nav>
  <a class="btn btn-a">{{CTA}}</a>
</div></header>

<section class="hero">
  <div class="hero-bg"><img src="{{HERO_IMG}}" alt=""></div>
  <div class="wrap hero-inner">
    <span class="eyebrow" style="color:var(--accent2)">{{EYEBROW}}</span>
    <h1>{{HEADLINE}}</h1>
    <p class="lead">{{SUB}}</p>
    <div class="cta"><a class="btn btn-a">{{CTA}}</a><a class="btn btn-line" style="color:#fff">{{SECTOR}}</a></div>
    <div class="stats">{{STATS}}</div>
  </div>
  <div class="scrollcue">{{CITY}}</div>
</section>

<section class="section"><div class="wrap">
  <div class="shead"><span class="eyebrow">{{SVC_EYEBROW}}</span><h2>{{SVC_TITLE}}</h2>
  <p>{{PROMISE}}</p></div>
  <div class="svcs">{{SERVICES}}</div>
</div></section>

<section class="section" style="background:var(--bg2)"><div class="wrap">
  <div class="split">
    <div class="media"><img src="{{FEATURE_IMG}}" alt=""></div>
    <div><span class="eyebrow">{{WHY_EYEBROW}}</span><h2>{{WHY_TITLE}}</h2>
      <ul class="why">{{WHY}}</ul>
      <div style="margin-top:32px"><a class="btn btn-a">{{CTA}}</a></div>
    </div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="shead"><span class="eyebrow">{{GAL_EYEBROW}}</span><h2>{{GAL_TITLE}}</h2></div>
  <div class="gal">{{GALLERY}}</div>
</div></section>

<section class="section"><div class="wrap"><div class="band">
  <h2>{{HEADLINE}}</h2><p>{{PROMISE}}</p><a class="btn btn-a">{{CTA}}</a>
</div></div></section>

<footer><div class="wrap">
  <div class="foot">
    <div><div class="brand"><span class="dot"></span>{{BRAND}}</div>
      <p style="margin-top:14px;max-width:22em">{{SECTOR}} · {{CITY}}</p></div>
    <div class="foot-cols">
      <div><h4>{{F_EXPLORE}}</h4>{{NAVLINKS_F}}</div>
      <div><h4>{{F_VISIT}}</h4><span>{{CITY}}</span><span>{{F_HOURS}}</span><a>{{CTA}}</a></div>
    </div>
  </div>
  <div class="copy"><span>© {{BRAND}}</span>
    <span class="ribbon">◆ {{F_CONCEPT}}</span></div>
</div></footer>
</body>
</html>"""

CHECK = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M20 6L9 17l-5-5"/></svg>'
SVC_IC = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="9"/><path d="M8 12l2.5 2.5L16 9"/></svg>'

NAV = {"EN": ["Services", "About", "Gallery", "Contact"],
       "ES": ["Servicios", "Nosotros", "Galería", "Contacto"],
       "PT": ["Serviços", "Sobre", "Galeria", "Contacto"],
       "FR": ["Services", "À propos", "Galerie", "Contact"]}
WORDS = {"EN": ("Our craft", "What we do", "Close up", "In our care", "Explore", "Visit", "By appointment", "Concept preview by Meridante"),
         "ES": ("Nuestro oficio", "Lo que hacemos", "De cerca", "A tu cuidado", "Explorar", "Visítanos", "Con cita previa", "Vista previa de Meridante"),
         "PT": ("O nosso ofício", "O que fazemos", "De perto", "Ao seu cuidado", "Explorar", "Visite", "Com marcação", "Pré-visualização Meridante"),
         "FR": ("Notre métier", "Ce que nous faisons", "De près", "À vos soins", "Explorer", "Visiter", "Sur rendez-vous", "Aperçu concept par Meridante")}
STATS = {"EN": [("★★★★★", "What we aim for"), ("100%", "Care, every visit"), ("You", "At the centre")],
         "ES": [("★★★★★", "Nuestra meta"), ("100%", "Cuidado, cada visita"), ("Tú", "En el centro")],
         "PT": [("★★★★★", "O nosso objetivo"), ("100%", "Cuidado, cada visita"), ("Você", "No centro")],
         "FR": [("★★★★★", "Notre objectif"), ("100%", "Du soin, chaque visite"), ("Vous", "Au centre")]}

def build_html(lead, outdir, idx=0):
    lang = (lead.get("lang") or "EN").upper()[:2]
    if lang not in NAV:
        lang = "EN"
    theme_key, theme = theme_for(lead)
    copy = get_copy(lead, theme_key, lang)
    brand = lead.get("company") or "Studio"
    city = lead.get("city") or lead.get("country") or ""

    # imagery: seed from the lead id so same-sector leads differ visually. The
    # seed rotates the (on-subject) candidate pool, so lead A's hero != lead B's.
    seed = int(hashlib.md5((lead.get("id") or brand).encode()).hexdigest(), 16) % 997
    # +idx*5 spreads same-batch leads apart in the pool so heroes never repeat
    queries = list(theme["hero"]) + list(theme["gallery"])
    imgs = fetch_images(queries, outdir, want=5, seed=seed + idx * 5)
    def img_or_grad(i):
        return imgs[i] if i < len(imgs) else ""
    hero = img_or_grad(0)
    feature = img_or_grad(1) if len(imgs) > 1 else hero
    gal = imgs[2:5] if len(imgs) > 2 else imgs[:3]
    while len(gal) < 3 and imgs:
        gal.append(imgs[-1])
    # if no hero image downloaded, use a premium gradient background instead of a broken img
    grad = f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='1440' height='900'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0' y1='0' x2='1' y2='1'%3E%3Cstop offset='0' stop-color='{urllib.parse.quote(theme['vars']['dark'])}'/%3E%3Cstop offset='1' stop-color='{urllib.parse.quote(theme['vars']['accent'])}'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='1440' height='900' fill='url(%23g)'/%3E%3C/svg%3E"
    hero_src = hero or grad
    feature_src = feature or grad

    f1, f2, serif, sans = theme["fonts"]
    v = theme["vars"]
    nav = NAV[lang]; w = WORDS[lang]; st = STATS[lang]

    navlinks = "".join(f'<a>{html.escape(x)}</a>' for x in nav)
    navlinks_f = "".join(f'<a>{html.escape(x)}</a>' for x in nav)
    stats = "".join(f'<div class="stat"><div class="n">{html.escape(n)}</div><div class="l">{html.escape(l)}</div></div>' for n, l in st)
    services = "".join(
        f'<div class="svc"><div class="ic">{SVC_IC}</div><h3>{html.escape(t)}</h3><p>{html.escape(d)}</p></div>'
        for t, d in copy["services"])
    why = "".join(f'<li><span class="ck">{CHECK}</span><span>{html.escape(b)}</span></li>' for b in copy["why"])
    gallery = "".join(f'<div class="g"><img src="{html.escape(g)}" alt=""></div>' for g in gal[:3])

    repl = {
        "LANG": lang.lower(), "BRAND": html.escape(brand), "SECTOR": html.escape(copy["sector_label"]),
        "CITY": html.escape(city), "SUB": html.escape(copy["sub"]),
        "FONT1": f1, "FONT2": f2, "SERIF": serif, "SANS": sans,
        "BG": v["bg"], "BG2": v["bg2"], "INK": v["ink"], "INK2": v["ink2"],
        "ACCENT": v["accent"], "ACCENT2": v["accent2"], "DARK": v["dark"], "LINE": v["line"],
        "NAVLINKS": navlinks, "NAVLINKS_F": navlinks_f, "CTA": html.escape(copy["cta"]),
        "HERO_IMG": hero_src, "FEATURE_IMG": feature_src,
        "EYEBROW": html.escape(copy["eyebrow"]), "HEADLINE": html.escape(copy["headline"]),
        "STATS": stats, "SVC_EYEBROW": html.escape(w[1]), "SVC_TITLE": html.escape(copy["why_title"]),
        "PROMISE": html.escape(copy["promise"]), "SERVICES": services,
        "WHY_EYEBROW": html.escape(w[0]), "WHY_TITLE": html.escape(copy["why_title"]), "WHY": why,
        "GAL_EYEBROW": html.escape(w[2]), "GAL_TITLE": html.escape(w[3]), "GALLERY": gallery,
        "F_EXPLORE": html.escape(w[4]), "F_VISIT": html.escape(w[5]), "F_HOURS": html.escape(w[6]),
        "F_CONCEPT": html.escape(w[7]),
    }
    out = TEMPLATE
    for k, val in repl.items():
        out = out.replace("{{" + k + "}}", str(val))

    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "index.html"), "w") as fh:
        fh.write(out)
    # credits / placeholder flag
    with open(os.path.join(outdir, "CREDITS.txt"), "w") as fh:
        fh.write(f"CONCEPT MOCKUP for {brand} — Meridante.\n"
                 f"Stock imagery is PLACEHOLDER (Openverse CC0/PD or Pexels), for preview only.\n"
                 f"Theme: {theme_key} | lang: {lang} | copy: {'Groq' if GROQ_KEY else 'template'}.\n"
                 f"Images saved: {imgs}\n")
    return {"dir": outdir, "theme": theme_key, "lang": lang, "images": len(imgs),
            "html": os.path.join(outdir, "index.html")}

if __name__ == "__main__":
    import sys
    lead = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {
        "company": "Clínica Dental Sonrisa", "sector": "Clínica dental",
        "city": "Málaga", "country": "Spain", "lang": "ES", "status": "OUTDATED"}
    out = os.path.join(HERE, "mockups", _slug(lead["company"]))
    print(json.dumps(build_html(lead, out), ensure_ascii=False, indent=2))
