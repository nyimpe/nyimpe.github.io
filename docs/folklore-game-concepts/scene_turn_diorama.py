"""Concept 43 — turn-based diorama puzzle after Hitman GO (a secret royal inspector slips through a haunted magistrate's office)."""
import math
from pix import *

cv = Canvas("night1", seed=551)
rng = cv.rng
for k in range(60):
    cv.dot(rng.randrange(W), rng.randrange(H), "night2")

# Board slab ---------------------------------------------------------------------------------------------------------
BX0, BY0, BX1, BY1 = 26, 22, 294, 146
cv.rect(BX0 + 4, BY1, BX1 - BX0, 10, "ink0")                      # shadow
cv.rect(BX0, BY0, BX1 - BX0, BY1 - BY0, "parch")
cv.rect(BX0, BY1, BX1 - BX0, 8, "brown")                          # front face
cv.rect(BX0, BY1, BX1 - BX0, 1, "brown2")
for k in range(200):
    cv.dot(rng.randrange(BX0, BX1), rng.randrange(BY0, BY1), "parch0")

# Miniature walls and buildings
cv.rect(BX0, BY0, BX1 - BX0, 4, "brown2"); cv.rect(BX0, BY0 + 4, BX1 - BX0, 1, "brown0")
cv.rect(150, 60, 4, 50, "brown2"); cv.rect(150, 60, 1, 50, "brown0")                  # inner wall
cv.rect(236, 28, 50, 26, "red0"); giwa(cv, 232, 22, 58, 8, roof="ink1", edge="iron0", ridge="ink0")   # dongheon
cv.text(261, 38, "동헌", "parch2", 10, anchor="ma")
for tx, ty in ((96, 50),):  # a tree for the big-faced figure
    cv.disc(tx, ty, 12, "moss", ry=9); cv.disc(tx - 3, ty - 3, 7, "moss2", ry=5); cv.rect(tx - 1, ty + 8, 3, 8, "brown0")

# Nodes and paths ----------------------------------------------------------------------------------------------------
N = {"s": (46, 132), "a": (86, 132), "b": (126, 132), "c": (126, 96), "d": (86, 96), "e": (86, 62), "f": (126, 62),
     "g": (176, 62), "h": (176, 96), "i": (176, 132), "j": (216, 132), "k": (216, 96), "l": (216, 62), "m": (260, 62)}
E = ["sa", "ab", "bc", "cd", "de", "ef", "cf", "fg", "gh", "hi", "bi", "ij", "jk", "kh", "kl", "lg", "lm"]
for a, b in E:
    (x0, y0), (x1, y1) = N[a], N[b]
    cv.line(x0, y0, x1, y1, "brown0"); cv.line(x0, y0 + 1, x1, y1 + 1, "brown0")
for name, (x, y) in N.items():
    cv.disc(x, y, 4, "parch2"); cv.ring(x, y, 4, "brown0")
cv.ring(N["m"][0], N["m"][1], 7, "red2"); cv.ring(N["m"][0], N["m"][1], 8, "red2")
# Footprints of the moves made so far
for a, b in ("sa", "ab"):
    (x0, y0), (x1, y1) = N[a], N[b]
    cv.dot((x0 + x1) / 2, (y0 + y1) / 2 - 3, "gold0")


