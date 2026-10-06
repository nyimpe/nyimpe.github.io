"""Concept 29 — table gamble after Buckshot Roulette (poisoned blowfish soup against a three-mouthed ghost)."""
import math
from pix import *

cv = Canvas("ink0", seed=411)
rng = cv.rng
LX, LY = 112, 30  # hanging lamp

# Dark back wall with faint lattice -----------------------------------------------------------------------------
cv.rect(0, 0, W, 96, "ink1")
for x in range(8, W, 24):
    cv.rect(x, 0, 1, 96, "ink0")
for y in range(10, 96, 22):
    cv.rect(0, y, W, 1, "ink0")

# Next opponent waiting in the dark: one head, seven topknots
L = Layer(seed=5)
L.disc(286, 70, 16, "ink2", ry=26)
L.disc(286, 40, 10, "ink2")
for k in range(7):
    L.disc(272 + k * 4.6, 28 - abs(3 - k) * 1.5, 2.2, "ink3")
L.paste(cv, outline="ink0")
cv.dot(283, 40, "red2"); cv.dot(289, 40, "red2")
cv.text(286, 76, "다음 상대", "ink3", 10, shadow=None, anchor="ma")

# Three-mouthed ghost across the table ---------------------------------------------------------------------------
L = Layer(seed=2)
L.disc(160, 92, 46, "purple0", ry=30)           # shoulders in a dark robe
L.disc(160, 52, 30, "ghost", ry=34)             # one big head
L.rect(130, 20, 60, 6, "ink0")                  # black gat brim
L.rect(146, 8, 28, 13, "ink0")
L.paste(cv, outline="ink0")
for ex in (148, 172):  # eyes
    cv.disc(ex, 40, 4, "white", ry=3); cv.disc(ex, 40, 1.6, "red0")
cv.line(141, 33, 153, 35, "ink1"); cv.line(167, 35, 179, 33, "ink1")
mouths = [(160, 56, True), (146, 72, True), (174, 72, False)]  # (x, y, alive)
for mx, my, alive in mouths:
    if alive:
        cv.disc(mx, my, 7, "red0", ry=4); cv.rect(mx - 6, my, 13, 1, "ink0")
        for t in range(-5, 6, 3):
            cv.dot(mx + t, my - 2, "white"); cv.dot(mx + t + 1, my + 2, "white")
    else:  # a lost life: the mouth is sewn shut
        cv.rect(mx - 7, my, 15, 1, "ink1")
        for t in range(-6, 7, 3):
            cv.line(mx + t, my - 2, mx + t + 1, my + 2, "parch0")
cv.text(160, 2, "삼구일두귀", "ghost2", 11, anchor="ma")

# Lacquered table in perspective -----------------------------------------------------------------------------------
TY = 96
for j in range(TY, H):
    t = (j - TY) / (H - TY)
    half = 120 + t * 60
    cv.rect(160 - half, j, half * 2, 1, "red0" if j < TY + 3 else "brown0")
for j in range(TY + 3, H, 6):
    cv.rect(0, j, W, 1, "red0")
cv.rect(40, TY, 240, 2, "red")

# Eight bowls in a row: three poisoned, shuffled and covered
bowls_x = [70 + k * 25 for k in range(8)]
for k, bx in enumerate(bowls_x):
    by = 112
    cv.disc(bx, by + 6, 10, "ink0", ry=3)
    cv.rect(bx - 9, by, 19, 6, "parch2"); cv.rect(bx - 9, by + 5, 19, 1, "parch0")
    cv.disc(bx, by + 6, 9, "parch0", ry=2)
    if k == 2:  # spilt open: the eaten bowl
        cv.disc(bx, by, 9, "tan", ry=2)
        continue
    if k == 5:  # lid lifted by the silver spoon
        cv.disc(bx + 4, by - 14, 9, "parch", ry=3)
        cv.disc(bx, by, 9, "orange", ry=2)
        for f in range(4):  # tiny moth-like poison insects drifting up
            fx, fy = bx - 6 + f * 4, by - 6 - f * 5
            cv.sprite(["W.W", ".K.", "W.W"], fx, fy, {"W": "ghost2", "K": "ink0"})
        continue
    cv.disc(bx, by, 9, "parch", ry=3)  # lid
    cv.disc(bx, by - 2, 2, "parch0")

