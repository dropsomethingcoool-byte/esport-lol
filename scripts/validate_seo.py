#!/usr/bin/env python3
"""Validation SEO d'une page de content/ : règles de rédaction + maillage.

Usage : python3 scripts/validate_seo.py [slug ...]   (défaut : toutes les pages)
Les mentions légales de jeu d'argent (18 ans, Joueurs Info Service) ne sont
exigées que pour les pages du silo « paris » (type paris/parier-* ou cta affilié).
"""
import json, re, sys, glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")

MIN_WORDS = 800
MIN_WORDS_MONEY = 2000
MONEY_MARKERS = ("cta-box", "go/lol", "betninja")


def text(html):
    return re.sub(r"<[^>]+>", " ", html)


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def is_money_page(p):
    blob = json.dumps(p).lower()
    return any(m in blob for m in MONEY_MARKERS)


def validate(p, all_pages):
    slug = p["slug"]
    body = p.get("body", "")
    intro = p.get("intro", "")
    errs = []

    # meta
    if len(p.get("meta_title", "")) > 60:
        errs.append(f"meta_title > 60 ({len(p['meta_title'])})")
    if len(p.get("meta_description", "")) > 160:
        errs.append(f"meta_description > 160 ({len(p['meta_description'])})")
    kw = p.get("_keyword")
    if kw:
        for field in ("meta_title", "title"):
            if kw.lower() not in text(p.get(field, "")).lower():
                errs.append(f"mot-clé « {kw} » absent de {field}")

    # intro <= 50 mots + mot-clé dans l'intro
    iw = len(text(intro).split())
    if iw > 50:
        errs.append(f"intro > 50 mots ({iw})")
    if kw and kw.lower() not in text(intro).lower():
        errs.append(f"mot-clé « {kw} » absent de l'intro")

    # longueur
    total = len(text(body).split())
    floor = MIN_WORDS_MONEY if is_money_page(p) else MIN_WORDS
    if total < floor:
        errs.append(f"body trop court : {total} mots (< {floor})")
    if not is_money_page(p) and total > 1400:
        errs.append(f"body trop long pour une page standard : {total} mots (> 1400)")

    # paragraphes < 60 mots
    paras = re.findall(r"<p>(.*?)</p>", body, re.S)
    long_paras = [len(text(x).split()) for x in paras if len(text(x).split()) >= 60]
    if long_paras:
        errs.append(f"{len(long_paras)} paragraphe(s) >= 60 mots : {long_paras}")

    # H4 interdit + chaque H2 suivi d'au moins 2 H3
    if re.search(r"<h4", body):
        errs.append("H4 trouvé (interdit)")
    for part in re.split(r"<h2>", body)[1:]:
        title = re.match(r"(.*?)</h2>", part).group(1)
        n3 = len(re.findall(r"<h3>", part))
        if n3 < 2:
            errs.append(f"H2 « {title[:40]} » a {n3} H3 (< 2)")

    # max 2 <p> par section H3
    for s in re.split(r"<h3>", body)[1:]:
        np_ = len(re.findall(r"<p>", s))
        if np_ > 2:
            errs.append(f"section H3 avec {np_} paragraphes (>2)")

    # 1 <strong> exactement par paragraphe
    bad_bold = [len(re.findall(r"<strong>", x)) for x in paras if len(re.findall(r"<strong>", x)) != 1]
    if bad_bold:
        errs.append(f"{len(bad_bold)} paragraphe(s) sans exactement 1 <strong> : {bad_bold}")

    # liens vides
    if 'href="#"' in body or 'href=""' in body:
        errs.append("lien vide (#) présent")

    # maillage sortant : au moins 2 liens internes contextuels (cible : 2-3)
    out_links = set(re.findall(r'href="(/[a-z0-9-]+/)"', body))
    if len(out_links) < 2:
        errs.append(f"seulement {len(out_links)} lien(s) interne(s) dans le body (< 2)")
    for l in out_links:
        s = l.strip("/")
        if not any(q.get("slug") == s for q in all_pages):
            errs.append(f"lien interne cassé : {l}")

    # mentions légales gambling uniquement sur les pages paris
    if is_money_page(p):
        btxt = text(body).lower()
        for k in ["18 ans", "joueurs info service", "09 74 75 13 13", "dépendance"]:
            if k not in btxt:
                errs.append(f"mention manquante : {k}")

    return errs, total, sorted(out_links), len(paras)


def main():
    slugs = sys.argv[1:] or None
    pages = []
    for f in sorted(glob.glob(os.path.join(CONTENT, "*.json"))):
        try:
            pages.append(load(f))
        except Exception as e:
            print(f"✗ JSON invalide : {f} — {e}")
            sys.exit(1)
    by_slug = {p["slug"]: p for p in pages}
    targets = [by_slug[s] for s in slugs if s in by_slug] if slugs else pages
    if slugs:
        missing = [s for s in slugs if s not in by_slug]
        if missing:
            print(f"✗ page(s) introuvable(s) : {missing}")
            sys.exit(1)

    failed = 0
    for p in targets:
        errs, total, links, npar = validate(p, pages)
        print(f"\n— {p['slug']} : {total} mots body, {npar} paragraphes, liens {links}")
        if errs:
            failed += 1
            for e in errs:
                print("  ✗", e)
        else:
            print("  ✓ conforme")

    print("\n=== RÉSULTAT ===")
    if failed:
        print(f"ERREURS sur {failed} page(s).")
        sys.exit(1)
    print(f"✓ {len(targets)} page(s) conforme(s).")


if __name__ == "__main__":
    main()
