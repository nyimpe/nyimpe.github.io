"""Concept 31 — short exploration after A Short Hike (climbing Hallasan to the white deer of Baengnokdam)."""
import math
from pix import *

cv = Canvas("teal3", seed=431)
rng = cv.rng

# Sky, sun, sea ----------------------------------------------------------------------------------------------------
cv.vgrad(0, 120, ["teal2", "teal3", "ghost"])
cv.disc(132, 22, 10, "yellow"); cv.disc(132, 22, 7, "white")
for cx, cy in ((70, 52), (160, 44), (300, 66)):
    for k in range(5):
        cv.disc(cx + k * 7 - 14, cy + (k % 2) * 2, 6, "white", ry=3)
cv.rect(0, 120, W, 60, "teal")
for k in range(40):
    cv.rect(rng.randrange(W), rng.randrange(122, 180), rng.randrange(3, 8), 1, "teal2")
cv.sprite(["....W....", "...WW....", "..WWW....", "BBBBBBBBB", ".BBBBBBB."], 20, 136, {"W": "white", "B": "brown"})


# The mountain ------------------------------------------------------------------------------------------------------
PX, PY = 224, 30


def top(x):
    if 208 <= x <= 240:
        return PY
    s = 0.62 if x < PX else 0.95
    return PY + (abs(x - PX) - 16) * s + 3 * math.sin(x * 0.21) + 2 * math.sin(x * 0.57)


for x in range(W):
    y0 = int(top(x))
    for y in range(max(y0, 0), H):
        h = y - y0
        if y < 50:
            col = "white" if (x + y) % 7 else "ghost2"         # snow cap
        elif y < 74:
            col = "tan" if (x * 3 + y) % 9 else "brown2"       # bare upper slopes
        elif y < 120:
            col = "moss2"
        else:
            col = "moss3" if y < 150 else "moss2"
        cv.dot(x, y, col)
    if 50 <= y0 < 54:
        cv.dot(x, y0, "ghost2")
# shoreline
for x in range(70, W):
    yb = int(max(top(x), 150) + 18 + 3 * math.sin(x * 0.1))
    cv.rect(x, yb, 1, H - yb, "parch0")
# forest band
for k in range(26):
    x = rng.randrange(80, 318)
    y = rng.randrange(80, 128)
    if y > top(x) + 4:
        pine(cv, x, y, 10 + rng.randrange(6), dark="moss0", mid="moss", trunk="brown0", seed=k)
# Crater rim and the lake
cv.disc(PX, PY + 1, 16, "brown2", ry=4)
cv.disc(PX, PY + 1, 13, "teal2", ry=2.6)
cv.rect(PX - 6, PY, 8, 1, "teal3")

# Trail: switchbacks from the shore to the rim
trail = [(132, 168), (210, 150), (156, 130), (238, 112), (190, 92), (250, 74), (218, 56), (236, 36)]
for (x0, y0), (x1, y1) in zip(trail, trail[1:]):
    for t in range(0, 101):
        x, y = x0 + (x1 - x0) * t / 100, y0 + (y1 - y0) * t / 100
        cv.dot(x, y, "parch"); cv.dot(x, y + 1, "parch0")

# Characters along the way --------------------------------------------------------------------------------------------
# Hyeongu, the huge friendly turtle that puffs white breath, on the lower switchback
L = Layer(seed=2)
L.disc(176, 154, 15, "moss0", ry=8); L.disc(176, 151, 12, "moss", ry=6)
for k in range(5):
    L.rect(166 + k * 5, 148 + (k % 2), 3, 2, "moss2")
L.disc(193, 152, 5, "moss2", ry=4)
for lx in (166, 184):
    L.rect(lx, 158, 4, 4, "moss2")
L.paste(cv, outline="ink0")
cv.dot(195, 151, "ink0")
for k in range(4):
    cv.disc(200 + k * 5, 148 - k * 3, 2 + k * 0.6, "white")
cv.rect(196, 128, 50, 13, "white"); cv.frame(196, 128, 50, 13, "ink1")
cv.sprite(["W", "WW"], 202, 141, {"W": "white"})
cv.text(221, 129.5, "등에 타렴", "ink1", 10, shadow=None, anchor="ma")

# The player: a child in straw sandals with a walking stick
px, py = 214, 98
cv.sprite(["..KKK..", ".KKKKK.", "..SSS..", "..SES..", ".BBBBB.", "BBBBBBB", ".BBBBB.", "..T.T..", "..Y.Y.."], px, py,
          {"K": "ink1", "S": "skin", "E": "ink0", "B": "red2", "T": "skin0", "Y": "gold"}, outline="ink0")
cv.line(px + 9, py + 2, px + 9, py + 12, "brown0")

# Seocheon-gaek, feathered from face to feet, appears before heavy snow
cv.sprite(["...fff...", "..fFFFf..", ".fFEFEFf.", ".fFFFFFf.", "fFfFfFfFf", "FfFfFfFfF", "fFfFfFfFf", ".FfFfFfF.", "..fF.Ff..",
           "..K...K.."], 257, 48, {"F": "white", "f": "iron2", "E": "ink0", "K": "ink1"}, outline="ink1")
cv.text(262, 40, "서천객", "ink1", 10, shadow="white", anchor="ma")
# Chwimo's giant footprints in the snow
for k in range(3):
    fx, fy = 194 + k * 9, 46 - k * 3
    cv.sprite(["KK.KK", "KKKKK", ".KKK.", ".KKK."], fx, fy, {"K": "ghost"})
cv.text(178, 34, "큰 발자국", "ink1", 10, shadow="white", anchor="ma")
# The white deer at the lake
cv.sprite(["W.W..", ".WW..", ".WWWW", ".WWWW", ".W..W"], PX + 2, PY - 6, {"W": "white"}, outline="ink2")

# HUD -----------------------------------------------------------------------------------------------------------------
cv.rect(4, 4, 92, 30, "ink1"); cv.frame(4, 4, 92, 30, "parch0")
cv.text(9, 6, "짚신", "parch2", 10)
for k in range(5):
    cv.sprite([".YY.", "YKKY", "YYYY", "YKKY", "YYYY", ".YY."], 34 + k * 8, 7, {"Y": "gold2" if k < 3 else "ink3", "K": "gold0" if k < 3 else "ink2"})
cv.text(9, 19, "더 높이 오르려면 짚신", "parch0", 10)
cv.rect(232, 156, 84, 20, "ink1"); cv.frame(232, 156, 84, 20, "parch0")
cv.text(274, 157.5, "한라산", "parch2", 10, anchor="ma")
cv.text(274, 166, "백록담까지 셋째 굽이", "gold2", 10, anchor="ma")

cv.export("concept-31-itch-hike.png")
print("saved")
