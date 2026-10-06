"""Concept 5 — underworld metroidvania (side view, boss arena under the abandoned inn)."""
import math
from pix import *

cv = Canvas("night0", seed=51)
rng = cv.rng

# Cave depths ----------------------------------------------------------------------
cv.vgrad(0, 180, ["teal0", "teal0", "night1", "night1"])
cv.ridge(150, 18, "night1", seed=2, freq=1.4)
for x in range(0, W, 1):  # stalactites hanging from the ceiling
    h = int(18 + 10 * math.sin(x * 0.07) + 6 * math.sin(x * 0.31) + (rng.random() * 3))
    cv.rect(x, 0, 1, h, "night0")
for x in range(6, W, 23):
    L_ = 10 + (x * 7) % 18
    for j in range(L_):
        w_ = max(1, 3 - j // 6)
        cv.rect(x - w_ // 2, 20 + j, w_, 1, "night0")

# Abandoned inn (won) sunk into the cave wall, in the background
bx = 150
cv.rect(bx, 76, 86, 50, "night1")
for px_ in (bx + 4, bx + 30, bx + 56, bx + 80):
    cv.rect(px_, 76, 4, 50, "teal0"); cv.rect(px_, 76, 1, 50, "night2")
giwa(cv, bx - 6, 62, 98, 13, roof="night1", edge="night2", ridge="night0")
for k in range(6):  # broken tiles
    cv.rect(bx + 10 + k * 14, 70 + (k % 2) * 3, 3, 2, "night0")
cv.rect(bx + 36, 92, 18, 34, "night0")
for j in range(92, 126, 4):
    cv.rect(bx + 36, j, 18, 1, "teal0")

# Glow mushrooms and spirit motes
def mushroom(x, y, big=False):
    for r_ in (7, 5):
        for a in range(0, 360, 10):
            xx = x + 2 + r_ * math.cos(math.radians(a)); yy = y + 1 + r_ * 0.7 * math.sin(math.radians(a))
            if (int(xx) + int(yy)) % 2:
                cv.dot(xx, yy, "teal")
    if big:
        cv.sprite([".CCCC.", "CCcCCC", "CCCCcC", "..SS..", "..SS..", ".SSSS."], x - 1, y - 3,
                  {"C": "teal3", "c": "ghost2", "S": "parch0"}, outline="ink0")
    else:
        cv.sprite([".CC.", "CCcC", ".SS.", ".SS."], x, y, {"C": "teal3", "c": "ghost2", "S": "parch0"}, outline="ink0")


# Terrain --------------------------------------------------------------------------------
def rock(x, y, w, h, top=True):
    cv.rect(x - 1, y - 1, w + 2, h + 2, "ink0")
    cv.rect(x, y, w, h, "ink2")
    for _ in range(w * h // 14):
        cv.dot(x + rng.randrange(w), y + 2 + rng.randrange(max(1, h - 2)), rng.choice(("ink3", "ink1", "ink1")))
    for i in range(x, x + w, 9):
        cv.rect(i, y, 1, h, "ink1")
    if top:
        cv.rect(x, y, w, 2, "moss")
        for i in range(x, x + w):
            if (i * 7) % 5 < 2:
                cv.dot(i, y - 1, "moss2")
            if (i * 3) % 7 == 0:
                cv.rect(i, y + 2, 1, 2, "moss0")


rock(0, 148, 96, 32)
rock(96, 160, 64, 20, top=False)
for x in range(98, 158, 6):  # bone spikes
    cv.sprite(["..W..", ".WWW.", ".WWg.", "WWWgg"], x, 155, {"W": "parch", "g": "parch0"}, outline="ink0")
rock(160, 148, 160, 32)
rock(106, 112, 40, 10)
rock(30, 100, 34, 8)
mushroom(14, 142, big=True); mushroom(70, 144); mushroom(118, 107); mushroom(36, 95); mushroom(300, 143, big=True)
for _ in range(36):
    x, y = rng.randrange(W), rng.randrange(30, 150)
    cv.dot(x, y, rng.choice(("teal3", "ghost2", "gold2")))

# Stone lanterns lighting the arena
for lx in (176, 226):
    cv.sprite([".KKKK.", "KGGGGK", ".GOOG.", ".GYOG.", ".GGGG.", "..GG..", "..GG..", ".GGGG."], lx, 140 - 8,
              {"K": "ink2", "G": "iron", "O": "orange", "Y": "gold2"}, outline="ink0")

# Boss: Daeogong, the giant centipede of the abandoned inn ---------------------------
L = Layer(seed=9)
pts = []
for k in range(26):
    t = k / 25
    x = 330 - 40 * t - 50 * math.sin(t * 2.6)
    y = 176 - 112 * t + 18 * math.sin(t * 5.0)
    pts.append((x, y))
for k, (x, y) in enumerate(pts[:-1]):
    nx, ny = pts[k + 1]
    ang = math.atan2(ny - y, nx - x) + math.pi / 2
    for side in (-1, 1):
        lx0 = x + side * 6 * math.cos(ang); ly0 = y + side * 6 * math.sin(ang)
        kx = lx0 + side * 5 * math.cos(ang) - 2; ky = ly0 + side * 5 * math.sin(ang) + 2
        L.line(lx0, ly0, kx, ky, "gold0")
        L.line(kx, ky, kx - 2, ky + 4, "gold2")
for k, (x, y) in enumerate(pts[:-1]):
    r_ = 7 + 2 * (k / 25)
    L.disc(x, y, r_, "red0")
    L.disc(x - 1, y - 1, r_ - 2, "red")
    L.disc(x - 2, y - 3, r_ - 5, "orange")
    L.dot(x - 3, y - 4, "orange2")
    if k:
        px0, py0 = pts[k - 1]
        back = math.atan2(py0 - y, px0 - x)
        for d in range(-80, 81, 6):
            a = back + math.radians(d)
            L.dot(x + (r_ - 1) * math.cos(a), y + (r_ - 1) * math.sin(a), "red0")
            L.dot(x + r_ * math.cos(a), y + r_ * math.sin(a), "ink0")
hx, hy = pts[-1]
L.disc(hx, hy, 11, "red0", ry=9)
L.disc(hx - 1, hy - 1, 9, "red", ry=7)
L.disc(hx - 3, hy - 4, 4, "orange", ry=2)
for side in (-1, 1):  # mandibles
    for k in range(9):
        a = math.radians(200 + side * (20 + k * 8))
        L.rect(hx - 8 + 12 * math.cos(a) * 0.6 - k * 0.6, hy + side * 3 + k * 0.4 * side + 4, 2, 2, "parch")
L.rect(hx - 6, hy - 3, 3, 3, "gold2"); L.dot(hx - 5, hy - 2, "ink0")
L.rect(hx + 1, hy - 4, 3, 3, "gold2"); L.dot(hx + 2, hy - 3, "ink0")
for side, (ex, ey) in ((-1, (hx - 30, hy - 30)), (1, (hx + 6, hy - 40))):  # antennae
    mx, my = (hx + ex) / 2 + side * 6, (hy + ey) / 2 - 6
    L.line(hx - 2, hy - 7, mx, my, "gold0"); L.line(mx, my, ex, ey, "gold0")
L.paste(cv, outline="ink0")

# Player: apprentice underworld messenger mid double-jump --------------------------
PX, PY = 112, 74
pl = [
    ".....KKKK.....",
    ".....KkkK.....",
    "..kKKKKKKKKk..",
    ".....HSSS.....",
    ".....HSES.....",
    ".....HSSS.....",
    "....DDDDDD....",
    "...DDDRDDDD...",
    "..DDDDRDDDDSS.",
    ".SDDDDRDDDD...",
    "...DDRRRRDD...",
    "...DDDDDDDD...",
    "..DDDDDDDDDD..",
    "..DDDDD.DDDD..",
    ".DDDD....DDD..",
    ".DD.......DD..",
    "SS.........K..",
]
for k, (ox, oy) in enumerate(((-24, 22), (-12, 11))):  # afterimages
    for j, row in enumerate(pl):
        for i, ch in enumerate(row):
            if ch not in ". " and (i + j + k) % 2:
                cv.dot(PX + ox + i, PY + oy + j, "teal" if k == 0 else "teal2")
for r_ in range(14, 8, -1):
    for a in range(0, 360, 8):
        x = PX + 7 + r_ * math.cos(math.radians(a)); y = PY + 8 + r_ * math.sin(math.radians(a))
        if (int(x) + int(y)) % 2 and r_ > 11:
            cv.dot(x, y, "teal")
cv.sprite(pl, PX, PY, {"K": "ink0", "k": "ink3", "H": "ink1", "S": "skin", "E": "ink0", "D": "ink1", "R": "red2"},
          outline="ghost2")
for a in range(0, 360, 12):  # one-legged hop shockwave
    x = PX + 2 + 9 * math.cos(math.radians(a)); y = PY + 19 + 2.5 * math.sin(math.radians(a))
    cv.dot(x, y, "gold2" if a % 24 else "parch2")
for x, y in ((PX - 6, PY + 22), (PX + 10, PY + 23), (PX - 2, PY + 25), (PX + 6, PY + 26)):
    cv.dot(x, y, "gold2")

# HUD --------------------------------------------------------------------------------------
for k in range(6):
    x = 6 + k * 9
    filled = k < 4
    cv.rect(x, 5, 7, 11, "ink0")
    cv.rect(x + 1, 6, 5, 9, "yellow" if filled else "ink2")
    if filled:
        cv.rect(x + 3, 7, 1, 7, "red"); cv.rect(x + 2, 9, 3, 1, "red")
bar(cv, 7, 19, 52, 2, 0.7, "teal2", hi="teal3")
cv.text(62, 16.5, "혼불", "teal3", 10)

mx, my = 262, 4
cv.rect(mx - 1, my - 1, 56, 34, "ink0"); cv.rect(mx, my, 54, 32, "night1")
rooms = [(0, 1, 2, 1), (2, 1, 1, 2), (3, 2, 2, 1), (5, 0, 1, 3), (1, 3, 3, 1), (4, 3, 1, 1), (6, 1, 1, 1)]
for rx, ry, rw, rh in rooms:
    cv.rect(mx + 3 + rx * 7, my + 3 + ry * 7, rw * 7 - 1, rh * 7 - 1, "teal")
cv.rect(mx + 3 + 3 * 7, my + 3 + 2 * 7, 2 * 7 - 1, 6, "red2")
cv.dot(mx + 3 + 3 * 7 + 6, my + 3 + 2 * 7 + 3, "white")
cv.text(mx + 27, my + 33, "남굴북벽", "parch0", 10, anchor="ma")

# Ability banner (scroll)
sx, sy, sw = 92, 22, 136
cv.rect(sx, sy, sw, 22, "parch2"); cv.frame(sx, sy, sw, 22, "brown0")
cv.rect(sx - 4, sy - 2, 4, 26, "brown"); cv.rect(sx + sw, sy - 2, 4, 26, "brown")
cv.rect(sx - 4, sy - 2, 4, 1, "brown2"); cv.rect(sx + sw, sy - 2, 4, 1, "brown2")
cv.text(sx + sw / 2, sy + 1.5, "능력 획득 · 독각의 외발 도약", "red0", 11, shadow=None, anchor="ma")
cv.text(sx + sw / 2, sy + 11.5, "공중에서 한 발로 한 번 더 뛴다", "brown", 10, shadow=None, anchor="ma")

# Boss bar
cv.rect(40, 168, 240, 10, "ink0")
cv.text(160, 163, "대오공 · 버려진 원(院)의 주인", "orange2", 11, anchor="ma")
bar(cv, 44, 174, 232, 2, 0.78, "red2", hi="orange")

cv.export("concept-3-metroidvania.png")
print("saved")
