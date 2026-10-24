#!/usr/bin/env python3
"""Retire l'entrée publiée (slug debuter-lol) de data/backlog.json."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "data", "backlog.json")

with open(PATH, encoding="utf-8") as f:
    backlog = json.load(f)

before = len(backlog.get("pages", []))
backlog["pages"] = [p for p in backlog.get("pages", []) if p.get("slug") != "debuter-lol"]

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(backlog, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(f"{before} -> {len(backlog['pages'])} entrée(s) restante(s) dans le backlog")
