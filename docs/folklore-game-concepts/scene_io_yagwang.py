"""Concept 18 — Yagwang.io: shoe-stealing team game; sieves freeze the thieves (capture the flag)."""
import math
from pix import *
from io_ui import tag, nick

cv = Canvas("moss0", seed=201)
rng = cv.rng

# Hill at the top (Yagwang's lair), village below ------------------------------------------------
for y in range(H):
    for x in range(W):
        hill = y < 44 + 10 * math.sin(x * 0.03)
        cv.dot(x, y, ("moss" if rng.random() > 0.1 else "moss2") if hill else ("moss0" if rng.random() > 0.1 else "moss"))
for x in range(W):
    y = int(44 + 10 * math.sin(x * 0.03))
    cv.dot(x, y, "moss2"); cv.dot(x, y + 1, "ink1")
for t in range(0, 100):  # path up the hill
    x = 150 + 30 * math.sin(t * 0.05); y = 150 - t * 1.2
    cv.disc(x, y, 5, "tan")
for x in (40, 70, 250, 290):
    pine(cv, x, 34 + (x % 7), 18, dark="moss0", mid="moss2", trunk="brown0", seed=x)


def house(x, y):
    cv.rect(x + 2, y + 18, 44, 10, "brown")  # maru
    cv.rect(x + 2, y + 18, 44, 1, "brown2")
    cv.disc(x + 24, y + 10, 26, "gold0", ry=12)
    cv.disc(x + 24, y + 9, 24, "gold", ry=10)
    cv.disc(x + 20, y + 6, 13, "gold2", ry=4)


shoe_cols = ["tan", "red2", "white", "brown2", "pink", "tan"]
for hx, hy in ((14, 120), (86, 128), (196, 126), (262, 118)):
    house(hx, hy)
    for k in range(5):  # shoes lined up below the maru
        cv.sprite(["SS.SS"], hx + 6 + k * 8, hy + 30, {"S": shoe_cols[(k + hx) % 6]}, outline="ink0")

# Night: lanterns at the houses, moon on the hill
cv.darken(lambda i, j: max(1.25 - math.hypot(i - 60, j - 150) / 70, 1.25 - math.hypot(i - 230, j - 146) / 70,
                           0.62 if j < 50 else 0.4))

# Yagwang lair: pile of stolen shoes and a banner
for k in range(26):
    a, r = rng.uniform(0, 6.28), rng.uniform(0, 14)
    cv.sprite(["SS"], 262 + r * math.cos(a), 34 + r * 0.5 * math.sin(a), {"S": rng.choice(shoe_cols)}, outline="ink0")
cv.rect(280, 14, 1, 18, "brown0"); cv.rect(281, 14, 12, 8, "flame"); cv.frame(281, 14, 12, 8, "flame0")
cv.text(262, 44, "야광 소굴", "flame2", 10, anchor="ma")


def yagwang(x, y, carry=None, frozen=False):
    cv.sprite(["..BBBB..", ".BBBBBB.", "BBhBBBBB", "BWWBBWWB", "BWKBBWKB", "BBBBBBBB", "BBBBBBBB", "B.BB.BB."], x, y,
              {"B": "flame" if not frozen else "ghost", "h": "flame2" if not frozen else "white", "W": "white", "K": "ink0"},
              outline="ink0")
    if carry:
        cv.sprite(["SSS.SSS", "SsS.SsS"], x, y - 6, {"S": carry, "s": "ink1"}, outline="ink0")


def kid(x, y, col, sieve=True):
    cv.sprite(["..KK..", ".SSSS.", ".SESE.", "CCCCCC", ".CCCC.", ".C..C."], x, y,
              {"K": "ink0", "S": "skin", "E": "ink0", "C": col}, outline="ink0")
    if sieve:
        cv.ring(x + 9, y + 6, 4, "brown2"); cv.dot(x + 9, y + 6, "parch0")


yagwang(146, 92, carry="pink")
nick(cv, 150, 76, "나 (야광)", "flame2")
yagwang(178, 70, carry="white")
yagwang(118, 60)
# A thief frozen by a hung sieve, counting holes
SX, SY = 98, 100
cv.line(SX, SY - 12, SX, SY - 6, "brown0")
cv.disc(SX, SY, 6, "brown2"); cv.disc(SX, SY, 5, "brown0")
for j in range(-4, 5, 2):
    for i in range(-4, 5, 2):
        if i * i + j * j < 20:
            cv.dot(SX + i, SY + j, "parch0")
yagwang(84, 104, frozen=True)
cv.text(86, 116, "하나, 둘…", "ghost2", 10, anchor="ma")
for a in range(0, 360, 45):
    cv.dot(87 + 9 * math.cos(math.radians(a)), 107 + 9 * math.sin(math.radians(a)), "flame2")
kid(196, 96, "red2")
nick(cv, 199, 88, "마을 꼬마", "pink")
kid(124, 112, "white")
kid(60, 90, "red2", sieve=False)

# HUD ---------------------------------------------------------------------------------------------
cv.rect(104, 0, 112, 24, "ink0"); cv.frame(104, 0, 112, 24, "gold0")
cv.text(160, 1.5, "훔친 신발", "parch0", 10, anchor="ma")
cv.text(132, 10, "야광 14", "flame2", 12, anchor="ma")
cv.text(160, 10, ":", "parch2", 12, anchor="ma")
cv.text(188, 10, "9 마을", "red2", 12, anchor="ma")
tag(cv, 4, 4, "첫닭까지 2:10")
tag(cv, 4, 18, "명절 · 설날 밤 — 야광이 내려오는 밤", fg="ghost2", edge="night3")
for k, (name, state) in enumerate((("질주", "가능"), ("그림자 숨기", "5초"))):
    x = 4 + k * 66
    cv.rect(x, 162, 62, 14, "ink0"); cv.frame(x, 162, 62, 14, "ink2")
    cv.text(x + 4, 164, name, "parch", 10)
    cv.text(x + 58, 164, state, "moss3" if k == 0 else "parch0", 10, anchor="ra")
cv.rect(140, 162, 176, 14, "ink0"); cv.frame(140, 162, 176, 14, "gold0")
cv.text(228, 164, "신발장 +1 · 꽃신 (처음 훔침) — 18 / 24종", "gold2", 10, anchor="ma")

cv.export("concept-18-io-yagwang.png")
print("saved")
