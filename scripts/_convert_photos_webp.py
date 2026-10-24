#!/usr/bin/env python3
"""Télécharge + convertit les portraits joueurs en webp <50 Ko (local).
Écrit data/player_photos_local.json (clé -> {local, size})."""
import json
import os
import urllib.request

from PIL import Image

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
IMG = os.path.join(ROOT, "assets", "img", "players")
os.makedirs(IMG, exist_ok=True)

MAX = 240  # px, aucun upscale


def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; esport-lol)"})
    with urllib.request.urlopen(req, timeout=30) as r, open(dest, "wb") as f:
        f.write(r.read())


def to_webp(src, dst, max_dim=MAX):
    img = Image.open(src).convert("RGB")
    if max(img.size) > max_dim:
        img.thumbnail((max_dim, max_dim), Image.LANCZOS)
    for q in (82, 75, 68, 60):
        img.save(dst, "WEBP", quality=q, method=6)
        if os.path.getsize(dst) < 50_000:
            return True
    img.thumbnail((160, 160), Image.LANCZOS)
    img.save(dst, "WEBP", quality=60, method=6)
    return True


with open(os.path.join(ROOT, "data", "player_photos.json"), encoding="utf-8") as f:
    photos = json.load(f)

local = {}
for key, info in photos.items():
    url = (info.get("photo") or "").replace("http://", "https://")
    if not url or "default-headshot" in url:
        print(f"· {key}: pas de portrait réel, ignoré")
        continue
    tmp = os.path.join(IMG, key + ".png")
    webp = os.path.join(IMG, key + ".webp")
    try:
        download(url, tmp)
        to_webp(tmp, webp)
        sz = os.path.getsize(webp)
        local[key] = {"local": f"/assets/img/players/{key}.webp", "size": sz}
        print(f"✓ {key:14s} {sz:6d} o  /assets/img/players/{key}.webp")
        os.remove(tmp)
    except Exception as e:
        print(f"✗ {key}: {e}")

with open(os.path.join(ROOT, "data", "player_photos_local.json"), "w", encoding="utf-8") as f:
    json.dump(local, f, ensure_ascii=False, indent=2)
print(f"\n✓ {len(local)} portraits -> data/player_photos_local.json")
