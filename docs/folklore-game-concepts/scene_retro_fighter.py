"""Concept 26 — 2D versus fighter after Street Fighter II (Yeoyongsa vs. the long-armed Jangbiin)."""
import math
from pix import *

cv = Canvas("teal3", seed=281)
rng = cv.rng
FLOOR = 150

# Dano fair stage: mountains, banners, crowd, sand ring ---------------------------------------------
cv.vgrad(0, 120, ["teal2", "teal3", "parch2"])
cv.ridge(86, 18, "moss3", seed=2, freq=1.3, to=120)
cv.ridge(98, 10, "moss2", seed=6, freq=2.2, to=120)
for k, col in enumerate(("red", "flame", "gold", "moss3", "white", "red")):
    x = 14 + k * 54
    cv.rect(x, 54, 2, 52, "brown0")
    cv.rect(x + 2, 56, 12, 30, col); cv.frame(x + 2, 56, 12, 30, "ink1")
for x in range(0, W, 7):  # crowd silhouettes
    h = 10 + (x * 13) % 6
    cv.disc(x + 3, 116 - h, 3, "ink2")
    cv.rect(x, 118 - h, 7, h, "ink2")
cv.rect(0, 118, W, 62, "tan")
cv.disc(160, 150, 150, "parch", ry=22)
cv.ring(160, 150, 148, "brown2", ry=21)
for _ in range(500):
    x, y = rng.randrange(W), rng.randrange(120, 180)
    cv.dot(x, y, rng.choice(("parch0", "tan", "parch2")))

# Yeoyongsa: the strongwoman born from a gourd-sized egg (left) --------------------------------------
L = Layer(seed=3)
fx = 78
L.disc(fx, FLOOR - 52, 7, "skin0", ry=8)  # head (dark complexion)
L.disc(fx - 1, FLOOR - 59, 6, "ink0", ry=3); L.disc(fx - 6, FLOOR - 58, 3, "ink0")  # hair bun
L.rect(fx - 7, FLOOR - 57, 14, 2, "red2")  # headband
L.rect(fx - 9, FLOOR - 44, 18, 16, "white")  # jeogori
L.rect(fx - 9, FLOOR - 32, 18, 3, "red")  # sash
for t in range(14):  # forward fist (right arm)
    L.disc(fx + 8 + t, FLOOR - 40 - t * 0.2, 3, "skin0")
L.disc(fx + 23, FLOOR - 43, 4, "skin0")
L.rect(fx - 13, FLOOR - 42, 5, 12, "skin0")  # guard arm
L.disc(fx - 11, FLOOR - 29, 3, "skin0")
L.rect(fx - 10, FLOOR - 29, 9, 20, "teal"); L.rect(fx + 2, FLOOR - 29, 9, 20, "teal")  # baggy pants
L.rect(fx - 14, FLOOR - 10, 12, 10, "teal0"); L.rect(fx + 4, FLOOR - 10, 12, 10, "teal0")
L.rect(fx - 15, FLOOR - 2, 13, 3, "ink1"); L.rect(fx + 4, FLOOR - 2, 13, 3, "ink1")
L.paste(cv, outline="ink0")
cv.rect(fx - 3, FLOOR - 53, 2, 1, "ink0"); cv.rect(fx + 2, FLOOR - 53, 2, 1, "ink0")

# Jangbiin: arms many times a man's height, sleeves trailing (right) -------------------------------
L = Layer(seed=4)
jx = 246
L.disc(jx, FLOOR - 58, 6, "skin", ry=7)
L.rect(jx - 6, FLOOR - 66, 12, 4, "ink0")  # topknot cloth
L.rect(jx - 7, FLOOR - 50, 14, 24, "purple2")  # robe
L.rect(jx - 7, FLOOR - 28, 6, 26, "purple"); L.rect(jx + 1, FLOOR - 28, 6, 26, "purple")
L.rect(jx - 8, FLOOR - 2, 8, 3, "ink1"); L.rect(jx + 1, FLOOR - 2, 8, 3, "ink1")
for t in range(118):  # the stretching arm, nearly across the ring
    x = jx - 8 - t
    y = FLOOR - 44 - 4 * math.sin(t * 0.05)
    L.rect(x, y, 1, 4, "skin")
    if t < 40:  # long trailing sleeve
        L.rect(x, y - 3, 1, 9 - t * 0.1, "purple2")
L.disc(jx - 128, FLOOR - 42, 4, "skin")
L.rect(jx + 6, FLOOR - 48, 10, 4, "purple2")  # other sleeve hanging
L.rect(jx + 14, FLOOR - 48, 4, 30, "purple2")
L.paste(cv, outline="ink0")
cv.rect(jx - 4, FLOOR - 59, 2, 1, "ink0"); cv.rect(jx + 1, FLOOR - 59, 2, 1, "ink0")
for k in range(6):  # impact
    a = math.radians(k * 60 + 15)
    cv.line(jx - 132, FLOOR - 42, jx - 132 + 8 * math.cos(a), FLOOR - 42 + 8 * math.sin(a), "gold2")

# HUD ---------------------------------------------------------------------------------------------------
def health(x, w, frac, rev=False):
    cv.rect(x - 1, 9, w + 2, 8, "ink0")
    cv.rect(x, 10, w, 6, "red0")
    fw = int(w * frac)
    cv.rect(x + (w - fw if rev else 0), 10, fw, 6, "gold2")
    cv.rect(x + (w - fw if rev else 0), 10, fw, 1, "white")


health(20, 120, 0.72)
health(180, 120, 0.41, rev=True)
cv.text(20, 18, "여용사", "parch2", 11)
cv.text(300, 18, "장비인", "parch2", 11, anchor="ra")
cv.rect(146, 4, 28, 22, "ink0"); cv.frame(146, 4, 28, 22, "gold0")
cv.text(160, 6, "68", "gold2", 15, anchor="ma")
for k, won in enumerate((True, False)):
    cv.disc(30 + k * 8, 34, 2.5, "gold2" if won else "ink2")
for k, won in enumerate((False, False)):
    cv.disc(290 - k * 8, 34, 2.5, "gold2" if won else "ink2")
cv.text(160, 40, "팔 늘이기 주먹!", "gold2", 12, anchor="ma")
cv.text(160, 54, "단오 씨름판", "ink1", 10, shadow="parch2", anchor="ma")
cv.rect(20, 168, 80, 4, "ink0"); cv.rect(21, 169, 56, 2, "flame")
cv.text(20, 160, "기운", "flame0", 10, shadow="parch2")
cv.rect(220, 168, 80, 4, "ink0"); cv.rect(221, 169, 30, 2, "flame")
cv.text(300, 160, "기운", "flame0", 10, shadow="parch2", anchor="ra")

cv.export("concept-26-retro-fighter.png")
print("saved")
