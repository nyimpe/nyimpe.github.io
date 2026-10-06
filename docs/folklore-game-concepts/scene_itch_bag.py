"""Concept 32 — inventory roguelike after Backpack Hero (a peddler's bundle of strange goods)."""
import math
from pix import *

cv = Canvas("brown0", seed=441)
rng = cv.rng
GX, GY, C, COLS, ROWS = 12, 30, 20, 6, 5

# Road backdrop on the right ------------------------------------------------------------------------------------
cv.vgrad(14, 120, ["teal2", "teal3", "parch2"], x0=150, x1=W)
cv.ridge(92, 12, "moss", seed=3, x0=150)
cv.ridge(104, 8, "moss0", seed=4, x0=150, freq=1.6)
cv.rect(150, 120, 170, 46, "tan")
for k in range(30):
    cv.dot(rng.randrange(150, W), rng.randrange(122, 164), "brown2")
pine(cv, 168, 118, 26, dark="moss0", mid="moss", trunk="brown0", seed=2)

# Bundle cloth behind the grid: a bojagi with patchwork --------------------------------------------------------
cv.rect(0, 14, 150, 166, "red0")
cols = ["red", "purple", "gold0", "teal", "moss"]
for j in range(14, 180, 12):
    for i in range(0, 150, 14):
        cv.rect(i, j, 13, 11, cols[(i // 14 + j // 12) % 5])
cv.rect(GX - 4, GY - 4, COLS * C + 8, ROWS * C + 8, "ink0")
for r in range(ROWS):
    for c in range(COLS):
        x, y = GX + c * C, GY + r * C
        cv.rect(x, y, C, C, "brown"); cv.frame(x, y, C, C, "brown0")
        cv.rect(x + 1, y + 1, C - 2, 1, "brown2")


def cell(c, r):
    return GX + c * C, GY + r * C


def slot(c, r, w, h, edge="gold2"):
    x, y = cell(c, r)
    cv.rect(x + 1, y + 1, w * C - 2, h * C - 2, "brown0")
    cv.frame(x + 1, y + 1, w * C - 2, h * C - 2, edge)
    return x, y


# Pearl's glow on its neighbours (drawn first so items sit on top)
for dc, dr in ((-1, 0), (1, 0), (0, -1), (0, 1)):
    x, y = cell(2 + dc, 2 + dr)
    cv.dither(x + 2, y + 2, C - 4, C - 4, "gold0", "brown")

# Giant ginseng, four cells tall: a root shaped like a person
x, y = slot(0, 0, 1, 4, edge="moss3")
for j in range(46):
    w = 4 + 3 * math.sin(min(j, 40) / 40 * math.pi)
    cv.rect(x + 10 - w / 2, y + 14 + j, w, 1, "parch" if j % 7 else "tan")
for s_ in (-1, 1):
    for t in range(14):  # arms
        cv.rect(x + 10 + s_ * (3 + t * 0.4), y + 30 + t, 2, 1, "parch")
    for t in range(18):  # legs
        cv.rect(x + 10 + s_ * (1 + t * 0.35) - 1, y + 58 + t, 2, 1, "parch")
    cv.line(x + 10 + s_ * 7, y + 76, x + 10 + s_ * 8, y + 79, "parch0")
for k in range(3):
    cv.sprite([".G.", "GGG", ".G."], x + 4 + k * 4, y + 4 + (k % 2) * 3, {"G": "moss2"})
cv.sprite(["R.R", ".R."], x + 8, y + 2, {"R": "red2"})
cv.line(x + 10, y + 8, x + 10, y + 14, "moss")
# Coin string, two cells
x, y = slot(1, 0, 2, 1)
for k in range(5):
    coin(cv, x + 4 + k * 7, y + 7, big=True)
# Pillow with a tiny chicken that wakes you each morning
x, y = slot(3, 0, 2, 1, edge="orange2")
cv.rect(x + 4, y + 9, 32, 8, "brown2"); cv.frame(x + 4, y + 9, 32, 8, "brown0")
cv.sprite(["..RR...", ".WWWW..", "WWKWWY.", "WWWWWW.", ".WWWWW.", "..O.O.."], x + 15, y + 1, {"R": "red2", "W": "white", "K": "ink0", "Y": "orange", "O": "orange"}, outline="ink0")
# Silver knife, two cells tall
x, y = slot(1, 1, 1, 2, edge="iron2")
cv.rect(x + 9, y + 6, 2, 20, "iron2"); cv.rect(x + 9, y + 6, 1, 20, "white")
cv.rect(x + 7, y + 26, 6, 2, "gold"); cv.rect(x + 8, y + 28, 4, 8, "brown2")
# The moon-bright pearl
x, y = slot(2, 2, 1, 1, edge="gold2")
cv.disc(x + 10, y + 10, 5, "ghost2"); cv.disc(x + 9, y + 9, 2, "white")
# Straw sandals
x, y = slot(3, 2, 1, 1)
cv.sprite([".YY.", "YKKY", "YYYY", "YKKY", "YYYY", ".YY."], x + 4, y + 6, {"Y": "gold2", "K": "gold0"})
cv.sprite([".YY.", "YKKY", "YYYY", "YKKY", "YYYY", ".YY."], x + 11, y + 5, {"Y": "gold2", "K": "gold0"})
# White and black beans that turn into little armoured soldiers when they touch
x, y = slot(1, 4, 1, 1)
cv.disc(x + 10, y + 11, 4, "white", ry=3)
cv.sprite(["W", "W"], x + 9, y + 4, {"W": "iron2"})
x, y = slot(2, 4, 1, 1)
cv.disc(x + 10, y + 11, 4, "ink1", ry=3)
cv.sprite(["K", "K"], x + 9, y + 4, {"K": "iron"})
cv.rect(GX + C * 2 - 2, GY + C * 4 + 9, 4, 2, "gold2")  # adjacency spark
# Bamboo box with something thrashing inside: shoves its neighbours
x, y = slot(4, 3, 2, 2, edge="red2")
cv.rect(x + 4, y + 6, 32, 28, "moss3")
for i in range(x + 4, x + 36, 5):
    cv.rect(i, y + 6, 1, 28, "moss")
cv.rect(x + 4, y + 18, 32, 2, "moss")
for k in range(3):
    cv.line(x + 2 - k * 2, y + 10 + k * 6, x - 1 - k * 2, y + 10 + k * 6, "red2")
    cv.line(x + 38 + k * 2, y + 14 + k * 5, x + 41 + k * 2, y + 14 + k * 5, "red2")
cv.sprite(["R.R", ".R."], x + 18, y + 22, {"R": "red2"})

cv.rect(0, 0, W, 14, "ink0")
cv.text(6, 1.5, "봇짐 6×5", "parch2", 10)
cv.text(316, 1.5, "장터 가는 길 · 넷째 고개", "parch2", 10, anchor="ra")

# Tooltip for the pearl
cv.rect(8, 136, 134, 40, "ink1"); cv.frame(8, 136, 134, 40, "gold2")
cv.text(14, 138, "명월주", "gold2", 11)
cv.text(14, 151, "고래 눈에서 떨어진 구슬", "parch0", 10)
cv.text(14, 162, "닿은 칸의 물건 힘 +1", "parch2", 10)

# Battle on the road --------------------------------------------------------------------------------------------
# The peddler: bamboo hat with white cotton tufts, A-frame carrier with a bundle on the back
px, py = 182, 98
L = Layer(seed=7)
for xx in (166, 171):
    L.rect(xx, py - 8, 2, 40, "brown2")
for j in range(py - 4, py + 30, 7):
    L.rect(166, j, 7, 1, "brown0")
L.disc(169, py - 12, 9, "red", ry=7); L.rect(166, py - 20, 6, 3, "red2")   # the bundle on the jige
L.rect(px - 7, py + 6, 15, 18, "parch2")                                  # white coat
L.rect(px - 7, py + 6, 15, 2, "parch0")
L.rect(px - 6, py + 24, 5, 6, "brown"); L.rect(px + 2, py + 24, 5, 6, "brown")
L.rect(px - 6, py + 30, 5, 2, "ink1"); L.rect(px + 2, py + 30, 5, 2, "ink1")
L.disc(px, py, 6, "skin", ry=6)
L.disc(px, py - 6, 12, "ink1", ry=2.5)                                    # hat brim
L.disc(px, py - 9, 5, "ink1", ry=3)
L.rect(px + 7, py + 12, 6, 3, "parch2")                                   # arm thrusting
L.paste(cv, outline="ink0")
for s_ in (-1, 1):
    cv.disc(px + s_ * 12, py - 6, 2.6, "white")                           # cotton tufts
cv.dot(px - 2, py + 1, "ink0"); cv.dot(px + 2, py + 1, "ink0")
cv.rect(px + 13, py + 13, 12, 1, "iron2"); cv.rect(px + 13, py + 12, 10, 1, "white")  # knife thrust
bar(cv, px - 14, py - 22, 30, 3, 0.75, "red2")
cv.text(px, py - 33, "보부상", "parch2", 10, anchor="ma")

# Bokgi: three hungry bundles of wood wearing black wrapping cloths
for k, (ex, ey) in enumerate(((226, 104), (256, 112), (288, 100))):
    L = Layer(seed=10 + k)
    L.disc(ex, ey + 12, 10, "brown", ry=13)
    for t in range(-8, 9, 4):
        L.rect(ex + t, ey + 2, 2, 22, "brown2")
    L.disc(ex, ey + 2, 11, "ink1", ry=7)
    L.rect(ex - 2, ey - 6, 4, 4, "ink1")
    L.paste(cv, outline="ink0")
    cv.dot(ex - 3, ey + 4, "gold2"); cv.dot(ex + 3, ey + 4, "gold2")
    cv.rect(ex - 2, ey + 8, 5, 1, "ink0")
    bar(cv, ex - 10, ey - 12, 20, 2, (0.9, 0.6, 1.0)[k], "red2")
    cv.text(ex, ey - 24, ("공격 4", "훔치기", "공격 3")[k], ("red2", "gold2", "red2")[k], 10, anchor="ma")
cv.rect(204, 136, 108, 14, "parch2"); cv.frame(204, 136, 108, 14, "ink1")
cv.text(258, 137.5, "배고프다… 봇짐을 내놔라", "ink1", 10, shadow=None, anchor="ma")

# Energy and end turn
cv.rect(150, 166, 170, 14, "ink0")
cv.text(156, 167.5, "기력", "parch2", 10)
for k in range(3):
    cv.disc(184 + k * 9, 173, 3, "gold2" if k < 2 else "ink3")
cv.rect(262, 166, 54, 14, "red0"); cv.frame(262, 166, 54, 14, "gold2")
cv.text(289, 167.5, "차례 끝", "gold2", 10, anchor="ma")

cv.export("concept-32-itch-bag.png")
print("saved")
