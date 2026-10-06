"""Concept 36 — action-gauge RPG after Epic Seven (a tiger-hunting squad pushes back the beast's turn)."""
import math
from pix import *

cv = Canvas("night2", seed=481)
rng = cv.rng

# Snowy forest at dusk -----------------------------------------------------------------------------------------------
cv.vgrad(0, 120, ["night1", "purple", "purple2", "pink"])
cv.ridge(92, 16, "night2", seed=3, freq=1.4)
for k in range(9):
    pine(cv, 20 + k * 36 + rng.randrange(10), 112, 30 + rng.randrange(14), dark="night1", mid="night2", trunk="ink1", seed=k)
cv.rect(0, 112, W, 68, "ghost")
cv.rect(0, 112, W, 2, "white")
for k in range(80):
    cv.dot(rng.randrange(W), rng.randrange(0, 150), "white")


def hunter(x, y, coat, hat, weapon):
    cv.sprite(["...HHHH...", ".HHHHHHHH.", "...SSSS...", "...SESE...", "..CCCCCC..", ".CCCCCCCC.", ".CCCCCCCC.", "..CCCCCC..",
               "..TT..TT..", "..KK..KK.."], x, y, {"H": hat, "S": "skin", "E": "ink0", "C": coat, "T": "brown0", "K": "ink0"},
              outline="ink0")
    if weapon == "gun":
        cv.rect(x + 8, y + 5, 14, 2, "brown0"); cv.rect(x + 16, y + 5, 8, 1, "iron2")
    elif weapon == "spear":
        cv.line(x + 9, y - 6, x + 9, y + 12, "brown2"); cv.sprite(["I", "I", "I"], x + 9, y - 9, {"I": "iron2"})
    elif weapon == "bag":
        cv.rect(x - 3, y + 5, 4, 5, "red")


# Party: father and son gunners, a spearman, a healer ------------------------------------------------------------------
party = [(34, 96, "brown2", "ink1", "gun", "김파총", 0.82), (64, 108, "flame0", "ink1", "gun", "아들", 0.64),
         (28, 124, "red", "ink1", "spear", "창수", 0.9), (60, 138, "parch2", "brown0", "bag", "의원", 1.0)]
for k, (x, y, coat, hat, wpn, name, hp) in enumerate(party):
    if k == 1:  # the acting unit glows
        cv.disc(x + 5, y + 12, 12, "gold2", ry=3)
    hunter(x, y, coat, hat, wpn)
    bar(cv, x - 2, y + 12, 16, 2, hp, "moss3")
# Muzzle fire from the son toward the tiger
cv.sprite([".Y.", "YWY", ".Y."], 89, 111, {"Y": "gold2", "W": "white"})
for k in range(9):
    cv.dot(94 + k * 12, 113 - k * 1, "gold2")

# Cheonmoho: a huge tiger with patchy fur and tough hide ----------------------------------------------------------------
L = Layer(seed=2)
tx, ty = 222, 116
for t in range(26):  # thick tail curling up
    L.disc(tx + 40 + t * 1.0, ty - 6 - t * 1.3 + 4 * math.sin(t * 0.3), 3, "orange")
L.disc(tx, ty, 44, "orange", ry=17)                       # body
for lx in (tx - 34, tx - 16, tx + 14, tx + 32):
    L.rect(lx, ty + 8, 10, 18, "orange")
    L.rect(lx - 1, ty + 24, 12, 3, "parch2")              # paws
L.disc(tx - 50, ty - 10, 18, "orange", ry=16)             # head
for ex_ in (tx - 62, tx - 40):
    L.disc(ex_, ty - 25, 5, "orange")                     # ears
L.paste(cv, outline="ink0")
cv.disc(tx, ty + 9, 36, "parch", ry=6)                    # pale belly
for ex_ in (tx - 62, tx - 40):
    cv.disc(ex_, ty - 25, 2.5, "ink1")
cv.disc(tx - 58, ty - 2, 9, "parch2", ry=6)               # white muzzle
for k in range(10):  # body stripes
    sx = tx - 34 + k * 8
    for j in range(14):
        cv.dot(sx + int(2 * math.sin(j * 0.5)), ty - 15 + j, "ink0")
        cv.dot(sx + 1 + int(2 * math.sin(j * 0.5)), ty - 15 + j, "ink0")
