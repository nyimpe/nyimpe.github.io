"""Concept 28 — 1-bit deduction after Return of the Obra Dinn (the drifting grain-tax ship)."""
import math
from pix import *

B, Wh = "ink0", "parch2"  # 1-bit: ink and paper only
cv = Canvas(B, seed=401)
rng = cv.rng
SH = 132  # scene height


def dither(x0, y0, x1, y1, density):
    """Ordered 2x2 dither at 0..4 levels."""
    m = [[0, 2], [3, 1]]
    for y in range(int(y0), int(y1)):
        for x in range(int(x0), int(x1)):
            if m[y % 2][x % 2] < density:
                cv.dot(x, y, Wh)


# Sky, horizon, sparse sea strokes ------------------------------------------------------------------------
dither(0, 0, W, 34, 1)
cv.rect(0, 48, W, 1, Wh)
for k in range(30):
    x, y = rng.randrange(W), rng.randrange(52, 74)
    cv.rect(x, y, rng.randrange(4, 10), 1, Wh)

# Deck: gunwale and a few planks
cv.rect(0, 78, W, 2, Wh)
for y in (92, 108, 124):
    for x in range(0, W, 3):
        cv.dot(x, y, Wh)
cv.rect(158, 4, 3, 74, Wh)  # mast
for y in range(10, 78, 3):
    cv.dot(158 - (y - 10) * 1.4, y, Wh); cv.dot(160 + (y - 10) * 1.4, y, Wh)  # stays
cv.rect(118, 22, 84, 2, Wh); cv.rect(126, 36, 68, 1, Wh)  # yard and furled sail

# Tanjueo: a whale-fish lunging over the rail, mouth open
L = Layer(seed=2)
L.disc(34, 62, 48, B, ry=38)
L.paste(cv, outline="parch2")
dither(0, 30, 60, 50, 1)
cv.disc(40, 74, 28, B, ry=16)
cv.ring(40, 74, 28, Wh, ry=16)
for k in range(9):  # teeth
    x = 16 + k * 6
    cv.sprite(["W", "W"], x, 60 + abs(4 - k), {"W": Wh})
    cv.sprite(["W", "W"], x + 2, 86 - abs(4 - k), {"W": Wh})
cv.disc(60, 44, 3, Wh); cv.dot(60, 44, B)

# Namoh: the long-legged squid reaching over the right rail
for k in range(2):
    pts = [(320, 56 + k * 18)]
    for t in range(1, 22):
        pts.append((320 - t * 4, 56 + k * 18 + 8 * math.sin(t * 0.4 + k)))
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        cv.line(x0, y0, x1, y1, Wh); cv.line(x0, y0 + 1, x1, y1 + 1, Wh)

# Frozen figures: white silhouettes, ink details
def figure(x, y, rows, label=None):
    cv.sprite(rows, x, y, {"W": Wh, "K": B}, outline="ink0")
    if label:
        w = len(label) * 6 + 8
        cv.rect(x + 5 - w // 2, y - 14, w, 12, Wh); cv.frame(x + 5 - w // 2, y - 14, w, 12, B)
        cv.text(x + 5, y - 12.5, label, B, 10, shadow=None, anchor="ma")


man = ["...WWW....", "..WWWWW...", "...WWW....", ".WWWWWWW..", "WWWWWWWWW.", "W.WWWWW.W.", "..WWWWW...", "..WW.WW...",
       "..WW.WW...", ".WWW.WWW.."]
figure(36, 70, man, "?")  # half inside the mouth
figure(110, 98, man, "사공 박돌이")
figure(166, 40, ["...WWW....", "..WKKKW...", "...WWW....", "WWWWWWWW..", ".WWWWWWW..", "..WWWWW...", "..WW.WW..."])
figure(204, 98, ["..WWWW....", ".WWKWKW...", "..WWWW....", ".WWKWKW...", "..WWWW....", ".WWWWWW...", "WWWWWWWW..",
                 "..WWWW....", "..WW.WW..."], "얼굴 둘")
figure(268, 84, man, "?")
cv.rect(146, 26, 46, 12, Wh); cv.frame(146, 26, 46, 12, B)
cv.text(169, 27.5, "머리털 없음", B, 10, shadow=None, anchor="ma")

# Ledger -----------------------------------------------------------------------------------------------------
cv.rect(0, SH, W, H - SH, Wh)
cv.rect(0, SH, W, 1, B)
cv.text(6, SH + 3, "조운선 표류 기록 · 열둘째 기억", B, 11, shadow=None)
cv.text(316, SH + 3, "확인 7 / 20", B, 11, shadow=None, anchor="ra")
rows = [("사공 박돌이", "탄주어에게 삼켜짐", True), ("격군 (머리털 없음)", "삼켜졌다 살아 나옴", True),
        ("얼굴 둘인 손님", "말이 안 통해 굶음", False), ("격군 ???", "??? 다리에 끌려감", False)]
for k, (who, fate, ok) in enumerate(rows):
    x = 6 + (k % 2) * 158
    y = SH + 17 + (k // 2) * 13
    cv.text(x, y, ("✓ " if ok else "· ") + who + " — " + fate, B, 10, shadow=None)

cv.export("concept-28-indie-shipwreck.png")
print("saved")
