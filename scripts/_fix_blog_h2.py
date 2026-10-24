#!/usr/bin/env python3
"""Réparation ciblée de content/blog.json : les essais précédents ont laissé
deux H2 dédoublés/collés autour de la section « Guides ». Idempotent."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "content", "blog.json")

with open(PATH, encoding="utf-8") as f:
    blog = json.load(f)

body = blog["body"]
before = body
body = body.replace("<h2><h2>Guides</h2>", "<h2>Guides</h2>")
body = body.replace("<h2>Actualités</h2><h2>Actualités</h2>", "<h2>Actualités</h2>")

if body != before:
    blog["body"] = body
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(blog, f, ensure_ascii=False, indent=2)
    print("✓ content/blog.json réparé")
else:
    print("rien à réparer")

# Contrôle de structure : aucun H2 vide, pas de croisement.
import re
print("H2 vides :", len(re.findall(r"<h2>\s*<", body)))
for h in re.findall(r"<h2>[^<]*</h2>", body):
    print("  ", h)
