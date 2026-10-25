"""Original scenes for the 222-word picture bank.

Each function paints one image_hint. English answers are never drawn.
Calendar words use Traditional Chinese labels so the day or month is clear
without spelling the English lemma.
"""

import math

from drawlib import (
    BLUE,
    BLUE_DARK,
    BROWN,
    CREAM,
    GREEN,
    GREEN_DARK,
    GREY,
    HEAD,
    INK,
    NAVY,
    ORANGE,
    PINK,
    PURPLE,
    RED,
    SKIN,
    TEAL,
    WHITE,
    YELLOW,
    world,
)

SCENES = {}


def scene(num):
    def wrap(fn):
        if num in SCENES:
            raise ValueError("duplicate scene %s" % num)
        SCENES[num] = fn
        return fn

    return wrap


def face(d, mood, bg, hair_style="short", shirt=BLUE):
    d.rect(0, 0, 640, 480, bg)
    scale = 2.05
    feet = 250 + 214 * scale
    d.person(320, feet, scale, mood=mood, hair_style=hair_style, shirt=shirt)
    return world(320, feet, scale, HEAD)


def backpack(d, x, y, sc=1):
    d.rrect(x, y, 78 * sc, 88 * sc, 14, BLUE, INK, 4)
    d.path(
        f"M{n(x + 16 * sc)} {n(y + 10)} Q{n(x + 39 * sc)} {n(y - 36 * sc)} {n(x + 62 * sc)} {n(y + 10)}",
        stroke=INK, sw=5,
    )
    d.rect(x + 12 * sc, y + 22 * sc, 54 * sc, 16 * sc, YELLOW)


def n(value):
    return round(float(value), 1)


def music(d, x, y, sc=1):
    d.circle(x, y, 12 * sc, INK)
    d.circle(x + 36 * sc, y + 10 * sc, 12 * sc, INK)
    d.line([(x + 10 * sc, y - 4 * sc), (x + 10 * sc, y - 52 * sc)], INK, 5)
    d.line([(x + 46 * sc, y + 4 * sc), (x + 46 * sc, y - 40 * sc)], INK, 5)
    d.line([(x + 10 * sc, y - 52 * sc), (x + 46 * sc, y - 40 * sc)], INK, 5)


def palette(d, x, y, sc=1):
    d.ellipse(x, y, 54 * sc, 40 * sc, WHITE, INK, 4)
    d.circle(x + 10 * sc, y + 8 * sc, 12 * sc, "#f3f6fb", INK, 3)
    colors = (RED, YELLOW, BLUE, GREEN, ORANGE)
    for i, color in enumerate(colors):
        d.circle(x - 36 * sc + i * 18 * sc, y - 12 * sc, 8 * sc, color, INK, 2)


def ball(d, x, y, r=36, color=ORANGE):
    d.circle(x, y, r, color, INK, 4)
    d.path(f"M{n(x - r)} {n(y)} Q{n(x)} {n(y - r * 0.2)} {n(x + r)} {n(y)}", stroke=WHITE, sw=3)
    d.line([(x, y - r), (x, y + r)], WHITE, 3)


def weekday(d, index, icon):
    d.rect(0, 0, 640, 480, "#f4f8fc")
    d.calendar_base(70, 28, 500, 424)
    labels = ["一", "二", "三", "四", "五", "六", "日"]
    d.week_cells(92, 96, 456, active=index, marks=labels)
    names = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    d.zh(names[index], 320, 250, 54, BLUE_DARK)
    icon(d)


def month_card(d, name, icon, tint):
    d.rect(0, 0, 640, 480, tint)
    d.calendar_base(150, 24, 340, 150)
    d.zh(name, 320, 42, 32, WHITE)
    icon(d)


@scene(1)
def close_houses(d):
    d.outdoor()
    d.house(210, 400, 1)
    d.house(430, 400, 1)
    d.line([(300, 300), (340, 300)], RED, 6)
    d.line([(300, 292), (300, 308)], RED, 4)
    d.line([(340, 292), (340, 308)], RED, 4)


@scene(2)
def milk_glass(d):
    d.rect(0, 0, 640, 480, "#e7f3ff")
    d.glass_cup(250, 90, "#f7fbff", 140, 250)
    d.ellipse(320, 400, 80, 16, "rgba(36,48,68,0.12)")
    d.circle(300, 70, 10, WHITE, INK, 2)
    d.circle(340, 50, 8, WHITE, INK, 2)


@scene(3)
def jam_jar(d):
    d.rect(0, 0, 640, 480, "#fff4f0")
    d.jar(250, 110)
    d.circle(180, 280, 28, RED, INK, 3)
    d.circle(460, 300, 24, "#7dce6a", INK, 3)


@scene(4)
def black_swatch(d):
    d.rect(0, 0, 640, 480, "#eef2f6")
    d.rrect(170, 70, 300, 300, 28, "#1b1e26", INK, 6)
    for i, color in enumerate((RED, YELLOW, BLUE, GREEN, WHITE)):
        d.circle(120, 100 + i * 58, 18, color, INK, 3)


@scene(5)
def popcorn_bowl(d):
    d.rect(0, 0, 640, 480, "#fff8ea")
    d.bowl(180, 250, 280, 90, YELLOW)
    for x, y, r in (
        (250, 200, 22), (310, 170, 26), (370, 200, 22), (280, 140, 20),
        (350, 130, 18), (320, 210, 20), (400, 160, 16), (230, 160, 16),
    ):
        d.circle(x, y, r, "#fffdf6", INK, 3)


@scene(6)
def clear_glass(d):
    d.rect(0, 0, 640, 480, "#e5f6ff")
    d.circle(300, 250, 70, YELLOW, INK, 4)
    d.glass_cup(250, 110, "rgba(186,224,255,0.35)", 130, 230)
    d.sparkles([(430, 140, 10), (180, 180, 8), (470, 240, 6)])


@scene(7)
def soda_can(d):
    d.rect(0, 0, 640, 480, "#e7f7ff")
    d.can(270, 120)
    d.circle(180, 180, 14, "rgba(255,255,255,0.8)", "#9fd4ff", 2)
    d.circle(470, 220, 20, "rgba(255,255,255,0.8)", "#9fd4ff", 2)
    d.circle(160, 280, 10, "rgba(255,255,255,0.8)", "#9fd4ff", 2)


@scene(8)
def house_roof(d):
    d.outdoor()
    d.house(320, 400, 1.35)
    d.arrow(480, 120, 360, 200, RED, 8)


@scene(9)
def giving_up(d):
    d.outdoor(sky="#d5e4f2")
    d.person(300, 430, 1.15, mood="sad", pose="giveup", shirt=GREY)
    d.line([(430, 150), (430, 300)], "#d9dee6", 4)
    d.rect(400, 150, 70, 46, WHITE, INK, 3)
    d.rrect(150, 360, 70, 22, 8, "#8aa0b8", INK, 3)


@scene(10)
def floating_feather(d):
    d.rect(0, 0, 640, 480, "#eef8ff")
    d.path("M300 80 Q360 180 300 300 Q250 190 300 80 Z", fill=WHITE, stroke=INK, sw=4)
    d.line([(300, 90), (300, 290)], GREY, 3)
    d.circle(300, 400, 36, "#7d8b99", INK, 4)
    d.line([(180, 160), (240, 170)], "#9fd4ff", 4)
    d.line([(400, 140), (460, 150)], "#9fd4ff", 4)


@scene(11)
def gift_bow(d):
    d.rect(0, 0, 640, 480, "#fff4f8")
    d.gift(320, 280, 2.1)
    d.sparkles([(140, 120, 12), (500, 140, 10), (120, 300, 8), (520, 320, 8)])


@scene(12)
def sick_in_bed(d):
    d.indoor(wall="#e7eef6")
    d.bed(80, 390, 480, 150)
    d.person(300, 360, 0.85, mood="sad", pose="lie", shirt="#d7e4f5", pale=True)
    d.rrect(470, 180, 18, 90, 8, WHITE, INK, 3)
    d.rect(474, 210, 10, 40, RED)


@scene(13)
def slumped(d):
    d.outdoor(sky="#c9d7ea", ground="#b7c4b0")
    d.cloud(140, 90, 1.1, "#d5deea")
    d.person(330, 430, 1.2, mood="sad", pose="giveup", shirt="#7f8ea3")


@scene(14)
def empty_calendar(d):
    d.rect(0, 0, 640, 480, "#f4fbf8")
    d.calendar_base(70, 50, 340, 360)
    d.week_cells(90, 130, 300, active=2)
    d.person(520, 430, 0.7, mood="smile", pose="wave", shirt=TEAL)


@scene(15)
def empty_shelf(d):
    d.indoor(wall="#f6f1e8", floor="#e7d7c0")
    for y in (80, 180, 280):
        d.rect(80, y, 480, 16, BROWN, INK, 3)
    d.rrect(250, 200, 36, 28, 4, "#f0d2b0", INK, 2)


@scene(16)
def sunny_sky(d):
    d.outdoor(sky="#bfe9ff")
    d.sun(200, 140, 78, face=True)
    d.cloud(460, 110, 1.1)
    d.sparkles([(360, 80, 8), (100, 200, 6)])


@scene(17)
def nearby_arrow(d):
    d.outdoor()
    d.person(140, 420, 1, mood="smile", pose="point")
    d.tree(500, 400, 1.1)
    d.arrow(230, 250, 400, 250, RED, 8)


@scene(18)
def muddy_shoes(d):
    d.rect(0, 0, 640, 480, "#efe6d6")
    d.ellipse(230, 300, 90, 46, "#6b4a32", INK, 4)
    d.ellipse(400, 300, 90, 46, "#6b4a32", INK, 4)
    d.ellipse(210, 270, 50, 24, "#8a5a3b", INK, 3)
    d.ellipse(380, 270, 50, 24, "#8a5a3b", INK, 3)
    for x, y in ((140, 180), (180, 220), (480, 170), (500, 230), (300, 150)):
        d.circle(x, y, 8, "#6b4a32")


@scene(19)
def cracked_earth(d):
    d.rect(0, 0, 640, 480, "#e7c99a")
    d.path("M80 80 L200 160 L120 240 L220 320 L100 420", stroke="#a67c52", sw=5)
    d.path("M300 40 L260 160 L360 220 L280 340 L340 460", stroke="#a67c52", sw=5)
    d.path("M480 90 L420 200 L540 280 L460 400", stroke="#8a5a3b", sw=5)
    d.flower(500, 300, "#c9b48a", 0.5)


@scene(20)
def vivid_painting(d):
    d.indoor()
    d.line([(320, 300), (320, 420)], BROWN, 8)
    d.rrect(120, 60, 400, 250, 8, WHITE, INK, 5)
    d.circle(200, 150, 36, RED)
    d.rect(250, 120, 80, 110, YELLOW)
    d.poly([(360, 220), (420, 120), (480, 220)], BLUE)
    d.circle(300, 200, 20, GREEN)


