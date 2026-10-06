"""Concept 35 — dice board after Modoo Marble (claim shrines across the eight provinces; spirits take them over)."""
from pix import *

cv = Canvas("night1", seed=471)
rng = cv.rng
T, N = 18, 9
BX, BY = 80, 9

# Ring of tiles: corners plus seven towns per side -----------------------------------------------------------------
names = ["출발", "한양", "개성", "해주", "평양", "의주", "함흥", "경성", "표류",
         "춘천", "원주", "강릉", "삼척", "울진", "경주", "동래", "단오",
         "진주", "나주", "목포", "제주", "대정", "전주", "공주", "나루",
         "청주", "충주", "안동", "상주", "부여", "수원", "인천"]


def ring():
    """Clockwise from the bottom-right corner."""
    out = []
    for i in range(N):
        out.append((N - 1 - i, N - 1))
    for j in range(N - 2, 0, -1):
        out.append((0, j))
    for i in range(N):
        out.append((i, 0))
    for j in range(1, N - 1):
        out.append((N - 1, j))
    return out


cells = ring()
region_col = ["parch2"] + ["pink"] * 7 + ["parch2"] + ["teal3"] * 7 + ["parch2"] + ["moss3"] * 7 + ["parch2"] + ["gold2"] * 7
owners = {2: "red2", 4: "flame", 11: "red2", 12: "purple2", 14: "flame", 20: "red2", 21: "flame", 26: "red2"}
cv.rect(BX - 2, BY - 2, N * T + 4, N * T + 4, "ink0")
for k, (c, r) in enumerate(cells[:len(names)]):
    x, y = BX + c * T, BY + r * T
    cv.rect(x, y, T, T, "parch"); cv.frame(x, y, T, T, "ink1")
    cv.rect(x + 1, y + 1, T - 2, 4, region_col[k] if k < len(region_col) else "parch2")
    if k in owners:  # a claimed shrine: a little seonang pole with the owner's colour
        cv.rect(x + 12, y + 6, 1, 8, "brown0")
        cv.rect(x + 13, y + 6, 4, 3, owners[k])
    cv.text(x + T / 2 - (2 if k in owners else 0), y + 8.5, names[k], "ink1", 10, shadow=None, anchor="ma")

# Board centre ------------------------------------------------------------------------------------------------------
CX0, CY0, CW = BX + T, BY + T, (N - 2) * T
cv.rect(CX0, CY0, CW, CW, "teal0")
for k in range(70):
    cv.dot(CX0 + rng.randrange(CW), CY0 + rng.randrange(CW), "teal")
cv.text(BX + N * T / 2, CY0 + 4, "팔도 서낭 마블", "gold2", 12, anchor="ma")
# Two dice just rolled
for k, pips in enumerate(((1, 1), (2, 2))):
    dx, dy = BX + N * T / 2 - 22 + k * 26, CY0 + 22
    cv.rect(dx, dy, 18, 18, "white"); cv.frame(dx, dy, 18, 18, "ink1")
for px_, py_ in ((0, 0),):
    pass
cv.disc(BX + N * T / 2 - 13, CY0 + 31, 2, "red2")                            # one
for ox, oy in ((-5, -5), (5, 5), (5, -5), (-5, 5)):                           # four
    cv.disc(BX + N * T / 2 + 13 + ox, CY0 + 31 + oy, 1.5, "ink0")
cv.text(BX + N * T / 2, CY0 + 44, "다섯 칸 → 삼척", "parch2", 10, anchor="ma")
# Event card: the blue fire spirit has taken the shrine
cv.rect(CX0 + 10, CY0 + 60, CW - 20, 58, "parch2"); cv.frame(CX0 + 10, CY0 + 60, CW - 20, 58, "purple")
L = Layer(seed=4)
L.disc(CX0 + 30, CY0 + 88, 10, "flame0", ry=12); L.disc(CX0 + 30, CY0 + 90, 7, "flame", ry=8); L.disc(CX0 + 30, CY0 + 92, 4, "flame2", ry=4)
L.paste(cv, outline="ink0")
cv.dot(CX0 + 27, CY0 + 88, "white"); cv.dot(CX0 + 33, CY0 + 88, "white")
cv.text(CX0 + 46, CY0 + 64, "요무지귀", "purple", 11, shadow=None)
cv.text(CX0 + 46, CY0 + 78, "삼척 서낭을 차지해", "ink1", 10, shadow=None)
cv.text(CX0 + 46, CY0 + 89, "제물을 받아먹는다", "ink1", 10, shadow=None)
cv.rect(CX0 + 44, CY0 + 102, 34, 12, "red0"); cv.text(CX0 + 61, CY0 + 103.5, "제물 120", "gold2", 10, anchor="ma")
cv.rect(CX0 + 82, CY0 + 102, 34, 12, "ink1"); cv.text(CX0 + 99, CY0 + 103.5, "부적 쓰기", "parch2", 10, anchor="ma")

# Player pieces on the board
for k, col in ((12, "gold2"), (5, "red2"), (21, "flame")):
    c, r = cells[k]
    x, y = BX + c * T + 7, BY + r * T + 6
    x += 15 if c == 0 else (-15 if c == N - 1 else 0)    # stand just inside the ring, off the town name
    y += 15 if r == 0 else (-15 if r == N - 1 else 0)
    cv.sprite(["..K..", ".KCK.", ".KCK.", "KCCCK", "KCCCK"], x - 1, y - 2, {"K": "ink0", "C": col}, outline="white")

# Side panels: players and their money ----------------------------------------------------------------------------
players = [("나", "gold2", "엽전 860", "서낭 0"), ("도깨비", "red2", "엽전 1,240", "서낭 4"), ("여우", "flame", "엽전 530", "서낭 3"),
           ("요무지귀", "purple2", "제물 ∞", "서낭 1")]
for k, (name, col, money, shrines) in enumerate(players):
    x = 4 if k < 2 else 246
    y = 12 + (k % 2) * 82
    panel(cv, x, y, 70, 72)
    cv.rect(x + 6, y + 6, 14, 14, col); cv.frame(x + 6, y + 6, 14, 14, "ink0")
    cv.text(x + 24, y + 7, name, col, 11)
    cv.text(x + 6, y + 28, money, "parch2", 10)
    cv.text(x + 6, y + 42, shrines, "parch0", 10)
    if k == 0:
        cv.text(x + 6, y + 56, "내 차례", "gold2", 10)

cv.export("concept-35-turn-board.png")
print("saved")
