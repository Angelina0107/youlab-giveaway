#!/usr/bin/env python3
"""Вырезка лицевых панелей шокобоксов перспективной трансформацией (без перерисовки)."""
import os, math, json, sys
from PIL import Image, ImageDraw, ImageFont

SRC = os.path.expanduser("~/Claude/Projects/youlab-landing/img")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fronts")
os.makedirs(OUT, exist_ok=True)

# Нормированные углы лицевой панели: TL, TR, BR, BL (доли ширины/высоты)
QUADS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "quads.json")))

def dist(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def warp(n):
    img = Image.open(os.path.join(SRC, f"box{n}.jpg")).convert("RGB")
    W, H = img.size
    tl, tr, br, bl = [(x*W, y*H) for x, y in QUADS[str(n)]]
    w = int((dist(tl, tr) + dist(bl, br)) / 2)
    h = int((dist(tl, bl) + dist(tr, br)) / 2)
    # PIL QUAD: NW, SW, SE, NE
    data = [tl[0], tl[1], bl[0], bl[1], br[0], br[1], tr[0], tr[1]]
    out = img.transform((w, h), Image.QUAD, data, resample=Image.BICUBIC)
    out.save(os.path.join(OUT, f"box{n}.png"))
    return out

def contact_sheet():
    cell_w, cell_h, pad = 460, 420, 16
    sheet = Image.new("RGB", (cell_w*5 + pad*6, cell_h*2 + pad*3), (240, 240, 240))
    d = ImageDraw.Draw(sheet)
    for i in range(1, 11):
        im = warp(i)
        im.thumbnail((cell_w, cell_h - 26))
        col, row = (i-1) % 5, (i-1)//5
        x = pad + col*(cell_w+pad)
        y = pad + row*(cell_h+pad)
        sheet.paste(im, (x + (cell_w - im.width)//2, y + 24))
        d.rectangle([x, y, x+cell_w, y+cell_h], outline=(180, 180, 180))
        d.text((x+6, y+4), f"box{i}", fill=(0, 0, 0))
    p = os.path.join(OUT, "_sheet.jpg")
    sheet.save(p, quality=88)
    print(p)

contact_sheet()
