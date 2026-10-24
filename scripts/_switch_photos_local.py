#!/usr/bin/env python3
"""Bascule fiches joueur + backlog vers les portraits webp locaux + alt SEO."""
import json
import os
import re
import shutil

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
CONTENT = os.path.join(ROOT, "content")
IMG = os.path.join(ROOT, "assets", "img", "players")

# 1) normaliser le nom de fichier (espace -> tiret)
for old, new in [("hans sama", "hans-sama")]:
    a, b = os.path.join(IMG, old + ".webp"), os.path.join(IMG, new + ".webp")
    if os.path.exists(a) and not os.path.exists(b):
        shutil.move(a, b)
        print(f"✓ renommé {old}.webp -> {new}.webp")


def local_path(key):
    return f"/assets/img/players/{key.replace(' ', '-')}.webp"


def alt(pseudo, role, team):
    return f"{pseudo}, {role} de {team} — Worlds 2026"


# 2) fiches publiées
PAGE_MAP = {"joueur-faker": "faker", "joueur-caliste": "caliste"}
for slug, key in PAGE_MAP.items():
    p = os.path.join(CONTENT, slug + ".json")
    with open(p, encoding="utf-8") as f:
        d = json.load(f)
    lp = local_path(key)
    a = alt(d.get("pseudo", ""), d.get("role", ""), d.get("team_name", ""))
    d["photo"] = lp
    d["body"] = re.sub(
        r'<img class="player-photo" src="[^"]*" alt="[^"]*"',
        f'<img class="player-photo" src="{lp}" alt="{a}"',
        d["body"],
        count=1,
    )
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print(f"✓ {slug} -> {lp} (alt: {a})")

# 3) backlog
bp = os.path.join(ROOT, "data", "backlog.json")
with open(bp, encoding="utf-8") as f:
    b = json.load(f)
for e in b["pages"]:
    e["photo"] = local_path(e["label"].lower())
with open(bp, "w", encoding="utf-8") as f:
    json.dump(b, f, ensure_ascii=False, indent=2)
print(f"✓ backlog.json : {len(b['pages'])} photos locales")
