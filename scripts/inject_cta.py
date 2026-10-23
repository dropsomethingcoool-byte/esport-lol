#!/usr/bin/env python3
"""Injecte un CTA BetNinja dans les récaps (blog) et les pages équipes."""
import json
import os

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
CONTENT = os.path.join(ROOT, "content")

RECAP_CTA = (
    '<div class="cta-affiliate"><div class="cta-box">\n'
    '<span class="cta-bonus">Bonus de dépôt 75 % jusqu\'à 500 €</span>\n'
    '<div class="cta-box-title">Parier sur les Worlds LoL</div>\n'
    '<p>Suivez les cotes des prochains matchs des Worlds 2026 et placez vos paris esport sur BetNinja.</p>\n'
    '<a class="cta-btn" href="/go/lol" rel="nofollow sponsored noopener">Parier sur les Worlds <span class="cta-arrow">→</span></a>\n'
    '<p class="cta-disclosure">18+ · Jouer comporte des risques · Lien partenaire.</p>\n'
    '</div></div>'
)


def team_cta(team):
    return (
        '<div class="cta-affiliate"><div class="cta-box">\n'
        '<div class="cta-box-title">Parier sur les matchs de ' + team + '</div>\n'
        '<p>Retrouvez les cotes des matchs de ' + team + ' sur BetNinja et profitez du bonus de dépôt de 75 % jusqu\'à 500 €.</p>\n'
        '<a class="cta-btn" href="/go/lol" rel="nofollow sponsored noopener">Parier sur ' + team + ' <span class="cta-arrow">→</span></a>\n'
        '<p class="cta-disclosure">18+ · Jouer comporte des risques · Lien partenaire.</p>\n'
        '</div></div>'
    )


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def save(p, d):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


recap_slugs = []
team_slugs = []
for fn in sorted(os.listdir(CONTENT)):
    if not fn.endswith(".json"):
        continue
    p = os.path.join(CONTENT, fn)
    d = load(p)
    slug = d.get("slug", "")
    if slug.endswith("-resume") or slug in ("karmine-corp-remporte-play-in", "tirage-au-sort-worlds-2026"):
        recap_slugs.append(fn)
    elif slug.startswith("equipe-"):
        team_slugs.append(fn)

# 1. Récaps
n_recap = 0
for fn in recap_slugs:
    p = os.path.join(CONTENT, fn)
    d = load(p)
    body = d.get("body", "")
    if 'href="/go/lol"' in body:
        continue
    body = body.rstrip() + "\n\n" + RECAP_CTA
    d["body"] = body
    d["date_modified"] = "2026-10-19"
    save(p, d)
    n_recap += 1

# 2. Équipes
n_team = 0
for fn in team_slugs:
    p = os.path.join(CONTENT, fn)
    d = load(p)
    body = d.get("body", "")
    if 'href="/go/lol"' in body:
        continue
    h1 = d.get("h1", "") or d.get("title", "")
    team = h1.replace(" aux Worlds LoL 2026", "").strip()
    if not team or team == h1:
        team = d.get("title", "").replace(" aux Worlds LoL 2026", "").strip() or "cette équipe"
    body = body.rstrip() + "\n\n" + team_cta(team)
    d["body"] = body
    d["date_modified"] = "2026-10-19"
    save(p, d)
    n_team += 1

print(f"récaps modifiés : {n_recap}  ({', '.join(recap_slugs)})")
print(f"équipes modifiées : {n_team}")
