"""Concept 9 — mercy bullet-hell RPG after Undertale (soothe, don't slay)."""
import math
from pix import *

cv = Canvas("ink0", seed=111)
rng = cv.rng

# Sieve hung up to stall the Yagwang, who counts its holes until dawn ------------------
SX, SY = 112, 28
cv.line(SX, 0, SX, SY - 13, "parch0")
cv.disc(SX, SY, 13, "brown2"); cv.disc(SX, SY, 11, "brown0")
for j in range(SY - 10, SY + 11, 2):
    for i in range(SX - 10, SX + 11, 2):
        if (i - SX) ** 2 + (j - SY) ** 2 < 100:
            cv.dot(i, j, "parch0")
cv.ring(SX, SY, 13, "brown")
for k, (dx, dy) in enumerate(((-6, -4), (-2, -6), (3, -5))):  # counted holes glint
    cv.dot(SX + dx, SY + dy, "gold2")

# Yagwang hugging stolen straw shoes ---------------------------------------------------
L = Layer(seed=2)
mx, my = 164, 50
L.disc(mx, my, 22, "night2", ry=24)
L.disc(mx - 3, my - 4, 18, "night3", ry=19)
for k in range(9):  # ragged hem
    L.disc(mx - 18 + k * 4.5, my + 22 + (k % 2) * 2, 3, "night2")
L.disc(mx - 8, my - 10, 5, "white"); L.disc(mx + 7, my - 10, 5, "white")
L.disc(mx - 7, my - 11, 2, "ink0"); L.disc(mx + 6, my - 11, 2, "ink0")
L.line(mx - 5, my - 1, mx + 4, my - 1, "night0")
for k, (dx, dy) in enumerate(((-14, 6), (-4, 10), (6, 7), (-9, 14), (2, 15))):  # shoe pile
    L.sprite([".TTTTT.", "TTtTtTT", "TtTTTtT", ".TTTTT."], mx + dx - 3, my + dy, {"T": "tan", "t": "brown2"})
for side in (-1, 1):  # long arms wrapped around the pile
    for t in range(14):
        a = math.radians(200 + side * 0 + t * 10) if side < 0 else math.radians(-20 - t * 10)
        L.disc(mx + side * 14 + 9 * math.cos(a) * -side, my + 8 + 6 * math.sin(a), 2, "night3")
L.paste(cv, outline="ghost")

cv.rect(196, 18, 96, 30, "white"); cv.frame(196, 18, 96, 30, "ink2")
cv.sprite(["W..", "WW.", "WWW"], 193, 34, {"W": "white"})
cv.text(202, 22.5, "구멍이… 하나, 둘,", "ink0", 11, shadow=None)
cv.text(202, 33, "셋… 어디까지 셌더라", "ink0", 11, shadow=None)

cv.text(160, 80, "야광", "parch2", 11, anchor="ma")
cv.text(118, 89, "달램", "gold2", 10)
for k in range(5):
    cv.rect(138 + k * 9, 90, 7, 4, "gold2" if k < 3 else "ink2")
    cv.frame(138 + k * 9, 90, 7, 4, "gold0")

# Bullet box: straw shoes rain down while the soul dodges -------------------------------
BX, BY, BW, BH = 104, 100, 112, 44
cv.rect(BX - 2, BY - 2, BW + 4, BH + 4, "white")
cv.rect(BX, BY, BW, BH, "ink0")
shoe = [".TTTTT.", "TtTtTtT", ".TTTTT."]
for x, y in ((112, 104), (128, 114), (150, 102), (172, 118), (194, 106), (206, 128), (120, 132), (184, 136), (140, 124)):
    cv.sprite(shoe, x, y, {"T": "tan", "t": "brown2"})
    cv.dot(x + 2, y - 2, "brown2"); cv.dot(x + 2, y - 4, "brown0")
for a in range(0, 360, 30):  # ring of sieve holes closing in
    cv.rect(160 + 20 * math.cos(math.radians(a)), 128 + 9 * math.sin(math.radians(a)), 2, 2, "parch0")
cv.sprite(["..R..", ".RRR.", "RROrR", "RRRRR", ".RRR."], 158, 126, {"R": "red2", "r": "pink", "O": "orange2"})

# Player line and commands ---------------------------------------------------------------
cv.text(104, 149, "서생  Lv 3", "parch2", 11)
cv.text(176, 149, "넋", "parch2", 11)
bar(cv, 188, 152, 28, 4, 18 / 20, "red2", bg="red0")
cv.text(220, 149, "18/20", "parch2", 11)
cmds = [("베기", False), ("살피기", False), ("물건", False), ("달래기", True)]
for k, (name, on) in enumerate(cmds):
    x = 20 + k * 72
    cv.rect(x, 160, 64, 16, "ink0")
    cv.frame(x, 160, 64, 16, "gold2" if on else "parch0")
    cv.frame(x + 1, 161, 62, 14, "gold0" if on else "ink2")
    cv.text(x + 32, 163.5, name, "gold2" if on else "parch", 12, anchor="ma")
cv.sprite(["R.", "RR", "R."], 20 + 3 * 72 + 5, 166, {"R": "red2"})

cv.export("concept-9-mercy-rpg.png")
print("saved")
