"""Concept 25 — lead the tail-to-mouth rat procession after Lemmings (Sageumgap tale)."""
import math
from pix import *

cv = Canvas("teal3", seed=271)
rng = cv.rng
GH = 144  # game area height

# Sky, distant palace, cross-section of earth ----------------------------------------------------------
cv.vgrad(0, GH, ["teal2", "teal3", "parch", "parch2"])
cv.ridge(70, 12, "moss3", seed=3, freq=1.2, to=GH)
cv.rect(262, 52, 52, 30, "red0")
giwa(cv, 256, 40, 64, 12, roof="ink1", edge="ink2", ridge="ink0")
cv.rect(278, 62, 20, 20, "ink0"); cv.rect(280, 64, 16, 18, "brown0")  # palace gate = exit
cv.text(288, 26, "궁궐 문", "parch2", 10, anchor="ma")


def ground(x):
    if 150 <= x < 170:
        return None  # gap with a stream
    return 96 + int(6 * math.sin(x * 0.04)) - (10 if x > 230 else 0)


for x in range(W):
    gy = ground(x)
    if gy is None:
        for y in range(118, GH):
            cv.dot(x, y, "teal" if (x + y) % 5 else "teal2")
        continue
    for y in range(gy, GH):
        d = y - gy
        cv.dot(x, y, "moss2" if d < 2 else ("brown2" if d < 5 else ("brown" if (x * 3 + y) % 11 else "brown0")))
for x in range(40, 64):  # tunnel being dug downward
    for y in range(ground(x) + 2, ground(x) + 22):
        if abs(x - 52) < 5:
            cv.dot(x, y, "ink1")

# Entrance: rat hole hatch at the top left
cv.rect(10, 20, 26, 10, "brown0"); cv.rect(12, 22, 22, 6, "ink0")
cv.text(23, 8, "쥐구멍", "parch2", 10, anchor="ma")

rat = ["..KK..", ".KKKKK", "KRKKKK", ".K.K.."]


def rat_at(x, y, flip=False, col="iron"):
    cv.sprite(rat, x, y - 4, {"K": col, "R": "red2"}, outline="ink0", flip=flip)


# The procession: each rat holds the tail of the one in front
xs = [20, 30, 74, 84, 94, 104, 114, 124, 134]
for k, x in enumerate(xs):
    y = ground(x) if ground(x) else 96
    if k < 2:
        y = 36 + k * 10  # dropping from the hatch
    rat_at(x, y)
    if 0 < k and k >= 3:
        cv.line(x - 4, y - 2, x - 1, y - 2, "pink")
# Roles
bx = 52  # digger
rat_at(bx - 3, ground(bx) + 18, col="gold0")
cv.text(bx, ground(bx) + 24, "파기", "gold2", 10, anchor="ma")
rat_at(140, ground(140), col="red")  # blocker
cv.rect(139, ground(140) - 9, 8, 1, "red2")
cv.text(132, ground(140) - 30, "막기", "red2", 10, anchor="ma")
cv.line(134, ground(140) - 22, 141, ground(140) - 10, "red2")
for k in range(8):  # tail bridge across the stream
    cv.rect(150 + k * 2.6, 96 - k * 0.2, 3, 2, "pink")
rat_at(158, 95, col="flame0")
cv.text(170, 78, "꼬리 다리", "flame2", 10, anchor="ma")
for k in range(2):
    rat_at(190 + k * 14, ground(190 + k * 14))

# The crow the rats were told to follow
cv.sprite(["K....K", "KK..KK", ".KKKK.", "..KKKY", "...K.."], 214, 46, {"K": "ink0", "Y": "gold"})
for k in range(4):
    cv.dot(208 - k * 6, 54 + k, "ink2")
cv.text(222, 34, "까마귀를 따라가라", "ink0", 10, shadow="parch2", anchor="ma")

# HUD -----------------------------------------------------------------------------------------------------
cv.rect(0, GH, W, H - GH, "ink1"); cv.rect(0, GH, W, 1, "gold0")
roles = [("파기", 5), ("막기", 2), ("꼬리 다리", 3), ("나뭇잎", 4), ("올라가기", 1), ("멈춤", 0)]
for k, (name, n) in enumerate(roles):
    x = 4 + k * 38
    on = name == "꼬리 다리"
    cv.rect(x, GH + 4, 34, 30, "ink2" if not on else "flame0")
    cv.frame(x, GH + 4, 34, 30, "gold2" if on else "parch0")
    cv.text(x + 17, GH + 6, str(n), "parch2", 11, anchor="ma")
    cv.text(x + 17, GH + 19, name, "parch2" if not on else "flame2", 10, anchor="ma")
cv.text(316, GH + 5, "나온 쥐 20", "parch", 10, anchor="ra")
cv.text(316, GH + 15, "도착 12 / 15", "gold2", 10, anchor="ra")
cv.text(316, GH + 25, "남은 시간 3:20", "parch0", 10, anchor="ra")

cv.export("concept-25-retro-rats.png")
print("saved")
