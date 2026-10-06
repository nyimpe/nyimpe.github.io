"""Concept 24 — maze chase after Pac-Man (red-bean porridge; each ghost follows its record)."""
import math
from pix import *

cv = Canvas("night0", seed=261)
rng = cv.rng
T, OX, OY = 8, 52, 12

MAZE = [
    "###########################",
    "#P...........#...........P#",
    "#.###.#####..#..#####.###.#",
    "#.....#...........#.......#",
    "#.###.#.#######.#.#.#####.#",
    "#.....#....#....#.#.....#.#",
    "#####.####.#.####.#.###.#.#",
    "#..........w..............#",
    "#.###.##.#####.#####.##.#.#",
    "#...#.##....H........##.#.#",
    "###.#.#####.###.####.##...#",
    "#.....#...............#####",
    "#.###...#####.#.#####.....#",
    "#P..#.........#.........#P#",
    "#.#.#.#######.#.#######.#.#",
    "#...........#.#...........#",
    "###########################",
]
for r, row in enumerate(MAZE):
    for c, ch in enumerate(row):
        x, y = OX + c * T, OY + r * T
        if ch == "#":
            cv.rect(x, y, T, T, "iron0")
            cv.rect(x + 1, y + 1, T - 2, T - 2, "iron")
            cv.rect(x + 1, y + 1, T - 2, 1, "iron2")
            if (c + r) % 3 == 0:
                cv.rect(x + 2, y + 4, 4, 1, "iron0")
        elif ch == ".":
            cv.rect(x + 3, y + 3, 2, 2, "red0"); cv.dot(x + 3, y + 3, "red2")  # red beans
        elif ch == "P":  # dongji red-bean porridge
            cv.disc(x + 4, y + 5, 4, "parch2", ry=2)
            cv.disc(x + 4, y + 4, 3, "red", ry=2); cv.dot(x + 3, y + 3, "white")
        elif ch == "w":  # a well in the alley
            cv.disc(x + 4, y + 4, 4, "iron2"); cv.disc(x + 4, y + 4, 2, "teal0")
# eaten path behind the player
for c in range(14, 19):
    if MAZE[3][c] != ".":
        continue
    x, y = OX + c * T, OY + 3 * T
    cv.rect(x + 2, y + 2, 4, 4, "night0")

# Player: a round saealsim rice ball, mouth open
px, py = OX + 19 * T + 4, OY + 3 * T + 4
cv.disc(px, py, 4, "white")
for k in range(5):
    cv.line(px, py, px + 4, py - 2 + k, "night0")
cv.dot(px - 1, py - 2, "ink0")

def ghost(c, r, body, eyes="white", name=None, col="white"):
    x, y = OX + c * T - 1, OY + r * T - 1
    cv.sprite(["..BBBB..", ".BBBBBB.", "BBEEBEEB", "BBEKBEKB", "BBBBBBBB", "BBBBBBBB", "B.BB.BB."], x, y,
              {"B": body, "E": eyes, "K": "ink0"}, outline="ink0")
    if name:
        cv.text(x + 4, y - 8, name, col, 10, anchor="ma")


ghost(13, 11, "purple", name="두억시니", col="purple2")
ghost(5, 7, "ghost2", name="착착귀신", col="ghost2")
ghost(22, 3, "red2", name="홍난삼", col="pink")
ghost(11, 7, "teal2", name="물귀신", col="teal3")
for k in range(3):  # Hongnansam flees from a fearless approach
    cv.dot(OX + 23 * T + 2 + k * 3, OY + 3 * T + 3, "pink")
cv.text(OX + 4 * T, OY + 7 * T - 8 + 16, "착 착", "ghost", 10, anchor="ma")
# bonus: dried persimmon
cv.sprite([".G.", "OOO", "OOO", ".O."], OX + 13 * T + 2, OY + 9 * T + 1, {"G": "moss2", "O": "orange"})

# Side panels -------------------------------------------------------------------------------------------
cv.text(26, 14, "1P", "red2", 11, anchor="ma")
cv.text(26, 26, "12,340", "parch2", 11, anchor="ma")
cv.text(26, 48, "최고", "red2", 11, anchor="ma")
cv.text(26, 60, "50,000", "parch2", 11, anchor="ma")
cv.text(26, 90, "남은 새알", "parch0", 10, anchor="ma")
for k in range(3):
    cv.disc(14 + k * 12, 104, 4, "white"); cv.line(14 + k * 12, 104, 18 + k * 12, 102, "night0")
cv.text(26, 130, "3판 · 동짓날", "gold2", 10, anchor="ma")
cv.text(295, 14, "귀신 성미", "gold2", 10, anchor="ma")
notes = [("두억시니", "쫓아온다", "purple2"), ("착착귀신", "소리 뒤 돌진", "ghost2"), ("홍난삼", "다가가면 도망", "pink"),
         ("물귀신", "우물가만 맴돔", "teal3")]
for k, (n, d, col) in enumerate(notes):
    cv.text(295, 30 + k * 22, n, col, 10, anchor="ma")
    cv.text(295, 39 + k * 22, d, "parch0", 10, anchor="ma")
cv.text(295, 130, "팥죽 먹으면", "red2", 10, anchor="ma")
cv.text(295, 139, "모두 달아남", "red2", 10, anchor="ma")
cv.text(160, 156, "팥죽 미로", "gold2", 12, anchor="ma")

cv.export("concept-24-retro-maze.png")
print("saved")
