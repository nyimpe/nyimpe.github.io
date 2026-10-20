"""Hand-drawn pixel mockup of a battle screen for the cat yokai roguelike plan."""
import math
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO = Path(__file__).resolve().parents[2]
W, H, S = 320, 180, 4  # low-res canvas and integer upscale
FONT = "/System/Library/Fonts/AppleSDGothicNeo.ttc"

INK = (38, 28, 36)
CREAM = (247, 236, 209)
CREAM_D = (226, 207, 166)
BROWN = (122, 78, 46)
BROWN_D = (84, 52, 32)


def font(size, bold=True):
    # AppleSDGothicNeo.ttc: index 6 is Bold, 0 is Regular on current macOS
    return ImageFont.truetype(FONT, size, index=6 if bold else 0)


def outline(layer, color=INK):
    """Add a 1px outline around every opaque pixel of an RGBA layer."""
    alpha = layer.getchannel("A").point(lambda a: 255 if a > 0 else 0)
    grown = alpha.filter(ImageFilter.MaxFilter(3))
    ring = Image.new("RGBA", layer.size, color + (255,))
    base = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    base.paste(ring, mask=grown)
    base.alpha_composite(layer)
    return base


def sky(img):
    d = ImageDraw.Draw(img)
    bands = [(150, 214, 240), (166, 222, 243), (182, 229, 245), (199, 236, 247), (214, 241, 248)]
    for i, c in enumerate(bands):
        d.rectangle([0, i * 14, W, i * 14 + 14], fill=c)
    d.rectangle([0, 70, W, 100], fill=bands[-1])
    # clouds
    for cx, cy, r in [(40, 18, 7), (52, 15, 9), (64, 19, 6), (120, 30, 5), (130, 27, 7), (140, 31, 5)]:
        d.ellipse([cx - r, cy - r * 0.7, cx + r, cy + r * 0.7], fill=(255, 255, 255))


def hills(img):
    d = ImageDraw.Draw(img)
    for x in range(W):
        y1 = 68 + 8 * math.sin(x / 23) + 5 * math.sin(x / 9 + 1)
        d.line([x, y1, x, 110], fill=(126, 190, 120))
        y2 = 82 + 6 * math.sin(x / 17 + 2) + 3 * math.sin(x / 7)
        d.line([x, y2, x, 110], fill=(96, 168, 98))
    # pines
    for px, base in [(20, 92), (34, 95), (150, 88), (164, 92)]:
        for i in range(10):
            half = 1 + i // 2
            d.line([px - half, base - 18 + i * 2, px + half, base - 18 + i * 2], fill=(52, 120, 76))
            d.line([px - half, base - 17 + i * 2, px + half, base - 17 + i * 2], fill=(52, 120, 76))
        d.rectangle([px - 1, base + 2, px, base + 5], fill=BROWN_D)


def waterfall(img):
    d = ImageDraw.Draw(img)
    d.polygon([(256, 104), (258, 30), (264, 22), (272, 16), (306, 14), (314, 20), (320, 18), (320, 104)], fill=(118, 120, 128))
    d.polygon([(256, 104), (258, 30), (264, 22), (270, 104)], fill=(140, 142, 150))
    d.polygon([(306, 104), (306, 14), (314, 20), (320, 18), (320, 104)], fill=(100, 102, 112))
    d.rectangle([272, 16, 302, 104], fill=(170, 216, 240))
    for x in range(272, 303, 3):
        d.line([x, 16, x, 104], fill=(234, 247, 252))
    for x in range(274, 303, 7):
        d.line([x, 30, x, 104], fill=(255, 255, 255))
    for x, y in [(262, 40), (310, 50), (260, 70), (312, 80)]:
        d.rectangle([x, y, x + 2, y + 1], fill=(96, 98, 106))


def pond_and_bank(img):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 104, W, 128], fill=(90, 168, 214))
    for y in range(106, 128, 4):
        for x in range((y * 7) % 13, W, 26):
            d.line([x, y, x + 6, y], fill=(150, 210, 238))
    # foam under the waterfall
    for cx in range(266, 312, 6):
        d.ellipse([cx - 4, 101, cx + 4, 108], fill=(240, 250, 255))
    # left bank
    pts = [(0, 100), (120, 100), (138, 108), (142, 128), (0, 128)]
    d.polygon(pts, fill=(196, 176, 120))
    d.polygon([(0, 98), (116, 98), (126, 103), (0, 103)], fill=(118, 186, 96))
    for x in range(6, 118, 9):
        d.line([x, 97, x + 1, 94], fill=(80, 150, 80))
    # reeds
    for x in [132, 136, 141, 146]:
        d.line([x, 112, x, 100], fill=(70, 130, 70))
        d.rectangle([x - 1, 98, x, 101], fill=BROWN)


