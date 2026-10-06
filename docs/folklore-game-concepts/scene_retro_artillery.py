"""Concept 20 — turn-based artillery after Fortress 2 (Yeongdeung's wind decides each shot)."""
import math
from pix import *

cv = Canvas("night1", seed=221)
rng = cv.rng

# Sky and destructible hills ---------------------------------------------------------------------
cv.vgrad(0, 140, ["teal2", "teal3", "parch", "parch2"])
cv.disc(260, 34, 12, "parch2"); cv.disc(260, 34, 10, "white")
cv.ridge(100, 16, "parch0", seed=4, freq=1.4, to=140)
cv.ridge(108, 10, "moss3", seed=9, freq=2.0, to=140)


def ground_y(x):
    return int(112 - 22 * math.sin(x * 0.022 + 0.6) - 10 * math.sin(x * 0.061) + 8 * math.sin(x * 0.11))


craters = [(128, 9), (206, 7)]
for x in range(W):
    gy = ground_y(x)
    for y in range(gy, 140):
        if any((x - cx) ** 2 + (y - ground_y(cx)) ** 2 < r * r for cx, r in craters):
            continue
        d = y - gy
        cv.dot(x, y, "moss2" if d < 2 else ("brown2" if d < 8 else ("brown" if (x + y) % 7 else "brown0")))
for _ in range(60):  # grass tufts
    x = rng.randrange(W); cv.dot(x, ground_y(x) - 1, "moss3")

# Units on the ridge ----------------------------------------------------------------------------------
def unit(x, rows, cmap, name, hp, col):
    gy = ground_y(x)
    w, h = len(rows[0]), len(rows)
    cv.sprite(rows, x - w // 2, gy - h, cmap, outline="ink0")
    cv.text(x, gy - h - 13, name, col, 10, anchor="ma")
    bar(cv, x - 10, gy - h - 4, 20, 1, hp, "red2" if hp < 0.4 else "moss3")


crab = ["..R....R..", ".RR....RR.", "..RRRRRR..", ".RrRRRRrR.", "RRRRRRRRRR", ".R.R..R.R."]
conch = ["....PP..", "..PPPPP.", ".PPpPPPP", "PPPPPpPP", ".PPPPPP.", "..BBBB.."]
beast = ["..KKKKK...", ".KKKKKKKI.", "KKOKKKKKKI", "KKKKKKKKK.", ".KK.KK.KK."]
cart = ["...RRRRR", "..RYRYRY", ".RRRRRRR", "BBBBBBB.", ".O...O.."]
unit(36, crab, {"R": "red2", "r": "white"}, "거해", 0.8, "parch2")
unit(102, conch, {"P": "parch", "p": "pink", "B": "brown"}, "고산나봉 (나)", 0.66, "gold2")
unit(236, beast, {"K": "ink1", "O": "orange2", "I": "iron2"}, "불가살이", 0.3, "parch2")
unit(292, cart, {"R": "red", "Y": "gold2", "B": "brown0", "O": "ink1"}, "신기전 화차", 0.55, "parch2")

# Shot arc from my conch, pushed by the wind
x0, y0 = 106, ground_y(102) - 8
vx, vy, wind = 2.6, -2.75, -0.012
x, y = x0, y0
for k in range(70):
    x += vx; y += vy; vx += wind; vy += 0.065
    if k % 3 == 0:
        cv.rect(x, y, 2, 2, "white")
    if y > ground_y(int(x)) - 2:
        break
cv.disc(x, y, 4, "gold2"); cv.ring(x, y, 7, "orange")
for a in range(0, 360, 30):  # sound-wave shell
    cv.dot(x0 + 10 * math.cos(math.radians(a)), y0 + 6 * math.sin(math.radians(a)), "gold2")
for k in range(3):
    cv.line(x0 + 2, y0 - 2, x0 + 14, y0 - 12, "white")

# Yeongdeung descends to set the wind
cv.sprite(["..WWW..", ".WSSSW.", ".WSESW.", "..BBB..", ".BBBBB.", "BBBBBBB", ".B.B.B."], 154, 14,
          {"W": "white", "S": "skin", "E": "ink0", "B": "teal"}, outline="ink0")
for k in range(5):
    cv.line(144 - k * 6, 26 + k, 134 - k * 6, 26 + k, "white")

# HUD -------------------------------------------------------------------------------------------------
cv.rect(0, 140, W, 40, "ink1"); cv.rect(0, 140, W, 1, "gold0")
cv.text(6, 143, "각도 52°", "parch2", 11)
cv.text(6, 155, "고산나봉 · 나팔 포탄", "gold2", 10)
cv.text(6, 165, "지형을 넓게 깎는다", "parch0", 10)
cv.text(116, 143, "힘", "parch0", 10)
bar(cv, 130, 146, 120, 6, 0.72, "orange", bg="ink2", hi="orange2")
for k in range(0, 121, 12):
    cv.rect(130 + k, 153, 1, 2, "ink3")
cv.rect(130 + int(120 * 0.6), 145, 2, 8, "white")  # last shot's power
cv.text(116, 160, "남은 시간 12", "parch", 10)
cv.text(258, 143, "영등바람", "ghost2", 11)
cv.sprite(["...W....", "..WW....", ".WWWWWWW", "..WW....", "...W...."], 262, 157, {"W": "flame2"}, outline="ink0")
cv.text(276, 157, "3", "flame2", 12)
cv.rect(0, 0, W, 12, "ink0")
cv.text(4, 1.5, "영등바람 포격전 · 2 대 2 · 7턴", "parch2", 10)
cv.text(316, 1.5, "비 올 확률 30%", "ghost", 10, anchor="ra")

cv.export("concept-20-retro-artillery.png")
print("saved")
