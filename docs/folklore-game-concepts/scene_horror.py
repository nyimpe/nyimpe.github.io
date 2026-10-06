"""Concept 7 — psychological horror: the shadow that grows with fear (side view)."""
import math
from pix import *

cv = Canvas("ink0", seed=91)
rng = cv.rng
LX, LY = 182, 104  # oil lamp


def blend(a, b, t):
    return tuple(int(a[k] * (1 - t) + b[k] * t) for k in range(3))


# Room: beams, paper doors, floor -----------------------------------------------------
cv.rect(0, 0, W, 26, "ink0")
for x in range(0, W, 10):
    cv.rect(x, 0, 4, 20, "brown0")
cv.rect(0, 20, W, 5, "brown"); cv.rect(0, 20, W, 1, "brown2")
cv.rect(0, 25, W, 104, "brown0")
cv.rect(0, 126, W, 3, "brown"); cv.rect(0, 126, W, 1, "brown2")
for y in range(129, 154):  # maru boards
    for x in range(W):
        cv.dot(x, y, "brown" if (y - 129) % 5 else "brown0")
for y in range(131, 154, 5):
    for x in range((y * 17) % 60, W, 60):
        cv.rect(x, y, 1, 4, "brown0")
cv.rect(0, 154, W, 26, "ink0")

DOORS = [(18, 32, 66, 92), (92, 32, 66, 92), (166, 32, 66, 92), (240, 32, 66, 92)]
for x, y, w, h in DOORS:
    cv.rect(x - 3, y - 3, w + 6, h + 6, "brown")
    cv.rect(x, y, w, h, "parch0")

# Folding screen with a faded crane painting, and what stands behind it
SX = 100
cv.rect(SX, 70, 60, 50, "brown0")
for k in range(4):
    cv.rect(SX + 1 + k * 15, 71, 13, 48, "parch0")
    cv.rect(SX + 1 + k * 15, 71, 13, 2, "red0")
cv.line(SX + 6, 108, SX + 24, 86, "ink3"); cv.line(SX + 24, 86, SX + 40, 98, "ink3")
cv.disc(SX + 42, 82, 3, "red0")
for lx in (SX + 18, SX + 30):  # black bony legs under the screen
    cv.rect(lx, 120, 2, 9, "ink0"); cv.dot(lx + 2, 123, "ink0"); cv.dot(lx - 1, 126, "ink0")
    cv.rect(lx - 2, 128, 5, 1, "ink0")
for i in range(SX + 12, SX + 40):  # hem of a paper skirt
    if i % 3:
        cv.dot(i, 119 + (i % 2), "white")
        cv.dot(i, 118, "parch")

# Darkness: only the oil lamp lights the room ----------------------------------------
cv.darken(lambda i, j: 1.18 - math.hypot(i - LX, (j - LY) * 1.1) / 62)
for _ in range(2):  # make the dark parts darker still
    for j in range(H):
        for i in range(W):
            d = math.hypot(i - LX, (j - LY) * 1.1)
            if d > 70:
                r, g, b = cv.px[i, j]
                cv.px[i, j] = (int(r * 0.62), int(g * 0.62), int(b * 0.7))

# Moonlit doors on the right, lit from the other side, with the shadow growing on them
glow = blend(P["parch0"], P["night3"], 0.45)
glow2 = blend(P["parch"], P["night3"], 0.35)
for x, y, w, h in DOORS[2:]:
    for j in range(y, y + h):
        for i in range(x, x + w):
            cv.px[i, j] = glow2 if rng.random() > 0.12 else glow