def cat_sprite(height):
    src = Image.open(f"{REPO}/public/cat.png").convert("RGBA")
    w = round(src.width * height / src.height)
    small = src.resize((w, height), Image.BOX)
    pal = [(24, 20, 28), (253, 253, 253), (214, 212, 226), (249, 150, 70), (214, 110, 40), (240, 150, 160), (60, 36, 26)]
    out = Image.new("RGBA", small.size, (0, 0, 0, 0))
    sp, op = small.load(), out.load()
    for y in range(small.height):
        for x in range(small.width):
            r, g, b, a = sp[x, y]
            if a < 110:
                continue
            c = min(pal, key=lambda p: (p[0] - r) ** 2 + (p[1] - g) ** 2 + (p[2] - b) ** 2)
            op[x, y] = c + (255,)
    return out


def fish_sprite():
    layer = Image.new("RGBA", (124, 104), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    body = (246, 154, 52)
    belly = (255, 214, 120)
    red = (226, 64, 60)
    pts = []
    n = 40
    for i in range(n):
        t = i / (n - 1)
        x = 18 + 88 * t
        y = 22 + 58 * t ** 1.6
        r = 13 * (1 - t) ** 0.7 + 2
        pts.append((x, y, r, t))
    def normal(i):
        a = pts[max(i - 1, 0)]
        b = pts[min(i + 1, n - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = dy / L, -dx / L
        return (nx, ny) if ny < 0 else (-nx, -ny)
    # dorsal spikes on the upper side
    for i in range(6, 30, 3):
        x, y, r, t = pts[i]
        nx, ny = normal(i)
        tip = (x + nx * (r + 6), y + ny * (r + 6))
        d.polygon([(x + nx * r - 3, y + ny * r), (x + nx * r + 3, y + ny * r), tip], fill=red)
    for x, y, r, t in pts:
        d.ellipse([x - r, y - r, x + r, y + r], fill=body)
    for i, (x, y, r, t) in enumerate(pts[:32]):
        nx, ny = normal(i)
        bx, by = x - nx * r * 0.45, y - ny * r * 0.45
        d.ellipse([bx - r * 0.55, by - r * 0.55, bx + r * 0.55, by + r * 0.55], fill=belly)
    for i in range(5, 30, 3):
        x, y, r, t = pts[i]
        nx, ny = normal(i)
        d.point([(x + nx * r * 0.35, y + ny * r * 0.35), (x + nx * r * 0.35 + 2, y + ny * r * 0.35 + 1)], fill=(214, 108, 34))
    hx, hy, hr, _ = pts[0]
    # pectoral fin
    d.polygon([(hx + 8, hy + 10), (hx + 2, hy + 20), (hx + 14, hy + 15)], fill=red)
    # horns
    d.polygon([(hx - 1, hy - 12), (hx + 1, hy - 21), (hx + 4, hy - 12)], fill=(255, 228, 140))
    d.polygon([(hx + 5, hy - 11), (hx + 9, hy - 19), (hx + 10, hy - 9)], fill=(255, 228, 140))
    # eye and mouth
    d.ellipse([hx - 9, hy - 7, hx - 1, hy + 1], fill=(255, 255, 255))
    d.rectangle([hx - 7, hy - 5, hx - 4, hy - 2], fill=INK)
    d.point((hx - 7, hy - 5), fill=(255, 255, 255))
    d.polygon([(hx - 15, hy + 4), (hx - 8, hy + 3), (hx - 10, hy + 7)], fill=(150, 40, 40))
    # forked tail fin at the end
    tx, ty, tr, _ = pts[-1]
    d.polygon([(tx - 2, ty - 1), (tx + 12, ty - 10), (tx + 7, ty + 1), (tx + 13, ty + 11)], fill=red)
    layer = outline(layer, (110, 44, 24))
    d = ImageDraw.Draw(layer)
    for k in range(18):
        d.point((hx - 13 - k, hy + 6 + int(3 * math.sin(k / 3))), fill=(110, 44, 24))
        d.point((hx - 11 - k, hy + 1 - int(3 * math.sin(k / 4))), fill=(110, 44, 24))
    return layer


def rain_cloud(img, x, y):
    d = ImageDraw.Draw(img)
    for cx, cy, r in [(x, y, 8), (x + 10, y - 3, 10), (x + 22, y, 8), (x + 32, y + 1, 6)]:
        d.ellipse([cx - r, cy - r * 0.7, cx + r, cy + r * 0.7], fill=(150, 156, 170))
    d.rectangle([x - 6, y, x + 36, y + 4], fill=(150, 156, 170))
    for rx in range(x - 3, x + 36, 5):
        d.line([rx, y + 7, rx - 1, y + 11], fill=(120, 170, 220))


def panel(img):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 128, W, H], fill=BROWN_D)
    d.rectangle([2, 130, W - 3, H - 3], fill=CREAM)
    d.rectangle([2, 130, W - 3, 131], fill=CREAM_D)


def hud(img):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 11], fill=(255, 250, 236))
    d.line([0, 11, W, 11], fill=BROWN)


