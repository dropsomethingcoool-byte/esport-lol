#!/usr/bin/env python3
"""Ajoute photo + infobox annuaire (player-hero) aux fiches joueurs existantes."""
import json
import os

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
CONTENT = os.path.join(ROOT, "content")

with open(os.path.join(ROOT, "data", "player_photos.json"), encoding="utf-8") as f:
    photos = json.load(f)

def https(url):
    return url.replace("http://", "https://") if url else url

# slug -> clé photo + libellé rôle
MAPPING = {
    "joueur-faker": {"key": "faker", "alt": "Faker, midlaner de T1"},
    "joueur-caliste": {"key": "caliste", "alt": "Caliste, ADC de la Karmine Corp"},
}

for slug, meta in MAPPING.items():
    p = os.path.join(CONTENT, slug + ".json")
    with open(p, encoding="utf-8") as f:
        d = json.load(f)
    photo = https(photos.get(meta["key"], {}).get("photo", ""))
    role = d.get("role", "")
    team = d.get("team_name", "")
    team_slug = d.get("team_slug", "")
    country = d.get("country", "")
    hero = (
        '<div class="player-hero">'
        f'<img class="player-photo" src="{photo}" alt="{meta["alt"]}" loading="lazy">'
        '<div class="player-hero-meta">'
        f'<span class="player-name">{d.get("pseudo", d.get("h1", ""))}</span>'
        '<ul class="player-facts">'
        f"<li><span>Rôle</span>{role}</li>"
        f'<li><span>Équipe</span><a href="/{team_slug}/">{team}</a></li>'
        f"<li><span>Pays</span>{country}</li>"
        "</ul></div></div>"
    )
    body = d["body"]
    if 'class="player-hero"' not in body:
        body = hero + body
    d["body"] = body
    d["photo"] = photo
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print(f"✓ {slug} : photo + infobox ({photo})")
