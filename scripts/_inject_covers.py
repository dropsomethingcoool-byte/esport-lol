#!/usr/bin/env python3
"""Injecte l'image de couverture en tête du body des articles (alt SEO),
et ajoute un champ `cover` (URL relative) pour l'og:image spécifique."""
import json
import os

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
CONTENT = os.path.join(ROOT, "content")

COVERS = {
    "builds-lol": "Guide des builds League of Legends",
    "compteurs-lol": "Guide des counters League of Legends",
    "lexique-lol": "Lexique des termes League of Legends",
    "guide-champions-lol": "Guide des champions League of Legends",
    "tirage-au-sort-worlds-2026": "Tirage au sort du système suisse Worlds 2026",
    "galions-emea-masters-2026": "Galions remporte l'EMEA Masters 2026 Summer",
    "meilleurs-champions-worlds": "Meilleurs champions des Worlds 2026",
}


def cover_html(slug, alt):
    return (
        f'<img class="article-cover" src="/assets/img/covers/{slug}.png" '
        f'alt="{alt}" loading="lazy" width="1200" height="630">'
    )


for slug, alt in COVERS.items():
    p = os.path.join(CONTENT, f"{slug}.json")
    if not os.path.exists(p):
        print(f"  ✗ {slug}.json introuvable")
        continue
    d = json.load(open(p, encoding="utf-8"))
    body = d["body"]
    if 'class="article-cover"' not in body:
        # insérer en tête du body (avant le CTA)
        body = cover_html(slug, alt) + "\n" + body
        d["body"] = body
    # champ cover pour og:image
    d["cover"] = f"/assets/img/covers/{slug}.png"
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"  ✓ {slug}: cover + og:image")
