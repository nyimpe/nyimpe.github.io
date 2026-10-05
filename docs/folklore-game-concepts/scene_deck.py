"""Concept 1 — talisman roguelike deckbuilder (battle screen)."""
from pix import *

cv = Canvas("night0", seed=11)

# Sky, moon, mountains -------------------------------------------------------
cv.vgrad(12, 104, ["night0", "night1", "night1", "night2"])
cv.stars(70, 70)
cv.disc(262, 36, 16, "night2")
cv.disc(262, 36, 13, "parch")
cv.disc(264, 34, 11, "parch2")
for dx, dy, r in ((-4, 2, 2), (3, -3, 1.5), (5, 5, 1.5)):
    cv.disc(262 + dx, 36 + dy, r, "parch")
cv.ridge(78, 16, "night2", seed=3, freq=1.2)
cv.ridge(90, 10, "teal0", seed=7, freq=1.6)
for x, y, w in ((206, 47, 26), (176, 52, 12), (230, 58, 18)):  # moonlit cloud streaks
    cv.rect(x, y, w, 1, "night3"); cv.rect(x + 4, y + 1, w - 8, 1, "night2")

# Mountain temple silhouette
cv.rect(102, 82, 52, 14, "ink1")
giwa(cv, 96, 72, 64, 10, roof="ink0", edge="ink1", ridge="ink0")
for i in range(3):
    cv.rect(110 + i * 14, 85, 8, 9, "orange")
    cv.rect(110 + i * 14, 85, 8, 1, "orange2")
    cv.rect(113 + i * 14, 85, 1, 9, "brown"); cv.rect(110 + i * 14, 89, 8, 1, "brown")
pine(cv, 82, 98, 26, dark="ink0", mid="moss0", trunk="ink0", seed=4)
pine(cv, 176, 98, 20, dark="ink0", mid="moss0", trunk="ink0", seed=9)
pine(cv, 306, 100, 30, dark="ink0", mid="moss0", trunk="ink0", seed=2)

