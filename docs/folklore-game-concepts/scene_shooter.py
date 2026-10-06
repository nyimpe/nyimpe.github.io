"""Concept 6 — palace exorcism boomer shooter (raycast 2.5D with pixel sprites)."""
import math
from PIL import Image
from pix import *

cv = Canvas("night0", seed=81)
rng = cv.rng
VH = 150  # 3D view height; HUD below
HOR = VH // 2

# Textures (32x32) -------------------------------------------------------------------
def make_tex(fn):
    t = [[P["ink0"]] * 32 for _ in range(32)]
    fn(t)
    return t


def palace_wall(t):
    for y in range(32):
        for x in range(32):
            if y < 6:  # dancheong band
                c = "moss" if y in (1, 2, 3, 4) else "teal"
                if y in (2, 3) and x % 8 in (2, 3, 4, 5):
                    c = "red2" if x % 16 < 8 else "white"
                if y in (2, 3) and x % 8 == 3 and x % 16 < 8:
                    c = "gold2"
            elif y >= 26:  # stone base
                c = "iron2" if (y == 26 or x % 11 == 0) else "iron"
                if y == 31:
                    c = "iron0"
            elif x < 4 or x > 27:  # red pillars
                c = "red" if 0 < x < 3 or 28 < x < 31 else "red0"
            else:
                c = "parch2" if (x + y) % 9 else "parch"
                if 9 <= x <= 22 and 9 <= y <= 21:  # lattice window
                    c = "brown" if (x - 9) % 4 == 0 or (y - 9) % 4 == 0 else "parch0"
            t[y][x] = P[c]


def gate(t):
    for y in range(32):
        for x in range(32):
            if y < 6:
                c = "moss" if 0 < y < 5 else "teal"
                if y in (2, 3) and x % 6 < 3:
                    c = "gold2"
            else:
                c = "red" if x % 15 else "red0"
                if x in (15, 16):
                    c = "ink0"
                if (y - 8) % 6 == 0 and (x - 3) % 5 == 0 and x not in (15, 16):
                    c = "gold2"
                if y == 31:
                    c = "iron0"
            t[y][x] = P[c]


TEX = {1: make_tex(palace_wall), 2: make_tex(gate)}

M = [
    "1111111111111111",
    "1111112222111111",
    "1111110000111111",
    "1111100000011111",
    "1111100000011111",
    "1111100000011111",
    "1111100000011111",
    "1111100000011111",
    "1111100000011111",
    "1111100000011111",
    "1111111111111111",
]
WALL = 1.5  # walls are taller than the eye line
MAP = [[int(ch) for ch in row] for row in M]
px0, py0 = 8.35, 9.4
ang = math.radians(-92)
dx, dy = math.cos(ang), math.sin(ang)
plx, ply = -dy * 0.66, dx * 0.66


def shade(rgb, dist, side):
    k = max(0.28, min(1.0, 1.25 - dist * 0.11))
    k = round(k * 6) / 6
    if side:
        k *= 0.82
    return (int(rgb[0] * k * 0.92), int(rgb[1] * k * 0.95), int(min(255, rgb[2] * k + (1 - k) * 30)))


# Sky with a distant throne-hall roof ---------------------------------------------------
cv.vgrad(0, HOR, ["night0", "night1", "night1", "night2"])
cv.stars(60, HOR - 10)
cv.disc(250, 20, 8, "parch2"); cv.disc(252, 19, 7, "white")
cv.rect(110, HOR - 24, 100, 24, "night0")
giwa(cv, 96, HOR - 36, 128, 13, roof="night0", edge="night1", ridge="night0")
giwa(cv, 120, HOR - 50, 80, 10, roof="night0", edge="night1", ridge="night0")
cv.rect(132, HOR - 40, 56, 5, "night0")