SH = Layer(seed=3)
cx_, base = 236, 125
SH.disc(cx_, base - 30, 34, "ink0", ry=34)  # hunched mass
SH.disc(cx_ - 14, base - 66, 20, "ink0", ry=18)  # head bowed toward the boy
SH.disc(cx_ - 26, base - 58, 9, "ink0", ry=8)
for k, (x0, y0, x1, y1) in enumerate(((cx_ - 20, base - 40, cx_ - 58, base - 4), (cx_ + 12, base - 44, cx_ + 40, base - 2))):
    for t in range(5):
        SH.line(x0 + t, y0, x1 + t // 2, y1, "ink0")
    for f in range(4):
        SH.line(x1 + f * 2, y1, x1 + f * 3 - 4, y1 + 6, "ink0")
for k in range(9):
    SH.line(cx_ - 26 + k * 4, base - 82, cx_ - 30 + k * 5, base - 96 - (k % 3) * 3, "ink0")
for j in range(H):
    for i in range(W):
        if SH.px[i, j][3] and any(x <= i < x + w and y <= j < y + h for x, y, w, h in DOORS[2:]):
            cv.px[i, j] = blend(P["ink0"], glow, 0.15)
for x, y, w, h in DOORS[2:]:  # lattice drawn over the shadow
    for gx in range(x, x + w + 1, 11):
        cv.rect(gx, y, 1, h, "brown0")
    for gy in range(y, y + h + 1, 13):
        cv.rect(x, gy, w, 1, "brown0")
    cv.frame(x - 1, y - 1, w + 2, h + 2, "brown0")
for k in range(3):  # two small eyes on the paper
    cv.dot(cx_ - 30 + k * 0, base - 62, None)
cv.rect(cx_ - 32, base - 62, 2, 1, "red2"); cv.rect(cx_ - 24, base - 62, 2, 1, "red2")

# Bamboo box rattling on the floor
cv.sprite([
    "..TTTTTTTTTTTT..",
    ".TtTtTtTtTtTtTT.",
    "TTTTTTTTTTTTTTTT",
    "TtTtTtTtTtTtTtTt",
    "TTTTTTTTTTTTTTTT",
    "TtTtTtTtTtTtTtTt",
    "TTTTTTTTTTTTTTTT",
    ".BBBBBBBBBBBBBB.",
], 210, 120, {"T": "moss2", "t": "moss0", "B": "brown0"}, outline="ink0")
cv.rect(208, 115, 20, 3, "moss3"); cv.frame(208, 115, 20, 3, "ink0")

# The boy with the oil lamp ---------------------------------------------------------------
for r_, col in ((16, "gold0"), (11, "gold")):
    for a in range(0, 360, 6):
        x = LX + r_ * math.cos(math.radians(a)); y = LY + r_ * 0.9 * math.sin(math.radians(a))
        if (int(x) + int(y)) % 2:
            cv.dot(x, y, col)
cv.sprite([
    "....KKKK....",
    "...KKKKKK...",
    "...KSSSSK...",
    "...SEsSEs...",
    "...SSSSSS...",
    "....SSSS....",
    "..WWWWWWWW..",
    ".WWWWWWWWWS.",
    ".WwWWWWWW.SS",
    ".WwWWRRWW...",
    ".WwWWWWWW...",
    ".WwWWWWWW...",
    "..WWWWWWW...",
    "..WW...WW...",
    "..WW...WW...",
    "..KK...KK...",
], LX - 12, 112, {"K": "ink0", "S": "skin", "s": "skin0", "E": "ink0", "W": "parch", "w": "parch0", "R": "red"},
          outline="ink0")
cv.sprite([".Y.", "YOY", ".O.", "GGG"], LX - 1, LY - 2, {"Y": "white", "O": "orange2", "G": "brown2"})
cv.disc(LX - 6, 128, 9, "ink0", ry=1)

# Sound cue from the box
for k, (x, y) in enumerate(((204, 112), (232, 112), (202, 120), (234, 119))):
    cv.line(x, y, x + (-3 if x < 218 else 3), y - 2, "parch")

# HUD ---------------------------------------------------------------------------------------
cv.text(6, 4, "두려움", "red2", 11)
bar(cv, 36, 7, 70, 3, 0.78, "red", bg="ink1", hi="red2")
cv.sprite([".R.R.", "RRRRR", "RRRRR", ".RRR.", "..R.."], 110, 6, {"R": "red2"})
cv.text(6, 13, "등잔 기름", "parch0", 10)
bar(cv, 36, 16, 40, 1, 0.35, "gold", bg="ink1")
cv.text(316, 4, "뛰면 두려움이 오른다", "ink3", 10, anchor="ra")

cv.rect(20, 158, 280, 20, "ink1"); cv.frame(20, 158, 280, 20, "ink3")
cv.text(160, 159.5, "병풍 뒤에서 죽은 고모의 목소리가 들린다.", "parch", 10, anchor="ma")
cv.text(160, 167, "“배가 고프구나… 밥 한 술만 다오.”", "red2", 11, anchor="ma")

cv.export("concept-7-psychological-horror.png")
print("saved")
