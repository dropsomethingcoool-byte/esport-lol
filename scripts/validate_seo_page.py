#!/usr/bin/env python3
"""Validation SEO d'une page de contenu esport-lol (règles de rédaction de la skill).

Usage : python3 scripts/validate_seo_page.py <slug>
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GAMBLING_PAGES = {"parier-worlds-lol"}


def text(html):
    return re.sub(r"<[^>]+>", " ", html)


def main():
    if len(sys.argv) < 2:
        print("usage: validate_seo_page.py <slug>")
        sys.exit(2)
    slug = sys.argv[1]
    path = os.path.join(ROOT, "content", f"{slug}.json")
    with open(path, encoding="utf-8") as f:
        p = json.load(f)

    body, intro = p["body"], p["intro"]
    errs = []

    # --- meta
    if len(p["meta_title"]) > 60:
        errs.append(f"meta_title > 60 ({len(p['meta_title'])}) : {p['meta_title']}")
    if len(p["meta_description"]) > 160:
        errs.append(f"meta_description > 160 ({len(p['meta_description'])})")

    # --- mot-clé
    # mot-clé : 2e argument > champ _keyword > backlog
    kw = sys.argv[2].lower() if len(sys.argv) > 2 else p.get("_keyword", "").lower()
    if not kw:
        # déduit du backlog si possible
        bl = os.path.join(ROOT, "data", "backlog.json")
        if os.path.exists(bl):
            with open(bl, encoding="utf-8") as f:
                for e in json.load(f).get("pages", []):
                    if e["slug"] == slug:
                        kw = e["keyword"].lower()
    if kw:
        for field in ("title", "meta_title"):
            if kw not in p[field].lower():
                errs.append(f"mot-clé « {kw} » absent de {field}")
        if kw.replace("-", " ") not in text(intro).lower().replace("\n", " "):
            errs.append(f"mot-clé « {kw} » absent de l'intro")
        if kw not in p["h1"].lower():
            print(f"WARN: mot-clé absent du h1 ({p['h1']})")
        # variantes : on tolère
    else:
        print("WARN: mot-clé introuvable (backlog vide ?)")

    # --- intro
    iw = len(text(intro).split())
    if iw > 50:
        errs.append(f"intro > 50 mots ({iw})")

    # --- longueur
    total = len(text(body).split())
    print(f"total mots body (avec titres) : {total}")
    if total < 800:
        errs.append(f"body < 800 mots ({total})")
    if total > 1000:
        print(f"WARN: body > 1000 mots ({total})")

    # --- paragraphes
    paras = re.findall(r"<p>(.*?)</p>", body, re.S)
    long_paras = [len(text(x).split()) for x in paras if len(text(x).split()) >= 60]
    if long_paras:
        errs.append(f"{len(long_paras)} paragraphe(s) >= 60 mots : {long_paras}")
    else:
        print(f"OK : {len(paras)} paragraphes, tous < 60 mots "
              f"(max={max((len(text(x).split()) for x in paras), default=0)})")

    # --- structure
    h2s = re.findall(r"<h2>(.*?)</h2>", body, re.S)
    h3s = re.findall(r"<h3>(.*?)</h3>", body, re.S)
    print(f"H2: {len(h2s)} | H3: {len(h3s)}")
    if re.search(r"<h4", body):
        errs.append("H4 trouvé (interdit)")
    for part in re.split(r"<h2>", body)[1:]:
        title = re.match(r"(.*?)</h2>", part).group(1)
        n3 = len(re.findall(r"<h3>", part))
        if n3 < 2:
            errs.append(f"H2 « {title[:40]} » a {n3} H3 (< 2)")
    for s in re.split(r"<h3>", body)[1:]:
        np_ = len(re.findall(r"<p>", s))
        if np_ > 2:
            errs.append(f"section H3 avec {np_} paragraphes (>2)")

    # --- 1 strong par paragraphe
    bad_bold = [len(re.findall(r"<strong>", x)) for x in paras if len(re.findall(r"<strong>", x)) != 1]
    if bad_bold:
        errs.append(f"{len(bad_bold)} paragraphe(s) sans exactement 1 <strong> : {bad_bold}")

    # --- liens vides
    if 'href="#"' in body or 'href=""' in body:
        errs.append("lien vide (#) présent")

    # --- mentions légales gambling (uniquement pages paris)
    if slug in GAMBLING_PAGES:
        btxt = text(body).lower()
        for kwm in ["18 ans", "joueurs info service", "09 74 75 13 13", "dépendance"]:
            if kwm not in btxt:
                errs.append(f"mention manquante : {kwm}")

    # --- maillage interne : 2-3 liens contextualisés dans le corps
    out_links = re.findall(r'href="(/[a-z0-9-]+/)"', body)
    uniq = sorted(set(out_links))
    print("liens sortants internes (body) :", uniq)
    if len(uniq) < 2:
        errs.append(f"moins de 2 liens internes contextualisés ({len(uniq)})")

    print("\n=== RÉSULTAT ===")
    if errs:
        print("ERREURS :")
        for e in errs:
            print("  ✗", e)
        sys.exit(1)
    print("✓ Aucune erreur. Page conforme.")


if __name__ == "__main__":
    main()
