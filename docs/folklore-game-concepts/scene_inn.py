"""Concept 3 — cozy ghost-tavern management (side-view interior at night)."""
import math
from pix import *

cv = Canvas("brown0", seed=31)
rng = cv.rng


def blend(a, b, t):
    return tuple(int(a[k] * (1 - t) + b[k] * t) for k in range(3))


def ghostly(rows, x, y, cmap, alpha=0.7):
    """Translucent sprite: mixes with whatever is behind it."""
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch in ". ":
                continue
            under = cv.get(x + i, y + j)
            if under is None:
                continue
            col = P[cmap[ch]]
            t = 1.0 if ch in "KE" else alpha
            cv.dot(x + i, y + j, blend(under, col, t))


# Back wall ---------------------------------------------------------------------
for y in range(13, 122):
    for x in range(W):
        cv.dot(x, y, "tan" if (x * 7 + y * 13) % 17 else "parch0")
cv.dither(0, 13, 320, 12, "brown0", "brown")
for x in range(0, 320, 8):  # rafters
    cv.rect(x, 13, 3, 12, "brown0"); cv.rect(x, 13, 1, 12, "brown2")
cv.rect(0, 25, 320, 3, "brown"); cv.rect(0, 25, 320, 1, "brown2")
cv.rect(0, 102, 320, 3, "brown"); cv.rect(0, 102, 320, 1, "brown2")
for x in (0, 104, 214, 314):
    cv.rect(x, 25, 6, 97, "brown"); cv.rect(x, 25, 1, 97, "brown2"); cv.rect(x + 5, 25, 1, 97, "brown0")

