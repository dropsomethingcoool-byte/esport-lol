#!/usr/bin/env python3
"""Retire l'entrée publiée (première du backlog) de data/backlog.json."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(ROOT, "data", "backlog.json")
d = json.load(open(path, encoding="utf-8"))
removed = d["pages"].pop(0)
json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("retiré:", removed["slug"], "| restant:", len(d["pages"]))
print([p["slug"] for p in d["pages"]])