# Courtyard stones
cv.rect(0, 98, 320, 82, "ink1")
for row, y in enumerate(range(98, 122, 6)):
    off = 0 if row % 2 else 9
    for x in range(-off, 320, 18):
        shade = "ink3" if (x // 18 + row) % 3 == 0 else "ink2"
        cv.rect(x + 1, y + 1, 16, 4, shade)
        cv.rect(x + 1, y + 1, 16, 1, "ink3" if shade == "ink2" else "parch0")
cv.darken(lambda i, j: 1 if j < 108 else max(0.0, 1 - (j - 108) / 18))

# Stone lantern
cv.sprite([
    "..KKKKKK..",
    ".KGGGGGGK.",
    "KGGGGGGGGK",
    "...GOOG...",
    "...GOYG...",
    "...GOOG...",
    "..GGGGGG..",
    "....GG....",
    "....GG....",
    "....GG....",
    "...GGGG...",
    "..GGGGGG..",
], 22, 86, {"K": "ink2", "G": "iron", "O": "orange", "Y": "gold2"}, outline="ink0")

# Shadows
for cx, rw in ((54, 10), (208, 22)):
    cv.disc(cx, 106, rw, "ink0", ry=2)

# Player: exorcist scholar in gat and dopo, holding a talisman forward
player = [
    ".......KKKK.......",
    ".......KkkK.......",
    ".......KkkK.......",
    ".......KKKK.......",
    "..kKKKKKKKKKKKKk..",
    ".......HSSSS......",
    ".......HSSES......",
    ".......HSSSS......",
    "........sSS.......",
    ".......TWWWW......",
    "......wWWWWWW.....",
    ".....wwWWWWWWW....",
    ".....wwWWWWWWSYYY.",
    ".....wwWWWWWW.YrY.",
    ".....wwWWWWWW.YrY.",
    ".....wwRRRRRR.YrY.",
    ".....wwWWWRWW.YYY.",
    ".....wwWWWRWW.....",
    "....wwwWWWRWWW....",
    "....wwwWWWWWWW....",
    "....wwwWWWWWWWW...",
    "...wwwwWWWWWWWW...",
    "...wwwwWWWWWWWWW..",
    "...GwwwWWWWWWWWW..",
    "....KK......KK....",
]
cv.sprite(player, 45, 81, {
    "K": "ink0", "k": "ink2", "H": "ink1", "S": "skin", "s": "skin0", "E": "ink0",
    "T": "teal", "W": "parch2", "w": "parch", "G": "parch0", "R": "red", "Y": "yellow", "r": "red",
}, outline="ink0")
for x, y in ((66, 90), (64, 96), (68, 98), (66, 93)):
    cv.dot(x, y, "gold2")

# Dueoksini: a hulking, hunched shadow ghost said to bring plague
L = Layer(seed=5)
bx, by = 186, 58
blobs = [(bx + 26, by + 20, 14, 15), (bx + 24, by + 34, 17, 12), (bx + 16, by + 24, 9, 9)]
for cx, cy, rx, ry in blobs:
    L.disc(cx, cy, rx, "purple0", ry=ry)
for i in range(bx + 6, bx + 44):  # ragged hem
    if (i * 5) % 7 < 4:
        L.rect(i, by + 44, 1, 2 + (i % 3), "purple0")
# rim light from the moon (upper right)
src = [[L.get(i, j)[3] if L.get(i, j) else 0 for j in range(H)] for i in range(W)]
for i in range(bx, bx + 46):
    for j in range(by, by + 50):
        if not src[i][j]:
            continue
        if not src[i + 1][j - 1] or not src[i + 2][j - 2]:
            L.dot(i, j, "purple2" if not src[i + 1][j - 1] else "purple")
        elif i > bx + 28 and j < by + 36 and (i + j) % 2:
            L.dot(i, j, "purple")
# head thrust forward and low
L.disc(bx + 10, by + 18, 7, "purple0")
L.disc(bx + 11, by + 16, 5, "purple")
for k, dx in enumerate((-7, -4, -1, 2, 5, 8)):  # long hair hanging down
    L.line(bx + 10 + dx // 2, by + 11, bx + 10 + dx, by + 26 + (k % 3) * 3, "ink0")
for k, (dx, dy) in enumerate(((-5, -6), (-1, -8), (3, -7), (7, -4))):
    L.line(bx + 10, by + 12, bx + 10 + dx, by + 12 + dy, "ink0")
L.rect(bx + 5, by + 17, 3, 2, "red2"); L.dot(bx + 6, by + 17, "gold2")
L.rect(bx + 11, by + 17, 3, 2, "red2"); L.dot(bx + 12, by + 17, "gold2")
L.rect(bx + 5, by + 22, 9, 2, "ink0")
for i in range(0, 9, 2):
    L.dot(bx + 5 + i, by + 22, "parch2")
# long arms dragging on the ground
for x0, y0, x1, y1, col in ((bx + 18, by + 26, bx + 2, by + 46, "purple0"), (bx + 30, by + 30, bx + 24, by + 47, "purple0")):
    for t in range(4):
        L.line(x0 + t, y0, x1 + t, y1, col if t < 3 else "purple")
    for c in range(4):
        L.line(x1 + c, y1, x1 + c - 2, y1 + 2, "parch")
L.paste(cv, outline="ink0")

# Dokkaebi fire wisps
wisp = [
    "....c.....",
    "...cc.....",
    "...cCc..c.",
    "..cCCc.cc.",
    "..cCWCccc.",
    ".cCCWWCCc.",
    ".cCWWWWCc.",
    "cCCWWWWCCc",
    "cCWWWWWWCc",
    "cCWEWWEWCc",
    ".cCWWWWCc.",
    ".cCCWWCCc.",
    "..ccCCcc..",
    "...cccc...",
]
wmap = {"c": "flame0", "C": "flame", "W": "flame2", "E": "night0"}
for (x, y) in ((244, 64), (276, 78)):
    cv.disc(x + 5, y + 8, 9, "night2")
    cv.sprite(wisp, x, y, wmap, outline="night0")
    cv.disc(x + 5, 106, 4, "ink0", ry=1)
for x, y in ((240, 62), (288, 74), (272, 94), (256, 82)):
    cv.dot(x, y, "flame2")

# Enemy intents and HP --------------------------------------------------------
def sword(x, y):
    cv.sprite(["....W", "...W.", "R.W..", ".R...", "R.R.."], x, y, {"W": "parch2", "R": "red2"}, outline="ink0")


def swirl(x, y):
    cv.sprite([".PPP.", "P...P", "P.P.P", "P..P.", ".P..."], x, y, {"P": "purple2"}, outline="ink0")


sword(198, 40); cv.text(205, 39.5, "14", "red2", 11)
swirl(244, 49); cv.text(251, 48.5, "현혹 2", "pink", 10)
sword(276, 63); cv.text(283, 62.5, "6", "red2", 11)
cv.text(220, 33.5, "두억시니", "parch2", 10, anchor="ma")
bar(cv, 192, 109, 24, 2, 38 / 52, "red2", hi="pink"); cv.text(218, 107.5, "38/52", "parch", 10)
bar(cv, 248, 109, 12, 2, 9 / 12, "flame", hi="flame2"); cv.text(262, 107.5, "9", "parch", 10)
bar(cv, 278, 109, 12, 2, 1.0, "flame", hi="flame2"); cv.text(292, 107.5, "12", "parch", 10)
bar(cv, 42, 109, 26, 2, 41 / 60, "red2", hi="pink"); cv.text(70, 107.5, "41/60", "parch", 10)
cv.sprite(["SSSSS", "SWWWS", "SWWWS", ".SWS.", "..S.."], 30, 107, {"S": "teal2", "W": "teal3"}, outline="ink0")
cv.text(28, 108.5, "8", "teal3", 10, anchor="ra")

# Top HUD -----------------------------------------------------------------
cv.rect(0, 0, 320, 12, "ink0"); cv.rect(0, 12, 320, 1, "gold0")
cv.text(5, 1.5, "벽사록  2막 · 산사의 밤", "parch2", 11)
coin(cv, 236, 3, big=True); cv.text(243, 1.5, "128", "gold2", 11)
cv.sprite(["RRRR", "RYYR", "RYRR", "RYYR", "RRRR"], 268, 3, {"R": "red", "Y": "yellow"})
cv.text(274, 1.5, "부적 18", "parch", 11)

# Bottom: ink-stone energy, hand of talismans, tooltip, end turn ----------
cv.rect(0, 122, 320, 58, "ink0")
cv.rect(0, 122, 320, 1, "ink2")
cv.disc(24, 147, 15, "ink2"); cv.disc(24, 147, 13, "ink1"); cv.disc(24, 147, 10, "ink0")
cv.disc(21, 144, 4, "night2", ry=2)
cv.text(24, 140, "3/3", "parch2", 12, anchor="ma")
cv.text(24, 165, "먹", "parch0", 10, anchor="ma")
cv.text(6, 171.5, "덱 12 · 버림 5", "ink3", 10, shadow=None)


def card(x, y, glyph, name, cost, hover=False):
    w, h = 34, 48
    if hover:
        cv.rect(x - 2, y - 2, w + 4, h + 4, "gold2")
    cv.rect(x, y, w, h, "red0")
    cv.rect(x + 1, y + 1, w - 2, h - 2, "yellow")
    cv.dither(x + 2, y + 2, w - 4, h - 4, "yellow", "gold2")
    cv.rect(x + 2, y + 2, w - 4, h - 4, "yellow")
    cv.frame(x + 2, y + 2, w - 4, h - 4, "red")
    for k in range(3, h - 14, 3):  # faint brush fibres
        cv.dot(x + 3 + (k * 7) % (w - 6), y + k, "gold2")
    glyph(x + 10, y + 9)
    cv.rect(x + 2, y + 34, w - 4, 11, "parch2")
    cv.rect(x + 2, y + 34, w - 4, 1, "red")
    cv.disc(x + 3, y + 3, 4, "ink0"); cv.disc(x + 3, y + 3, 3, "ink1")
    cv.text(x + 3, y + 0, str(cost), "parch2", 11, anchor="ma")
    cv.text(x + 17, y + 36.5, name, "red0", 10, shadow=None, anchor="ma")


R = "red"


def g_cheoyong(x, y):  # Cheoyong mask
    cv.sprite([
        "..RRRRRRRR..",
        ".RrrrrrrrrR.",
        "RrrKrrrrKrrR",
        "RrKKKrrKKKrR",
        "RrrrrrrrrrrR",
        "RrrrrRRrrrrR",
        "RrrrrRRrrrrR",
        ".RrrrrrrrrR.",
        ".RrKKKKKKrR.",
        "..RrrrrrrR..",
        "...RRRRRR...",
        "..R..R..R...",
        ".R...R...R..",
    ], x, y, {"R": "red0", "r": "red2", "K": "ink0"})


def g_rooster(x, y):
    cv.sprite([
        "...RR.......",
        "..RRRR......",
        "..KRRR......",
        ".YRRRR......",
        "YY.RRR....RR",
        "...RRRR..RRR",
        "...RRRRRRRR.",
        "...RRRRRRRR.",
        "....RRRRRR..",
        ".....R..R...",
        ".....R..R...",
        "....RR.RR...",
    ], x, y, {"R": R, "K": "ink0", "Y": "gold0"})


def g_beans(x, y):
    for dx, dy in ((2, 2), (6, 1), (9, 4), (4, 6), (8, 8), (1, 9), (5, 10), (10, 11), (3, 13)):
        cv.sprite(["RR", "Rr"], x + dx, y + dy, {"R": "red0", "r": "red2"})


def g_axe(x, y):
    cv.sprite([
        "......BB....",
        "..RRRRBB....",
        ".RRRRRBB....",
        "RRRRRRBB....",
        "RRRrrRBB....",
        "RRRRRRBB....",
        ".RRRRRBB....",
        "..RRRRBB....",
        "......BB....",
        "......BB....",
        "......BB....",
        "......BB....",
        ".....BBBB...",
    ], x + 1, y, {"R": R, "r": "red2", "B": "brown0"})


def g_eye(x, y):
    cv.sprite([
        "...RRRRRR...",
        ".RR......RR.",
        "R...KKKK...R",
        "R..KKrrKK..R",
        "R..KKrrKK..R",
        "R...KKKK...R",
        ".RR......RR.",
        "...RRRRRR...",
        "............",
        "..R.R.R.R.R.",
    ], x, y + 2, {"R": R, "K": "ink0", "r": "red2"})


hand = [(g_cheoyong, "처용 부적", 1), (g_rooster, "닭 울음", 2), (g_beans, "팥 뿌리기", 1),
        (g_axe, "금갑장군", 2), (g_eye, "응시", 0)]
for k, (g, name, cost) in enumerate(hand):
    hover = k == 0
    cv_y = 118 if hover else 128 + abs(k - 2) * 2
    card(52 + k * 37, cv_y, g, name, cost, hover)

panel(cv, 240, 116, 76, 46, fill="ink1", edge="gold0", inner="ink2")
cv.text(244, 118.5, "처용 부적", "gold2", 11)
cv.text(244, 126.5, "방어 8", "parch2", 10)
cv.text(244, 132.5, "역신 1턴 봉인", "parch2", 10)
cv.text(244, 140.5, "문에 붙인 처용의", "parch0", 10)
cv.text(244, 146.5, "얼굴을 역신이 피한다", "parch0", 10)
cv.text(244, 153.5, "『삼국유사』", "ink3", 10)
cv.rect(252, 165, 56, 12, "red0"); cv.rect(253, 166, 54, 10, "red"); cv.rect(253, 166, 54, 1, "red2")
cv.text(280, 166.5, "턴 종료", "parch2", 11, anchor="ma")

cv.export("concept-1-deckbuilder.png")
print("saved")
