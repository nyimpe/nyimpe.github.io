"""Concept 24 — rhythm roguelike after Crypt of the NecroDancer (move only on the janggu beat)."""
import math
from pix import *

cv = Canvas("ink0", seed=361)
rng = cv.rng
T, OX, OY, COLS, ROWS = 16, 24, 14, 17, 8

# Dungeon floor that lights up in the five cardinal colours on the beat ---------------------------------
OBANG = ["flame0", "red0", "gold0", "ink3", "ink1"]
walls = {(c, 0) for c in range(COLS)} | {(c, ROWS - 1) for c in range(COLS)} | {(0, r) for r in range(ROWS)} | \
        {(COLS - 1, r) for r in range(ROWS)} | {(5, 2), (5, 3), (11, 4), (11, 5), (8, 2)}
for r in range(ROWS):
    for c in range(COLS):
        x, y = OX + c * T, OY + r * T
        if (c, r) in walls:
            cv.rect(x, y, T, T, "brown0"); cv.rect(x + 1, y + 1, T - 2, T - 2, "brown")
            cv.rect(x + 1, y + 1, T - 2, 2, "brown2")
            if (c + r) % 4 == 0:  # wall torches
                cv.sprite([".Y.", "YOY", ".B."], x + 6, y + 4, {"Y": "gold2", "O": "orange", "B": "brown0"})
            continue
        lit = (c + r) % 2 == 0
        cv.rect(x, y, T, T, OBANG[(c * 2 + r) % 5] if lit else "ink1")
        cv.frame(x, y, T, T, "ink0")


def at(c, r):
    return OX + c * T, OY + r * T


# Player: a shaman dancer with fan and bell
x, y = at(7, 4)
cv.sprite(["..KKKK..", ".KRRRRK.", "..SSSS..", "..SESE..", "RWWWWWWB", ".WWWWWW.", ".TTTTTT.", ".T....T."], x + 4, y + 3,
          {"K": "ink0", "R": "red2", "S": "skin", "E": "ink0", "W": "white", "B": "gold2", "T": "flame"}, outline="ink0")
# Enemies with rhythmic habits
x, y = at(10, 3)  # chakchak ghost lunges every second beat
cv.sprite(["..KKKK..", ".KGGGGK.", ".KGEGEK.", "KKWWWWKK", "K.WWWW.K", "..W.W.W."], x + 4, y + 4,
          {"K": "ink0", "G": "ghost2", "E": "red2", "W": "ghost"}, outline="ink0")
cv.text(x + 8, y - 6, "착착", "ghost2", 10, anchor="ma")
x, y = at(4, 5)  # one-legged dokgak hops two tiles
cv.sprite(["KKKKKK", ".SSSS.", ".SESE.", "DDDDDD", "DDDDDD", "..DD..", "..DD.."], x + 5, y + 3,
          {"K": "tan", "S": "skin", "E": "ink0", "D": "moss0"}, outline="ink0")
for k in range(3):
    cv.dot(x + 8 - 16 - k * 3, y + 14 - abs(1 - k) * 3, "parch2")
x, y = at(13, 2)  # gourd that bursts into magpies when struck
cv.sprite(["..G..", ".GGG.", "..G..", ".GGG.", "GGGGG", ".GGG."], x + 5, y + 5, {"G": "parch2"}, outline="ink0")
cv.text(x + 8, y - 6, "훼훼", "parch2", 10, anchor="ma")
for k in range(4):  # a wisp procession circling
    a = math.radians(k * 90 + 20)
    wx, wy = at(13, 5)
    cv.sprite([".c.", "cCc", ".W."], wx + 7 + 12 * math.cos(a), wy + 8 + 8 * math.sin(a), {"c": "flame0", "C": "flame", "W": "flame2"})

# Singer shopkeeper
x, y = at(2, 2)
cv.sprite(["..KKK..", ".SSSSS.", ".SESES.", "PPPPPPP", "PPPPPPP", ".P...P."], x + 4, y + 4,
          {"K": "ink0", "S": "skin", "E": "ink0", "P": "purple2"}, outline="ink0")
for k in range(3):
    cv.sprite(["..N", "..N", "NNN"], x + 14 + k * 5, y - 2 - k * 3, {"N": "gold2"})
cv.text(x + 8, y + 18, "소리꾼", "gold2", 10, anchor="ma")

# Beat bar: janggu strokes sliding toward the centre ----------------------------------------------------------
cv.rect(0, 146, W, 34, "ink0"); cv.rect(0, 146, W, 1, "gold0")
cv.disc(160, 162, 10, "red0"); cv.disc(160, 162, 8, "red2")
cv.sprite(["R.R", "RRR", ".R."], 159, 160, {"R": "white"})
for k in range(1, 6):
    for side in (-1, 1):
        x = 160 + side * k * 22
        cv.rect(x - 2, 154, 4, 16, "flame" if k % 2 else "gold2")
cv.text(160, 147, "덩 · 덕 · 쿵", "parch0", 10, anchor="ma")
cv.text(6, 150, "자진모리 · 빠르기 120", "parch2", 10)
cv.text(6, 162, "연속 ×3", "gold2", 11)
cv.text(316, 150, "넷째 굴 · 2층", "parch2", 10, anchor="ra")
for k in range(5):
    cv.sprite([".R.R.", "RRRRR", ".RRR.", "..R.."], 268 + k * 9, 164, {"R": "red2" if k < 4 else "ink3"})
cv.rect(0, 0, W, 12, "ink0")
cv.text(4, 1.5, "장단 던전 — 박자에 맞춰야만 움직인다", "parch2", 10)
cv.text(316, 1.5, "부채 · 방울", "gold2", 10, anchor="ra")

cv.export("concept-24-indie-beat.png")
print("saved")
