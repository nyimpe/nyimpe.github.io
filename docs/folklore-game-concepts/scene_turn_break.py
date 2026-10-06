"""Concept 42 — weakness-break JRPG after Octopath Traveler (eight wanderers of the eight provinces, HD-2D-style layers)."""
import math
from pix import *

cv = Canvas("moss0", seed=541)
rng = cv.rng


def big(rows):
    return ["".join(ch * 2 for ch in r) for r in rows for _ in (0, 1)]


# Layered forest with soft light shafts --------------------------------------------------------------------------------
cv.vgrad(0, 120, ["moss", "moss2", "moss3"])
for k in range(7):  # distant trunks (blurred: dithered)
    x = 20 + k * 46
    cv.dither(x, 10, 10, 100, "moss", "moss2", phase=k)
for k in range(4):  # light shafts
    for j in range(0, 120):
        x = 60 + k * 70 + j * 0.4
        if j % 2 == 0:
            cv.rect(x, j, 8, 1, "parch2" if (k + j // 2) % 2 else "moss3")
cv.rect(0, 112, W, 68, "brown"); cv.rect(0, 112, W, 3, "moss")
for k in range(40):
    cv.dot(rng.randrange(W), rng.randrange(116, 150), "brown2")
# Rock with the deep hole the serpent lives under
L = Layer(seed=2)
L.disc(70, 108, 52, "iron0", ry=26); L.disc(64, 100, 40, "iron", ry=18)
L.paste(cv, outline="ink0")
cv.disc(76, 112, 22, "ink0", ry=10)
# Blurred foreground leaves in the corners (depth of field)
for cx, cy in ((0, 0), (320, 0), (0, 180), (320, 180)):
    for j in range(-40, 41):
        for i in range(-50, 51):
            if (i / 50) ** 2 + (j / 40) ** 2 < 1 and (i + j) % 2 == 0:
                cv.dot(cx + i, cy + j, "moss0")

# Sadu-yeojang: a long serpent body with a roe-deer head --------------------------------------------------------------
pts = [(76 + 40 * math.sin(t * 0.12) + t * 0.6, 112 - t * 1.0) for t in range(60)]
for x, y in pts:
    cv.disc(x, y, 7, "ink0")
for k, (x, y) in enumerate(pts):
    cv.disc(x, y, 6, "teal2" if (k // 3) % 2 else "teal")
    cv.dot(x - 2, y, "teal3")
hx, hy = pts[-1]
L = Layer(seed=3)
L.disc(hx + 4, hy - 4, 9, "tan", ry=7)
L.disc(hx + 12, hy - 1, 5, "tan", ry=4)
for s_ in (-1, 1):
    L.disc(hx + s_ * 5, hy - 12, 2.5, "tan", ry=4)       # ears
L.paste(cv, outline="ink0")
cv.dot(hx + 6, hy - 6, "ink0"); cv.dot(hx + 15, hy - 1, "ink0")
cv.text(82, 128, "사두여장", "parch2", 11, anchor="ma")
# Shield and weakness row
cv.disc(hx + 26, hy - 10, 8, "iron2"); cv.disc(hx + 26, hy - 10, 6, "iron")
cv.text(hx + 26, hy - 15.5, "3", "white", 11, shadow="ink0", anchor="ma")
icons = [(["..I..", "..I..", "..I..", ".III.", "..B.."], {"I": "iron2", "B": "brown2"}, True),   # sword
         (["..I..", ".III.", "..B..", "..B..", "..B.."], {"I": "iron2", "B": "brown2"}, False),  # spear
         ([".B...", "B.S..", "B..S.", "B.S..", ".B..."], {"B": "brown2", "S": "parch2"}, None),   # bow (unknown)
         ([".R.", "ROR", "OYO"], {"R": "red2", "O": "orange", "Y": "gold2"}, True),            # fire
         ([".W.", "WFW", ".W."], {"W": "white", "F": "flame2"}, None),                         # water/ice
         (["GG..", ".GGG", "GG.."], {"G": "moss3"}, None)]                                     # wind
for k, (rows, cmap, known) in enumerate(icons):
    x, y = 112 + k * 11, 128
    cv.rect(x, y, 10, 10, "ink0"); cv.frame(x, y, 10, 10, "gold2" if known else "ink3")
    if known is None:
        cv.text(x + 5, y + 0.5, "?", "ink3", 10, shadow=None, anchor="ma")
    else:
        cv.sprite(rows, x + 2, y + 2, cmap)

# Party of four wanderers on the right ---------------------------------------------------------------------------------
party = [
    ("녹족 부인", ["..KKK..", ".KSSSK.", "..SES..", ".PPPPP.", "PPPPPPP", ".PPPPP.", ".T...T."], {"K": "ink0", "S": "skin", "E": "ink0", "P": "pink", "T": "tan"}, 3),
    ("강수", ["..HHH..", ".HHHHH.", "..SES..", ".WWWWW.", "WWWWWWW", ".WWWWW.", ".K...K."], {"H": "skin0", "S": "skin", "E": "ink0", "W": "parch2", "K": "ink0"}, 1),
    ("장원심", ["..KKK..", "..SSS..", "..SES..", ".BBBBB.", ".BBBBB.", ".BBBBB.", ".K...K."], {"K": "ink0", "S": "skin", "E": "ink0", "B": "brown2"}, 2),
    ("춘천 할미", ["..WWW..", ".WSSSW.", "..SES..", ".GGGGG.", "GGGGGGG", ".GGGGG.", ".K...K."], {"W": "white", "S": "skin", "E": "ink0", "G": "moss3", "K": "ink0"}, 5),
]
for k, (name, rows, cmap, bp) in enumerate(party):
    x, y = 222 + (k % 2) * 34 - k * 4, 100 + k * 8
    cv.sprite(big(rows), x, y, cmap, outline="ink0")
    if k == 3:  # boosting: light gathers
        cv.ring(x + 7, y + 7, 12, "gold2")

# Command menu and status ------------------------------------------------------------------------------------------------
cv.rect(150, 142, 166, 36, "ink0"); cv.frame(150, 142, 166, 36, "parch0")
for k, (name, bp) in enumerate([(p[0], p[3]) for p in party]):
    x, y = 154 + (k % 2) * 82, 145 + (k // 2) * 16
    cv.text(x, y, name, "parch2", 10)
    for j in range(5):
        cv.rect(x + 48 + j * 6, y + 3, 4, 4, "gold2" if j < bp else "ink3")
cv.rect(4, 142, 90, 36, "ink0"); cv.frame(4, 142, 90, 36, "parch0")
for k, c in enumerate(("공격", "능력", "길 행동", "도망")):
    cv.text(14 + (k % 2) * 42, 146 + (k // 2) * 15, c, "gold2" if k == 1 else "parch2", 10)
cv.sprite(["G..", "GG.", "GGG", "GG.", "G.."], 50, 147, {"G": "gold2"})
cv.text(98, 146, "부스트 ×3", "gold2", 10)
cv.text(98, 160, "약점 2/6 발견", "parch2", 10)
cv.rect(0, 0, W, 13, "ink0")
cv.text(4, 1, "팔도 나그네 · 춘천 할미 이야기 2장", "parch2", 10)
cv.text(316, 1, "방패 3 → 0이면 쓰러짐", "gold2", 10, anchor="ra")

cv.export("concept-42-turn-break.png")
print("saved")
