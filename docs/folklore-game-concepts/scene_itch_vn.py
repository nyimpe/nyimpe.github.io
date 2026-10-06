"""Concept 30 — meta-horror visual novel after Doki Doki Literature Club (a poetry circle of disguised spirits)."""
import math
from pix import *

cv = Canvas("parch", seed=421)
rng = cv.rng
DY = 126  # dialogue box top

# Spring study room ----------------------------------------------------------------------------------------------
cv.rect(0, 0, W, DY, "parch")
cv.rect(0, 0, W, 6, "brown0"); cv.rect(0, 6, W, 2, "brown")
for x in (0, 90, 174, 316):
    cv.rect(x, 0, 6, DY, "brown"); cv.rect(x + 1, 0, 1, DY, "brown2")
# Open lattice window with plum blossoms outside
cv.rect(98, 14, 70, 70, "teal3")
cv.vgrad(14, 84, ["teal3", "parch2"], x0=98, x1=168)
for k in range(5):
    bx, by = 102 + k * 13, 70 - (k % 3) * 18
    cv.line(bx, by, bx + 10, by - 8, "brown0")
    for f in range(3):
        cv.sprite([".P.", "PWP", ".P."], bx + f * 4, by - 6 - f * 3, {"P": "pink", "W": "white"})
cv.frame(98, 14, 70, 70, "brown0"); cv.frame(97, 13, 72, 72, "brown")
for x in range(98, 168, 14):
    cv.rect(x, 14, 1, 70, "brown2")
cv.rect(98, 48, 70, 1, "brown2")
# Paper doors either side
for x0, w in ((8, 78), (182, 130)):
    cv.rect(x0, 16, w, 104, "parch2")
    for x in range(x0, x0 + w, 11):
        cv.rect(x, 16, 1, 104, "tan")
    for y in range(16, 120, 13):
        cv.rect(x0, y, w, 1, "tan")


def girl(L, cx, hair, jeogori, skirt, eyes="ink0", white_hair=False):
    """Bust of a girl in hanbok; head centre at (cx, 56)."""
    L.disc(cx, 60, 15, hair, ry=17)                      # hair mass behind
    L.rect(cx - 15, 60, 30, 46, hair)                    # long hair down the back
    L.disc(cx, 112, 30, skirt, ry=20)                     # chima
    L.disc(cx, 92, 19, jeogori, ry=13)                    # jeogori
    L.rect(cx - 20, 92, 40, 12, jeogori)
    L.rect(cx - 4, 78, 8, 6, "skin")                      # neck
    L.disc(cx, 58, 12, "skin", ry=13)                     # face
    L.disc(cx, 47, 13, hair, ry=6)                        # bangs
    for s in (-1, 1):
        L.rect(cx + s * 12 - (1 if s < 0 else 0), 50, 2, 16, hair)
    L.rect(cx - 6, 61, 3, 3, eyes); L.rect(cx + 4, 61, 3, 3, eyes)
    L.dot(cx - 6, 61, "white"); L.dot(cx + 4, 61, "white")
    L.rect(cx - 9, 66, 3, 1, "pink"); L.rect(cx + 7, 66, 3, 1, "pink")
    L.rect(cx - 1, 69, 3, 1, "red")
    L.line(cx - 6, 84, cx, 92, "white"); L.line(cx + 6, 84, cx, 92, "white")   # collar


# Yeoni (lovesick snake) with her jar --------------------------------------------------------------------------------
L = Layer(seed=2)
girl(L, 48, "ink1", "moss3", "red")
L.rect(47, 92, 2, 10, "red2")  # goreum ribbon
L.disc(48, 106, 12, "brown", ry=10); L.rect(40, 94, 16, 4, "brown0")  # jar held at the chest
L.paste(cv, outline="ink0")
pts = [(50 + 8 * math.sin(k * 0.5), 95 - k * 1.5) for k in range(16)]  # a snake slipping out of the jar
for x, y in pts:
    cv.disc(x, y, 3.2, "ink0")
for k, (x, y) in enumerate(pts):
    cv.disc(x, y, 2.4, "moss")
    cv.dot(x - 1, y, "moss3")
    if k % 2:
        cv.dot(x + 1, y + 1, "moss0")
