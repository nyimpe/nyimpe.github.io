"""Concept 20 — memory-walk narrative after To the Moon (why Jigwi burned)."""
import math
from pix import *

cv = Canvas("tan", seed=321)
rng = cv.rng

# Temple courtyard at dusk, seen in a fading memory ---------------------------------------------------
for y in range(H):
    for x in range(W):
        cv.dot(x, y, "parch" if (x // 16 + y // 16) % 2 else "parch0")
for y in range(0, H, 16):
    cv.rect(0, y, W, 1, "tan")
for x in range(0, W, 16):
    cv.rect(x, 0, 1, H, "tan")
cv.rect(0, 0, W, 30, "brown")  # temple wall
giwa(cv, -4, 2, 328, 10, roof="ink2", edge="iron", ridge="ink1")
for x in range(8, W, 40):
    cv.rect(x, 14, 4, 16, "red0")

# Stone pagoda in the middle
px = 160
for k, (w, h) in enumerate(((44, 8), (38, 10), (32, 8), (26, 10), (20, 8), (14, 10))):
    y = 108 - sum(hh for _, hh in ((44, 8), (38, 10), (32, 8), (26, 10), (20, 8), (14, 10))[:k + 1])
    cv.rect(px - w // 2, y, w, h, "iron2" if k % 2 == 0 else "iron")
    cv.rect(px - w // 2, y, w, 1, "white")
    cv.frame(px - w // 2, y, w, h, "iron0")
cv.rect(px - 1, 44, 2, 8, "gold0")

# Jigwi asleep at the foot of the pagoda, a bracelet left on his chest
L = Layer(seed=2)
L.rect(px - 22, 112, 30, 8, "teal2")
L.disc(px - 26, 115, 5, "skin", ry=4)
L.disc(px - 29, 113, 3, "ink0", ry=2)
L.paste(cv, outline="ink0")
for r_ in (8, 5):
    for a in range(0, 360, 20):
        cv.dot(px - 10 + r_ * math.cos(math.radians(a)), 114 + r_ * 0.6 * math.sin(math.radians(a)), "gold2" if r_ == 5 else "orange")
cv.ring(px - 10, 114, 2, "gold2")

# The royal procession leaving through the gate (memory figures, faint)
for k in range(6):
    x = 236 + k * 12
    cv.sprite(["..K..", ".SSS.", "RRRRR", "RRRRR", ".R.R."], x, 40 + (k % 2), {"K": "ink1", "S": "skin", "R": "red" if k == 2 else "brown"},
              outline="ink0")
cv.rect(254, 34, 20, 14, "gold0"); cv.rect(256, 36, 16, 10, "gold"); cv.rect(258, 30, 12, 4, "red")  # palanquin

# Two underworld messengers walking his memory (drawn in cool ghost tones)
for k, x in enumerate((56, 78)):
    cv.sprite(["KKKKKKKKKKK", "....KKK....", "....SSS....", "....SES....", "...DDDDD...", "..DDDDDDD..", "..DDDDDDD..",
               "..DDDDDDD..", "...DD.DD...", "...KK.KK..."], x, 92, {"K": "ink1", "S": "ghost2", "E": "ink0", "D": "night3"},
              outline="ink0")
cv.text(72, 82, "차사 둘", "ink1", 10, shadow="parch2", anchor="ma")

# Memory links: glowing mementos to unlock the previous memory
for k, (x, y) in enumerate(((120, 70), (210, 92), (100, 128))):
    cv.disc(x, y, 4, "white"); cv.ring(x, y, 6, "gold2")
cv.text(210, 80, "팔찌", "gold0", 10, shadow="parch2", anchor="ma")

# Vignette: the memory fraying at the edges
for j in range(H):
    for i in range(W):
        d = math.hypot((i - 160) / 160, (j - 80) / 90)
        if d > 0.92 and (i + j) % 2 == 0:
            cv.dot(i, j, "parch2")
        if d > 1.05:
            cv.dot(i, j, "parch2")

# RPG-style dialogue box with portrait ----------------------------------------------------------------
cv.rect(4, 140, 312, 36, "night1"); cv.frame(4, 140, 312, 36, "parch2"); cv.frame(5, 141, 310, 34, "night3")
cv.rect(9, 144, 28, 28, "ink1"); cv.frame(9, 144, 28, 28, "parch0")
cv.sprite(["KKKKKKKKKK", "...KKKK...", "..SSSSSS..", "..SESSES..", "..SSSSSS..", "...SSSS...", ".DDDDDDDD."], 18, 152,
          {"K": "ink0", "S": "skin", "E": "ink0", "D": "ink2"})
cv.text(42, 143, "차사", "gold2", 10)
cv.text(42, 152, "글귀로 막기만 했지, 왜 타오르는지는 아무도 묻지 않았어.", "parch2", 10)
cv.text(42, 161, "이 팔찌부터 거슬러 올라가 보자.", "parch2", 10)
cv.rect(4, 4, 112, 12, "night1"); cv.frame(4, 4, 112, 12, "parch0")
cv.text(8, 5.5, "지귀의 기억 · 셋째 장면", "parch2", 10)

cv.export("concept-20-indie-memory.png")
print("saved")
