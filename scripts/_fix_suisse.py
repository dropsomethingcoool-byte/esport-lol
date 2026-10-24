#!/usr/bin/env python3
"""Remplace les traductions FR « suisse » restantes par « swiss stage »
(content/*.json + scripts sources), sans toucher au « Swiss » déjà correct."""
import json
import os
import re

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
CONTENT = os.path.join(ROOT, "content")

# ordre important : les expressions les plus spécifiques d'abord
REPL = [
    ("de la phase suisse", "du swiss stage"),
    ("la phase suisse", "le swiss stage"),
    ("Matchs du suisse", "Matchs du swiss stage"),
    ("le format suisse", "le swiss stage"),
    ("système suisse", "swiss stage"),
    ("phase suisse", "swiss stage"),
    ("format suisse", "swiss stage"),
]

FIELDS = ["body", "intro", "title", "meta_title", "meta_description", "h1"]

n = 0
for fn in sorted(os.listdir(CONTENT)):
    if not fn.endswith(".json"):
        continue
    p = os.path.join(CONTENT, fn)
    with open(p, encoding="utf-8") as f:
        d = json.load(f)
    changed = False
    for field in FIELDS:
        t = d.get(field)
        if not isinstance(t, str):
            continue
        orig = t
        for old, new in REPL:
            t = t.replace(old, new)
        if t != orig:
            d[field] = t
            changed = True
    if changed:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        n += 1
        print(f"✓ {fn}")

# scripts sources (évite la réintroduction)
for sfn in ["build_teams.py", "update_swiss_draw.py", "fix_bo1.py", "_write_galions_article.py"]:
    sp = os.path.join(ROOT, "scripts", sfn)
    if not os.path.exists(sp):
        continue
    with open(sp, encoding="utf-8") as f:
        txt = f.read()
    orig = txt
    for old, new in REPL:
        txt = txt.replace(old, new)
    if txt != orig:
        with open(sp, "w", encoding="utf-8") as f:
            f.write(txt)
        print(f"✓ scripts/{sfn}")

print(f"\n{'' if n else 'Aucune '}occurrence « suisse » remplacée ({n} fichier(s) content).")
