"""Concept 28 — lane-crossing arcade after Frogger (Geumwa hops home across road and river)."""
import math
from pix import *

cv = Canvas("ink0", seed=301)
rng = cv.rng
LANE = 12

# Layout: top bank with five homes, river lanes, middle bank, road lanes, start bank --------------------
def band(y0, y1, col, alt=None):
    for y in range(y0, y1):
        for x in range(W):
            cv.dot(x, y, col if not alt or rng.random() > 0.1 else alt)


band(10, 30, "moss", "moss2")
band(30, 90, "teal", "teal2")
band(90, 102, "moss", "moss2")
band(102, 150, "brown", "brown2")
band(150, 166, "moss", "moss2")
for y in range(30, 90, LANE):
    for x in range(0, W, 9):
        cv.rect(x + (y // LANE % 2) * 4, y + 6, 4, 1, "teal3")
for y in range(114, 150, LANE):
    for x in range(0, W, 16):
        cv.rect(x, y, 8, 1, "tan")

# Five homes: rocks by the lotus pond where Geumwa was found
for k in range(5):
    hx = 22 + k * 64
    cv.rect(hx - 12, 14, 24, 16, "teal0")
    cv.disc(hx, 24, 9, "teal", ry=5)
    cv.disc(hx - 8, 16, 5, "iron", ry=3); cv.disc(hx + 9, 17, 4, "iron2", ry=3)
    if k == 1:  # already home
        cv.sprite(["G...G", "GGGGG", "GEGEG", "GGGGG", ".G.G."], hx - 2, 20, {"G": "gold2", "E": "ink0"}, outline="ink0")
    if k == 3:  # lotus bonus
        cv.disc(hx, 24, 4, "pink", ry=3); cv.dot(hx, 23, "white")

# River lanes -----------------------------------------------------------------------------------------------
def turtles(x, y, n, sinking=False):
    for k in range(n):
        cv.sprite([".GGG.", "GgGgG", "GGGGG", ".G.G."], x + k * 7, y + 3, {"G": "moss0" if not sinking else "teal2", "g": "moss2"},
                  outline="ink0")


def crab_shell(x, y, w):
    cv.disc(x + w / 2, y + 6, w / 2, "red0", ry=5); cv.disc(x + w / 2, y + 5, w / 2 - 2, "red", ry=3)
    for k in range(4):
        cv.dot(x + 4 + k * (w - 8) / 3, y + 2, "orange")


def log(x, y, w):
    cv.rect(x, y + 2, w, 8, "brown0"); cv.rect(x + 1, y + 3, w - 2, 5, "brown2"); cv.rect(x + 1, y + 6, w - 2, 1, "brown")


turtles(10, 30, 4); turtles(120, 30, 3, sinking=True); turtles(220, 30, 4)          # coin-sized turtle swarms
crab_shell(30, 42, 46); crab_shell(170, 42, 52)                                       # giant crab shells as rafts
log(80, 54, 60); log(220, 54, 70)
turtles(40, 66, 3); turtles(150, 66, 4); turtles(260, 66, 3)
L = Layer(seed=4)  # Jangryangi: a big snake with ears spread, slicing the water
for t in range(50):
    L.disc(90 + t * 1.6, 82 + 2 * math.sin(t * 0.4), 2.5, "ink1")
L.disc(172, 81, 4, "ink1")
L.sprite(["E.", "EE", "E."], 168, 74, {"E": "ink2"}); L.sprite(["E.", "EE", "E."], 168, 85, {"E": "ink2"})
L.paste(cv, outline="ink0")
cv.dot(174, 80, "red2")
for k in range(4):
    cv.line(176 + k * 3, 78 + k, 180 + k * 3, 78 + k, "white")
# Mulgwisin's red hand reaching up between lanes
cv.sprite(["R.R.R", "RRRRR", ".RRR.", ".RRR."], 250, 80, {"R": "red2"}, outline="ink0")

# Player: Geumwa, the golden frog-like child, riding a crab shell
cv.sprite(["G...G", "GGGGG", "GEGEG", "GGGGG", "G.G.G"], 192, 41, {"G": "gold2", "E": "ink0"}, outline="ink0")

# Road lanes: will-o'-wisp processions and ox carts ------------------------------------------------------------
for k in range(6):
    cv.sprite(["..c..", ".cCc.", "cCWCc", ".cWc."], 20 + k * 9, 104, {"c": "flame0", "C": "flame", "W": "flame2"})
for k in range(5):
    cv.sprite(["..c..", ".cCc.", "cCWCc", ".cWc."], 200 + k * 9, 104, {"c": "red0", "C": "orange", "W": "gold2"})
for x in (60, 220):
    cv.sprite(["..BB.......", ".BBBB.RRRRR", "BBBBBBRRRRR", ".B..B.O...O"], x, 116, {"B": "brown0", "R": "brown2", "O": "ink0"},
              outline="ink0")
for x in (130, 280):
    cv.sprite(["KKKKKK..", "KWWWWKK.", "KKKKKKKK", ".O....O."], x, 128, {"K": "red0", "W": "parch2", "O": "ink0"}, outline="ink0")
for k in range(4):
    cv.sprite(["..c..", ".cCc.", "cCWCc", ".cWc."], 90 + k * 9, 140, {"c": "moss0", "C": "moss2", "W": "moss3"})

# HUD ----------------------------------------------------------------------------------------------------------
cv.rect(0, 0, W, 10, "ink0")
cv.text(4, 0, "1P 04,820", "parch2", 10)
cv.text(160, 0, "금와 징검다리", "gold2", 10, anchor="ma")
cv.text(316, 0, "최고 12,000", "red2", 10, anchor="ra")
cv.rect(0, 166, W, 14, "ink0")
for k in range(3):
    cv.sprite(["G...G", "GGGGG", "GEGEG", "GGGGG"], 6 + k * 9, 169, {"G": "gold2", "E": "ink0"})
cv.text(40, 167, "2판", "parch", 10)
cv.text(210, 167, "시간", "gold2", 10, anchor="ra")
bar(cv, 214, 171, 100, 3, 0.58, "moss3", bg="ink2")

cv.export("concept-28-retro-crossing.png")
print("saved")
