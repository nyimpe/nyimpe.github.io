"""Concept 41 — reactive turn-based RPG after Clair Obscur: Expedition 33 (masked exorcists parry the night terrors of the year-end rite)."""
import math
from pix import *


def big(rows):
    return ["".join(ch * 2 for ch in r) for r in rows for _ in (0, 1)]


cv = Canvas("night0", seed=531)
rng = cv.rng
FY = 132

# Palace courtyard on the last night of the year ---------------------------------------------------------------------
cv.vgrad(0, 100, ["night0", "night1", "purple0"])
for k in range(160):  # brushy painted strokes in the sky
    x, y = rng.randrange(W), rng.randrange(0, 90)
    cv.rect(x, y, rng.randrange(4, 12), 1, rng.choice(("night2", "purple", "night1")))
cv.rect(0, 70, W, 30, "ink1")
giwa(cv, 40, 58, 240, 14, roof="ink2", edge="iron0", ridge="ink0")
cv.rect(46, 72, 228, 28, "red0")
for x in range(52, 274, 22):
    cv.rect(x, 72, 3, 28, "red")
for lx in (70, 130, 190, 250):  # red lanterns
    cv.rect(lx, 74, 1, 6, "ink2")
    cv.disc(lx, 84, 4, "red2", ry=5); cv.disc(lx, 84, 2, "orange2", ry=3)
cv.rect(0, 100, W, 80, "iron0")
cv.rect(0, 100, W, 2, "iron")
for k in range(120):  # snow on the stones and in the air
    cv.dot(rng.randrange(W), rng.randrange(H), "white")

# Party: the four-eyed gold-masked bangsangsi, a chorani jester, a drummer -------------------------------------------
L = Layer(seed=2)
bx, by = 70, 100
L.disc(bx, by + 18, 11, "red", ry=16)            # red robe
L.disc(bx, by + 6, 13, "brown0", ry=8)           # bear-skin cape
L.disc(bx, by - 6, 9, "gold", ry=10)             # gold mask
L.rect(bx + 10, by - 18, 2, 44, "brown2")        # spear
L.rect(bx - 18, by + 6, 8, 18, "iron")           # shield
L.paste(cv, outline="ink0")
for ex in (-5, -1, 3, 7):                        # four eyes
    cv.rect(bx + ex - 1, by - 8, 2, 2, "ink0")
cv.sprite(["I", "III", "I"], bx + 9, by - 22, {"I": "iron2"})
cv.rect(bx - 4, by - 1, 9, 1, "red0")
# chorani jester
cv.sprite(big(["..WWWW..", ".WWWWWW.", ".WKWWKW.", ".WWRRWW.", "..RRRR..", ".RRRRRR.", "RRRRRRRR", ".RR..RR.", ".KK..KK."]), 4, 96,
          {"W": "parch2", "K": "ink0", "R": "red2"}, outline="ink0")
# drummer
cv.sprite(big(["..KKK...", ".SSSSS..", ".SESES..", "..WWW...", ".WWWWW.D", "WWWWWWDD", ".WWWWW.D", ".KK.KK.."]), 14, 134,
          {"K": "ink0", "S": "skin", "E": "ink0", "W": "parch2", "D": "red0"}, outline="ink0")
for k, (x, y, hp) in enumerate(((60, 136, 0.7), (4, 116, 0.9), (14, 152, 0.5))):
    bar(cv, x, y, 22, 2, hp, "moss3")

# Enemies: the black shape that roams the streets at night, with rumour-born ghost soldiers ---------------------------
L = Layer(seed=3)
hx, hy = 248, 98
for k in range(26):
    a = k / 26 * 6.28
    L.disc(hx + 26 * math.cos(a) * (0.8 + 0.2 * math.sin(k * 3)), hy + 30 * math.sin(a), 9, "ink0")
L.disc(hx, hy, 26, "ink0", ry=30)
L.paste(cv, outline="purple2")
cv.rect(hx - 10, hy - 10, 6, 3, "gold2"); cv.rect(hx + 6, hy - 10, 6, 3, "gold2")
cv.text(hx, hy - 46, "흑기", "parch2", 11, anchor="ma")
bar(cv, hx - 30, hy - 34, 60, 3, 0.6, "red2")
for sx, sy in ((192, 124), (284, 130)):
    cv.sprite(big(["..GGG..", ".GKGKG.", "..GGG..", ".IIIII.", "GIIIIIG", ".II.II.", ".G...G."]), sx, sy,
              {"G": "ghost", "K": "ink0", "I": "iron"}, outline="ink1")
    cv.line(sx + 15, sy - 10, sx + 15, sy + 14, "brown2"); cv.sprite(["I", "III"], sx + 14, sy - 12, {"I": "iron2"})
cv.text(247, 158, "탁탁귀병", "ghost", 10, anchor="ma")

# Incoming strike and the parry prompt ----------------------------------------------------------------------------------
for t in range(40):  # a black lash sweeping toward the bangsangsi
    x = hx - 30 - t * 3.6
    y = hy + 6 + 12 * math.sin(t * 0.25)
    cv.disc(x, y, 2.6 - t * 0.04, "ink0")
cv.ring(bx, by + 6, 30, "gold2"); cv.ring(bx, by + 6, 31, "gold2")
cv.ring(bx, by + 6, 20, "white")
cv.rect(bx + 26, by - 40, 74, 26, "ink0"); cv.frame(bx + 26, by - 40, 74, 26, "gold2")
cv.text(bx + 63, by - 38, "막기!", "gold2", 12, anchor="ma")
cv.text(bx + 63, by - 25, "고리가 겹칠 때", "parch2", 10, anchor="ma")

# HUD ----------------------------------------------------------------------------------------------------------------
cv.rect(0, 0, W, 14, "ink0")
cv.text(4, 1.5, "섣달그믐 나례 · 궐 안 마당", "parch2", 10)
for k, col in enumerate(("gold", "ink0", "red2", "parch2", "ghost")):
    cv.rect(200 + k * 14, 2, 11, 10, col); cv.frame(200 + k * 14, 2, 11, 10, "purple2" if col == "ink0" else "ink2")
cv.rect(0, 168, W, 12, "ink0")
cv.text(4, 168.5, "기운", "parch2", 10)
for k in range(9):
    cv.sprite([".G.", "GGG", ".G."], 28 + k * 6, 172, {"G": "gold2" if k < 5 else "ink3"})
cv.text(316, 168.5, "완벽히 막으면 반격 · 놓치면 탈이 깨짐", "parch0", 10, anchor="ra")

cv.export("concept-41-turn-parry.png")
print("saved")