# Window: lattice paper on the left, slid open on the right to the night
wx, wy, ww, wh = 118, 34, 84, 50
cv.rect(wx - 3, wy - 3, ww + 6, wh + 6, "brown0")
cv.vgrad(wy, wy + wh, ["night0", "night1", "night2"], x0=wx + ww // 2, x1=wx + ww)
cv.disc(wx + 66, wy + 13, 6, "parch2"); cv.disc(wx + 68, wy + 12, 5, "white")
cv.ridge(wy + 40, 8, "teal0", seed=5, x0=wx + ww // 2, x1=wx + ww, to=wy + wh)
cv.ridge(wy + 46, 4, "ink0", seed=9, x0=wx + ww // 2, x1=wx + ww, to=wy + wh)
cv.sprite(["..c..", ".cCc.", "cCWCc", "cWWWc", ".cWc."], wx + 50, wy + 26,
          {"c": "flame0", "C": "flame", "W": "flame2"})
for _ in range(10):
    cv.dot(rng.randrange(wx + 44, wx + ww), rng.randrange(wy, wy + 24), "parch")
cv.rect(wx, wy, ww // 2, wh, "parch2")
for gx in range(wx, wx + ww // 2, 7):
    cv.rect(gx, wy, 1, wh, "brown")
for gy in range(wy, wy + wh, 8):
    cv.rect(wx, gy, ww // 2, 1, "brown")
cv.dither(wx + 1, wy + 1, ww // 2 - 1, wh - 1, "parch2", "yellow", phase=1)
for gx in range(wx, wx + ww // 2 + 1, 7):
    cv.rect(gx, wy, 1, wh, "brown")
for gy in range(wy, wy + wh + 1, 8):
    cv.rect(wx, gy, ww // 2, 1, "brown")
cv.rect(wx + ww // 2 - 1, wy - 2, 3, wh + 4, "brown")
cv.rect(wx - 3, wy + wh, ww + 6, 3, "brown2")

# Shelves of onggi jars and liquor bottles
for sy in (44, 72):
    cv.rect(10, sy, 90, 3, "brown"); cv.rect(10, sy, 90, 1, "brown2")
jar = ["..KK..", ".BBBB.", "BBbBBB", "BbBBBB", "BBBBBB", ".BBBB."]
bottle = [".W.", ".W.", "WWW", "WgW", "WWW"]
for k, x in enumerate(range(14, 96, 10)):
    if k % 3 == 2:
        cv.sprite(bottle, x + 2, 39, {"W": "parch2", "g": "parch0"}, outline="ink0")
    else:
        cv.sprite(jar, x, 38, {"K": "ink0", "B": "brown0", "b": "brown2"}, outline="ink0")
for k, x in enumerate(range(14, 96, 12)):
    cv.sprite(["......", "GGGGGG", ".GGGG."] if k % 2 else bottle, x, 67 if k % 2 else 67,
              {"G": "gold", "W": "white", "g": "parch0"}, outline="ink0")

# Hanging meju blocks and red pepper strings from the rafters
for mx in (230, 246, 262):
    cv.rect(mx + 3, 25, 1, 10, "parch0")
    cv.rect(mx, 34, 7, 9, "tan"); cv.dither(mx + 1, 35, 5, 7, "tan", "brown2")
for px_ in (282, 292, 302):
    cv.rect(px_, 25, 1, 4, "parch0")
    for k in range(6):
        cv.rect(px_ - (k % 2), 29 + k * 3, 2, 3, "red" if k % 2 else "red2")

# Lantern glow: warm the wall in two dithered steps
lx, ly = 110, 30
for j in range(28, 102):
    for i in range(60, 160):
        d = math.hypot(i - lx, (j - ly - 6) * 1.2)
        if d < 44 and (d < 28 or (i + j) % 2):
            under = cv.get(i, j)
            cv.dot(i, j, blend(under, P["gold2"], 0.22 if d < 28 else 0.14))
cv.rect(lx, 25, 1, 4, "ink0")
cv.sprite([".KKK.", "TTTTT", "TTYTT", "RRYRR", "RRRRR", ".KKK."], lx - 2, 29,
          {"K": "ink0", "T": "teal2", "Y": "gold2", "R": "red2"}, outline="ink0")

# Floor boards and the kitchen stove --------------------------------------------
for y in range(122, 152):
    for x in range(W):
        cv.dot(x, y, "brown2" if (y - 122) % 6 else "brown")
for y in range(124, 152, 6):
    for x in range((y * 13) % 40, W, 40):
        cv.rect(x, y, 1, 5, "brown")
cv.rect(0, 121, 320, 1, "brown0")

cv.rect(232, 92, 80, 30, "parch0")  # agungi
cv.dither(233, 93, 78, 28, "parch0", "tan")
cv.rect(232, 92, 80, 2, "iron2")
for fx in (246, 286):
    cv.rect(fx - 7, 106, 14, 16, "ink0")
    cv.disc(fx, 116, 6, "orange", ry=5)
    cv.disc(fx, 118, 4, "orange2", ry=3)
    cv.disc(fx, 120, 2, "white", ry=1)
for cx_ in (246, 286):
    cv.disc(cx_, 88, 15, "ink0", ry=7)
    cv.disc(cx_, 86, 14, "iron0", ry=6)
    cv.disc(cx_, 84, 12, "brown0", ry=3)
    cv.disc(cx_ - 2, 84, 8, "brown", ry=2)
    cv.rect(cx_ - 15, 86, 30, 1, "iron")
for k in range(9):  # steam
    sx = 286 + int(3 * math.sin(k * 0.9)) + (k % 3) - 1
    cv.dot(sx, 78 - k * 3, "white"); cv.dot(sx + 1, 77 - k * 3, "parch2")
    sx = 246 + int(3 * math.sin(k * 1.1 + 2))
    cv.dot(sx, 78 - k * 3, "parch2")

# Innkeeper ladling soup
cv.sprite([
    "....KKKK......",
    "...KKKKKK.....",
    "...KKKKKKK....",
    "..KKSSSSKK....",
    "...SSESSS.....",
    "...SSSSSS.....",
    "....SSSS......",
    "..GGGRGGGG....",
    ".GGGGRGGGGGSLL",
    ".GGGGGGGGG..L.",
    ".GGWWWWWWG..L.",
    "..GWWWWWW...L.",
    "..WWWWWWW...L.",
    "..WWWWWWW...L.",
    ".WWWWWWWWW..L.",
    ".WWWWWWWWW....",
    ".WWWWWWWWWW...",
    ".WWWWWWWWWW...",
    "..KK....KK....",
], 268, 98, {"K": "ink0", "S": "skin", "E": "ink0", "G": "moss2", "R": "red2", "W": "parch2", "L": "iron2"},
          outline="ink0", flip=True)

# Guests sit behind low soban tables -------------------------------------------------
# Dokkaebi with a club (loves buckwheat jelly)
cv.sprite([
    "........WW..........",
    ".......WWW..........",
    "....HHHHHHHHH.......",
    "...HHHHHHHHHHH......",
    "..HHRRRRRRRRRHH.....",
    "..HRRRRRRRRRRRH.....",
    ".HHREERRRRREERHH....",
    "..HREKRRRRREKRH.....",
    "..HRRRRRNRRRRRH.....",
    "..HRRRRNNRRRRRH.....",
    "...RWRWRWRWRWR......",
    "...RRRRRRRRRRR...BB.",
    "....RRRRRRRRR...BBBB",
    "..LLLLLLLLLLLLL.BBBB",
    ".LLLKKLLLLLKKLLLRBB.",
    "LLLLLLLLLLLLLLLLRR..",
    "LLLKKLLLLLLKKLLLR...",
    "LLLLLLLLLLLLLLLL....",
    "LLLLLLLLLLLLLLLL....",
    "LLLLLLLLLLLLLLLL....",
], 22, 108, {"W": "parch2", "H": "ink1", "R": "red2", "E": "parch2", "K": "ink0", "N": "red0",
             "L": "orange", "B": "brown"}, outline="ink0")

# White fox sitting in a person's seat
cv.sprite([
    ".W.......W.....",
    ".WW.....WW.....",
    ".WPW...WPW.....",
    ".WWWWWWWWW.....",
    "WWWWWWWWWWW....",
    "WWEKWWWEKWW....",
    "WWWWWWWWWWW....",
    ".WWWWKKWWWW....",
    "..WWWWWWWW.....",
    "...WWWWWW....WW",
    "..WWWWWWWW..WWW",
    ".WWWWWWWWWW.WWg",
    ".WWWWWWWWWWgWWg",
    "WWWWWWWWWWWWWg.",
    "WWWWWWWWWWWWg..",
    "WWWWWWWWWWWW...",
], 100, 113, {"W": "white", "P": "pink", "E": "parch2", "K": "ink0", "g": "ghost"}, outline="ink0")

# Neglected ghost (musagwi) waiting for a ritual meal
ghostly([
    "...KKKKKKKK...",
    "..KKKKKKKKKK..",
    ".KKGGGGGGGGKK.",
    ".KGGGGGGGGGGK.",
    ".KGTEGGGGTEGK.",
    ".KGGGGGGGGGGK.",
    ".KKGGGTTGGGKK.",
    ".KKGGGGGGGGKK.",
    "KKK.GGGGGG.KKK",
    "KK.WWWWWWWW.KK",
    "K.WWWWWWWWWW.K",
    "K.WWWWWWWWWW.K",
    "..WWWWWWWWWW..",
    ".WWWWWWWWWWWW.",
    ".WWWWWWWWWWWW.",
    "WWWWWWWWWWWWWW",
    "WWWWWWWWWWWWWW",
    "WWWWWWWWWWWWWW",
], 172, 110, {"K": "ink0", "G": "ghost2", "T": "teal0", "E": "teal3", "W": "ghost"}, alpha=0.62)

for tx in (34, 110, 182):
    cv.disc(tx, 133, 19, "red0", ry=4)
    cv.disc(tx, 132, 18, "red", ry=3)
    cv.rect(tx - 18, 133, 37, 2, "red0")
    cv.rect(tx - 14, 135, 3, 10, "red0"); cv.rect(tx + 12, 135, 3, 10, "red0")
    cv.rect(tx - 15, 144, 5, 1, "red0"); cv.rect(tx + 11, 144, 5, 1, "red0")
    cv.disc(tx, 148, 18, "ink1", ry=2)
cv.sprite(["GGGGGGGG", ".GBBBBG.", ".GBbbBG.", "GGGGGGGG"], 40, 125, {"G": "gold", "B": "brown2", "b": "tan"}, outline="ink0")
cv.sprite([".WWWWW.", "WMMMMMW", "WMMMMMW", ".WWWWW."], 120, 126, {"W": "parch2", "M": "white"}, outline="ink0")
cv.sprite(["GGGGGGGG", ".G....G.", "..GGGG.."], 188, 127, {"G": "gold0"}, outline="ink0")

# A satisfied ghost rising as light by the window
ghostly([".GGGG.", "GGEGEG", "GGGGGG", ".WWWW.", ".WWWW.", "..WW..", "...W.."], 194, 64,
        {"G": "ghost2", "E": "teal", "W": "ghost"}, alpha=0.45)
for k in range(14):
    cv.dot(188 + rng.randrange(18), 52 + rng.randrange(26), rng.choice(("gold2", "ghost2", "white")))

# Speech bubbles with orders ---------------------------------------------------------
def bubble(x, y, w=18, h=13, tail=6):
    cv.rect(x + 1, y, w - 2, h, "white"); cv.rect(x, y + 1, w, h - 2, "white")
    cv.frame(x, y, w, h, "ink0")
    for c in ((x, y), (x + w - 1, y), (x, y + h - 1), (x + w - 1, y + h - 1)):
        cv.dot(*c, "brown2")
    cv.rect(x + tail, y + h - 1, 3, 1, "white")
    cv.dot(x + tail, y + h, "ink0"); cv.dot(x + tail + 1, y + h, "white"); cv.dot(x + tail + 2, y + h, "ink0")
    cv.dot(x + tail + 1, y + h + 1, "ink0")


bubble(18, 84, 22)
cv.sprite(["..BBBB..", ".BbBBbB.", ".BBBBBB.", "GGGGGGGG", ".GGGGGG."], 25, 87,
          {"B": "brown2", "b": "tan", "G": "gold"})
bar(cv, 20, 100, 18, 1, 0.55, "gold2")

bubble(166, 84, 24)
cv.sprite(["..WWWW..", ".WWWWWW.", "GGGGGGGG", ".GGGGGG.", "..GGGG.."], 174, 87,
          {"W": "white", "G": "gold0"})
bar(cv, 178, 100, 12, 1, 0.3, "purple2")

for hx, hy in ((112, 100), (120, 95), (104, 94)):
    cv.sprite(["P.P", "PPP", ".P."], hx, hy, {"P": "pink"}, outline="red0")

cv.text(170, 97.5, "한", "purple2", 10)
cv.text(176, 26, "성불 +12", "gold2", 10, anchor="ma")

# HUD ------------------------------------------------------------------------------------
cv.rect(0, 0, 320, 13, "ink0"); cv.rect(0, 13, 320, 1, "gold0")
cv.text(5, 1.5, "귀객주막 · 사흘째 밤", "parch2", 11)
cv.disc(140, 6, 4, "parch2"); cv.disc(142, 5, 4, "ink0")
cv.text(148, 1.5, "삼경 (밤 11시)", "parch", 11)
coin(cv, 246, 4, big=True); cv.text(253, 1.5, "340", "gold2", 11)
cv.sprite([".G.", "GWG", ".G."], 280, 5, {"G": "ghost", "W": "white"})
cv.text(286, 1.5, "영험 27", "ghost2", 11)

cv.rect(0, 152, 320, 28, "ink0"); cv.rect(0, 152, 320, 1, "gold0")
cv.text(5, 154.5, "주문", "parch0", 10)
tickets = [("메밀묵", "brown2", 0.55), ("막걸리", "white", 0.9), ("제삿밥", "gold", 0.3)]
for k, (name, col, t) in enumerate(tickets):
    x = 5 + k * 44
    panel(cv, x, 161, 42, 16, fill="parch", edge="brown0", inner="parch2")
    cv.rect(x + 3, 164, 6, 6, col); cv.frame(x + 3, 164, 6, 6, "ink0")
    cv.text(x + 11, 162.5, name, "brown0", 10, shadow=None)
    bar(cv, x + 3, 173, 36, 1, t, "red2" if t < 0.4 else "moss2", bg="parch0", edge="brown")
cv.text(142, 154.5, "재료", "parch0", 10)
ingredients = [("메밀", "tan", 6), ("쌀", "white", 9), ("누룩", "parch0", 3), ("나물", "moss2", 4), ("탕국", "brown2", 2)]
for k, (name, col, n) in enumerate(ingredients):
    x = 142 + k * 26
    panel(cv, x, 161, 24, 16, fill="ink1", edge="parch0", inner="ink2")
    cv.disc(x + 6, 169, 3, col)
    cv.text(x + 11, 162.5, name, "parch", 10)
    cv.text(x + 11, 169, f"x{n}", "gold2", 10)
cv.text(316, 154.5, "오늘 손님", "parch0", 10, anchor="ra")
cv.text(316, 164.5, "5 / 8", "parch2", 12, anchor="ra")

cv.export("concept-3-ghost-inn.png")
print("saved")
