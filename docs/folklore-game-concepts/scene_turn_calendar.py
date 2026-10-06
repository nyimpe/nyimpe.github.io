"""Concept 39 — calendar RPG after Persona 5 (a Seonggyungwan student's double life inside a road-blocking mouth)."""
import math
from pix import *

cv = Canvas("red", seed=511)
rng = cv.rng

# Inside the great mouth: red flesh, black diagonal bands, teeth at top and bottom -------------------------------------
for j in range(H):
    for i in range(W):
        if (i + j * 2) // 22 % 3 == 0:
            cv.dot(i, j, "red0")
for k in range(-10, W, 40):  # big teeth framing the view
    for j in range(16):
        w = 36 - j * 2
        cv.rect(k + (36 - w) / 2, j, w, 1, "parch2")
        cv.rect(k + 20 + (36 - w) / 2, H - 1 - j, w, 1, "parch2")
    cv.line(k, 0, k + 18, 16, "ink0"); cv.line(k + 36, 0, k + 18, 16, "ink0")
    cv.line(k + 20, H - 1, k + 38, H - 17, "ink0"); cv.line(k + 56, H - 1, k + 38, H - 17, "ink0")
# A blue-robed child spirit waits deep in the throat
cv.disc(250, 70, 18, "red0", ry=20); cv.disc(250, 72, 13, "ink0", ry=15)
cv.sprite(["..KK..", ".SSSS.", ".SKSK.", "BBBBBB", "BBBBBB", ".B..B."], 247, 64, {"K": "ink0", "S": "skin", "B": "flame0"})

# The knocked-down enemy: bulging eyes, flat nose, long mouth, red and blue body --------------------------------------
L = Layer(seed=3)
ex, ey = 220, 112
L.disc(ex, ey, 26, "flame0", ry=12)
L.disc(ex - 8, ey - 2, 14, "red2", ry=8)
L.disc(ex - 30, ey - 6, 11, "red2", ry=9)
for s_ in (-1, 1):
    L.disc(ex - 30 + s_ * 9, ey + 2, 3, "red", ry=7)                # drooping ears
for lx in (ex - 16, ex + 14):
    L.rect(lx, ey - 18, 5, 8, "flame0")                              # legs in the air
L.paste(cv, outline="ink0")
for s_ in (-1, 1):
    cv.disc(ex - 30 + s_ * 4, ey - 10, 3, "white"); cv.dot(ex - 30 + s_ * 4, ey - 10, "ink0")
cv.rect(ex - 40, ey - 2, 12, 2, "ink0")                             # long mouth
for k in range(3):  # dizzy stars
    a = k * 2.1
    cv.sprite([".Y.", "YYY", ".Y."], ex - 32 + 12 * math.cos(a), ey - 24 + 4 * math.sin(a), {"Y": "gold2"})
cv.rect(ex - 46, ey + 16, 68, 12, "ink0")
cv.text(ex - 12, ey + 17.5, "약점! 쓰러짐", "gold2", 10, anchor="ma")
cv.text(ex + 4, ey - 34, "출목축비", "white", 11, shadow="ink0", anchor="ma")

# Player student lunging, with Taejae the questioning child spirit behind ----------------------------------------------
L = Layer(seed=4)
px, py = 92, 104
L.disc(px, py, 7, "skin", ry=7)
L.rect(px - 8, py - 12, 16, 4, "ink0"); L.rect(px - 4, py - 16, 8, 5, "ink0")   # scholar's hat
L.rect(px - 7, py + 6, 16, 18, "flame0")                                         # blue robe
L.line(px + 8, py + 10, px + 30, py + 4, "parch2"); L.line(px + 8, py + 11, px + 30, py + 5, "parch2")  # brush-sword
L.rect(px - 6, py + 24, 5, 8, "ink1"); L.rect(px + 3, py + 24, 5, 8, "ink1")
L.paste(cv, outline="ink0")
cv.dot(px + 2, py, "ink0")
for k in range(10):  # Taejae: a pale child spirit rising from a pouch
    cv.disc(px - 22, py - 10 - k * 2, 9 - k * 0.5, "ghost")
cv.disc(px - 22, py - 32, 7, "ghost2")
cv.dot(px - 24, py - 33, "ink0"); cv.dot(px - 20, py - 33, "ink0")
cv.rect(px - 26, py + 14, 8, 8, "red2"); cv.frame(px - 26, py + 14, 8, 8, "ink0")      # the pouch
cv.text(px - 22, py - 50, "태재", "white", 10, anchor="ma")

# ONE MORE splash ---------------------------------------------------------------------------------------------------
for j in range(28):
    x0 = 100 + j * 0.9
    cv.rect(x0, 18 + j, 150, 1, "ink0")
cv.text(186, 22, "한 번 더!", "white", 20, shadow="red", anchor="ma")

# Calendar ----------------------------------------------------------------------------------------------------------
for j in range(30):
    cv.rect(4 - j * 0.2, 18 + j, 76, 1, "white")
cv.text(41, 20, "4월 12일 · 밤", "ink0", 11, shadow=None, anchor="ma")
cv.rect(10, 36, 58, 10, "red"); cv.text(39, 36.5, "과거까지 47일", "white", 10, shadow=None, anchor="ma")

# Command list and party ------------------------------------------------------------------------------------------------
cmds = ["치기", "넋 부르기", "막기", "도구"]
for k, c in enumerate(cmds):
    x, y = 6 + k * 3, 120 + k * 12
    cv.rect(x, y, 46, 10, "ink0" if k != 1 else "white")
    cv.text(x + 23, y + 0.5, c, "white" if k != 1 else "ink0", 10, shadow=None, anchor="ma")
party = [("나", 0.8, 0.6), ("단이", 0.6, 0.9), ("막동", 0.9, 0.3)]
for k, (nm, hp, sp) in enumerate(party):
    x, y = 252, 124 + k * 15
    for j in range(13):
        cv.rect(x - j * 0.4, y + j, 64, 1, "ink0")
    cv.text(x + 4, y + 1, nm, "white", 10, shadow=None)
    bar(cv, x + 30, y + 3, 30, 2, hp, "moss3", edge="ink0")
    bar(cv, x + 30, y + 8, 30, 2, sp, "pink", edge="ink0")

cv.export("concept-39-turn-calendar.png")
print("saved")