def bar(img, x, y, w, ratio, color):
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w, y + 4], fill=INK)
    d.rectangle([x + 1, y + 1, x + w - 1, y + 3], fill=(90, 70, 70))
    d.rectangle([x + 1, y + 1, x + 1 + round((w - 2) * ratio), y + 3], fill=color)


SKILLS = [
    {"name": "할퀴기", "kind": "공격", "line": "피해 6", "color": (226, 84, 70), "state": "ready"},
    {"name": "웅크리기", "kind": "막기", "line": "막기 6", "color": (70, 130, 210), "state": "selected"},
    {"name": "돌진", "kind": "말 재주", "line": "피해 14", "color": (236, 150, 50), "state": "cooldown", "wait": 2},
    {"name": "비어 있음", "kind": "", "line": "강 끝에서 배움", "color": (180, 170, 150), "state": "locked"},
]


def skill_buttons(img):
    d = ImageDraw.Draw(img)
    boxes = []
    for i, s in enumerate(SKILLS):
        x0 = 8 + i * 77
        box = [x0, 136, x0 + 71, 173]
        boxes.append(box)
        if s["state"] == "locked":
            for x in range(box[0], box[2], 4):
                d.line([x, box[1], x + 1, box[1]], fill=BROWN)
                d.line([x, box[3], x + 1, box[3]], fill=BROWN)
            for y in range(box[1], box[3], 4):
                d.line([box[0], y, box[0], y + 1], fill=BROWN)
                d.line([box[2], y, box[2], y + 1], fill=BROWN)
            # lock icon
            lx, ly = box[0] + 8, box[1] + 9
            d.rectangle([lx, ly + 4, lx + 8, ly + 11], fill=(150, 130, 100))
            d.arc([lx + 1, ly, lx + 7, ly + 8], 180, 360, fill=(150, 130, 100))
            continue
        face = (255, 252, 242) if s["state"] != "cooldown" else (214, 206, 190)
        d.rectangle(box, fill=INK)
        d.rectangle([box[0] + 1, box[1] + 1, box[2] - 1, box[3] - 1], fill=face)
        d.rectangle([box[0] + 1, box[1] + 1, box[2] - 1, box[1] + 3], fill=s["color"] if s["state"] != "cooldown" else (170, 160, 150))
        if s["state"] == "selected":
            d.rectangle([box[0] - 2, box[1] - 2, box[2] + 2, box[3] + 2], outline=(255, 196, 40))
            d.rectangle([box[0] - 3, box[1] - 3, box[2] + 3, box[3] + 3], outline=INK)
    return boxes


def snail(img, x, y):
    d = ImageDraw.Draw(img)
    d.ellipse([x + 2, y, x + 8, y + 6], fill=(214, 150, 90), outline=BROWN_D)
    d.rectangle([x, y + 5, x + 10, y + 6], fill=(170, 200, 120))
    d.point([(x + 10, y + 3), (x + 9, y + 4)], fill=BROWN_D)


def label_box(img, x0, y0, x1, y1):
    d = ImageDraw.Draw(img)
    d.rectangle([x0, y0, x1, y1], fill=INK)
    d.rectangle([x0 + 1, y0 + 1, x1 - 1, y1 - 1], fill=(64, 52, 60))


