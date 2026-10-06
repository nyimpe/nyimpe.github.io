"""Concept 22 — Buyeo/Goguryeo myth MMORPG after 바람의 나라 (classic 2D online world)."""
import math
from pix import *

cv = Canvas("moss", seed=241)
rng = cv.rng
VW, VH = 240, 136  # world view

# Town tiles ---------------------------------------------------------------------------------------
for y in range(VH):
    for x in range(VW):
        cv.dot(x, y, "moss" if rng.random() > 0.08 else rng.choice(("moss2", "moss0")))
for y in range(60, 76):
    for x in range(VW):
        cv.dot(x, y, "tan" if (x + y) % 9 else "brown2")
for x in range(108, 124):
    for y in range(VH):
        cv.dot(x, y, "tan" if (x * 3 + y) % 9 else "brown2")


def tiled_house(x, y, w):
    cv.rect(x, y + 12, w, 14, "parch0"); cv.frame(x, y + 12, w, 14, "ink1")
    cv.rect(x + w // 2 - 4, y + 16, 8, 10, "brown0")
    for px_ in range(x + 3, x + w - 3, 10):
        cv.rect(px_, y + 15, 5, 5, "parch2"); cv.frame(px_, y + 15, 5, 5, "brown")
    giwa(cv, x - 2, y, w + 4, 11, roof="ink2", edge="iron", ridge="ink1")


tiled_house(10, 18, 56)
tiled_house(146, 14, 70)
tiled_house(150, 88, 50)
for tx, ty in ((84, 30), (96, 100), (20, 110), (228, 120)):
    cv.disc(tx, ty + 4, 9, "moss0", ry=4); cv.disc(tx, ty, 8, "moss2", ry=7); cv.disc(tx - 2, ty - 2, 4, "moss3", ry=3)
    cv.rect(tx - 1, ty + 5, 2, 5, "brown0")


def person(x, y, robe, hat="ink0", name=None, col="white"):
    cv.sprite(["..HH..", ".HHHH.", ".SSSS.", ".SESE.", "RRRRRR", ".RRRR.", ".R..R."], x, y,
              {"H": hat, "S": "skin", "E": "ink0", "R": robe}, outline="ink0")
    if name:
        cv.text(x + 3, y - 8, name, col, 10, anchor="ma")


person(60, 64, "teal2", name="주몽의후예")
person(88, 74, "red2", name="해명", col="pink")
person(130, 52, "parch2", name="소서노")
person(30, 66, "moss3", name="뱁새")
person(196, 60, "gold", name="유리왕자", col="gold2")
person(166, 44, "purple2", hat="gold0")  # NPC elder with a quest
cv.sprite(["Y", "Y", "Y", ".", "Y"], 168, 32, {"Y": "gold2"}, outline="ink0")
cv.text(169, 26, "금와 촌장", "gold2", 10, anchor="ma")

# Me riding Georu, the divine horse that came back leading a hundred horses
L = Layer(seed=2)
hx, hy = 116, 92
L.disc(hx, hy + 6, 10, "ink1", ry=5)
L.rect(hx - 9, hy + 9, 3, 7, "ink1"); L.rect(hx + 6, hy + 9, 3, 7, "ink1")
L.disc(hx - 11, hy + 1, 4, "ink1", ry=5)
L.rect(hx + 9, hy + 2, 5, 2, "ink2")
L.paste(cv, outline="ink0")
cv.sprite(["..HH..", ".HHHH.", ".SSSS.", ".SESE.", "RRRRRR"], hx - 3, hy - 6,
          {"H": "ink0", "S": "skin", "E": "ink0", "R": "flame"}, outline="ink0")
cv.text(hx, hy - 14, "nyimpe [거루]", "flame2", 10, anchor="ma")
for k in range(5):
    cv.dot(hx + 14 + k * 3, hy + 14, "parch0")

# Field boss: the bright, tailless great tiger Buyeo sent to Goguryeo
L = Layer(seed=3)
tx, ty = 214, 104
L.disc(tx, ty, 14, "orange", ry=8)
L.disc(tx - 13, ty - 3, 7, "orange", ry=6)
for k in range(5):
    L.rect(tx - 8 + k * 5, ty - 6, 2, 9, "ink1")
L.rect(tx - 10, ty + 6, 3, 6, "orange"); L.rect(tx + 8, ty + 6, 3, 6, "orange")
L.paste(cv, outline="ink0")
cv.rect(tx - 17, ty - 5, 2, 2, "gold2")
cv.text(tx, ty - 22, "소단미선생", "red2", 10, anchor="ma")
bar(cv, tx - 14, ty - 13, 28, 1, 0.8, "red2")

# Three-antlered deer: catch it and the whole server's penalties are pardoned
cv.sprite(["W.W.W", ".WWW.", "..BB.", ".BBBB", "BBBBB", "B...B"], 40, 96, {"W": "parch2", "B": "tan"}, outline="ink0")
cv.text(43, 88, "삼각록", "gold2", 10, anchor="ma")

# Win95-style interface ---------------------------------------------------------------------------------
def bevel(x, y, w, h, fill="iron2"):
    cv.rect(x, y, w, h, fill)
    cv.rect(x, y, w, 1, "white"); cv.rect(x, y, 1, h, "white")
    cv.rect(x, y + h - 1, w, 1, "ink1"); cv.rect(x + w - 1, y, 1, h, "ink1")


bevel(0, VH, W, H - VH)
cv.rect(3, VH + 3, 186, 38, "ink0")
chat = [("[공지] 삼각록이 졸본 동쪽에 나타났습니다.", "gold2"), ("주몽의후예: 거루 어디서 얻음?", "white"),
        ("해명: 부여 국경 퀘 깨면 줌", "pink"), ("[국가] 부여군이 성문 앞에 모였습니다", "flame2")]
for k, (line, col) in enumerate(chat):
    cv.text(6, VH + 4 + k * 9, line, col, 10, shadow=None)
bevel(VW, 0, W - VW, VH)
cv.rect(VW + 4, 4, 72, 52, "moss0"); cv.frame(VW + 4, 4, 72, 52, "ink1")
for x, y, col in ((20, 20, "white"), (40, 30, "red2"), (30, 12, "gold2"), (60, 44, "orange")):
    cv.rect(VW + 4 + x, 4 + y, 3, 3, col)
cv.text(VW + 40, 58, "졸본성 동문", "ink0", 10, shadow=None, anchor="ma")
cv.text(VW + 6, 70, "nyimpe", "ink0", 10, shadow=None)
cv.text(VW + 6, 79, "고구려 · 전사 32", "ink1", 10, shadow=None)
cv.text(VW + 6, 90, "체력", "ink0", 10, shadow=None); bar(cv, VW + 24, 93, 50, 3, 0.8, "red2", bg="ink2")
cv.text(VW + 6, 99, "마력", "ink0", 10, shadow=None); bar(cv, VW + 24, 102, 50, 3, 0.45, "flame", bg="ink2")
cv.text(VW + 6, 108, "경험", "ink0", 10, shadow=None); bar(cv, VW + 24, 111, 50, 3, 0.62, "gold", bg="ink2")
for k in range(4):
    bevel(VW + 6 + k * 18, 118, 16, 14, "iron")
    cv.text(VW + 14 + k * 18, 120, str(k + 1), "ink0", 10, shadow=None, anchor="ma")
for k, label in enumerate(("말하기", "가방", "기술", "국가")):
    bevel(192 + (k % 2) * 63, VH + 4 + (k // 2) * 19, 60, 16)
    cv.text(222 + (k % 2) * 63, VH + 7 + (k // 2) * 19, label, "ink0", 10, shadow=None, anchor="ma")

cv.export("concept-22-retro-mmo.png")
print("saved")
