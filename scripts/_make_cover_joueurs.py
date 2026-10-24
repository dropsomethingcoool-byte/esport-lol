#!/usr/bin/env python3
"""Génère la cover (webp + jpg) de l'article joueurs-a-suivre-worlds-2026.
Style « éditorial sombre » : fond #0b0b0d, accent or, serif. 1200x630."""
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
COVERS = os.path.join(ROOT, "assets", "img", "covers")

W, H = 1200, 630
BG = (11, 11, 13)
GOLD = (200, 169, 106)
GOLD3 = (155, 125, 69)
TEXT = (236, 236, 233)
FAINT = (98, 98, 93)

SERIF = "/System/Library/Fonts/NewYork.ttf"
MONO = "/System/Library/Fonts/Supplemental/Arial Narrow.ttf"

TITLE = "Joueurs à suivre"
SUBTITLE = "Worlds 2026"


def make(path):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # dégradé radial or (simulé) en haut-droite
    for i, r in enumerate(range(640, 80, -80)):
        a = int(6 * (1 - i / 8))
        if a <= 0:
            break
        d.ellipse([W - r, -r // 2, W + r, r // 2], fill=(200 + a, 169 + a, 106 + a))

    # règle or à gauche
    d.rectangle([80, 150, 84, H - 80], fill=GOLD3)

    f_label = ImageFont.truetype(MONO, 30)
    d.text((120, 110), "LEAGUE OF LEGENDS", font=f_label, fill=FAINT)

    f_title = ImageFont.truetype(SERIF, 82)
    wrapped = textwrap.wrap(TITLE, width=17)
    y = 200
    for line in wrapped:
        d.text((120, y), line, font=f_title, fill=TEXT)
        y += 92

    f_sub = ImageFont.truetype(SERIF, 54)
    d.text((120, y + 8), SUBTITLE, font=f_sub, fill=GOLD)

    f_brand = ImageFont.truetype(SERIF, 34)
    d.text((120, H - 96), "esport-lol.com", font=f_brand, fill=GOLD)

    img.save(path)


os.makedirs(COVERS, exist_ok=True)
webp = os.path.join(COVERS, "joueurs-a-suivre-worlds-2026.webp")
jpg = os.path.join(COVERS, "joueurs-a-suivre-worlds-2026.jpg")

make(webp)
make(jpg)
print("✓ webp:", os.path.getsize(webp), "octets")
print("✓ jpg :", os.path.getsize(jpg), "octets")
