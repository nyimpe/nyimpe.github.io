"""Concept 4 — castaway survival craft (top-down island at dusk)."""
import math
from pix import *

cv = Canvas("teal", seed=61)
rng = cv.rng


def island(x, y):
    n = 0.06 * math.sin(x * 0.09) + 0.05 * math.sin(y * 0.13 + 1) + 0.03 * math.sin((x + y) * 0.21)
    return ((x - 214) / 196) ** 2 + ((y - 64) / 124) ** 2 + n


# Sea, beach, grass -------------------------------------------------------------
for y in range(H):
    for x in range(W):
        v = island(x, y)
        if v > 1.0:
            col = "teal" if v < 1.18 else "teal0"
            if v < 1.05 and (x + 2 * y) % 5 == 0:
                col = "teal2"
        elif v > 0.86:
            col = "parch" if rng.random() > 0.1 else "parch0"
        elif v > 0.8:
            col = "tan"
        else:
            col = "moss" if rng.random() > 0.12 else rng.choice(("moss2", "moss0"))
        cv.dot(x, y, col)
for _ in range(60):  # foam and wave lines
    x, y = rng.randrange(W), rng.randrange(H)
    if 1.0 < island(x, y) < 1.3:
        cv.rect(x, y, rng.randrange(3, 8), 1, "teal3" if island(x, y) > 1.05 else "white")
for _ in range(220):  # reeds and grass tufts
    x, y = rng.randrange(W), rng.randrange(H)
    if island(x, y) < 0.78:
        cv.dot(x, y, rng.choice(("moss2", "moss3", "moss0")))
        cv.dot(x, y - 1, "moss3")

# Wrecked boat on the shore
L = Layer(seed=2)
for k in range(5):
    L.rect(22 + k * 2, 132 + k, 40 - k * 4, 3, "brown" if k % 2 else "brown2")
L.rect(26, 131, 30, 1, "brown0")
L.line(30, 128, 62, 116, "brown0"); L.line(31, 128, 63, 116, "brown2")
L.rect(48, 118, 12, 7, "parch0"); L.rect(49, 119, 10, 5, "parch")
L.paste(cv, outline="ink0")

# Giant crab shell shelter (geohae)
L = Layer(seed=3)
cx, cy = 112, 56
L.disc(cx, cy, 30, "red0", ry=21)
L.disc(cx, cy - 2, 28, "red", ry=19)
L.disc(cx - 6, cy - 8, 18, "red2", ry=10)
for k in range(9):
    a = math.radians(200 + k * 17)
    L.disc(cx + 29 * math.cos(a), cy + 20 * math.sin(a), 3, "red0")
for bx_, by_ in ((cx - 12, cy - 8), (cx + 4, cy - 12), (cx + 14, cy - 4), (cx - 2, cy + 2), (cx - 18, cy + 4)):
    L.disc(bx_, by_, 2, "orange")
L.disc(cx, cy + 14, 11, "ink0", ry=8)  # entrance
L.rect(cx - 11, cy + 14, 22, 8, "ink0")
L.rect(cx - 6, cy + 16, 12, 4, "brown")
L.paste(cv, outline="ink0")
for px_ in (cx - 26, cx + 24):
    cv.rect(px_, cy + 8, 2, 14, "brown0")

# Log pile, stones
for k in range(4):
    cv.sprite(["BBBBBBBBBB", "bBBBBBBBBb", ".bbbbbbbb."], 70 + (k % 2) * 4, 100 + k * 3, {"B": "brown2", "b": "brown"}, outline="ink0")
for sx, sy in ((88, 128), (240, 150), (206, 40), (290, 128)):
    cv.sprite([".GG.", "GgGG", "GGGg", ".gg."], sx, sy, {"G": "iron2", "g": "iron"}, outline="ink1")

