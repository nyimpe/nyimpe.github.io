"""Concept 21 — lineage roguelite after Rogue Legacy (dragon-blood heirs with folklore traits)."""
import math
from pix import *

cv = Canvas("teal0", seed=331)
rng = cv.rng

# Undersea palace backdrop -----------------------------------------------------------------------------
cv.vgrad(0, H, ["teal", "teal0", "night1", "night0"])
for k in range(3):
    x = 30 + k * 100
    cv.rect(x, 120, 70, 40, "night1")
    giwa(cv, x - 6, 106, 82, 12, roof="night0", edge="teal0", ridge="night0")
for _ in range(40):
    x, y = rng.randrange(W), rng.randrange(H)
    cv.ring(x, y, rng.choice((1, 2)), "teal2")

# Family tree of fallen heirs --------------------------------------------------------------------------
graves = [(60, "1대 용녀", "해룡의 궁에서"), (160, "2대 맏아들", "장수피 떼에게"), (260, "3대 둘째", "탄주어 뱃속에서")]
cv.line(60, 14, 260, 14, "gold0")
for x, name, death in graves:
    cv.line(x, 14, x, 20, "gold0")
    cv.sprite([".GGGG.", "GGGGGG", "GGKKGG", "GGGGGG", "GGGGGG"], x - 3, 20, {"G": "iron2", "K": "iron0"}, outline="ink0")
    cv.text(x, 27, name, "parch2", 10, anchor="ma")
    cv.text(x, 35, death, "ghost", 10, anchor="ma")
cv.text(160, 2, "용손 가문 · 넷째 대를 고르시오", "gold2", 11, anchor="ma")

# Three heirs, each with traits drawn from the catalog ----------------------------------------------------
def heir(x, name, traits, art, chosen=False):
    cv.rect(x, 50, 92, 98, "night0"); cv.frame(x, 50, 92, 98, "gold2" if chosen else "teal2")
    if chosen:
        cv.frame(x + 1, 51, 90, 96, "gold0")
    cv.rect(x + 26, 56, 40, 40, "teal0"); cv.frame(x + 26, 56, 40, 40, "ink2")
    art(x + 46, 76)
    cv.text(x + 46, 99, name, "gold2" if chosen else "parch2", 10, anchor="ma")
    for k, (t, good) in enumerate(traits):
        cv.text(x + 6, 110 + k * 9, ("+ " if good else "- ") + t, "moss3" if good else "pink", 10)


def face(cx, cy, skin="skin", hair="ink0"):
    cv.disc(cx, cy, 9, skin, ry=11)
    cv.disc(cx, cy - 8, 9, hair, ry=4)
    cv.rect(cx - 4, cy - 1, 2, 2, "ink0"); cv.rect(cx + 3, cy - 1, 2, 2, "ink0")
    cv.rect(cx - 2, cy + 5, 5, 1, "red0")


def heir_scales_wings(cx, cy):  # Yongson scales + Ubuma feathers
    face(cx, cy)
    for k in range(5):
        cv.dot(cx - 7 + k * 3, cy + 7 + (k % 2), "teal3")
    for side in (-1, 1):
        for k in range(4):
            cv.line(cx + side * 10, cy + 12, cx + side * (16 + k * 2), cy + 4 + k * 3, "parch2")


def heir_strong_three_eyes(cx, cy):  # Yeoyongsa strength + Sammogin third eye
    face(cx, cy, skin="skin0")
    cv.rect(cx - 1, cy - 5, 3, 2, "red2"); cv.dot(cx, cy - 5, "ink0")
    cv.rect(cx - 10, cy - 7, 20, 2, "red2")
    cv.rect(cx - 13, cy + 10, 26, 6, "skin0")


def heir_long_arms_two_faces(cx, cy):  # Jangbiin arms + Buyumyeon second face
    face(cx, cy + 3)
    cv.disc(cx, cy - 11, 6, "skin", ry=5)
    cv.rect(cx - 3, cy - 12, 2, 1, "ink0"); cv.rect(cx + 2, cy - 12, 2, 1, "ink0")
    for side in (-1, 1):
        cv.rect(cx + side * 12 - (6 if side < 0 else 0), cy + 12, 12, 3, "purple2")


heir(14, "셋째 아들 · 해랑", [("비늘: 물속 숨 길게", True), ("깃털: 두 번 뛰기", True), ("겁 많음", False)], heir_scales_wings, chosen=True)
heir(114, "둘째 딸 · 솔이", [("장사: 큰 종 들기", True), ("세 눈: 숨은 길", True), ("느림", False)], heir_strong_three_eyes)
heir(214, "막내 · 두면", [("긴 팔: 사거리 둘", True), ("얼굴 둘: 뒤도 봄", True), ("상인과 말 안 통함", False)], heir_long_arms_two_faces)

# Footer: shrine upgrades that persist ---------------------------------------------------------------------
cv.rect(0, 152, W, 28, "ink0"); cv.rect(0, 152, W, 1, "gold0")
cv.text(6, 155, "가문 사당", "gold2", 10)
for k, (name, lv) in enumerate((("대장간", 3), ("약방", 2), ("노래패", 1), ("사당 등불", 4))):
    x = 60 + k * 62
    cv.text(x, 155, name, "parch2", 10)
    for p in range(5):
        cv.rect(x + p * 6, 166, 4, 3, "gold2" if p < lv else "ink2")
cv.text(316, 165, "엽전 1,820", "gold2", 10, anchor="ra")

cv.export("concept-21-indie-lineage.png")
print("saved")
