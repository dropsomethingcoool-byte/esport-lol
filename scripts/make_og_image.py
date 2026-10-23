#!/usr/bin/env python3
"""Génère l'image OG (1200x630) pour esport-lol.com — design éditorial sombre."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = (11, 11, 13)          # #0b0b0d
GOLD = (200, 169, 106)     # #c8a96a
GOLD2 = (224, 197, 143)    # #e0c58f
TEXT = (236, 236, 233)     # #ecece9
FAINT = (154, 154, 148)    # #9a9a94

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def font(name, size):
    return ImageFont.truetype(name, size)

serif = "/System/Library/Fonts/NewYork.ttf"
mono = "/System/Library/Fonts/Supplemental/Arial Narrow.ttf"

# --- Hexagone (logo) centré ---
cx, cy, r = W // 2, 175, 46
import math
pts = []
for i in range(6):
    a = math.pi / 3 * i - math.pi / 6
    pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
# hexagone plein or + facette ombrée
d.polygon(pts, fill=GOLD)
inner = []
for i in range(6):
    a = math.pi / 3 * i - math.pi / 6
    rr = r * 0.52
    inner.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
d.polygon(inner, fill=(0, 0, 0))
# petit diamant doré au centre
d.polygon([(cx, cy - r * 0.26), (cx + r * 0.26, cy), (cx, cy + r * 0.26), (cx - r * 0.26, cy)], fill=GOLD)

# --- Wordmark ---
f_brand = font(serif, 92)
brand = "esport-lol"
bb = d.textbbox((0, 0), brand, font=f_brand)
tw = bb[2] - bb[0]
x = (W - tw) // 2
y = 255
d.text((x, y), brand, font=f_brand, fill=TEXT)
# trait d'union doré
w_esport = d.textbbox((0, 0), "esport", font=f_brand)[2]
hx = x + w_esport - 4
d.text((hx, y), "-", font=f_brand, fill=GOLD)

# --- Règle or + tagline ---
rule_y = 395
d.rectangle([(W // 2 - 40, rule_y), (W // 2 + 40, rule_y + 2)], fill=GOLD)

f_tag = font(mono, 34)
tag = "SUIVI DES WORLDS  ·  LEAGUE OF LEGENDS"
tb = d.textbbox((0, 0), tag, font=f_tag)
tw2 = tb[2] - tb[0]
d.text(((W - tw2) // 2, 430), tag, font=f_tag, fill=FAINT)

# --- URL discrète ---
f_url = font(mono, 26)
url = "esport-lol.com"
ub = d.textbbox((0, 0), url, font=f_url)
d.text(((W - (ub[2] - ub[0])) // 2, 540), url, font=f_url, fill=(98, 98, 93))

img.save("assets/img/og-image.png")
print("OK og-image.png", img.size)
