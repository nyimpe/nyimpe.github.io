"""Tiny pixel-art toolkit: draw at 320x180, text on a 2x layer, export 1280x720."""
import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 320, 180
FONT_PATH = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"

P = {
    "ink0": (22, 18, 26), "ink1": (40, 34, 42), "ink2": (64, 54, 60), "ink3": (92, 80, 84),
    "brown0": (62, 42, 34), "brown": (96, 66, 48), "brown2": (132, 94, 64), "tan": (176, 136, 92),
    "parch0": (196, 174, 132), "parch": (222, 204, 166), "parch2": (238, 228, 200), "white": (250, 246, 234),
    "red0": (92, 28, 34), "red": (158, 48, 46), "red2": (206, 86, 66), "pink": (232, 150, 132),
    "gold0": (132, 94, 36), "gold": (200, 156, 58), "gold2": (240, 208, 112), "yellow": (236, 210, 120),
    "moss0": (34, 54, 44), "moss": (62, 90, 60), "moss2": (108, 136, 84), "moss3": (156, 172, 108),
    "teal0": (20, 38, 52), "teal": (38, 74, 90), "teal2": (72, 124, 132), "teal3": (128, 176, 170),
    "night0": (12, 14, 28), "night1": (22, 28, 52), "night2": (38, 46, 80), "night3": (62, 72, 112),
    "ghost": (170, 216, 224), "ghost2": (222, 246, 244), "flame0": (40, 92, 180), "flame": (70, 150, 232),
    "flame2": (150, 222, 255), "purple0": (44, 30, 56), "purple": (82, 58, 102), "purple2": (124, 92, 140),
    "skin": (232, 188, 148), "skin0": (184, 132, 104), "orange": (226, 128, 52), "orange2": (250, 184, 88),
    "iron0": (54, 58, 66), "iron": (98, 104, 112), "iron2": (150, 156, 160),
}