@scene(21)
def empty_pockets(d):
    d.outdoor(sky="#efe8dc")
    d.person(320, 430, 1.2, mood="sad", shirt="#6b7c90", pants="#4a5568")
    d.poly([(250, 300), (230, 360), (280, 340)], WHITE, INK, 3)
    d.poly([(390, 300), (410, 360), (360, 340)], WHITE, INK, 3)


@scene(22)
def abc_blocks(d):
    d.rect(0, 0, 640, 480, "#fff8ea")
    colors = (RED, BLUE, GREEN)
    letters = "ABC"
    for i, letter in enumerate(letters):
        x = 90 + i * 170
        d.rrect(x, 160, 140, 140, 16, colors[i], INK, 5)
        d.glyph(letter, x + 70, 210, 72, WHITE)


@scene(23)
def mean_face(d):
    face(d, "angry", "#ffe4e0", shirt=RED)
    d.line([(180, 150), (250, 190)], INK, 6)
    d.line([(460, 150), (390, 190)], INK, 6)


@scene(24)
def iron_appliance(d):
    d.rect(0, 0, 640, 480, "#f4f7fb")
    d.path("M160 280 L200 180 L460 180 L500 280 Z", fill="#d5dde6", stroke=INK, sw=5)
    d.rrect(190, 150, 250, 40, 10, "#9aa8b8", INK, 4)
    d.circle(250, 250, 10, BLUE)
    d.ellipse(330, 310, 150, 18, "rgba(36,48,68,0.12)")


@scene(25)
def rice_bowl(d):
    d.rect(0, 0, 640, 480, "#fffaf2")
    d.bowl(170, 230, 300, 100, "#fffdf8")
    d.ellipse(320, 220, 110, 36, WHITE, INK, 3)
    d.line([(430, 120), (470, 250)], BROWN, 5)
    d.line([(450, 110), (500, 240)], BROWN, 5)


@scene(26)
def honeybee(d):
    d.rect(0, 0, 640, 480, "#fff6d2")
    d.bee(300, 230, 2.4)
    d.flower(80, 360, PINK, 1)
    d.flower(540, 380, ORANGE, 0.9)


@scene(27)
def church_building(d):
    d.outdoor()
    d.rrect(200, 180, 240, 200, 6, CREAM, INK, 4)
    d.poly([(180, 190), (320, 70), (460, 190)], "#c9ccd4", INK, 4)
    d.rect(300, 40, 40, 50, "#c9ccd4", INK, 3)
    d.line([(320, 16), (320, 50)], INK, 4)
    d.line([(306, 32), (334, 32)], INK, 4)
    d.path("M290 380 L290 250 Q320 210 350 250 L350 380", fill="#8eb6e0", stroke=INK, sw=3)
    d.rrect(292, 300, 56, 80, 4, BROWN, INK, 3)


@scene(28)
def crane_build(d):
    d.outdoor(sky="#d9ecff")
    d.rect(120, 160, 36, 240, YELLOW, INK, 4)
    d.rect(120, 150, 280, 18, YELLOW, INK, 4)
    d.line([(300, 168), (300, 230)], INK, 3)
    d.rrect(250, 230, 90, 70, 6, ORANGE, INK, 3)
    d.rrect(200, 250, 70, 50, 4, "#d9dee6", INK, 3)
    d.rrect(280, 310, 70, 50, 4, "#d9dee6", INK, 3)


@scene(29)
def continue_arrow(d):
    d.rect(0, 0, 640, 480, "#eef8ff")
    for i, x in enumerate((80, 140, 200)):
        d.circle(x, 240, 14, GREY, INK, 3)
    d.arrow(250, 240, 540, 240, GREEN, 12)


@scene(30)
def seedling_grow(d):
    d.outdoor()
    for i, h in enumerate((40, 80, 130)):
        x = 140 + i * 160
        d.rrect(x, 400 - h, 16, h, 6, GREEN_DARK)
        d.ellipse(x - 16, 400 - h, 22, 12, GREEN, INK, 3)
        d.ellipse(x + 22, 392 - h, 22, 12, GREEN, INK, 3)
    d.arrow(500, 300, 500, 140, GREEN_DARK, 8)


@scene(31)
def know_bulb(d):
    d.outdoor()
    d.person(300, 430, 1.15, mood="think", pose="think", shirt=BLUE)
    d.bulb(460, 150, 1.5, on=True)


@scene(32)
def handshake(d):
    d.outdoor()
    d.person(200, 430, 1.05, mood="smile", shirt=BLUE, pose="hug")
    d.person(440, 430, 1.05, mood="smile", shirt=ORANGE, pose="hug", flip=True)
    d.ellipse(320, 300, 28, 16, SKIN, INK, 3)


@scene(33)
def puzzle_match(d):
    d.rect(0, 0, 640, 480, "#f4f7fb")
    d.rrect(120, 140, 160, 160, 16, BLUE, INK, 4)
    d.circle(280, 220, 28, "#f4f7fb")
    d.rrect(300, 180, 160, 160, 16, GREEN, INK, 4)
    d.circle(300, 260, 28, GREEN)
    d.check(320, 360, 1.4)


@scene(34)
def elderly(d):
    d.outdoor()
    d.person(300, 430, 1.15, mood="smile", hair_style="grey", shirt="#7f8ea3", pants=BROWN)
    d.glasses(300, 430, 1.15)
    d.cane(300, 430, 1.15)