def piece(x, y, rows, cmap, ghost=False):
    rows = ["".join(ch * 2 for ch in r) for r in rows for _ in (0, 1)]   # figurines at 2x
    w = max(len(r) for r in rows)
    y += 2
    cv.disc(x, y + 1, 10, "ink0", ry=3.5)             # base disc shadow
    cv.disc(x, y, 9, "iron2", ry=3)                   # base
    cv.rect(x - 9, y, 19, 1, "iron")
    if ghost:
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch not in ". " and (i + j) % 2 == 0:
                    cv.dot(x - w // 2 + i, y - len(rows) + j, cmap[ch])
    else:
        cv.sprite(rows, x - w // 2, y - len(rows), cmap, outline="ink0")


# The inspector at node b, holding the horse tablet
piece(*N["b"], ["..KKKKK..", ".KKKKKKK.", "...SSS...", "...SES...", "..WWWWW..", ".WWWWWWW.", ".WWGWWWW.", "..WWWWW..",
                "..W...W.."], {"K": "ink0", "S": "skin", "E": "ink0", "W": "white", "G": "gold2"})
# Gwigu: a pair of watchdogs, red and black, guarding on command
for nd, face in (("i", 1), ("h", 0)):
    x, y = N[nd]
    rows = ["R.....", "RRRRR.", "RKRRRR", "RRRRRR", ".R..R."]
    piece(x, y, [r[::-1] for r in rows] if face == 1 else rows, {"R": "red", "K": "ink0"})
    if face == 1:  # looking away toward the next node: approach from behind
        cv.line(x + 12, y - 4, x + 24, y - 4, "red2"); cv.dot(x + 23, y - 5, "red2"); cv.dot(x + 23, y - 3, "red2")
    else:
        cv.line(x + 8, y - 12, x + 8, y - 24, "red2"); cv.dot(x + 7, y - 23, "red2"); cv.dot(x + 9, y - 23, "red2")
cv.text(196, 140, "귀구 한 쌍", "red0", 10, shadow="parch2", anchor="ma")
# Mangryang: barely visible at the edge of a shadow, shown by the mirror
piece(*N["k"], ["..GGG..", ".GGGGG.", "GKGGGKG", ".GGGGG.", "..GGG..", ".G.G.G."], {"G": "ghost", "K": "ink0"}, ghost=True)
cv.text(228, 100, "망량", "teal", 10, shadow="parch2", anchor="la")
cv.sprite(["..III..", ".IWWWI.", "IWWGWWI", "IWWWWWI", ".IWWWI.", "..III..", "...B...", "..BBB.."], N["c"][0] - 3, N["c"][1] - 12,
          {"I": "gold0", "W": "ghost2", "G": "white", "B": "brown0"}, outline="ink0")
cv.text(N["c"][0] + 8, N["c"][1] - 12, "거울", "brown0", 10, shadow="parch2")
# Gogwan-daemyeon: a huge face in a high hat leaning on the tree; vanishes when stared at
piece(*N["e"], ["..KKKK..", "..KKKK..", ".KKKKKK.", ".SSSSSS.", "SSESSESS", "SSSSSSSS", "SSSRRSSS", ".SSSSSS.", "..BBBB.."],
      {"K": "ink0", "S": "skin0", "E": "ink0", "R": "red0", "B": "purple"})
cv.text(N["e"][0] - 12, N["e"][1] - 12, "고관대면", "purple", 10, shadow="parch2", anchor="ra")
# The corrupt magistrate at the dongheon
piece(*N["m"], ["..KKK..", ".KKKKK.", "..SSS..", "..SES..", ".PPPPP.", "PPPPPPP", ".PPPPP."], {"K": "ink0", "S": "skin", "E": "ink0", "P": "purple2"})

# HUD -------------------------------------------------------------------------------------------------------------------
cv.rect(0, 0, W, 14, "ink0")
cv.text(4, 1.5, "암행어사 출두 · 넷째 고을 관아", "parch2", 10)
cv.text(316, 1.5, "2수째", "gold2", 10, anchor="ra")
cv.rect(0, 158, W, 22, "ink0")
goals = ["동헌까지 들키지 않기", "여덟 수 안에", "마패만 보이고 끝내기"]
for k, g in enumerate(goals):
    x = 6 + k * 106
    cv.sprite(["..Y..", ".YYY.", "YYYYY", ".YYY.", ".Y.Y."], x, 164, {"Y": "gold2" if k == 0 else "ink3"})
    cv.text(x + 8, 162, g, "parch2" if k == 0 else "parch0", 10)

cv.export("concept-43-turn-diorama.png")
print("saved")
