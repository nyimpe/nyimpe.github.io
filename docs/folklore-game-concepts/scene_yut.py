"""Concept 13 — yut-nori score roguelike after Balatro (monster cards bend the rules)."""
import math
from pix import *

cv = Canvas("teal0", seed=151)
rng = cv.rng

# Felt with slow swirling bands --------------------------------------------------------------
for y in range(H):
    for x in range(W):
        v = math.sin(x * 0.035 + math.sin(y * 0.05) * 2.2) + math.sin(y * 0.04 - x * 0.01)
        col = "teal0" if v < 0.4 else ("night1" if v < 1.1 else "teal")
        if v > 1.1 and (x + y) % 2:
            col = "teal0"
        cv.dot(x, y, col)

# Straw mat (meongseok) under the board and sticks
MX, MY, MW, MH = 84, 58, 200, 94
for y in range(MY, MY + MH):
    for x in range(MX, MX + MW):
        cv.dot(x, y, "tan" if (x // 2 + y) % 4 else "brown2")
cv.frame(MX, MY, MW, MH, "brown0")

# Yut board: 20 outer stations, two diagonals, centre ----------------------------------------
BX, BY, S = 96, 64, 80
pts = []
for k in range(5):
    t = k / 5
    pts += [(BX + S, BY + S - S * t), (BX + S - S * t, BY), (BX, BY + S * t), (BX + S * t, BY + S)]
cv.line(BX, BY, BX + S, BY + S, "brown0"); cv.line(BX + S, BY, BX, BY + S, "brown0")
cv.frame(BX, BY, S + 1, S + 1, "brown0")
for x, y in set(pts):
    big = (x in (BX, BX + S)) and (y in (BY, BY + S))
    cv.disc(x, y, 4 if big else 2.5, "ink1")
    cv.disc(x, y, 3 if big else 1.5, "parch2")
for t in (1 / 3, 2 / 3):
    for x, y in ((BX + S * t, BY + S * t), (BX + S - S * t, BY + S * t)):
        cv.disc(x, y, 2.5, "ink1"); cv.disc(x, y, 1.5, "parch2")
cv.disc(BX + S / 2, BY + S / 2, 4, "ink1"); cv.disc(BX + S / 2, BY + S / 2, 3, "gold2")

piece = ["..PP..", ".PPPP.", "PPpPPP", "PPPPPP", ".PPPP."]
cv.sprite(piece, BX + S - 3, BY + S - 34, {"P": "red2", "p": "pink"}, outline="ink0")  # carried pair (eopgi)
cv.sprite(piece, BX + S - 3, BY + S - 38, {"P": "red2", "p": "pink"}, outline="ink0")
cv.sprite(piece, BX + 13, BY - 3, {"P": "flame", "p": "flame2"}, outline="ink0")
for k in range(3):  # three-step move arrow
    y = BY + S - 44 - k * 16
    cv.rect(BX + S - 1, y - 6, 2, 6, "gold2")
cv.sprite(["..G..", ".GGG.", "GGGGG"], BX + S - 2, BY + S - 82, {"G": "gold2"})
cv.text(BX + S - 36, BY + S - 32, "+30 끗", "flame2", 10)

# Thrown sticks: three flat faces up, one round → geol ------------------------------------------
for k, flat in enumerate((True, True, False, True)):
    x0, y0 = 200 + k * 18, 63 + (k % 2) * 5
    for j in range(50):
        dx = int(j * 0.12 * (1 if k % 2 else -1))
        cv.rect(x0 + dx, y0 + j, 9, 1, "parch2" if flat else "brown")
        cv.dot(x0 + dx, y0 + j, "ink1"); cv.dot(x0 + dx + 8, y0 + j, "ink1")
        if not flat and j % 14 == 7:
            cv.line(x0 + dx + 2, y0 + j - 3, x0 + dx + 6, y0 + j + 3, "ink0")
            cv.line(x0 + dx + 6, y0 + j - 3, x0 + dx + 2, y0 + j + 3, "ink0")
        if flat and j in (0, 49):
            cv.rect(x0 + dx, y0 + j, 9, 1, "ink1")
cv.text(236, 122, "걸!", "gold2", 15, anchor="ma")
cv.text(236, 138, "세 칸", "parch2", 10, anchor="ma")

# Monster cards (the rule-benders) --------------------------------------------------------------
def card(x, y, name, art, hi=False):
    if hi:
        cv.rect(x - 1, y - 1, 34, 46, "gold2")
    cv.rect(x, y, 32, 44, "parch2"); cv.frame(x, y, 32, 44, "ink1")
    cv.rect(x + 3, y + 3, 26, 26, "ink1")
    art(x + 3, y + 3)
    cv.text(x + 16, y + 31, name, "ink0", 10, shadow=None, anchor="ma")


def red_crow(x, y):
    for bx in (5, 15):
        cv.sprite(["..RRR..", ".RRRRR.", "RRRRRRR", ".RR.RR.", ".K...K."], x + bx - 3, y + 12, {"R": "red", "K": "ink0"})
    cv.sprite([".RRR.", "RRERR", "RRRRY", ".RRR."], x + 8, y + 5, {"R": "red2", "E": "gold2", "Y": "gold"})


def seven_knots(x, y):
    cv.disc(x + 13, y + 16, 7, "skin")
    cv.rect(x + 9, y + 15, 2, 1, "ink0"); cv.rect(x + 15, y + 15, 2, 1, "ink0")
    cv.rect(x + 11, y + 19, 4, 1, "red0")
    for k in range(7):
        cv.disc(x + 4 + k * 3, y + 6 + (abs(k - 3) % 2), 1.5, "ink0")
        cv.rect(x + 4 + k * 3, y + 7, 1, 3, "ink0")


def rainbow_bird(x, y):
    for k, col in enumerate(("red2", "orange", "gold2", "moss3", "flame")):
        cv.line(x + 12, y + 14, x + 2 + k * 2, y + 24, col)
    cv.disc(x + 14, y + 11, 4, "pink"); cv.disc(x + 16, y + 8, 2.5, "pink")
    cv.dot(x + 17, y + 7, "ink0"); cv.dot(x + 19, y + 8, "gold2")


def gold_toad(x, y):
    cv.disc(x + 13, y + 16, 9, "gold0", ry=7)
    cv.disc(x + 13, y + 15, 8, "gold", ry=6)
    cv.disc(x + 9, y + 10, 2.5, "gold2"); cv.disc(x + 17, y + 10, 2.5, "gold2")
    cv.dot(x + 9, y + 10, "ink0"); cv.dot(x + 17, y + 10, "ink0")
    cv.rect(x + 10, y + 17, 7, 1, "gold0")


def rat_chain(x, y):
    for k in range(3):
        cv.sprite([".KK..", "KKKKK", "KRKKK", ".K.K."], x + 2 + k * 8, y + 10 + k * 3, {"K": "iron", "R": "red2"})
        cv.line(x + 7 + k * 8, y + 12 + k * 3, x + 10 + k * 8, y + 13 + k * 3, "pink")


cards = [("적오", red_crow), ("일두칠계", seven_knots), ("오색란연", rainbow_bird), ("금섬", gold_toad), ("중서함미", rat_chain)]
for k, (name, art) in enumerate(cards):
    card(92 + k * 38, 6, name, art, hi=(k == 0))
cv.text(282, 8, "5/5", "parch0", 10)
cv.text(94, 52.5, "적오 · 머리 하나에 몸 둘 — 같은 윷을 두 번 센다", "gold2", 10)

# Left panel: the run ---------------------------------------------------------------------------------
cv.rect(0, 0, 78, H, "ink1"); cv.rect(78, 0, 1, H, "ink0")
cv.rect(4, 4, 70, 26, "red0"); cv.frame(4, 4, 70, 26, "red2")
cv.text(39, 5, "셋째 판", "parch2", 11, anchor="ma")
cv.text(39, 16, "목표 1,200", "gold2", 11, anchor="ma")
cv.text(39, 35, "판 점수", "parch0", 10, anchor="ma")
cv.text(39, 43, "840", "parch2", 15, anchor="ma")
cv.rect(4, 60, 32, 22, "flame0"); cv.frame(4, 60, 32, 22, "flame")
cv.rect(42, 60, 32, 22, "red"); cv.frame(42, 60, 32, 22, "red2")
cv.text(20, 61, "끗", "flame2", 10, anchor="ma"); cv.text(20, 69, "36", "white", 12, anchor="ma")
cv.text(58, 61, "배", "pink", 10, anchor="ma"); cv.text(58, 69, "8", "white", 12, anchor="ma")
cv.text(39, 66, "×", "white", 11, anchor="ma")
for k, (lab, val, col) in enumerate((("던지기", "2", "flame2"), ("다시", "3", "red2"), ("엽전", "14", "gold2"), ("회차", "3/8", "parch2"))):
    y = 90 + k * 20
    cv.rect(4, y, 70, 16, "ink2")
    cv.text(8, y + 2.5, lab, "parch0", 10)
    cv.text(70, y + 1.5, val, col, 12, anchor="ra")

# Buttons --------------------------------------------------------------------------------------------
cv.rect(196, 158, 56, 16, "flame0"); cv.frame(196, 158, 56, 16, "flame2")
cv.text(224, 160, "던지기", "white", 11, anchor="ma")
cv.rect(258, 158, 58, 16, "red0"); cv.frame(258, 158, 58, 16, "red2")
cv.text(287, 160, "다시 던지기", "white", 11, anchor="ma")
cv.text(88, 160, "모 아니면 도", "parch2", 12)

cv.export("concept-13-yut-roguelike.png")
print("saved")
