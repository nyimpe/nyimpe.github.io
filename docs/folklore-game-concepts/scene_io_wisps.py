"""Concept 15 — Dokkaebibul.io: lead a procession of ghost-fire, encircle rivals (Slither.io)."""
import math
from pix import *
from io_ui import leaderboard, minimap, tag, nick

cv = Canvas("night1", seed=171)
rng = cv.rng

# Night road with a faint hex-ish dot lattice ---------------------------------------------------
for _ in range(900):
    cv.dot(rng.randrange(W), rng.randrange(H), rng.choice(("night0", "night2", "moss0")))
for y in range(0, H, 10):
    for x in range((y // 10 % 2) * 6, W, 12):
        cv.dot(x, y, "night2")

# Scattered soul-fires where a procession broke apart
for _ in range(60):
    a, r = rng.uniform(0, 6.28), rng.uniform(0, 26)
    x, y = 62 + r * math.cos(a), 52 + r * 0.7 * math.sin(a)
    col = rng.choice(("orange", "orange2", "gold2"))
    cv.rect(x, y, 2, 2, col); cv.dot(x, y, "white")


def procession(points, body, glow, core, me=False):
    beads = points[:-1][::3]
    for k, (x, y) in enumerate(beads):  # a string of separate flames, not a tube
        r = 2.6 + 1.4 * (k / len(beads))
        cv.disc(x, y, r + 1.2, glow)
    for k, (x, y) in enumerate(beads):
        r = 2.6 + 1.4 * (k / len(beads))
        cv.disc(x, y, r, body)
        cv.dot(x, y - 1, core)
        cv.dot(x + (k % 2) - 0.5, y - r - 1, core)  # flame tip
    hx, hy = points[-1]
    cv.disc(hx, hy, 7, glow); cv.disc(hx, hy, 6, body); cv.disc(hx, hy - 1, 3, core)
    px, py = points[-2]
    a = math.atan2(hy - py, hx - px)
    for side in (-1, 1):
        ex = hx + 2.5 * math.cos(a + side * 1.0); ey = hy + 2.5 * math.sin(a + side * 1.0)
        cv.rect(ex - 1, ey - 1, 2, 2, "white"); cv.dot(ex, ey, "ink0")
    for k in range(3):  # flickering tongue at the head
        cv.dot(hx - 2 + k * 2, hy - 8 - (k % 2), core)


def path(fn, n, step=0.02):
    return [fn(i * step) for i in range(n)]


# Me: a blue procession coiling around a smaller red one
me = path(lambda t: (150 + (38 - t * 9) * math.cos(t * 3.3 + 0.6), 96 + (30 - t * 7) * math.sin(t * 3.3 + 0.6)), 90)
red = path(lambda t: (146 + 8 * math.cos(t * 4), 94 + 6 * math.sin(t * 4)), 14, 0.08)
green = path(lambda t: (14 + t * 110, 152 - 14 * math.sin(t * 5.5)), 100)
white = path(lambda t: (210 - t * 70, 34 + 10 * math.sin(t * 7)), 48)
orange = path(lambda t: (300 - t * 40, 150 - t * 60 + 8 * math.sin(t * 6)), 40)

procession(green, "moss2", "moss0", "moss3")
procession(white, "ghost", "night3", "white")
procession(orange, "orange", "red0", "gold2")
procession(red, "red2", "red0", "pink")
procession(me, "flame", "flame0", "flame2", me=True)

nick(cv, me[-1][0], me[-1][1] - 16, "푸른등 (나)", "flame2")
nick(cv, 146, 80, "횃불이", "pink")
nick(cv, green[-1][0], green[-1][1] - 15, "솔방울불", "moss3")
nick(cv, white[-1][0], white[-1][1] - 15, "소복불", "ghost2")
nick(cv, orange[-1][0], orange[-1][1] - 15, "주홍초롱", "orange2")

# HUD ---------------------------------------------------------------------------------------------
leaderboard(cv, [("솔방울불", "212"), ("푸른등", "148"), ("주홍초롱", "96"), ("소복불", "71"), ("횃불이", "18")], "푸른등")
minimap(cv, 268, 132, 48, 44, [(8, 38, "moss3"), (34, 10, "ghost"), (44, 34, "orange"), (24, 22, "red2")], (26, 24))
tag(cv, 4, 4, "절기 · 동지 — 밤이 가장 긴 판")
tag(cv, 4, 18, "‘푸른등’이 ‘횃불이’를 둘러쌌다", fg="flame2", edge="flame0")
cv.rect(4, 162, 118, 14, "ink0"); cv.frame(4, 162, 118, 14, "ink2")
cv.text(8, 164, "행렬 148 · 2위 · 둘러싸기 9회", "parch2", 10)
cv.rect(128, 162, 136, 14, "night0"); cv.frame(128, 162, 136, 14, "gold0")
cv.text(196, 164, "다음 칭호까지 1회 · ‘길을 막는 불’", "gold2", 10, anchor="ma")

cv.export("concept-15-io-dokkaebibul.png")
print("saved")
