"""Concept 34 — turn-based golf after Pangya (Joseon gyeokgu with holes called wa-a, on a haunted mountain course)."""
import math
from pix import *

cv = Canvas("teal3", seed=461)
rng = cv.rng

# Sky and far ridges --------------------------------------------------------------------------------------------
cv.vgrad(0, 110, ["teal2", "teal3", "ghost"])
cv.ridge(70, 14, "teal2", seed=5, freq=1.3)
cv.ridge(86, 10, "moss", seed=6, freq=1.8)
# Gang-gil: a long horsetail shape riding the wind
for k in range(40):
    x = 196 + k * 2.4
    y = 24 + 5 * math.sin(k * 0.35)
    cv.disc(x, y, 2.6 - k * 0.04, "parch2")
cv.text(250, 36, "강길 · 바람 3 →", "ink1", 10, shadow="white", anchor="ma")

# Course: tee cliff, gorge with a mountain pond, green on stone steps by a pavilion ---------------------------------
cv.rect(0, 110, W, 70, "moss")
for x in range(W):  # ground line
    cv.rect(x, 108 + int(3 * math.sin(x * 0.05)), 1, 4, "moss2")
cv.rect(0, 112, 64, 68, "moss2"); cv.rect(0, 112, 64, 2, "moss3")       # tee
cv.rect(64, 116, 150, 64, "moss")
for k in range(30):
    cv.dot(rng.randrange(64, 214), rng.randrange(118, 150), "moss2")
# Pond with the swallowing fish
cv.disc(112, 134, 28, "teal0", ry=10); cv.disc(112, 133, 26, "teal", ry=8)
L = Layer(seed=3)
L.disc(104, 128, 12, "teal2", ry=7)
L.paste(cv, outline="ink0")
cv.disc(98, 128, 6, "ink0", ry=4); cv.disc(98, 128, 5, "red0", ry=3)
for t in range(-4, 5, 2):
    cv.dot(98 + t, 125, "white"); cv.dot(98 + t + 1, 131, "white")
cv.dot(108, 125, "gold2")
cv.text(118, 146, "어탄독물", "white", 10, anchor="ma")
# Self-moving rocks on the fairway, with arrows showing next turn's move
for rx, ry, dx in ((160, 120, -1), (188, 126, 1)):
    L = Layer(seed=rx)
    L.disc(rx, ry, 8, "iron", ry=6); L.disc(rx - 2, ry - 2, 4, "iron2", ry=3)
    L.paste(cv, outline="ink0")
    cv.dot(rx - 3, ry, "ink0"); cv.dot(rx + 2, ry, "ink0")   # the rocks have faces
    cv.line(rx + dx * 10, ry + 2, rx + dx * 20, ry + 2, "gold2")
    cv.dot(rx + dx * 19, ry + 1, "gold2"); cv.dot(rx + dx * 19, ry + 3, "gold2")
cv.text(174, 136, "영암 · 다음 차례 움직임", "parch2", 10, anchor="ma")
# Green on stone steps with the pavilion
cv.rect(214, 104, 106, 76, "brown2")
for j in range(104, 180, 8):
    cv.rect(214, j, 106, 1, "brown")
cv.rect(222, 96, 98, 10, "moss3"); cv.rect(222, 96, 98, 1, "white")
cv.rect(270, 62, 44, 34, "red"); cv.rect(272, 64, 4, 32, "red0"); cv.rect(306, 64, 4, 32, "red0")
giwa(cv, 264, 50, 56, 12, roof="ink2", edge="iron", ridge="ink1")
cv.disc(250, 98, 3, "ink0", ry=1.4)  # the wa-a hole
cv.rect(250, 78, 1, 20, "parch2")
cv.sprite(["RRR", "RRRR", "RRR"], 251, 78, {"R": "red2"})

# Player at the tee with a spoon-shaped stick ------------------------------------------------------------------------
px, py = 30, 102
cv.sprite(["..KKKKK..", "KKKKKKKKK", "...SSS...", "...SES...", "..WWWWW..", ".WWWWWWW.", ".WWWWWWW.", "..WWWWW..", "..B...B..",
           "..K...K.."], px, py, {"K": "ink1", "S": "skin", "E": "ink0", "W": "parch2", "B": "brown2"}, outline="ink0")
cv.line(px + 8, py + 5, px + 16, py + 8, "brown0")
cv.disc(px + 17, py + 8, 2, "brown2", ry=1.4)
cv.disc(px + 21, py + 8, 1.5, "white")
# Planned arc and the dodging blue bird
pts = []
for t in range(0, 101, 3):
    x = px + 22 + (250 - px - 22) * t / 100
    y = py + 6 - 80 * math.sin(math.pi * t / 100) + (98 - py - 6) * t / 100
    pts.append((x, y))
for x, y in pts:
    cv.dot(x, y, "white")
cv.sprite([".BB..", "BBBBB", ".BWB.", "..B.."], 168, 32, {"B": "flame0", "W": "white"}, outline="ink0")
cv.line(172, 38, 182, 46, "flame2"); cv.dot(183, 47, "flame2")
cv.text(160, 18, "도전복 · 피할 곳을 노려라", "ink1", 10, shadow="white", anchor="ma")

# HUD -----------------------------------------------------------------------------------------------------------------
cv.rect(0, 0, 112, 30, "ink0")
cv.text(4, 1.5, "산골 코스 3번 와아", "parch2", 10)
cv.text(4, 14, "셋째 타 · 남은 거리 112보", "gold2", 10)
cv.rect(0, 156, W, 24, "ink0")
cv.text(6, 160, "힘", "parch2", 10)
GX, GW = 22, 180
cv.rect(GX, 160, GW, 10, "ink2"); cv.frame(GX - 1, 159, GW + 2, 12, "parch0")
for i in range(GW):
    t = i / GW
    cv.rect(GX + i, 161, 1, 8, "moss2" if t < 0.7 else ("gold2" if t < 0.86 else "red2"))
cv.rect(GX + int(GW * 0.80), 158, 2, 14, "white")      # sweet spot
cv.rect(GX + int(GW * 0.74), 157, 1, 16, "ink0")       # moving cursor
cv.rect(GX + int(GW * 0.74) - 1, 156, 3, 2, "white")
cv.text(GX + GW * 0.80 + 1, 171, "딱!", "gold2", 10, anchor="ma")
cv.text(232, 160, "나 7타", "parch2", 10)
cv.text(274, 160, "김 서방 6타", "red2", 10)

cv.export("concept-34-turn-golf.png")
print("saved")
