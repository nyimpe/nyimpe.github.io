"""Concept 37 — dice-clash card battles after Library of Ruina (librarians receive strange guests; the losers become books)."""
import math
from pix import *

cv = Canvas("brown0", seed=491)
rng = cv.rng

# Archive hall: tall shelves of books -------------------------------------------------------------------------------
cv.rect(0, 0, W, 112, "brown0")
SPINES = ["red", "teal", "gold0", "moss", "purple", "brown2", "red0", "flame0"]
for sx in range(0, W, 40):
    cv.rect(sx, 10, 38, 100, "brown")
    for shelf in range(4):
        y = 14 + shelf * 24
        x = sx + 2
        while x < sx + 36:
            w = rng.randrange(2, 5)
            h = rng.randrange(14, 20)
            cv.rect(x, y + 20 - h, w, h, rng.choice(SPINES))
            x += w
        cv.rect(sx, y + 20, 38, 3, "brown2")
cv.darken(lambda x, y: 0.55 if y < 112 else 1)
cv.rect(0, 112, W, 68, "brown"); cv.rect(0, 112, W, 2, "brown2")
for x in range(0, W, 26):
    cv.rect(x, 114, 1, 66, "brown0")
for lx in (60, 160, 260):  # hanging lanterns
    cv.rect(lx, 0, 1, 14, "ink2")
    cv.disc(lx, 18, 5, "orange", ry=6); cv.disc(lx, 18, 3, "orange2", ry=4)


def dice_box(x, y, n, col="parch2", edge="ink0"):
    cv.rect(x, y, 10, 10, col); cv.frame(x, y, 10, 10, edge)
    cv.text(x + 5, y + 0.5, str(n), "ink0", 10, shadow=None, anchor="ma")


# Librarians ---------------------------------------------------------------------------------------------------------
libs = [(30, 104, "flame0"), (58, 116, "moss"), (34, 132, "purple")]
for k, (x, y, robe) in enumerate(libs):
    cv.sprite(["..KKKK..", ".KKKKKK.", "..SSSS..", "..SESE..", ".RRRRRR.", "RRRRRRRR", "RRRRGRRR", ".RRRRRR.", ".RR..RR."], x, y,
              {"K": "ink0", "S": "skin", "E": "ink0", "R": robe, "G": "gold2"}, outline="ink0")
    bar(cv, x - 2, y + 11, 12, 2, (0.8, 0.5, 0.9)[k], "moss3")
dice_box(32, 90, 6, "gold2"); dice_box(60, 102, 4); dice_box(36, 118, 3)

# Guests --------------------------------------------------------------------------------------------------------------
# Seonghwi: palm-sized eyes, gold-thread robe, a great gong
gx, gy = 252, 100
L = Layer(seed=5)
L.disc(gx, gy + 12, 13, "red0", ry=16)
L.disc(gx, gy - 8, 10, "skin0", ry=10)
L.paste(cv, outline="ink0")
for ex in (gx - 5, gx + 5):
    cv.disc(ex, gy - 9, 4, "white", ry=3); cv.disc(ex, gy - 9, 1.5, "ink0")
for j in range(gy, gy + 26, 4):
    cv.line(gx - 8, j, gx + 8, j + 2, "gold2")
cv.disc(gx + 22, gy + 6, 9, "gold0"); cv.disc(gx + 22, gy + 6, 7, "gold"); cv.disc(gx + 22, gy + 6, 2, "gold2")
cv.text(gx, gy - 30, "성귀", "gold2", 10, anchor="ma")
dice_box(gx - 5, gy - 44, 5, "red2")
# Seonhal-seonsok: a string thin as a geomungo string, speaking in a woman's voice
sx0, sy0 = 210, 126
for t in range(80):
    x = sx0 + 16 * math.sin(t * 0.16) + t * 0.1
    y = sy0 - t * 0.5 + 6 * math.cos(t * 0.33)
    cv.rect(x, y, 2, 1, "parch2"); cv.dot(x, y + 1, "tan")
cv.text(sx0 + 4, sy0 + 6, "선할선속", "parch2", 10, anchor="ma")
cv.text(196, 44, "“끊어도 다시 이어져요”", "pink", 10, anchor="ma")
dice_box(sx0 - 2, sy0 - 60, 8, "red2"); dice_box(sx0 + 10, sy0 - 60, 2, "red2")
# Jeseong-daegok: a crowd of crying ghosts
for k in range(4):
    x, y = 276 + (k % 2) * 16, 116 + (k // 2) * 11
    cv.sprite([".WWWW.", "WKWWKW", "WBWWBW", "WWWWWW", "W.WW.W"], x, y, {"W": "ghost2", "K": "ink0", "B": "flame"}, outline="ink1")
cv.text(290, 138, "제성대곡", "ghost2", 10, anchor="ma")
dice_box(285, 102, 4, "red2")

# Clash lines between dice ------------------------------------------------------------------------------------------
for (x0, y0), (x1, y1), col in (((42, 95), (247, 61), "gold2"), ((70, 107), (208, 71), "gold2"), ((46, 123), (285, 107), "parch0")):
    for t in range(0, 101, 2):
        cv.dot(x0 + (x1 - x0) * t / 100, y0 + (y1 - y0) * t / 100 + -18 * math.sin(math.pi * t / 100), col)
# The current clash
cv.rect(120, 64, 80, 30, "ink0"); cv.frame(120, 64, 80, 30, "gold2")
cv.text(140, 66, "7", "gold2", 20, anchor="ma")
cv.text(160, 72, "합", "parch2", 11, anchor="ma")
cv.text(180, 66, "5", "red2", 20, anchor="ma")
cv.text(160, 84, "사서 승리", "gold2", 10, anchor="ma")

# Hand of combat pages ------------------------------------------------------------------------------------------------
pages = [("먹 튀기기", "2-5", "teal3"), ("붓끝 찌르기", "4-8", "red2"), ("책장 덮기", "막기 3-6", "flame"), ("낭독", "원거리 3-7", "gold2"),
         ("서명", "회복 2-4", "moss3")]
for k, (name, dice, col) in enumerate(pages):
    x = 8 + k * 50
    y = 148 + (2 if k != 1 else -4)
    cv.rect(x, y, 46, 30, "parch2"); cv.frame(x, y, 46, 30, col); cv.frame(x + 1, y + 1, 44, 28, "ink1")
    cv.text(x + 23, y + 3, name, "ink0", 10, shadow=None, anchor="ma")
    cv.text(x + 23, y + 16, dice, "red0" if col == "red2" else "ink1", 10, shadow=None, anchor="ma")
cv.rect(262, 148, 56, 30, "ink0"); cv.frame(262, 148, 56, 30, "parch0")
cv.text(290, 150, "빛 3 / 4", "gold2", 10, anchor="ma")
cv.text(290, 163, "진 손님은 책으로", "parch0", 10, anchor="ma")

cv.rect(0, 0, W, 13, "ink0")
cv.text(4, 1, "사고(史庫) 넷째 층 · 기이한 것들의 서가", "parch2", 10)
cv.text(316, 1, "접대 3막", "gold2", 10, anchor="ra")

cv.export("concept-37-turn-clash.png")
print("saved")
