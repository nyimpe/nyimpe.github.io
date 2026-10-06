"""Concept 25 — falling shooter after Downwell (down the old well, firing red beans from clogs)."""
import math
from pix import *

# Three-colour palette: black, paper white, red
K, Wh, R = "ink0", "parch2", "red2"
cv = Canvas(K, seed=371)
rng = cv.rng
X0, X1 = 104, 216  # well shaft

# Stone well walls ------------------------------------------------------------------------------------------
for y in range(H):
    for x in list(range(X0 - 14, X0)) + list(range(X1, X1 + 14)):
        if (y // 6) % 2 == 0 and x % 7 == 0 or y % 6 == 0:
            cv.dot(x, y, Wh)
for y in range(0, H, 6):
    cv.rect(X0 - 14, y, 14, 1, Wh); cv.rect(X1, y, 14, 1, Wh)
cv.rect(X0, 0, 1, H, Wh); cv.rect(X1 - 1, 0, 1, H, Wh)

# Ledges and an alcove shop where a rock spills rice
for x, y, w in ((X0, 52, 26), (X1 - 34, 96, 34), (X0, 140, 40)):
    cv.rect(x, y, w, 5, Wh); cv.rect(x + 1, y + 1, w - 2, 3, K)
cv.rect(X1, 60, 30, 26, K); cv.frame(X1, 60, 30, 26, Wh)
cv.sprite([".WWW.", "WKKWW", "WWWWW", ".W.W."], X1 + 12, 70, {"W": Wh, "K": K})
for k in range(4):
    cv.dot(X1 + 10 + k * 3, 80, Wh)
cv.text(X1 + 15, 88, "천량", Wh, 10, shadow=None, anchor="ma")

# Enemies in white: a ground-fish bursting from the wall, a drowning-ghost's hand in red
cv.sprite(["...WWWW...", ".WWKWWWWW.", "WWWWWWWWWW", ".WWWWWWW.W", "...WW...WW"], X0 + 2, 74, {"W": Wh, "K": K})
cv.text(X0 + 22, 64, "토어", Wh, 10, shadow=None, anchor="ma")
cv.sprite(["R.R.R", "RRRRR", ".RRR.", ".RRR."], X1 - 10, 120, {"R": R})
for k, (x, y) in enumerate(((150, 40), (180, 116), (132, 112))):  # floating cow-cry spirits (old well)
    cv.sprite([".WWW.", "WKWKW", "WWWWW", "W.W.W"], x, y, {"W": Wh, "K": K})
cv.text(150, 32, "음메…", Wh, 10, shadow=None, anchor="ma")

# Player falling, red beans spraying down from the clogs
px, py = 160, 78
cv.sprite(["..WW..", ".WWWW.", ".WKKW.", "WWWWWW", ".W..W.", "RR..RR"], px - 3, py, {"W": Wh, "K": K, "R": R})
for k in range(6):
    cv.rect(px - 3 + (k % 2) * 6, py + 10 + k * 5, 2, 3, R)
for x, y in ((140, 132), (176, 60), (198, 150), (124, 30), (190, 20)):  # gems (red beans) to collect
    cv.sprite([".R.", "RRR", ".R."], x, y, {"R": R})

# Black dragon's eye opening at the bottom
cv.disc(160, 176, 22, Wh, ry=8); cv.disc(160, 176, 20, K, ry=6); cv.disc(160, 176, 6, R, ry=6); cv.rect(159, 170, 2, 12, K)
cv.text(160, 158, "흑룡", R, 10, shadow=None, anchor="ma")

# HUD -------------------------------------------------------------------------------------------------------
cv.text(52, 8, "우물 아래로", Wh, 12, shadow=None, anchor="ma")
for k in range(4):
    cv.rect(24 + k * 14, 30, 10, 8, R if k < 3 else K); cv.frame(24 + k * 14, 30, 10, 8, R)
cv.text(52, 42, "목숨", Wh, 10, shadow=None, anchor="ma")
cv.rect(40, 60, 24, 90, K); cv.frame(40, 60, 24, 90, Wh)
cv.rect(42, 62 + 36, 20, 86 - 36, R)
cv.text(52, 152, "팥 8 / 14", Wh, 10, shadow=None, anchor="ma")
cv.text(270, 8, "깊이 42장", Wh, 12, shadow=None, anchor="ma")
cv.text(270, 30, "팥알 1,384", R, 11, shadow=None, anchor="ma")
cv.text(270, 50, "밟기 연속 7", Wh, 11, shadow=None, anchor="ma")
cv.text(270, 130, "나막신 · 세 갈래", Wh, 10, shadow=None, anchor="ma")
cv.text(270, 142, "(계룡이 나온 칸에서 얻음)", Wh, 10, shadow=None, anchor="ma")

cv.export("concept-25-indie-well.png")
print("saved")
