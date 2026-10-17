#!/usr/bin/env python3
"""Micro-optimisations meta_title/meta_description/intro/h1 (P1/P2) — léger, sans casser la tendance."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

edits = {
    "resultats": {
        "meta_title": "Résultats des Worlds LoL 2026 en direct | esport-lol",
        "meta_description": "Résultats et scores des Worlds LoL 2026 en direct, mis à jour dès la fin de chaque match. Play-ins, système suisse et phase finale.",
        "h1": "Résultats des Worlds LoL 2026 en direct",
        "intro": '<p class="lead">Les <strong>résultats et scores des Worlds 2026</strong> en direct, mis à jour dès la fin de chaque match.</p>',
    },
    "planning": {
        "meta_title": "Planning et calendrier des Worlds LoL 2026 | esport-lol",
    },
    "classement": {
        "meta_title": "Classement des Worlds LoL 2026 en direct | esport-lol",
    },
}

for slug, changes in edits.items():
    p = os.path.join(ROOT, "content", slug + ".json")
    d = json.load(open(p, encoding="utf-8"))
    for k, v in changes.items():
        old = d.get(k, "")
        d[k] = v
        print(f"[{slug}] {k}: '{old}'  ->  '{v}'")
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print()

print("=" * 30, "VERIF", "=" * 30)
for f in ["resultats", "planning", "classement"]:
    d = json.load(open(os.path.join(ROOT, "content", f + ".json"), encoding="utf-8"))
    mt = d["meta_title"]
    md = d["meta_description"]
    flag = "OK" if len(mt) <= 60 else "!!! >60"
    flagd = "OK" if len(md) <= 160 else "!!! >160"
    print(f"{f}: meta_title={len(mt)}ch [{flag}]  meta_desc={len(md)}ch [{flagd}]")
    print(f"   title: {mt}")
