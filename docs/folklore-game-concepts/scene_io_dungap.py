"""Concept 17 — Dungap.io: foxes disguise as market goods, hunters sniff them out (Prop Hunt)."""
import math
from pix import *
from io_ui import tag, nick

cv = Canvas("tan", seed=191)
rng = cv.rng

# Market ground ----------------------------------------------------------------------------------
for _ in range(1500):
    cv.dot(rng.randrange(W), rng.randrange(H), rng.choice(("parch0", "brown2", "tan")))
cv.rect(0, 84, W, 18, "parch0")  # main alley
for _ in range(300):
    cv.dot(rng.randrange(W), rng.randrange(84, 102), rng.choice(("parch", "tan")))


def stall(x, y, w, cloth="white"):
    cv.rect(x, y + 10, w, 14, "brown")  # counter
    cv.rect(x, y + 10, w, 2, "brown2")
    for px_ in (x + 1, x + w - 3):
        cv.rect(px_, y, 2, 24, "brown0")
    cv.rect(x - 2, y - 2, w + 4, 8, cloth)  # awning
    for k in range(x - 2, x + w + 2, 6):
        cv.rect(k, y + 6, 3, 2, cloth)
    cv.frame(x - 2, y - 2, w + 4, 8, "parch0")


jar = [".KKK.", "KbBBK", "BbBBB", "BBBBB", "BBBbB", ".BBB."]
straw = ["..Y.Y..", ".YYYYY.", "YYyYYyY", "YYYYYYY", ".YYrYY.", "YYYYYYY", ".Y.Y.Y."]
jige = ["B...B", "BB.BB", "B.B.B", "B...B", "BBBBB", "B...B", "B...B"]
for x, y, w, cloth in ((16, 30, 54, "white"), (96, 26, 60, "parch2"), (190, 32, 50, "white"), (40, 118, 56, "parch2"),
                       (180, 120, 64, "white")):
    stall(x, y, w, cloth)
for k in range(8):  # rows of onggi jars
    cv.sprite(jar, 96 + k * 8, 54, {"K": "ink0", "B": "brown0", "b": "brown2"}, outline="ink0")
for k in range(5):
    cv.sprite(straw, 252 + (k % 3) * 9, 44 + (k // 3) * 9, {"Y": "gold", "y": "gold0", "r": "brown"}, outline="ink0")
cv.sprite(jige, 16, 66, {"B": "brown2"}, outline="ink0")
cv.sprite(jige, 24, 66, {"B": "brown2"}, outline="ink0")

# Seated villagers, and one white fox sitting in a person's seat
villager = ["..KK..", ".SSSS.", ".SESE.", "WWWWWW", "WWWWWW", ".W..W."]
for x, y, col in ((58, 140, "parch2"), (72, 140, "teal3"), (204, 144, "parch2")):
    cv.sprite(villager, x, y, {"K": "ink0", "S": "skin", "E": "ink0", "W": col}, outline="ink0")
cv.sprite(villager, 86, 140, {"K": "ink0", "S": "skin", "E": "ink0", "W": "parch2"}, outline="ink0")
cv.dot(93, 146, "white"); cv.dot(94, 147, "white")  # a white tail tip peeking out

# A fox mid-transformation into a straw bundle (poof)
for a in range(0, 360, 20):
    r = 9 + (a % 40) / 10
    cv.disc(268 + r * math.cos(math.radians(a)), 72 + r * 0.7 * math.sin(math.radians(a)), 2.5, "parch2")
cv.sprite(["W....W", "WW..WW", "WWWWWW", "WEWWEW", ".WWWW."], 262, 64, {"W": "white", "E": "red2"}, outline="ink0")
cv.sprite(straw, 263, 71, {"Y": "gold", "y": "gold0", "r": "brown"}, outline="ink0")

# Hunters: the yellow dog barks at the jar row, the mirror reveals a fox in the straw
DX, DY = 150, 76
cv.sprite(["..YY......", ".YYYY...YY", "YKYYYYYYY.", ".YYYYYYYY.", ".Y.Y..Y.Y."], DX, DY,
          {"Y": "gold", "K": "ink0"}, outline="ink0")
for r_ in (10, 15, 20):
    for a in range(200, 340, 8):
        cv.dot(DX + 2 + r_ * math.cos(math.radians(a)), DY + 2 + r_ * 0.6 * math.sin(math.radians(a)), "red2")
cv.text(DX - 10, DY - 4, "멍!", "red2", 11, anchor="ma")
hunter = ["..KKKK..", ".KKKKKK.", "..SSSS.I", "..SESE.I", ".BBBBBBI", "BBBBBBB.", ".BB..BB.", ".KK..KK."]
cv.sprite(hunter, 166, 86, {"K": "ink0", "S": "skin", "E": "ink0", "B": "brown0", "I": "iron2"}, outline="ink0")
nick(cv, 170, 96, "포수 막쇠 (나)", "gold2")
cv.sprite(hunter, 228, 92, {"K": "ink0", "S": "skin", "E": "ink0", "B": "teal0", "I": "iron2"}, outline="ink0")
nick(cv, 232, 104, "포수 순덕", "parch2")
for t in range(4, 30):  # mirror beam toward the straw bundles
    half = t * 0.35
    for d in range(-int(half), int(half) + 1):
        if (t + d) % 2:
            cv.dot(236 + t * 0.9, 90 - t * 0.7 + d, "ghost2")
cv.disc(236, 92, 3, "gold"); cv.disc(236, 92, 2, "ghost2")

# HUD ------------------------------------------------------------------------------------------------
cv.rect(110, 0, 100, 22, "ink0"); cv.frame(110, 0, 100, 22, "gold0")
cv.text(160, 1.5, "포수 팀 · 1:24", "gold2", 11, anchor="ma")
cv.text(160, 11, "숨은 여우 3 / 6", "parch2", 10, anchor="ma")
tag(cv, 4, 4, "명절 · 단오 — 그네 뛰는 장터")
tag(cv, 4, 18, "판마다 포수와 여우를 바꾼다", fg="ghost2", edge="night3")
for k, (name, state, col) in enumerate((("누렁개", "가능", "moss3"), ("거울", "8초", "parch0"), ("엽총", "2발", "parch2"))):
    x = 4 + k * 56
    cv.rect(x, 162, 52, 14, "ink0"); cv.frame(x, 162, 52, 14, "ink2")
    cv.text(x + 4, 164, name, "parch", 10)
    cv.text(x + 48, 164, state, col, 10, anchor="ra")
cv.rect(176, 162, 140, 14, "ink0"); cv.frame(176, 162, 140, 14, "gold0")
cv.text(246, 164, "둔갑 해금 · 지게 (여우로 5판 생존)", "gold2", 10, anchor="ma")
cv.rect(258, 0, 62, 22, "ink0"); cv.frame(258, 0, 62, 22, "ink2")
cv.text(289, 1.5, "판 점수", "parch0", 10, anchor="ma")
cv.text(289, 10, "포수 2 : 1 여우", "parch2", 10, anchor="ma")

cv.export("concept-17-io-dungap.png")
print("saved")
