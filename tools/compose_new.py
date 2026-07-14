#!/usr/bin/env python3
"""Раскладка новых боксов — 5 ровных колонок, два ряда с равными промежутками."""
import os
from PIL import Image

SRC = os.path.expanduser("~/Claude/Projects/youlab-landing/img/new/ordered")
OUT = os.path.expanduser("~/Claude/Projects/youlab-landing/img/boxes.webp")

MARGIN = 560
STEP = 800                      # равный шаг между колонками
COLS = [MARGIN + i*STEP for i in range(5)]   # 560,1360,2160,2960,3760
CW = COLS[-1] + MARGIN          # симметричные поля
CH = 1620

BACK_H, BACK_TOP = 715, 70
FRONT_H, FRONT_TOP = 800, 610

# какой бокс в какой колонке (слева направо)
BACK = [3, 10, 4, 1, 6]         # тюлень, подбешивать, матрёшка, свинья, капибара
FRONT = [7, 8, 5, 9, 2]         # скорая, лев, ничего, брату, мужу

def place(canvas, n, cx, top, h):
    im = Image.open(os.path.join(SRC, f"n{n}.png")).convert("RGBA")
    w = int(im.width * h / im.height)
    im = im.resize((w, h), Image.LANCZOS)
    canvas.alpha_composite(im, (int(cx - w/2), int(top)))

canvas = Image.new("RGBA", (CW, CH), (0,0,0,0))
for col, n in zip(COLS, BACK):   # задний ряд, слева направо (правый сосед сверху)
    place(canvas, n, col, BACK_TOP, BACK_H)
for col, n in zip(COLS, FRONT):  # передний ряд поверх заднего
    place(canvas, n, col, FRONT_TOP, FRONT_H)

canvas = canvas.crop(canvas.getbbox())
big = canvas.copy(); big.thumbnail((2600,2600), Image.LANCZOS)
big.save(OUT, quality=88, method=6)

prev = canvas.copy(); prev.thumbnail((1900,1900))
bg = Image.new("RGB", prev.size, (255,120,160)); bg.paste(prev,(0,0),prev)
bg.save("/private/tmp/claude-501/-Users-angelinasergeeva/e5004884-b407-46cb-b76f-1d9d9b2bb171/scratchpad/new_layout.jpg", quality=88)
print(OUT, canvas.size)
