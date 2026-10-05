"""Concept 4 — bestiary creature collector (turn-based encounter on painted paper)."""
import math
from pix import *

cv = Canvas("parch", seed=41)
rng = cv.rng

# Painted paper landscape ----------------------------------------------------------
for _ in range(1600):
    cv.dot(rng.randrange(W), rng.randrange(H), rng.choice(("parch0", "parch2", "parch2")))
cv.ridge(70, 22, "parch0", seed=12, freq=1.1, rough=0.6)
cv.ridge(84, 14, "moss3", seed=4, freq=1.5)
for i in range(W):  # dry-brush ink on ridge tops
    for j in range(40, 100):
        if cv.get(i, j) == P["moss3"] and cv.get(i, j - 1) not in (P["moss3"],):
            cv.dot(i, j, "moss2")
            if i % 3:
                cv.dot(i, j + 1, "moss2")
            break
cv.rect(0, 96, 320, 10, "teal3")
for k in range(24):
    x = rng.randrange(W); cv.rect(x, 98 + rng.randrange(6), rng.randrange(4, 12), 1, "white")
cv.ridge(102, 4, "moss2", seed=6, freq=2.0)
for _ in range(500):
    x, y = rng.randrange(W), rng.randrange(104, 140)
    cv.dot(x, y, rng.choice(("moss", "moss2", "moss3")))
for x, y, w in ((30, 22, 40), (150, 14, 30), (230, 30, 36)):  # cloud swirls
    cv.rect(x, y, w, 1, "parch0"); cv.rect(x + 6, y - 2, w - 14, 1, "parch0")
    cv.dot(x - 1, y - 1, "parch0"); cv.dot(x + w, y - 1, "parch0")
cv.disc(56, 30, 7, "red2"); cv.disc(56, 30, 6, "pink")  # pale sun stamp
pine(cv, 160, 96, 30, dark="ink2", mid="moss", trunk="brown0", seed=3)
pine(cv, 16, 98, 22, dark="ink2", mid="moss", trunk="brown0", seed=8)


