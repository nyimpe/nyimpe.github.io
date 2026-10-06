"""Concept 14 — Bulgasari.io: eat iron, grow, swallow smaller players (Agar.io / Hole.io)."""
import math
from pix import *
from io_ui import leaderboard, minimap, tag, nick

cv = Canvas("tan", seed=161)
rng = cv.rng

# Market ground with a faint grid ---------------------------------------------------------
for _ in range(1400):
    cv.dot(rng.randrange(W), rng.randrange(H), rng.choice(("parch0", "tan", "brown2")))
for x in range(0, W, 20):
    for y in range(H):
        if y % 2:
            cv.dot(x, y, "parch0")
for y in range(0, H, 20):
    for x in range(W):
        if x % 2:
            cv.dot(x, y, "parch0")

# Iron to eat: needles, spoons, sickles, pots, a temple bell
needle = ["I", "I", "I", "i"]
spoon = [".II.", "IIII", ".II.", ".I..", ".I..", ".I.."]
hoe = ["IIII.", "...I.", "...B.", "...B.", "...B."]
pot = [".KKKKK.", "KIIIIIK", "KIiIIIK", ".KKKKK."]
bell = ["..GG..", ".GGGG.", ".GGGG.", "GGGGGG", "GgGGgG", "GGGGGG"]
items = [(needle, 1), (spoon, 1), (hoe, 1), (pot, 1)]
for _ in range(70):
    rows, _w = rng.choice(items + [(needle, 1)] * 3)
    x, y = rng.randrange(4, 220), rng.randrange(16, 170)
    cv.sprite(rows, x, y, {"I": "iron2", "i": "iron", "B": "brown", "K": "ink1", "G": "gold", "g": "gold0"}, outline="ink1")
for x, y in ((40, 40), (196, 150)):
    cv.sprite(bell, x, y, {"G": "gold", "g": "gold0"}, outline="ink0")


def beast(cx, cy, r, body="ink1", eye="orange2", burning=False):
    L = Layer(seed=int(cx * 7 + cy))
    L.disc(cx, cy, r, "ink0")
    L.disc(cx - r * 0.15, cy - r * 0.2, r * 0.82, body)
    n = max(10, int(r * 2.2))
    for k in range(n):  # iron needles bristling
        a = 2 * math.pi * k / n
        x0, y0 = cx + r * math.cos(a), cy + r * math.sin(a)
        L.line(x0, y0, x0 + 3 * math.cos(a), y0 + 3 * math.sin(a), "iron2" if k % 2 else "iron")
    L.paste(cv, outline="ink0")
    e = max(1, int(r * 0.18))
    for sx in (-1, 1):
        cv.disc(cx + sx * r * 0.35, cy - r * 0.15, e + 1, eye); cv.dot(cx + sx * r * 0.35, cy - r * 0.15, "ink0")
    if burning:
        for k in range(16):
            a = 2 * math.pi * k / 16
            cv.sprite([".O.", "OYO"], cx + (r + 4) * math.cos(a) - 1, cy + (r + 4) * math.sin(a) - 1,
                      {"O": "orange", "Y": "gold2"})


# Players ----------------------------------------------------------------------------------------
beast(268, 104, 26, burning=False)  # the leader, breathing fire
for t in range(2, 46):  # fire breath cone toward the left
    half = 2 + t * 0.34 + 2 * math.sin(t * 0.7)
    for d in range(-int(half), int(half) + 1):
        edge = abs(d) / max(half, 1)
        if rng.random() < 1.05 - edge * 0.7 - t / 90:
            col = "gold2" if edge < 0.35 and t < 26 else ("orange2" if edge < 0.7 and t < 36 else "orange")
            cv.dot(268 - 24 - t, 104 + d, col)
nick(cv, 268, 66, "범종먹보")
beast(118, 96, 16)  # me
nick(cv, 118, 72, "nyimpe", "gold2")
beast(150, 120, 6)  # smaller prey about to be swallowed
nick(cv, 150, 108, "호미도둑")
beast(64, 132, 10, burning=True)  # set alight but still roaming
nick(cv, 64, 116, "불붙은돌쇠")
beast(178, 40, 8)
nick(cv, 178, 26, "숟가락")
for k in range(5):
    cv.dot(130 + k * 4, 104 + k * 3, "gold2")

cv.text(122, 50, "+호미 ×3", "gold2", 10, anchor="ma")

# HUD ------------------------------------------------------------------------------------------------
leaderboard(cv, [("범종먹보", "4,120"), ("쇠먹보", "2,870"), ("nyimpe", "1,640"), ("가마솥", "1,210"), ("호미도둑", "640")], "nyimpe")
minimap(cv, 268, 132, 48, 44, [(10, 12, "red2"), (30, 20, "orange"), (40, 34, "iron2"), (8, 30, "iron2"), (22, 8, "iron2")], (20, 22))
tag(cv, 4, 4, "절기 · 상강 — 서리 내린 장터")
tag(cv, 4, 18, "오늘의 출몰 · 천구성", fg="flame2", edge="flame0")
cv.rect(4, 162, 124, 14, "ink0"); cv.frame(4, 162, 124, 14, "ink2")
cv.text(8, 164, "크기 1,640 · 3위 · 먹혀도 작아질 뿐", "parch2", 10)
cv.rect(70, 142, 128, 14, "moss0"); cv.frame(70, 142, 128, 14, "moss3")
cv.text(134, 144, "도감 +1 · 범종 (처음 먹어 봄)", "moss3", 10, anchor="ma")

cv.export("concept-14-io-bulgasari.png")
print("saved")