class Canvas:
    def __init__(self, bg="ink0", seed=1):
        self.img = Image.new("RGB", (W, H), P[bg])
        self.px = self.img.load()
        self.rng = random.Random(seed)
        self.texts = []  # drawn on the 2x layer at export

    # --- primitives -------------------------------------------------------
    def c(self, col):
        return P[col] if isinstance(col, str) else col

    def dot(self, x, y, col):
        x, y = int(x), int(y)
        if 0 <= x < W and 0 <= y < H and col is not None:
            self.px[x, y] = self.c(col)

    def get(self, x, y):
        return self.px[int(x), int(y)] if 0 <= x < W and 0 <= y < H else None

    def rect(self, x, y, w, h, col):
        for j in range(int(y), int(y + h)):
            for i in range(int(x), int(x + w)):
                self.dot(i, j, col)

    def frame(self, x, y, w, h, col):
        self.rect(x, y, w, 1, col); self.rect(x, y + h - 1, w, 1, col)
        self.rect(x, y, 1, h, col); self.rect(x + w - 1, y, 1, h, col)

    def dither(self, x, y, w, h, a, b, phase=0):
        for j in range(int(y), int(y + h)):
            for i in range(int(x), int(x + w)):
                self.dot(i, j, a if (i + j + phase) % 2 else b)

    def line(self, x0, y0, x1, y1, col):
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx + dy
        while True:
            self.dot(x0, y0, col)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy; x0 += sx
            if e2 <= dx:
                err += dx; y0 += sy

    def disc(self, cx, cy, r, col, ry=None):
        ry = r if ry is None else ry
        for j in range(int(cy - ry) - 1, int(cy + ry) + 2):
            for i in range(int(cx - r) - 1, int(cx + r) + 2):
                if ((i - cx) / max(r, .5)) ** 2 + ((j - cy) / max(ry, .5)) ** 2 <= 1.0:
                    self.dot(i, j, col)

    def ring(self, cx, cy, r, col, ry=None, steps=None):
        ry = r if ry is None else ry
        steps = steps or int(8 * max(r, ry)) + 8
        for k in range(steps):
            a = 2 * math.pi * k / steps
            self.dot(round(cx + r * math.cos(a)), round(cy + ry * math.sin(a)), col)

    def vgrad(self, y0, y1, cols, x0=0, x1=W):
        """Banded vertical gradient with a dithered seam between bands."""
        n = len(cols)
        span = (y1 - y0) / n
        for j in range(y0, y1):
            t = (j - y0) / span
            k = min(int(t), n - 1)
            frac = t - k
            for i in range(x0, x1):
                col = cols[k]
                if k + 1 < n and frac > 0.75 and (i + j) % 2 == 0:
                    col = cols[k + 1]
                self.dot(i, j, col)

    def ridge(self, y_base, amp, col, seed, freq=1.0, x0=0, x1=W, rough=1.0, to=H):
        rng = random.Random(seed)
        ph = [rng.uniform(0, 6.28) for _ in range(4)]
        for i in range(x0, x1):
            t = i / W * freq
            y = (y_base - amp * (0.55 * math.sin(t * 6.1 + ph[0]) + 0.3 * math.sin(t * 13.7 + ph[1])
                                 + 0.15 * rough * math.sin(t * 31.0 + ph[2]) + 0.1 * rough * math.sin(t * 57 + ph[3])))
            for j in range(int(y), to):
                self.dot(i, j, col)

    def stars(self, n, y1, cols=("parch", "ghost2", "parch0")):
        for _ in range(n):
            self.dot(self.rng.randrange(W), self.rng.randrange(y1), self.rng.choice(cols))

    # --- sprites ----------------------------------------------------------
    def sprite(self, rows, x, y, cmap, outline=None, flip=False):
        """Stamp ASCII art. '.' and ' ' are transparent. Optional 1px outline."""
        h = len(rows)
        w = max(len(r) for r in rows)
        grid = [[None] * w for _ in range(h)]
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch not in ". ":
                    grid[j][(w - 1 - i) if flip else i] = cmap[ch]
        if outline:
            for j in range(-1, h + 1):
                for i in range(-1, w + 1):
                    filled = 0 <= j < h and 0 <= i < w and grid[j][i] is not None
                    if filled:
                        continue
                    for dj, di in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                        jj, ii = j + dj, i + di
                        if 0 <= jj < h and 0 <= ii < w and grid[jj][ii] is not None:
                            self.dot(x + i, y + j, outline)
                            break
        for j in range(h):
            for i in range(w):
                if grid[j][i] is not None:
                    self.dot(x + i, y + j, grid[j][i])
        return w, h

    # --- post effects -----------------------------------------------------
    def darken(self, fn):
        """fn(x, y) -> 0..1 light level, quantized into 3 dithered steps."""
        for j in range(H):
            for i in range(W):
                lv = fn(i, j)
                if lv >= 1:
                    continue
                r, g, b = self.px[i, j]
                if lv > 0.66:
                    k = 0.78 if (i + j) % 2 else 1.0
                elif lv > 0.33:
                    k = 0.6
                elif lv > 0.15:
                    k = 0.48 if (i + j) % 2 else 0.6
                else:
                    k = 0.42
                # Night tint: pull toward blue as it darkens.
                self.px[i, j] = (int(r * k * 0.9), int(g * k * 0.95), int(min(255, b * k + (1 - k) * 26)))

    # --- text (2x layer) --------------------------------------------------
    def text(self, x, y, s, col="parch2", size=11, shadow="ink0", anchor="la"):
        """x, y in 320x180 space; may be fractional (.5 = one 2x pixel)."""
        self.texts.append((x, y, s, col, size, shadow, anchor))

    def export(self, path):
        up = self.img.resize((W * 2, H * 2), Image.NEAREST)
        d = ImageDraw.Draw(up)
        d.fontmode = "1"
        for x, y, s, col, size, shadow, anchor in self.texts:
            f = ImageFont.truetype(FONT_PATH, size)
            X, Y = int(x * 2), int(y * 2)
            if shadow:
                for ox, oy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1)):
                    d.text((X + ox, Y + oy), s, font=f, fill=self.c(shadow), anchor=anchor)
            d.text((X, Y), s, font=f, fill=self.c(col), anchor=anchor)
        out = up.resize((W * 4, H * 4), Image.NEAREST)
        out = out.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        out.save(path, optimize=True)
        return out


