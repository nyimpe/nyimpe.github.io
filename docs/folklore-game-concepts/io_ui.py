"""Shared HUD pieces for the .io concept screens: leaderboard, minimap, tags."""
from pix import *


def leaderboard(cv, rows, me, x=232, y=4, w=84, title="순위"):
    h = 12 + len(rows) * 9
    cv.rect(x, y, w, h, "ink0"); cv.frame(x, y, w, h, "ink2")
    cv.text(x + 4, y + 1.5, title, "gold2", 10)
    for k, (name, score) in enumerate(rows):
        yy = y + 11 + k * 9
        col = "gold2" if name == me else "parch"
        if name == me:
            cv.rect(x + 1, yy, w - 2, 9, "ink2")
        cv.text(x + 4, yy + 0.5, f"{k + 1}. {name}", col, 10)
        cv.text(x + w - 4, yy + 0.5, score, col, 10, anchor="ra")


def minimap(cv, x, y, w, h, dots, me, bg="ink0"):
    cv.rect(x, y, w, h, bg); cv.frame(x, y, w, h, "ink2")
    for dx, dy, col in dots:
        cv.rect(x + dx, y + dy, 2, 2, col)
    cv.rect(x + me[0] - 1, y + me[1] - 1, 3, 3, "white")


def tag(cv, x, y, text, fg="parch2", bg="ink0", edge="gold0"):
    w = int(len(text) * 5.2) + 8
    cv.rect(x, y, w, 12, bg); cv.frame(x, y, w, 12, edge)
    cv.text(x + 4, y + 2, text, fg, 10)
    return w


def nick(cv, x, y, name, col="white"):
    cv.text(x, y, name, col, 10, anchor="ma")
