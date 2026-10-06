"""Concept 19 — roguelike tomb platformer after Spelunky (Deokheung-ri mural beasts wake up)."""
import math
from pix import *

cv = Canvas("ink0", seed=311)
rng = cv.rng
T = 16

# Tomb chambers: stone blocks with a few open rooms ------------------------------------------------
LV = [
    "####################",
    "#......####.......##",
    "#..M...####..M.....#",
    "#......#..........##",
    "###.####..####..####",
    "#......#..#.......##",
    "#..S...#..#..M.....#",
    "#.....##..........##",
    "####################",
]
for r, row in enumerate(LV):
    for c, ch in enumerate(row):
        x, y = c * T, 8 + r * T + 4
        if ch == "#":
            cv.rect(x, y, T, T, "ink2")
            cv.rect(x + 1, y + 1, T - 2, T - 2, "ink3")
            cv.rect(x + 1, y + 1, T - 2, 2, "iron")
            if (c * 7 + r) % 4 == 0:
                cv.rect(x + 4, y + 7, 6, 1, "ink2")
        else:
            cv.rect(x, y, T, T, "ink1")
            if (c + r) % 3 == 0:
                cv.dot(x + 5, y + 9, "ink2")

# Mural panels coming alive: two-headed bird Cheongyang, horned Yeongyang
def mural(c, r, art):
    x, y = c * T + 2, 8 + r * T + 4 + 2
    cv.rect(x - 2, y - 2, 28, 18, "parch0"); cv.rect(x - 1, y - 1, 26, 16, "parch")
    art(x, y)


def two_head_bird(x, y):
    cv.sprite([".R....R.", "RRR..RRR", ".RRRRRR.", "..RRRR..", "..R..R.."], x + 8, y + 3, {"R": "red"})


def seven_horn(x, y):
    cv.sprite(["G.G.G.G", "GGGGGGG", ".BBBBB.", "BBBBBBB", "B.B.B.B"], x + 8, y + 3, {"G": "ink2", "B": "brown2"})


def horse4(x, y):
    cv.sprite(["E.EE.E", ".BBBB.", "BBBBBB", ".B..B."], x + 9, y + 4, {"E": "ink1", "B": "teal"})


mural(3, 2, two_head_bird); mural(13, 2, seven_horn)
# the bird has stepped out of its panel
L = Layer(seed=2)
L.sprite([".RR......RR.", "RRRR....RRRR", ".KRRR..RRRK.", "..RRRRRRRR..", "...RRRRRR...", "....R..R...."], 120, 30,
         {"R": "red2", "K": "ink0"})
L.paste(cv, outline="ink0")
cv.text(126, 22, "청양", "pink", 10, anchor="ma")

# Player: a court painter recording the murals, rope and torch in hand
px, py = 88, 68
cv.sprite(["..KKKK..", "KKKKKKKK", "..SSSS..", "..SESE..", ".TTTTTT.", "TTTTTTTT", ".TT..TT.", ".KK..KK."], px, py,
          {"K": "ink0", "S": "skin", "E": "ink0", "T": "teal2"}, outline="ink0")
cv.line(px + 4, py - 4, px + 4, 20, "tan")  # rope up to the ledge
for r_ in (14, 10):
    for a in range(0, 360, 10):
        x = px + 14 + r_ * math.cos(math.radians(a)); y = py + 2 + r_ * 0.8 * math.sin(math.radians(a))
        if (int(x) + int(y)) % 2:
            cv.dot(x, y, "gold0")
cv.sprite([".Y.", "YOY", ".B.", ".B."], px + 12, py - 2, {"Y": "gold2", "O": "orange", "B": "brown"})

# Three great bees from under the stones chase whoever blasts the auspicious ground
for k, (bx, by) in enumerate(((40, 100), (50, 94), (60, 102))):
    cv.sprite(["W.W", "YKY", "KYK"], bx, by, {"W": "ghost2", "Y": "gold2", "K": "ink0"})
cv.text(50, 84, "삼대봉!", "gold2", 10, anchor="ma")
for k in range(9):  # blast hole in the floor
    cv.dot(70 + k * 2, 132 + (k % 2), "orange")

# Talking skull Nogol keeps the shop
cv.rect(190, 124, 42, 4, "brown"); cv.rect(190, 124, 42, 1, "tan")
cv.sprite([".WWW.", "WKWKW", "WWWWW", ".WRW.", ".W.W."], 176, 110, {"W": "parch2", "K": "ink0", "R": "red2"}, outline="ink0")
cv.text(180, 98, "“질문 하나에 엽전 열 냥”", "parch2", 10, anchor="ma")
for k, (rows, m) in enumerate(((["..T..", "TTTTT", "..T.."], {"T": "tan"}), ([".K.", "KKK", "KKK"], {"K": "ink1"}),
                               (["YYY", "YRY", "YYY"], {"Y": "yellow", "R": "red"}))):
    cv.sprite(rows, 196 + k * 12, 116, m, outline="ink0")
# wooden dolls that grew hair in the grave
cv.sprite([".HHH.", "HSSSH", "HSKSH", ".BBB.", ".B.B."], 268, 120, {"H": "ink0", "S": "tan", "K": "ink1", "B": "brown"}, outline="ink0")

# HUD ----------------------------------------------------------------------------------------------------
cv.rect(0, 0, W, 12, "ink0")
for k in range(4):
    cv.sprite([".R.R.", "RRRRR", ".RRR.", "..R.."], 4 + k * 7, 3, {"R": "red2" if k < 3 else "ink3"})
cv.text(40, 1.5, "화약 2 · 밧줄 3 · 엽전 240", "parch2", 10)
cv.text(316, 1.5, "덕흥리 고분 2-3 · 벽화 기록 4 / 13", "gold2", 10, anchor="ra")
cv.rect(0, 160, W, 20, "ink0")
cv.text(160, 163, "벽을 함부로 부수면 삼대봉이 쫓아온다", "parch0", 10, anchor="ma")

cv.export("concept-19-indie-tomb.png")
print("saved")
