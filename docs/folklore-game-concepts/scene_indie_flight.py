"""Concept 26 — flying carry adventure after Owlboy (Ubuma, the feather-armpit hero of Goguryeo)."""
import math
from pix import *

cv = Canvas("teal3", seed=381)
rng = cv.rng

# Sky, clouds, floating crags -----------------------------------------------------------------------------
cv.vgrad(0, H, ["flame0", "teal2", "teal3", "parch2"])
for cx, cy, r in ((40, 30, 22), (250, 20, 26), (180, 150, 30), (60, 150, 24)):
    for k in range(6):
        cv.disc(cx + k * 8 - 20, cy + (k % 2) * 4, r * 0.5, "white", ry=r * 0.28)


def crag(x, y, w, h):
    L = Layer(seed=x)
    for k in range(h):
        half = w / 2 * (1 - k / h) ** 0.7
        L.rect(x + w / 2 - half, y + k, half * 2, 1, "brown" if k > 4 else "moss2")
    L.rect(x + 2, y, w - 4, 3, "moss3")
    L.paste(cv, outline="ink0")
    for k in range(3):
        pine(cv, int(x + 8 + k * (w - 16) / 2), y - 1, 12, dark="moss0", mid="moss", trunk="brown0", seed=x + k)


crag(14, 92, 70, 40)
crag(236, 108, 76, 44)
cv.rect(258, 96, 30, 12, "parch0"); giwa(cv, 254, 88, 38, 8, roof="ink2", edge="iron", ridge="ink1")  # fortress gate

# Yukdeogwi, the giant raptor guarding the sky road
L = Layer(seed=2)
ex, ey = 236, 46
for side in (-1, 1):
    for k in range(22):
        L.rect(ex + side * (6 + k * 1.6) - (1 if side < 0 else 0), ey - 4 + k * 0.5 - (k > 14) * (k - 14) * 0.8, 3, 6 - k * 0.15,
               "brown0" if k % 3 else "brown")
L.disc(ex, ey + 2, 8, "brown", ry=10)
L.disc(ex, ey - 9, 5, "parch2")
L.rect(ex - 7, ey - 9, 4, 2, "gold")
L.paste(cv, outline="ink0")
cv.dot(ex - 2, ey - 10, "ink0")
cv.text(ex, ey - 26, "육덕위", "red2", 11, shadow="white", anchor="ma")
bar(cv, ex - 20, ey - 17, 40, 2, 0.7, "red2")

# Ubuma flies, carrying a hunter who fires the matchlock
L = Layer(seed=3)
ux, uy = 120, 70
L.disc(ux, uy, 5, "skin", ry=6)
L.disc(ux, uy - 5, 5, "ink0", ry=2)
L.rect(ux - 5, uy + 5, 10, 12, "flame")
for side in (-1, 1):  # feathered arms spread as wings
    for k in range(10):
        L.rect(ux + side * (5 + k * 2) - (1 if side < 0 else 0), uy + 4 - k * 0.6, 2, 6 + (k % 3), "white" if k % 2 else "parch0")
L.paste(cv, outline="ink0")
cv.dot(ux - 2, uy - 1, "ink0"); cv.dot(ux + 2, uy - 1, "ink0")
cv.line(ux - 2, uy + 17, ux - 2, uy + 22, "skin"); cv.line(ux + 2, uy + 17, ux + 2, uy + 22, "skin")
cv.sprite(["..BBBB..", ".BBBBBB.", "..SSSS..", "..SESE..", ".TTTTTTI", "TTTTTTTI", ".TT..TT.", ".KK..KK."], ux - 4, uy + 22,
          {"B": "brown0", "S": "skin", "E": "ink0", "T": "brown2", "I": "iron2", "K": "ink0"}, outline="ink0")
for k in range(5):  # shot toward the raptor
    cv.rect(ux + 8 + k * 18, uy + 24 - k * 5, 4, 1, "gold2")
cv.text(ux, uy - 18, "우부마", "flame0", 11, shadow="white", anchor="ma")

# HUD -----------------------------------------------------------------------------------------------------
cv.rect(0, 0, W, 14, "ink0")
for k in range(5):
    cv.sprite([".R.R.", "RRRRR", ".RRR.", "..R.."], 4 + k * 8, 5, {"R": "red2" if k < 4 else "ink3"})
cv.text(48, 3, "엽전 312", "gold2", 10)
cv.text(316, 3, "졸본 하늘길 · 셋째 구름섬", "parch2", 10, anchor="ra")
cv.rect(0, 156, W, 24, "ink0")
cv.text(6, 160, "업을 동료", "parch0", 10)
for k, (name, col, on) in enumerate((("포수", "brown2", True), ("여용사", "red2", False), ("무당", "purple2", False))):
    x = 58 + k * 62
    cv.rect(x, 158, 58, 18, "ink2" if not on else "flame0"); cv.frame(x, 158, 58, 18, "gold2" if on else "parch0")
    cv.rect(x + 3, 161, 12, 12, col)
    cv.text(x + 18, 160, name, "parch2", 10)
    cv.text(x + 18, 168, ("조총", "던지기", "바람")[k], "gold2" if on else "parch0", 10)
cv.text(316, 164, "동료를 바꿔 업으면 공격이 바뀐다", "parch0", 10, anchor="ra")

cv.export("concept-26-indie-flight.png")
print("saved")