# Lamp light ----------------------------------------------------------------------------------------------------
cv.rect(LX, 0, 1, LY - 4, "ink2")
cv.sprite(["...GG...", "..GGGG..", ".GYYYYG.", "GYYOOYYG", "GYOWWOYG", "GYYOOYYG", ".GYYYYG.", "..GGGG..", "...GG..."],
          LX - 4, LY - 6, {"G": "gold0", "Y": "gold2", "O": "orange2", "W": "white"})
cv.darken(lambda x, y: 1.25 - math.hypot((x - 150) * 0.9, (y - 70) * 1.2) / 150 if math.hypot(x - LX, y - LY) > 7 else 1)

# Player's arm in a white sleeve with a red cuff, holding a blackened silver spoon over bowl 6
def arm_pt(t):
    return 284 - t * 1.25, 192 - t * 0.98, 17 - t * 0.14


for t in range(44):
    x, y, r = arm_pt(t)
    cv.disc(x, y, r + 1, "ink0")
for t in range(44):
    x, y, r = arm_pt(t)
    cv.disc(x, y, r, "red" if t > 39 else "parch0")
    if t <= 39:
        cv.disc(x + 3, y + 4, r * 0.5, "tan")
cv.disc(223, 144, 7, "ink0", ry=6)
cv.disc(223, 144, 6, "skin0", ry=5)       # fist
for k in range(3):                          # knuckles toward the bowl
    cv.disc(216 - k, 139 + k * 3, 2.4, "skin0")
cv.sprite(["SSS", "SSS"], 213, 136, {"S": "skin"}, outline="ink0")  # thumb and finger pinching the spoon
cv.line(214, 136, 198, 121, "iron2"); cv.line(215, 136, 199, 121, "iron2")
cv.disc(196, 117, 3, "ink0", ry=4)  # the spoon's bowl has turned black
cv.ring(196, 117, 4, "iron", ry=5)

# Player items and lives (drawn after lighting) --------------------------------------------------------------------
items = [(["..II..", ".IIII.", ".IIII.", "..II..", "..I...", "..I...", "..I...", "..I...", "..I..."], {"I": "iron2"}, "은수저"),
         (["..........", "BBBBBBBBBB", "BTTTTTTTTB", ".BBBBBBBB.", "..BBBBBB.."], {"B": "parch0", "T": "brown2"}, "숭늉"),
         (["..RRRR..", ".R....R.", "R..RR..R", "R.R..R.R", "R..RR..R", ".R....R.", "..RRRRR."], {"R": "tan"}, "오랏줄"),
         (["..KK..", ".RRRR.", "RRRRRR", "RRRRRR", "RRRRRR", ".RRRR."], {"R": "red", "K": "brown0"}, "고추장")]
for k, (rows, cmap, name) in enumerate(items):
    x = 8 + k * 30
    cv.rect(x, 150, 26, 26, "ink1"); cv.frame(x, 150, 26, 26, "ink3")
    w = max(len(r) for r in rows)
    cv.sprite(rows, x + 13 - w // 2, 162 - len(rows), cmap, outline="ink0")
    cv.text(x + 13, 165, name, "parch0", 10, anchor="ma")
for k in range(4):  # player's lives as candles
    lit = k < 3
    cv.rect(10 + k * 9, 132, 4, 12, "parch2" if lit else "ink3")
    if lit:
        cv.sprite([".Y.", "YOY"], 10 + k * 9, 128, {"Y": "gold2", "O": "orange"})
cv.text(10, 118, "내 목숨", "parch2", 10)

# Round header and the choice -------------------------------------------------------------------------------------
cv.rect(232, 0, 88, 26, "ink0")
cv.text(276, 2, "셋째 상 · 독 셋", "red2", 10, anchor="ma")
for k in range(8):
    cv.rect(238 + k * 10, 16, 7, 5, "red2" if k < 3 else "parch")
cv.rect(0, 0, 92, 26, "ink0")
cv.text(46, 2, "은수저가 검게 변했다", "gold2", 10, anchor="ma")
cv.text(46, 13, "여섯째 그릇에 독", "parch0", 10, anchor="ma")
for k, s in enumerate(("내가 먹는다", "상대에게 민다")):
    x = 254
    y = 140 + k * 18
    cv.rect(x - 6, y - 2, 70, 15, "ink0" if k else "red0"); cv.frame(x - 6, y - 2, 70, 15, "gold2" if k else "parch0")
    cv.text(x + 29, y + 0.5, s, "gold2" if k else "parch0", 10, anchor="ma")

cv.export("concept-29-itch-table.png")
print("saved")
