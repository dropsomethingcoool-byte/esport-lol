#!/usr/bin/env python3
"""Validation SEO de la page paris (et générique) : règles de rédaction + maillage."""
import json, re, sys, html as H

def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def text(html):
    return re.sub(r"<[^>]+>", " ", html)

def main():
    p = load("/Users/charlesploteau/esport-lol/content/parier-worlds-lol.json")
    body = p["body"]
    intro = p["intro"]
    errs, warns = [], []

    # meta
    if len(p["meta_title"]) > 60:
        errs.append(f"meta_title > 60 ({len(p['meta_title'])})")
    if len(p["meta_description"]) > 160:
        errs.append(f"meta_description > 160 ({len(p['meta_description'])})")

    # intro <= 50 mots
    iw = len(text(intro).split())
    if iw > 50:
        errs.append(f"intro > 50 mots ({iw})")

    # mots total
    total = len(text(body).split())
    print(f"total mots body (avec titres) : {total}")

    # paragraphes < 60 mots
    paras = re.findall(r"<p>(.*?)</p>", body, re.S)
    long_paras = [len(text(x).split()) for x in paras if len(text(x).split()) >= 60]
    if long_paras:
        errs.append(f"{len(long_paras)} paragraphe(s) >= 60 mots : {long_paras}")
    else:
        print(f"OK : {len(paras)} paragraphes, tous < 60 mots (max={max((len(text(x).split()) for x in paras), default=0)})")

    # structure H2/H3
    h2s = re.findall(r"<h2>(.*?)</h2>", body, re.S)
    h3s = re.findall(r"<h3>(.*?)</h3>", body, re.S)
    print(f"H2: {len(h2s)} | H3: {len(h3s)}")
    # H4 interdit
    if re.search(r"<h4", body):
        errs.append("H4 trouvé (interdit)")
    # chaque H2 suivi d'au moins 2 H3 : on vérifie en découpant
    parts = re.split(r"<h2>", body)[1:]
    for part in parts:
        title = re.match(r"(.*?)</h2>", part).group(1)
        n3 = len(re.findall(r"<h3>", part))
        if n3 < 2:
            errs.append(f"H2 « {title[:40]} » a {n3} H3 (< 2)")
    # max 2 <p> par section H3
    sections = re.split(r"<h3>", body)[1:]
    for s in sections:
        np_ = len(re.findall(r"<p>", s))
        if np_ > 2:
            errs.append(f"section H3 avec {np_} paragraphes (>2)")

    # 1 <strong> par paragraphe
    bad_bold = [len(re.findall(r"<strong>", x)) for x in paras if len(re.findall(r"<strong>", x)) != 1]
    if bad_bold:
        errs.append(f"{len(bad_bold)} paragraphe(s) sans exactement 1 <strong> : {bad_bold}")

    # mentions ANJ
    btxt = text(body).lower()
    for kw in ["18 ans", "joueurs info service", "09 74 75 13 13", "dépendance"]:
        if kw not in btxt:
            errs.append(f"mention manquante : {kw}")

    # pas de lien Betsson (href vide / #)
    if 'href="#"' in body or 'href=""' in body:
        errs.append("lien vide (#) présent")
    cta_links = re.findall(r'cta-btn[^>]*>', body)
    print("CTA Betsson (balise) :", cta_links)

    # maillage sortant (hors nav/footer)
    out_links = set(re.findall(r'href="(/[a-z0-9-]+/)"', body))
    print("liens sortants internes (body) :", sorted(out_links))

    # maillage entrant : liens vers parier-worlds-lol dans les autres pages
    entrants = []
    import glob
    for f in glob.glob("/Users/charlesploteau/esport-lol/content/*.json"):
        d = load(f)
        if d.get("slug") == "parier-worlds-lol":
            continue
        blob = json.dumps(d)
        if "/parier-worlds-lol/" in blob:
            entrants.append(d["slug"])
    print("liens entrants vers la page pari :", entrants)

    print("\n=== RÉSULTAT ===")
    if errs:
        print("ERREURS :")
        for e in errs:
            print("  ✗", e)
        sys.exit(1)
    print("✓ Aucune erreur. Page conforme.")

if __name__ == "__main__":
    main()
