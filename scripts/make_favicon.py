#!/usr/bin/env python3
"""Génère les favicons esport-lol (losange doré) à partir de rien (Pillow)."""
from PIL import Image, ImageDraw
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "img")

GOLD = (200, 170, 110, 255)
GOLD_LIGHT = (233, 214, 163, 255)
GOLD_DARK = (168, 135, 63, 255)
BG = (10, 14, 25, 255)


def make_logo(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    radius = max(1, int(size * 0.22))
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=BG)

    # Losange (diamant) — coordonnées normalisées
    top = (0.5 * size, 0.14 * size)
    right = (0.86 * size, 0.375 * size)
    bottom = (0.5 * size, 0.86 * size)
    left = (0.14 * size, 0.375 * size)
    mid_l = (0.34 * size, 0.375 * size)
    mid_r = (0.66 * size, 0.375 * size)
    mid_c = (0.5 * size, 0.46 * size)

    d.polygon([top, right, bottom, left], fill=GOLD)
    d.polygon([top, mid_l, bottom, mid_r], fill=GOLD_DARK)
    d.polygon([top, right, mid_c, left], fill=GOLD_LIGHT)
    return img


def main():
    os.makedirs(OUT, exist_ok=True)

    for name, size in [("favicon-16.png", 16), ("favicon-32.png", 32),
                       ("apple-touch-icon.png", 180)]:
        make_logo(size).save(os.path.join(OUT, name))
        print(f"  ✓ {name} ({size}x{size})")

    # ICO multi-résolutions
    ico = make_logo(48)
    ico.save(os.path.join(OUT, "favicon.ico"), format="ICO",
             sizes=[(16, 16), (32, 32), (48, 48)])
    print("  ✓ favicon.ico (16/32/48)")


if __name__ == "__main__":
    main()
