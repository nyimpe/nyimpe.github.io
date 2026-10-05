"""Concept 2 — night-patrol bullet heaven (top-down village crossroads)."""
import math
from pix import *

cv = Canvas("moss0", seed=21)
rng = cv.rng
PX, PY = 160, 96  # player feet

# Ground: grass, crossroads, ruts --------------------------------------------
for _ in range(900):
    x, y = rng.randrange(W), rng.randrange(H)
    cv.dot(x, y, rng.choice(("moss", "moss", "moss2", "moss0")))
for x in range(W):
    for y in range(84, 106):
        cv.dot(x, y, "tan" if (x * 3 + y * 7) % 11 else "brown2")
for y in range(H):
    for x in range(150, 172):
        cv.dot(x, y, "tan" if (x * 5 + y * 3) % 13 else "brown2")
for x in range(W):
    cv.dot(x, 84, "moss0"); cv.dot(x, 105, "moss")
    if (x // 3) % 2:
        cv.dot(x, 90, "brown2"); cv.dot(x, 99, "brown2")
for y in range(H):
    cv.dot(150, y, "moss0"); cv.dot(171, y, "moss")


def stone_wall(x, y, n, vertical=False):
    for k in range(n):
        sx, sy = (x, y + k * 4) if vertical else (x + k * 5, y)
        cv.sprite([".GGG.", "GgGGG", "GGGGg", ".ggg."], sx, sy, {"G": "iron2", "g": "iron"}, outline="ink1")


def thatch_house(x, y, w, h):
    """Three-quarter top-down choga: rounded straw roof over a mud-wall front."""
    cv.rect(x + 3, y + h - 2, w - 6, 9, "parch0")
    for px_ in range(x + 6, x + w - 6, 9):
        cv.rect(px_, y + h - 2, 2, 9, "brown")
    cv.rect(x + w // 2 - 4, y + h + 1, 8, 6, "brown0")
    cv.rect(x + w // 2 - 3, y + h + 2, 6, 5, "orange")  # lit paper door
    cv.rect(x + w // 2, y + h + 2, 1, 5, "brown")
    cv.disc(x + w / 2, y + h / 2, w / 2, "gold0", ry=h / 2)
    cv.disc(x + w / 2, y + h / 2 - 1, w / 2 - 2, "gold", ry=h / 2 - 2)
    cv.disc(x + w / 2 - 3, y + h / 2 - 4, w / 2 - 9, "gold2", ry=h / 2 - 8)
    for k in range(-3, 4):  # rope net
        cv.line(x + w / 2 + k * 7, y + 2, x + w / 2 + k * 9, y + h - 2, "gold0")
    for k in range(1, 4):
        cv.ring(x + w / 2, y + h / 2, w / 2 * k / 4, "gold0", ry=h / 2 * k / 4)
    cv.rect(x + w // 2 - 1, y + 2, 2, h - 4, "brown2")


thatch_house(14, 10, 58, 36)
thatch_house(236, 8, 64, 40)
thatch_house(22, 120, 54, 32)
thatch_house(240, 122, 60, 34)
stone_wall(80, 70, 12)
stone_wall(182, 70, 12)
stone_wall(80, 110, 12)
stone_wall(182, 110, 12)
stone_wall(80, 4, 15, vertical=True)
stone_wall(228, 120, 14, vertical=True)

# Jangseung guardian posts at the crossing
for jx, face in ((140, "R"), (176, "B")):
    cv.sprite([
        ".KKK.",
        "KKKKK",
        "WWWWW",
        "WKWKW",
        "WWWWW",
        "WKKKW",
        "WWWWW",
        "BBBBB",
        "BWBWB",
        "BBBBB",
        "BBBBB",
        "BBBBB",
        "BBBBB",
        ".BBB.",
    ], jx, 66, {"K": "ink0", "W": "parch" if face == "R" else "parch2", "B": "brown2"}, outline="ink0")
    cv.rect(jx + 1, 74, 3, 1, "red" if face == "R" else "teal")

for tx, ty in ((110, 24), (204, 40), (118, 150), (210, 152), (300, 92), (8, 92)):
    cv.disc(tx, ty + 3, 9, "ink0", ry=5)
    cv.disc(tx, ty, 9, "moss0", ry=7)
    cv.disc(tx - 2, ty - 2, 6, "moss", ry=4)

# Night: only the lantern circle is lit -------------------------------------
cv.darken(lambda i, j: 1.3 - math.hypot((i - PX) * 0.9, (j - PY) * 1.25) / 58)

# Coins to collect
for _ in range(34):
    a, r = rng.uniform(0, 6.28), rng.uniform(10, 120)
    coin(cv, PX + r * math.cos(a), PY + r * 0.7 * math.sin(a))

# Enemies -------------------------------------------------------------------
wisp = ["...c...", "..cC.c.", "..cCcC.", ".cCWWCc", "cCWWWWc", "cCWEWEc", "cCWWWWc", ".cCWWc.", "..ccc.."]
wmap = {"c": "flame0", "C": "flame", "W": "flame2", "E": "night0"}
ghost = ["..KKKK..", ".KKKKKK.", ".KGGGGK.", ".KEGGEK.", ".KGGGGK.", "KKWWWWKK", "KWWWWWWK",
         ".WWWWWW.", ".WWgWWW.", ".WgWWgW.", "..W.W.W."]
gmap = {"K": "ink0", "G": "ghost2", "E": "red", "W": "ghost", "g": "teal3"}
blob = ["...PPPP....", ".PPPPPPPP..", "PPPPPPPPPP.", "PPRPPRPPPPp", "PPPPPPPPPPp", "PPWPWPWPPPp",
        "PPPPPPPPPpp", "PPPPPPPPPpp", ".PPPPPPPpp.", ".P.PP.PP.p."]
bmap = {"P": "purple0", "p": "purple", "R": "red2", "W": "parch2"}

spawn = []
for _ in range(220):
    a = rng.uniform(0, 6.28)
    r = rng.uniform(46, 150)
    x, y = PX + r * math.cos(a), PY + r * 0.68 * math.sin(a)
    if 236 < x < 320 and 34 < y < 110:  # keep the boss area clear
        continue
    if y < 16 or (x < 112 and y > 146) or (x > 200 and y > 150):  # keep HUD clear
        continue
    if all(math.hypot(x - sx, y - sy) > 9 for sx, sy, _ in spawn):
        bias = 0.62 if math.cos(a) < 0.3 else 0.35
        if rng.random() < bias:
            spawn.append((x, y, rng.random()))
spawn.sort(key=lambda t: t[1])
for x, y, k in spawn[:64]:
    if k < 0.55:
        cv.sprite(wisp, x, y, wmap, outline="night0")
    elif k < 0.85:
        cv.sprite(ghost, x, y, gmap, outline="ink0")
    else:
        cv.sprite(blob, x, y, bmap, outline="ink0")

# Boss: Bulgasari, the iron-eating beast that cannot be killed
L = Layer(seed=8)
bx, by = 250, 54
L.disc(bx + 22, by + 20, 21, "iron0", ry=13)
L.disc(bx + 24, by + 17, 18, "iron", ry=10)
for k in range(8):  # iron scale plates along the back
    sx = bx + 8 + k * 4
    L.sprite(["..W..", ".WIW.", "WIIIW"], sx, by + 4 + abs(k - 4), {"W": "iron2", "I": "iron"})
for lx in (bx + 8, bx + 16, bx + 30, bx + 38):  # tiger-striped legs
    L.rect(lx, by + 28, 5, 8, "orange")
    for s in range(3):
        L.rect(lx, by + 29 + s * 3, 5, 1, "ink0")
    L.rect(lx - 1, by + 35, 7, 2, "parch")
L.disc(bx + 4, by + 18, 8, "iron0", ry=7)  # head
L.disc(bx + 5, by + 16, 6, "iron", ry=5)
L.rect(bx - 4, by + 20, 6, 3, "iron")  # elephant-like trunk curling down
L.rect(bx - 6, by + 22, 3, 6, "iron")
L.rect(bx - 5, by + 27, 3, 2, "iron2")
L.rect(bx + 1, by + 14, 3, 2, "orange2"); L.dot(bx + 2, by + 14, "red")
L.rect(bx + 7, by + 14, 3, 2, "orange2"); L.dot(bx + 8, by + 14, "red")
L.line(bx - 8, by + 24, bx + 6, by + 24, "iron2")  # a sword being chewed
L.rect(bx + 6, by + 23, 2, 3, "brown")
L.line(bx + 42, by + 18, bx + 48, by + 10, "iron"); L.rect(bx + 47, by + 8, 3, 3, "ink2")  # cow tail
for k in range(26):  # needle-like fur bristling over the back
    t = k / 25
    ang = math.pi * (1.05 + 0.9 * t)
    x0 = bx + 22 + 20 * math.cos(ang); y0 = by + 20 + 12 * math.sin(ang)
    L.line(x0, y0, x0 + 4 * math.cos(ang), y0 + 4 * math.sin(ang), "iron2" if k % 2 else "iron")
L.disc(bx + 24, by + 14, 12, "iron0", ry=4)
for k in range(14):
    L.dot(bx + 14 + k * 1.5, by + 12 + (k % 3), "iron2")
L.paste(cv, outline="ink0")
cv.disc(bx + 22, by + 39, 20, "ink0", ry=2)

# Player: night watchman with a blue-and-red silk lantern ---------------------
for r_, col in ((13, "gold0"), (9, "gold")):
    for a in range(0, 360, 6):
        x = PX + 9 + r_ * math.cos(math.radians(a))
        y = PY - 7 + r_ * 0.8 * math.sin(math.radians(a))
        if (int(x) + int(y)) % 2:
            cv.dot(x, y, col)
cv.disc(PX, PY + 1, 6, "ink0", ry=2)
cv.sprite([
    "...KKKKK....",
    ".KKKKKKKKK..",
    "KkKKKRKKKkK.",
    ".KKSSSSSKK..",
    "...SESSES...",
    "...SSSSSS...",
    "..NNNNNNNN..",
    ".NNnNNNNnNN.",
    ".SNnRRRRnNS.",
    "..NNNNNNNN..",
    "..NN....NN..",
    "..KK....KK..",
], PX - 6, PY - 12, {"K": "ink0", "k": "ink2", "R": "red", "S": "skin", "E": "ink0",
                     "N": "night3", "n": "night2"}, outline="ink0")
cv.sprite([".K.", "BBB", "BYB", "RYR", "RRR", ".K."], PX + 7, PY - 10,
          {"K": "ink0", "B": "teal2", "Y": "gold2", "R": "red2"}, outline="ink0")
bar(cv, PX - 8, PY + 4, 16, 1, 0.7, "red2")

# Weapons in flight ------------------------------------------------------------
for k in range(3):  # orbiting talismans
    a = math.radians(30 + k * 120)
    x, y = PX + 22 * math.cos(a), PY - 6 + 16 * math.sin(a)
    cv.sprite(["YYY", "YRY", "YYY", "YRY", "YYY"], x, y, {"Y": "yellow", "R": "red"}, outline="ink0")
for a in range(-38, 40, 2):  # peach-branch sweep
    for r_ in (27, 28, 29):
        x = PX + r_ * math.cos(math.radians(a))
        y = PY - 6 + r_ * 0.75 * math.sin(math.radians(a))
        cv.dot(x, y, "pink" if r_ != 29 else "red2")
for a in (-30, -10, 10, 30):
    x = PX + 30 * math.cos(math.radians(a)); y = PY - 6 + 22 * math.sin(math.radians(a))
    cv.sprite([".G", "GG", "G."], x, y, {"G": "moss3"})
for stream in (150, 195, 240):  # red beans
    for k in range(5):
        a = math.radians(stream + k * 3)
        r_ = 18 + k * 11
        x, y = PX + r_ * math.cos(a), PY - 6 + r_ * 0.75 * math.sin(a)
        cv.rect(x, y, 2, 2, "red2"); cv.dot(x, y, "pink")
for a in range(0, 360, 5):  # bell ring wave
    if a % 15:
        cv.dot(PX + 44 * math.cos(math.radians(a)), PY - 6 + 32 * math.sin(math.radians(a)), "gold2")

for x, y, n in ((112, 72, "23"), (128, 112, "17"), (192, 60, "41"), (104, 96, "17"), (198, 94, "38")):
    cv.text(x, y, n, "white", 10)

# HUD -------------------------------------------------------------------------
cv.rect(0, 0, 320, 4, "ink0")
bar(cv, 1, 1, 318, 2, 0.64, "gold2", bg="ink2", edge="ink0")
cv.text(4, 5.5, "Lv 14", "gold2", 11)
cv.sprite([".RR..", "RRRK.", "YRRRR", ".RRRR", "..R.R"], 128, 7, {"R": "red2", "K": "ink0", "Y": "gold2"}, outline="ink0")
cv.text(135, 5.5, "첫닭까지 04:12", "parch2", 11)
cv.text(316, 5.5, "퇴치 1,284", "parch", 11, anchor="ra")

icons = [
    ["RR.R", "RrRR", ".RRr", "RR.R"],
    ["G..P", ".GPP", "BGG.", "B..."],
    ["YYY.", "YRY.", "YYY.", "YRY."],
    [".GG.", "GYYG", "GYYG", "GGGG"],
    ["....", ".WW.", "WWWW", "WWWW"],
    ["B.T.", ".BT.", "TB..", "..B."],
]
imaps = [{"R": "red2", "r": "pink"}, {"G": "moss3", "P": "pink", "B": "brown2"}, {"Y": "yellow", "R": "red"},
         {"G": "gold0", "Y": "gold2"}, {"W": "white"}, {"B": "brown2", "T": "moss2"}]
names = ["팥", "복숭아", "부적", "방울", "소금", "엄나무"]
for k, (ic, m) in enumerate(zip(icons, imaps)):
    x = 4 + k * 17
    panel(cv, x, 160, 15, 15, fill="ink1", edge="parch0", inner="ink2")
    cv.sprite([r.replace("", "")[0:4] for r in ic], x + 5, 163, m)
    for pip in range(4 if k < 3 else 2):
        cv.dot(x + 3 + pip * 3, 172, "gold2")
cv.text(4, 152.5, "팥 · 복숭아 가지 · 부적 · 방울 · 소금 · 엄나무", "parch0", 10)

panel(cv, 206, 158, 110, 18, fill="red0", edge="gold2", inner="red")
cv.text(261, 158.5, "진화 가능", "gold2", 10, anchor="ma")
cv.text(261, 165.5, "팥 + 가마솥 → 동지팥죽", "parch2", 10, anchor="ma")

cv.rect(250, 46, 56, 1, "ink0")
cv.text(278, 38.5, "불가살이", "orange2", 10, anchor="ma")
bar(cv, 252, 48, 52, 2, 0.83, "orange", hi="orange2")

cv.export("concept-2-bullet-heaven.png")
print("saved", len(spawn))
