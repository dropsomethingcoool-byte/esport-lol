#!/usr/bin/env python3
"""Retire une entrée publiée de data/backlog.json (par slug)."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(ROOT, "data", "backlog.json")

if len(sys.argv) < 2:
    print("usage: consume_backlog.py <slug>")
    sys.exit(2)

slug = sys.argv[1]
with open(path, encoding="utf-8") as f:
    data = json.load(f)

before = len(data.get("pages", []))
data["pages"] = [e for e in data.get("pages", []) if e.get("slug") != slug]
after = len(data["pages"])

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(f"backlog : {before} -> {after} entrées (retiré: {slug})")
