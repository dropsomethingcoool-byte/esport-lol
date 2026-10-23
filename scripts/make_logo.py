#!/usr/bin/env python3
"""Recolore le logo (noir) en or #c8a96a et génère les variantes :
logo.png (header), favicon.svg, favicon-32/16.png, favicon.ico, apple-touch-icon.png.
Source : l'image fournie par l'utilisateur."""
import base64
import os
from PIL import Image

SRC = "/Users/charlesploteau/.hermes/profiles/esport-lol/image_cache/img_c669e8475cab.png"
OUT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir/assets/img"
GOLD = (200, 169, 106)  # #c8a96a

im = Image.open(SRC).convert("RGBA")
W, H = im.size
px = im.load()
# Recoloriage : pixels opaques -> or (conserve l'alpha pour l'antialiasing)
for y in range(H):
    for x in range(W):
        r, g, b, a = px[x, y]
        if a > 0:
            px[x, y] = (GOLD[0], GOLD[1], GOLD[2], a)

os.makedirs(OUT, exist_ok=True)

# Logo header (assez grand, net)
logo = im.copy()
logo.save(os.path.join(OUT, "logo.png"))
print("logo.png", logo.size)

# Favicon PNG 32 / 16
for s in (32, 16):
    im.resize((s, s), Image.LANCZOS).save(os.path.join(OUT, f"favicon-{s}.png"))
    print(f"favicon-{s}.png")

# apple-touch-icon 180x180
im.resize((180, 180), Image.LANCZOS).save(os.path.join(OUT, "apple-touch-icon.png"))
print("apple-touch-icon.png")

# favicon.ico multi-résolution (16/32/48)
im_ico = im.convert("RGBA")
im_ico.save(
    os.path.join(OUT, "favicon.ico"),
    sizes=[(16, 16), (32, 32), (48, 48)],
)
print("favicon.ico")

# favicon.svg : SVG qui embarque le PNG 64px (base64)
svg_im = im.resize((64, 64), Image.LANCZOS)
import io
buf = io.BytesIO()
svg_im.save(buf, format="PNG")
b64 = base64.b64encode(buf.getvalue()).decode()
svg = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" '
    'viewBox="0 0 64 64">'
    f'<image width="64" height="64" href="data:image/png;base64,{b64}"/>'
    "</svg>"
)
with open(os.path.join(OUT, "favicon.svg"), "w") as f:
    f.write(svg)
print("favicon.svg")
