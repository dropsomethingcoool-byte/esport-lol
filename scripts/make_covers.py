#!/usr/bin/env python3
"""Génère une image de couverture éditoriale (1200x630) par article blog,
en Pillow (FAL indisponible). Design cohérent avec le système « éditorial sombre » :
fond #0b0b0d, motif or discret, titre serif or, label esport-lol."""
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
IMG = os.path.join(ROOT, "assets", "img")
COVERS = os.path.join(IMG, "covers")

W, H = 1200, 630
BG = (11, 11, 13)
GOLD = (200, 169, 106)
GOLD2 = (224, 197, 143)
GOLD3 = (155, 125, 69)
TEXT = (236, 236, 233)
FAINT = (98, 98, 93)

SERIF = "/System/Library/Fonts/NewYork.ttf"
MONO = "/System/Library/Fonts/Supplemental/Arial Narrow.ttf"

# slug -> (titre court, alt SEO)
COVERS_MAP = {
    "builds-lol": ("Build League of Legends", "Guide des builds League of Legends"),
    "compteurs-lol": ("Counter League of Legends", "Guide des counters League of Legends"),
    "lexique-lol": ("Lexique League of Legends", "Lexique des termes League of Legends"),
    "guide-champions-lol": ("Guide des champions", "Guide des champions League of Legends"),
    "tirage-au-sort-worlds-2026": ("Tirage au sort Worlds 2026", "Tirage au sort du système suisse Worlds 2026"),
    "galions-emea-masters-2026": ("Galions champion EMEA Masters", "Galions remporte l'EMEA Masters 2026 Summer"),
    "meilleurs-champions-worlds": ("Meilleurs champions des Worlds", "Meilleurs champions des Worlds 2026"),
}


def make_cover(path, title, label):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # fond : léger dégradé radial or en haut-droite (simulé par ellipses concentriques)
    for i, r in enumerate(range(640, 80, -80)):
        a = int(6 * (1 - i / 8))
        if a <= 0:
            break
        d.ellipse([W - r, -r // 2, W + r, r // 2], fill=(200 + a, 169 + a, 106 + a))

    # règle or à gauche
    d.rectangle([80, 150, 84, H - 80], fill=GOLD3)

    f_label = ImageFont.truetype(MONO, 30)
    d.text((120, 110), label.upper(), font=f_label, fill=FAINT)

    # titre (serif, wrappé)
    f_title = ImageFont.truetype(SERIF, 78)
    wrapped = textwrap.wrap(title, width=24)
    y = 200
    for line in wrapped:
        d.text((120, y), line, font=f_title, fill=TEXT)
        y += 88

    # mot-clé esport-lol en bas
    f_brand = ImageFont.truetype(SERIF, 34)
    d.text((120, H - 96), "esport-lol.com", font=f_brand, fill=GOLD)

    img.save(path)
    print(f"  ✓ {os.path.basename(path)}")


def main():
    os.makedirs(COVERS, exist_ok=True)
    for slug, (title, alt) in COVERS_MAP.items():
        make_cover(os.path.join(COVERS, f"{slug}.png"), title, alt)


if __name__ == "__main__":
    main()
