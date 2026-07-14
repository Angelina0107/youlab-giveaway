#!/usr/bin/env python3
"""Раскладка новых боксов (уже с прозрачным фоном, объёмом и тенью) — два ряда с лёгким наложением."""
import os
from PIL import Image

SRC = os.path.expanduser("~/Claude/Projects/youlab-landing/img/new/ordered")
OUT = os.path.expanduser("~/Claude/Projects/youlab-landing/img/boxes.webp")

CW, CH = 3960, 1650
# (номер, x центра, y верха, высота); порядок отрисовки — по списку (позже = сверху)
ROW_BACK = [(3,430,40,715),(10,1160,50,705),(4,1900,30,725),(1,2660,50,715),(6,3470,60,705)]
ROW_FRONT = [(7,500,625,790),(8,1250,625,785),(5,2010,620,780),(9,2760,635,775),(2,3400,615,795)]
BACK_ORDER = [4,1,10,3,6]
FRONT_ORDER = [7,8,5,9,2]

def spec(n, table):
    return next(t for t in table if t[0]==n)

def place(canvas, n, table):
    _,cx,top,h = spec(n, table)
    im = Image.open(os.path.join(SRC, f"n{n}.png")).convert("RGBA")
    w = int(im.width * h / im.height)
    im = im.resize((w,h), Image.LANCZOS)
    canvas.alpha_composite(im, (int(cx-w/2), int(top)))

canvas = Image.new("RGBA",(CW,CH),(0,0,0,0))
for n in BACK_ORDER: place(canvas, n, ROW_BACK)
for n in FRONT_ORDER: place(canvas, n, ROW_FRONT)

canvas = canvas.crop(canvas.getbbox())
big = canvas.copy(); big.thumbnail((2600,2600), Image.LANCZOS)
big.save(OUT, quality=88, method=6)

prev = canvas.copy(); prev.thumbnail((1800,1800))
bg = Image.new("RGB", prev.size, (255,120,160)); bg.paste(prev,(0,0),prev)
bg.save("/private/tmp/claude-501/-Users-angelinasergeeva/e5004884-b407-46cb-b76f-1d9d9b2bb171/scratchpad/new_layout.jpg", quality=88)
print(OUT, canvas.size)
