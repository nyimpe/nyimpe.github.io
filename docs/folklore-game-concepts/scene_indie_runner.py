"""Concept 22 — side-scrolling runner after Cookie Run (Mokgaek races a mountain that moves unseen)."""
import math
from pix import *

cv = Canvas("teal3", seed=341)
rng = cv.rng
G = 138  # ground line

cv.vgrad(0, G, ["teal2", "teal3", "parch", "parch2"])
cv.ridge(90, 22, "moss3", seed=3, freq=1.1, to=G)
cv.ridge(110, 12, "moss2", seed=7, freq=1.8, to=G)
for x in (40, 120, 230, 300):
    pine(cv, x, G - 2, 34, dark="moss0", mid="moss", trunk="brown0", seed=x)

# Gongjusan: the mountain that creeps forward when nobody looks
L = Layer(seed=2)
L.disc(28, G + 10, 62, "moss0", ry=86)
L.disc(16, G + 6, 40, "moss", ry=70)
for k in range(10):  # rocky ridge texture
    L.line(-10 + k * 9, 70 + abs(5 - k) * 6, -4 + k * 9, 78 + abs(5 - k) * 6, "ink1")
L.paste(cv, outline="ink0")
for ex in (16, 42):
    cv.rect(ex, 84, 8, 5, "white"); cv.rect(ex + 3, 85, 3, 4, "ink0")
cv.rect(22, 104, 20, 3, "ink0")
for k in range(4):
    cv.line(74 + k * 3, 80 + k * 8, 80 + k * 3, 80 + k * 8, "parch0")
cv.text(40, 40, "공주산", "red2", 11, anchor="ma")
cv.text(40, 50, "돌아보면 멈춘다", "parch2", 10, anchor="ma")

# Ground with a ditch left by the great serpent Daemang
for x in range(W):
    if 170 <= x < 196:
        continue
    for y in range(G, H - 22):
        cv.dot(x, y, "moss2" if y - G < 3 else ("brown2" if (x + y) % 5 else "brown"))
cv.rect(170, G + 6, 26, 14, "teal")
cv.text(183, G + 8, "도랑", "parch2", 10, anchor="ma")

# Mountain ginseng in a jumping arc
for k in range(9):
    t = k / 8
    x = 120 + t * 110; y = G - 24 - 34 * math.sin(t * math.pi)
    cv.sprite(["..G..", ".GGG.", "..T..", ".TTT.", "T.T.T"], x, y, {"G": "moss3", "T": "tan"}, outline="ink0")

# Mokgaek mid-jump, with a one-legged Dokgak hopping alongside
MX, MY = 150, 70
cv.sprite([
    "...GG.....",
    "..GGGG....",
    ".BBBBBB...",
    ".BSSSSB...",
    ".BSESEB...",
    "..SSSS....",
    ".TTTTTT.S.",
    "STTTTTTSS.",
    "..TTTT....",
    "..T..T....",
    ".TT...TT..",
], MX, MY, {"G": "moss3", "B": "brown", "S": "skin", "E": "ink0", "T": "moss"}, outline="ink0")
for k in range(5):
    cv.dot(MX - 4 - k * 4, MY + 8 + k, "parch2")
cv.sprite(["KKKKK", ".SSS.", ".SES.", "DDDDD", "DDDDD", "..D..", "..D..", ".KK.."], 100, G - 18,
          {"K": "tan", "S": "skin", "E": "ink0", "D": "moss0"}, outline="ink0")
cv.text(102, G - 26, "독각", "parch2", 10, anchor="ma")

# Three-bee swarm as an overhead hazard
for k, (bx, by) in enumerate(((262, 96), (272, 92), (282, 98))):
    cv.sprite(["W.W", "YKY", "KYK"], bx, by, {"W": "ghost2", "Y": "gold2", "K": "ink0"})

# HUD -------------------------------------------------------------------------------------------------------
cv.rect(0, 0, W, 14, "ink0")
cv.sprite([".R.R.", "RRRRR", ".RRR.", "..R.."], 4, 4, {"R": "red2"})
bar(cv, 12, 5, 120, 4, 0.64, "red2", bg="ink2", hi="pink")
cv.text(140, 2, "기운이 계속 줄어든다", "parch0", 10)
cv.text(316, 2, "점수 1,284,600", "gold2", 10, anchor="ra")
cv.text(316, 16, "3,420m", "parch2", 11, anchor="ra")
cv.rect(0, H - 22, W, 22, "ink0")
for k, (name, x) in enumerate((("뛰기", 6), ("숙이기", 254))):
    cv.rect(x, H - 19, 60, 16, "ink2" if k else "moss0"); cv.frame(x, H - 19, 60, 16, "moss3" if not k else "parch0")
    cv.text(x + 30, H - 17, name, "parch2", 11, anchor="ma")
cv.text(160, H - 17, "목객 · 산삼 42", "moss3", 11, anchor="ma")

cv.export("concept-22-indie-runner.png")
print("saved")
