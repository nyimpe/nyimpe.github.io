"""Concept 21 — gourd-bomb arena after Crazy Arcade (gourds burst into magpies; losers get boxed)."""
import math
from pix import *

cv = Canvas("ink1", seed=231)
rng = cv.rng
T, OX, OY, COLS, ROWS = 16, 4, 2, 13, 11


def at(c, r):
    return OX + c * T, OY + r * T


# Board: hard tiled-wall blocks, soft jars and straw ----------------------------------------------
soft = set()
for r in range(ROWS):
    for c in range(COLS):
        x, y = at(c, r)
        cv.rect(x, y, T, T, "tan" if (c + r) % 2 else "parch0")
        if rng.random() < 0.05:
            cv.dot(x + rng.randrange(T), y + rng.randrange(T), "brown2")
        if c % 2 == 1 and r % 2 == 1:  # hard stone-and-tile wall
            cv.rect(x + 1, y + 2, 14, 13, "iron0")
            cv.rect(x + 1, y + 2, 14, 4, "ink1")
            for k in range(3):
                cv.rect(x + 2 + k * 5, y + 3, 3, 2, "ink2")
            cv.rect(x + 2, y + 8, 12, 6, "iron"); cv.rect(x + 2, y + 10, 12, 1, "iron0")
        elif rng.random() < 0.34 and not (c < 3 and r < 3) and not (c > 9 and r > 7):
            soft.add((c, r))
jar = ["..KKKK..", ".BBBBBB.", "BBbBBBBB", "BbBBBBBB", "BBBBBBBB", ".BBBBBB.", "..BBBB.."]
straw = ["..Y.Y.Y.", ".YYYYYY.", "YYyYYyYY", "YYYYYYYY", "YYYrYYYY", ".YYYYYY.", "Y.Y.Y.Y."]
burst_cells = {(6, 4), (6, 3), (6, 2), (6, 5), (6, 6), (5, 4), (4, 4), (7, 4), (8, 4)}
for c, r in soft:
    if (c, r) in burst_cells:
        continue
    x, y = at(c, r)
    if (c * 3 + r) % 2:
        cv.sprite(jar, x + 4, y + 5, {"K": "ink0", "B": "brown0", "b": "brown2"}, outline="ink0")
    else:
        cv.sprite(straw, x + 4, y + 5, {"Y": "gold", "y": "gold0", "r": "brown"}, outline="ink0")

# A gourd bursting into a cross of magpies
for c, r in burst_cells:
    x, y = at(c, r)
    if (c, r) == (6, 4):
        continue
    horizontal = r == 4
    for k in range(2):
        mx, my = x + 3 + k * 7, y + 5 + (k % 2) * 4
        cv.sprite(["K.....", "KKW...", ".KKKKW", "..WW.."] if horizontal else [".K.K.", "KKWKK", ".KKK.", "..W.."], mx, my,
                  {"K": "ink0", "W": "white"})
cx, cy = at(6, 4)
cv.disc(cx + 8, cy + 8, 7, "white"); cv.disc(cx + 8, cy + 8, 5, "gold2")
for a in range(0, 360, 45):
    cv.line(cx + 8, cy + 8, cx + 8 + 9 * math.cos(math.radians(a)), cy + 8 + 9 * math.sin(math.radians(a)), "parch2")

# Placed gourds waiting to burst
gourd = ["..G..", ".GGG.", "..G..", ".GGG.", "GGgGG", "GGGGG", ".GGG."]
for c, r in ((2, 8), (10, 2)):
    x, y = at(c, r)
    cv.sprite(gourd, x + 5, y + 4, {"G": "parch2", "g": "parch0"}, outline="ink0")
    cv.rect(x + 7, y + 2, 1, 2, "moss2")

# Players (children in coloured jackets); one is trapped in a bamboo box
def kid(c, r, col, trapped=False):
    x, y = at(c, r)
    cv.sprite(["..KK..", ".KKKK.", ".SSSS.", ".SESE.", "CCCCCC", ".CCCC.", ".C..C."], x + 5, y + 4,
              {"K": "ink0", "S": "skin", "E": "ink0", "C": col}, outline="ink0")
    if trapped:
        cv.rect(x + 1, y + 1, 14, 15, "moss2")
        cv.dither(x + 2, y + 2, 12, 13, "moss2", "moss0")
        for k in range(x + 2, x + 15, 4):
            cv.rect(k, y + 1, 1, 15, "moss0")
        cv.frame(x + 1, y + 1, 14, 15, "ink0")
        cv.sprite(["..KK..", ".SSSS.", ".SESE."], x + 5, y + 5, {"K": "ink0", "S": "skin", "E": "ink0"})
        for k in range(3):
            cv.line(x - 2 - k, y + 4 + k * 4, x - 4 - k, y + 2 + k * 4, "parch2")


kid(2, 2, "red2")
kid(10, 10, "flame")
kid(11, 6, "gold2", trapped=True)
kid(4, 9, "moss3")
cv.text(at(2, 2)[0] + 8, at(2, 2)[1] - 7, "나", "red2", 10, anchor="ma")

# Items dropped by broken jars
items = [((3, 6), ["..W..", ".WWW.", "WWWWW"], {"W": "white"}), ((8, 8), ["TTT.", "TtTT", ".TTT"], {"T": "tan", "t": "brown2"}),
         ((10, 4), ["..G..", ".GGG.", "..G.."], {"G": "parch2"})]
for (c, r), rows, m in items:
    x, y = at(c, r)
    cv.disc(x + 8, y + 8, 6, "gold2"); cv.disc(x + 8, y + 8, 5, "ink1")
    cv.sprite(rows, x + 6, y + 6, m)

# Right panel -----------------------------------------------------------------------------------------
PX = OX + COLS * T + 4
cv.rect(PX, 0, W - PX, H, "ink0")
cv.text(PX + 50, 3, "뒤웅박 대작전", "gold2", 11, anchor="ma")
cv.text(PX + 50, 14, "2:31", "parch2", 15, anchor="ma")
players = [("나", "red2", "살아 있음"), ("청사초롱", "flame", "살아 있음"), ("노랑저고리", "gold2", "상자 속!"), ("솔잎", "moss3", "살아 있음")]
for k, (name, col, state) in enumerate(players):
    y = 34 + k * 22
    cv.rect(PX + 4, y, 92, 19, "ink1"); cv.frame(PX + 4, y, 92, 19, col)
    cv.sprite([".KK.", "SSSS", "SESE", "CCCC"], PX + 8, y + 6, {"K": "ink0", "S": "skin", "E": "ink0", "C": col})
    cv.text(PX + 18, y + 2, name, "parch2", 10)
    cv.text(PX + 18, y + 10, state, "pink" if "상자" in state else "parch0", 10)
cv.text(PX + 6, 126, "뒤웅박 3 · 까치 4칸", "parch", 10)
cv.text(PX + 6, 136, "신발 2 · 속도 ▲", "parch", 10)
cv.rect(PX + 4, 150, 92, 26, "red0"); cv.frame(PX + 4, 150, 92, 26, "red2")
cv.text(PX + 50, 152, "상자에 갇힌 친구를", "parch2", 10, anchor="ma")
cv.text(PX + 50, 162, "건드려 꺼내 주세요", "parch2", 10, anchor="ma")

cv.export("concept-21-retro-arena.png")
print("saved")