# Geunhwacho plot: blooms within a day
for k in range(6):
    px_, py_ = 196 + (k % 3) * 14, 112 + (k // 3) * 12
    cv.rect(px_, py_, 12, 10, "brown0"); cv.rect(px_ + 1, py_ + 1, 10, 8, "brown")
    for r in range(3):
        cv.rect(px_ + 1, py_ + 2 + r * 3, 10, 1, "brown0")
    stage = k % 3
    cv.rect(px_ + 5, py_ + 5 - stage * 2, 2, 2 + stage * 2, "moss2")
    if stage >= 1:
        cv.dot(px_ + 4, py_ + 3, "moss3"); cv.dot(px_ + 7, py_ + 2, "moss3")
    if stage == 2:
        cv.sprite([".P.", "PYP", ".P."], px_ + 4, py_ - 2, {"P": "pink", "Y": "gold2"})

# Pines inland
for tx, ty, h in ((250, 92, 24), (282, 104, 30), (236, 64, 18), (300, 70, 22)):
    pine(cv, tx, ty, h, dark="moss0", mid="moss", trunk="brown0", seed=tx)

# One-eyed giant (Daein) looming over the treeline, half hidden in sea fog
L = Layer(seed=7)
gx, gy = 284, 26
L.disc(gx, gy + 38, 40, "brown", ry=20)  # hunched shoulders
L.disc(gx - 6, gy + 34, 32, "skin0", ry=14)
L.disc(gx, gy, 19, "brown", ry=22)
L.disc(gx - 3, gy - 1, 16, "skin0", ry=19)
L.disc(gx - 6, gy - 4, 9, "skin", ry=10)
for k in range(16):  # wild hair
    L.line(gx - 20 + k * 2.6, gy - 16, gx - 26 + k * 3.4, gy - 30 + (k % 4) * 2, "ink0")
    L.line(gx - 19 + k * 2.6, gy - 16, gx - 25 + k * 3.4, gy - 29 + (k % 4) * 2, "ink1")
L.disc(gx - 2, gy - 17, 19, "ink1", ry=6)
for k in range(10):  # beard
    L.line(gx - 12 + k * 2.5, gy + 12, gx - 14 + k * 2.8, gy + 24 + (k % 3) * 2, "ink1")
L.rect(gx - 14, gy - 6, 22, 3, "ink0")  # heavy brow
L.disc(gx - 3, gy + 1, 7, "parch", ry=5)
L.rect(gx - 9, gy + 13, 14, 3, "red0")
for k in range(4):
    L.dot(gx - 8 + k * 4, gy + 13, "parch")
L.paste(cv, outline="ink0")
for tx, ty, h in ((232, 76, 30), (256, 72, 34), (300, 78, 30), (318, 70, 26)):
    pine(cv, tx, ty, h, dark="moss0", mid="moss", trunk="brown0", seed=tx + 1)
for y in range(30, 76):  # sea fog
    for x in range(214, 320):
        f = math.sin(x * 0.07) + math.sin(x * 0.023 + y * 0.19) + 0.9 * math.sin(y * 0.31 - x * 0.05)
        if f > 0.9 and (x + y) % 2 == 0:
            cv.dot(x, y, "iron2" if f > 1.6 else "iron")
        elif f > 1.8:
            cv.dot(x, y, "iron2")

# Dusk: warm near the fire, dim at the edges
FX, FY = 150, 104
cv.darken(lambda i, j: 1.25 - math.hypot(i - FX, (j - FY) * 1.2) / 190)

cv.disc(gx - 3, gy + 1, 3, "red2"); cv.dot(gx - 4, gy, "white")
for a_ in range(0, 360, 30):
    cv.dot(gx - 3 + 6 * math.cos(math.radians(a_)), gy + 1 + 4 * math.sin(math.radians(a_)), "red")

# Campfire with a giant conch cooking
for r_, col in ((22, "gold0"), (15, "orange")):
    for a in range(0, 360, 5):
        x = FX + r_ * math.cos(math.radians(a)); y = FY + r_ * 0.7 * math.sin(math.radians(a))
        if (int(x) + int(y)) % 2:
            cv.dot(x, y, col)
for a in range(0, 360, 40):
    cv.sprite(["GG", "Gg"], FX - 1 + 8 * math.cos(math.radians(a)), FY + 1 + 5 * math.sin(math.radians(a)), {"G": "iron2", "g": "iron"})
cv.sprite(["..Y..", ".YOY.", "YOWOY", "OOWOO", ".OOO."], FX - 2, FY - 4, {"Y": "gold2", "O": "orange", "W": "white"})
cv.line(FX - 7, FY - 12, FX, FY - 2, "brown0"); cv.line(FX + 7, FY - 12, FX, FY - 2, "brown0")
cv.sprite([".PPPP..", "PPpPPP.", "PPPPpPP", ".PPPPP."], FX - 3, FY - 14, {"P": "parch", "p": "pink"}, outline="ink0")

cv.sprite(["W", "W", "W", ".", "W"], 176, 82, {"W": "red2"}, outline="ink0")

# Castaway with an axe
cv.disc(176, 106, 6, "ink0", ry=2)
cv.sprite([
    "....KK......",
    "...KKKK.....",
    "...SSSS.....",
    "..SSESSE....",
    "...SSSS.....",
    "..WWWWWW..I.",
    ".WWwWWwWW.II",
    ".SWWWWWWWSB.",
    "..WWRRWW..B.",
    "..BBBBBB....",
    "..BB..BB....",
    "..SS..SS....",
], 170, 94, {"K": "ink0", "S": "skin", "E": "ink0", "W": "parch2", "w": "parch0", "R": "red",
             "B": "brown", "I": "iron2"}, outline="ink0")

# HUD ---------------------------------------------------------------------------------
panel(cv, 4, 4, 92, 30, fill="ink1", edge="parch0", inner="ink2")
for k in range(5):
    cv.sprite([".R.R.", "RRRRR", "RRRRR", ".RRR.", "..R.."], 9 + k * 7, 9, {"R": "red2" if k < 4 else "ink3"})
for k in range(5):
    cv.sprite(["WWWWW", "GGGGG", ".GGG."], 9 + k * 7, 18, {"W": "white" if k < 2 else "ink3", "G": "gold" if k < 2 else "ink3"})
cv.text(46, 6.5, "체력", "parch", 10)
cv.text(46, 14.5, "허기", "parch", 10)
cv.text(9, 23.5, "표류 12일째 · 해 질 녘", "gold2", 10)

panel(cv, 240, 74, 76, 74, fill="ink1", edge="gold0", inner="ink2")
cv.text(245, 76.5, "제작", "gold2", 11)
recipes = [("거해 껍질 지붕", "완성", "moss3"), ("고산나봉 나팔", "소라 1 · 밧줄 1", "parch"),
           ("돌도끼", "돌 2 · 나무 1", "parch"), ("뗏목", "통나무 12 · 밧줄 6", "ink3")]
for k, (name, need, col) in enumerate(recipes):
    y = 86 + k * 15
    cv.rect(244, y, 68, 13, "ink2" if k == 1 else "ink1")
    if k == 1:
        cv.frame(244, y, 68, 13, "gold2")
    cv.text(247, y + 0.5, name, "parch2" if k < 3 else "ink3", 10)
    cv.text(247, y + 6.5, need, col, 10)

icons = [
    (["...II", "..III", ".BBI.", "BB...", "B...."], {"I": "iron2", "B": "brown2"}),             # stone axe
    (["..O..", ".OYO.", "..B..", "..B..", "..B.."], {"O": "orange", "Y": "gold2", "B": "brown2"}),  # torch
    (["P....", "PPP..", ".PPPP", "..PPp", "...pp"], {"P": "parch", "p": "pink"}),              # mountain conch
    ([".RRR.", "R...R", ".RRR.", "R...R", ".RRR."], {"R": "tan"}),                              # rope
    (["..G..", ".G.G.", "..B..", ".BBB.", "BBBBB"], {"G": "moss3", "B": "brown"}),             # geunhwacho seeds
    (["WWWWW", "GGGGG", ".GGG."], {"W": "white", "G": "gold"}),                                # rice
    (["BBBBB", "bbbbb", "BBBBB", "bbbbb"], {"B": "brown2", "b": "brown"}),                     # planks
    ([".II..", "IIII.", ".IIII", "..II."], {"I": "iron2"}),                                     # stone
]
for k, (rows, m) in enumerate(icons):
    x = 88 + k * 18
    panel(cv, x, 158, 17, 17, fill="ink1", edge="gold2" if k == 0 else "parch0", inner="ink2")
    cv.sprite(rows, x + 6, 164, m)
cv.text(88, 150.5, "돌도끼", "parch2", 10)

cv.export("concept-4-survival-craft.png")
print("saved")
