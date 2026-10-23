#!/usr/bin/env python3
"""Diagnostic : liste les <p> (intro + body) qui n'ont pas exactement 1 <strong>."""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = json.load(open(os.path.join(ROOT, "content", "compteurs-lol.json"), encoding="utf-8"))
blob = p.get("intro", "") + "\n" + p.get("body", "")
paras = re.findall(r"<p[^>]*>(.*?)</p>", blob, re.S)
for i, x in enumerate(paras):
    n = len(re.findall(r"<strong>", x))
    if n != 1:
        print(f"[{i}] strong={n} :: {re.sub(r'<[^>]+>', '', x)[:160]}")
print(f"total paragraphes={len(paras)}")