def brush_platform(cx, cy, rx, ry):
    cv.disc(cx, cy, rx, "moss2", ry=ry)
    cv.disc(cx - 4, cy - 1, rx - 6, "moss3", ry=ry - 3)
    for a in range(10, 170, 2):
        if (a // 2) % 9 == 0:
            continue
        x = cx + rx * math.cos(math.radians(a)); y = cy + ry * math.sin(math.radians(a))
        cv.dot(x, y, "ink1"); cv.dot(x, y + 1, "ink2")


brush_platform(236, 92, 46, 9)
brush_platform(78, 134, 54, 10)

# Old tree the apparition leans on
tx = 262
for j in range(46, 92):
    w_ = 5 + (92 - j) // 18
    cv.rect(tx + int(2 * math.sin(j * 0.15)), j, w_, 1, "brown0")
    cv.dot(tx + int(2 * math.sin(j * 0.15)) + 1, j, "brown")
cv.line(tx + 2, 52, tx + 18, 40, "brown0"); cv.line(tx + 3, 56, tx + 22, 46, "brown0")
cv.line(tx + 1, 50, tx - 10, 38, "brown0")
for cx_, cy_ in ((tx + 18, 38), (tx + 24, 44), (tx - 10, 36), (tx + 6, 34)):
    cv.disc(cx_, cy_, 7, "moss", ry=3); cv.disc(cx_ - 1, cy_ - 1, 5, "moss2", ry=2)

# Gogwandaemyeon: a huge pale face under a tall stepped hat, leaning on the tree
L = Layer(seed=3)
fx, fy = 236, 46  # face centre
for j in range(36):  # long robe, leaning toward the tree
    yy = fy + 14 + j
    lean = int(j * 0.12)
    half = 6 + j * 0.28
    for i in range(int(fx - half + lean), int(fx + half + lean) + 1):
        L.dot(i, yy, "teal0" if i > fx + lean + half * 0.35 else "teal")
for side in (-1, 1):  # sleeves hanging from the shoulders
    for j in range(16):
        L.rect(fx + side * (9 + j * 0.25) - 2 + (2 if side > 0 else 0), fy + 18 + j, 4, 1, "teal0" if side > 0 else "teal")
    L.rect(fx + side * 13 - 1, fy + 33, 3, 2, "parch2")
L.disc(fx, fy, 14, "parch", ry=17)
L.disc(fx - 1, fy - 1, 13, "parch2", ry=16)
for i in range(int(fx - 12), int(fx + 12)):  # cold shadow under the chin
    L.dot(i, fy + 13 + (abs(i - fx) // 6), "ghost")
L.rect(fx - 9, fy - 5, 6, 1, "ink1"); L.rect(fx + 3, fy - 5, 6, 1, "ink1")  # brows
L.rect(fx - 8, fy - 1, 5, 1, "ink0"); L.rect(fx + 3, fy - 1, 5, 1, "ink0")  # narrowed eyes
L.dot(fx - 6, fy, "ink1"); L.dot(fx + 5, fy, "ink1")
L.rect(fx - 1, fy + 2, 2, 4, "parch0")
L.line(fx - 9, fy + 8, fx - 3, fy + 10, "red"); L.rect(fx - 3, fy + 10, 7, 1, "red"); L.line(fx + 4, fy + 10, fx + 9, fy + 8, "red")
L.line(fx - 2, fy + 7, fx - 8, fy + 12, "ink1"); L.line(fx + 2, fy + 7, fx + 8, fy + 12, "ink1")  # thin moustache
for tier, (w_, h_) in enumerate(((22, 5), (16, 6), (10, 7))):  # stepped jeongjagwan hat
    y0 = fy - 17 - sum(hh for _, hh in ((22, 5), (16, 6), (10, 7))[:tier + 1]) + 1
    L.rect(fx - w_ // 2, y0, w_, h_, "ink0")
    L.rect(fx - w_ // 2 + 1, y0 + 1, w_ - 2, 1, "ink2")
    for k in range(fx - w_ // 2 + 2, fx + w_ // 2 - 1, 3):
        L.dot(k, y0 + 2 + (k % 2), "ink2")
L.rect(fx - 13, fy - 15, 26, 2, "ink0")
L.paste(cv, outline="ink0")

# Gwigu: guardian dog with red-and-black swirls, seen from behind, eyeing the foe
L = Layer(seed=4)
L.disc(76, 126, 17, "ink1", ry=13)
L.disc(88, 110, 9, "ink1", ry=11)
L.disc(94, 97, 8, "ink1", ry=7)
L.disc(103, 99, 5, "ink1", ry=3)
for k in range(5):  # ears
    L.rect(88 + k // 2, 86 + k, 5 - k // 2, 1, "ink1")
    L.rect(96 + k // 2, 87 + k, 5 - k // 2, 1, "ink1")
for a in range(40, 320, 6):  # curled tail
    for t in range(3):
        L.dot(60 + (6 - t) * math.cos(math.radians(a)), 112 + (6 - t) * math.sin(math.radians(a)), "ink1")
L.rect(84, 134, 7, 4, "parch"); L.rect(64, 135, 9, 3, "parch")
src = [[(L.get(i, j) or (0, 0, 0, 0))[3] for j in range(H)] for i in range(W)]
for i in range(50, 112):
    for j in range(84, 140):
        if src[i][j] and (not src[i - 1][j - 1] or not src[i][j - 1]) and L.get(i, j)[:3] == P["ink1"]:
            L.dot(i, j, "ink3")
for cx_, cy_, r_ in ((72, 122, 6), (86, 128, 3), (88, 108, 4)):
    for a in range(0, 300, 8):
        rr = r_ * (0.4 + 0.6 * a / 300)
        L.dot(cx_ + rr * math.cos(math.radians(a)), cy_ + rr * math.sin(math.radians(a)), "red")
        L.dot(cx_ + rr * math.cos(math.radians(a)) + 1, cy_ + rr * math.sin(math.radians(a)), "red")
L.rect(89, 89, 2, 3, "red"); L.rect(97, 90, 2, 3, "red")
L.rect(98, 95, 2, 1, "gold2"); L.dot(99, 95, "ink0")
L.rect(107, 97, 2, 2, "ink0")
L.paste(cv, outline="ink0")

# Info boxes ------------------------------------------------------------------------
def info(x, y, w, h):
    cv.rect(x + 2, y + 2, w, h, "parch0")
    cv.rect(x, y, w, h, "parch2")
    cv.frame(x, y, w, h, "ink1")
    cv.rect(x + 1, y + h - 2, w - 2, 1, "parch0")


def badge(x, y, ch, col):
    cv.rect(x, y, 9, 8, col); cv.frame(x, y, 9, 8, "ink0")
    cv.text(x + 4.5, y + 0.5, ch, "white", 10, shadow=None, anchor="ma")


info(8, 16, 132, 38)
cv.text(13, 18, "고관대면", "ink0", 12, shadow=None)
badge(60, 19, "鬼", "red")
cv.text(134, 18.5, "Lv.12", "ink1", 10, shadow=None, anchor="ra")
cv.text(13, 28.5, "체력", "ink2", 10, shadow=None)
bar(cv, 30, 30, 104, 2, 0.46, "red", bg="parch0", edge="ink1", hi="red2")
cv.text(13, 36.5, "기록 조건  끝까지 눈을 피하지 말 것", "brown0", 10, shadow=None)
for k in range(3):
    cv.disc(17 + k * 7, 49, 2, "red" if k < 2 else "parch0")
    cv.ring(17 + k * 7, 49, 2, "ink1")
cv.text(38, 45.5, "응시 2 / 3", "ink2", 10, shadow=None)

info(178, 106, 134, 30)
cv.text(183, 108, "귀구", "ink0", 12, shadow=None)
badge(206, 109, "獸", "gold0")
cv.text(306, 108.5, "Lv.14", "ink1", 10, shadow=None, anchor="ra")
cv.text(183, 118.5, "체력", "ink2", 10, shadow=None)
bar(cv, 200, 120, 76, 2, 41 / 48, "moss", bg="parch0", edge="ink1", hi="moss2")
cv.text(306, 118, "41/48", "ink1", 10, shadow=None, anchor="ra")
bar(cv, 200, 127, 106, 1, 0.62, "teal2", bg="parch0", edge="ink1")

# Brush-stroke counter for the bestiary
cv.rect(136, 4, 84, 11, "ink1"); cv.rect(136, 15, 84, 1, "ink0")
cv.sprite(["....B", "...B.", "..B..", ".BB..", "KK..."], 140, 6, {"B": "brown2", "K": "ink0"})
cv.text(148, 4.5, "화첩  87 / 326", "parch2", 11, shadow=None)

# Dialogue + command box -----------------------------------------------------------
cv.rect(0, 142, 320, 38, "ink1")
cv.rect(0, 142, 320, 1, "gold0")
cv.rect(3, 145, 196, 32, "parch2"); cv.frame(3, 145, 196, 32, "brown0")
cv.text(8, 147.5, "고관대면이 나무에 기대어", "ink0", 11, shadow=None)
cv.text(8, 155.5, "이쪽을 가만히 내려다본다.", "ink0", 11, shadow=None)
cv.text(8, 165.5, "귀구는 무엇을 할까?", "brown", 11, shadow=None)
cv.rect(203, 145, 114, 32, "parch2"); cv.frame(203, 145, 114, 32, "brown0")
cmds = [("기술", 210, 148), ("응시", 262, 148), ("화첩에 담기", 210, 162), ("물러나기", 262, 162)]
for name, x, y in cmds:
    cv.text(x + 6, y, name, "red0" if name == "응시" else "ink0", 11, shadow=None)
cv.sprite(["R..", "RR.", "RRR", "RR.", "R.."], 262, 150, {"R": "red"})

cv.export("concept-4-creature-collector.png")
print("saved")
