"""Concept 8 — exorcist squad tactical RPG (grid battle in a village)."""
import math
from pix import *

cv = Canvas("ink1", seed=101)
rng = cv.rng
BX, BY, TW, TH, SIDE = 8, 22, 26, 18, 3
COLS, ROWS = 8, 6

G, D, Wt, Hs, Tr = "g", "d", "w", "h", "t"
MAP = [
    "ggtgdgtg",
    "gggddggg",
    "hggdgggg",
    "gggdggggw"[:8],
    "hggdggww",
    "ghgdgggg",
]


def tile_xy(c, r):
    return BX + c * TW, BY + r * TH


cv.vgrad(0, H, ["ink1", "ink0"])
for r in range(ROWS):
    for c in range(COLS):
        x, y = tile_xy(c, r)
        t = MAP[r][c]
        top, edge = {"g": ("moss", "moss0"), "d": ("tan", "brown"), "w": ("teal", "teal0"),
                     "h": ("moss", "moss0"), "t": ("moss", "moss0")}[t]
        cv.rect(x, y + TH - 1, TW, SIDE + 1, edge)
        cv.rect(x, y, TW, TH - 1, top)
        for _ in range(10):
            cv.dot(x + rng.randrange(TW), y + rng.randrange(TH - 1),
                   {"g": "moss2", "d": "brown2", "w": "teal2", "h": "moss2", "t": "moss2"}[t])
        cv.frame(x, y, TW, TH - 1, "ink1" if t != "w" else "teal0")

# Movement range of the selected monk, and spawn tiles for bean soldiers
sel = (3, 4)
for r in range(ROWS):
    for c in range(COLS):
        if abs(c - sel[0]) + abs(r - sel[1]) <= 2 and MAP[r][c] in "gd" and (c, r) != sel:
            x, y = tile_xy(c, r)
            for j in range(y + 1, y + TH - 2):
                for i in range(x + 1, x + TW - 1):
                    if (i + j) % 2 == 0:
                        cv.dot(i, j, "teal2")
            cv.frame(x + 1, y + 1, TW - 2, TH - 3, "teal3")

# Enemy intent: Singiwonyo's scattered body parts will merge on the marked tile
mx, my = tile_xy(6, 2)
for j in range(my + 1, my + TH - 2):
    for i in range(mx + 1, mx + TW - 1):
        if (i + j) % 2 == 0:
            cv.dot(i, j, "red0")
cv.frame(mx + 1, my + 1, TW - 2, TH - 3, "red2")
parts = {(6, 1): "head", (5, 2): "torso", (7, 2): "arm", (6, 3): "legs"}
for (c, r) in parts:
    x, y = tile_xy(c, r)
    x0, y0, x1, y1 = x + 13, y + 9, mx + 13, my + 9
    for k in range(0, 100, 12):
        t = k / 100
        cv.rect(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, 2, 1, "red2")

# Rat procession (jungseohammi) heading for a house
rat_tiles = [(7, 5), (6, 5), (5, 5), (4, 5)]
path = [(4, 5), (3, 5), (2, 5), (1, 5)]
for (c0, r0), (c1, r1) in zip(path, path[1:]):
    x0, y0 = tile_xy(c0, r0); x1, y1 = tile_xy(c1, r1)
    for k in range(0, 100, 10):
        t = k / 100
        cv.rect(x0 + 13 + (x1 - x0) * t, y0 + 12, 2, 1, "red2")
xa, ya = tile_xy(1, 5)
cv.sprite(["..R", ".RR", "RRR", ".RR", "..R"], xa + 20, ya + 10, {"R": "red2"}, outline="ink0")

# Houses, pines ------------------------------------------------------------------------------
def house(c, r):
    x, y = tile_xy(c, r)
    cv.rect(x + 3, y + 4, 20, 12, "parch0"); cv.rect(x + 3, y + 13, 20, 3, "brown")
    cv.rect(x + 11, y + 9, 4, 7, "brown0")
    cv.disc(x + 13, y + 4, 13, "gold0", ry=6)
    cv.disc(x + 13, y + 3, 12, "gold", ry=5)
    cv.disc(x + 11, y + 2, 7, "gold2", ry=2)
    cv.frame(x + 3, y + 4, 20, 12, "ink0")


