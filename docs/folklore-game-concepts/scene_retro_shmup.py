"""Concept 19 — vertical shooter after 그날이 오면 (ride the giant eagle Yukdeogwi)."""
import math
from pix import *

cv = Canvas("ink0", seed=211)
rng = cv.rng
PX0, PX1 = 88, 232  # playfield

# Playfield: sea under scrolling clouds ------------------------------------------------------
cv.vgrad(0, H, ["teal0", "teal", "teal", "teal0"], x0=PX0, x1=PX1)
for _ in range(90):
    x, y = rng.randrange(PX0, PX1), rng.randrange(H)
    cv.rect(x, y, rng.randrange(3, 9), 1, rng.choice(("teal2", "teal3")))
for cx, cy, r in ((110, 40, 18), (200, 26, 14), (120, 140, 16), (214, 120, 20)):
    for k in range(5):
        cv.disc(cx + k * 6 - 12, cy + (k % 2) * 3, r * 0.6, "parch0", ry=r * 0.35)
    for k in range(5):
        cv.disc(cx + k * 6 - 13, cy + (k % 2) * 3 - 1, r * 0.5, "parch2", ry=r * 0.28)

# Winged-ant soldier formation firing arrows (gyojeonjisang)
ant = [".W.W.", "WAAAW", ".AKA.", ".AAA.", "A.A.A"]
for k in range(7):
    x = 112 + k * 14 + (4 if k % 2 else 0)
    y = 30 + abs(3 - k) * 5
    cv.sprite(ant, x, y, {"W": "ghost2", "A": "ink2", "K": "red2"}, outline="ink0")
for k in range(16):  # arrow volley
    x = 116 + (k * 13) % 96; y = 52 + (k * 7) % 40
    cv.line(x, y, x - 1, y + 4, "parch2"); cv.dot(x - 1, y + 5, "red2")

# Falling star (cheongu-seong) bullets with fire tails
for x, y in ((206, 66), (148, 92), (184, 110)):
    for t in range(8):
        cv.dot(x - t, y - t * 1.4, "orange" if t > 3 else "gold2")
    cv.disc(x, y, 2.5, "gold2"); cv.dot(x, y, "white")

# Mid-boss: red crow with one head and two bodies (jeogo), splitting apart
L = Layer(seed=4)
for bx in (-10, 10):
    L.disc(176 + bx, 18, 9, "red0", ry=6)
    L.disc(176 + bx, 17, 7, "red", ry=4)
    L.line(176 + bx - 8, 16, 176 + bx - 18, 10, "red0"); L.line(176 + bx + 8, 16, 176 + bx + 18, 10, "red0")
L.disc(176, 10, 5, "red2"); L.rect(173, 13, 6, 2, "gold")
L.paste(cv, outline="ink0")
cv.dot(174, 9, "gold2"); cv.dot(178, 9, "gold2")

# Player: archer riding the giant eagle Yukdeogwi
L = Layer(seed=5)
ex, ey = 160, 142
for side in (-1, 1):
    for k in range(14):
        L.rect(ex + side * (4 + k), ey - 2 + k * 0.4, 2, 5 - k * 0.25, "brown" if k % 3 else "brown0")
    L.rect(ex + side * 17, ey + 3, 2, 3, "parch")
L.disc(ex, ey + 2, 5, "brown", ry=8)
L.disc(ex, ey - 6, 3, "parch2")
L.rect(ex - 1, ey - 10, 2, 3, "gold")
L.sprite(["..K..", ".KKK.", ".SSS.", ".TTT."], ex - 2, ey - 4, {"K": "ink0", "S": "skin", "T": "teal2"})
L.paste(cv, outline="ink0")
for k in range(4):  # spread of arrows
    x = ex - 6 + k * 4
    cv.line(x, ey - 22 - k % 2 * 4, x, ey - 14 - k % 2 * 4, "gold2")
cv.disc(ex, ey + 2, 1, "red2")  # hitbox

# Side panels -------------------------------------------------------------------------------------
for x0, x1 in ((0, PX0), (PX1, W)):
    cv.rect(x0, 0, x1 - x0, H, "ink1")
    for y in range(0, H, 8):
        for x in range(x0, x1, 8):
            cv.dot(x + (y // 8 % 2) * 4, y, "ink2")
cv.rect(PX0 - 2, 0, 2, H, "gold0"); cv.rect(PX1, 0, 2, H, "gold0")
cv.text(44, 6, "육덕위", "gold2", 12, anchor="ma")
cv.text(44, 18, "하늘 싸움", "parch", 10, anchor="ma")
cv.text(8, 40, "점수", "parch0", 10)
cv.text(80, 48, "0128400", "parch2", 12, anchor="ra")
cv.text(8, 66, "남은 날개", "parch0", 10)
for k in range(3):
    cv.sprite(["B...B", "BBBBB", ".BBB."], 10 + k * 10, 78, {"B": "brown2"}, outline="ink0")
cv.text(8, 92, "부적 폭탄", "parch0", 10)
for k in range(2):
    cv.sprite(["YYY", "YRY", "YYY", "YRY"], 10 + k * 8, 104, {"Y": "yellow", "R": "red"}, outline="ink0")
cv.text(8, 124, "화살", "parch0", 10)
cv.text(80, 132, "넷 갈래", "gold2", 10, anchor="ra")
cv.text(276, 6, "2면 · 동해", "parch2", 11, anchor="ma")
cv.text(276, 22, "적오", "red2", 10, anchor="ma")
bar(cv, 244, 34, 64, 3, 0.55, "red2", hi="pink")
cv.text(276, 44, "머리 하나 몸 둘", "parch0", 10, anchor="ma")
cv.text(276, 140, "최고 점수", "parch0", 10, anchor="ma")
cv.text(276, 150, "0200000", "parch2", 12, anchor="ma")

cv.export("concept-19-retro-shmup.png")
print("saved")
