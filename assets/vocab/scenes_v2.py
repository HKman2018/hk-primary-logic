"""Original v2.1 scenes for the 222-word picture bank.

Each scene matches that row's english + zh (pos when needed). image_hint is
only a starting point. English answers are never drawn. Short Traditional
Chinese appears only on calendar cards and the two gloss labels allowed by
the image spec (免費, 還可以).
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
    RED_DARK,
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


def n(value):
    return round(float(value), 1)


def face(d, mood, bg, hair_style="short", shirt=BLUE, scale=1.28):
    d.rect(0, 0, 640, 480, bg)
    # Full figure stays inside an 8% margin and still fills most of the frame.
    feet = 432
    d.person(320, feet, scale, mood=mood, hair_style=hair_style, shirt=shirt)
    return world(320, feet, scale, HEAD)


def ball(d, x, y, r=36, color=ORANGE):
    d.circle(x, y, r, color, INK, 4)
    d.path(f"M{n(x - r)} {n(y)} Q{n(x)} {n(y - r * 0.15)} {n(x + r)} {n(y)}", stroke=WHITE, sw=4)
    d.line([(x, y - r), (x, y + r)], WHITE, 3)


def weekday(d, index, icon):
    d.rect(0, 0, 640, 480, "#f4f8fc")
    d.calendar_base(70, 36, 500, 200)
    labels = ["一", "二", "三", "四", "五", "六", "日"]
    d.week_cells(92, 108, 456, active=index, marks=labels)
    names = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    d.zh(names[index], 320, 280, 48, BLUE_DARK)
    icon(d)


def month_card(d, name, icon, tint):
    d.rect(0, 0, 640, 480, tint)
    d.calendar_base(170, 28, 300, 110)
    d.zh(name, 320, 78, 40, WHITE)
    icon(d)


def shoe(d, x, y, fill, sc=1):
    d.ellipse(x, y, 78 * sc, 32 * sc, fill, INK, 4)
    d.path(
        f"M{n(x - 70 * sc)} {n(y)} Q{n(x - 40 * sc)} {n(y - 48 * sc)} {n(x - 8 * sc)} {n(y - 10 * sc)}",
        fill=fill, stroke=INK, sw=4,
    )
    d.circle(x + 36 * sc, y + 8 * sc, 10 * sc, NAVY, INK, 2)
    d.circle(x - 10 * sc, y + 10 * sc, 10 * sc, NAVY, INK, 2)


@scene(1)
def close_houses(d):
    d.outdoor()
    d.house(185, 410, 1.0)
    d.house(455, 410, 1.0)
    d.line([(268, 300), (372, 300)], RED, 8)
    d.line([(268, 282), (268, 318)], RED, 6)
    d.line([(372, 282), (372, 318)], RED, 6)


@scene(2)
def milk_glass(d):
    d.rect(0, 0, 640, 480, "#d7ecff")
    d.ellipse(320, 400, 120, 22, "rgba(36,48,68,0.12)")
    d.glass_cup(230, 70, "#fff4d2", 180, 300, level=0.22)
    d.circle(300, 40, 14, "#fff4d2", INK, 3)
    d.path("M292 54 Q300 70 308 54", stroke="#fff4d2", sw=6)


@scene(3)
def jam_jar(d):
    d.rect(0, 0, 640, 480, "#fff1ea")
    d.jar(250, 90)
    d.rrect(268, 150, 74, 28, 6, CREAM, INK, 2)
    d.circle(150, 300, 36, RED, INK, 4)
    d.circle(490, 280, 30, "#7dce6a", INK, 4)
    d.circle(170, 180, 16, RED, INK, 3)


@scene(4)
def black_swatch(d):
    d.rect(0, 0, 640, 480, "#eef2f6")
    d.rrect(160, 70, 320, 320, 36, "#141820", INK, 8)
    d.circle(250, 180, 28, "#141820", "#3a4254", 4)
    for i, color in enumerate((RED, YELLOW, BLUE, GREEN, WHITE)):
        d.circle(90, 110 + i * 60, 22, color, INK, 3)


@scene(5)
def popcorn_bowl(d):
    d.rect(0, 0, 640, 480, "#fff6e4")
    d.popcorn_bucket(320, 180, 1.7)


@scene(6)
def clear_glass(d):
    d.rect(0, 0, 640, 480, "#e5f7ff")
    d.circle(320, 250, 78, ORANGE, INK, 5)
    d.circle(300, 230, 14, YELLOW)
    d.glass_cup(230, 80, "rgba(186,230,255,0.25)", 180, 300, level=0.18)
    d.sparkles([(150, 120, 12), (500, 140, 14), (470, 300, 8)], BLUE)


@scene(7)
def soda_can(d):
    d.rect(0, 0, 640, 480, "#e7f7ff")
    d.can(250, 90)
    d.ellipse(330, 78, 36, 10, "#ffd0d0", INK, 3)
    d.rect(300, 70, 8, 16, GREY, INK, 2)
    for x, y, r in ((160, 160, 16), (480, 180, 22), (150, 280, 12), (500, 300, 14)):
        d.circle(x, y, r, "rgba(255,255,255,0.85)", "#7ec8f0", 3)


@scene(8)
def house_roof(d):
    d.outdoor()
    d.house(300, 420, 1.55)
    d.arrow(520, 70, 360, 150, RED, 10)
    d.circle(470, 90, 8, RED)


@scene(9)
def giving_up(d):
    d.outdoor(sky="#d5e4f2", ground="#c5d0b8")
    d.poly([(430, 430), (520, 220), (600, 430)], "#9aa8b8", INK, 4)
    d.rect(548, 200, 8, 36, BROWN)
    d.poly([(556, 200), (590, 212), (556, 226)], RED, INK, 3)
    d.person(230, 430, 1.2, mood="tired", pose="slump", shirt=GREY, pants="#6b7280")
    d.rrect(120, 360, 70, 50, 8, BLUE, INK, 3)
    d.line([(150, 340), (170, 360)], INK, 4)


@scene(10)
def floating_feather(d):
    d.rect(0, 0, 640, 480, "#e7f4ff")
    d.path("M300 60 Q420 200 300 360 Q190 200 300 60 Z", fill=WHITE, stroke=INK, sw=5)
    d.line([(300, 80), (300, 340)], GREY, 3)
    for y in (140, 190, 240, 290):
        d.line([(300, y), (250, y + 16)], "#c5ced8", 3)
        d.line([(300, y), (350, y + 16)], "#c5ced8", 3)
    d.circle(300, 420, 48, "#6b7280", INK, 5)
    d.line([(160, 140), (230, 150)], "#9fd4ff", 5)
    d.line([(380, 120), (470, 132)], "#9fd4ff", 5)


@scene(11)
def gift_bow(d):
    d.rect(0, 0, 640, 480, "#fff0f6")
    d.gift(320, 300, 2.4)
    d.sparkles([(120, 90, 14), (520, 110, 12), (100, 280, 10), (540, 300, 10)])


@scene(12)
def sick_in_bed(d):
    d.indoor(wall="#e7eef6")
    d.bed(70, 400, 500, 170)
    d.ellipse(360, 330, 170, 48, "#d5e4f5", INK, 4)
    d.circle(168, 248, 46, "#f3e2cf", INK, 4)
    d.line([(148, 242), (162, 242)], INK, 4)
    d.line([(174, 242), (188, 242)], INK, 4)
    d.path("M152 262 Q168 274 184 262", stroke=INK, sw=3)
    d.rrect(500, 130, 24, 110, 8, WHITE, INK, 3)
    d.rect(506, 160, 12, 50, RED)
    d.circle(512, 154, 8, RED, INK, 2)
    d.glass_cup(80, 250, "#d7ecff", 48, 86, level=0.35)


@scene(13)
def slumped(d):
    d.outdoor(sky="#c5d2e4", ground="#b7c3b4", horizon=360)
    d.cloud(140, 80, 1.3, "#d5deea")
    d.person(320, 450, 1.35, mood="sad", pose="slump", shirt="#7f8ea3")
    d.path("M470 150 Q500 110 490 170", stroke="#9aa8b8", sw=4)


@scene(14)
def empty_calendar(d):
    d.rect(0, 0, 640, 480, "#f3fbf6")
    d.calendar_base(36, 28, 430, 420)
    labels = ["一", "二", "三", "四", "五", "六", "日"]
    d.week_cells(56, 100, 390, marks=labels)
    gap = 8
    width = 390
    cell = (width - gap * 6) / 7
    for i in range(7):
        xx = 56 + i * (cell + gap)
        if i == 2:
            d.rrect(xx, 190, cell, 180, 8, WHITE, GREEN, 5)
        else:
            d.rrect(xx, 190, cell, 180, 8, "#e7eef6", INK, 2)
            d.circle(xx + cell / 2, 240, 7, BLUE)
            d.circle(xx + cell / 2, 280, 7, ORANGE)
    d.person(545, 400, 0.5, mood="smile", pose="sit", shirt=TEAL)


@scene(15)
def empty_shelf(d):
    d.indoor(wall="#f7f1e6", floor="#e6d3b8")
    d.rect(70, 70, 16, 340, BROWN, INK, 3)
    d.rect(540, 70, 16, 340, BROWN, INK, 3)
    for y in (110, 210, 310):
        d.rect(70, y, 486, 16, BROWN, INK, 4)
    d.rrect(250, 240, 40, 50, 6, "#f0d2b0", INK, 3)


@scene(16)
def sunny_sky(d):
    d.outdoor(sky="#b7e6ff")
    d.sun(240, 150, 90, face=True)
    d.cloud(500, 90, 0.9)
    d.sparkles([(80, 80, 10), (400, 70, 8), (120, 200, 6)])


@scene(17)
def nearby_arrow(d):
    d.outdoor()
    d.person(150, 420, 1.05, mood="smile", shirt=BLUE)
    d.tree(470, 400, 1.25)
    d.arrow(230, 250, 360, 250, RED, 8)
    d.line([(230, 236), (230, 264)], RED, 5)
    d.circle(290, 250, 10, YELLOW, INK, 3)


@scene(18)
def muddy_shoes(d):
    d.rect(0, 0, 640, 480, "#efe4d2")
    shoe(d, 220, 260, "#6b4428", 1.35)
    shoe(d, 430, 280, "#6b4428", 1.25)
    for x, y, r in ((120, 140, 14), (160, 200, 10), (500, 150, 16), (540, 220, 10), (300, 120, 12), (360, 380, 18)):
        d.circle(x, y, r, "#5a3a22")


@scene(19)
def cracked_earth(d):
    d.rect(0, 0, 640, 480, "#e8c48a")
    d.path("M40 60 L180 150 L90 240 L210 330 L70 450", stroke="#8a5a3b", sw=7)
    d.path("M260 30 L230 160 L360 220 L250 360 L340 470", stroke="#8a5a3b", sw=7)
    d.path("M430 50 L390 180 L560 250 L470 400 L580 450", stroke="#6b4428", sw=7)
    d.flower(500, 300, "#c9b48a", 0.55)
    d.path("M470 250 Q500 280 490 310", stroke="#a67c52", sw=4)


@scene(20)
def vivid_painting(d):
    d.indoor(wall="#f4f1ea")
    d.line([(320, 340), (320, 450)], BROWN, 10)
    d.rrect(90, 40, 460, 280, 10, WHITE, INK, 6)
    d.circle(190, 150, 50, RED, INK, 4)
    d.rect(250, 100, 90, 140, YELLOW, INK, 4)
    d.poly([(370, 250), (450, 90), (530, 250)], BLUE, INK, 4)
    d.circle(300, 220, 28, GREEN, INK, 3)
    d.rect(140, 230, 70, 50, ORANGE, INK, 3)


@scene(21)
def empty_pockets(d):
    d.outdoor(sky="#efe6d8", ground="#d7c4a3")
    d.person(320, 440, 1.3, mood="sad", shirt="#6d7c90", pants="#3a322c")
    d.poly([(230, 300), (190, 390), (270, 350)], WHITE, INK, 4)
    d.poly([(410, 300), (450, 390), (370, 350)], WHITE, INK, 4)
    d.circle(200, 400, 6, "#c0c7d0")
    d.path("M250 160 L270 200 L290 160", stroke="#8a5a3b", sw=4)


@scene(22)
def abc_blocks(d):
    d.rect(0, 0, 640, 480, "#fff6e6")
    d.rrect(120, 250, 150, 150, 16, RED, INK, 5)
    d.glyph("A", 195, 300, 72, WHITE)
    d.rrect(370, 250, 150, 150, 16, BLUE, INK, 5)
    d.glyph("B", 445, 300, 72, WHITE)
    d.rrect(245, 90, 150, 150, 16, GREEN, INK, 5)
    d.glyph("C", 320, 140, 72, WHITE)


@scene(23)
def mean_face(d):
    d.rect(0, 0, 640, 480, "#ffe8e4")
    d.person(200, 430, 1.15, mood="angry", shirt=RED)
    d.person(470, 450, 0.7, mood="cry", shirt=GREY)
    d.line([(300, 180), (390, 220)], INK, 5)
    d.poly([(390, 220), (370, 200), (400, 190)], INK)


@scene(24)
def iron_appliance(d):
    d.rect(0, 0, 640, 480, "#f4f7fb")
    d.rrect(80, 300, 480, 28, 8, "#d9dee6", INK, 4)
    d.iron(200, 200, 1.7)


@scene(25)
def rice_bowl(d):
    d.rect(0, 0, 640, 480, "#fffaf2")
    d.bowl(140, 230, 360, 120, WHITE)
    d.ellipse(320, 220, 140, 42, "#fffdf8", INK, 4)
    for x in (250, 290, 330, 370):
        d.ellipse(x, 210, 16, 10, WHITE, INK, 2)
    d.line([(470, 80), (520, 250)], BROWN, 6)
    d.line([(500, 70), (555, 230)], BROWN, 6)


@scene(26)
def honeybee(d):
    d.rect(0, 0, 640, 480, "#fff3c4")
    d.bee(300, 220, 2.8)
    d.flower(90, 380, PINK, 1.1)
    d.flower(540, 390, ORANGE, 1)


@scene(27)
def church_building(d):
    d.outdoor()
    d.rrect(180, 190, 280, 220, 8, CREAM, INK, 5)
    d.poly([(160, 200), (320, 60), (480, 200)], "#d5dbe3", INK, 5)
    d.rect(304, 28, 32, 48, "#d5dbe3", INK, 3)
    d.line([(320, 8), (320, 40)], INK, 5)
    d.line([(304, 24), (336, 24)], INK, 5)
    d.path("M270 400 L270 260 Q320 210 370 260 L370 400", fill="#8eb6e0", stroke=INK, sw=4)
    d.rrect(292, 310, 56, 90, 4, BROWN, INK, 3)


@scene(28)
def crane_build(d):
    d.outdoor(sky="#d5ebff")
    d.rect(100, 140, 28, 270, YELLOW, INK, 5)
    d.rect(100, 130, 340, 22, YELLOW, INK, 5)
    d.line([(90, 152), (140, 200)], YELLOW, 6)
    d.line([(340, 152), (340, 230)], INK, 4)
    d.rrect(280, 230, 110, 80, 8, ORANGE, INK, 4)
    d.rrect(160, 280, 90, 70, 6, "#d9dee6", INK, 4)
    d.rrect(250, 360, 90, 60, 6, "#d9dee6", INK, 4)
    d.person(500, 430, 0.55, mood="smile", shirt=ORANGE)


@scene(29)
def continue_arrow(d):
    d.rect(0, 0, 640, 480, "#eef8ff")
    for x, color in ((90, GREY), (160, GREY), (230, "#9aa8b8")):
        d.circle(x, 240, 22, color, INK, 4)
    d.arrow(280, 240, 560, 240, GREEN, 16)
    d.path("M300 180 Q400 140 500 180", stroke=GREEN, sw=5)


@scene(30)
def seedling_grow(d):
    d.outdoor()
    heights = (50, 110, 180)
    for i, h in enumerate(heights):
        x = 120 + i * 160
        d.rrect(x, 400 - h, 18, h, 6, GREEN_DARK)
        d.ellipse(x - 22, 400 - h, 28, 14, GREEN, INK, 3)
        d.ellipse(x + 28, 390 - h, 28, 14, GREEN, INK, 3)
    d.arrow(530, 320, 530, 120, GREEN_DARK, 10)


@scene(31)
def know_bulb(d):
    d.outdoor()
    d.person(250, 440, 1.25, mood="confident", pose="think", shirt=BLUE)
    d.bulb(470, 140, 1.8, on=True)


@scene(32)
def handshake(d):
    d.outdoor()
    d.person(190, 440, 1.15, mood="smile", shirt=BLUE, pose="hug")
    d.person(450, 440, 1.15, mood="smile", shirt=ORANGE, pose="hug", flip=True)
    d.ellipse(320, 280, 36, 18, SKIN, INK, 4)
    d.check(320, 140, 1.3)


@scene(33)
def puzzle_match(d):
    d.rect(0, 0, 640, 480, "#f3f6fb")
    d.path("M120 140 H250 V200 A28 28 0 0 1 250 260 V320 H120 Z", fill=BLUE, stroke=INK, sw=5)
    d.path("M300 180 A28 28 0 0 1 300 240 H390 V300 H250 V180 Z", fill=GREEN, stroke=INK, sw=5)
    d.path("M250 200 A28 28 0 0 0 250 260", fill=GREEN, stroke=INK, sw=5)
    d.check(320, 390, 1.5)


@scene(34)
def elderly(d):
    d.outdoor()
    d.person(300, 440, 1.3, mood="smile", hair_style="grey", shirt="#8aa0b4", pants=BROWN)
    d.glasses(300, 440, 1.3)
    d.cane(300, 440, 1.3)


@scene(35)
def bouquet(d):
    d.rect(0, 0, 640, 480, "#fff3f7")
    d.path("M230 460 L310 200 L410 460 Z", fill="#c9854a", stroke=INK, sw=4)
    colors = (PINK, RED, YELLOW, PURPLE, WHITE, ORANGE)
    for i, color in enumerate(colors):
        d.flower(150 + (i % 3) * 120, 120 + (i // 3) * 80, color, 0.85)


@scene(36)
def cheetah_run(d):
    d.outdoor(sky="#fff1cc", ground="#e6c27a", horizon=330)
    d.speed_lines(40, 160)
    d.speed_lines(30, 210)
    d.speed_lines(50, 260)
    d.cheetah(360, 300, 1.55)


@scene(37)
def small_kitten(d):
    d.indoor(wall="#fff4ea")
    d.kitten(300, 280, 2.15)
    d.ellipse(460, 360, 50, 18, "#f0d2b8")
    d.circle(120, 300, 18, PINK, INK, 3)


@scene(38)
def calm_lake(d):
    d.rect(0, 0, 640, 220, "#c5e8ff")
    d.rect(0, 300, 640, 180, "#7dce6a")
    d.ellipse(320, 310, 280, 100, "#3d98e0", INK, 5)
    d.ellipse(250, 290, 90, 16, "rgba(255,255,255,0.55)")
    d.sun(100, 80, 40, face=True)
    d.tree(70, 300, 0.75)
    d.tree(560, 310, 0.85)
    d.poly([(200, 220), (260, 150), (310, 220)], "#7ea0c4", INK, 3)


@scene(39)
def flowing_river(d):
    d.outdoor()
    d.path(
        "M-20 40 C140 120 60 200 200 250 C360 310 240 390 420 430 C540 470 620 400 680 460 "
        "L680 180 C500 160 460 280 300 210 C140 140 160 40 -20 10 Z",
        fill="#3d98e0", stroke=INK, sw=5,
    )
    d.arrow(180, 180, 240, 230, WHITE, 6)
    d.arrow(360, 300, 430, 360, WHITE, 6)
    d.tree(70, 380, 0.85)
    d.tree(560, 180, 0.6)


@scene(40)
def welcome_door(d):
    d.outdoor()
    d.house(420, 400, 1.05)
    d.door(330, 400, 150, 210, open_=True)
    d.person(160, 420, 1.05, mood="happy", pose="wave", shirt=TEAL)
    d.heart(250, 140, 22)


@scene(41)
def thought_bubble(d):
    d.outdoor()
    d.person(210, 440, 1.2, mood="think", pose="think")
    d.ellipse(470, 140, 110, 64, WHITE, INK, 4)
    d.circle(380, 210, 16, WHITE, INK, 3)
    d.circle(350, 240, 9, WHITE, INK, 3)
    ball(d, 430, 140, 22, RED)
    d.circle(510, 140, 18, BLUE, INK, 3)
    d.line([(455, 120), (485, 160)], GREY, 4)


@scene(42)
def large_elephant(d):
    d.outdoor()
    d.elephant(340, 400, 1.35)
    d.person(90, 430, 0.48, mood="wow", shirt=RED)


@scene(43)
def headline_news(d):
    d.indoor(wall="#f6f4f1")
    d.rrect(70, 30, 500, 400, 12, WHITE, INK, 6)
    d.rect(90, 50, 460, 90, "#1b1e26")
    d.glyph("!", 320, 70, 64, YELLOW)
    for i, w in enumerate((400, 360, 430, 280, 390, 250)):
        d.rect(110, 170 + i * 36, w, 16, GREY)
    d.star(470, 300, 36)
    d.person(80, 460, 0.4, mood="wow", shirt=RED)


@scene(44)
def mountain_view(d):
    d.rect(0, 0, 640, 480, "#b7e6ff")
    d.sun(520, 80, 46, face=True)
    d.poly([(0, 430), (150, 160), (280, 430)], "#8eafd0", INK, 4)
    d.poly([(140, 430), (340, 90), (540, 430)], "#5d86b4", INK, 4)
    d.poly([(300, 160), (360, 110), (400, 170)], WHITE)
    d.ellipse(320, 440, 360, 48, "#7dce6a")
    d.sparkles([(80, 70, 8), (200, 50, 6)], YELLOW)


@scene(45)
def silent_reading(d):
    d.indoor(wall="#f4f0ea")
    d.person(300, 420, 1.25, mood="shut", pose="read", shirt="#6b8f71")
    d.book(300, 200, 1.25)
    d.circle(500, 120, 36, WHITE, INK, 4)
    d.line([(484, 104), (516, 136)], INK, 5)
    d.line([(516, 104), (484, 136)], INK, 5)


@scene(46)
def reading_aloud(d):
    d.rect(0, 0, 640, 300, "#243044")
    d.rect(0, 300, 640, 180, "#6b5344")
    d.ellipse(180, 40, 70, 24, "rgba(255,211,77,0.45)")
    d.person(200, 400, 1.15, mood="happy", pose="read", shirt=RED)
    d.book(200, 190, 1.15)
    for x, y in ((420, 150), (490, 180), (450, 240)):
        d.circle(x, y, 22, SKIN, INK, 3)
        d.circle(x, y + 48, 26, BLUE, INK, 3)
    d.path("M330 140 Q380 100 400 150", stroke=YELLOW, sw=5)


@scene(47)
def holding_keys(d):
    d.outdoor()
    d.person(200, 430, 1.2, mood="smile", pose="carry", shirt=BLUE)
    d.house(480, 280, 0.7)
    d.circle(250, 170, 22, YELLOW, INK, 4)
    d.rect(268, 160, 46, 12, YELLOW, INK, 3)
    d.rect(300, 172, 12, 22, YELLOW, INK, 3)


@scene(48)
def permission_sign(d):
    d.outdoor()
    d.rect(250, 90, 18, 300, BROWN, INK, 3)
    d.rrect(80, 70, 230, 190, 18, WHITE, INK, 5)
    d.circle(195, 165, 58, "#e5f8ee", GREEN, 8)
    d.check(195, 165, 1.6)
    d.person(470, 430, 0.95, mood="smile", pose="wave", shirt=GREEN)


@scene(49)
def faith_heart(d):
    d.rect(0, 0, 640, 480, "#fff4e6")
    d.person(280, 450, 1.3, mood="shut", pose="think", shirt="#f0d2b0")
    d.heart(480, 130, 42, PINK)
    d.sparkles([(400, 70, 10), (540, 90, 10), (160, 120, 8)])


@scene(50)
def magician_reveal(d):
    d.rect(0, 0, 640, 480, "#243044")
    d.path("M200 340 L240 150 L400 150 L440 340 Z", fill="#1b1e26", stroke=INK, sw=5)
    d.ellipse(320, 150, 110, 26, "#3a322c", INK, 4)
    d.circle(320, 90, 36, WHITE, INK, 4)
    d.circle(306, 82, 5, INK)
    d.circle(332, 82, 5, INK)
    d.poly([(300, 104), (340, 104), (328, 128)], PINK, INK, 3)
    d.line([(300, 70), (340, 70)], INK, 3)
    d.sparkles([(120, 80, 14), (520, 90, 16), (100, 220, 10)], YELLOW)


@scene(51)
def fragile_glass(d):
    d.indoor()
    d.person(190, 430, 1.15, mood="wow", pose="carry", shirt=BLUE)
    d.glass_cup(380, 140, "rgba(186,224,255,0.35)", 100, 180, level=0.4)
    d.path("M400 200 L430 250", stroke="#9fd4ff", sw=3)
    d.path("M450 210 L470 250", stroke="#9fd4ff", sw=3)
    d.sparkles([(500, 130, 8), (370, 120, 6)])


@scene(52)
def magnifier_inspect(d):
    d.indoor(wall="#f4f9ff")
    d.person(170, 430, 1.1, mood="think", shirt=TEAL)
    d.circle(430, 210, 84, "rgba(186,224,255,0.4)", INK, 10)
    d.line([(490, 270), (560, 350)], BROWN, 12)
    d.flower(430, 210, PINK, 0.55)
    d.circle(430, 210, 84, "none", "rgba(255,255,255,0.0)", 0)


@scene(53)
def hard_puzzle(d):
    d.rect(0, 0, 640, 480, "#f4f7fb")
    d.rrect(60, 150, 150, 150, 14, BLUE, INK, 5)
    d.rrect(250, 250, 150, 150, 14, ORANGE, INK, 5)
    d.rrect(430, 120, 150, 150, 14, GREEN, INK, 5)
    d.path("M180 180 Q300 40 470 150", stroke=RED, sw=6)
    d.path("M300 300 Q380 200 450 250", stroke=RED, sw=6)
    d.glyph("?", 320, 40, 56, RED)


@scene(54)
def blue_rain(d):
    d.rect(0, 0, 640, 480, "#6b97cf")
    d.rect(80, 60, 220, 280, "#d7e6f5", INK, 5)
    d.rect(100, 80, 180, 220, "#9ec4ea", INK, 3)
    d.cloud(160, 40, 1.1, "#e7eef6")
    d.rain(100, 70, 6)
    d.person(460, 440, 1.15, mood="sad", shirt="#2f6fe0")


@scene(55)
def depressed(d):
    d.rect(0, 0, 640, 360, "#c5ced8")
    d.rect(0, 360, 640, 120, "#b7b0a4")
    d.person(320, 470, 1.2, mood="cry", pose="sit", shirt="#6d7c90")
    d.cloud(470, 90, 1.1, "#9aa8b8")
    d.rain(430, 130, 4)


@scene(56)
def world_flags(d):
    d.rect(0, 0, 640, 480, "#e5f3ff")
    d.circle(320, 250, 130, "#4aa3e8", INK, 6)
    d.ellipse(320, 250, 52, 128, GREEN, INK, 4)
    d.ellipse(320, 250, 128, 42, "none", GREEN_DARK, 4)
    d.rect(40, 70, 100, 64, RED, INK, 4)
    d.rect(500, 70, 100, 64, BLUE, INK, 4)
    d.rect(40, 340, 100, 64, YELLOW, INK, 4)
    d.rect(500, 340, 100, 64, GREEN, INK, 4)
    d.line([(90, 134), (90, 200)], BROWN, 4)
    d.line([(550, 134), (550, 200)], BROWN, 4)


@scene(57)
def countryside(d):
    d.outdoor()
    d.rrect(70, 200, 230, 180, 6, RED, INK, 5)
    d.poly([(50, 210), (185, 90), (320, 210)], "#f7f4ee", INK, 5)
    d.rect(150, 270, 60, 90, WHITE, INK, 3)
    for x in range(40, 620, 36):
        d.line([(x, 390), (x, 450)], "#c4a574", 4)
    d.line([(30, 390), (620, 390)], BROWN, 5)
    d.sheep(500, 400, 0.85)


@scene(58)
def bus_driver(d):
    d.rect(0, 0, 640, 480, "#d7f0ff")
    d.rect(0, 360, 640, 120, "#9aa8b8")
    d.rrect(30, 70, 580, 280, 36, "#f5d76e", INK, 6)
    d.rrect(60, 100, 180, 130, 14, "#9fd4ff", INK, 4)
    d.rrect(260, 100, 150, 80, 10, "#9fd4ff", INK, 3)
    d.rrect(430, 100, 150, 80, 10, "#9fd4ff", INK, 3)
    d.circle(120, 360, 40, "#1b1e26", INK, 4)
    d.circle(500, 360, 40, "#1b1e26", INK, 4)
    d.circle(150, 170, 36, SKIN, INK, 4)
    d.circle(138, 164, 4, INK)
    d.circle(162, 164, 4, INK)
    d.circle(90, 190, 40, "#d0d7e0", INK, 4)


@scene(59)
def aiming(d):
    d.outdoor(ground="#c4a574")
    d.person(160, 430, 1.15, mood="think", pose="point", shirt=NAVY)
    d.circle(490, 210, 80, WHITE, INK, 5)
    d.circle(490, 210, 54, RED, INK, 4)
    d.circle(490, 210, 26, YELLOW, INK, 4)
    d.circle(490, 210, 8, INK)
    d.arrow(250, 250, 420, 210, BROWN, 6)


@scene(60)
def proof_stamp(d):
    d.rect(0, 0, 640, 480, "#f6f4f1")
    d.rrect(110, 40, 420, 400, 14, WHITE, INK, 5)
    for i, w in enumerate((300, 260, 320, 200, 280)):
        d.rect(150, 90 + i * 44, w, 16, GREY)
    d.circle(400, 320, 70, "none", RED, 10)
    d.check(400, 320, 1.5, RED)


@scene(61)
def wild_hair(d):
    face(d, "wild", "#fff4c8", hair_style="wild", shirt=ORANGE)
    d.star(120, 80, 18, YELLOW)
    d.star(520, 100, 16, PINK)
    d.path("M80 200 Q120 160 100 240", stroke=PURPLE, sw=5)
    d.path("M540 180 Q500 140 560 240", stroke=BLUE, sw=5)


@scene(62)
def angry_red(d):
    face(d, "angry", "#ffd0cc", shirt=RED)
    d.path("M140 70 Q170 20 200 80", stroke="#d9dee6", sw=8)
    d.path("M450 60 Q490 10 520 80", stroke="#d9dee6", sw=8)
    d.path("M160 40 Q180 10 190 50", stroke="#c5ced8", sw=5)


@scene(63)
def clown_face(d):
    hx, hy = face(d, "silly", "#fff0f6", hair_style="wild", shirt=PINK)
    d.circle(hx, hy + 36, 22, RED, INK, 3)
    d.circle(hx - 70, hy + 10, 16, YELLOW, INK, 3)
    d.circle(hx + 70, hy + 10, 16, GREEN, INK, 3)


@scene(64)
def ham_slice(d):
    d.rect(0, 0, 640, 480, "#fff4f0")
    d.plate(320, 330, 320)
    d.ellipse(320, 250, 140, 90, "#f0a0b0", INK, 5)
    d.ellipse(370, 240, 36, 28, "#f7d7c4", INK, 4)
    d.ellipse(280, 270, 20, 14, "#e07088")


@scene(65)
def inch_ruler(d):
    d.rect(0, 0, 640, 480, "#f7f5f2")
    d.rrect(50, 200, 540, 90, 10, "#f0d7a2", INK, 5)
    for i in range(13):
        h = 48 if i % 4 == 0 else 26
        d.line([(90 + i * 40, 210), (90 + i * 40, 210 + h)], INK, 3)
    d.line([(90, 150), (130, 150)], RED, 8)
    d.line([(90, 136), (90, 164)], RED, 5)
    d.line([(130, 136), (130, 164)], RED, 5)
    d.glyph("1", 110, 100, 40, RED)


@scene(66)
def bathtub(d):
    d.indoor(wall="#e5f6fb", floor="#d5e6ee")
    d.ellipse(320, 320, 230, 90, WHITE, INK, 6)
    d.ellipse(320, 300, 180, 48, "#8ec8f0", INK, 4)
    d.circle(240, 230, 42, SKIN, INK, 4)
    d.circle(224, 222, 5, INK)
    d.circle(254, 222, 5, INK)
    d.path("M226 246 Q240 258 256 246", stroke=INK, sw=3)
    d.circle(450, 160, 14, "#9fd4ff", INK, 3)
    d.circle(470, 190, 10, "#9fd4ff")


@scene(67)
def digging(d):
    d.outdoor(ground="#c4a574", horizon=300)
    d.ellipse(460, 390, 90, 28, "#8a5a3b")
    d.person(200, 420, 1.15, mood="think", pose="push", shirt=GREEN)
    d.line([(340, 140), (450, 360)], "#c5ced6", 10)
    d.poly([(420, 340), (510, 360), (460, 410)], "#d9dee6", INK, 5)


@scene(68)
def doctor_exam(d):
    d.indoor(wall="#f5fbff")
    d.person(200, 430, 1.15, mood="smile", shirt=WHITE)
    d.circle(210, 250, 18, "#d9dee6", INK, 3)
    d.line([(210, 268), (210, 310)], "#c5ced8", 5)
    d.path("M180 310 Q210 340 240 310", stroke="#c5ced8", sw=5)
    d.person(470, 440, 0.85, mood="smile", shirt=BLUE, pose="sit")
    d.circle(430, 180, 50, "rgba(186,224,255,0.45)", INK, 6)
    d.line([(468, 214), (510, 260)], NAVY, 8)


@scene(69)
def hot_sun(d):
    d.rect(0, 0, 640, 480, "#ffe4b8")
    d.sun(200, 180, 90, face=True)
    d.rrect(450, 140, 36, 200, 14, WHITE, INK, 4)
    d.rect(458, 200, 20, 120, RED)
    d.circle(468, 190, 12, RED, INK, 2)
    for i in range(3):
        d.path(
            f"M{n(360)} {n(120 + i * 50)} Q{n(410)} {n(145 + i * 50)} {n(360)} {n(170 + i * 50)}",
            stroke=RED, sw=6,
        )


@scene(70)
def supporting_friend(d):
    d.outdoor()
    d.person(200, 430, 1.15, mood="smile", pose="hug", shirt=BLUE)
    d.person(400, 440, 1.05, mood="sad", pose="slump", shirt=ORANGE)
    d.heart(320, 120, 26)


@scene(71)
def pushing_door(d):
    d.indoor()
    d.rrect(340, 80, 220, 340, 10, "#d9dee6", INK, 5)
    d.person(200, 430, 1.2, mood="angry", pose="push", shirt=RED)
    d.line([(300, 180), (350, 180)], "#9aa8b8", 5)
    d.line([(300, 230), (360, 230)], "#9aa8b8", 5)
    d.line([(300, 280), (350, 280)], "#9aa8b8", 5)
    d.path("M150 140 Q170 100 190 140", stroke="#9ec4ea", sw=4)


@scene(72)
def welcome_mat(d):
    d.outdoor()
    d.door(220, 300, 200, 240, open_=True)
    d.rrect(180, 340, 280, 70, 12, "#c9854a", INK, 5)
    d.heart(320, 372, 18, RED)
    d.person(80, 430, 0.7, mood="happy", pose="wave", shirt=TEAL)
    d.person(520, 430, 0.7, mood="smile", pose="wave", shirt=PINK, hair_style="long")


@scene(73)
def helping(d):
    d.outdoor()
    d.person(180, 440, 1.05, mood="sad", pose="sit", shirt=GREY)
    d.person(400, 420, 1.1, mood="smile", pose="hug", shirt=GREEN)
    d.heart(500, 140, 20)
    d.rrect(300, 240, 50, 16, 6, WHITE, INK, 3)


@scene(74)
def shark_ocean(d):
    d.rect(0, 0, 640, 120, "#bfe8ff")
    d.rect(0, 120, 640, 360, "#2a78b8")
    d.path("M0 120 Q80 96 160 120 T320 120 T480 120 T640 120 L640 150 L0 150 Z", fill="#4aa3e8")
    d.shark(330, 300, 1.6)
    for x, y, r in ((80, 220, 10), (140, 300, 8), (540, 200, 9), (560, 340, 7)):
        d.circle(x, y, r, "rgba(255,255,255,0.75)")


@scene(75)
def fluffy_sheep(d):
    d.outdoor()
    d.sheep(320, 360, 2.05)
    d.cloud(110, 80, 0.8)


@scene(76)
def tiger_stand(d):
    d.outdoor(ground="#d5e8c0")
    d.tiger(330, 370, 1.7)
    d.tree(80, 400, 0.8)


@scene(77)
def wedding_couple(d):
    d.rect(0, 0, 640, 480, "#fff3f7")
    d.person(230, 440, 1.2, mood="smile", hair_style="long", shirt=WHITE)
    d.path("M170 160 Q230 80 290 170", stroke=WHITE, sw=10)
    d.person(420, 440, 1.15, mood="smile", shirt=NAVY)
    d.heart(320, 70, 22)


@scene(78)
def actor_stage(d):
    d.rect(0, 0, 640, 480, "#243044")
    d.ellipse(320, 50, 120, 36, "rgba(255,211,77,0.4)")
    d.rect(30, 360, 580, 36, BROWN, INK, 4)
    d.person(320, 430, 1.3, mood="happy", pose="wave", shirt=RED)
    d.rrect(230, 90, 180, 18, 6, YELLOW, INK, 3)


@scene(79)
def actress_stage(d):
    d.rect(0, 0, 640, 480, "#3a2744")
    d.ellipse(320, 50, 130, 34, "rgba(255,143,171,0.5)")
    d.rect(30, 360, 580, 36, BROWN, INK, 4)
    d.person(300, 430, 1.3, mood="smile", pose="wave", shirt=PINK, hair_style="long")
    d.flower(480, 200, PINK, 0.8)


@scene(80)
def parking_sign(d):
    d.outdoor(ground="#9aa3ad", horizon=340)
    d.rect(150, 70, 16, 300, GREY, INK, 4)
    d.rrect(70, 50, 170, 170, 16, BLUE, INK, 6)
    d.glyph("P", 155, 100, 84, WHITE)
    d.rrect(300, 220, 260, 90, 20, RED, INK, 5)
    d.rrect(330, 240, 90, 40, 8, "#9fd4ff", INK, 3)
    d.circle(360, 330, 28, "#1b1e26", INK, 3)
    d.circle(500, 330, 28, "#1b1e26", INK, 3)


@scene(81)
def blowing_wind(d):
    d.outdoor(sky="#e4f3ff")
    for y, w in ((70, 200), (120, 260), (170, 180)):
        d.line([(30, y), (30 + w, y - 12)], "#8ec8f0", 8)
    d.ellipse(340, 140, 36, 16, GREEN, INK, 3)
    d.ellipse(430, 100, 30, 14, ORANGE, INK, 3)
    d.ellipse(500, 160, 26, 12, YELLOW, INK, 3)
    d.person(180, 430, 0.9, mood="wow", shirt=BLUE)
    d.path("M250 240 Q340 160 420 250 Q480 190 540 260", stroke=BROWN, sw=5)


@scene(82)
def carrying_box(d):
    d.outdoor()
    d.person(320, 440, 1.25, mood="smile", pose="carry", shirt=ORANGE)
    d.rrect(230, 90, 180, 140, 12, "#e0b44a", INK, 5)
    d.line([(230, 160), (410, 160)], BROWN, 4)
    d.line([(320, 90), (320, 230)], BROWN, 4)


@scene(83)
def pleasant_scene(d):
    d.outdoor()
    d.sun(90, 80, 40, face=True)
    d.person(200, 410, 0.95, mood="happy", shirt=YELLOW)
    d.person(420, 410, 0.95, mood="smile", shirt=PINK, hair_style="long")
    d.flower(80, 380, PINK, 0.7)
    d.flower(560, 390, RED, 0.7)
    d.ellipse(320, 300, 70, 16, "#e7c98a", INK, 3)
    d.circle(300, 270, 16, RED, INK, 2)
    d.circle(340, 274, 14, GREEN, INK, 2)


@scene(84)
def tall_tower(d):
    d.outdoor(sky="#d5ecff")
    d.rrect(250, 20, 130, 390, 8, "#d5dee6", INK, 5)
    for y in (50, 100, 150, 200, 250, 300, 350):
        d.rect(270, y, 32, 22, "#9fd4ff", INK, 2)
        d.rect(328, y, 32, 22, "#9fd4ff", INK, 2)
    d.person(120, 440, 0.55, mood="wow")
    d.arrow(500, 360, 500, 80, BLUE, 8)


@scene(85)
def wide_road(d):
    d.rect(0, 0, 640, 160, "#bfe8ff")
    d.poly([(40, 180), (600, 180), (560, 450), (80, 450)], "#6b7280", INK, 5)
    d.line([(300, 210), (320, 430)], YELLOW, 10)
    d.arrow(70, 300, 200, 300, WHITE, 8)
    d.arrow(570, 300, 440, 300, WHITE, 8)
    d.cloud(120, 70, 0.7)


@scene(86)
def yellow_banana(d):
    d.rect(0, 0, 640, 480, "#fff6df")
    d.banana(330, 250, 1.7)


@scene(87)
def ant_insect(d):
    d.rect(0, 0, 640, 480, "#f4f0e8")
    d.ant(320, 250, 2.8)


@scene(88)
def bat_animal(d):
    d.night()
    d.circle(500, 70, 36, "#f4f1ea")
    d.bat(310, 240, 2.2)
    d.circle(80, 90, 3, WHITE)
    d.circle(140, 50, 2, WHITE)
    d.circle(200, 100, 2, WHITE)


@scene(89)
def filling_cup(d):
    d.rect(0, 0, 640, 480, "#e5f6ff")
    d.glass_cup(250, 150, "#7ec8f0", 150, 240, level=0.15)
    d.path("M300 20 Q340 80 320 150", stroke="#3d98e0", sw=14)
    d.circle(325, 150, 8, "#3d98e0")
    d.arrow(480, 300, 480, 160, BLUE, 10)


@scene(90)
def wedding_rings(d):
    d.rect(0, 0, 640, 480, "#fff6ea")
    d.ellipse(240, 230, 80, 80, "none", "#e0b44a", 16)
    d.ellipse(380, 250, 80, 80, "none", "#f0d78c", 16)
    d.person(140, 450, 0.55, mood="smile", shirt=NAVY)
    d.person(520, 450, 0.55, mood="smile", shirt=WHITE, hair_style="long")
    d.sparkles([(160, 120, 10), (500, 130, 10)])


@scene(91)
def forgetting(d):
    d.outdoor()
    d.person(230, 440, 1.2, mood="think", pose="think")
    d.ellipse(480, 140, 100, 60, WHITE, INK, 4)
    d.glyph("?", 480, 115, 48, GREY)
    d.circle(400, 210, 14, WHITE, INK, 3)
    d.circle(370, 240, 8, WHITE, INK, 2)
    d.path("M430 130 Q470 150 510 130", stroke="#d9dee6", sw=4)


@scene(92)
def string_finger(d):
    d.rect(0, 0, 640, 480, "#fff6f0")
    d.ellipse(320, 400, 90, 18, "rgba(36,48,68,0.1)")
    d.rrect(250, 160, 90, 200, 36, SKIN, INK, 6)
    d.circle(295, 140, 40, SKIN, INK, 5)
    d.path("M320 120 Q420 70 390 180 Q340 140 330 170", stroke=RED, sw=8)
    d.circle(400, 100, 10, RED)


@scene(93)
def clover(d):
    d.rect(0, 0, 640, 480, "#e5f8e8")
    for ang in (0, 90, 180, 270):
        rad = math.radians(ang)
        d.circle(320 + math.cos(rad) * 58, 190 + math.sin(rad) * 58, 52, GREEN, INK, 5)
    d.circle(320, 190, 18, GREEN_DARK)
    d.line([(320, 250), (320, 430)], GREEN_DARK, 8)
    d.sparkles([(150, 90, 12), (500, 110, 12), (120, 250, 8)])


@scene(94)
def cooked_chicken(d):
    d.rect(0, 0, 640, 480, "#fff4ec")
    d.plate(320, 340, 300)
    d.ellipse(320, 250, 130, 70, "#e0a85a", INK, 5)
    d.ellipse(210, 230, 48, 28, "#e0a85a", INK, 4)
    d.ellipse(430, 240, 36, 22, "#c4844a", INK, 4)
    d.circle(300, 230, 6, "#8a5a3b")
    d.circle(340, 240, 5, "#8a5a3b")


@scene(95)
def fruit_pie(d):
    d.rect(0, 0, 640, 480, "#fff6f0")
    d.ellipse(320, 300, 180, 80, "#e0b44a", INK, 6)
    d.ellipse(320, 260, 150, 60, "#d64545", INK, 5)
    d.line([(200, 250), (440, 250)], "#f3e2c4", 5)
    d.line([(320, 200), (320, 310)], "#f3e2c4", 5)
    d.circle(260, 240, 12, RED, INK, 2)
    d.circle(370, 250, 12, RED, INK, 2)
    d.circle(320, 230, 10, "#7dce6a", INK, 2)


@scene(96)
def speech_bubble(d):
    d.outdoor()
    d.person(190, 440, 1.15, mood="happy", pose="wave")
    d.rrect(320, 60, 260, 160, 28, WHITE, INK, 5)
    d.poly([(360, 210), (300, 280), (420, 210)], WHITE, INK, 4)
    d.line([(370, 120), (530, 120)], GREY, 8)
    d.line([(370, 160), (490, 160)], GREY, 8)


@scene(97)
def taking_object(d):
    d.indoor()
    d.rrect(280, 280, 280, 28, 8, BROWN, INK, 4)
    d.circle(460, 230, 36, RED, INK, 4)
    d.path("M60 300 C160 180 240 160 340 210", stroke=SKIN, sw=22)
    d.circle(330, 200, 18, SKIN, INK, 4)
    d.arrow(140, 100, 300, 170, BLUE, 8)


@scene(98)
def plus_blocks(d):
    d.rect(0, 0, 640, 480, "#f2f6ff")
    d.rrect(50, 150, 160, 160, 18, BLUE, INK, 5)
    d.glyph("2", 130, 200, 72, WHITE)
    d.glyph("+", 290, 200, 80, INK)
    d.rrect(380, 150, 160, 160, 18, GREEN, INK, 5)
    d.glyph("3", 460, 200, 72, WHITE)


@scene(99)
def growing_bars(d):
    d.rect(0, 0, 640, 480, "#f5f9ff")
    d.line([(90, 60), (90, 400), (560, 400)], INK, 5)
    heights = (70, 140, 210, 300)
    colors = ("#c5dff8", "#7eb6ef", "#4c8dff", "#2f6fe0")
    for i, (h, color) in enumerate(zip(heights, colors)):
        d.rrect(140 + i * 90, 400 - h, 64, h, 8, color, INK, 4)
    d.arrow(520, 280, 560, 100, GREEN, 10)


@scene(100)
def asking_question(d):
    d.outdoor()
    d.person(210, 440, 1.25, mood="think", pose="wave")
    d.circle(470, 150, 70, WHITE, INK, 5)
    d.glyph("?", 470, 115, 72, BLUE)


@scene(101)
def requesting_help(d):
    d.outdoor()
    d.person(180, 440, 1.15, mood="sad", pose="plead", shirt=GREY)
    d.person(480, 430, 1.1, mood="smile", shirt=GREEN)
    d.rrect(390, 200, 50, 40, 6, BROWN, INK, 3)
    d.heart(330, 130, 18, PINK)


@scene(102)
def booking_stamp(d):
    d.rect(0, 0, 640, 480, "#f3fbf7")
    d.calendar_base(40, 50, 360, 370)
    d.week_cells(60, 130, 320, active=3, marks=["一", "二", "三", "四", "五", "六", "日"])
    d.circle(500, 250, 70, "none", RED, 10)
    d.poly([(470, 250), (500, 290), (545, 210)], "none", RED, 8)


@scene(103)
def bringing_gift(d):
    d.outdoor()
    d.person(160, 430, 1.1, mood="smile", pose="carry", shirt=ORANGE)
    d.gift(230, 160, 0.95)
    d.person(500, 430, 1.0, mood="happy", pose="wave", shirt=PINK, flip=True)
    d.arrow(300, 260, 430, 260, BLUE, 8)


@scene(104)
def checklist(d):
    d.rect(0, 0, 640, 480, "#f5f9ff")
    d.rrect(120, 30, 400, 420, 18, WHITE, INK, 5)
    for i in range(5):
        y = 80 + i * 70
        d.rrect(160, y, 44, 44, 8, WHITE, INK, 4)
        d.check(182, y + 22, 0.85)
        d.rect(230, y + 14, 230, 14, GREY)


@scene(105)
def doing_chores(d):
    d.indoor()
    d.person(180, 420, 1.15, mood="smile", pose="push", shirt=TEAL)
    d.rrect(360, 160, 200, 140, 16, "#d5dee6", INK, 5)
    d.ellipse(460, 220, 60, 20, "#9fd4ff", INK, 3)
    d.circle(400, 200, 18, YELLOW, INK, 3)
    d.circle(500, 210, 14, WHITE, INK, 3)


@scene(106)
def starting_line(d):
    d.outdoor(ground="#6b7280", horizon=280)
    d.line([(70, 280), (70, 470)], WHITE, 10)
    d.person(180, 450, 1.15, mood="think", pose="run", shirt=RED)
    d.circle(500, 90, 32, "#3cb371", INK, 4)
    d.circle(500, 160, 32, YELLOW, INK, 4)
    d.circle(500, 230, 32, "#d9dee6", INK, 4)


@scene(107)
def hogging_toys(d):
    d.indoor(wall="#fff4ec")
    d.person(230, 420, 1.15, mood="angry", pose="hug", shirt=RED)
    ball(d, 150, 240, 26, BLUE)
    d.circle(230, 210, 20, YELLOW, INK, 3)
    d.rrect(280, 230, 48, 48, 8, GREEN, INK, 3)
    d.person(510, 440, 0.75, mood="sad", shirt=GREY)


@scene(108)
def dunce_cap(d):
    hx, hy = face(d, "silly", "#fff6e4", shirt=ORANGE)
    d.poly([(hx - 70, hy - 80), (hx, hy - 190), (hx + 70, hy - 80)], "#f0d78c", INK, 5)
    d.path(f"M{n(hx - 40)} {n(hy - 20)} Q{n(hx)} {n(hy - 60)} {n(hx + 50)} {n(hy - 10)}", stroke=BLUE, sw=5)


@scene(109)
def policeman(d):
    d.outdoor()
    d.person(320, 440, 1.35, mood="smile", shirt="#2458c8", pants=NAVY)
    hx, hy = world(320, 440, 1.35, HEAD)
    d.ellipse(hx, hy - 46, 58, 18, "#1d3f86", INK, 4)
    d.rrect(hx - 10, hy - 86, 20, 40, 4, "#1d3f86", INK, 3)
    d.star(hx, hy + 80, 18, YELLOW)


@scene(110)
def attention_sign(d):
    d.rect(0, 0, 640, 480, "#fff6e0")
    d.poly([(320, 30), (590, 420), (50, 420)], YELLOW, INK, 8)
    d.glyph("!", 320, 190, 120, INK)
    d.person(100, 460, 0.42, mood="wow")


@scene(111)
def missed_bus(d):
    d.outdoor()
    d.rrect(280, 120, 320, 160, 20, "#f5d76e", INK, 5)
    d.rrect(310, 145, 80, 60, 8, "#9fd4ff", INK, 3)
    d.circle(340, 290, 28, NAVY, INK, 3)
    d.circle(530, 290, 28, NAVY, INK, 3)
    d.arrow(340, 80, 540, 80, RED, 8)
    d.person(110, 430, 1.0, mood="sad", pose="run", shirt=BLUE)


# Scenes 112–222 live in scenes_v2b and register on import.
import scenes_v2b  # noqa: E402,F401
