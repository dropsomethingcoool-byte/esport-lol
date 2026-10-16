#!/usr/bin/env python3
"""Publie un article « résumé de match » sur le blog esport-lol.

Mécanique pure (pas d'écriture éditoriale) : l'article (titre, chapeau, corps,
liens) est fourni par l'agent via un fichier spec JSON, ce script se charge de :
  1. créer content/<slug>.json  (type article, silo blog, + champ match_id)
  2. mettre à jour la liste « Résumés de matchs » de content/blog.json
     (reconstruite depuis tous les articles ayant un champ match_id)
  3. régénérer le site (generate.py) et le déployer (deploy.py)

Usage :
  python3 scripts/publish_recap.py /chemin/vers/spec.json [--no-deploy]

Le spec.json doit contenir :
{
  "match_id": "115660588583171786",
  "slug": "kc-vs-cloud9-resume",
  "title": "KC vs Cloud9 : résumé du match",
  "meta_title": "KC vs Cloud9 : résumé du match | esport-lol",
  "meta_description": "Résumé du match KC vs Cloud9 aux Worlds 2026 : score, déroulé et suite de la compétition.",
  "h1": "KC vs Cloud9 : résumé du match",
  "intro": "<p class=\"lead\">...</p>",
  "body": "<h2>...</h2><p>...</p>...",
  "related": [{"slug": "planning", "anchor": "planning des Worlds"}],
  "date": "2026-10-16"          (optionnel, défaut = aujourd'hui)
}
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
BLOG = os.path.join(CONTENT, "blog.json")
START = "<!-- RECAPS_START -->"
END = "<!-- RECAPS_END -->"

REQUIRED = ["match_id", "slug", "title", "meta_title", "meta_description", "h1", "intro", "body"]


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def slug_exists(slug):
    return os.path.exists(os.path.join(CONTENT, f"{slug}.json"))


def unique_slug(slug):
    if not slug_exists(slug):
        return slug
    i = 2
    while slug_exists(f"{slug}-{i}"):
        i += 1
    return f"{slug}-{i}"


def today():
    return datetime.now().strftime("%Y-%m-%d")


def build_content_json(spec):
    slug = unique_slug(spec["slug"])
    date = spec.get("date") or today()
    return {
        "slug": slug,
        "type": "article",
        "silo": "blog",
        "match_id": spec["match_id"],
        "title": spec["title"],
        "meta_title": spec["meta_title"],
        "meta_description": spec["meta_description"],
        "h1": spec["h1"],
        "intro": spec["intro"],
        "body": spec["body"],
        "related": spec.get("related", []),
        "date_modified": date,
        "date_published": date,
    }, slug


def collect_recaps():
    """Retourne les articles « résumé de match » (match_id présent), du plus récent au plus ancien."""
    recaps = []
    for fn in sorted(os.listdir(CONTENT)):
        if not fn.endswith(".json"):
            continue
        try:
            d = load_json(os.path.join(CONTENT, fn))
        except Exception:
            continue
        if isinstance(d, dict) and d.get("match_id"):
            recaps.append(d)
    recaps.sort(key=lambda d: (d.get("date_published") or ""), reverse=True)
    return recaps


def recap_list_html(recaps):
    if not recaps:
        return "<p class=\"muted\">Aucun résumé de match pour le moment.</p>"
    items = []
    for r in recaps:
        date = r.get("date_published") or ""
        items.append(
            f'<p class="recap-item"><a href="/{r["slug"]}/">{r["h1"]}</a>'
            f'<span class="recap-date">· {date}</span></p>'
        )
    return "\n".join(items)


def update_blog(recaps):
    blog = load_json(BLOG)
    body = blog.get("body", "")
    html = recap_list_html(recaps)
    if START in body and END in body:
        pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
        body = pattern.sub(START + "\n" + html + "\n" + END, body)
    else:
        body = f'{body}\n<h2>Résumés de matchs</h2>\n{START}\n{html}\n{END}\n'
    blog["body"] = body
    blog["date_modified"] = today()
    with open(BLOG, "w", encoding="utf-8") as f:
        json.dump(blog, f, ensure_ascii=False, indent=2)


def run(cmd):
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def main():
    if len(sys.argv) < 2:
        print("usage: publish_recap.py <spec.json> [--no-deploy]", file=sys.stderr)
        return 1
    spec_path = sys.argv[1]
    no_deploy = "--no-deploy" in sys.argv

    with open(spec_path, "r", encoding="utf-8") as f:
        spec = json.load(f)

    missing = [k for k in REQUIRED if not spec.get(k)]
    if missing:
        print(f"ERREUR : champs manquants dans le spec : {missing}", file=sys.stderr)
        return 1

    content_json, slug = build_content_json(spec)
    out = os.path.join(CONTENT, f"{slug}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(content_json, f, ensure_ascii=False, indent=2)
    print(f"✓ article créé : content/{slug}.json")

    update_blog(collect_recaps())
    print("✓ blog.json mis à jour")

    rc, msg = run([sys.executable, os.path.join(ROOT, "scripts", "generate.py")])
    if rc != 0:
        print(f"ERREUR generate.py : {msg}", file=sys.stderr)
        return 1
    print("✓ site régénéré")

    if no_deploy:
        print("(déploiement ignoré — --no-deploy)")
        return 0

    rc, msg = run([sys.executable, os.path.join(ROOT, "scripts", "deploy.py")])
    if rc != 0:
        print(f"ERREUR deploy.py : {msg}", file=sys.stderr)
        return 1
    print("✓ déployé")
    return 0


if __name__ == "__main__":
    sys.exit(main())
