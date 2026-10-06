"""Concept 12 — 49-day afterlife loop after Loop Hero (place land, the dead walk on)."""
import math
from pix import *

cv = Canvas("night0", seed=141)
rng = cv.rng
C, GX, GY = 12, 4, 18


def cell(c, r):
    return GX + c * C, GY + r * C


# Void with faint mist -------------------------------------------------------------------------
for _ in range(500):
    x, y = rng.randrange(0, 232), rng.randrange(14, 140)
    cv.dot(x, y, rng.choice(("night1", "night1", "night2", "teal0")))
for _ in range(25):
    cv.dot(rng.randrange(0, 232), rng.randrange(14, 140), "ghost")

path = [(c, 7) for c in range(3, 13)] + [(12, 6), (12, 5), (13, 5), (14, 5), (15, 5), (15, 4), (15, 3), (15, 2)] \
    + [(c, 2) for c in range(14, 7, -1)] + [(8, 3)] + [(c, 3) for c in range(7, 2, -1)] + [(3, 4), (3, 5), (3, 6)]
for c, r in path:
    x, y = cell(c, r)
    cv.rect(x, y, C, C, "brown0")
    cv.rect(x + 1, y + 1, C - 2, C - 2, "brown")
    cv.dot(x + 3 + (c * 5) % 6, y + 4 + (r * 3) % 5, "brown2")
    cv.dot(x + 7, y + 8, "brown0")

# Placed land tiles ------------------------------------------------------------------------------
def bamboo(c, r, ghostly=False, px=None):
    x, y = px or cell(c, r)
    if ghostly:
        cv.frame(x, y, C, C, "gold2")
        for k in range(0, C, 3):
            cv.dot(x + k, y + 6, "moss2")
        return
    cv.rect(x, y, C, C, "moss0")
    for k in range(4):
        cv.rect(x + 1 + k * 3, y + 1, 1, C - 2, "moss2")
        cv.dot(x + 1 + k * 3, y + 4 + k, "moss3")


def well(c, r, px=None):
    x, y = px or cell(c, r)
    cv.rect(x, y, C, C, "moss0")
    cv.disc(x + 6, y + 6, 5, "iron2"); cv.disc(x + 6, y + 6, 3, "ink0")
    cv.dot(x + 6, y + 6, "teal2")


def grave(c, r, px=None):
    x, y = px or cell(c, r)
    cv.rect(x, y, C, C, "moss0")
    cv.disc(x + 6, y + 7, 5, "moss", ry=4); cv.disc(x + 5, y + 6, 3, "moss2", ry=2)
    cv.rect(x + 5, y + 1, 2, 3, "iron2")


def rock(c, r, px=None):
    x, y = px or cell(c, r)
    cv.rect(x, y, C, C, "ink1")
    cv.disc(x + 6, y + 6, 5, "iron", ry=4); cv.disc(x + 5, y + 5, 3, "iron2", ry=2)
    cv.dot(x + 7, y + 8, "ink0")
    for k in range(3):
        cv.dot(x + 3 + k * 2, y + 10, "white")  # rice spilling from the hole


def pond(c, r, px=None):
    x, y = px or cell(c, r)
    cv.rect(x, y, C, C, "moss0")
    cv.disc(x + 6, y + 6, 5, "teal", ry=4); cv.rect(x + 3, y + 5, 4, 1, "teal3")
    cv.sprite(["WWW.", ".WWW"], x + 5, y + 7, {"W": "white"})


def iron_horse(c, r, px=None):
    x, y = px or cell(c, r)
    cv.rect(x, y, C, C, "moss0")
    cv.sprite(["..II.", "IIII.", ".III.", ".I.I."], x + 3, y + 3, {"I": "iron2"}, outline="ink0")
    if px is None:  # aura that weakens nearby monsters
        cv.ring(x + 6, y + 6, 9, "teal2")


def camp(c, r, px=None):
    x, y = px or cell(c, r)
    cv.rect(x, y, C, C, "brown0")
    cv.disc(x + 6, y + 5, 6, "gold0", ry=3); cv.disc(x + 6, y + 4, 5, "gold", ry=2)
    cv.rect(x + 2, y + 7, 8, 4, "parch0"); cv.rect(x + 5, y + 8, 2, 3, "orange")


for c in (5, 6):
    bamboo(c, 2)
bamboo(4, 2, ghostly=True)
well(13, 6)
grave(7, 8); grave(8, 8); grave(9, 8)
rock(10, 1)
pond(16, 4)
iron_horse(2, 5)
camp(3, 7)

# The dead wanderer and what waits on the road ---------------------------------------------------
hx, hy = cell(10, 7)
cv.sprite(["..WW..", ".WWWW.", ".WSSW.", "WWWWWW", ".WWWW.", ".W..W."], hx + 3, hy + 2,
          {"W": "white", "S": "skin"}, outline="ink0")
