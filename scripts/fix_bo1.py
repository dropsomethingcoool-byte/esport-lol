#!/usr/bin/env python3
"""Précise le format Bo1 du Round 1 suisse dans l'article et le planning."""
import json
import os

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
CONTENT = os.path.join(ROOT, "content")

def load(p):
    with open(os.path.join(CONTENT, p), encoding="utf-8") as f:
        return json.load(f)

def save(p, d):
    with open(os.path.join(CONTENT, p), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

# 1. Article : préciser Bo1 sur le Round 1 + clarifier le format
art = load("tirage-au-sort-worlds-2026.json")
b = art["body"]
b = b.replace(
    "<h3>Les huit affiches du Round 1</h3>",
    "<h3>Les huit affiches du Round 1, en Bo1</h3>",
)
b = b.replace(
    "Au système suisse, chaque équipe enchaîne jusqu'à cinq rondes. Trois victoires qualifient pour les quarts de finale, trois défaites éliminent. Les matchs de qualification et d'élimination se jouent en <strong>Bo3</strong>, les autres en <strong>Bo1</strong>.",
    "Au système suisse, chaque équipe enchaîne jusqu'à cinq rondes. Trois victoires qualifient pour les quarts de finale, trois défaites éliminent. Le <strong>Round 1 se joue en Bo1</strong>, une seule manche. Les matchs de qualification et d'élimination, à partir du Round 3, se jouent en <strong>Bo3</strong>, les autres restent en <strong>Bo1</strong>.",
)
art["body"] = b
save("tirage-au-sort-worlds-2026.json", art)
print("✓ article : Round 1 en Bo1 précisé")

# 2. Planning : préciser Bo1
pl = load("planning.json")
pb = pl["body"]
pb = pb.replace(
    "Les affiches du Round 1 :",
    "Les affiches du Round 1 (toutes en <strong>Bo1</strong>) :",
)
pl["body"] = pb
save("planning.json", pl)
print("✓ planning : Round 1 en Bo1 précisé")
