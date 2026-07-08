#!/usr/bin/env python3
"""Фавиконки YL: v1 — графит + золото (серифом), v2 — розово-оранжевый градиент."""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEORGIA = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
ARIAL = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

def rounded(size, radius):
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size-1, size-1], radius=radius, fill=255)
    return m

def gradient(size, c1, c2):
    im = Image.new("RGB", (size, size))
    d = ImageDraw.Draw(im)
    for y in range(size):
        t = y / (size - 1)
        d.line([(0, y), (size, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(c1, c2)))
    return im

def make(size, bg, text_color, font_path, out):
    if isinstance(bg[0], int):
        im = Image.new("RGB", (size, size), bg)
    else:
        im = gradient(size, *bg)
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(font_path, int(size * 0.52))
    bb = d.textbbox((0, 0), "YL", font=f)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((size - w) / 2 - bb[0], (size - h) / 2 - bb[1]), "YL", font=f, fill=text_color)
    rgba = im.convert("RGBA")
    rgba.putalpha(rounded(size, int(size * 0.22)))
    rgba.save(out)
    return rgba

os.makedirs(os.path.join(ROOT, "img"), exist_ok=True)

# v1: графит + золото, сериф
for s, name in [(64, "favicon-v1.png"), (180, "favicon-v1-180.png")]:
    make(s, (33, 29, 24), (232, 197, 124), GEORGIA, os.path.join(ROOT, "img", name))

# v2: градиент розовый→оранжевый, белые буквы
for s, name in [(64, "favicon-v2.png"), (180, "favicon-v2-180.png")]:
    make(s, ((255, 62, 143), (255, 138, 52)), (255, 255, 255), ARIAL, os.path.join(ROOT, "img", name))

# favicon.ico в корень (запасной вариант для браузеров)
ico = make(48, (33, 29, 24), (232, 197, 124), GEORGIA, os.path.join(ROOT, "img", "_tmp48.png"))
ico.save(os.path.join(ROOT, "favicon.ico"), format="ICO", sizes=[(48, 48), (32, 32), (16, 16)])
os.remove(os.path.join(ROOT, "img", "_tmp48.png"))
print("ok")