@scene(35)
def bouquet(d):
    d.rect(0, 0, 640, 480, "#fff5f8")
    d.path("M250 460 L300 220 L390 460 Z", fill="#c9854a", stroke=INK, sw=4)
    for i, color in enumerate((PINK, RED, YELLOW, PURPLE, WHITE, ORANGE)):
        d.flower(180 + (i % 3) * 90, 150 + (i // 3) * 70, color, 0.7)


@scene(36)
def cheetah_run(d):
    d.outdoor(sky="#fff4d8", ground="#e7c98a", horizon=340)
    d.speed_lines(60, 180)
    d.speed_lines(40, 230)
    d.cheetah(340, 300, 1.35)


@scene(37)
def small_kitten(d):
    d.indoor(wall="#fff6ee")
    d.kitten(300, 300, 1.8)
    d.ellipse(420, 360, 40, 16, "#f0d8c4")


@scene(38)
def calm_lake(d):
    d.outdoor(sky="#cfeaff", ground="#7dce6a", horizon=250)
    d.ellipse(320, 360, 280, 90, "#4aa3e8", INK, 4)
    d.ellipse(250, 340, 80, 16, "rgba(255,255,255,0.55)")
    d.sun(110, 90, 36, face=True)
    d.tree(80, 270, 0.7)
    d.tree(540, 280, 0.8)


@scene(39)
def flowing_river(d):
    d.outdoor()
    d.path("M-20 80 C120 140 80 220 200 260 C340 310 260 380 420 420 C520 450 600 400 680 460 L680 200 C520 180 480 300 320 240 C180 180 160 80 -20 40 Z", fill="#4aa3e8", stroke=INK, sw=4)
    d.tree(80, 360, 0.8)
    d.tree(540, 200, 0.6)


@scene(40)
def welcome_door(d):
    d.outdoor()
    d.door(250, 400, 180, 250, open_=True)
    d.person(140, 420, 0.9, mood="smile", pose="wave", shirt=TEAL)
    d.heart(470, 180, 18)


@scene(41)
def thought_bubble(d):
    d.outdoor()
    d.person(240, 430, 1.1, mood="think", pose="think")
    d.ellipse(460, 140, 90, 54, WHITE, INK, 4)
    d.circle(390, 200, 12, WHITE, INK, 3)
    d.circle(360, 230, 7, WHITE, INK, 3)
    d.circle(430, 130, 6, GREY)
    d.circle(460, 130, 6, GREY)
    d.circle(490, 130, 6, GREY)


@scene(42)
def large_elephant(d):
    d.outdoor()
    d.elephant(300, 390, 1.15)
    d.person(80, 420, 0.45, mood="wow", shirt=RED)


@scene(43)
def headline_news(d):
    d.indoor(wall="#f7f5f2")
    d.rrect(80, 40, 480, 360, 8, WHITE, INK, 5)
    d.rect(100, 60, 440, 70, "#1b1e26")
    d.glyph("!", 320, 78, 48, YELLOW)
    for i, w in enumerate((400, 360, 420, 300, 380)):
        d.rect(110, 160 + i * 28, w, 12, GREY)
    d.star(430, 250, 28)


@scene(44)
def mountain_view(d):
    d.rect(0, 0, 640, 480, "#bfe9ff")
    d.sun(500, 90, 40, face=True)
    d.poly([(0, 420), (140, 180), (260, 420)], "#7ea0c4", INK, 4)
    d.poly([(160, 420), (340, 120), (520, 420)], "#5e7fa8", INK, 4)
    d.poly([(300, 180), (360, 140), (390, 190)], WHITE)
    d.ellipse(320, 430, 340, 50, "#7dce6a")
    d.ellipse(200, 400, 160, 30, "#4aa3e8")


@scene(45)
def silent_reading(d):
    d.indoor(wall="#f6f3ee")
    d.person(300, 400, 1.15, mood="shut", pose="read", shirt="#6b8f71")
    d.book(300, 230, 1.1)
    d.circle(470, 150, 28, WHITE, INK, 3)
    d.line([(458, 138), (482, 162)], INK, 4)
    d.line([(482, 138), (458, 162)], INK, 4)


@scene(46)
def reading_aloud(d):
    d.indoor(wall="#2c3e50", floor="#6b5344")
    d.person(250, 390, 1.05, mood="happy", pose="read", shirt=RED)
    d.book(250, 210, 1)
    d.circle(430, 160, 16, "#f6c7a1", INK, 3)
    d.circle(490, 180, 16, "#f6c7a1", INK, 3)
    d.circle(450, 230, 16, "#f6c7a1", INK, 3)
    d.path("M360 150 Q390 130 400 160", stroke=YELLOW, sw=4)


@scene(47)
def holding_keys(d):
    d.outdoor()
    d.person(240, 430, 1.1, mood="smile", pose="carry")
    d.house(470, 250, 0.55)
    d.circle(250, 210, 16, YELLOW, INK, 3)
    d.rect(262, 204, 28, 8, YELLOW, INK, 2)


@scene(48)
def permission_sign(d):
    d.outdoor()
    d.rect(300, 120, 16, 260, BROWN)
    d.rrect(150, 80, 200, 160, 16, WHITE, INK, 5)
    d.circle(250, 160, 48, "#e5f8ee", GREEN, 6)
    d.check(250, 160, 1.3)
    d.person(500, 420, 0.75, mood="smile", pose="wave", shirt=GREEN)


@scene(49)
def faith_heart(d):
    d.rect(0, 0, 640, 480, "#fff6ea")
    d.person(300, 450, 1.2, mood="shut", pose="think", shirt="#f0d2b0")
    d.heart(460, 140, 36, PINK)
    d.sparkles([(400, 80, 8), (520, 100, 8)])


@scene(50)
def magician_reveal(d):
    d.rect(0, 0, 640, 480, "#2c3e50")
    d.path("M220 300 L250 160 L390 160 L420 300 Z", fill="#1b1e26", stroke=INK, sw=4)
    d.ellipse(320, 160, 90, 22, "#3a322c", INK, 3)
    d.circle(320, 110, 28, WHITE, INK, 3)
    d.circle(310, 104, 4, INK)
    d.circle(328, 104, 4, INK)
    d.poly([(300, 120), (340, 120), (330, 140)], PINK)
    d.sparkles([(160, 80, 10), (480, 90, 12), (140, 200, 8)], YELLOW)


@scene(51)
def fragile_glass(d):
    d.indoor()
    d.person(220, 420, 1, mood="wow", pose="carry", shirt=BLUE)
    d.glass_cup(360, 150, "rgba(186,224,255,0.45)", 80, 140)
    d.sparkles([(470, 140, 8), (350, 130, 6)])
    d.line([(430, 200), (450, 230)], "#9fd4ff", 3)


@scene(52)
def magnifier_inspect(d):
    d.indoor(wall="#f7fbff")
    d.person(200, 420, 1, mood="think", shirt=TEAL)
    d.circle(420, 220, 70, "rgba(186,224,255,0.35)", INK, 8)
    d.line([(470, 270), (530, 340)], BROWN, 10)
    d.flower(420, 220, PINK, 0.45)


@scene(53)
def hard_puzzle(d):
    d.rect(0, 0, 640, 480, "#f4f7fb")
    d.rrect(80, 80, 150, 150, 12, BLUE, INK, 4)
    d.rrect(250, 200, 150, 150, 12, ORANGE, INK, 4)
    d.rrect(400, 80, 140, 140, 12, GREEN, INK, 4)
    d.path("M200 160 Q280 40 400 120", stroke=RED, sw=6)
    d.glyph("?", 320, 40, 48, RED)


@scene(54)
def blue_rain(d):
    d.rect(0, 0, 640, 480, "#6ea0d8")
    d.cloud(200, 90, 1.4, "#d5e4f5")
    d.rain(140, 130, 8)
    d.person(400, 430, 1.05, mood="sad", shirt="#2f6fe0")


@scene(55)
def depressed(d):
    d.rect(0, 0, 640, 480, "#d5dbe3")
    d.person(320, 460, 1.15, mood="cry", pose="sit", shirt="#7f8ea3")
    d.cloud(460, 120, 0.8, "#b7c4d4")
    d.rain(430, 150, 3)


@scene(56)
def world_flags(d):
    d.rect(0, 0, 640, 480, "#e7f4ff")
    d.circle(320, 250, 120, "#4aa3e8", INK, 5)
    d.ellipse(320, 250, 50, 120, GREEN, INK, 3)
    d.ellipse(320, 250, 120, 40, "none", GREEN_DARK, 3)
    d.rect(80, 80, 70, 46, RED, INK, 3)
    d.rect(490, 90, 70, 46, BLUE, INK, 3)
    d.rect(70, 320, 70, 46, YELLOW, INK, 3)
    d.rect(500, 330, 70, 46, GREEN, INK, 3)


@scene(57)
def countryside(d):
    d.outdoor()
    d.rrect(80, 200, 200, 160, 6, RED, INK, 4)
    d.poly([(60, 210), (180, 110), (300, 210)], "#f4f1ea", INK, 4)
    d.rect(150, 250, 50, 70, WHITE, INK, 3)
    d.line([(40, 360), (600, 360)], BROWN, 4)
    for x in range(40, 600, 40):
        d.line([(x, 360), (x, 400)], BROWN, 4)
    d.sheep(480, 400, 0.7)


@scene(58)
def bus_driver(d):
    d.rect(0, 0, 640, 480, "#d7f0ff")
    d.rrect(40, 80, 560, 300, 30, "#f5d76e", INK, 5)
    d.rrect(70, 110, 160, 120, 12, "#9fd4ff", INK, 4)
    d.circle(110, 340, 36, "#2c3e50", INK, 4)
    d.circle(500, 340, 36, "#2c3e50", INK, 4)
    d.circle(230, 180, 28, SKIN, INK, 3)
    d.circle(150, 190, 36, "#d9dee6", INK, 4)


@scene(59)
def aiming(d):
    d.outdoor()
    d.person(180, 420, 1.05, mood="think", pose="point", shirt=NAVY)
    d.circle(480, 220, 70, WHITE, INK, 4)
    d.circle(480, 220, 46, RED, INK, 3)
    d.circle(480, 220, 22, YELLOW, INK, 3)
    d.circle(480, 220, 8, INK)
    d.arrow(250, 240, 430, 220, BROWN, 6)


@scene(60)
def proof_stamp(d):
    d.rect(0, 0, 640, 480, "#f7f5f2")
    d.rrect(140, 60, 360, 360, 12, WHITE, INK, 5)
    for i, w in enumerate((280, 250, 300, 180)):
        d.rect(170, 100 + i * 36, w, 14, GREY)
    d.circle(400, 280, 60, "none", RED, 8)
    d.check(400, 280, 1.2, RED)


@scene(61)
def wild_hair(d):
    face(d, "silly", "#fff6d8", hair_style="wild", shirt=ORANGE)
    d.circle(250, 300, 10, YELLOW)
    d.circle(400, 280, 8, PINK)


@scene(62)
def angry_red(d):
    face(d, "angry", "#ffd0cc", shirt=RED)
    d.path("M150 80 Q170 40 190 80", stroke="#d9dee6", sw=6)
    d.path("M450 70 Q480 30 500 80", stroke="#d9dee6", sw=6)


@scene(63)
def clown_face(d):
    hx, hy = face(d, "silly", "#fff0f6", hair_style="wild", shirt="#ff8fab")
    d.circle(hx, hy + 28, 18, RED, INK, 3)


@scene(64)
def ham_slice(d):
    d.rect(0, 0, 640, 480, "#fff6f2")
    d.plate(320, 300, 280)
    d.ellipse(320, 250, 110, 70, "#f2a3b0", INK, 4)
    d.ellipse(360, 240, 28, 22, "#f7d7c4", INK, 3)


@scene(65)
def inch_ruler(d):
    d.rect(0, 0, 640, 480, "#f7f5f2")
    d.rrect(70, 200, 500, 80, 8, "#f0d7a2", INK, 4)
    for i in range(11):
        h = 40 if i % 5 == 0 else 22
        d.line([(100 + i * 44, 210), (100 + i * 44, 210 + h)], INK, 3)
    d.line([(100, 170), (144, 170)], RED, 6)
    d.line([(100, 160), (100, 180)], RED, 4)
    d.line([(144, 160), (144, 180)], RED, 4)
    d.glyph("1", 122, 120, 36, RED)


@scene(66)
def bathtub(d):
    d.indoor(wall="#e7f6fb", floor="#d5e4ea")
    d.ellipse(320, 300, 200, 80, WHITE, INK, 5)
    d.ellipse(320, 280, 160, 40, "#9fd4ff", INK, 3)
    d.circle(250, 230, 36, SKIN, INK, 4)
    d.circle(236, 224, 4, INK)
    d.circle(262, 224, 4, INK)
    d.path("M236 242 Q250 252 264 242", stroke=INK, sw=3)
    d.circle(430, 180, 10, "#9fd4ff")


@scene(67)
def digging(d):
    d.outdoor(ground="#c4a574")
    d.person(220, 400, 1, mood="think", pose="push", shirt=GREEN)
    d.line([(340, 160), (420, 340)], "#c0c7d0", 8)
    d.poly([(400, 330), (470, 350), (430, 390)], "#d9dee6", INK, 4)
    d.ellipse(430, 400, 70, 20, "#8a5a3b")


@scene(68)
def doctor_exam(d):
    d.indoor(wall="#f7fbff")
    d.person(240, 420, 1.05, mood="smile", shirt=WHITE)
    d.circle(250, 250, 16, "#d9dee6", INK, 3)
    d.line([(250, 266), (250, 300)], "#d9dee6", 4)
    d.circle(430, 200, 54, "rgba(186,224,255,0.4)", INK, 6)
    d.line([(470, 240), (520, 290)], NAVY, 8)


@scene(69)
def hot_sun(d):
    d.rect(0, 0, 640, 480, "#ffe8c2")
    d.sun(250, 180, 80, face=True)
    for i in range(4):
        d.path(f"M{n(430)} {n(120 + i * 40)} Q{n(470)} {n(140 + i * 40)} {n(430)} {n(160 + i * 40)}", stroke=RED, sw=5)
    d.rrect(470, 200, 24, 120, 10, WHITE, INK, 3)
    d.rect(476, 230, 12, 70, RED)


@scene(70)
def supporting_friend(d):
    d.outdoor()
    d.person(230, 420, 1.05, mood="smile", pose="hug", shirt=BLUE)
    d.person(390, 420, 1.05, mood="sad", shirt=ORANGE)
    d.heart(320, 140, 22)


@scene(71)
def pushing_door(d):
    d.indoor()
    d.door(340, 400, 200, 280, open_=False)
    d.person(200, 420, 1.05, mood="angry", pose="push", shirt=RED)
    d.line([(300, 200), (340, 200)], "#9aa8b8", 4)
    d.line([(300, 240), (340, 240)], "#9aa8b8", 4)


@scene(72)
def welcome_mat(d):
    d.outdoor()
    d.door(230, 300, 180, 220, open_=False)
    d.rrect(200, 330, 240, 70, 10, "#c9854a", INK, 4)
    d.heart(320, 360, 16, RED)
    d.person(80, 420, 0.55, mood="smile", pose="wave")


@scene(73)
def helping(d):
    d.outdoor()
    d.person(200, 420, 1, mood="sad", shirt=GREY)
    d.person(400, 420, 1, mood="smile", pose="hug", shirt=GREEN)
    d.rrect(300, 250, 40, 16, 6, WHITE, INK, 2)
    d.heart(470, 160, 16)


@scene(74)
def shark_ocean(d):
    d.rect(0, 0, 640, 140, "#bfe9ff")
    d.rect(0, 140, 640, 340, "#2f7fbe")
    d.path("M0 140 Q80 120 160 140 T320 140 T480 140 T640 140 L640 160 L0 160 Z", fill="#4aa3e8")
    d.shark(340, 300, 1.3)
    for x, y, r in ((80, 220, 8), (140, 280, 6), (500, 200, 7), (560, 320, 5)):
        d.circle(x, y, r, "rgba(255,255,255,0.7)")


@scene(75)
def fluffy_sheep(d):
    d.outdoor()
    d.sheep(300, 340, 1.8)
    d.cloud(100, 80, 0.7)


@scene(76)
def tiger_stand(d):
    d.outdoor(ground="#d7e8c4")
    d.tiger(320, 360, 1.5)
    d.tree(80, 380, 0.7)


@scene(77)
def wedding_couple(d):
    d.rect(0, 0, 640, 480, "#fff5f8")
    d.person(250, 430, 1.1, mood="smile", hair_style="long", shirt=WHITE)
    d.person(400, 430, 1.05, mood="smile", shirt=NAVY)
    d.path("M210 150 Q250 90 290 150", stroke=WHITE, sw=8)
    d.heart(320, 80, 18)


@scene(78)
def actor_stage(d):
    d.rect(0, 0, 640, 480, "#2c3e50")
    d.ellipse(320, 80, 80, 30, "rgba(255,211,77,0.35)")
    d.rect(40, 360, 560, 40, BROWN)
    d.person(320, 420, 1.15, mood="happy", shirt=RED, hair_style="short")
    d.rrect(250, 120, 140, 16, 6, YELLOW, INK, 3)


@scene(79)
def actress_stage(d):
    d.rect(0, 0, 640, 480, "#3a2a44")
    d.ellipse(320, 70, 90, 28, "rgba(255,143,171,0.45)")
    d.rect(40, 360, 560, 40, BROWN)
    d.person(320, 420, 1.15, mood="smile", shirt=PINK, hair_style="long")
    d.flower(430, 200, PINK, 0.6)


@scene(80)
def parking_sign(d):
    d.outdoor()
    d.rect(180, 80, 18, 280, GREY, INK, 3)
    d.rrect(120, 70, 150, 150, 12, BLUE, INK, 5)
    d.glyph("P", 195, 120, 72, WHITE)
    d.rrect(340, 230, 180, 80, 16, RED, INK, 4)
    d.circle(380, 330, 22, "#2c3e50")
    d.circle(480, 330, 22, "#2c3e50")


@scene(81)
def blowing_wind(d):
    d.outdoor(sky="#e7f4ff")
    for y in (80, 130, 180):
        d.line([(40, y), (180, y - 10)], "#9fd4ff", 6)
    d.ellipse(300, 160, 28, 14, GREEN, INK, 3)
    d.ellipse(380, 120, 24, 12, ORANGE, INK, 3)
    d.ellipse(460, 170, 20, 10, YELLOW, INK, 3)
    d.path("M250 220 Q300 160 340 230 Q380 180 430 240", stroke=BROWN, sw=4)


@scene(82)
def carrying_box(d):
    d.outdoor()
    d.person(320, 430, 1.15, mood="smile", pose="carry", shirt=ORANGE)
    d.rrect(250, 120, 140, 110, 10, "#e0b44a", INK, 4)
    d.line([(250, 175), (390, 175)], BROWN, 3)
    d.line([(320, 120), (320, 230)], BROWN, 3)


@scene(83)
def pleasant_scene(d):
    d.outdoor()
    d.sun(100, 80, 36, face=True)
    d.person(220, 400, 0.85, mood="happy", shirt=YELLOW)
    d.person(400, 400, 0.85, mood="smile", shirt=PINK, hair_style="long")
    d.flower(120, 360, PINK, 0.6)
    d.flower(520, 370, RED, 0.6)


@scene(84)
def tall_tower(d):
    d.outdoor(sky="#d7ecff")
    d.rrect(250, 40, 120, 340, 8, "#d9dee6", INK, 4)
    for y in range(70, 340, 36):
        d.rect(270, y, 28, 18, "#9fd4ff", INK, 2)
        d.rect(322, y, 28, 18, "#9fd4ff", INK, 2)
    d.person(120, 420, 0.55, mood="wow")


@scene(85)
def wide_road(d):
    d.rect(0, 0, 640, 200, "#bfe9ff")
    d.poly([(0, 200), (640, 200), (520, 480), (120, 480)], "#6b7280", INK, 4)
    d.line([(300, 230), (320, 460)], YELLOW, 8)
    d.arrow(80, 300, 200, 300, WHITE, 6)
    d.arrow(560, 300, 440, 300, WHITE, 6)


@scene(86)
def yellow_banana(d):
    d.rect(0, 0, 640, 480, "#fff8e8")
    d.banana(320, 250, 1.5)


@scene(87)
def ant_insect(d):
    d.rect(0, 0, 640, 480, "#f6f3ee")
    d.ant(320, 250, 2.4)


@scene(88)
def bat_animal(d):
    d.night()
    d.circle(500, 80, 28, "#f4f1ea")
    d.bat(300, 240, 1.8)


@scene(89)
def filling_cup(d):
    d.rect(0, 0, 640, 480, "#e7f6ff")
    d.glass_cup(280, 160, "#9fd4ff", 120, 200)
    d.path("M250 40 Q300 80 310 150", stroke="#4aa3e8", sw=10)
    d.arrow(430, 260, 430, 180, BLUE, 8)


@scene(90)
def wedding_rings(d):
    d.rect(0, 0, 640, 480, "#fff6ea")
    d.ellipse(250, 250, 70, 70, "none", "#e0b44a", 14)
    d.ellipse(370, 250, 70, 70, "none", "#f0d78c", 14)
    d.sparkles([(180, 140, 8), (480, 160, 8)])


@scene(91)
def forgetting(d):
    d.outdoor()
    d.person(260, 430, 1.1, mood="think", pose="think")
    d.ellipse(470, 150, 80, 48, WHITE, INK, 4)
    d.glyph("?", 470, 130, 36, GREY)
    d.circle(400, 210, 10, WHITE, INK, 2)


@scene(92)
def string_finger(d):
    d.rect(0, 0, 640, 480, "#fff8f2")
    d.rrect(250, 180, 70, 160, 30, SKIN, INK, 5)
    d.circle(285, 160, 28, SKIN, INK, 4)
    d.path("M300 150 Q360 120 340 190 Q320 160 300 170", stroke=RED, sw=5)


@scene(93)
def clover(d):
    d.rect(0, 0, 640, 480, "#e9f8ea")
    for ang in (0, 90, 180, 270):
        rad = math.radians(ang)
        d.circle(320 + math.cos(rad) * 48, 200 + math.sin(rad) * 48, 42, GREEN, INK, 4)
    d.circle(320, 200, 16, GREEN_DARK)
    d.line([(320, 250), (320, 400)], GREEN_DARK, 6)
    d.sparkles([(180, 120, 8), (470, 140, 8)])


@scene(94)
def cooked_chicken(d):
    d.rect(0, 0, 640, 480, "#fff6ee")
    d.plate(320, 320, 260)
    d.ellipse(320, 250, 110, 60, "#e0a85a", INK, 4)
    d.ellipse(230, 230, 36, 22, "#e0a85a", INK, 3)
    d.ellipse(410, 230, 28, 18, "#e0a85a", INK, 3)


@scene(95)
def fruit_pie(d):
    d.rect(0, 0, 640, 480, "#fff8f2")
    d.ellipse(320, 280, 150, 70, "#e0b44a", INK, 5)
    d.ellipse(320, 250, 130, 50, "#d64545", INK, 4)
    d.line([(230, 240), (410, 240)], "#f0d7a2", 4)
    d.line([(320, 200), (320, 290)], "#f0d7a2", 4)
    d.circle(280, 230, 8, RED)
    d.circle(360, 240, 8, RED)


@scene(96)
def speech_bubble(d):
    d.outdoor()
    d.person(220, 430, 1.05, mood="happy")
    d.rrect(340, 70, 220, 130, 24, WHITE, INK, 4)
    d.poly([(380, 190), (340, 240), (420, 190)], WHITE, INK, 4)
    d.line([(390, 120), (500, 120)], GREY, 6)
    d.line([(390, 150), (470, 150)], GREY, 6)


@scene(97)
def taking_object(d):
    d.indoor()
    d.rrect(300, 250, 220, 24, 6, BROWN)
    d.circle(420, 210, 28, RED, INK, 4)
    d.path("M80 280 C160 200 220 180 300 200", fill=SKIN, stroke=INK, sw=16)
    d.arrow(180, 120, 300, 180, BLUE, 6)


@scene(98)
def plus_blocks(d):
    d.rect(0, 0, 640, 480, "#f4f8ff")
    d.rrect(70, 150, 140, 140, 16, BLUE, INK, 4)
    d.glyph("2", 140, 200, 64, WHITE)
    d.glyph("+", 280, 200, 64, INK)
    d.rrect(360, 150, 140, 140, 16, GREEN, INK, 4)
    d.glyph("3", 430, 200, 64, WHITE)


@scene(99)
def growing_bars(d):
    d.rect(0, 0, 640, 480, "#f7fbff")
    d.line([(80, 80), (80, 400), (560, 400)], INK, 4)
    heights = (80, 150, 230, 300)
    colors = ("#b7d4f5", "#7eb6ef", "#4c8dff", "#2f6fe0")
    for i, (h, color) in enumerate(zip(heights, colors)):
        d.rrect(140 + i * 90, 400 - h, 60, h, 8, color, INK, 3)
    d.arrow(500, 300, 540, 140, GREEN, 8)


@scene(100)
def asking_question(d):
    d.outdoor()
    d.person(240, 430, 1.1, mood="think", pose="wave")
    d.circle(460, 150, 54, WHITE, INK, 4)
    d.glyph("?", 460, 125, 56, BLUE)


@scene(101)
def requesting_help(d):
    d.outdoor()
    d.person(180, 430, 1, mood="sad", pose="giveup", shirt=GREY)
    d.person(460, 430, 1, mood="smile", shirt=GREEN)
    d.heart(320, 160, 20)
    d.arrow(260, 250, 380, 250, PINK, 6)


@scene(102)
def booking_stamp(d):
    d.rect(0, 0, 640, 480, "#f4fbf8")
    d.calendar_base(80, 60, 320, 340)
    d.week_cells(100, 140, 280, active=4)
    d.circle(470, 250, 60, "none", RED, 8)
    d.poly([(440, 250), (470, 280), (510, 220)], "none", RED, 6)


@scene(103)
def bringing_gift(d):
    d.outdoor()
    d.person(180, 420, 1, mood="smile", pose="carry", shirt=ORANGE)
    d.gift(250, 180, 0.8)
    d.person(500, 420, 0.9, mood="happy", pose="wave", shirt=PINK, flip=True)
    d.arrow(300, 250, 420, 250, BLUE, 6)


@scene(104)
def checklist(d):
    d.rect(0, 0, 640, 480, "#f7fbff")
    d.rrect(140, 40, 360, 400, 16, WHITE, INK, 5)
    for i in range(5):
        y = 100 + i * 60
        d.rrect(180, y, 36, 36, 6, WHITE, INK, 3)
        d.check(198, y + 18, 0.7)
        d.rect(240, y + 10, 200, 12, GREY)


@scene(105)
def doing_chores(d):
    d.indoor()
    d.person(200, 400, 1, mood="smile", pose="push", shirt=TEAL)
    d.rrect(360, 180, 160, 120, 12, "#d9dee6", INK, 4)
    d.ellipse(440, 230, 50, 16, "#9fd4ff")
    d.circle(400, 210, 16, YELLOW, INK, 3)


@scene(106)
def starting_line(d):
    d.outdoor(ground="#6b7280", horizon=300)
    d.line([(80, 300), (80, 460)], WHITE, 8)
    d.person(180, 430, 1, mood="think", pose="run", shirt=RED)
    d.circle(500, 120, 28, "#3cb371", INK, 4)
    d.circle(500, 180, 28, "#f5a524", INK, 4)


@scene(107)
def hogging_toys(d):
    d.indoor(wall="#fff6ee")
    d.person(250, 400, 1.05, mood="angry", pose="hug", shirt=RED)
    d.circle(180, 250, 22, BLUE, INK, 3)
    d.circle(250, 230, 18, YELLOW, INK, 3)
    d.rrect(300, 240, 40, 40, 6, GREEN, INK, 3)
    d.person(500, 420, 0.7, mood="sad", shirt=GREY)


@scene(108)
def dunce_cap(d):
    hx, hy = face(d, "silly", "#fff8ea", shirt=ORANGE)
    d.poly([(hx - 50, hy - 70), (hx, hy - 160), (hx + 50, hy - 70)], "#f0d78c", INK, 4)
    d.glyph("?", hx + 90, hy - 20, 42, BLUE)


@scene(109)
def policeman(d):
    d.outdoor()
    d.person(320, 430, 1.2, mood="smile", shirt="#2f6fe0", pants=NAVY)
    hx, hy = world(320, 430, 1.2, HEAD)
    d.ellipse(hx, hy - 40, 48, 16, "#1d3f86", INK, 3)
    d.rrect(hx - 8, hy - 70, 16, 30, 4, "#1d3f86", INK, 3)
    d.star(hx, hy + 70, 14, YELLOW)


@scene(110)
def attention_sign(d):
    d.rect(0, 0, 640, 480, "#fff8ea")
    d.poly([(320, 40), (560, 400), (80, 400)], YELLOW, INK, 6)
    d.glyph("!", 320, 200, 96, INK)
    d.person(110, 450, 0.45, mood="wow")


@scene(111)
def missed_bus(d):
    d.outdoor()
    d.rrect(300, 140, 280, 140, 16, "#f5d76e", INK, 4)
    d.circle(360, 290, 24, NAVY)
    d.circle(520, 290, 24, NAVY)
    d.arrow(360, 120, 500, 120, RED, 6)
    d.person(120, 420, 0.9, mood="sad", pose="run", shirt=BLUE)


@scene(112)
def rubbing_hands(d):
    d.rect(0, 0, 640, 480, "#fff6ee")
    d.ellipse(250, 250, 70, 46, SKIN, INK, 4)
    d.ellipse(370, 250, 70, 46, SKIN, INK, 4)
    d.path("M180 180 Q220 140 250 180", stroke="#9aa8b8", sw=4)
    d.path("M430 170 Q470 140 490 190", stroke="#9aa8b8", sw=4)


@scene(113)
def wilted_flower(d):
    d.rect(0, 0, 640, 480, "#f4f1ea")
    d.path("M300 420 L320 180", stroke="#8a7a62", sw=6)
    d.circle(300, 160, 28, "#b7a48a", INK, 3)
    d.circle(340, 180, 24, "#a89078", INK, 3)
    d.circle(280, 190, 22, "#c4b49a", INK, 3)
    d.path("M250 360 Q300 390 360 350", stroke="#6b7c50", sw=4)


@scene(114)
def thumbs_up(d):
    d.rect(0, 0, 640, 480, "#e9f8ee")
    d.thumb(320, 180, up=True, sc=2.2)
    d.sparkles([(160, 120, 10), (480, 140, 10)])


@scene(115)
def good_enough(d):
    d.rect(0, 0, 640, 480, "#f4fbf6")
    d.rrect(80, 160, 360, 40, 12, "#e5f0ea", INK, 4)
    d.rect(80, 160, 250, 40, "#b7e6c8")
    d.line([(330, 140), (330, 220)], GREEN_DARK, 4)
    d.thumb(500, 200, up=True, sc=1.1)


@scene(116)
def giant_whale(d):
    d.rect(0, 0, 640, 160, "#bfe9ff")
    d.rect(0, 160, 640, 320, "#2f7fbe")
    d.whale(300, 300, 1.15)
    d.path("M470 150 L520 190 L480 190 Z", fill=WHITE, stroke=INK, sw=3)


@scene(117)
def priority_star(d):
    d.rect(0, 0, 640, 480, "#fff8ea")
    d.star(320, 220, 120, YELLOW)
    d.glyph("!", 320, 190, 72, RED)


@scene(118)
def four_seasons(d):
    d.rect(0, 0, 640, 480, "#f7fbff")
    colors = ("#f7c1d4", GREEN, ORANGE, "#d5dde6")
    for i, color in enumerate(colors):
        x = 80 + i * 140
        d.rrect(x + 28, 250, 16, 120, 4, BROWN)
        d.circle(x + 36, 220, 40, color, INK, 3)
    d.snowflake(500, 150, 8)


@scene(119)
def storybook(d):
    d.rect(0, 0, 640, 480, "#fff8ee")
    d.book(320, 120, 2.2)
    d.circle(230, 200, 16, YELLOW, INK, 2)
    d.circle(400, 210, 18, GREEN, INK, 2)
    d.star(250, 250, 12)


@scene(120)
def wearing_coat(d):
    d.outdoor(sky="#d5e4f2")
    d.person(320, 430, 1.2, mood="smile", shirt="#3a6ea5")
    d.rrect(250, 200, 140, 150, 20, "#2f5580", INK, 4)
    d.circle(250, 230, 22, SKIN, INK, 3)


@scene(121)
def laying_book(d):
    d.indoor()
    d.rrect(160, 250, 360, 28, 6, BROWN)
    d.book(340, 160, 1.2, open_=False)
    d.path("M120 200 C180 160 240 180 300 190", fill=SKIN, stroke=INK, sw=14)


@scene(122)
def lying_down(d):
    d.indoor(wall="#e7eef8")
    d.bed(60, 360, 520, 140)
    with d.g("translate(340 300) rotate(-75)"):
        d.person(0, 0, 0.75, mood="shut", pose="lie", shirt="#9eb6e0")


@scene(123)
def caterpillar_butterfly(d):
    d.outdoor()
    d.ellipse(150, 250, 70, 28, GREEN, INK, 4)
    d.circle(210, 240, 16, GREEN, INK, 3)
    d.circle(200, 234, 3, INK)
    d.arrow(250, 240, 360, 240, ORANGE, 8)
    d.ellipse(470, 200, 36, 22, "#7eb6ef", INK, 3)
    d.ellipse(520, 230, 30, 18, PINK, INK, 3)
    d.ellipse(430, 230, 28, 16, YELLOW, INK, 3)
    d.circle(490, 240, 10, "#3a322c", INK, 2)


@scene(124)
def changing_weather(d):
    d.rect(0, 0, 640, 480, "#e7f2fb")
    d.sun(150, 180, 50, face=True)
    d.arrow(250, 220, 380, 220, GREY, 8)
    d.cloud(500, 180, 1.3, "#d5dde6")
    d.rain(460, 230, 4)


@scene(125)
def trophy(d):
    d.rect(0, 0, 640, 480, "#fff8ea")
    d.path("M220 120 H420 V230 Q320 320 220 230 Z", fill="#f0d78c", stroke=INK, sw=5)
    d.ellipse(190, 170, 30, 40, "none", "#f0d78c", 8)
    d.ellipse(450, 170, 30, 40, "none", "#f0d78c", 8)
    d.rect(300, 300, 40, 50, "#e0b44a", INK, 3)
    d.rrect(250, 350, 140, 28, 6, BROWN, INK, 3)
    d.glyph("1", 320, 160, 64, RED)


@scene(126)
def sharp_knife(d):
    d.rect(0, 0, 640, 480, "#f7f5f2")
    d.rrect(80, 220, 280, 28, 6, "#d9dee6", INK, 4)
    d.rrect(340, 200, 120, 60, 10, BROWN, INK, 4)
    d.ellipse(200, 300, 40, 18, ORANGE, INK, 3)
    d.ellipse(250, 320, 36, 16, ORANGE)
    d.sparkles([(180, 160, 8), (260, 150, 6)])


@scene(127)
def round_ball(d):
    d.rect(0, 0, 640, 480, "#f4f8ff")
    ball(d, 320, 240, 100, ORANGE)
    d.path("M320 80 A160 160 0 0 1 480 240", stroke=BLUE, sw=6)
    d.arrow(470, 210, 500, 250, BLUE, 6)


@scene(128)
def yummy_cake(d):
    d.rect(0, 0, 640, 480, "#fff5f8")
    d.rrect(170, 200, 300, 140, 16, PINK, INK, 4)
    d.rrect(170, 180, 300, 40, 10, WHITE, INK, 3)
    d.circle(400, 230, 28, "#f4f7fb")
    d.rect(300, 140, 8, 50, YELLOW)
    d.circle(304, 130, 10, RED)
    d.heart(140, 120, 16)


@scene(129)
def lifting(d):
    d.outdoor()
    d.person(320, 430, 1.15, mood="smile", pose="carry", shirt=GREEN)
    d.rrect(250, 90, 140, 90, 10, BROWN, INK, 4)
    d.check(480, 160, 1.2)


@scene(130)
def giving_gift(d):
    d.outdoor()
    d.person(200, 420, 1, mood="smile", pose="carry", shirt=BLUE)
    d.gift(300, 200, 0.9)
    d.person(480, 420, 0.95, mood="happy", pose="wave", shirt=PINK, hair_style="long", flip=True)


@scene(131)
def providing_tray(d):
    d.indoor(wall="#fff8f2")
    d.person(200, 420, 1.05, mood="smile", shirt=WHITE)
    d.ellipse(340, 230, 80, 16, "#d9dee6", INK, 3)
    d.circle(310, 200, 16, "#f2a3b0", INK, 2)
    d.glass_cup(350, 140, "#9fd4ff", 36, 70)
    d.person(500, 420, 0.8, mood="smile", shirt=BLUE, flip=True)


@scene(132)
def cuddling(d):
    d.rect(0, 0, 640, 480, "#fff5f8")
    d.person(280, 430, 1.15, mood="smile", hair_style="long", shirt=PINK)
    d.circle(400, 250, 28, SKIN, INK, 3)
    d.rrect(370, 280, 50, 60, 16, YELLOW, INK, 3)
    d.heart(160, 140, 20)
    d.heart(480, 120, 14)


@scene(133)
def laughing(d):
    face(d, "happy", "#fff8ea", shirt=YELLOW)


@scene(134)
def soft_pillow(d):
    d.rect(0, 0, 640, 480, "#f7f3ff")
    d.ellipse(320, 260, 180, 90, "#d7c4f5", INK, 5)
    d.ellipse(300, 240, 40, 16, "rgba(255,255,255,0.7)")
    d.path("M160 180 C200 140 240 200 200 230", fill=SKIN, stroke=INK, sw=12)


@scene(135)
def writer_desk(d):
    d.indoor(wall="#f6f3ee")
    d.rrect(120, 250, 400, 28, 6, BROWN)
    d.person(300, 400, 1, mood="think", pose="read", shirt="#6b8f71")
    d.rrect(360, 180, 90, 70, 4, WHITE, INK, 3)
    d.line([(430, 160), (470, 230)], YELLOW, 6)


@scene(136)
def zoo_gate(d):
    d.outdoor()
    d.rect(80, 80, 24, 280, BROWN, INK, 3)
    d.rect(520, 80, 24, 280, BROWN, INK, 3)
    d.path("M80 80 Q320 10 544 80", stroke=GREEN, sw=16)
    d.elephant(180, 300, 0.4)
    d.circle(460, 200, 30, YELLOW, INK, 3)
    d.person(320, 420, 0.6, mood="wow")


@scene(137)
def town_street(d):
    d.outdoor(horizon=320)
    for i, color in enumerate((RED, BLUE, GREEN, ORANGE)):
        d.house(90 + i * 150, 360, 0.55, roof=color)
    d.rect(40, 360, 560, 16, "#6b7280")


@scene(138)
def annoying_bug(d):
    d.outdoor()
    d.person(300, 430, 1.15, mood="angry", shirt=BLUE)
    d.bee(460, 180, 0.8)
    d.path("M420 160 Q400 120 440 100", stroke="#9aa8b8", sw=3)
    d.path("M480 150 Q510 110 490 90", stroke="#9aa8b8", sw=3)


@scene(139)
def rising_chart(d):
    d.rect(0, 0, 640, 480, "#f7fbff")
    d.line([(80, 60), (80, 400), (560, 400)], INK, 4)
    d.path("M120 340 L200 300 L280 310 L360 200 L460 120", stroke=GREEN, sw=8)
    for x, y in ((120, 340), (200, 300), (280, 310), (360, 200), (460, 120)):
        d.circle(x, y, 8, GREEN, INK, 3)
    d.arrow(480, 140, 520, 80, GREEN, 8)


@scene(140)
def dying_plant(d):
    d.indoor()
    d.path("M240 360 L280 300 L360 360 Z", fill="#c9854a", stroke=INK, sw=4)
    d.path("M300 300 Q340 220 300 160", stroke="#8a7a62", sw=6)
    d.ellipse(330, 170, 30, 14, "#b7a48a", INK, 3)
    d.ellipse(250, 240, 22, 10, "#a89078")


@scene(141)
def tiny_ant(d):
    d.rect(0, 0, 640, 480, "#f7f5f2")
    d.circle(250, 250, 90, "#e0b44a", INK, 5)
    d.circle(250, 250, 70, "#f0d78c", INK, 3)
    d.ant(470, 260, 0.7)


@scene(142)
def multitool(d):
    d.rect(0, 0, 640, 480, "#f4f7fb")
    d.rrect(270, 180, 100, 36, 8, RED, INK, 4)
    d.poly([(200, 198), (270, 186), (270, 210)], "#d9dee6", INK, 3)
    d.line([(370, 198), (470, 120)], "#d9dee6", 8)
    d.line([(370, 198), (480, 230)], BROWN, 6)
    d.circle(470, 250, 16, "none", INK, 4)


@scene(143)
def shy_child(d):
    d.indoor(wall="#fff5f8")
    d.rect(360, 40, 40, 400, "#e7d3b0", INK, 3)
    d.person(300, 430, 1, mood="shy", hair_style="long", shirt=PINK)
    d.circle(250, 200, 16, PINK, opacity=0.7)


@scene(144)
def graduation(d):
    d.outdoor()
    d.person(320, 430, 1.15, mood="smile", shirt=NAVY)
    hx, hy = world(320, 430, 1.15, HEAD)
    d.poly([(hx - 50, hy - 30), (hx, hy - 55), (hx + 50, hy - 30), (hx, hy - 10)], "#1b1e26", INK, 3)
    d.line([(hx + 40, hy - 30), (hx + 55, hy)], YELLOW, 3)
    d.bulb(480, 140, 0.8)


@scene(145)
def strange_door(d):
    d.rect(0, 0, 640, 480, "#e7e4f5")
    d.path("M220 420 L200 80 Q320 20 450 100 L430 420 Z", fill="#6b5b95", stroke=INK, sw=5)
    d.circle(330, 200, 28, YELLOW, INK, 4)
    d.circle(322, 194, 5, INK)
    d.circle(340, 194, 5, INK)
    d.glyph("?", 480, 80, 48, PURPLE)


@scene(146)
def calendar_week(d):
    d.rect(0, 0, 640, 480, "#f4f8fc")
    d.calendar_base(40, 80, 560, 250)
    d.week_cells(60, 160, 520, marks=["一", "二", "三", "四", "五", "六", "日"])
    d.path("M70 430 Q320 300 570 430", stroke=BLUE, sw=6)
    d.zh("一星期", 320, 40, 36, BLUE_DARK)


@scene(147)
def weekend_days(d):
    d.rect(0, 0, 640, 480, "#fff8ea")
    d.calendar_base(40, 70, 560, 230)
    d.week_cells(60, 150, 520, marks=["一", "二", "三", "四", "五", "六", "日"])
    d.rrect(430, 150, 150, 64, 8, "#ffe08a", ORANGE, 4)
    ball(d, 200, 390, 40, ORANGE)
    d.sun(460, 390, 36, face=True)


@scene(148)
def calendar_year(d):
    d.rect(0, 0, 640, 480, "#f7fbff")
    d.zh("一年", 320, 24, 40, BLUE_DARK)
    for i in range(12):
        x = 40 + (i % 4) * 150
        y = 110 + (i // 4) * 110
        d.rrect(x, y, 130, 90, 8, WHITE, INK, 3)
        d.glyph(str(i + 1), x + 65, y + 24, 28, BLUE)


@scene(149)
def small_pond(d):
    d.outdoor()
    d.ellipse(320, 320, 180, 70, "#3aa0a8", INK, 4)
    d.ellipse(280, 310, 30, 12, GREEN, INK, 3)
    d.circle(400, 330, 16, GREEN, INK, 3)
    d.circle(390, 324, 3, INK)
    d.flower(120, 360, PINK, 0.6)


@scene(150)
def swimming_pool(d):
    d.rect(0, 0, 640, 480, "#e7f6ff")
    d.rrect(80, 80, 480, 300, 20, "#4aa3e8", INK, 5)
    for x in (180, 300, 420):
        d.line([(x, 90), (x, 370)], WHITE, 3)
    d.line([(100, 200), (140, 140)], "#d9dee6", 6)


@scene(151)
def tangled_knot(d):
    d.rect(0, 0, 640, 480, "#fff8ee")
    d.path("M120 160 C220 40 200 300 320 180 C440 60 400 360 520 200", stroke=ORANGE, sw=16)
    d.path("M160 300 C260 420 380 80 460 320", stroke=BLUE, sw=12)
    d.glyph("?", 320, 40, 42, RED)


@scene(152)
def tree_rings(d):
    d.rect(0, 0, 640, 480, "#f6f1e8")
    for i, r in enumerate((150, 120, 90, 60, 30)):
        d.circle(320, 250, r, "none", BROWN if i % 2 == 0 else "#e0b44a", 8)
    d.circle(320, 250, 8, BROWN)


@scene(153)
def mirage(d):
    d.rect(0, 0, 640, 480, "#f6e2b8")
    d.rect(0, 300, 640, 180, "#e7c98a")
    d.tree(180, 300, 0.8, "#2e9a5c")
    d.tree(420, 300, 0.8, "#2e9a5c")
    d.path("M80 250 Q200 230 320 250 T560 250", stroke="rgba(255,255,255,0.8)", sw=6)
    d.tree(420, 250, 0.5, "rgba(46,154,92,0.35)")


@scene(154)
def sudden_burst(d):
    d.rect(0, 0, 640, 480, "#fff8ea")
    d.star(320, 230, 90, YELLOW)
    for ang in range(0, 360, 30):
        rad = math.radians(ang)
        d.line([
            (320 + math.cos(rad) * 110, 230 + math.sin(rad) * 110),
            (320 + math.cos(rad) * 170, 230 + math.sin(rad) * 170),
        ], ORANGE, 6)
    d.glyph("!", 320, 200, 48, RED)


@scene(155)
def closed_door(d):
    d.indoor()
    d.door(220, 420, 200, 300, open_=False)
    d.line([(250, 160), (390, 160)], "#e0a56a", 3)


@scene(156)
def storage_shelves(d):
    d.indoor(wall="#f6f1e8")
    for y in (60, 180, 300):
        d.rect(70, y, 500, 18, BROWN, INK, 3)
        for i in range(4):
            d.rrect(100 + i * 120, y - 50, 70, 50, 6, [BLUE, GREEN, ORANGE, RED][i], INK, 3)


@scene(157)
def certain_check(d):
    d.rect(0, 0, 640, 480, "#e9f8ee")
    d.circle(320, 230, 120, WHITE, GREEN, 10)
    d.check(320, 230, 3, GREEN)


@scene(158)
def overlapping_circles(d):
    d.rect(0, 0, 640, 480, "#f4f8ff")
    d.circle(250, 240, 120, "rgba(76,141,255,0.45)", BLUE, 5)
    d.circle(390, 240, 120, "rgba(60,179,113,0.45)", GREEN, 5)
    d.heart(320, 240, 18, RED)


@scene(159)
def finish_flag(d):
    d.outdoor()
    d.rect(420, 80, 12, 300, INK)
    d.rrect(200, 80, 220, 120, 8, WHITE, INK, 4)
    for i in range(4):
        for j in range(3):
            if (i + j) % 2 == 0:
                d.rect(210 + i * 50, 90 + j * 34, 50, 34, INK)
    d.person(160, 420, 0.8, mood="happy", pose="run", shirt=RED)


@scene(160)
def important_key(d):
    d.rect(0, 0, 640, 480, "#fff8ea")
    d.circle(220, 200, 60, "#f0d78c", INK, 5)
    d.circle(220, 200, 24, "#fff8ea", INK, 4)
    d.rect(270, 184, 180, 28, "#f0d78c", INK, 4)
    d.rect(400, 212, 20, 36, "#f0d78c", INK, 3)
    d.rect(440, 212, 20, 24, "#f0d78c", INK, 3)
    d.star(500, 120, 24)


@scene(161)
def nodding_sure(d):
    d.outdoor()
    d.person(300, 430, 1.2, mood="confident", shirt=GREEN)
    d.check(480, 150, 1.6)
    d.arrow(430, 220, 400, 180, GREEN, 6)


@scene(162)
def hammer_wrench(d):
    d.rect(0, 0, 640, 480, "#f4f7fb")
    d.rect(140, 180, 180, 28, BROWN, INK, 4)
    d.rrect(300, 150, 80, 90, 8, "#9aa8b8", INK, 4)
    d.path("M160 320 Q240 250 340 340", stroke="#7f8ea3", sw=14)
    d.circle(340, 340, 22, "none", INK, 6)


@scene(163)
def unit_blocks(d):
    d.rect(0, 0, 640, 480, "#f7fbff")
    for i in range(4):
        d.rrect(80 + i * 130, 180, 100, 100, 10, [BLUE, GREEN, ORANGE, PURPLE][i], INK, 4)
    d.line([(80, 150), (180, 150)], RED, 5)
    d.line([(80, 140), (80, 160)], RED, 4)
    d.line([(180, 140), (180, 160)], RED, 4)
    d.glyph("1", 130, 90, 32, RED)


@scene(164)
def voice_waves(d):
    d.rect(0, 0, 640, 480, "#f7fbff")
    d.ellipse(200, 250, 70, 40, SKIN, INK, 4)
    d.path("M160 250 Q200 300 240 250", stroke=RED, sw=6)
    for i, rx in enumerate((40, 70, 100)):
        d.path(
            f"M{n(280)} {n(250 - rx)} A{n(rx)} {n(rx)} 0 0 1 {n(280)} {n(250 + rx)}",
            stroke=BLUE, sw=6,
        )


@scene(165)
def running_action(d):
    d.outdoor()
    d.person(300, 420, 1.2, mood="happy", pose="run", shirt=RED)
    d.speed_lines(40, 200)
    d.speed_lines(60, 250)


@scene(166)
def tied_knot(d):
    d.rect(0, 0, 640, 480, "#fff8ee")
    d.path("M80 240 C180 80 180 400 320 240 C460 80 460 400 560 240", stroke=BROWN, sw=16)
    d.circle(320, 240, 28, "none", BROWN, 10)


@scene(167)
def improvement(d):
    d.rect(0, 0, 640, 480, "#f4fbf6")
    d.flower(160, 300, "#b7a48a", 0.7)
    d.arrow(250, 260, 390, 200, GREEN, 10)
    d.flower(500, 280, PINK, 1.1)


@scene(168)
def broom_clear(d):
    d.indoor()
    d.line([(180, 80), (260, 320)], BROWN, 8)
    d.poly([(230, 300), (320, 300), (300, 380), (210, 370)], "#e0b44a", INK, 4)
    d.ellipse(430, 360, 70, 24, "#c4b49a")
    d.circle(400, 340, 10, "#a89078")
    d.circle(450, 350, 12, "#a89078")
    d.arrow(360, 200, 430, 280, GREY, 5)


@scene(169)
def thumbs_down(d):
    d.rect(0, 0, 640, 480, "#ffefef")
    d.thumb(320, 140, up=False, sc=2.2)


@scene(170)
def different_shapes(d):
    d.rect(0, 0, 640, 480, "#f7fbff")
    d.circle(180, 240, 80, BLUE, INK, 5)
    d.poly([(400, 120), (520, 360), (280, 360)], ORANGE, INK, 5)
    d.line([(300, 80), (340, 40)], RED, 6)
    d.line([(300, 40), (340, 80)], RED, 6)


def _weekday_icon_bag(d):
    backpack(d, 280, 300, 1.3)


def _weekday_icon_music(d):
    music(d, 280, 360, 1.4)


def _weekday_icon_palette(d):
    palette(d, 320, 360, 1.3)


def _weekday_icon_book(d):
    d.book(320, 300, 1.4, open_=False)


def _weekday_icon_star(d):
    d.star(320, 360, 48)


def _weekday_icon_ball(d):
    ball(d, 320, 360, 48, ORANGE)


def _weekday_icon_sun(d):
    d.sun(320, 350, 48, face=True)


@scene(171)
def monday(d):
    weekday(d, 0, _weekday_icon_bag)


@scene(172)
def tuesday(d):
    weekday(d, 1, _weekday_icon_music)


@scene(173)
def wednesday(d):
    weekday(d, 2, _weekday_icon_palette)


@scene(174)
def thursday(d):
    weekday(d, 3, _weekday_icon_book)


@scene(175)
def friday(d):
    weekday(d, 4, _weekday_icon_star)


@scene(176)
def saturday(d):
    weekday(d, 5, _weekday_icon_ball)


@scene(177)
def sunday(d):
    weekday(d, 6, _weekday_icon_sun)


@scene(178)
def one_month(d):
    d.rect(0, 0, 640, 480, "#f7fbff")
    d.calendar_base(70, 30, 500, 420)
    d.zh("月", 320, 90, 36, WHITE)
    for r in range(5):
        for c in range(7):
            d.rrect(100 + c * 64, 180 + r * 48, 48, 36, 6, "#f4f7fb", INK, 2)


def _month(name, tint, icon):
    def paint(d):
        month_card(d, name, icon, tint)
    return paint


def _snow(d):
    d.circle(320, 300, 50, WHITE, INK, 4)
    d.circle(280, 340, 36, WHITE, INK, 4)
    d.circle(370, 345, 30, WHITE, INK, 4)
    d.snowflake(180, 250, 10)
    d.snowflake(480, 240, 12)


def _hearts(d):
    d.heart(320, 300, 50, RED)
    d.heart(200, 250, 20, PINK)
    d.heart(450, 260, 18, PINK)


def _wind(d):
    for i, y in enumerate((240, 290, 340)):
        d.path(f"M120 {y} Q240 {y - 30} 360 {y} T540 {y}", stroke=BLUE, sw=6)


def _april_rain(d):
    d.cloud(320, 240, 1.6, "#d5e4f5")
    d.rain(240, 280, 6)
    d.umbrella(320, 340, 0.8)


def _may_flowers(d):
    for i, color in enumerate((PINK, RED, YELLOW, PURPLE, WHITE)):
        d.flower(120 + i * 100, 340, color, 0.8)


def _june_sun(d):
    d.sun(320, 320, 70, face=True)


def _july_fire(d):
    d.star(220, 280, 30, RED)
    d.star(320, 240, 40, YELLOW)
    d.star(430, 300, 28, BLUE)
    d.line([(320, 300), (320, 400)], BROWN, 3)


def _august_beach(d):
    d.ellipse(320, 360, 200, 40, "#f0d78c")
    d.umbrella(250, 300, 0.7)
    d.sun(480, 250, 36, face=True)


def _sept_leaves(d):
    for i, color in enumerate((ORANGE, RED, YELLOW, BROWN)):
        d.ellipse(160 + i * 110, 300, 36, 20, color, INK, 3)


def _oct_pumpkin(d):
    d.ellipse(320, 320, 90, 70, ORANGE, INK, 5)
    d.rect(306, 240, 28, 24, GREEN_DARK, INK, 3)
    d.line([(290, 300), (350, 300)], "#d64545", 3)
    d.line([(290, 330), (350, 330)], "#d64545", 3)


def _nov_bird(d):
    d.ellipse(320, 320, 90, 60, BROWN, INK, 4)
    d.circle(400, 280, 28, BROWN, INK, 3)
    d.poly([(420, 280), (460, 290), (420, 300)], ORANGE, INK, 3)
    d.ellipse(250, 300, 40, 16, "#8a5a3b", INK, 3)


def _dec_tree(d):
    d.pine(320, 400, 1.3)
    d.circle(300, 250, 8, RED)
    d.circle(340, 290, 8, YELLOW)
    d.circle(310, 330, 8, BLUE)


SCENES[179] = _month("一月", "#e7f4ff", _snow)
SCENES[180] = _month("二月", "#fff0f4", _hearts)
SCENES[181] = _month("三月", "#e7f6ff", _wind)
SCENES[182] = _month("四月", "#e7f2fb", _april_rain)
SCENES[183] = _month("五月", "#f4fbf4", _may_flowers)
SCENES[184] = _month("六月", "#fff8ea", _june_sun)
SCENES[185] = _month("七月", "#2c3e50", _july_fire)
SCENES[186] = _month("八月", "#fff4d8", _august_beach)
SCENES[187] = _month("九月", "#fff1e4", _sept_leaves)
SCENES[188] = _month("十月", "#fff4e8", _oct_pumpkin)
SCENES[189] = _month("十一月", "#f6f1e8", _nov_bird)
SCENES[190] = _month("十二月", "#e9f6ee", _dec_tree)


@scene(191)
def ironing_shirt(d):
    d.indoor()
    d.path("M120 280 L200 230 L480 230 L520 280 Z", fill="#d9dee6", stroke=INK, sw=4)
    d.line([(300, 280), (300, 400)], GREY, 8)
    d.rrect(180, 200, 200, 40, 8, "#7eb6ef", INK, 3)
    d.path("M300 160 L340 120 L460 150 L420 200 Z", fill="#c5ced8", stroke=INK, sw=4)


@scene(192)
def joining_group(d):
    d.outdoor()
    for i, x in enumerate((180, 280, 380)):
        d.person(x, 400, 0.7, mood="smile", shirt=BLUE)
    d.person(520, 420, 0.75, mood="happy", pose="run", shirt=ORANGE)
    d.arrow(450, 250, 400, 250, GREEN, 6)


@scene(193)
def making_craft(d):
    d.indoor(wall="#fff8f2")
    d.rrect(160, 250, 320, 24, 6, BROWN)
    d.rrect(220, 160, 90, 80, 6, PINK, INK, 3)
    d.rrect(330, 170, 80, 70, 6, YELLOW, INK, 3)
    d.path("M140 220 C200 160 240 200 280 190", fill=SKIN, stroke=INK, sw=12)
    d.line([(430, 140), (480, 210)], "#d9dee6", 6)


@scene(194)
def planting(d):
    d.outdoor(ground="#8a5a3b", horizon=300)
    d.person(180, 400, 0.95, mood="smile", pose="push", shirt=GREEN)
    d.ellipse(420, 340, 70, 24, "#6b4a32")
    d.rrect(412, 250, 12, 90, 4, GREEN_DARK)
    d.ellipse(400, 250, 22, 12, GREEN, INK, 3)
    d.ellipse(436, 246, 22, 12, GREEN, INK, 3)


@scene(195)
def reaching(d):
    d.outdoor()
    d.person(180, 430, 1, mood="smile", pose="point", shirt=BLUE)
    d.star(500, 180, 36)
    d.arrow(280, 220, 450, 190, ORANGE, 6)


@scene(196)
def crying_face(d):
    face(d, "cry", "#e7f2fb", shirt=BLUE)


@scene(197)
def flexing(d):
    d.rect(0, 0, 640, 480, "#fff4ea")
    d.person(300, 450, 1.3, mood="confident", pose="flex", shirt=RED)
    d.circle(180, 200, 28, SKIN, INK, 4)
    d.sparkles([(140, 140, 8), (480, 150, 8)])


@scene(198)
def apology_bow(d):
    d.indoor()
    with d.g("translate(320 430) rotate(18)"):
        d.person(0, 0, 1.15, mood="sad", pose="bow", shirt=BLUE)
    d.heart(140, 120, 18, PINK)


@scene(199)
def short_and_tall(d):
    d.outdoor()
    d.person(180, 430, 0.65, mood="smile", shirt=ORANGE)
    d.person(420, 430, 1.25, mood="smile", shirt=BLUE)
    d.line([(120, 200), (120, 430)], GREY, 3)
    d.line([(110, 280), (130, 280)], RED, 4)


@scene(200)
def empty_gauge(d):
    d.rect(0, 0, 640, 480, "#f7f5f2")
    d.path("M120 340 A200 200 0 0 1 520 340", stroke=GREY, sw=18)
    d.path("M120 340 A200 200 0 0 1 200 180", stroke=RED, sw=18)
    d.line([(320, 340), (180, 200)], INK, 8)
    d.circle(320, 340, 16, NAVY)
    d.glyph("0", 150, 300, 28, RED)


@scene(201)
def eagle_bird(d):
    d.rect(0, 0, 640, 480, "#d7f0ff")
    d.cloud(100, 80, 0.8)
    d.eagle(320, 250, 1.5)
    d.sun(520, 80, 30)


@scene(202)
def fact_document(d):
    d.rect(0, 0, 640, 480, "#f7fbff")
    d.rrect(160, 50, 320, 380, 12, WHITE, INK, 5)
    for i, w in enumerate((240, 200, 220, 180)):
        d.rect(200, 110 + i * 40, w, 14, GREY)
    d.circle(320, 320, 40, "none", BLUE, 6)
    d.check(320, 320, 1)


@scene(203)
def farmer(d):
    d.outdoor()
    d.person(300, 430, 1.15, mood="smile", shirt="#2e9a5c", pants=BROWN)
    hx, hy = world(300, 430, 1.15, HEAD)
    d.ellipse(hx, hy - 36, 60, 16, "#f0d78c", INK, 3)
    d.line([(430, 160), (470, 360)], BROWN, 6)
    d.line([(450, 170), (510, 190)], "#c0c7d0", 6)


@scene(204)
def piggy_bank(d):
    d.rect(0, 0, 640, 480, "#fff0f4")
    d.ellipse(320, 260, 140, 90, PINK, INK, 5)
    d.circle(430, 230, 28, PINK, INK, 4)
    d.circle(440, 224, 4, INK)
    d.ellipse(250, 250, 20, 14, PINK, INK, 3)
    d.rect(300, 180, 40, 10, INK)
    d.circle(200, 140, 22, "#f0d78c", INK, 3)
    d.arrow(210, 160, 280, 200, ORANGE, 5)


@scene(205)
def sending_envelope(d):
    d.rect(0, 0, 640, 480, "#f4f8ff")
    d.rrect(180, 160, 240, 160, 8, WHITE, INK, 5)
    d.poly([(180, 160), (300, 250), (420, 160)], "none", INK, 4)
    d.arrow(460, 240, 580, 160, BLUE, 8)


@scene(206)
def teaching(d):
    d.indoor(wall="#f7fbff")
    d.rrect(60, 60, 250, 180, 8, "#2c3e50", INK, 4)
    d.circle(140, 130, 24, WHITE)
    d.poly([(200, 160), (250, 90), (280, 170)], YELLOW)
    d.person(430, 400, 0.9, mood="smile", pose="point", shirt=TEAL)
    d.circle(200, 360, 22, SKIN, INK, 3)
    d.circle(280, 380, 22, SKIN, INK, 3)


@scene(207)
def understanding(d):
    d.rect(0, 0, 640, 480, "#fffbea")
    d.bulb(300, 180, 2.4, on=True)
    d.check(300, 175, 1.2, GREEN_DARK)
    d.person(480, 450, 0.7, mood="wow", pose="wave")


@scene(208)
def open_gate(d):
    d.outdoor()
    d.rect(80, 120, 18, 260, BROWN, INK, 3)
    d.rect(200, 120, 18, 260, BROWN, INK, 3)
    d.rrect(200, 150, 120, 180, 6, "#c9854a", INK, 4)
    d.person(430, 420, 0.9, mood="smile", pose="run", shirt=GREEN)
    d.arrow(300, 80, 400, 80, GREEN, 6)


@scene(209)
def listening_ear(d):
    d.rect(0, 0, 640, 480, "#f7fbff")
    d.ear_icon(260, 240, 1.6)
    for i, rx in enumerate((30, 55)):
        d.path(
            f"M{n(420)} {n(200 - rx)} A {n(rx)} {n(rx)} 0 0 1 {n(420)} {n(200 + rx)}",
            stroke=BLUE, sw=6,
        )


@scene(210)
def shiny_new(d):
    d.rect(0, 0, 640, 480, "#f7fbff")
    d.rrect(200, 160, 240, 180, 16, WHITE, INK, 5)
    d.star(320, 120, 36)
    d.sparkles([(160, 140, 10), (500, 160, 12), (140, 300, 8), (520, 320, 8)])


@scene(211)
def left_arrow(d):
    d.rect(0, 0, 640, 480, "#f4f8ff")
    d.arrow(520, 240, 120, 240, BLUE, 16)
    d.person(500, 400, 0.6, mood="smile", pose="point", flip=True)


@scene(212)
def passport_stamps(d):
    d.rect(0, 0, 640, 480, "#f4f7fb")
    d.rrect(180, 60, 280, 360, 12, "#7d3c4a", INK, 5)
    d.rrect(200, 90, 240, 300, 8, CREAM, INK, 3)
    d.circle(280, 180, 28, "none", BLUE, 4)
    d.rect(340, 160, 50, 36, "none", RED, 4)
    d.poly([(300, 250), (340, 230), (350, 280)], "none", GREEN, 4)
    d.circle(400, 280, 20, "none", ORANGE, 4)


@scene(213)
def ice_cubes(d):
    d.rect(0, 0, 640, 480, "#e7f6ff")
    d.rrect(180, 140, 120, 120, 12, "rgba(186,224,255,0.85)", INK, 4)
    d.rrect(300, 180, 120, 120, 12, "rgba(255,255,255,0.9)", BLUE, 4)
    d.line([(200, 170), (270, 230)], WHITE, 4)
    d.line([(330, 210), (390, 270)], WHITE, 4)


@scene(214)
def shopping_cart(d):
    d.rect(0, 0, 640, 480, "#f7fbff")
    d.path("M140 140 H300 L340 300 H180 Z", fill="none", stroke=INK, sw=6)
    d.line([(300, 160), (380, 120)], INK, 6)
    d.circle(210, 340, 22, NAVY)
    d.circle(320, 340, 22, NAVY)
    d.circle(230, 200, 16, RED)
    d.circle(270, 210, 14, GREEN)
    d.rrect(240, 230, 30, 24, 4, YELLOW, INK, 2)


@scene(215)
def looking_eye(d):
    d.rect(0, 0, 640, 480, "#f7fbff")
    d.eye_icon(320, 240, 2)


@scene(216)
def free_tag(d):
    d.rect(0, 0, 640, 480, "#e9f8ee")
    d.poly([(220, 80), (460, 80), (420, 220), (180, 220)], WHITE, INK, 5)
    d.circle(250, 140, 12, "#e9f8ee", INK, 3)
    d.glyph("0", 330, 120, 64, GREEN)
    d.gift(320, 360, 1)


@scene(217)
def spirit_level(d):
    d.rect(0, 0, 640, 480, "#f4f7fb")
    d.rrect(60, 200, 520, 70, 20, "#f0d78c", INK, 5)
    d.rrect(250, 212, 140, 46, 20, "#e7f6ff", INK, 3)
    d.circle(320, 235, 16, GREEN, INK, 3)
    d.line([(80, 300), (560, 300)], GREEN, 3)


@scene(218)
def child_playing(d):
    d.outdoor()
    d.person(260, 420, 0.85, mood="happy", pose="run", shirt=ORANGE, hair_style="short")
    ball(d, 430, 300, 36, RED)
    d.sun(80, 80, 32, face=True)


@scene(219)
def leader_group(d):
    d.outdoor()
    d.person(180, 420, 1.05, mood="confident", pose="point", shirt=RED)
    d.rect(150, 140, 8, 80, BROWN)
    d.poly([(158, 140), (230, 155), (158, 175)], YELLOW, INK, 3)
    d.person(360, 430, 0.7, mood="smile", shirt=BLUE)
    d.person(470, 440, 0.65, mood="smile", shirt=GREEN)
    d.person(560, 430, 0.6, mood="smile", shirt=ORANGE)


@scene(220)
def quality_meter(d):
    d.rect(0, 0, 640, 480, "#f7fbff")
    d.path("M100 360 A220 220 0 0 1 540 360", stroke=GREY, sw=20)
    d.path("M300 150 A220 220 0 0 1 540 360", stroke=GREEN, sw=20)
    d.line([(320, 360), (460, 200)], INK, 8)
    d.circle(320, 360, 18, NAVY)
    d.star(480, 120, 24)


@scene(221)
def setting_pot(d):
    d.indoor()
    d.rrect(120, 280, 400, 24, 6, BROWN)
    d.path("M300 260 L280 180 L400 180 L380 260 Z", fill="#c9854a", stroke=INK, sw=4)
    d.flower(340, 150, PINK, 0.7)
    d.path("M120 200 C180 140 240 180 290 190", fill=SKIN, stroke=INK, sw=12)


@scene(222)
def spelling_tiles(d):
    d.rect(0, 0, 640, 480, "#fff8ea")
    letters = ("A", "B", "C")
    colors = (RED, BLUE, GREEN)
    for i, letter in enumerate(letters):
        x = 80 + i * 140
        d.rrect(x, 180, 110, 110, 12, colors[i], INK, 4)
        d.glyph(letter, x + 55, 215, 48, WHITE)
    d.rrect(500, 180, 80, 110, 12, WHITE, INK, 4)
    d.line([(160, 360), (420, 300)], YELLOW, 8)