def tree(c, r):
    x, y = tile_xy(c, r)
    pine(cv, x + 13, y + 14, 18, dark="moss0", mid="moss2", trunk="brown0", seed=c * 7 + r)


for r in range(ROWS):
    for c in range(COLS):
        if MAP[r][c] == "h":
            house(c, r)
        elif MAP[r][c] == "t":
            tree(c, r)

# Units --------------------------------------------------------------------------------------------
def unit(c, r, rows, cmap, hp=None, foe=False):
    x, y = tile_xy(c, r)
    w = max(len(row) for row in rows)
    h = len(rows)
    cv.disc(x + 13, y + 14, 5, "moss0" if MAP[r][c] != "d" else "brown", ry=1)
    cv.sprite(rows, x + 13 - w // 2, y + 14 - h, cmap, outline="ink0")
    if hp:
        n, m = hp
        for k in range(m):
            cv.rect(x + 13 - m * 2 + k * 4, y + 16, 3, 2, ("red2" if foe else "moss3") if k < n else "ink2")


mudang = ["..KKKK..", ".KKKKKK.", "..SSSS..", "..SESE..", "..SSSS..", ".RRRRRR.", "RRBBBBRR", "RWBBBBWR",
          ".WBBBBW.", ".WWWWWW.", ".WWWWWW.", "..W..W.."]
hunter = ["..BBBB..", ".BBBBBB.", "..SSSS..", "..SESE..", "..SSSS.I", ".TTTTTTI", "TTTTTTI.", "STTTTTI.",
          ".TTTTT..", ".TT.TT..", ".KK.KK.."]
monk = ["..SSSS..", ".SSSSSS.", "..SESE..", "..SSSS..", ".GGGGGG.", "GGGGGGGG", "GgGYGGgG", "GgGYYGgG",
        ".GGGGGG.", ".GG..GG.", ".KK..KK."]
bean_w = [".WW.", "WWWW", "WKKW", ".WW.", "W..W"]
bean_b = [".KK.", "KKKK", "KWWK", ".KK.", "K..K"]
unit(1, 3, mudang, {"K": "ink0", "S": "skin", "E": "ink0", "R": "red", "B": "teal2", "W": "white"}, hp=(4, 4))
unit(1, 1, hunter, {"B": "brown0", "S": "skin", "E": "ink0", "T": "brown2", "I": "iron2", "K": "ink0"}, hp=(3, 4))
unit(4, 3, bean_w, {"W": "white", "K": "ink0"}, hp=(1, 1))
unit(4, 4, bean_w, {"W": "white", "K": "ink0"}, hp=(1, 1))
unit(2, 4, bean_b, {"W": "white", "K": "ink1"}, hp=(1, 1))
sx, sy = tile_xy(*sel)
cv.frame(sx, sy, TW, TH - 1, "gold2"); cv.frame(sx + 1, sy + 1, TW - 2, TH - 3, "gold")
unit(3, 4, monk, {"S": "skin", "E": "ink0", "G": "iron", "g": "iron0", "Y": "gold2", "K": "ink0"}, hp=(4, 5))

ghost = {"P": "ghost", "p": "ghost2", "K": "ink0", "R": "red2"}
unit(6, 1, ["..pppp..", ".pPPPPp.", ".PKPPKP.", ".PPPPPP.", ".PPRRPP.", "..PPPP.."], ghost, hp=(2, 2), foe=True)
unit(5, 2, [".pPPPPp.", "pPPPPPPp", "PPPPPPPP", "PPPPPPPP", ".PPPPPP.", "..PPPP.."], ghost, hp=(3, 3), foe=True)
unit(7, 2, ["pPP.....", ".PPP....", "..PPP...", "...PPPp.", "....PPP."], ghost, hp=(1, 1), foe=True)
unit(6, 3, [".PP..PP.", ".PP..PP.", ".PP..PP.", ".PP..PP.", "PPP..PPP"], ghost, hp=(2, 2), foe=True)
rat = ["..KK...", ".KKKKK.", "KRKKKKK", ".KKKKKK", "..K.K.K"]
for k, (c, r) in enumerate(rat_tiles):
    x, y = tile_xy(c, r)
    cv.sprite(rat, x + 9, y + 6, {"K": "iron0", "R": "red2"}, outline="ink0")
    cv.line(x + 16, y + 10, x + 24, y + 10, "pink")

# Top bar --------------------------------------------------------------------------------------------
cv.rect(0, 0, W, 16, "ink0"); cv.rect(0, 16, W, 1, "gold0")
cv.text(5, 3, "팔도 퇴마군 · 3턴 / 6", "parch2", 11)
cv.text(132, 3, "목표: 초가 3채 지키기", "parch", 11)
for k in range(3):
    cv.rect(236 + k * 7, 5, 5, 6, "gold"); cv.frame(236 + k * 7, 5, 5, 6, "ink2")
cv.text(316, 3, "적 의도 표시 중", "red2", 10, anchor="ra")

# Right panel: selected unit -----------------------------------------------------------------------
panel(cv, 222, 22, 94, 128, fill="ink0", edge="gold0", inner="ink2")
cv.rect(227, 27, 22, 22, "ink2"); cv.frame(227, 27, 22, 22, "parch0")
cv.sprite(["..SSSS..", ".SSSSSS.", "SSESSESS", ".SSSSSS.", "..SSSS..", "GGGGGGGG", "GGGYYGGG"], 234, 34,
          {"S": "skin", "E": "ink0", "G": "iron", "Y": "gold2"})
cv.text(253, 27, "혜통", "gold2", 12)
cv.text(253, 36, "승려 · 이동 2", "parch0", 10)
for k in range(5):
    cv.rect(254 + k * 6, 44, 4, 3, "moss3" if k < 4 else "ink2")
skills = [("콩 뿌리기", "흰콩·검은콩 병사 소환", True), ("금갑장군", "도끼는 공격, 깃발은 아군 강화", False),
          ("염불", "곁의 아군 회복", False)]
for k, (name, desc, on) in enumerate(skills):
    y = 53 + k * 22
    cv.rect(226, y, 86, 20, "ink2" if on else "ink1")
    if on:
        cv.frame(226, y, 86, 20, "gold2")
    cv.text(229, y + 2, name, "parch2" if on else "parch", 10)
    cv.text(229, y + 10.5, desc, "gold2" if on else "ink3", 10)
cv.rect(226, 120, 86, 26, "red0"); cv.frame(226, 120, 86, 26, "red2")
cv.text(229, 121.5, "신기원요", "parch2", 10)
cv.text(229, 129, "다음 턴에 머리·몸통·팔·", "pink", 10)
cv.text(229, 137, "다리가 한 칸에 모인다", "pink", 10)

# Bottom bar ------------------------------------------------------------------------------------------
cv.rect(0, 152, W, 28, "ink0"); cv.rect(0, 152, W, 1, "gold0")
for k, name in enumerate(("이동", "기술", "대기")):
    x = 8 + k * 46
    cv.rect(x, 158, 42, 14, "ink2" if k != 1 else "teal0"); cv.frame(x, 158, 42, 14, "parch0" if k != 1 else "teal3")
    cv.text(x + 21, 159.5, name, "parch2", 11, anchor="ma")
cv.text(150, 156.5, "조각을 떼어 놓으면 합체를 막는다.", "parch0", 10)
cv.text(150, 164.5, "쥐 행렬은 꼬리를 끊으면 흩어진다.", "parch0", 10)
cv.rect(268, 158, 46, 14, "red0"); cv.frame(268, 158, 46, 14, "red2")
cv.text(291, 159.5, "턴 종료", "parch2", 11, anchor="ma")

cv.export("concept-8-tactical-rpg.png")
print("saved")
