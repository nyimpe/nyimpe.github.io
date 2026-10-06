"""Concept 23 — five-panel rhythm game after Pump It Up (Silla's five entertainments)."""
import math
from pix import *

cv = Canvas("ink0", seed=251)
rng = cv.rng

# Stage backdrop with lantern strings ---------------------------------------------------------------
cv.vgrad(0, H, ["purple0", "night1", "red0", "night0"])
for k in range(0, W, 24):
    cv.line(k, 6, k + 24, 12 + (k // 24 % 2) * 3, "gold0")
    cv.sprite([".R.", "RYR", "RRR", ".R."], k + 10, 10 + (k // 24 % 2) * 2, {"R": "red2", "Y": "gold2"})
cv.rect(0, 150, W, 30, "brown0"); cv.rect(0, 150, W, 1, "gold0")
for x in range(0, W, 16):
    cv.rect(x, 151, 1, 29, "brown")

# Daemyeon dancer: golden four-eyed mask, bear hide, red robe, spear and shield
L = Layer(seed=2)
dx, dy = 56, 70
L.disc(dx, dy + 30, 16, "red", ry=26)  # robe
L.disc(dx, dy + 6, 14, "brown0", ry=10)  # bear hide over shoulders
L.disc(dx, dy - 8, 10, "gold", ry=11)  # golden mask
for ex in (-5, 5):
    for ey in (-11, -5):
        L.rect(dx + ex - 1, dy + ey, 3, 2, "ink0")
L.rect(dx - 4, dy + 0, 8, 2, "red0")
L.line(dx + 18, dy - 30, dx + 18, dy + 50, "brown2")  # spear
L.sprite([".W.", "WWW", ".W."], dx + 17, dy - 34, {"W": "iron2"})
L.disc(dx - 18, dy + 18, 9, "teal", ry=11); L.disc(dx - 18, dy + 18, 5, "gold0", ry=7)  # shield
L.paste(cv, outline="ink0")
for k in range(6):  # motion lines
    cv.line(dx - 30 - k * 2, dy - 10 + k * 8, dx - 24 - k * 2, dy - 8 + k * 8, "gold2")

# Sokdok and Sanye silhouettes on the right
cv.sprite(["..HHHH..", ".HHHHHH.", "HHBBBBHH", ".BBBBBB.", "..TTTT..", ".TTTTTT.", "TTTTTTTT", ".T....T."], 246, 98,
          {"H": "ink0", "B": "flame0", "T": "teal"}, outline="ink0")
cv.text(255, 90, "속독", "flame2", 10, anchor="ma")
L = Layer(seed=3)
L.disc(290, 120, 18, "gold0", ry=12); L.disc(278, 106, 10, "gold", ry=9)
for k in range(10):
    L.line(270 + k * 2, 98, 266 + k * 3, 90 + (k % 3), "orange")
L.rect(276, 104, 3, 2, "ink0"); L.rect(282, 104, 3, 2, "ink0")
L.paste(cv, outline="ink0")
cv.text(290, 136, "산예", "gold2", 10, anchor="ma")

# Five lanes in the five cardinal colours ------------------------------------------------------------
LX = 112
lanes = [("↙", "flame"), ("↖", "red2"), ("●", "gold2"), ("↗", "red2"), ("↘", "flame")]
cv.rect(LX - 2, 0, 5 * 20 + 4, H, "ink0")
for k in range(5):
    x = LX + k * 20
    cv.rect(x, 0, 19, H, "night0")
    cv.rect(x + 19, 0, 1, H, "ink1")


def note(k, y, receptor=False):
    x = LX + k * 20 + 2
    col = lanes[k][1]
    shapes = {
        0: ["W.......", "WW......", "WWW.....", "W.WW....", "W..WW...", "WWWWWW..", "WWWWWWW."],
        1: ["WWWWWWW.", "WWWWWW..", "W..WW...", "W.WW....", "WWW.....", "WW......", "W......."],
        2: ["..WWW...", ".WWWWW..", "WWWWWWW.", "WWWWWWW.", "WWWWWWW.", ".WWWWW..", "..WWW..."],
    }
    rows = shapes[k] if k < 3 else [r[::-1] for r in shapes[4 - k]]
    if k > 2:
        rows = [r[:7][::-1] + "." for r in shapes[4 - k]]
    m = {"W": "ink3" if receptor else col}
    cv.sprite([r[:8] for r in rows], x + 4, y, m, outline="parch0" if receptor else "white")


for k in range(5):
    note(k, 16, receptor=True)
for k, y in ((0, 40), (2, 62), (4, 62), (1, 96), (3, 118), (2, 140), (0, 160), (4, 170), (1, 130)):
    note(k, y)
cv.rect(LX, 14, 100, 1, "gold2")
cv.text(LX + 50, 30, "얼쑤!", "gold2", 15, anchor="ma")
cv.text(LX + 50, 46, "128 장단", "parch2", 12, anchor="ma")

# HUD --------------------------------------------------------------------------------------------------
cv.rect(0, 0, 104, 30, "ink0"); cv.frame(0, 0, 104, 30, "gold0")
cv.text(4, 2, "대면 — 금빛 가면의 춤", "gold2", 10)
cv.text(4, 12, "굿거리장단 · 빠르기 92", "parch", 10)
bar(cv, 4, 25, 96, 2, 0.74, "red2", hi="pink")
cv.rect(216, 0, 104, 30, "ink0"); cv.frame(216, 0, 104, 30, "gold0")
cv.text(220, 2, "점수", "parch0", 10)
cv.text(316, 10, "0,842,330", "parch2", 12, anchor="ra")
cv.text(220, 20, "다음 곡 · 월전 (웃음 장단)", "parch0", 10)
judg = [("얼쑤", 412, "gold2"), ("좋다", 58, "moss3"), ("어허", 6, "orange"), ("놓침", 2, "red2")]
for k, (name, n, col) in enumerate(judg):
    cv.text(6 + k * 26, 160, name, col, 10)
    cv.text(6 + k * 26, 169, str(n), "parch2", 10)

cv.export("concept-23-retro-rhythm.png")
print("saved")
