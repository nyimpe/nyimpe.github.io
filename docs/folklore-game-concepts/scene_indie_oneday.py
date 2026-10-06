"""Concept 27 — one-minute adventure after Minit (a geunhwacho sprite lives a single day per run)."""
import math
from pix import *

K, Wh, Pk = "ink0", "white", "pink"
cv = Canvas(K, seed=391)
rng = cv.rng
OY = 16

# Monochrome island ------------------------------------------------------------------------------------------
for _ in range(260):  # grass ticks
    x, y = rng.randrange(W), rng.randrange(OY, H)
    cv.dot(x, y, Wh); cv.dot(x + 1, y - 1, Wh)
for y in range(OY, H):  # river
    x = int(200 + 10 * math.sin(y * 0.05))
    cv.rect(x, y, 18, 1, K)
    if y % 5 == 0:
        cv.rect(x + 3 + (y % 3), y, 5, 1, Wh)
    cv.dot(x, y, Wh); cv.dot(x + 17, y, Wh)
cv.rect(196, 96, 28, 8, K); cv.frame(196, 96, 28, 8, Wh)  # bridge
for x in range(198, 222, 4):
    cv.rect(x, 97, 1, 6, Wh)

# Home where every new day begins
cv.sprite(["....WWWW....", "..WWWWWWWW..", ".WWKKKKKKWW.", "WWWWWWWWWWWW", ".W........W.", ".W..WKKW..W.", ".W..W..W..W.",
           ".WWWWWWWWWW."], 30, 40, {"W": Wh, "K": K})
cv.text(36, 70, "집", Wh, 10, shadow=None, anchor="ma")

# Cheollyang rock spilling rice; a creeping mountain that halts when watched
cv.sprite(["..WWWWW...", ".WWKKWWW..", "WWWKKWWWW.", "WWWWWWWWWW", ".WWWWWWWW."], 92, 120, {"W": Wh, "K": K})
for k in range(5):
    cv.dot(102 + k * 3, 127 + (k % 2), Wh)
cv.text(98, 134, "천량", Wh, 10, shadow=None, anchor="ma")
L = Layer(seed=2)
L.disc(270, 74, 30, Wh, ry=34)
L.disc(270, 76, 28, K, ry=32)
L.paste(cv, outline=None)
for k in range(8):
    cv.line(246 + k * 6, 60 + abs(4 - k) * 3, 250 + k * 6, 66 + abs(4 - k) * 3, Wh)
cv.rect(258, 72, 6, 4, Wh); cv.rect(276, 72, 6, 4, Wh); cv.rect(262, 86, 16, 2, Wh)
cv.text(270, 112, "공주산 — 바라보면 멈춘다", Wh, 10, shadow=None, anchor="ma")

# The player: a tiny sprite with a pink geunhwacho bud on its head
px, py = 150, 92
cv.sprite(["..P..", ".PPP.", "..G..", ".WWW.", "WWKWW", ".WWW.", ".W.W."], px, py, {"P": Pk, "G": Wh, "W": Wh, "K": K})
for k in range(4):
    cv.dot(px + 8 + k * 6, py + 4, Wh)  # looking toward the mountain

# An old woman with a hint
cv.sprite(["..WWW..", ".WWWWW.", ".WKWKW.", "..WWW..", ".WWWWW.", "WWWWWWW", ".W...W."], 110, 50, {"W": Wh, "K": K})
cv.rect(124, 36, 70, 16, K); cv.frame(124, 36, 70, 16, Wh)
cv.text(159, 40.5, "해 지면 씨앗만 남지", Wh, 10, shadow=None, anchor="ma")

# HUD: the day ticking away, life stages, seeds kept between days -------------------------------------------
cv.rect(0, 0, W, OY, K); cv.rect(0, OY - 1, W, 1, Wh)
cv.text(6, 1, "0:34", Wh, 15, shadow=None)
stages = ["싹", "잎", "꽃", "씨"]
for k, st in enumerate(stages):
    x = 60 + k * 26
    on = k == 2
    cv.rect(x, 3, 22, 10, Wh if on else K); cv.frame(x, 3, 22, 10, Wh)
    cv.text(x + 11, 4.5, st, K if on else Wh, 10, shadow=None, anchor="ma")
cv.sprite(["P.P", ".P.", "P.P"], 166, 6, {"P": Pk})
cv.text(316, 1.5, "씨앗 3 · 하루 7번째", Wh, 10, shadow=None, anchor="ra")

cv.export("concept-27-indie-oneday.png")
print("saved")
