#!/usr/bin/env python3
"""Retire les covers génériques (img.article-cover) des articles + le champ 'cover'.
Les couvertures sombres/or identiques sont jugées inutiles."""
import json
import os
import re

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
CONTENT = os.path.join(ROOT, "content")

PAT = re.compile(r'<img class="article-cover"[^>]*>', re.S)

n = 0
for fn in sorted(os.listdir(CONTENT)):
    if not fn.endswith(".json"):
        continue
    p = os.path.join(CONTENT, fn)
    with open(p, encoding="utf-8") as f:
        b = json.load(f)
    body = b.get("body", "")
    new = PAT.sub("", body)
    changed = new != body
    if "cover" in b:
        del b["cover"]
        changed = True
    if changed:
        b["body"] = new
        with open(p, "w", encoding="utf-8") as f:
            json.dump(b, f, ensure_ascii=False, indent=2)
        n += 1
        print("✓ cover retirée :", fn)

print(f"\n{'' if n else 'Aucune '}cover retirée ({n} fichier(s) modifié(s)).")