hx, hy = pts[-1]
cv.sprite([".GGGG.", "GGGGGG", "GRGGRG", "GGGGGG", ".GGGG."], int(hx) - 3, int(hy) - 6, {"G": "moss", "R": "red"}, outline="ink0")
cv.sprite(["R.R", ".R.", ".R."], int(hx) - 1, int(hy) - 1, {"R": "red2"})
cv.text(48, 18, "연이", "brown0", 10, shadow="parch2", anchor="ma")

# Hwangyeon (shows the face you will love) ---------------------------------------------------------------------------
L = Layer(seed=3)
girl(L, 132, "ink0", "pink", "purple2")
L.paste(cv, outline="ink0")
# Glitch: rows slide sideways and the true form, limp blue-haired cloth, shows through
for y in range(46, 80):  # right half of the face: limp cloth with blue hair
    for x in range(133, 147):
        if cv.get(x, y) in (P["skin"], P["ink0"], P["pink"], P["red"], P["white"]) and (x + y // 2) % 4:
            cv.dot(x, y, "teal2" if (x * 3 + y) % 5 else "ghost")
for y0, h, off in ((62, 2, 5), (90, 3, -7)):
    rows = [[cv.get(x, y) for x in range(100, 166)] for y in range(y0, y0 + h)]
    for j, row in enumerate(rows):
        for i, col in enumerate(row):
            cv.dot(100 + (i + off) % 66, y0 + j, col)
cv.text(132, 18, "황연", "brown0", 10, shadow="parch2", anchor="ma")

# Hiya (white fox) sitting where you sat ------------------------------------------------------------------------------
L = Layer(seed=4)
girl(L, 216, "white", "ghost2", "teal2", eyes="red")
for s in (-1, 1):  # fox ears
    L.sprite(["..W", ".WW", "WPW", "WWW"] if s < 0 else ["W..", "WW.", "WPW", "WWW"], 216 + s * 9 - 1, 36,
             {"W": "white", "P": "pink"})
L.paste(cv, outline="ink2")
cv.text(216, 18, "희야", "brown0", 10, shadow="parch2", anchor="ma")

# Meta window: the cast list file --------------------------------------------------------------------------------------
WX, WY, WW, WH = 248, 24, 66, 76
cv.rect(WX + 2, WY + 2, WW, WH, "ink2")
cv.rect(WX, WY, WW, WH, "white"); cv.frame(WX, WY, WW, WH, "ink1")
cv.rect(WX, WY, WW, 10, "night2")
cv.text(WX + 4, WY + 0.5, "명부 폴더", "white", 10, shadow=None)
cv.rect(WX + WW - 9, WY + 2, 6, 6, "red2")
files = [("연이.명", "ink0"), ("황연.명", "ink0"), ("희야.명", "ink0"), ("나.명", "ink3")]
for k, (name, col) in enumerate(files):
    y = WY + 13 + k * 12
    cv.sprite(["KKKK.", "KWWKK", "KWWWK", "KWWWK", "KKKKK"], WX + 5, y + 1, {"K": col, "W": "white"})
    cv.text(WX + 14, y - 1, name, col, 10, shadow=None)
cv.rect(WX + 13, WY + 13 + 3 * 12 + 5, 26, 1, "red2")
cv.text(WX + 33, WY + 13 + 4 * 12 - 2, "찾을 수 없음", "red2", 10, shadow=None, anchor="ma")

# Dialogue box --------------------------------------------------------------------------------------------------------
cv.rect(0, DY, W, H - DY, "ink2")
cv.rect(8, DY + 8, W - 16, H - DY - 12, "white"); cv.frame(8, DY + 8, W - 16, H - DY - 12, "pink")
cv.rect(16, DY, 46, 14, "pink"); cv.frame(16, DY, 46, 14, "white")
cv.text(39, DY + 1.5, "희야", "white", 11, shadow="red", anchor="ma")
cv.text(18, DY + 17, "여기, 원래 네 자리였니?", "ink1", 11, shadow=None)
cv.text(18, DY + 30, "이제 명부에 네 이름은 없어. 시는 내가 대신 쓸게.", "red", 11, shadow=None)
for k, s in enumerate(("기록", "자동", "넘기기", "저장", "불러오기", "설정")):
    cv.text(150 + k * 27, DY + 44, s, "ink3", 10, shadow=None, anchor="ma")

cv.export("concept-30-itch-vn.png")
print("saved")
