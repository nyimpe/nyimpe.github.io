"""Concept 38 — stress-driven party crawler after Darkest Dungeon (four travellers end the centipede's yearly sacrifice)."""
import math
from pix import *

cv = Canvas("ink0", seed=501)
rng = cv.rng
FY = 128  # floor line

# Ruined inn corridor ------------------------------------------------------------------------------------------------
cv.rect(0, 14, W, FY - 14, "brown0")
for x in range(0, W, 46):
    cv.rect(x, 14, 6, FY - 14, "ink1"); cv.rect(x + 1, 14, 1, FY - 14, "brown")
for y in (40, 84):
    cv.rect(0, y, W, 3, "ink1")
for k in range(14):  # holes in the plaster
    x, y = rng.randrange(W), rng.randrange(20, FY - 10)
    cv.disc(x, y, rng.randrange(3, 8), "ink1", ry=rng.randrange(2, 5))
for cx, cy in ((10, 16), (300, 16)):  # cobwebs
    for k in range(5):
        cv.line(cx, cy, cx + (k - 2) * 8, cy + 18, "ink3")
    for r in (6, 11, 16):
        cv.ring(cx, cy, r, "ink3", ry=r * 0.8)
cv.rect(0, FY, W, 52, "ink1")
for x in range(0, W, 14):
    cv.rect(x, FY, 1, 26, "ink0")
# The shadow that grows as fear grows, looming behind the party
for j in range(14, 112):
    for i in range(10, 140):
        d = ((i - 72) / 56) ** 2 + ((j - 66) / 46) ** 2
        horns = min(((i - 44) / 9) ** 2 + ((j - 34) / 12) ** 2, ((i - 100) / 9) ** 2 + ((j - 34) / 12) ** 2)
        if (d < 1 or horns < 1) and ((i + j) % 2 == 0 or d < 0.55):
            cv.dot(i, j, "night1")
cv.rect(56, 54, 8, 3, "red2"); cv.rect(82, 54, 8, 3, "red2")
cv.text(70, 22, "어둑서니 · 두려울수록 커진다", "red2", 10, anchor="ma")


def big(rows):
    return ["".join(ch * 2 for ch in r) for r in rows for _ in (0, 1)]


def hero(x, y, rows, cmap):
    cv.sprite(big(rows), x, y, cmap, outline="ink0")


BASE = ["...HHHH...", "..HHHHHH..", "...SSSS...", "...SESE...", "..CCCCCC..", ".CCCCCCCC.", ".CCCCCCCC.", ".CCCCCCCC.", "..CCCCCC..",
        "..LL..LL..", "..KK..KK.."]
party = [  # back to front: shaman, physician, hunter, soldier
    (6, "무당", {"H": "ink0", "S": "skin", "E": "ink0", "C": "red", "L": "parch", "K": "ink0"}, 0.7, 3, False),
    (34, "의원", {"H": "ink1", "S": "skin", "E": "ink0", "C": "parch2", "L": "brown2", "K": "ink0"}, 0.9, 2, False),
    (62, "포수", {"H": "ink1", "S": "skin", "E": "ink0", "C": "brown2", "L": "brown0", "K": "ink0"}, 0.5, 9, True),
    (90, "장수", {"H": "iron", "S": "skin", "E": "ink0", "C": "flame0", "L": "ink2", "K": "ink0"}, 0.8, 5, False),
]
for x, name, cmap, hp, stress, afflicted in party:
    y = FY - 22
    if afflicted:
        for k in range(24):
            a = k / 24 * 6.28
            cv.dot(x + 10 + 15 * math.cos(a), y + 11 + 15 * math.sin(a), "purple2")
    hero(x, y, BASE, cmap)
    bar(cv, x, FY + 4, 20, 2, hp, "red2")
    for k in range(10):
        cv.rect(x + (k % 5) * 4, FY + 9 + (k // 5) * 3, 3, 2, "white" if k < stress else "ink3")
    cv.text(x + 10, FY + 16, name, "parch0", 10, anchor="ma")
cv.text(72, FY - 40, "겁에 질림", "purple2", 10, anchor="ma")
cv.rect(110, FY - 12, 16, 2, "iron2")   # front soldier's blade
# The toad that once stood against the centipede, puffing white breath
cv.sprite(big(["..GG.GG..", ".GKGGGKG.", "GGGGGGGGG", "GYYYYYYYG", ".GG...GG."]), 116, FY - 9, {"G": "moss2", "K": "ink0", "Y": "moss3"},
          outline="ink0")
for k in range(5):
    cv.disc(138 + k * 7, FY - 10 - k * 3, 2.5 + k * 0.8, "parch2")

# The great centipede and its little kin -------------------------------------------------------------------------------
segs = []
for k in range(16):
    t = k / 15
    segs.append((292 - 90 * t + 10 * math.sin(t * 9), FY - 10 - 70 * math.sin(t * 2.4) * (1 - 0.3 * t)))
for k, (x, y) in enumerate(reversed(segs)):
    cv.disc(x, y, 9, "ink0", ry=7)
for k, (x, y) in enumerate(reversed(segs)):
    cv.disc(x, y, 8, "red0" if k % 2 else "red", ry=6)
    cv.line(x - 6, y + 4, x - 10, y + 12, "gold0"); cv.line(x + 6, y + 4, x + 10, y + 12, "gold0")
hx, hy = segs[-1]
cv.disc(hx - 4, hy, 9, "red", ry=8)
cv.line(hx - 12, hy - 2, hx - 22, hy - 12, "gold2"); cv.line(hx - 12, hy + 2, hx - 22, hy + 10, "gold2")   # mandibles
cv.rect(hx - 8, hy - 4, 3, 2, "gold2")
cv.text(250, 22, "대오공", "red2", 12, anchor="ma")
bar(cv, 220, 34, 60, 3, 0.85, "red2")
for k, x in enumerate((268, 294)):  # hyangrang: little millipedes
    for j in range(6):
        cv.disc(x + j * 3, FY + 10 - (j % 2), 2, "brown2")
    cv.dot(x - 1, FY + 9, "gold2")
cv.text(286, FY + 18, "향랑", "parch0", 10, anchor="ma")

# Torch meter and skill bar ---------------------------------------------------------------------------------------------
cv.rect(0, 0, W, 14, "ink0")
cv.text(4, 1.5, "버려진 원 · 셋째 방", "parch2", 10)
cv.sprite([".Y.", "YOY", ".B.", ".B."], 150, 2, {"Y": "gold2", "O": "orange", "B": "brown2"})
bar(cv, 158, 5, 70, 4, 0.35, "orange", hi="gold2")
cv.text(316, 1.5, "횃불이 꺼져 간다", "orange", 10, anchor="ra")
cv.rect(0, 156, W, 24, "ink0"); cv.frame(0, 156, W, 24, "brown")
cv.text(6, 158, "장수", "flame", 10)
for k, nm in enumerate(("베기", "막아서기", "호통", "자리 바꾸기")):
    x = 38 + k * 46
    cv.rect(x, 159, 42, 17, "ink1"); cv.frame(x, 159, 42, 17, "gold0" if k else "gold2")
    cv.text(x + 21, 162, nm, "parch2", 10, anchor="ma")
cv.text(316, 158, "제물을 받던 지네", "parch0", 10, anchor="ra")
cv.text(316, 168, "스트레스 10이면 넋이 나감", "red2", 10, anchor="ra")

cv.export("concept-38-turn-stress.png")
print("saved")
