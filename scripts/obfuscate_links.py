#!/usr/bin/env python3
"""Obfusque les liens affiliés : href statique -> fallback guide, destination
réelle encodée en base64 dans data-go (décodée par JS). Ajoute target=_blank."""
import base64
import json
import os

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
CONTENT = os.path.join(ROOT, "content")
TEMPLATE = os.path.join(ROOT, "templates", "base.html")

GO = "/go/lol"
B64 = base64.b64encode(GO.encode()).decode()
FALLBACK = "/parier-worlds-lol/"

OLD = f'href="{GO}" rel="nofollow sponsored noopener"'
NEW = f'href="{FALLBACK}" data-go="{B64}" rel="nofollow sponsored noopener" target="_blank"'

total = 0

# 1. Contenu (JSON)
for fn in sorted(os.listdir(CONTENT)):
    if not fn.endswith(".json"):
        continue
    p = os.path.join(CONTENT, fn)
    with open(p, encoding="utf-8") as f:
        d = json.load(f)
    body = d.get("body", "")
    n = body.count(OLD)
    if n:
        body = body.replace(OLD, NEW)
        d["body"] = body
        with open(p, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        total += n

# 2. Template base.html (bandeau sticky)
with open(TEMPLATE, encoding="utf-8") as f:
    html = f.read()
n = html.count(OLD)
if n:
    html = html.replace(OLD, NEW)
    with open(TEMPLATE, "w", encoding="utf-8") as f:
        f.write(html)
    total += n

print(f"liens obfusqués : {total} (data-go={B64}, fallback={FALLBACK}, target=_blank)")
