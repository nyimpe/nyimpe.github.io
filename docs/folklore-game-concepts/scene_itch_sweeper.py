"""Concept 33 — minesweeper RPG after Dragonsweeper (sweeping a haunted house; numbers add up ghost power)."""
import random
from pix import *

cv = Canvas("ink0", seed=451)
rng = random.Random(7)
T, COLS, ROWS = 12, 13, 9
BX, BY = 82, 30

# Ghost types: (name, power, sprite rows, palette)
KINDS = {
    1: ("감서", ["..........", "..........", "..........", "....KK....", "..KGGGK...", ".KGGGGGGK.", "KRGGGGGGGT", ".KKK.KK..T"],
        {"K": "ink0", "G": "iron2", "R": "red2", "T": "pink"}),
    2: ("소귀", ["..........", "...WWWW...", "..WWWWWW..", "..WKWWKW..", "..WWWWWW..", "..WWWWWW..", "..W.WW.W..", ".........."],
        {"W": "ghost2", "K": "ink0"}),
    3: ("청군여귀", ["...WWWW...", "..WWWWWW..", "..WSSSSW..", "..WSKSKW..", "...SSSS...", "..BBBBBB..", ".BBBBBBBB.", "BBBBBBBBBB"],
        {"W": "white", "S": "ghost", "K": "ink0", "B": "flame0"}),
    5: ("귀매면", ["..WWWWWW..", ".WWWWWWWW.", "WWSSSSSSWW", "WSKSSSSKSW", "WSSSSSSSSW", "WSSRRRRSSW", ".WSSSSSSW.", "..W.WW.W.."],
        {"W": "parch2", "S": "skin0", "K": "ink0", "R": "red0"}),
    6: ("대귀", ["..PPPPPP..", ".PPPPPPPP.", "PPYPPPPYPP", "PPPPPPPPPP", "PPPRRRRPPP", "PPPPPPPPPP", "PP.PPPP.PP", "P..P..P..P"],
        {"P": "purple", "Y": "gold2", "R": "red2"}),
    7: ("은불", ["....GG....", "...GGGG...", "...GKGK...", "...GGGG...", "..GGGGGG..", ".GGGGGGGG.", ".GGGGGGGG.", "GGGGGGGGGG"],
        {"G": "iron2", "K": "ink1"}),
    8: ("취생", ["..MMMMM...", ".MMMMMMMM.", "MMYMMMYMMM", "MMMMMMMMMM", ".MMMMMMMMM", "MMMMMMMMM.", ".MM.MMM.M.", "..M..M...."],
        {"M": "moss2", "Y": "gold2"}),
}


def stamp(kind, x, y):
    cv.sprite(KINDS[kind][1], x, y, KINDS[kind][2])


