#!/usr/bin/env python3
"""Convertit les références d'images png -> webp + optimise les alt text SEO.
Agit sur content/*.json (logos équipes + covers) et templates/base.html (logo site).
Supprime ensuite les PNG obsolètes (sauf og-image + favicons)."""
import os, glob

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
IMG = os.path.join(ROOT, "assets", "img")

# --- mapping chemin png -> webp ---
path_map = {
    "/assets/img/teams/kc.png": "/assets/img/teams/kc.webp",
    "/assets/img/teams/mvk.png": "/assets/img/teams/mvk.webp",
    "/assets/img/teams/fur.png": "/assets/img/teams/fur.webp",
    "/assets/img/teams/c9.png": "/assets/img/teams/c9.webp",
}
covers_dir = os.path.join(IMG, "covers")
for fn in os.listdir(covers_dir):
    if fn.endswith(".png"):
        path_map[f"/assets/img/covers/{fn}"] = f"/assets/img/covers/{fn[:-4]}.webp"

# --- alt text SEO optimisés (logos équipes des matchup-hero) ---
alt_map = {
    "Logo Karmine Corp": "Logo Karmine Corp — Worlds 2026",
    "Logo MVK Esports": "Logo MVK Esports — Worlds 2026",
    "Logo FURIA": "Logo FURIA — Worlds 2026",
    "Logo Cloud9 Kia": "Logo Cloud9 Kia — Worlds 2026",
}

# 1) content/*.json
n = 0
for fp in glob.glob(os.path.join(ROOT, "content", "*.json")):
    with open(fp, encoding="utf-8") as f:
        txt = f.read()
    orig = txt
    for a, b in path_map.items():
        txt = txt.replace(a, b)
    for a, b in alt_map.items():
        txt = txt.replace(a, b)
    if txt != orig:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(txt)
        n += 1
        print("content:", os.path.basename(fp))

# 2) templates/base.html (logo site)
bp = os.path.join(ROOT, "templates", "base.html")
with open(bp, encoding="utf-8") as f:
    txt = f.read()
txt2 = txt.replace("/assets/img/logo.png", "/assets/img/logo.webp")
txt2 = txt2.replace('alt="esport-lol"', 'alt="esport-lol.com"')
if txt2 != txt:
    with open(bp, "w", encoding="utf-8") as f:
        f.write(txt2)
    print("templates/base.html")

# 3) suppression des PNG obsolètes (source assets/)
removed = []
for sub, pat in [("teams", "*.png"), ("covers", "*.png")]:
    for fp in glob.glob(os.path.join(IMG, sub, pat)):
        os.remove(fp)
        removed.append(os.path.relpath(fp, IMG))
# logo.png (remplacé par logo.webp) — on garde og-image.png + favicons
logo_png = os.path.join(IMG, "logo.png")
if os.path.exists(logo_png):
    os.remove(logo_png)
    removed.append("logo.png")

print("\nSupprimés (PNG obsolètes):")
for r in removed:
    print("  -", r)

print(f"\nOK — {n} fichiers content modifiés.")
