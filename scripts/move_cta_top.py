#!/usr/bin/env python3
"""Remonte les CTA BetNinja en tête de contenu (bandeau) sur les pages où
ils sont actuellement en bas (récaps, équipes, planning, résultat, classement, index)."""
import json
import os
import re

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
CONTENT = os.path.join(ROOT, "content")

CTA_RE = re.compile(r'<div class="cta-affiliate"><div class="cta-box">.*?</div></div>', re.DOTALL)


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def save(p, d):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


targets = []
for fn in sorted(os.listdir(CONTENT)):
    if not fn.endswith(".json"):
        continue
    slug = fn[:-5]
    if slug.endswith("-resume") or slug in (
        "karmine-corp-remporte-play-in", "tirage-au-sort-worlds-2026",
    ) or slug.startswith("equipe-") or slug in (
        "planning", "resultats", "classement",
    ):
        targets.append(fn)

moved = 0
for fn in targets:
    p = os.path.join(CONTENT, fn)
    d = load(p)
    body = d.get("body", "")
    m = CTA_RE.search(body)
    if not m:
        continue
    cta = m.group(0)
    # retirer du corps
    body = CTA_RE.sub("", body, count=1).strip()
    # remonter en tête de body
    body = cta + "\n\n" + body
    d["body"] = body
    save(p, d)
    moved += 1

print(f"CTA remontés : {moved}  ({', '.join(targets)})")
