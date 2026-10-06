"""Concept 5 — one-arrow boss rush (top-down paddy field in a hailstorm)."""
import math
from pix import *

cv = Canvas("night1", seed=71)
rng = cv.rng

# Flooded paddies and raised dikes --------------------------------------------------
for y in range(H):
    for x in range(W):
        cv.dot(x, y, "teal0" if rng.random() > 0.08 else "night2")
def dike(x0, y0, x1, y1):
    for t in range(0, 101):
        x = x0 + (x1 - x0) * t / 100; y = y0 + (y1 - y0) * t / 100
        cv.disc(x, y, 2, "brown0")
    for t in range(0, 101):
        x = x0 + (x1 - x0) * t / 100; y = y0 + (y1 - y0) * t / 100
        cv.dot(x, y, "brown"); cv.dot(x, y - 1, "brown2" if t % 3 else "moss2")


for x0, x1 in ((62, 70), (146, 140), (222, 230), (300, 296)):
    dike(x0, 0, x1, H)
for y0, y1 in ((46, 40), (116, 124)):
    dike(0, y0, W, y1)
for _ in range(500):  # rice seedlings in rows
    x, y = rng.randrange(W), rng.randrange(H)
    if cv.get(x, y) in (P["teal0"], P["night2"]) and x % 6 < 2 and y % 7 < 3:
        cv.dot(x, y, "moss"); cv.dot(x, y - 1, "moss2")
for _ in range(40):  # ripples
    x, y = rng.randrange(W), rng.randrange(H)
    if cv.get(x, y) in (P["teal0"], P["night2"]):
        cv.ring(x, y, rng.randrange(2, 5), "teal", ry=1)

# Gangcheol in the form of an ox: storm and hail ---------------------------------
BX, BY = 212, 66
cv.disc(BX + 2, BY + 30, 40, "night0", ry=8)  # shadow
L = Layer(seed=4)
L.disc(BX, BY + 6, 38, "ink0", ry=22)
L.disc(BX - 2, BY + 2, 34, "ink1", ry=18)
L.disc(BX + 6, BY - 4, 20, "ink2", ry=8)
for lx in (BX - 26, BX - 12, BX + 14, BX + 28):  # legs
    L.rect(lx, BY + 20, 7, 9, "ink0"); L.rect(lx, BY + 27, 7, 3, "iron0")
L.disc(BX - 34, BY + 6, 14, "ink0", ry=12)  # lowered head, charging left
L.disc(BX - 36, BY + 4, 11, "ink1", ry=9)
L.rect(BX - 46, BY + 8, 10, 7, "ink2")  # muzzle
L.dot(BX - 44, BY + 10, "ink0"); L.dot(BX - 40, BY + 10, "ink0")
hx, hy = BX - 36, BY + 4
for side in (-1, 1):  # great crescent horns, sweeping out and curling forward
    for k in range(22):
        t = k / 21
        x = hx + 4 - 16 * t + 6 * t * t
        y = hy + side * (5 + 14 * math.sin(t * 2.2))
        r_ = 2.2 - 1.4 * t
        L.disc(x, y, r_, "parch" if t < 0.75 else "parch2")
        L.dot(x, y + side, "parch0")
L.paste(cv, outline="ink0")
cv.rect(BX - 41, BY + 1, 3, 2, "gold2"); cv.rect(BX - 33, BY + 1, 3, 2, "gold2")
for k in range(9):  # storm-cloud mane boiling along the spine
    cx_ = BX - 22 + k * 7
    cv.disc(cx_, BY - 14 + (k % 2) * 2, 6, "iron", ry=4)
    cv.disc(cx_ - 1, BY - 15 + (k % 2) * 2, 4, "iron2", ry=2)
pts = [(BX - 6, BY - 18), (BX - 2, BY - 8), (BX - 8, BY - 2), (BX - 3, BY + 8)]
for (x0, y0), (x1, y1) in zip(pts, pts[1:]):  # lightning crackling on its back
    cv.line(x0, y0, x1, y1, "gold2"); cv.line(x0 + 1, y0, x1 + 1, y1, "white")

