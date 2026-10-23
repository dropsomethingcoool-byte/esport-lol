#!/usr/bin/env python3
"""Inspecte les paragraphes sans <strong> et l'intro."""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(ROOT, "content", "guide-champions-lol.json"), encoding="utf-8") as f:
    p = json.load(f)

for i, x in enumerate(re.findall(r"<p>(.*?)</p>", p["body"], re.S)):
    if "<strong>" not in x:
        print(i, "|", re.sub(r"<[^>]+>", "", x).strip()[:160])

print("\nINTRO:", re.sub(r"<[^>]+>", "", p["intro"]).strip())
print("len meta_title:", len(p["meta_title"]), "|", p["meta_title"])
print("len meta_desc:", len(p["meta_description"]))
