"""Concept 23 — block-chain party RPG after Crusaders Quest (three heroes vs. Baekjukmo's mob)."""
import math
from pix import *

cv = Canvas("teal3", seed=351)
rng = cv.rng
G = 112

cv.vgrad(0, G, ["teal2", "teal3", "parch2"])
cv.ridge(70, 14, "moss3", seed=5, freq=1.4, to=G)
cv.ridge(86, 8, "moss2", seed=8, freq=2.2, to=G)
for y in range(G, 134):
    for x in range(W):
        cv.dot(x, y, "moss2" if y < G + 2 else ("tan" if (x * 3 + y) % 7 else "brown2"))


def hero(x, rows, cmap, name, hp):
    w, h = len(rows[0]), len(rows)
    cv.disc(x + w // 2, G + 2, w // 2 + 2, "moss0", ry=2)
    cv.sprite(rows, x, G - h, cmap, outline="ink0")
    bar(cv, x + w // 2 - 9, G - h - 6, 18, 1, hp, "moss3")
    cv.text(x + w // 2, G - h - 16, name, "ink0", 10, shadow="parch2", anchor="ma")


hero(14, ["..KKKK..", ".KRRRRK.", "..SSSS..", "..SESE..", "WWWWWWWW", "SWWWWWWS", "SWRRRRWS", ".TTTTTT.", ".TT..TT.", ".KK..KK."],
     {"K": "ink0", "R": "red2", "S": "skin0", "E": "ink0", "W": "white", "T": "teal"}, "여용사", 0.8)
hero(44, ["W.W.....", ".WW.....", "..LLLL..", "..LELE..", "..LLLL..", "..LLLL..", ".GGGGGG.", "GGGGGGGG", ".GGGGGG.", ".GG..GG."],
     {"W": "parch0", "L": "parch2", "E": "ink0", "G": "iron2"}, "백운거사", 0.6)
hero(74, ["..FFFF..", ".FSSSSF.", ".FSESEF.", "FFFFFFFF", "FfFFFFfF", "F.FFFF.F", "..FFFF..", "..F..F.."],
     {"F": "moss3", "f": "white", "S": "skin", "E": "ink0"}, "비모척", 0.9)

# Baekjukmo's ragged band and their leader Sajang
for k, x in enumerate((196, 220, 244)):
    cv.sprite(["WWWWWW", ".WWWW.", ".KKKK.", ".KEKE.", ".KBBK.", "RRRRRR", "RRRRRR", ".R..R."], x, G - 8 - 2 * (k % 2),
              {"W": "parch2", "K": "ink1", "E": "red2", "B": "ink0", "R": "tan"}, outline="ink0")
    bar(cv, x, G - 14 - 2 * (k % 2), 8, 1, 0.5 + 0.2 * k, "red2")
L = Layer(seed=3)
L.disc(286, G - 20, 14, "purple", ry=18)
L.disc(286, G - 40, 8, "ink1", ry=8)
L.rect(274, G - 52, 24, 4, "parch2")
L.paste(cv, outline="ink0")
cv.rect(283, G - 42, 2, 2, "red2"); cv.rect(289, G - 42, 2, 2, "red2")
cv.text(286, G - 64, "사장", "red2", 10, shadow="parch2", anchor="ma")
cv.text(220, 70, "“밥 내놔라!”", "ink0", 10, shadow="parch2", anchor="ma")

# Skill effect: the strongwoman hurls a great bell (3-chain)
for k in range(10):
    t = k / 9
    cv.dot(30 + t * 180, G - 30 - 40 * math.sin(t * math.pi), "gold2")
cv.sprite(["..GG..", ".GGGG.", ".GGGG.", "GGGGGG", "GgGGgG", "GGGGGG"], 204, 56, {"G": "gold", "g": "gold0"}, outline="ink0")
for x, y, n in ((222, 84, "1,280"), (246, 90, "1,140")):
    cv.text(x, y, n, "white", 11, anchor="ma")
cv.text(120, 36, "큰 종 던지기!", "red2", 15, shadow="white", anchor="ma")

# Block bar ------------------------------------------------------------------------------------------------
cv.rect(0, 134, W, 46, "ink0"); cv.rect(0, 134, W, 1, "gold0")
blocks = [("red2", "R"), ("red2", "R"), ("red2", "R"), ("ink3", "W"), ("moss2", "F"), ("ink3", "W"), ("moss2", "F"), ("red2", "R")]
icons = {"R": ["...GG...", "..GGGG..", "..GGGG..", ".GGGGGG.", ".GGGGGG.", "GGGGGGGG", "GgGGGGgG", "GGGGGGGG"],  # bell
         "W": ["W......W", ".W....W.", "..WWWW..", ".WWEEWW.", ".WWWWWW.", "..WWWW..", "..W..W..", "..W..W.."],  # deer sage
         "F": ["F......F", "FF....FF", "FFF..FFF", "FFFFFFFF", ".FFFFFF.", "..FFFF..", "..F..F..", "..F..F.."]}  # feathers
for k, (col, kind) in enumerate(blocks):
    x = 8 + k * 38
    cv.rect(x, 140, 34, 32, col); cv.frame(x, 140, 34, 32, "ink2")
    cv.rect(x + 1, 141, 32, 2, "white")
    cv.sprite(icons[kind], x + 13, 150, {"G": "gold2", "g": "gold0", "W": "white", "E": "ink0", "F": "white"}, outline="ink0")
cv.frame(6, 138, 3 * 38 + 2, 36, "gold2"); cv.frame(7, 139, 3 * 38, 34, "gold2")
cv.text(64, 162, "3연결", "gold2", 11, anchor="ma")
cv.rect(0, 0, W, 12, "ink0")
cv.text(4, 1.5, "퇴마 일행 · 셋째 고개 3 / 5", "parch2", 10)
cv.text(316, 1.5, "같은 색 블록을 이어 누르면 큰 기술", "parch0", 10, anchor="ra")

cv.export("concept-23-indie-blocks.png")
print("saved")
