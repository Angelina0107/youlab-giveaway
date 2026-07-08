#!/usr/bin/env python3
"""Групповая раскладка 10 шокобоксов: два ряда с наложением, мягкие тени, прозрачный фон.
Порядок отрисовки подобран так, чтобы наложения не резали тексты соседей."""
import os
from PIL import Image, ImageDraw, ImageFilter

SCR = os.path.dirname(os.path.abspath(__file__))
FRONTS = os.path.join(SCR, "fronts")
OUT = os.path.join(SCR, "boxes_composite.png")

CANVAS_W, CANVAS_H = 3800, 1600

# (номер бокса, x центра, y верха, целевая высота, поворот)
# позиции слева направо: задний ряд [3, 10, 4, 1, 6], передний [5, 9, 2, 7, 8]
BACK_SPECS = {
    3:  (395, 60, 700, -2.5),
    10: (1115, 70, 690, 2.0),
    4:  (1852, 50, 705, -1.5),
    1:  (2590, 60, 700, 2.2),
    6:  (3330, 72, 685, -2.0),
}
FRONT_SPECS = {
    5: (425, 645, 775, 2.0),
    8: (1118, 640, 780, 2.2),
    2: (1905, 640, 780, 1.2),
    7: (2595, 655, 770, -1.8),
    9: (3300, 665, 740, -1.6),
}
# порядок отрисовки: кто позже — тот сверху; бережём тексты
BACK_ORDER = [4, 10, 3, 1, 6]
FRONT_ORDER = [5, 2, 8, 9, 7]

def rounded_mask(size, radius):
    m = Image.new("L", size, 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle([0, 0, size[0]-1, size[1]-1], radius=radius, fill=255)
    return m

def place(canvas, n, cx, top, h, angle):
    im = Image.open(os.path.join(FRONTS, f"box{n}.png")).convert("RGBA")
    w = int(im.width * h / im.height)
    im = im.resize((w, h), Image.LANCZOS)
    im.putalpha(rounded_mask(im.size, 12))
    rot = im.rotate(angle, expand=True, resample=Image.BICUBIC)
    a = rot.split()[3]
    shadow = Image.new("RGBA", rot.size, (0, 0, 0, 0))
    black = Image.new("RGBA", rot.size, (30, 25, 18, 78))
    shadow.paste(black, (0, 0), a)
    shadow = shadow.filter(ImageFilter.GaussianBlur(30))
    x = int(cx - rot.width / 2)
    y = int(top)
    canvas.alpha_composite(shadow, (x + 6, y + 34))
    canvas.alpha_composite(rot, (x, y))

canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
for n in BACK_ORDER:
    place(canvas, n, *BACK_SPECS[n])
for n in FRONT_ORDER:
    place(canvas, n, *FRONT_SPECS[n])

bbox = canvas.getbbox()
canvas = canvas.crop(bbox)
canvas.save(OUT)

preview = canvas.copy()
preview.thumbnail((1800, 1200))
bg = Image.new("RGB", preview.size, (246, 241, 232))
bg.paste(preview, (0, 0), preview)
bg.save(os.path.join(SCR, "boxes_preview.jpg"), quality=88)
print(OUT, canvas.size)
