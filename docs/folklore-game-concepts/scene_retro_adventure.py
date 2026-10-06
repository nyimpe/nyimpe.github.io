"""Concept 27 — point-and-click mystery after The Secret of Monkey Island (the Yu Gyeryang haunting)."""
import math
from pix import *

cv = Canvas("brown0", seed=291)
rng = cv.rng
SH = 124  # scene height

# Kitchen (buseok) interior ----------------------------------------------------------------------------------
for y in range(SH):
    for x in range(W):
        cv.dot(x, y, "tan" if rng.random() > 0.08 else "parch0")
cv.rect(0, 0, W, 14, "brown0")
for x in range(0, W, 12):
    cv.rect(x, 0, 4, 14, "brown")
cv.rect(0, 92, W, 32, "brown2")  # earthen floor
for _ in range(200):
    cv.dot(rng.randrange(W), rng.randrange(92, SH), rng.choice(("brown", "tan")))
# fire pit (agungi) with the pot knocked off
cv.rect(196, 62, 90, 30, "parch0"); cv.dither(197, 63, 88, 28, "parch0", "tan")
cv.rect(212, 76, 16, 16, "ink0"); cv.disc(220, 86, 5, "orange", ry=4)
cv.disc(262, 66, 12, "ink0", ry=4); cv.disc(262, 66, 10, "brown0", ry=2)  # empty hole where the pot sat
L = Layer(seed=2)  # the cauldron, upside down on the floor
L.disc(160, 104, 16, "iron0", ry=10); L.disc(160, 100, 14, "ink1", ry=7); L.rect(144, 104, 32, 2, "iron")
L.paste(cv, outline="ink0")
for k in range(24):  # spilled rice
    cv.dot(130 + rng.randrange(60), 108 + rng.randrange(12), "white")
L = Layer(seed=3)  # flipped soban table
L.rect(96, 98, 30, 4, "red"); L.rect(98, 102, 3, 12, "red0"); L.rect(121, 102, 3, 12, "red0")
L.paste(cv, outline="ink0")
for k in range(3):  # shelf with jars
    cv.sprite(["..KK..", ".BBBB.", "BBbBBB", "BBBBBB", ".BBBB."], 18 + k * 12, 40, {"K": "ink0", "B": "brown0", "b": "brown2"}, outline="ink0")
cv.rect(14, 46, 44, 2, "brown")
cv.rect(70, 22, 34, 46, "brown"); cv.rect(72, 24, 30, 42, "parch2")  # paper door
for gx in range(72, 102, 6):
    cv.rect(gx, 24, 1, 42, "brown")
for gy in range(24, 66, 7):
    cv.rect(72, gy, 30, 1, "brown")
for k in range(5):  # a floating bowl moved by the invisible ghost
    cv.dot(186 + k, 44 - k % 2, "parch2")
cv.sprite([".WWWW.", "WWWWWW", ".WWWW."], 184, 46, {"W": "white"}, outline="ink0")
for k in range(3):
    cv.line(182 - k * 3, 52 + k * 2, 180 - k * 3, 56 + k * 2, "ghost")

# Characters ------------------------------------------------------------------------------------------------
def person(x, feet, robe, hat=True, face_left=False):
    """About 34px tall, standing on the floor at y=feet."""
    L = Layer(seed=int(x))
    L.rect(x - 7, feet - 20, 14, 18, robe)  # robe body
    L.rect(x - 8, feet - 6, 16, 4, robe)
    L.rect(x - 5, feet - 2, 4, 2, "ink1"); L.rect(x + 1, feet - 2, 4, 2, "ink1")
    side = -1 if face_left else 1
    L.rect(x + side * 6 - (2 if side < 0 else 0), feet - 18, 3, 10, robe)  # arm
    L.disc(x + side * 7, feet - 8, 2, "skin")
    L.disc(x, feet - 25, 5, "skin", ry=6)
    if hat:
        L.rect(x - 10, feet - 30, 20, 2, "ink0")  # gat brim
        L.rect(x - 4, feet - 36, 8, 7, "ink0")
    else:
        L.disc(x, feet - 30, 5, "ink1", ry=3)
        L.disc(x + 3, feet - 33, 2, "ink1")
    L.paste(cv, outline="ink0")
    cv.dot(x + side * 2, feet - 26, "ink0"); cv.dot(x + side * 2 - 3 * side, feet - 26, "ink0")
    cv.rect(x - 1, feet - 22, 3, 1, "red0")
    cv.rect(x - 7, feet - 14, 14, 2, "red" if hat else "brown")  # sash


person(52, 118, "teal2")  # me, the investigator
person(262, 120, "parch", hat=False, face_left=True)  # Gi-yu, the house owner
cv.text(262, 70, "솥이 저절로 뒤집혔다니까요!", "pink", 10, anchor="ma")
cv.text(262, 80, "밥상도요!", "pink", 10, anchor="ma")
cv.text(64, 70, "보이지 않는 손님이로군…", "flame2", 10, anchor="ma")
cv.text(196, 30, "“밥을 다오”", "ghost2", 10, anchor="ma")

# SCUMM-style verbs and inventory ----------------------------------------------------------------------------
cv.rect(0, SH, W, H - SH, "night0")
cv.text(160, SH + 2, "체를 솥에 쓰기", "parch2", 10, anchor="ma")
verbs = ["보다", "줍다", "쓰다", "열다", "닫다", "말하다", "주다", "밀다", "당기다"]
for k, v in enumerate(verbs):
    x, y = 6 + (k % 3) * 42, SH + 14 + (k // 3) * 13
    cv.text(x, y, v, "gold2" if v == "쓰다" else "moss3", 11)
cv.rect(136, SH + 12, 180, 40, "night1"); cv.frame(136, SH + 12, 180, 40, "night3")
inv = [(["..BB..", ".B..B.", "B.BB.B", "B.BB.B", ".B..B.", "..BB.."], {"B": "brown2"}, "체"),
       (["......W", ".....W.", "....W..", "...W...", "GGW....", "GG....."], {"W": "iron2", "G": "gold"}, "은비녀"),
       ([".GGG.", "GYYYG", "GY.YG", "GYYYG", ".GGG."], {"G": "gold0", "Y": "gold2"}, "엽전"),
       (["YYY", "YRY", "YYY", "YRY", "YYY"], {"Y": "yellow", "R": "red"}, "부적"),
       (["....B", "...B.", "..B..", ".BB..", "KK..."], {"B": "brown2", "K": "ink0"}, "붓"),
       (["WWWWW", "WKKKW", "WWWWW", "WKKKW", "WWWWW"], {"W": "parch2", "K": "ink1"}, "명부")]
for k, (rows, m, name) in enumerate(inv):
    x, y = 142 + (k % 3) * 58, SH + 15 + (k // 3) * 18
    cv.sprite(rows, x, y + 2, m, outline="ink0")
    cv.text(x + 12, y + 2, name, "gold2" if name == "체" else "parch", 10)

cv.export("concept-27-retro-adventure.png")
print("saved")