bar(cv, hx + 1, hy - 3, 10, 1, 0.68, "red2")
ex, ey = cell(6, 3)
cv.sprite([".KKK.", "KRRRK", "KRSRK", ".RRR.", "RRRRR", "R.R.R"], ex + 3, ey + 3, {"K": "ink0", "R": "red", "S": "parch"},
          outline="ink0")
for c in (8, 9):
    wx, wy = cell(c, 7)
    cv.sprite(["..c..", ".cCc.", "cCWCc", ".cWc."], wx + 4, wy + 4, {"c": "flame0", "C": "flame", "W": "flame2"})
wx, wy = cell(13, 5)
cv.sprite([".WW.", "WWWW", "W..W"], wx + 4, wy + 4, {"W": "teal3"}, outline="ink0")  # well's lowing spirit
cv.text(cell(13, 6)[0] + 6, cell(13, 6)[1] + 12, "음메…", "ghost", 10, anchor="ma")

# Top bar ----------------------------------------------------------------------------------------------
cv.rect(0, 0, W, 13, "ink0"); cv.rect(0, 13, W, 1, "gold0")
cv.text(4, 2, "사십구재 · 셋째 이레 (21일째)", "parch2", 10)
for k in range(7):
    cv.rect(124 + k * 8, 4, 6, 5, "gold" if k < 3 else "ink2")
cv.text(316, 2, "생사귀까지 63%", "red2", 10, anchor="ra")

# Right panel: the dead -------------------------------------------------------------------------------
panel(cv, 236, 16, 80, 124, fill="ink1", edge="parch0", inner="ink2")
cv.text(241, 18.5, "이름 없는 망자", "parch2", 10)
cv.text(241, 27, "넋", "parch0", 10)
bar(cv, 252, 30, 58, 2, 82 / 120, "red2", hi="pink")
cv.text(241, 35, "공덕 340", "gold2", 10)
slots = [(["..G..", ".G.G.", "G...G", ".G.G.", "..G.."], {"G": "brown2"}, "염주"),
         ([".TTT.", "TtTtT", ".TTT."], {"T": "tan", "t": "brown2"}, "짚신"),
         (["RRRRR", ".RRR.", "..B.."], {"R": "red2", "B": "brown2"}, "부채"),
         (["YYY", "YRY", "YYY", "YRY"], {"Y": "yellow", "R": "red"}, "부적")]
for k, (rows, m, name) in enumerate(slots):
    x, y = 241 + (k % 2) * 37, 46 + (k // 2) * 26
    cv.rect(x, y, 34, 22, "ink2"); cv.frame(x, y, 34, 22, "parch0")
    cv.sprite(rows, x + 4, y + 7, m)
    cv.text(x + 20, y + 6, name, "parch", 10)
cv.text(241, 100, "가방", "parch0", 10)
for k in range(6):
    x, y = 241 + (k % 3) * 24, 110 + (k // 3) * 14
    cv.rect(x, y, 22, 12, "ink2"); cv.frame(x, y, 22, 12, "ink3")
    if k < 4:
        cv.rect(x + 8, y + 3, 6, 6, ("gold", "moss2", "teal2", "red")[k])

def jangseung(c, r, px=None):
    x, y = px or cell(c, r)
    cv.rect(x, y, C, C, "moss0")
    for k, col in ((3, "parch"), (7, "parch2")):
        cv.rect(x + k, y + 1, 3, 10, col); cv.dot(x + k, y + 3, "ink0"); cv.dot(x + k + 2, y + 3, "ink0")
        cv.rect(x + k, y + 5, 3, 1, "red" if k == 3 else "teal")


def pagoda_tree(c, r, px=None):
    x, y = px or cell(c, r)
    cv.rect(x, y, C, C, "moss0")
    cv.rect(x + 5, y + 6, 2, 5, "brown0")
    cv.disc(x + 6, y + 5, 5, "moss2", ry=4); cv.disc(x + 5, y + 4, 3, "moss3", ry=2)


# Hand of land cards ------------------------------------------------------------------------------------
cv.rect(0, 142, W, 38, "ink0"); cv.rect(0, 142, W, 1, "gold0")
cards = [("대숲", "moss2"), ("우물", "iron2"), ("무덤", "moss"), ("바위", "iron"), ("연못", "teal2"), ("철마", "iron2"),
         ("장승", "brown2"), ("회나무", "moss3")]
for k, (name, col) in enumerate(cards):
    x = 8 + k * 38
    y = 146 if k else 143
    cv.rect(x, y, 34, 32, "parch0" if k else "gold2")
    cv.rect(x + 1, y + 1, 32, 30, "ink1")
    cv.rect(x + 4, y + 4, 26, 14, "ink2")
    painter = [bamboo, well, grave, rock, pond, iron_horse, jangseung, pagoda_tree][k]
    painter(0, 0, px=(x + 11, y + 5))
    cv.frame(x + 4, y + 4, 26, 14, col)
    cv.text(x + 17, y + 19, name, "parch2", 10, anchor="ma")
cv.line(25, 143, 52, 52, "gold2")  # dragging the bamboo card onto the map

cv.export("concept-12-afterlife-loop.png")
print("saved")
