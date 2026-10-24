#!/usr/bin/env python3
"""Ajoute le toggle de phase (Swiss stage / Play-in) sur classement + resultats."""
import json
import os

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
CONTENT = os.path.join(ROOT, "content")

TOGGLE = ('<div class="stage-toggle">'
          '<button class="stage-btn active" data-stage="swiss" type="button">Swiss stage</button>'
          '<button class="stage-btn" data-stage="play_ins" type="button">Play-in</button></div>')


def edit(fn, anchor):
    p = os.path.join(CONTENT, fn)
    with open(p, encoding="utf-8") as f:
        d = json.load(f)
    body = d["body"]
    if "stage-toggle" in body:
        print(f"· {fn}: déjà présent")
        return
    if anchor not in body:
        print(f"✗ {fn}: ancre introuvable")
        return
    d["body"] = body.replace(anchor, TOGGLE + anchor, 1)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print(f"✓ {fn}: toggle ajouté")


edit("classement.json", '<div id="live-standings" class="standings"></div>')
edit("resultats.json", '<div id="live-results" class="match-list"></div>')