# Floor casting: granite slabs (bakseok) -------------------------------------------------
for y in range(HOR + 1, VH):
    p = y - HOR
    row_dist = (0.5 * VH) / p
    fx_step = row_dist * (2 * plx) / W
    fy_step = row_dist * (2 * ply) / W
    fx = px0 + row_dist * (dx - plx)
    fy = py0 + row_dist * (dy - ply)
    for x in range(W):
        cx_, cy_ = fx % 1.0, fy % 1.0
        c = P["iron"] if (int(fx * 2) + int(fy * 3)) % 3 else P["iron0"]
        if cx_ < 0.04 or (cy_ * 2) % 1.0 < 0.05:
            c = P["ink1"]
        cv.px[x, y] = shade(c, row_dist, 0)
        fx += fx_step; fy += fy_step

# Walls (DDA) ----------------------------------------------------------------------------
zbuf = [99.0] * W
for x in range(W):
    cam = 2 * x / W - 1
    rdx, rdy = dx + plx * cam, dy + ply * cam
    mx, my = int(px0), int(py0)
    ddx = abs(1 / rdx) if rdx else 1e30
    ddy = abs(1 / rdy) if rdy else 1e30
    stx, sdx = (-1, (px0 - mx) * ddx) if rdx < 0 else (1, (mx + 1 - px0) * ddx)
    sty, sdy = (-1, (py0 - my) * ddy) if rdy < 0 else (1, (my + 1 - py0) * ddy)
    while True:
        if sdx < sdy:
            sdx += ddx; mx += stx; side = 0
        else:
            sdy += ddy; my += sty; side = 1
        if MAP[my][mx]:
            break
    dist = (sdx - ddx) if side == 0 else (sdy - ddy)
    zbuf[x] = dist
    lh = int(VH * WALL / dist)
    top = HOR + int(VH / dist / 2) - lh
    wx = (py0 + dist * rdy) if side == 0 else (px0 + dist * rdx)
    wx -= math.floor(wx)
    tx = int(wx * 32)
    tex = TEX[MAP[my][mx]]
    for y in range(max(0, top), min(VH, top + lh)):
        ty = int((y - top) * 32 / lh)
        cv.px[x, y] = shade(tex[min(31, ty)][tx], dist, side)

# Sprites (billboards with z-buffer) -----------------------------------------------------
def sprite_img(rows, cmap):
    h, w = len(rows), max(len(r) for r in rows)
    im = Image.new("RGBA", (w + 2, h + 2), (0, 0, 0, 0))
    pxi = im.load()
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch not in ". ":
                pxi[i + 1, j + 1] = P[cmap[ch]] + (255,)
    out = im.copy(); po = out.load()
    for j in range(h + 2):
        for i in range(w + 2):
            if pxi[i, j][3]:
                continue
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ii, jj = i + di, j + dj
                if 0 <= ii < w + 2 and 0 <= jj < h + 2 and pxi[ii, jj][3]:
                    po[i, j] = P["ink0"] + (255,)
                    break
    return out


wisp = sprite_img(["...c...", "..cC.c.", "..cCcC.", ".cCWWCc", "cCWWWWc", "cCWEWEc", "cCWWWWc", ".cCWWc.", "..ccc.."],
                  {"c": "flame0", "C": "flame", "W": "flame2", "E": "night0"})