# Haunted room floor ----------------------------------------------------------------------------------------------
for y in range(0, H, 6):
    cv.rect(0, y, W, 6, "brown0" if (y // 6) % 2 else "ink1")
    for x in range(rng.randrange(20), W, 34):
        cv.rect(x, y, 1, 6, "ink0")

# Board ---------------------------------------------------------------------------------------------------------------
monsters = {(6, 4): 13}
pool = [1] * 7 + [2] * 5 + [3] * 4 + [5] * 3 + [6] * 2 + [7] * 2 + [8] * 2
cells = [(c, r) for r in range(ROWS) for c in range(COLS) if (c, r) != (6, 4)]
rng.shuffle(cells)
for (c, r), p in zip(cells, pool):
    monsters[(c, r)] = p
revealed = {(c, r) for r in range(ROWS) for c in range(COLS) if c + abs(r - 4) * 0.6 < 5.2}
defeated = {cell for cell in revealed if cell in monsters}

cv.rect(BX - 3, BY - 3, COLS * T + 6, ROWS * T + 6, "ink0"); cv.frame(BX - 3, BY - 3, COLS * T + 6, ROWS * T + 6, "parch0")
for r in range(ROWS):
    for c in range(COLS):
        x, y = BX + c * T, BY + r * T
        if (c, r) in revealed:
            cv.rect(x, y, T, T, "ink1"); cv.frame(x, y, T, T, "ink0")
            if (c, r) in monsters:
                stamp(monsters[(c, r)], x + 1, y + 2)
                cv.sprite([".G.", "GYG", ".G."], x + 8, y + 8, {"G": "gold0", "Y": "gold2"})  # dropped coin
            else:
                total = sum(monsters.get((c + dc, r + dr), 0) for dc in (-1, 0, 1) for dr in (-1, 0, 1))
                if total:
                    col = "parch2" if total < 5 else ("gold2" if total < 10 else "red2")
                    cv.text(x + T / 2, y + 1.5, str(total), col, 10, shadow=None, anchor="ma")
        else:
            cv.rect(x, y, T, T, "brown"); cv.rect(x, y, T, 1, "brown2"); cv.rect(x, y + T - 1, T, 1, "brown0")
            cv.rect(x + T - 1, y, 1, T, "brown0")
# The master of the house in the middle, wings spilling over its tile
mx, my = BX + 6 * T, BY + 4 * T
cv.rect(mx, my, T, T, "red0")
cv.sprite(["W.........W", "WW.H.H.H.WW", "WWWHHHHHWWW", "WWWHRHRHWWW", ".WWHHHHHWW.", "..WHHHHHW..", "...HH.HH...", "...H...H..."],
          mx - 0, my + 2, {"W": "purple2", "H": "purple0", "R": "red2"}, outline="ink0")
cv.rect(mx + 7, my - 5, 9, 7, "red2"); cv.text(mx + 11.5, my - 5.5, "13", "white", 10, shadow=None, anchor="ma")
# Player marks on hidden tiles, a hint from gathering fireflies, and the cursor
for (c, r), m in (((7, 2), "5"), ((8, 6), "8?")):
    x, y = BX + c * T, BY + r * T
    cv.text(x + T / 2, y + 1.5, m, "ink0", 10, shadow=None, anchor="ma")
fx, fy = BX + 9 * T, BY + 1 * T
for k in range(6):
    cv.dot(fx + rng.randrange(-4, T + 4), fy + rng.randrange(-4, T + 4), "gold2")
cv.dither(fx + 1, fy + 1, T - 2, T - 2, "gold0", "brown")
cx_, cy_ = BX + 5 * T, BY + 3 * T
cv.frame(cx_ - 1, cy_ - 1, T + 2, T + 2, "gold2"); cv.frame(cx_ - 2, cy_ - 2, T + 4, T + 4, "ink0")

# Left panel: the sweeper ---------------------------------------------------------------------------------------------
panel(cv, 4, 30, 72, 112)
rows = ["...KKKK.....", "..KKKKKK....", "...SSSS.....", "...SESE.....", "...SSSS.....", "..WWWWWW..B.", ".WWWWWWWW.B.",
        ".WWWWWWWWSB.", "..WWWWWW..B.", "..TTTTTT.YYY", "..TT..TT.YYY", "..KK..KK.Y.Y"]
big = ["".join(ch * 2 for ch in r) for r in rows for _ in (0, 1)]  # 2x portrait
cv.sprite(big, 28, 34, {"K": "ink0", "S": "skin", "E": "ink0", "W": "parch2", "T": "brown2", "B": "brown0", "Y": "gold"},
          outline="ink0")
cv.text(40, 60, "마당쇠", "parch2", 11, anchor="ma")
cv.text(10, 73, "담력", "parch0", 10)
for k in range(9):
    cv.rect(10 + (k % 5) * 12, 84 + (k // 5) * 9, 9, 6, "red2" if k < 6 else "ink3")
cv.text(10, 103, "레벨 3", "gold2", 10)
cv.text(10, 115, "엽전 14 / 20", "gold2", 10)
cv.text(10, 127, "담력 0까지 버팀", "parch0", 10)

# Right panel: ghost ledger with powers --------------------------------------------------------------------------------
panel(cv, 244, 30, 72, 112)
for k, p in enumerate((1, 2, 3, 5, 6, 7, 8)):
    y = 34 + k * 13
    stamp(p, 248, y)
    cv.text(262, y + 1, KINDS[p][0], "parch2", 10)
    cv.text(311, y + 1, str(p), "gold2", 10, anchor="ra")
cv.sprite(["W......W", "WWH.H.WW", "WWHHHHWW", "WWHRRHWW", ".WHHHHW.", "..H..H.."], 249, 126, {"W": "purple2", "H": "purple0", "R": "red2"})
cv.text(262, 126, "마귀", "red2", 10)
cv.text(311, 126, "13", "red2", 10, anchor="ra")

# Header and rule -----------------------------------------------------------------------------------------------------
cv.rect(0, 0, W, 16, "ink0")
cv.text(160, 2, "흉가 쓸기 · 사랑채", "parch2", 11, anchor="ma")
cv.rect(0, 150, W, 30, "ink0")
cv.text(160, 152, "숫자 = 둘레 여덟 칸 귀신 힘의 합", "gold2", 11, anchor="ma")
cv.text(160, 166, "귀신을 쓸어 담을 때마다 힘만큼 담력이 줄어든다", "parch0", 10, anchor="ma")

cv.export("concept-33-itch-sweeper.png")
print("saved")
