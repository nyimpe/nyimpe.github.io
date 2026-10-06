"""Concept 40 — tactical CRPG after Baldur's Gate 3 (surfaces, dice checks, and a calamity that switches between horse and ox)."""
import math
from pix import *

cv = Canvas("tan", seed=521)
rng = cv.rng

# Village square seen from above -----------------------------------------------------------------------------------
for j in range(14, 156):
    for i in range(W):
        if rng.random() < 0.06:
            cv.dot(i, j, "brown2" if rng.random() < 0.6 else "parch0")
for x in range(0, W, 16):  # faint movement grid
    for y in range(14, 156, 2):
        cv.dot(x, y, "parch0")
for y in range(14, 156, 16):
    for x in range(0, W, 2):
        cv.dot(x, y, "parch0")
# Thatched houses along the top
for hx in (8, 70, 132):
    cv.rect(hx, 18, 50, 22, "parch0"); cv.rect(hx, 38, 50, 3, "brown")
    cv.disc(hx + 25, 22, 30, "gold", ry=10); cv.disc(hx + 25, 20, 26, "yellow", ry=7)
    cv.rect(hx + 21, 30, 8, 10, "brown0")
# The luring tree that glows and whistles
L = Layer(seed=2)
L.disc(22, 92, 16, "moss0"); L.disc(18, 86, 10, "moss")
L.rect(20, 100, 5, 14, "brown0")
L.paste(cv, outline="ink0")
for k in range(6):
    cv.dot(10 + rng.randrange(24), 80 + rng.randrange(20), "gold2")
cv.text(22, 116, "장화훤요", "moss0", 10, shadow="parch2", anchor="ma")

# Surfaces: an electrified puddle and a burning oil spill ------------------------------------------------------------
cv.disc(92, 110, 30, "teal", ry=14); cv.disc(92, 109, 27, "teal2", ry=11)
for k in range(5):  # lightning crackling over the water
    x0, y0 = 72 + k * 9, 100 + (k % 2) * 6
    cv.line(x0, y0, x0 + 4, y0 + 5, "gold2"); cv.line(x0 + 4, y0 + 5, x0 + 1, y0 + 9, "gold2")
cv.text(92, 126, "물 + 번개", "flame0", 10, shadow="parch2", anchor="ma")
cv.disc(200, 118, 34, "ink2", ry=13)
for k in range(26):
    fx, fy = 172 + rng.randrange(56), 108 + rng.randrange(20)
    cv.sprite([".R.", "ROR", "OYO"], fx, fy - 3, {"R": "red2", "O": "orange", "Y": "gold2"})
cv.text(200, 136, "기름 + 불", "red0", 10, shadow="parch2", anchor="ma")
# Burning bark falling from the sky
for k in range(3):
    bx, by = 150 + k * 40, 54 + k * 6
    cv.line(bx - 14, by - 14, bx, by, "orange")
    cv.rect(bx - 1, by - 1, 5, 3, "brown0"); cv.dot(bx + 1, by - 2, "gold2")
cv.text(196, 46, "천화", "red0", 10, shadow="parch2", anchor="ma")

# Gangcheol: a calamity in horse form, wreathed in heat ------------------------------------------------------------------
L = Layer(seed=4)
gx, gy = 270, 92
L.disc(gx, gy, 22, "red2", ry=10)
L.disc(gx - 24, gy - 10, 9, "red2", ry=7); L.rect(gx - 20, gy - 14, 8, 10, "red2")
for lx in (gx - 14, gx - 4, gx + 8, gx + 16):
    L.rect(lx, gy + 6, 4, 14, "red")
for k in range(10):  # flaming mane and tail
    L.disc(gx - 14 + k * 3, gy - 10 - (k % 3) * 2, 3, "orange")
    L.disc(gx + 22 + k, gy - 4 + k * 1.5, 2.4, "orange")