# Charge telegraph toward the archer
PX, PY = 78, 132
for t in range(0, 100, 4):
    tt = t / 100
    x = BX - 50 + (PX + 6 - (BX - 50)) * tt; y = BY + 10 + (PY - 4 - (BY + 10)) * tt
    if (t // 4) % 2 == 0:
        cv.rect(x, y, 2, 2, "red2")
cv.sprite(["R...", "RR..", "RRR.", "RR..", "R..."], PX + 16, PY - 14, {"R": "red2"}, outline="ink0")

# Lightning strike on a paddy
bolt = [(120, 0), (114, 12), (122, 20), (112, 34), (118, 40)]
for (x0, y0), (x1, y1) in zip(bolt, bolt[1:]):
    for o in (-1, 0, 1):
        cv.line(x0 + o, y0, x1 + o, y1, "gold2" if o else "white")
cv.ring(118, 42, 6, "gold2", ry=3); cv.ring(118, 42, 9, "gold0", ry=4)

# The one arrow, stuck in the mud after a miss
cv.line(150, 96, 160, 88, "brown2"); cv.rect(149, 96, 2, 2, "parch")
cv.sprite(["W.", ".W"], 159, 86, {"W": "white"})
for x, y in ((147, 90), (163, 93), (155, 84)):
    cv.dot(x, y, "gold2")

# Archer drawing the bow (holds no arrow: it must be recovered)
cv.disc(PX + 5, PY + 12, 7, "night0", ry=2)
cv.sprite([
    "...KKKKK....",
    ".KKKKRKKKK..",
    "...KSSSK....",
    "...SESES..B.",
    "...SSSSS.B..",
    "..NNNNNNBW..",
    ".SNnNNNnB.W.",
    "..NNNNNNB.W.",
    "..NNRRNN.BW.",
    "..NNNNNN..B.",
    "..NN..NN....",
    "..KK..KK....",
], PX, PY, {"K": "ink0", "R": "red", "S": "skin", "E": "ink0", "N": "teal", "n": "teal0", "B": "brown2", "W": "parch2"},
          outline="ink0")
for k in range(0, 30, 3):  # aim line drifting with the wind
    t = k / 30
    cv.dot(PX + 12 + 70 * t, PY - 2 - 50 * t + 8 * t * t, "white")

# Rain and hail ---------------------------------------------------------------------
for _ in range(260):
    x, y = rng.randrange(-20, W), rng.randrange(H)
    cv.line(x, y, x + 3, y + 6, "teal3" if rng.random() > 0.3 else "teal2")
for _ in range(46):
    x, y = rng.randrange(W), rng.randrange(14, H)
    cv.dot(x + 1, y + 2, "night0")
    cv.rect(x, y, 2, 2, "white"); cv.dot(x + 1, y + 1, "ghost")

# HUD (souls-like: no health bars, just the name) ------------------------------------
cv.text(160, 6, "강 철", "parch2", 12, anchor="ma")
cv.text(160, 15, "소의 형상 · 폭풍과 우박", "ghost", 10, anchor="ma")
cv.rect(116, 23, 88, 1, "parch0")
cv.sprite([".GG.", "G..G", "G..G", ".GG."], 146, 26, {"G": "parch0"})
cv.sprite([".GG.", "GGGG", "GGGG", ".GG."], 170, 26, {"G": "gold2"})
cv.text(144, 25.5, "말", "parch0", 10, anchor="ra")
cv.text(176, 25.5, "소", "gold2", 10)

panel(cv, 4, 154, 120, 22, fill="ink1", edge="parch0", inner="ink2")
cv.sprite(["W......", ".B.....", "..B....", "...B...", "....B.R", ".....RR"], 9, 160, {"W": "parch2", "B": "brown2", "R": "red2"})
cv.text(20, 155.5, "화살 0 / 1", "parch2", 11)
cv.text(20, 164.5, "빗나간 화살을 주워라", "gold2", 10)
cv.text(316, 168.5, "바람 → 화살이 오른쪽으로 밀린다", "ghost", 10, anchor="ra")

cv.export("concept-5-boss-rush.png")
print("saved")
