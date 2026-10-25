"""Original flat illustrations for the picture-vocab bank (CC0).

Draws one WebP per item in js/vocab-data.js. From the repo root:

    python3 assets/vocab/generate_images.py

Requires Pillow. The site itself does not need this script or Pillow.
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw

S = 2
W, H = 640 * S, 480 * S
OUT = Path(__file__).resolve().parent / "images"

RED = "#ef4d4d"
RED_DARK = "#d63c3c"
GREEN = "#3cb371"
GREEN_DARK = "#2e9a5c"
YELLOW = "#ffd23f"
ORANGE = "#f5a023"
BROWN = "#8a5332"
BLUE = "#4d90f0"
BLUE_DARK = "#2f6fd0"
NAVY = "#2c3e50"
PINK = "#ff8fab"
PURPLE = "#7d5cc7"
CREAM = "#f6d7b0"
WHITE = "#ffffff"
INK = "#243044"


def circle(d, cx, cy, r, fill):
    cx, cy, r = cx * S, cy * S, r * S
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)


def ellipse(d, cx, cy, rx, ry, fill):
    d.ellipse([(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S], fill=fill)


def rrect(d, x0, y0, x1, y1, radius, fill):
    d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=radius * S, fill=fill)


def poly(d, pts, fill):
    d.polygon([(x * S, y * S) for x, y in pts], fill=fill)


def line(d, pts, fill, width):
    d.line([(x * S, y * S) for x, y in pts], fill=fill, width=max(1, int(width * S)))


def pie(d, box, start, end, fill):
    x0, y0, x1, y1 = box
    d.pieslice([x0 * S, y0 * S, x1 * S, y1 * S], start, end, fill=fill)


def arc(d, box, start, end, fill, width):
    x0, y0, x1, y1 = box
    d.arc([x0 * S, y0 * S, x1 * S, y1 * S], start, end, fill=fill, width=max(1, int(width * S)))


def eye(d, x, y, r=10):
    circle(d, x, y, r, WHITE)
    circle(d, x + r * 0.25, y + r * 0.1, r * 0.42, INK)


def blank():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def draw_apple(d):
    circle(d, 318, 268, 112, RED)
    ellipse(d, 268, 230, 26, 16, "#f47c72")
    poly(d, [(308, 170), (322, 132), (338, 146), (324, 178)], BROWN)
    poly(d, [(324, 168), (398, 132), (386, 168), (334, 188)], GREEN)


def draw_banana(d):
    outer = []
    inner = []
    for i in range(41):
        t = i / 40
        ang = math.radians(205 + t * 130)
        outer.append((300 + math.cos(ang) * 168, 300 + math.sin(ang) * 150))
        inner.append((300 + math.cos(ang) * 112, 300 + math.sin(ang) * 98))
    poly(d, outer + inner[::-1], YELLOW)
    a0 = math.radians(205)
    a1 = math.radians(335)
    circle(d, 300 + math.cos(a0) * 140, 300 + math.sin(a0) * 124, 16, BROWN)
    circle(d, 300 + math.cos(a1) * 140, 300 + math.sin(a1) * 124, 14, "#d7a441")


def draw_orange(d):
    circle(d, 320, 270, 112, ORANGE)
    ellipse(d, 274, 232, 24, 14, "#ffc15a")
    circle(d, 320, 348, 10, "#e08912")
    poly(d, [(314, 168), (330, 142), (340, 156), (326, 176)], GREEN_DARK)
    poly(d, [(328, 162), (386, 140), (372, 170), (334, 180)], GREEN)


def draw_grapes(d):
    spots = [
        (320, 168),
        (286, 206),
        (354, 206),
        (252, 248),
        (320, 248),
        (388, 248),
        (286, 292),
        (354, 292),
        (320, 334),
    ]
    for x, y in spots:
        circle(d, x, y, 32, PURPLE)
        circle(d, x - 8, y - 8, 8, "#9a80dc")
    line(d, [(320, 150), (320, 118)], BROWN, 8)
    poly(d, [(320, 124), (372, 96), (360, 132), (324, 142)], GREEN)


def draw_cat(d):
    ellipse(d, 330, 330, 78, 58, "#f4a25a")
    poly(d, [(392, 320), (470, 300), (430, 250), (400, 292)], "#f4a25a")
    circle(d, 300, 210, 78, "#f4a25a")
    poly(d, [(236, 176), (258, 78), (300, 156)], "#f4a25a")
    poly(d, [(300, 156), (342, 78), (364, 176)], "#f4a25a")
    poly(d, [(248, 164), (262, 104), (290, 152)], "#ffd0c4")
    poly(d, [(310, 152), (338, 104), (352, 164)], "#ffd0c4")
    eye(d, 274, 208, 11)
    eye(d, 328, 208, 11)
    poly(d, [(296, 228), (306, 228), (301, 238)], PINK)
    arc(d, (278, 228, 324, 262), 20, 160, INK, 4)
    line(d, [(214, 214), (262, 220)], INK, 3)
    line(d, [(214, 230), (262, 230)], INK, 3)
    line(d, [(338, 220), (386, 214)], INK, 3)
    line(d, [(338, 230), (386, 230)], INK, 3)


def draw_dog(d):
    ellipse(d, 318, 332, 86, 62, "#c4844a")
    ellipse(d, 250, 168, 28, 46, "#a86b34")
    ellipse(d, 390, 168, 28, 46, "#a86b34")
    circle(d, 320, 214, 80, "#d0975c")
    ellipse(d, 320, 252, 36, 26, "#f0d2b0")
    eye(d, 292, 200, 11)
    eye(d, 348, 200, 11)
    circle(d, 320, 236, 8, INK)
    arc(d, (300, 240, 340, 272), 10, 170, INK, 4)
    ellipse(d, 332, 268, 12, 8, "#ef6b6b")


def draw_bird(d):
    poly(d, [(168, 250), (230, 220), (230, 280)], BLUE)
    ellipse(d, 300, 270, 90, 62, BLUE)
    circle(d, 392, 214, 40, BLUE)
    poly(d, [(424, 206), (478, 214), (424, 230)], ORANGE)
    ellipse(d, 292, 250, 28, 18, "#7eb6ff")
    eye(d, 404, 206, 8)
    line(d, [(268, 328), (258, 372)], ORANGE, 6)
    line(d, [(330, 332), (340, 376)], ORANGE, 6)


def draw_fish(d):
    poly(d, [(188, 250), (250, 190), (250, 310)], ORANGE)
    ellipse(d, 360, 250, 120, 72, "#ff8a3d")
    poly(d, [(330, 190), (390, 150), (400, 206)], "#ffb067")
    poly(d, [(340, 300), (400, 340), (390, 286)], "#ffb067")
    eye(d, 430, 236, 12)
    arc(d, (400, 240, 450, 280), 20, 140, INK, 4)


def draw_sun(d):
    cx, cy, inner, outer = 320, 250, 78, 132
    for i in range(12):
        ang = math.radians(i * 30 - 90)
        line(
            d,
            [
                (cx + math.cos(ang) * inner, cy + math.sin(ang) * inner),
                (cx + math.cos(ang) * outer, cy + math.sin(ang) * outer),
            ],
            YELLOW,
            16,
        )
    circle(d, cx, cy, 86, YELLOW)
    circle(d, cx - 22, cy - 20, 16, "#ffe98a")


def draw_moon(d):
    circle(d, 300, 250, 108, "#f4d35e")
    circle(d, 356, 220, 92, WHITE)


def draw_star(d):
    pts = []
    for i in range(10):
        ang = math.radians(-90 + i * 36)
        radius = 120 if i % 2 == 0 else 50
        pts.append((320 + math.cos(ang) * radius, 255 + math.sin(ang) * radius))
    poly(d, pts, YELLOW)


def draw_tree(d):
    rrect(d, 292, 300, 348, 400, 8, BROWN)
    circle(d, 320, 250, 78, GREEN)
    circle(d, 250, 280, 58, GREEN_DARK)
    circle(d, 390, 280, 58, GREEN)
    circle(d, 320, 210, 48, "#67d18f")


def draw_flower(d):
    line(d, [(320, 250), (320, 400)], GREEN_DARK, 10)
    poly(d, [(320, 320), (250, 300), (320, 340)], GREEN)
    poly(d, [(320, 340), (390, 360), (320, 360)], GREEN)
    for i in range(6):
        ang = math.radians(i * 60 - 90)
        circle(d, 320 + math.cos(ang) * 48, 210 + math.sin(ang) * 48, 28, PINK)
    circle(d, 320, 210, 20, YELLOW)


def draw_book(d):
    poly(d, [(150, 170), (310, 210), (310, 360), (150, 330)], BLUE)
    poly(d, [(330, 210), (490, 170), (490, 330), (330, 360)], BLUE_DARK)
    poly(d, [(168, 188), (300, 222), (300, 342), (168, 314)], WHITE)
    poly(d, [(340, 222), (472, 188), (472, 314), (340, 342)], WHITE)
    rrect(d, 308, 206, 332, 364, 4, "#d7e6fb")
    for i, y in enumerate((240, 262, 284)):
        line(d, [(190, y), (280, y + 8)], "#c5d7ee", 4)
        line(d, [(360, y + 8), (450, y)], "#c5d7ee", 4)


def draw_pen(im):
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    rrect(d, 168, 214, 470, 286, 22, BLUE)
    rrect(d, 400, 206, 500, 294, 16, NAVY)
    poly(d, [(168, 226), (168, 274), (112, 250)], "#f3d2b6")
    rrect(d, 300, 214, 324, 286, 4, YELLOW)
    rotated = layer.rotate(-28, resample=Image.Resampling.BICUBIC, center=(310 * S, 250 * S))
    im.alpha_composite(rotated)


def draw_car(d):
    rrect(d, 150, 250, 510, 340, 36, BLUE)
    rrect(d, 230, 180, 410, 268, 28, BLUE)
    rrect(d, 248, 196, 392, 256, 14, "#d7ecff")
    line(d, [(320, 196), (320, 256)], "#d7ecff", 4)
    circle(d, 230, 340, 36, NAVY)
    circle(d, 430, 340, 36, NAVY)
    circle(d, 230, 340, 16, "#d5dde8")
    circle(d, 430, 340, 16, "#d5dde8")
    circle(d, 478, 286, 8, YELLOW)


def draw_bus(d):
    rrect(d, 120, 150, 530, 340, 28, "#f0b429")
    rrect(d, 148, 176, 500, 246, 10, "#d7ecff")
    for x in (170, 250, 330, 410):
        line(d, [(x, 176), (x, 246)], "#f0b429", 6)
    rrect(d, 168, 262, 230, 340, 8, "#8fd0ff")
    circle(d, 210, 348, 32, NAVY)
    circle(d, 450, 348, 32, NAVY)
    circle(d, 210, 348, 14, "#d5dde8")
    circle(d, 450, 348, 14, "#d5dde8")
    circle(d, 492, 286, 8, RED)


def draw_house(d):
    poly(d, [(140, 230), (320, 110), (500, 230)], RED)
    rrect(d, 176, 220, 464, 400, 8, CREAM)
    rrect(d, 286, 292, 354, 400, 8, BROWN)
    circle(d, 338, 348, 5, YELLOW)
    rrect(d, 210, 258, 268, 316, 6, "#9fd4ff")
    rrect(d, 372, 258, 430, 316, 6, "#9fd4ff")
    line(d, [(239, 258), (239, 316)], WHITE, 4)
    line(d, [(210, 287), (268, 287)], WHITE, 4)
    line(d, [(401, 258), (401, 316)], WHITE, 4)
    line(d, [(372, 287), (430, 287)], WHITE, 4)
    rrect(d, 392, 150, 430, 220, 4, BROWN)


def draw_ball(d):
    circle(d, 320, 255, 112, WHITE)
    pie(d, (208, 143, 432, 367), 250, 20, RED)
    pie(d, (208, 143, 432, 367), 70, 200, BLUE)
    pie(d, (208, 143, 432, 367), 200, 250, YELLOW)
    circle(d, 320, 255, 28, WHITE)


def draw_cup(d):
    rrect(d, 210, 160, 400, 360, 28, "#d7ecff")
    ellipse(d, 305, 168, 95, 24, "#b9dcff")
    ellipse(d, 305, 168, 72, 14, "#8d5a3c")
    arc(d, (360, 200, 470, 320), 280, 80, "#7eb6ff", 16)
    ellipse(d, 305, 352, 100, 18, "#c5dff8")


def draw_hat(d):
    ellipse(d, 320, 312, 168, 36, NAVY)
    pie(d, (210, 120, 430, 340), 180, 360, "#3d5a80")
    ellipse(d, 320, 228, 110, 22, RED)


def draw_clock(d):
    circle(d, 320, 250, 120, NAVY)
    circle(d, 320, 250, 102, WHITE)
    for i in range(12):
        ang = math.radians(i * 30 - 90)
        inner = 78 if i % 3 == 0 else 88
        line(
            d,
            [
                (320 + math.cos(ang) * inner, 250 + math.sin(ang) * inner),
                (320 + math.cos(ang) * 96, 250 + math.sin(ang) * 96),
            ],
            NAVY,
            6 if i % 3 == 0 else 3,
        )
    line(d, [(320, 250), (320, 180)], NAVY, 8)
    line(d, [(320, 250), (378, 270)], RED, 6)
    circle(d, 320, 250, 7, RED)


def draw_umbrella(d):
    pie(d, (150, 120, 490, 340), 180, 360, RED)
    pie(d, (150, 120, 320, 340), 180, 360, RED_DARK)
    line(d, [(320, 230), (206, 230)], WHITE, 4)
    line(d, [(320, 230), (434, 230)], WHITE, 4)
    line(d, [(320, 228), (320, 390)], NAVY, 8)
    arc(d, (320, 350, 400, 430), 0, 200, NAVY, 8)
    circle(d, 320, 228, 8, NAVY)


def draw_cake(d):
    ellipse(d, 320, 360, 150, 24, "#e7eef6")
    rrect(d, 180, 250, 460, 360, 18, "#f6c1d0")
    rrect(d, 180, 220, 460, 270, 16, WHITE)
    for x in (210, 250, 290, 330, 370, 410):
        circle(d, x, 268, 16, PINK)
    rrect(d, 300, 150, 312, 230, 3, YELLOW)
    rrect(d, 250, 170, 262, 230, 3, "#7ec8ff")
    rrect(d, 360, 165, 372, 230, 3, GREEN)
    circle(d, 306, 142, 10, ORANGE)
    circle(d, 256, 162, 10, RED)
    circle(d, 366, 156, 10, YELLOW)


DRAWINGS = [
    ("apple", draw_apple),
    ("banana", draw_banana),
    ("orange", draw_orange),
    ("grapes", draw_grapes),
    ("cat", draw_cat),
    ("dog", draw_dog),
    ("bird", draw_bird),
    ("fish", draw_fish),
    ("sun", draw_sun),
    ("moon", draw_moon),
    ("star", draw_star),
    ("tree", draw_tree),
    ("flower", draw_flower),
    ("book", draw_book),
    ("pen", draw_pen),
    ("car", draw_car),
    ("bus", draw_bus),
    ("house", draw_house),
    ("ball", draw_ball),
    ("cup", draw_cup),
    ("hat", draw_hat),
    ("clock", draw_clock),
    ("umbrella", draw_umbrella),
    ("cake", draw_cake),
]


def render(name, fn):
    im, draw = blank()
    if name == "pen":
        fn(im)
    else:
        fn(draw)
    flat = Image.new("RGB", (640, 480), WHITE)
    scaled = im.resize((640, 480), Image.Resampling.LANCZOS)
    flat.paste(scaled, mask=scaled.split()[-1])
    colors = flat.getcolors(maxcolors=640 * 480)
    painted = sum(count for count, color in colors if color != (255, 255, 255))
    if painted < 800:
        raise SystemExit(f"{name} looks blank ({painted} colored pixels)")
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}.webp"
    flat.save(path, "WEBP", quality=82, method=6)
    return path, path.stat().st_size


def main():
    total = 0
    for name, fn in DRAWINGS:
        path, size = render(name, fn)
        total += size
        print(f"{path.name:16} {size:6} bytes")
    print(f"{len(DRAWINGS)} images, {total} bytes")


if __name__ == "__main__":
    main()