headless = sprite_img([
    "......RR......",
    ".....RKKR.....",
    "....WWWWWW....",
    "W..WWWWWWWW..W",
    "WW.WWWWWWWW.WW",
    ".WWWWWWWWWWWW.",
    "..WWWWWWWWWW..",
    "...WWWWWWWW...",
    "...WWWgWWWW...",
    "...WWWgWWWW...",
    "..WWWWWWWWWW..",
    "..WWWWgWWWWW..",
    ".WWWWWWWWWWWW.",
    ".WWWWWWWWWWWW.",
    "WWWgWWWWWWgWWW",
    "WWWWWWWWWWWWWW",
    "W.W.W.W.W.W.W.",
], {"R": "red", "K": "red0", "W": "ghost2", "g": "ghost"})
hound = sprite_img([
    "..........KK....",
    ".........KKKK...",
    "..KKKKKKKKRKKK..",
    ".KKKKKKKKKKKKKKW",
    "KKKkKKKKKKKKKWW.",
    "KKkKKKKKKKKKKK..",
    ".KKKKKKKKKKKK...",
    ".KK.KK...KK.KK..",
    ".KK..KK..KK..KK.",
    ".WW...WW.WW...WW",
], {"K": "ink1", "k": "ink3", "R": "red2", "W": "parch"})
cheonrok = sprite_img([
    "..G.....G..",
    ".GgG...GgG.",
    ".GGGGGGGGG.",
    "GGKGGGGGKGG",
    "GGGGGGGGGGG",
    ".GGWWWWWGG.",
    "..GGGGGGG..",
    ".GGgGGGgGG.",
    "GGGGGGGGGGG",
    "GgGGgGGgGGg",
    "GGGGGGGGGGG",
    "IIIIIIIIIII",
], {"G": "iron2", "g": "iron", "K": "ink0", "W": "parch", "I": "iron0"})

sprites = [  # (x, y, image, world height, lift)
    (7.4, 3.4, wisp, 0.30, 0.45), (8.7, 3.1, wisp, 0.30, 0.6), (6.6, 3.0, wisp, 0.30, 0.3),
    (6.2, 5.0, cheonrok, 0.6, 0.0),
    (7.3, 5.2, headless, 0.8, 0.0),
    (8.9, 7.5, hound, 0.42, 0.0),
]
inv = 1.0 / (plx * dy - dx * ply)
order = sorted(sprites, key=lambda s: -((s[0] - px0) ** 2 + (s[1] - py0) ** 2))
for sx, sy, im, wh, lift in order:
    rx, ry = sx - px0, sy - py0
    tx_ = inv * (dy * rx - dx * ry)
    tz = inv * (-ply * rx + plx * ry)
    if tz <= 0.1:
        continue
    scr_x = int((W / 2) * (1 + tx_ / tz))
    h_ = int(abs(VH / tz) * wh)
    w_ = int(h_ * im.width / im.height)
    if h_ < 2 or w_ < 2:
        continue
    scaled = im.resize((w_, h_), Image.NEAREST).load()
    floor_y = HOR + int(VH / tz / 2)
    y0 = floor_y - h_ - int(VH / tz * lift)
    x0 = scr_x - w_ // 2
    for i in range(w_):
        X = x0 + i
        if not (0 <= X < W) or tz >= zbuf[X]:
            continue
        for j in range(h_):
            Y = y0 + j
            if 0 <= Y < VH:
                c = scaled[i, j]
                if c[3]:
                    cv.px[X, Y] = c[:3] if im is wisp else shade(c[:3], tz * 0.7, 0)
    if im is wisp:
        cv.px[max(0, min(W - 1, scr_x)), max(0, min(VH - 1, y0 - 1))] = P["flame2"]

# Matchlock (jochong) just fired ------------------------------------------------------------
L = Layer(seed=5)
MX, MY = 170, 98  # muzzle
for k in range(80):  # wooden stock running under the barrel
    t = k / 79
    x = 252 - (252 - MX - 6) * t; y = 152 - (152 - MY - 6) * t
    L.disc(x, y, 6.5 - 3.5 * t, "brown")
    L.disc(x - 1, y - 1.5, 4.5 - 2.5 * t, "brown2")
for k in range(84):  # iron barrel on top
    t = k / 83
    x = 244 - (244 - MX) * t; y = 140 - (140 - MY) * t
    L.disc(x, y - 3, 2.6 - 1.0 * t, "iron0")
    L.dot(x - 1, y - 4, "iron2")
for k in range(3):  # brass bands
    t = 0.3 + k * 0.22
    x = 244 - (244 - MX) * t; y = 140 - (140 - MY) * t
    L.rect(x - 2, y - 5, 4, 7, "gold")
