"""Concept 16 — Geumjul.io: drag a straw taboo-rope to enclose land (Paper.io)."""
import math
from pix import *
from io_ui import leaderboard, minimap, tag, nick

cv = Canvas("moss", seed=181)
rng = cv.rng
CS = 4  # cell size
GW, GH = W // CS, H // CS

# Fields
for y in range(H):
    for x in range(W):
        cv.dot(x, y, "moss" if (y // 6) % 2 else "moss0")
for _ in range(700):
    cv.dot(rng.randrange(W), rng.randrange(H), "moss2")

owner = [[None] * GW for _ in range(GH)]


def claim(name, cells):
    for cx, cy in cells:
        if 0 <= cx < GW and 0 <= cy < GH:
            owner[cy][cx] = name


def blob(cx, cy, rx, ry, wob=0.25, seed=0):
    out = []
    for y in range(GH):
        for x in range(GW):
            a = math.atan2(y - cy, x - cx)
            r = 1 + wob * math.sin(a * 3 + seed) + wob * 0.6 * math.sin(a * 5 + seed * 2)
            if ((x - cx) / (rx * r)) ** 2 + ((y - cy) / (ry * r)) ** 2 <= 1:
                out.append((x, y))
    return out


claim("red", blob(16, 12, 12, 8, seed=1))
claim("teal", blob(62, 34, 11, 8, seed=2))
claim("moss", blob(14, 36, 9, 6, seed=3))
claim("me", blob(44, 20, 9, 7, seed=4))
# Dueoksini wiped part of the red land that no iron horse protects
erased = [(x, y) for x, y in blob(22, 15, 6, 4, seed=5)]
for x, y in erased:
    if owner[y][x] == "red":
        owner[y][x] = "erased"

COL = {"red": ("red", "red0", "red2"), "teal": ("teal2", "teal", "teal3"), "moss": ("moss3", "moss2", "parch"),
       "me": ("gold", "gold0", "gold2"), "erased": ("purple0", "purple0", "purple")}
for y in range(GH):
    for x in range(GW):
        o = owner[y][x]
        if not o:
            continue
        fill, edge, hi = COL[o]
        border = any(not (0 <= x + dx < GW and 0 <= y + dy < GH) or owner[y + dy][x + dx] != o
                     for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        cv.rect(x * CS, y * CS, CS, CS, edge if border else fill)
        if o == "erased":
            cv.dither(x * CS, y * CS, CS, CS, "purple0", "moss0")
        elif not border and (x + y) % 5 == 0:
            cv.dot(x * CS + 1, y * CS + 1, hi)

# Iron horses buried at each village core
for cx, cy in ((12, 11), (62, 34), (14, 36), (44, 20)):
    cv.ring(cx * CS + 2, cy * CS + 2, 7, "iron2")
    cv.sprite(["..II.", "IIII.", ".III.", ".I.I."], cx * CS, cy * CS, {"I": "iron2"}, outline="ink0")


def rope(pts, knots=True):
    for k, ((x0, y0), (x1, y1)) in enumerate(zip(pts, pts[1:])):
        n = int(max(abs(x1 - x0), abs(y1 - y0)))
        for t in range(n + 1):
            x = x0 + (x1 - x0) * t / max(n, 1); y = y0 + (y1 - y0) * t / max(n, 1)
            cv.rect(x - 1, y - 1, 3, 3, "brown0")
            cv.dot(x, y, "tan" if (int(x) + int(y)) % 3 else "brown2")
            cv.dot(x - 1 if (t % 4 < 2) else x + 1, y, "parch0")
            if knots and t % 14 == 7:
                cv.rect(x - 1, y + 1, 2, 4, "red2" if (t // 14) % 2 else "ink0")  # pepper / charcoal


# My rope looping out of my land, about to close
me_path = [(214, 92), (232, 92), (244, 104), (244, 124), (226, 138), (200, 136), (188, 120), (184, 100)]
rope(me_path)
hx, hy = me_path[-1]
cv.sprite([".KKK.", "KKKKK", ".SSS.", ".SES.", "WWWWW", ".W.W."], hx - 2, hy - 6,
          {"K": "ink0", "S": "skin", "E": "ink0", "W": "parch2"}, outline="ink0")
nick(cv, hx, hy - 16, "새끼줄 (나)", "gold2")
for x, y in ((186, 96), (190, 90), (196, 88)):
    cv.dot(x, y, "gold2")

# A rival cutting toward my open rope
rx, ry = 262, 132
rope([(300, 150), (284, 146), (270, 138)], knots=False)
cv.sprite([".KKK.", "KKKKK", ".SSS.", ".SES.", "TTTTT", ".T.T."], rx - 2, ry - 6,
          {"K": "ink0", "S": "skin", "E": "ink0", "T": "teal2"}, outline="ink0")
nick(cv, rx, ry - 16, "청사초롱", "teal3")
cv.sprite(["R", "R", "R", ".", "R"], 252, 122, {"R": "red2"}, outline="ink0")

# Dueoksini roaming, wiping unprotected land
L = Layer(seed=3)
dx, dy = 98, 64
L.disc(dx, dy, 10, "purple0", ry=11)
L.disc(dx + 2, dy - 2, 7, "purple", ry=8)
L.paste(cv, outline="ink0")
cv.rect(dx - 4, dy - 3, 2, 2, "red2"); cv.rect(dx + 2, dy - 3, 2, 2, "red2")
for k in range(5):
    cv.dot(dx - 5 + k * 2, dy + 3 + (k % 2), "parch2")
nick(cv, dx, dy - 22, "두억시니", "purple2")

# HUD ------------------------------------------------------------------------------------------------
leaderboard(cv, [("붉은당집", "14.8%"), ("새끼줄", "12.4%"), ("청사초롱", "11.9%"), ("솔가지", "6.1%"), ("숯검댕", "3.2%")], "새끼줄", title="마을 넓이")
minimap(cv, 268, 132, 48, 44, [(8, 8, "red2"), (12, 10, "red2"), (40, 28, "teal2"), (8, 30, "moss3"), (26, 14, "gold")], (28, 16))
tag(cv, 4, 4, "절기 · 입춘 — 새 금줄 무늬가 풀리는 주간")
tag(cv, 4, 18, "두억시니 출몰 · 철마 없는 땅이 지워진다", fg="purple2", edge="purple")
cv.rect(4, 162, 112, 14, "ink0"); cv.frame(4, 162, 112, 14, "ink2")
cv.text(8, 164, "마을 12.4% · 2위 · 최고 18%", "parch2", 10)
cv.rect(120, 162, 144, 14, "ink0"); cv.frame(120, 162, 144, 14, "gold0")
cv.text(192, 164, "금줄 무늬 해금 · 숯과 솔가지", "gold2", 10, anchor="ma")

cv.export("concept-16-io-geumjul.png")
print("saved")