for t in range(0, 26, 5):  # tail stripes
    cv.disc(tx + 40 + t, ty - 6 - t * 1.3 + 4 * math.sin(t * 0.3), 3, "ink0", ry=1)
for k in range(3):  # forehead stripes
    cv.rect(tx - 56 + k * 5, ty - 22, 2, 5, "ink0")
for k in range(70):  # bald patches where the fur is thin
    ang = rng.uniform(0, 6.28); rr = rng.uniform(0, 1)
    cv.dot(tx + 38 * rr * math.cos(ang), ty - 4 + 10 * rr * math.sin(ang), "skin0")
cv.rect(tx - 60, ty - 14, 5, 3, "gold2"); cv.dot(tx - 59, ty - 13, "ink0")
cv.rect(tx - 46, ty - 14, 5, 3, "gold2"); cv.dot(tx - 45, ty - 13, "ink0")
cv.disc(tx - 62, ty + 3, 7, "red0", ry=4)
for t in range(-6, 7, 3):
    cv.dot(tx - 62 + t, ty, "white"); cv.dot(tx - 62 + t, ty + 6, "white")
cv.rect(tx - 58, ty - 6, 3, 2, "ink0")                    # nose
cv.text(tx, 62, "천모호", "red2", 12, anchor="ma")
bar(cv, tx - 50, 78, 100, 4, 0.58, "red2")
cv.text(tx + 52, 75, "가죽 질김", "parch0", 10, anchor="la")
# Heukho waiting behind, eyes like torches
cv.disc(296, 98, 12, "ink1", ry=9)
cv.rect(290, 95, 3, 2, "gold2"); cv.rect(298, 95, 3, 2, "gold2")

# Action gauge with portraits ------------------------------------------------------------------------------------------
cv.rect(0, 0, W, 30, "ink0")
cv.text(6, 1.5, "행동 게이지", "parch2", 10)
GX, GW = 70, 230
cv.rect(GX, 12, GW, 4, "ink2"); cv.rect(GX, 12, GW, 1, "ink3")
cv.rect(GX + GW - 2, 6, 3, 16, "gold2")
icons = [(0.98, "flame0", "아"), (0.71, "brown2", "김"), (0.55, "red", "창"), (0.40, "parch2", "의"), (0.08, "orange", "범"),
         (0.30, "ink1", "흑")]
for frac, col, ch in icons:
    x = GX + int(GW * frac) - 6
    cv.rect(x, 6, 12, 14, col); cv.frame(x, 6, 12, 14, "ink0" if ch != "아" else "gold2")
    cv.text(x + 6, 7.5, ch, "ink0" if col in ("parch2", "orange") else "white", 10, shadow=None, anchor="ma")
cv.line(GX + int(GW * 0.40), 25, GX + int(GW * 0.10), 25, "red2")
cv.dot(GX + int(GW * 0.10) + 1, 24, "red2"); cv.dot(GX + int(GW * 0.10) + 1, 26, "red2")
cv.text(GX + int(GW * 0.42), 21, "징 소리 · 범 -30%", "red2", 10)

# Skills and soul fire -------------------------------------------------------------------------------------------------
cv.rect(150, 150, 170, 30, "ink0")
skills = [("연사", "gold2"), ("징 울리기", "red2"), ("부자 합동 사격", "flame")]
xs = [154, 192, 246]
for (name, col), x in zip(skills, xs):
    w = len(name) * 6 + 10
    cv.rect(x, 154, w, 14, "ink1"); cv.frame(x, 154, w, 14, col)
    cv.text(x + w / 2, 155.5, name, col, 10, anchor="ma")
cv.text(160, 170, "넋 불", "parch0", 10)
for k in range(5):
    cv.sprite([".F.", "FFF", "FWF", ".F."], 186 + k * 8, 170, {"F": "flame" if k < 3 else "ink3", "W": "flame2" if k < 3 else "ink2"})
cv.text(316, 170, "합동 사격: 넋 불 2", "flame2", 10, anchor="ra")

cv.export("concept-36-turn-gauge.png")
print("saved")