def main():
    lo = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    sky(lo)
    hills(lo)
    waterfall(lo)
    pond_and_bank(lo)
    rain_cloud(lo, 226, 50)

    fish = fish_sprite()
    lo.alpha_composite(fish, (162, 30))
    d = ImageDraw.Draw(lo)
    d.ellipse([254, 112, 290, 120], outline=(240, 250, 255))
    d.ellipse([246, 114, 298, 124], outline=(200, 236, 250))

    cat = outline(cat_sprite(58), (24, 20, 28))
    d.ellipse([58, 99, 92, 105], fill=(170, 150, 100))
    lo.alpha_composite(cat, (60, 44))

    hud(lo)
    panel(lo)
    boxes = skill_buttons(lo)

    # name plates with health bars
    label_box(lo, 8, 15, 98, 33)
    bar(lo, 12, 26, 82, 22 / 30, (110, 200, 90))
    label_box(lo, 210, 15, 314, 33)
    bar(lo, 214, 26, 96, 41 / 55, (230, 80, 70))
    # slow status chip
    d.rectangle([8, 35, 40, 44], fill=(255, 244, 214), outline=BROWN)
    snail(lo, 10, 36)

    # intent bubble above the fish head
    d.rectangle([136, 16, 196, 32], fill=INK)
    d.rectangle([137, 17, 195, 31], fill=(255, 252, 242))
    d.polygon([(170, 32), (178, 32), (178, 37)], fill=INK)
    d.ellipse([140, 20, 148, 26], fill=(150, 156, 170))
    d.ellipse([144, 18, 152, 26], fill=(150, 156, 170))
    d.line([142, 28, 141, 30], fill=(120, 170, 220))
    d.line([146, 28, 145, 30], fill=(120, 170, 220))
    # coin icon in the HUD
    d.ellipse([289, 2, 296, 9], fill=(250, 200, 60), outline=BROWN_D)
    d.rectangle([292, 5, 293, 6], fill=BROWN_D)

    big = lo.resize((W * S, H * S), Image.NEAREST).convert("RGB")
    t = ImageDraw.Draw(big)

    def text(xy, s, size, fill=INK, bold=True, anchor="la"):
        t.text((xy[0] * S, xy[1] * S), s, font=font(size, bold), fill=fill, anchor=anchor)

    text((4, 1.6), "강 · 우두머리", 26)
    text((160, 1.6), "3번째 턴 · 나비 차례", 26, anchor="ma")
    text((250, 1.6), "꼬리 3", 26)
    text((298, 1.6), "42", 26)

    text((12, 16.6), "나비", 26, fill=(255, 246, 226))
    text((94, 17.2), "22/30", 22, fill=(255, 246, 226), anchor="ra")
    text((22, 35.4), "느림", 22, fill=(120, 70, 40))
    text((214, 16.6), "용이 되고 싶은 물고기", 24, fill=(255, 246, 226))
    text((310, 17.2), "41/55", 22, fill=(255, 246, 226), anchor="ra")
    text((154, 17.6), "비 부르기", 24)
    text((154, 24.2), "다음 턴 물살 18", 20, fill=(120, 90, 70), bold=False)

    # speech bubble from the fish
    sx, sy = 112, 52
    t.polygon([((sx + 50) * S, (sy + 4) * S), ((sx + 58) * S, (sy + 7) * S), ((sx + 50) * S, (sy + 9) * S)], fill=INK)
    t.rounded_rectangle([sx * S, sy * S, (sx + 51) * S, (sy + 12) * S], radius=10, fill=(255, 255, 255), outline=INK, width=4)
    t.text(((sx + 25.5) * S, (sy + 6) * S), "나도 용이 될 거야!", font=font(22), fill=INK, anchor="mm")

    for s, b in zip(SKILLS, boxes):
        x0, y0 = b[0] * S, b[1] * S
        if s["state"] == "locked":
            t.text((x0 + 76, y0 + 40), s["name"], font=font(24), fill=(150, 130, 100))
            t.text((x0 + 76, y0 + 76), s["line"], font=font(20, False), fill=(150, 130, 100))
            continue
        muted = s["state"] == "cooldown"
        t.text((x0 + 18, y0 + 26), s["name"], font=font(30), fill=(120, 110, 100) if muted else INK)
        if s["kind"]:
            t.text((x0 + 18, y0 + 66), s["kind"], font=font(20, False), fill=(130, 110, 90))
        t.text((x0 + 18, y0 + 100), s["line"], font=font(24), fill=(120, 110, 100) if muted else s["color"])
        if muted:
            cx, cy = (b[2] - 12) * S, (b[1] + 14) * S
            t.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=INK)
            t.text((cx, cy), str(s["wait"]), font=font(44), fill=(255, 255, 255), anchor="mm")
            t.text((x0 + 18, y0 + 128), "쉬는 턴 2", font=font(18, False), fill=(120, 110, 100))

    big.save(sys.argv[1])


if __name__ == "__main__":
    main()
