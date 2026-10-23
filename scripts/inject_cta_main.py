#!/usr/bin/env python3
"""Injecte un CTA BetNinja dans planning / resultats / classement / index."""
import json
import os

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
CONTENT = os.path.join(ROOT, "content")

CTA = (
    '<div class="cta-affiliate"><div class="cta-box">\n'
    '<span class="cta-bonus">Bonus de dépôt 75 % jusqu\'à 500 €</span>\n'
    '<div class="cta-box-title">Parier sur les Worlds LoL 2026</div>\n'
    '<p>Retrouvez les cotes de tous les matchs des Worlds et profitez du bonus de bienvenue BetNinja.</p>\n'
    '<a class="cta-btn" href="/go/lol" rel="nofollow sponsored noopener">Parier sur les Worlds <span class="cta-arrow">→</span></a>\n'
    '<p class="cta-disclosure">18+ · Jouer comporte des risques · Lien partenaire.</p>\n'
    '</div></div>\n'
)


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def save(p, d):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


# planning / resultats / classement : insérer le CTA avant les pills.
for slug in ("planning", "resultats", "classement"):
    p = os.path.join(CONTENT, slug + ".json")
    d = load(p)
    body = d["body"]
    if 'href="/go/lol"' in body:
        print(f"{slug} : CTA déjà présent, ignoré")
        continue
    marker = '<p><a class="pill"'
    assert marker in body, f"marker pills introuvable dans {slug}"
    body = body.replace(marker, CTA + marker, 1)
    d["body"] = body
    d["date_modified"] = "2026-10-19"
    save(p, d)
    print(f"{slug} : CTA inséré ✓")

# index (home) : ajouter une section CTA en fin de body.
p = os.path.join(CONTENT, "index.json")
d = load(p)
body = d["body"]
if 'href="/go/lol"' not in body:
    home_cta = ('<section class="home-section reveal">'
                '<div class="cta-affiliate"><div class="cta-box">\n'
                '<span class="cta-bonus">Bonus de dépôt 75 % jusqu\'à 500 €</span>\n'
                '<div class="cta-box-title">Parier sur les Worlds LoL 2026</div>\n'
                '<p>Retrouvez les cotes de tous les matchs des Worlds et profitez du bonus de bienvenue BetNinja.</p>\n'
                '<a class="cta-btn" href="/go/lol" rel="nofollow sponsored noopener">Parier sur les Worlds <span class="cta-arrow">→</span></a>\n'
                '<p class="cta-disclosure">18+ · Jouer comporte des risques · Lien partenaire.</p>\n'
                '</div></div></section>')
    body = body.rstrip() + home_cta
    d["body"] = body
    d["date_modified"] = "2026-10-19"
    save(p, d)
    print("index : CTA ajouté ✓")
else:
    print("index : CTA déjà présent, ignoré")
