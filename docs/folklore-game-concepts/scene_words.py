"""Concept 11 — rule-rewriting word puzzle after Baba Is You (talisman sentences)."""
import math
from pix import *

cv = Canvas("parch", seed=131)
rng = cv.rng
T, OY = 16, 12  # tile size, grid top
COLS, ROWS = 20, 10


def at(c, r):
    return c * T, OY + r * T


LEVEL = [
    "####################",
    "#.........F........#",
    "#.........F.########",
    "#.........F.#.....##",
    "#.........F.D..T..##",
    "#.........F.#.....##",
    "#.........F.#..G..##",
    "#.........F.#G....##",
    "#.........F.########",
    "####################",
]

# Floor and walls ----------------------------------------------------------------------
for r in range(ROWS):
    for c in range(COLS):
        x, y = at(c, r)
        ch = LEVEL[r][c]
        if ch == "#":
            cv.rect(x, y, T, T, "ink1")
            cv.rect(x + 1, y + 1, T - 2, T - 2, "ink2")
            cv.rect(x + 1, y + 1, T - 2, 1, "ink3")
        else:
            cv.rect(x, y, T, T, "parch")
            cv.dot(x, y, "parch0")
            if (c * 7 + r * 3) % 5 == 0:
                cv.dot(x + 5 + (c % 4), y + 7, "parch0")

# Objects -------------------------------------------------------------------------------
flame = ["...O....", "..OYO...", ".OYWYO..", "OYWWWYO.", "OYWWWYO.", ".OOYOO..", "..OOO..."]
ghost = ["..KKKK..", ".KGGGGK.", ".KGEGEK.", "KKGGGGKK", "K.WWWW.K", "..WWWW..", ".WWWWWW.", "..W.W.W."]
for r in range(ROWS):
    for c in range(COLS):
        x, y = at(c, r)
        ch = LEVEL[r][c]
        if ch == "F":
            cv.sprite(flame, x + 4, y + 4, {"O": "red2", "Y": "orange", "W": "gold2"}, outline="red0")
        elif ch == "G":
            cv.sprite(ghost, x + 4, y + 4, {"K": "ink0", "G": "ghost2", "E": "teal", "W": "ghost"}, outline="teal")
            cv.sprite(["W..W", ".WW.", ".WW.", "W..W"], x + 11, y + 1, {"W": "flame"})  # frozen mark
        elif ch == "D":  # the door, open now that its sentence is broken
            cv.rect(x + 2, y + 1, 12, 14, "red0")
            cv.rect(x + 3, y + 2, 4, 12, "red"); cv.rect(x + 9, y + 2, 4, 12, "red")
            for sy in range(y + 4, y + 13, 4):
                cv.dot(x + 4, sy, "gold2"); cv.dot(x + 11, sy, "gold2")
            cv.rect(x + 7, y + 2, 2, 12, "parch")
        elif ch == "T":  # goal talisman
            for a in range(0, 360, 30):
                cv.dot(x + 8 + 8 * math.cos(math.radians(a)), y + 8 + 8 * math.sin(math.radians(a)), "gold2")
            cv.sprite(["YYYYY", "YRRRY", "YYRYY", "YRRRY", "YYRYY", "YRYRY", "YYYYY"], x + 6, y + 4,
                      {"Y": "yellow", "R": "red"}, outline="ink0")

# Signature slip pasted on the inner wall (Dokgak cannot pass a sealed room)
sx, sy = at(12, 6)
cv.rect(sx + 4, sy + 2, 8, 12, "white"); cv.frame(sx + 4, sy + 2, 8, 12, "ink1")
cv.line(sx + 5, sy + 9, sx + 10, sy + 5, "ink0"); cv.line(sx + 6, sy + 11, sx + 10, sy + 9, "ink0")

# Player (scholar) who just pushed "막힘" down out of the door's sentence
px, py = at(3, 3)
cv.sprite([
    "...KKKK...",
    "..KKKKKK..",
    "KKKKKKKKKK",
    "...SSSS...",
    "...SESE...",
    "..WWWWWW..",
    ".WWWWWWWW.",
    "..WWRRWW..",
    "..WW..WW..",
    "..KK..KK..",
], px + 3, py + 3, {"K": "ink0", "S": "skin", "E": "ink0", "W": "white", "R": "red"}, outline="ink0")
cv.sprite(["..B..", "..B..", "BBBBB", ".BBB.", "..B.."], px + 6, py + 15, {"B": "teal2"})  # push arrow

# Word tiles ------------------------------------------------------------------------------
NOUN, IS, PROP = ("red0", "red2", "white"), ("parch2", "ink2", "ink0"), ("gold2", "gold0", "ink0")
words = [
    ((1, 1), "서생", NOUN), ((2, 1), "은", IS), ((3, 1), "나", PROP),
    ((1, 3), "문", NOUN), ((2, 3), "은", IS), ((3, 4), "막힘", PROP),
    ((1, 6), "불", NOUN), ((2, 6), "은", IS), ((3, 6), "뜨거움", PROP),
    ((1, 8), "귀신", NOUN), ((2, 8), "은", IS), ((3, 8), "멈춤", PROP),
    ((6, 6), "부적", NOUN), ((7, 6), "은", IS), ((8, 6), "이김", PROP),
]
for (c, r), word, (bg, edge, ink) in words:
    x, y = at(c, r)
    cv.rect(x + 1, y + 1, T - 2, T - 2, bg)
    cv.frame(x + 1, y + 1, T - 2, T - 2, edge)
    cv.rect(x + 2, y + T - 2, T - 3, 1, "ink1")
    cv.text(x + 8, y + 4.5, word, ink, 10, shadow=None, anchor="ma")
for (c, r) in ((1, 1), (1, 6), (1, 8), (6, 6)):  # active sentences glow
    x, y = at(c, r)
    n = 3
    cv.frame(x, y, T * n, T, "gold")
x, y = at(1, 3)
cv.frame(x, y, T * 2, T, "ink3")

# Bars ----------------------------------------------------------------------------------------
cv.rect(0, 0, W, OY, "ink0")
cv.text(4, 1.5, "글귀 · 셋째 방 — 지귀의 사랑방", "parch2", 10)
cv.text(316, 1.5, "되돌리기 Z · 처음부터 R", "parch0", 10, anchor="ra")
cv.rect(0, OY + ROWS * T, W, H - OY - ROWS * T, "ink0")
cv.text(160, 172.5, "‘문 은 막힘’이 깨졌다 — 이제 문을 지나갈 수 있다", "gold2", 10, anchor="ma")

cv.export("concept-11-word-puzzle.png")
print("saved")
