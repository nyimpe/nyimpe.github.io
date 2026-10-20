"""Pixel mockup of the branching area map screen."""
import random
import sys
from PIL import Image, ImageDraw
from battle import W, H, S, INK, CREAM, CREAM_D, BROWN, BROWN_D, font, outline, fish_sprite, cat_sprite

PAPER = (246, 236, 208)
random.seed(7)


def paper(d):
    d.rectangle([0, 12, 212, H], fill=PAPER)
    for _ in range(500):
        x, y = random.randrange(0, 212), random.randrange(12, H)
        d.point((x, y), fill=(236, 222, 190))
    # river winding from the bottom to the boss
    import math
    for y in range(12, H):
        cx = 106 + 30 * math.sin((y - 12) / 26)
        d.line([cx - 9, y, cx + 9, y], fill=(176, 214, 232))
        if y % 5 == 0:
            d.point((cx - 3 + (y % 7), y), fill=(214, 236, 246))
    for x, y in [(18, 30), (190, 44), (24, 118), (196, 128), (180, 90), (30, 74), (14, 158), (198, 166)]:
        for i in range(5):
            d.line([x - i // 2, y + i, x + i // 2, y + i], fill=(150, 190, 140))
        d.point((x, y + 5), fill=BROWN)


def icon(d, kind, x, y, dim=False):
    """Draw a node icon centred on (x, y) inside a round plate."""
    ring = (150, 140, 120) if dim else INK
    plate = (232, 224, 204) if dim else (255, 252, 242)
    r = 6
    if kind == "boss":
        r = 11
        d.ellipse([x - r - 1, y - r - 1, x + r + 1, y + r + 1], fill=(200, 60, 50))
    d.ellipse([x - r, y - r, x + r, y + r], fill=plate, outline=ring)
    c = lambda col: (190, 180, 160) if dim else col
    if kind == "fight":
        d.ellipse([x - 2, y - 1, x + 2, y + 3], fill=c((176, 96, 50)))
        for dx, dy in [(-3, -3), (-1, -4), (1, -4), (3, -3)]:
            d.point((x + dx, y + dy), fill=c((176, 96, 50)))
    elif kind == "elite":
        d.ellipse([x - 3, y - 2, x + 3, y + 4], fill=c((220, 70, 60)))
        d.polygon([(x - 3, y - 1), (x - 4, y - 5), (x - 1, y - 2)], fill=c((250, 210, 90)))
        d.polygon([(x + 3, y - 1), (x + 4, y - 5), (x + 1, y - 2)], fill=c((250, 210, 90)))
        d.point([(x - 1, y + 1), (x + 1, y + 1)], fill=c(INK))
    elif kind == "rest":
        d.polygon([(x - 4, y - 1), (x, y - 5), (x + 4, y - 1)], fill=c((90, 90, 110)))
        d.rectangle([x - 3, y - 1, x + 3, y + 3], fill=c((236, 220, 190)))
        d.rectangle([x - 1, y, x + 1, y + 2], fill=c((255, 200, 60)))
    elif kind == "shop":
        d.ellipse([x - 3, y - 2, x + 3, y + 4], fill=c((250, 200, 60)))
        d.rectangle([x - 1, y - 4, x + 1, y - 2], fill=c((176, 120, 60)))
        d.point((x, y + 1), fill=c(BROWN_D))
    elif kind == "event":
        col = c((130, 90, 190))
        d.line([x - 2, y - 3, x + 1, y - 3], fill=col)
        d.line([x + 2, y - 2, x + 2, y - 1], fill=col)
        d.line([x + 1, y, x, y], fill=col)
        d.line([x, y + 1, x, y + 1], fill=col)
        d.point((x, y + 3), fill=col)
    elif kind == "treasure":
        d.rectangle([x - 4, y - 2, x + 4, y + 3], fill=c((170, 104, 54)))
        d.rectangle([x - 4, y - 2, x + 4, y - 1], fill=c((120, 70, 40)))
        d.rectangle([x - 1, y - 2, x + 1, y + 1], fill=c((250, 200, 60)))
    elif kind == "start":
        d.rectangle([x - 2, y - 2, x + 2, y + 2], fill=c((120, 170, 100)))


ROWS = [
    [(106, 166, "start")],
    [(62, 148, "fight"), (106, 148, "event"), (150, 148, "fight")],
    [(80, 130, "rest"), (136, 130, "fight")],
    [(52, 112, "shop"), (106, 112, "elite"), (162, 112, "event")],
    [(78, 94, "fight"), (140, 94, "treasure")],
    [(56, 76, "elite"), (106, 76, "rest"), (156, 76, "fight")],
    [(106, 46, "boss")],
]
EDGES = {
    (0, 0): [0, 1, 2],
    (1, 0): [0], (1, 1): [0, 1], (1, 2): [1],
    (2, 0): [0, 1], (2, 1): [1, 2],
    (3, 0): [0], (3, 1): [0, 1], (3, 2): [1],
    (4, 0): [0, 1], (4, 1): [1, 2],
    (5, 0): [0], (5, 1): [0], (5, 2): [0],
}
VISITED = {(0, 0), (1, 2), (2, 1)}
CURRENT = (2, 1)


def dotted(d, a, b, col, step=3):
    import math
    n = int(math.dist(a, b) / step)
    for i in range(1, n):
        t = i / n
        d.point((round(a[0] + (b[0] - a[0]) * t), round(a[1] + (b[1] - a[1]) * t)), fill=col)


def main():
    lo = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    d = ImageDraw.Draw(lo)
    paper(d)
    # edges
    for (r, i), nexts in EDGES.items():
        a = ROWS[r][i][:2]
        for j in nexts:
            b = ROWS[r + 1][j][:2]
            walked = (r, i) in VISITED and (r + 1, j) in VISITED
            if walked:
                d.line([a, b], fill=(214, 110, 40), width=2)
            else:
                dotted(d, a, b, (150, 120, 90))
    # skip arrow from the current node over one row (horse skill)
    cur = ROWS[CURRENT[0]][CURRENT[1]][:2]
    tgt = ROWS[4][1][:2]
    ctrl = (cur[0] + 30, (cur[1] + tgt[1]) / 2)
    for k in range(2, 30, 2):
        t = k / 30
        bx = (1 - t) ** 2 * cur[0] + 2 * (1 - t) * t * ctrl[0] + t * t * tgt[0]
        by = (1 - t) ** 2 * cur[1] + 2 * (1 - t) * t * ctrl[1] + t * t * tgt[1]
        d.rectangle([round(bx), round(by), round(bx) + 1, round(by) + 1], fill=(70, 130, 210))
    for r, row in enumerate(ROWS):
        for i, (x, y, kind) in enumerate(row):
            icon(d, kind, x, y, dim=(r, i) in VISITED and (r, i) != CURRENT)
    # boss portrait inside the boss node
    bx, by = ROWS[-1][0][:2]
    mini = fish_sprite().crop((0, 0, 70, 56)).resize((22, 18), Image.NEAREST)
    lo.alpha_composite(mini, (bx - 10, by - 9))
    # cat token on the current node
    d.ellipse([cur[0] - 9, cur[1] - 9, cur[0] + 9, cur[1] + 9], outline=(255, 196, 40))
    face = Image.new("RGBA", (16, 15), (0, 0, 0, 0))
    f = ImageDraw.Draw(face)
    f.polygon([(2, 6), (3, 1), (7, 4)], fill=(249, 150, 70))
    f.polygon([(13, 6), (12, 1), (8, 4)], fill=(253, 253, 253))
    f.ellipse([1, 3, 14, 13], fill=(253, 253, 253))
    f.pieslice([1, 3, 14, 13], 180, 270, fill=(249, 150, 70))
    f.rectangle([4, 7, 5, 8], fill=INK)
    f.rectangle([10, 7, 11, 8], fill=INK)
    f.point((7, 10), fill=(240, 150, 160))
    face = outline(face)
    lo.alpha_composite(face, (cur[0] - 22, cur[1] - 14))

    # right info panel
    d.rectangle([212, 12, W, H], fill=BROWN_D)
    d.rectangle([215, 14, W - 3, H - 3], fill=CREAM)
    for y0, y1 in [(16, 62), (66, 100), (104, 174)]:
        d.rectangle([218, y0, W - 6, y1], fill=(255, 250, 236), outline=CREAM_D)
    fish = fish_sprite().resize((52, 44), Image.NEAREST)
    lo.alpha_composite(fish, (262, 17))
    legend = ["fight", "elite", "rest", "shop", "event", "treasure"]
    for k, kind in enumerate(legend):
        icon(d, kind, 227 + (k % 2) * 48, 122 + (k // 2) * 17)

    # HUD
    d.rectangle([0, 0, W, 11], fill=(255, 250, 236))
    d.line([0, 11, W, 11], fill=BROWN)
    d.ellipse([289, 2, 296, 9], fill=(250, 200, 60), outline=BROWN_D)
    d.rectangle([292, 5, 293, 6], fill=BROWN_D)

    big = lo.resize((W * S, H * S), Image.NEAREST).convert("RGB")
    t = ImageDraw.Draw(big)

    def text(xy, s, size, fill=INK, bold=True, anchor="la"):
        t.text((xy[0] * S, xy[1] * S), s, font=font(size, bold), fill=fill, anchor=anchor)

    text((4, 1.6), "강 · 지도", 26)
    text((160, 1.6), "나비 체력 22/30", 26, anchor="ma")
    text((250, 1.6), "꼬리 3", 26)
    text((298, 1.6), "42", 26)

    text((221, 17.5), "우두머리", 22, fill=(200, 60, 50))
    text((221, 50), "용이 되고 싶은 물고기", 21)
    text((221, 55.6), "체력 55 · 비를 부른다", 19, fill=(110, 90, 70), bold=False)

    text((221, 68), "가진 재주", 22, fill=(200, 110, 40))
    text((221, 74.6), "말 재주 · 돌진", 21)
    text((221, 81.2), "칸 건너뛰기 1번 남음", 19, fill=(70, 110, 190), bold=False)

    text((221, 106), "칸 안내", 22)
    names = ["잡요괴", "이름난 요괴", "쉬는 칸", "상점", "사건", "보물"]
    for k, name in enumerate(names):
        text((235 + (k % 2) * 48, 122 + (k // 2) * 17), name, 19, bold=False, anchor="lm")

    # label for the skip arc
    t.text((151 * S, 90.5 * S), "건너뛰기", font=font(19), fill=(70, 110, 190))
    t.text(((cur[0] + 12) * S, (cur[1] + 3) * S), "지금 여기", font=font(19), fill=(214, 110, 40))
    big.save(sys.argv[1])


if __name__ == "__main__":
    main()