# --- shared UI pieces -----------------------------------------------------
def panel(cv, x, y, w, h, fill="ink1", edge="parch0", inner="ink2"):
    cv.rect(x + 1, y + 1, w - 2, h - 2, fill)
    cv.frame(x, y, w, h, edge)
    cv.frame(x + 1, y + 1, w - 2, h - 2, inner)
    for cx, cy in ((x, y), (x + w - 1, y), (x, y + h - 1), (x + w - 1, y + h - 1)):
        cv.dot(cx, cy, None if False else "ink0")


def bar(cv, x, y, w, h, frac, fg, bg="ink2", edge="ink0", hi=None):
    cv.rect(x - 1, y - 1, w + 2, h + 2, edge)
    cv.rect(x, y, w, h, bg)
    fw = int(round(w * frac))
    cv.rect(x, y, fw, h, fg)
    if hi and fw > 1:
        cv.rect(x, y, fw, 1, hi)


def coin(cv, x, y, big=False):
    if big:
        cv.sprite([".GGG.", "GYYYG", "GY.YG", "GYYYG", ".GGG."], x, y,
                  {"G": "gold0", "Y": "gold2"})
    else:
        cv.sprite([".G.", "GYG", ".G."], x, y, {"G": "gold0", "Y": "gold2"})


class Layer(Canvas):
    """Transparent drawing layer; paste onto a Canvas with an automatic outline."""

    def __init__(self, seed=1):
        self.img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        self.px = self.img.load()
        self.rng = random.Random(seed)
        self.texts = []

    def c(self, col):
        rgb = P[col] if isinstance(col, str) else col
        return tuple(rgb[:3]) + (255,)

    def paste(self, cv, outline="ink0"):
        src = self.px
        if outline:
            oc = P[outline] if isinstance(outline, str) else outline
            for j in range(H):
                for i in range(W):
                    if src[i, j][3]:
                        continue
                    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ii, jj = i + di, j + dj
                        if 0 <= ii < W and 0 <= jj < H and src[ii, jj][3]:
                            cv.px[i, j] = oc
                            break
        for j in range(H):
            for i in range(W):
                if src[i, j][3]:
                    cv.px[i, j] = src[i, j][:3]


def pine(cv, x, y, h, dark="moss0", mid="moss", trunk="brown0", seed=0):
    """Korean red pine: crooked trunk with flat umbrella clumps. (x, y) = trunk base."""
    rng = random.Random(seed)
    tx = x
    for j in range(h):
        if j % 5 == 4:
            tx += rng.choice((-1, 0, 1))
        cv.dot(tx, y - j, trunk); cv.dot(tx + 1, y - j, trunk)
    for k in range(4):
        cy = y - h + k * (h // 5) + 1
        cx = tx + rng.randint(-6, 6)
        rw = 5 + rng.randint(0, 5) + k
        cv.disc(cx, cy + 1, rw, dark, ry=2)
        cv.disc(cx - 1, cy, rw - 1, mid, ry=1.5)


def giwa(cv, x, y, w, h, roof="ink1", edge="ink2", ridge="ink0"):
    """Tiled roof with upturned eaves; (x, y) = top-left of the roof box."""
    for j in range(h):
        inset = int((h - 1 - j) * 1.6)
        for i in range(x + inset - 2, x + w - inset + 2):
            cv.dot(i, y + j, roof)
    for i in range(x - 3, x + w + 3):
        t = min(i - (x - 3), (x + w + 3) - i)
        lift = 2 if t < 3 else (1 if t < 7 else 0)
        cv.dot(i, y + h - lift, edge)
        cv.dot(i, y + h - lift - 1, roof)
    for i in range(x + int((h - 1) * 1.6) - 3, x + w - int((h - 1) * 1.6) + 3):
        cv.dot(i, y - 1, ridge)
    for i in range(x, x + w, 3):
        for j in range(2, h - 1):
            if cv.get(i, y + j) == P[roof]:
                cv.dot(i, y + j, edge)
