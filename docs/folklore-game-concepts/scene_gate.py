"""Concept 10 — gate inspection document thriller after Papers, Please."""
import math
from pix import *

cv = Canvas("night1", seed=121)
rng = cv.rng

# Outside: the city gate at night and the queue -----------------------------------------
cv.vgrad(0, 58, ["night0", "night1", "night2"])
cv.stars(30, 30)
for y in range(30, 58):  # fortress wall
    for x in range(W):
        cv.dot(x, y, "iron0" if ((x // 8) + (y // 5)) % 2 else "ink2")
for y in range(30, 58, 5):
    cv.rect(0, y, W, 1, "ink1")
cv.rect(196, 34, 64, 24, "ink0")  # gate arch
cv.disc(228, 36, 32, "ink0", ry=8)
cv.rect(186, 20, 84, 12, "brown0")
for x in range(190, 268, 7):
    cv.rect(x, 22, 2, 10, "red0")
giwa(cv, 180, 8, 96, 11, roof="ink1", edge="ink2", ridge="ink0")
for tx in (182, 274):  # torches
    cv.rect(tx, 40, 2, 14, "brown")
    cv.sprite([".Y.", "YOY", "OOO"], tx - 1, 36, {"Y": "gold2", "O": "orange"})
for k in range(9):  # queue of travellers in silhouette
    x = 8 + k * 19 + (k % 2) * 3
    h = 16 + (k * 7) % 6
    cv.rect(x, 58 - h + 5, 9, h - 5, "night0")
    cv.disc(x + 4, 58 - h + 3, 4, "night0")
    if k % 3 == 0:
        cv.rect(x - 2, 58 - h, 13, 2, "night0")  # gat brim
cv.sprite(["..YY......", ".YYYY...YY", "YYYYYYYYY.", ".YYYYYYYY.", ".Y.Y..Y.Y."], 160, 50, {"Y": "gold"}, outline="ink0")
cv.sprite(["W", "W", ".", "W"], 166, 41, {"W": "red2"}, outline="ink0")  # the yellow dog growls

cv.rect(0, 0, 112, 12, "ink0")
cv.text(4, 1.5, "숭례문 · 열흘째 · 해시", "parch2", 10)
cv.rect(204, 0, 116, 12, "ink0")
cv.text(316, 1.5, "통과 12 · 적발 3 · 녹봉 -1", "gold2", 10, anchor="ra")

# Booth window with the traveller -------------------------------------------------------
cv.rect(0, 58, W, 122, "brown0")
cv.rect(4, 62, 100, 66, "night2"); cv.frame(4, 62, 100, 66, "brown2")
cv.rect(5, 63, 98, 64, "teal0")
L = Layer(seed=4)
fx, fy = 54, 92
L.disc(fx, fy + 30, 30, "moss", ry=14)  # jang-ot cloak
L.disc(fx, fy + 4, 14, "ink0", ry=12)  # hair
L.disc(fx, fy + 6, 11, "skin", ry=12)
L.disc(fx, fy - 8, 9, "ink0", ry=5)
L.rect(fx + 8, fy - 9, 10, 2, "gold2")  # binyeo
L.rect(fx - 6, fy + 3, 4, 1, "ink0"); L.rect(fx + 3, fy + 3, 4, 1, "ink0")
L.dot(fx - 5, fy + 2, "ink1"); L.dot(fx + 5, fy + 2, "ink1")
L.disc(fx - 7, fy + 9, 2, "pink", ry=1); L.disc(fx + 7, fy + 9, 2, "pink", ry=1)
L.rect(fx - 2, fy + 12, 5, 1, "red")
L.paste(cv, outline="ink0")
cv.rect(0, 128, 108, 52, "brown0")
cv.frame(4, 62, 100, 66, "brown2")
cv.rect(5, 120, 98, 7, "brown")
cv.text(54, 120, "“친정에 가는 길이에요.”", "parch2", 10, anchor="ma")

panel(cv, 6, 134, 96, 40, fill="ink1", edge="parch0", inner="ink2")
cv.text(12, 136.5, "대기 9명", "parch2", 11)
cv.text(12, 146, "파루까지 두 시진", "parch0", 10)
for k in range(12):
    cv.rect(12 + k * 7, 160, 5, 8, "gold" if k < 5 else "ink2")

# Desk with documents ---------------------------------------------------------------------
cv.rect(108, 60, 212, 120, "brown")
for y in range(62, 180, 6):
    cv.rect(108, y, 212, 1, "brown0")

# Hopae (wooden ID tag)
L = Layer(seed=5)
L.rect(116, 70, 34, 58, "tan")
L.disc(133, 70, 17, "tan", ry=6)
L.disc(133, 66, 2, "brown0")
L.rect(118, 74, 30, 52, "parch0")
L.paste(cv, outline="ink0")
cv.line(133, 58, 133, 64, "red0")
for k, line in enumerate(("김씨 소사", "갑자생", "한성부", "남부 명철방")):
    cv.text(133, 76 + k * 9, line, "brown0", 10, shadow=None, anchor="ma")

# Travel permit
cv.rect(158, 68, 70, 64, "parch2"); cv.frame(158, 68, 70, 64, "parch0")
cv.text(193, 70, "통 행 첩", "ink0", 11, shadow=None, anchor="ma")
for k, line in enumerate(("성명  김씨 소사", "사유  친정 방문", "기한  사흘")):
    cv.text(162, 82 + k * 9, line, "ink1", 10, shadow=None)
cv.rect(210, 112, 13, 13, "red2"); cv.frame(210, 112, 13, 13, "red0")
cv.rect(213, 115, 7, 1, "parch2"); cv.rect(216, 115, 1, 7, "parch2")

# Bronze mirror: the reflection is not the woman
cv.disc(272, 96, 24, "gold0")
cv.disc(272, 96, 21, "gold")
cv.disc(272, 96, 19, "teal0")
L = Layer(seed=6)
L.disc(272, 100, 10, "white", ry=8)
L.sprite(["W......W", "WW....WW", "WPW..WPW"], 268, 84, {"W": "white", "P": "pink"})
L.disc(268, 98, 2, "red2"); L.disc(277, 98, 2, "red2")
L.rect(271, 103, 3, 2, "ink0")
L.paste(cv, outline="ink0")
cv.rect(268, 120, 8, 22, "brown0"); cv.rect(269, 120, 6, 22, "brown2")
cv.text(272, 141, "거울", "parch", 10, anchor="ma")

# Rule book
cv.rect(232, 150, 86, 28, "parch2"); cv.frame(232, 150, 86, 28, "brown0")
cv.text(236, 152, "오늘의 수칙", "red0", 10, shadow=None)
cv.text(236, 160, "거울에 다른 것이 비치면 포박", "ink1", 10, shadow=None)
cv.text(236, 168, "누렁개가 짖는 자는 다시 살핀다", "ink1", 10, shadow=None)

# Stamps and the rope
for k, (name, ink, body) in enumerate((("통과", "teal2", "teal0"), ("불허", "red2", "red0"))):
    x = 120 + k * 40
    cv.rect(x, 142, 30, 10, body); cv.frame(x, 142, 30, 10, "ink0")
    cv.rect(x + 9, 152, 12, 10, "brown2"); cv.frame(x + 9, 152, 12, 10, "ink0")
    cv.rect(x + 7, 162, 16, 4, "brown0")
    cv.text(x + 15, 142.5, name, "white", 10, shadow=None, anchor="ma")
for k in range(10):
    cv.disc(206 + (k % 3) * 2, 146 + k * 2.6, 3, "tan" if k % 2 else "brown2")
cv.text(208, 170, "포박", "parch2", 10, anchor="ma")

cv.export("concept-10-gate-inspection.png")
print("saved")