L.paste(cv, outline="ink0")
cv.rect(gx - 28, gy - 12, 3, 2, "gold2")
for k in range(16):  # heat shimmer
    a = k / 16 * 6.28
    cv.dot(gx + 34 * math.cos(a), gy + 20 * math.sin(a), "orange2")
cv.text(gx, 50, "강철 · 말 모습", "red0", 11, shadow="parch2", anchor="ma")
cv.text(gx, 62, "다음 차례: 소 모습(우박)", "flame0", 10, shadow="parch2", anchor="ma")

# Party, with the archer's planned shot -----------------------------------------------------------------------------
members = [(128, 128, "flame0", True), (102, 138, "red", False), (152, 138, "moss", False), (126, 148, "parch2", False)]
rows = ["..KK..", ".SSSS.", ".CCCC.", "CCCCCC", ".CCCC.", ".K..K."]
rows = ["".join(ch * 2 for ch in r) for r in rows for _ in (0, 1)]
for x, y, col, sel in members:
    if sel:
        cv.ring(x + 6, y + 12, 10, "gold2", ry=3)
    cv.sprite(rows, x, y, {"K": "ink0", "S": "skin", "C": col}, outline="ink0")
cv.rect(140, 132, 2, 8, "brown0")  # bow
for t in range(0, 101, 4):  # arrow arc toward the horse
    x = 142 + (gx - 146) * t / 100
    y = 130 + (gy - 130) * t / 100 - 26 * math.sin(math.pi * t / 100)
    cv.dot(x, y, "ink0")
cv.rect(180, 72, 54, 12, "ink0"); cv.text(207, 73.5, "명중 72%", "gold2", 10, anchor="ma")

# Dice check popup ---------------------------------------------------------------------------------------------------
cv.rect(4, 18, 92, 44, "ink0"); cv.frame(4, 18, 92, 44, "gold0")
cv.sprite(["....GG....", "..GGGGGG..", ".GGGGGGGG.", "GGGGGGGGGG", "GGGGGGGGGG", "GGGGGGGGGG", ".GGGGGGGG.", "..GGGGGG..",
           "....GG...."], 10, 26, {"G": "gold"}, outline="gold0")
cv.text(15, 28.5, "18", "ink0", 10, shadow=None, anchor="ma")
cv.text(26, 21, "의지 판정", "parch2", 10)
cv.text(26, 33, "18 + 2 ≥ 15", "gold2", 10)
cv.text(26, 46, "나무의 휘파람을 버팀", "moss3", 10)

# Turn order and hotbar ----------------------------------------------------------------------------------------------
cv.rect(0, 0, W, 14, "ink0")
for k, col in enumerate(("flame0", "red2", "red", "moss", "parch2")):
    cv.rect(120 + k * 16, 2, 12, 10, col); cv.frame(120 + k * 16, 2, 12, 10, "gold2" if k == 0 else "ink2")
cv.text(4, 1.5, "강철이 지나간 고을", "parch2", 10)
cv.text(316, 1.5, "셋째 차례", "parch0", 10, anchor="ra")
cv.rect(0, 166, W, 14, "ink0")
cv.disc(10, 173, 4, "moss3"); cv.text(18, 167.5, "행동", "parch2", 10)
cv.sprite(["..G..", ".GGG.", "GGGGG"], 46, 170, {"G": "orange2"}); cv.text(54, 167.5, "보조", "parch2", 10)
cv.text(86, 167.5, "이동 9보", "parch2", 10)
for k, nm in enumerate(("활쏘기", "불화살", "물 붓기", "밀치기", "숨기")):
    x = 140 + k * 36
    cv.rect(x, 167, 33, 12, "ink1"); cv.frame(x, 167, 33, 12, "gold2" if k == 0 else "ink3")
    cv.text(x + 16.5, 168, nm, "parch2", 10, anchor="ma")

cv.export("concept-40-turn-crpg.png")
print("saved")