L.rect(222, 126, 6, 5, "gold"); L.rect(226, 122, 2, 5, "gold0")  # serpentine and pan
L.paste(cv, outline="ink0")
L = Layer(seed=6)  # hands and sleeves over the gun
L.disc(203, 128, 8, "skin", ry=6); L.disc(206, 132, 5, "skin0", ry=3)
L.disc(214, 150, 14, "parch2", ry=8); L.disc(218, 146, 9, "parch", ry=4)
L.disc(244, 144, 8, "skin", ry=6)
L.disc(258, 156, 16, "parch2", ry=9); L.disc(262, 150, 10, "parch", ry=4)
L.paste(cv, outline="ink0")
cv.dot(227, 120, "red2"); cv.dot(227, 119, "orange2")
for k in range(6):
    cv.dot(227 - (k % 2), 117 - k * 3, "iron2")
for r_, col in ((12, "orange"), (8, "orange2"), (4, "white")):  # muzzle flash
    for a in range(0, 360, 30):
        cv.line(MX, MY - 3, MX + r_ * math.cos(math.radians(a)), MY - 3 + r_ * 0.8 * math.sin(math.radians(a)), col)
for k in range(4):  # drifting powder smoke
    cx_, cy_, r_ = MX - 6 - k * 5, MY - 13 - k * 4, 3 + k
    for j in range(int(cy_ - r_), int(cy_ + r_) + 1):
        for i in range(int(cx_ - r_), int(cx_ + r_) + 1):
            if (i - cx_) ** 2 + (j - cy_) ** 2 <= r_ * r_ and (i + j + k) % 2 == 0 and j < VH:
                cv.dot(i, j, "iron2" if k < 3 else "iron")
cv.rect(158, HOR - 1, 5, 1, "white"); cv.rect(160, HOR - 3, 1, 5, "white")

# HUD (status bar) ----------------------------------------------------------------------------
cv.rect(0, VH, W, H - VH, "ink1")
cv.rect(0, VH, W, 1, "gold0"); cv.rect(0, VH + 1, W, 1, "brown0")
cells = [(2, 60, "화약", "24"), (64, 60, "체력", "87%"), (196, 58, "부적", "3"), (256, 62, "무기", "")]
for x, w_, lab, val in cells:
    cv.rect(x, VH + 3, w_, 26, "ink0"); cv.frame(x, VH + 3, w_, 26, "brown")
    cv.text(x + w_ / 2, VH + 4.5, lab, "parch0", 10, anchor="ma")
    if val:
        cv.text(x + w_ / 2, VH + 12, val, "red2" if lab != "부적" else "gold2", 15, anchor="ma")
for k, (n, own) in enumerate((("1", True), ("2", True), ("3", True), ("4", False))):
    cv.text(266 + k * 12, VH + 14, n, "gold2" if k == 1 else ("parch" if own else "ink3"), 11, anchor="ma")
cv.text(287, VH + 22, "활 조총 신기전", "ink3", 10, anchor="ma")
# face portrait
cv.rect(128, VH + 3, 64, 26, "ink0"); cv.frame(128, VH + 3, 64, 26, "brown")
cv.sprite([
    "......KKKKKK......",
    "......KkkkkK......",
    "..kKKKKKKKKKKKKk..",
    ".....HSSSSSSH.....",
    ".....SKKSSKKS.....",
    ".....SSESSESS.....",
    ".....SSSSSSSS.....",
    "......SSRRSS......",
    "......SSSSSS......",
    "....WWWWWWWWWW....",
], 151, VH + 6, {"K": "ink0", "k": "ink2", "H": "ink1", "S": "skin", "E": "ink0", "R": "red0", "W": "parch2"})
cv.rect(132, VH + 20, 4, 4, "red"); cv.rect(184, VH + 20, 4, 4, "teal2")

cv.text(4, 3, "영제교 · 근정문 앞", "parch2", 10)
cv.text(316, 3, "퇴치 41 / 60", "parch", 10, anchor="ra")

cv.export("concept-6-boomer-shooter.png")
print("saved")
