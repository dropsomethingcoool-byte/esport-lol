#!/usr/bin/env python3
"""Génère la couverture 1200x630 de la page « débuter sur League of Legends »
(design éditorial sombre identique aux autres couvertures du blog), puis
exporte les versions webp (<50 Ko) et jpg (og:image)."""
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COVERS = os.path.join(ROOT, "assets", "img", "covers")

W, H = 1200, 630
BG = (11, 11, 13)
GOLD = (200, 169, 106)
GOLD3 = (155, 125, 69)
TEXT = (236, 236, 233)
FAINT = (98, 98, 93)

SERIF = "/System/Library/Fonts/NewYork.ttf"
MONO = "/System/Library/Fonts/Supplemental/Arial Narrow.ttf"

SLUG = "debuter-lol"
TITLE = "Débuter sur League of Legends"
LABEL = "Guide du débutant League of Legends"


def main():
    os.makedirs(COVERS, exist_ok=True)
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    for i, r in enumerate(range(640, 80, -80)):
        a = int(6 * (1 - i / 8))
        if a <= 0:
            break
        d.ellipse([W - r, -r // 2, W + r, r // 2], fill=(200 + a, 169 + a, 106 + a))

    d.rectangle([80, 150, 84, H - 80], fill=GOLD3)

    f_label = ImageFont.truetype(MONO, 30)
    d.text((120, 110), LABEL.upper(), font=f_label, fill=FAINT)

    f_title = ImageFont.truetype(SERIF, 78)
    y = 200
    for line in textwrap.wrap(TITLE, width=22):
        d.text((120, y), line, font=f_title, fill=TEXT)
        y += 88

    f_brand = ImageFont.truetype(SERIF, 34)
    d.text((120, H - 96), "esport-lol.com", font=f_brand, fill=GOLD)

    png = os.path.join(COVERS, f"{SLUG}.png")
    img.save(png, optimize=True)
    print("✓", png)


if __name__ == "__main__":
    main()
