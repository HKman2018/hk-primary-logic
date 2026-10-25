"""Scenes 112–222 for the v2.1 picture bank. Imported by scenes_v2."""

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
from scenes_v2 import ball, face, month_card, n, scene, weekday


@scene(112)
def rubbing_hands(d):
    d.rect(0, 0, 640, 480, "#fff4ec")
    d.ellipse(230, 250, 90, 56, SKIN, INK, 5)
    d.ellipse(400, 250, 90, 56, SKIN, INK, 5)
    d.path("M150 170 Q210 110 250 180", stroke="#c5ced8", sw=6)
    d.path("M470 160 Q530 110 540 190", stroke="#c5ced8", sw=6)
    d.path("M200 140 Q240 100 230 160", stroke=ORANGE, sw=4)
    d.path("M420 130 Q470 90 480 150", stroke=ORANGE, sw=4)


@scene(113)
def wilted_flower(d):
    d.rect(0, 0, 640, 480, "#f3efe6")
    d.path("M300 440 Q340 300 310 160", stroke="#8a7a62", sw=8)
    d.circle(280, 150, 36, "#b7a48a", INK, 4)
    d.circle(340, 170, 32, "#a89078", INK, 4)
    d.circle(300, 190, 28, "#c4b49a", INK, 4)
    d.path("M220 360 Q300 410 400 340", stroke="#7d8a62", sw=5)
    d.line([(250, 80), (290, 120)], GREY, 5)
    d.line([(290, 80), (250, 120)], GREY, 5)


@scene(114)
def thumbs_up(d):
    d.rect(0, 0, 640, 480, "#e5f8ec")
    d.thumb(300, 150, up=True, sc=2.6)
    d.sparkles([(140, 100, 14), (510, 120, 14), (120, 280, 8)])
    d.circle(500, 300, 36, GREEN, INK, 4)
    d.check(500, 300, 0.9)


@scene(115)
def good_enough(d):
    d.rect(0, 0, 640, 480, "#f3faf5")
    d.rrect(70, 180, 360, 48, 16, "#e4f0e8", INK, 4)
    d.rect(70, 180, 240, 48, "#b7e4c7")
    d.line([(310, 150), (310, 250)], GREEN_DARK, 6)
    d.thumb(520, 190, up=True, sc=1.15)
    d.zh("還可以", 230, 280, 36, GREEN_DARK)


@scene(116)
def giant_whale(d):
    d.rect(0, 0, 640, 140, "#bfe8ff")
    d.rect(0, 140, 640, 340, "#2a78b8")
    d.whale(320, 300, 1.35)
    d.rrect(40, 200, 70, 24, 6, "#e0b44a", INK, 3)
    d.path("M500 150 L560 190 L510 190 Z", fill=WHITE, stroke=INK, sw=3)


@scene(117)
def priority_star(d):
    d.rect(0, 0, 640, 480, "#fff6e4")
    d.star(320, 230, 140, YELLOW)
    d.glyph("!", 320, 190, 90, RED)
    d.rrect(230, 340, 180, 28, 8, WHITE, INK, 3)
    d.rect(246, 350, 120, 8, RED)


@scene(118)
def four_seasons(d):
    d.rect(0, 0, 640, 480, "#f5f9ff")
    colors = ("#f7c1d4", GREEN, ORANGE, "#d5dde6")
    for i, color in enumerate(colors):
        x = 70 + i * 145
        d.rrect(x + 36, 250, 18, 140, 6, BROWN, INK, 3)
        d.circle(x + 45, 210, 52, color, INK, 4)
    d.flower(115, 190, PINK, 0.35)
    d.sun(250, 150, 18)
    d.ellipse(370, 170, 22, 12, ORANGE, INK, 2)
    d.snowflake(500, 160, 14)


@scene(119)
def storybook(d):
    d.rect(0, 0, 640, 480, "#fff6ea")
    d.book(320, 90, 2.5)
    d.circle(210, 190, 22, YELLOW, INK, 3)
    d.circle(420, 200, 24, GREEN, INK, 3)
    d.star(230, 260, 16)
    d.house(410, 280, 0.35)


@scene(120)
def wearing_coat(d):
    d.outdoor(sky="#d5e4f2")
    d.person(320, 440, 1.3, mood="smile", shirt="#3a6ea5")
    d.rrect(230, 180, 180, 180, 24, "#2c5288", INK, 5)
    d.circle(230, 220, 26, SKIN, INK, 3)
    d.circle(410, 220, 26, SKIN, INK, 3)
    d.snowflake(80, 80, 12)
    d.snowflake(540, 90, 10)


@scene(121)
def laying_book(d):
    d.indoor()
    d.rrect(140, 280, 400, 30, 8, BROWN, INK, 4)
    d.book(360, 150, 1.35, open_=False)
    d.path("M80 240 C180 150 250 190 330 200", stroke=SKIN, sw=18)
    d.circle(320, 190, 16, SKIN, INK, 3)
    d.arrow(120, 120, 240, 170, BLUE, 6)


@scene(122)
def lying_down(d):
    d.indoor(wall="#e6eef8", floor="#d7e4c8")
    d.ellipse(340, 300, 220, 50, "#f7f1e8", INK, 5)
    d.ellipse(160, 280, 70, 36, WHITE, INK, 4)
    with d.g("translate(380 300) rotate(-80)"):
        d.person(0, 0, 0.85, mood="shut", pose="lie", shirt="#8eb0e0")
    d.circle(80, 120, 8, "#c5ced8")
    d.circle(110, 90, 6, "#c5ced8")


@scene(123)
def caterpillar_butterfly(d):
    d.outdoor()
    d.ellipse(140, 250, 80, 32, GREEN, INK, 5)
    d.circle(210, 236, 20, GREEN, INK, 4)
    d.circle(200, 230, 4, INK)
    d.circle(218, 230, 4, INK)
    d.line([(190, 220), (180, 200)], INK, 3)
    d.line([(220, 218), (232, 198)], INK, 3)
    d.arrow(250, 240, 340, 240, ORANGE, 10)
    d.butterfly(490, 220, 1.35)


@scene(124)
def changing_weather(d):
    d.rect(0, 0, 640, 240, "#d7ecff")
    d.rect(0, 240, 640, 240, "#e7e0d4")
    d.sun(140, 150, 58, face=True)
    d.arrow(230, 200, 380, 200, GREY, 10)
    d.cloud(510, 150, 1.45, "#d5dee6")
    d.rain(450, 210, 5)
    d.person(140, 450, 0.55, mood="smile", shirt=YELLOW)
    d.person(510, 450, 0.55, mood="sad", shirt=BLUE)


@scene(125)
def trophy(d):
    d.rect(0, 0, 640, 480, "#fff6e4")
    d.path("M250 80 H400 V190 Q325 270 250 190 Z", fill="#f0d78c", stroke=INK, sw=5)
    d.ellipse(220, 130, 28, 40, "none", "#e0b44a", 8)
    d.ellipse(430, 130, 28, 40, "none", "#e0b44a", 8)
    d.rect(305, 250, 40, 50, "#e0b44a", INK, 3)
    d.rrect(250, 300, 150, 28, 6, BROWN, INK, 3)
    d.person(140, 450, 0.85, mood="happy", pose="wave", shirt=RED)
    d.person(510, 460, 0.7, mood="sad", pose="sit", shirt=GREY)


@scene(126)
def sharp_knife(d):
    d.rect(0, 0, 640, 480, "#f6f5f2")
    d.ellipse(200, 340, 70, 28, ORANGE, INK, 4)
    d.ellipse(250, 360, 50, 20, ORANGE)
    d.knife(80, 200, 1.35)
    d.poly([(150, 300), (210, 330), (160, 350)], "#f3d2a2", INK, 3)


@scene(127)
def round_ball(d):
    d.rect(0, 0, 640, 480, "#f3f6ff")
    ball(d, 320, 250, 120, ORANGE)
    d.path("M320 70 A180 180 0 0 1 500 250", stroke=BLUE, sw=8)
    d.arrow(480, 210, 530, 270, BLUE, 8)


@scene(128)
def yummy_cake(d):
    d.rect(0, 0, 640, 480, "#fff2f6")
    d.rrect(150, 200, 340, 160, 18, PINK, INK, 5)
    d.rrect(150, 176, 340, 46, 12, WHITE, INK, 4)
    d.circle(420, 250, 36, "#f7f4fb", INK, 3)
    d.rect(300, 120, 10, 60, YELLOW, INK, 3)
    d.ellipse(305, 112, 16, 22, ORANGE, INK, 3)
    d.heart(110, 120, 20)
    d.heart(520, 140, 16)


@scene(129)
def lifting(d):
    d.outdoor()
    d.person(300, 440, 1.25, mood="confident", pose="carry", shirt=GREEN)
    d.rrect(220, 70, 170, 110, 12, BROWN, INK, 5)
    d.check(500, 140, 1.4)


@scene(130)
def giving_gift(d):
    d.outdoor()
    d.person(180, 430, 1.1, mood="smile", pose="carry", shirt=BLUE)
    d.gift(300, 190, 1.15)
    d.person(500, 430, 1.05, mood="happy", pose="wave", shirt=PINK, hair_style="long", flip=True)


@scene(131)
def providing_tray(d):
    d.indoor(wall="#fff6f0")
    d.person(170, 430, 1.15, mood="smile", shirt=WHITE)
    d.ellipse(360, 230, 110, 20, "#d9dee6", INK, 4)
    d.line([(300, 230), (300, 300)], GREY, 6)
    d.circle(320, 200, 20, "#f2a3b0", INK, 3)
    d.glass_cup(370, 140, "#9fd4ff", 40, 80, level=0.35)
    d.person(520, 440, 0.85, mood="smile", shirt=BLUE, flip=True)


@scene(132)
def cuddling(d):
    d.rect(0, 0, 640, 480, "#fff2f6")
    d.person(250, 440, 1.3, mood="smile", hair_style="long", shirt=PINK, pose="hug")
    d.circle(400, 250, 36, SKIN, INK, 4)
    d.rrect(360, 290, 70, 80, 20, YELLOW, INK, 4)
    d.circle(388, 244, 4, INK)
    d.circle(412, 244, 4, INK)
    d.heart(120, 130, 24)
    d.heart(500, 110, 18)
    d.heart(460, 180, 12)


@scene(133)
def laughing(d):
    face(d, "happy", "#fff6e0", shirt=YELLOW)
    d.path("M120 120 Q150 80 180 130", stroke="#5aa6e6", sw=4)
    d.path("M480 100 Q520 60 530 130", stroke="#5aa6e6", sw=4)


@scene(134)
def soft_pillow(d):
    d.rect(0, 0, 640, 480, "#f4f0ff")
    d.ellipse(320, 280, 220, 120, "#d4c2f2", INK, 6)
    d.ellipse(250, 250, 70, 40, "#c3a8ea", INK, 4)
    d.ellipse(390, 260, 60, 34, "#c3a8ea", INK, 4)
    d.ellipse(280, 245, 50, 18, "rgba(255,255,255,0.75)")
    d.path("M100 190 C170 110 250 200 200 260", fill=SKIN, stroke=INK, sw=16)
    d.path("M140 230 Q200 290 250 250", stroke=INK, sw=5)
    d.sparkles([(120, 120, 8), (520, 140, 10)])


@scene(135)
def writer_desk(d):
    d.indoor(wall="#f4f0ea")
    d.rrect(100, 270, 440, 30, 8, BROWN, INK, 4)
    d.person(260, 420, 1.1, mood="think", pose="read", shirt="#6b8f71")
    d.rrect(380, 170, 120, 90, 6, WHITE, INK, 4)
    d.line([(400, 200), (480, 200)], GREY, 3)
    d.line([(400, 220), (460, 220)], GREY, 3)
    d.line([(450, 140), (500, 240)], YELLOW, 8)


@scene(136)
def zoo_gate(d):
    d.outdoor()
    d.rect(70, 90, 28, 280, BROWN, INK, 4)
    d.rect(530, 90, 28, 280, BROWN, INK, 4)
    d.path("M70 90 Q320 0 558 90", stroke=GREEN, sw=18)
    d.elephant(180, 300, 0.48)
    d.circle(470, 200, 36, YELLOW, INK, 4)
    d.circle(490, 190, 4, INK)
    d.person(340, 430, 0.65, mood="wow")


@scene(137)
def town_street(d):
    d.outdoor(horizon=300)
    for i, color in enumerate((RED, BLUE, GREEN, ORANGE)):
        d.house(100 + i * 145, 360, 0.7, roof=color)
    d.rect(20, 370, 600, 20, "#6b7280", INK, 3)
    d.line([(40, 380), (600, 380)], YELLOW, 4)


@scene(138)
def annoying_bug(d):
    d.outdoor()
    d.person(260, 440, 1.25, mood="angry", shirt=BLUE)
    d.ellipse(470, 160, 28, 16, "#3a322c", INK, 3)
    d.ellipse(455, 145, 18, 8, "rgba(200,220,255,0.8)", INK, 2)
    d.ellipse(490, 148, 16, 7, "rgba(200,220,255,0.8)", INK, 2)
    d.circle(478, 158, 3, WHITE)
    d.path("M430 130 Q400 90 450 70", stroke="#9aa8b8", sw=4)
    d.path("M500 130 Q540 90 510 60", stroke="#9aa8b8", sw=4)
    d.path("M500 200 Q540 230 500 260", stroke="#9aa8b8", sw=3)


@scene(139)
def rising_chart(d):
    d.rect(0, 0, 640, 480, "#f5f9ff")
    d.line([(80, 50), (80, 400), (580, 400)], INK, 5)
    d.path("M120 340 L210 290 L290 300 L380 180 L490 90", stroke=GREEN, sw=10)
    for x, y in ((120, 340), (210, 290), (290, 300), (380, 180), (490, 90)):
        d.circle(x, y, 10, GREEN, INK, 3)
    d.arrow(510, 110, 560, 50, GREEN, 10)


@scene(140)
def dying_plant(d):
    d.indoor()
    d.path("M220 390 L270 300 L380 390 Z", fill="#c9854a", stroke=INK, sw=5)
    d.path("M310 300 Q360 220 300 140", stroke="#8a7a62", sw=8)
    d.ellipse(340, 150, 36, 16, "#b7a48a", INK, 3)
    d.ellipse(250, 230, 28, 12, "#a89078", INK, 3)
    d.ellipse(400, 250, 22, 10, "#c4b49a", INK, 2)
    d.arrow(460, 180, 460, 280, GREY, 6)


@scene(141)
def tiny_ant(d):
    d.rect(0, 0, 640, 480, "#f6f4f1")
    d.circle(230, 250, 110, "#e0b44a", INK, 6)
    d.circle(230, 250, 82, "#f0d78c", INK, 4)
    d.rect(210, 160, 40, 18, "#e0b44a", INK, 3)
    d.ant(500, 270, 0.85)


@scene(142)
def multitool(d):
    d.rect(0, 0, 640, 480, "#f3f6fb")
    d.rrect(230, 200, 160, 48, 12, RED, INK, 5)
    d.poly([(140, 224), (230, 200), (230, 248)], "#d9dee6", INK, 4)
    d.line([(390, 224), (530, 120)], "#d5dee6", 10)
    d.line([(390, 224), (540, 280)], BROWN, 8)
    d.circle(530, 300, 22, "none", INK, 6)
    d.poly([(500, 100), (540, 130), (520, 140)], "#d9dee6", INK, 3)


@scene(143)
def shy_child(d):
    d.indoor(wall="#fff3f7")
    d.rect(400, 30, 50, 420, "#e7d3b0", INK, 4)
    d.person(300, 440, 1.15, mood="shy", hair_style="long", shirt=PINK)
    d.circle(200, 200, 22, PINK, opacity=0.75)
    d.circle(160, 250, 14, PINK, opacity=0.6)


@scene(144)
def graduation(d):
    d.outdoor()
    d.person(300, 440, 1.3, mood="smile", shirt=NAVY)
    hx, hy = world(300, 440, 1.3, HEAD)
    d.poly([(hx - 60, hy - 36), (hx, hy - 70), (hx + 60, hy - 36), (hx, hy - 8)], "#1b1e26", INK, 4)
    d.line([(hx + 48, hy - 36), (hx + 70, hy + 10)], YELLOW, 4)
    d.circle(hx + 70, hy + 14, 6, YELLOW, INK, 2)
    d.bulb(500, 130, 1.1)


@scene(145)
def strange_door(d):
    d.rect(0, 0, 640, 480, "#e6e3f4")
    d.path("M200 440 L170 90 Q320 10 470 110 L440 440 Z", fill="#6b5b95", stroke=INK, sw=6)
    d.circle(320, 200, 40, YELLOW, INK, 5)
    d.circle(306, 192, 7, INK)
    d.circle(334, 192, 7, INK)
    d.ellipse(320, 230, 16, 10, INK)
    d.circle(320, 340, 12, "#e0b44a", INK, 3)
    d.glyph("?", 520, 70, 56, PURPLE)


@scene(146)
def calendar_week(d):
    d.rect(0, 0, 640, 480, "#f3f7fc")
    d.zh("一星期", 320, 36, 40, BLUE_DARK)
    d.calendar_base(30, 90, 580, 230)
    d.week_cells(50, 170, 540, marks=["一", "二", "三", "四", "五", "六", "日"])
    d.path("M70 430 Q320 300 570 430", stroke=BLUE, sw=8)


@scene(147)
def weekend_days(d):
    d.rect(0, 0, 640, 480, "#fff6e4")
    d.calendar_base(30, 40, 580, 210)
    d.week_cells(50, 120, 540, marks=["一", "二", "三", "四", "五", "六", "日"])
    d.rrect(50 + 5 * ((540 - 48) / 7 + 8), 120, 78, 64, 8, "#ffe08a", ORANGE, 4)
    ball(d, 180, 380, 48, ORANGE)
    d.sun(470, 370, 46, face=True)


@scene(148)
def calendar_year(d):
    d.rect(0, 0, 640, 480, "#f5f9ff")
    d.zh("一年", 320, 28, 40, BLUE_DARK)
    for i in range(12):
        x = 36 + (i % 4) * 152
        y = 100 + (i // 4) * 120
        d.rrect(x, y, 136, 100, 10, WHITE, INK, 3)
        d.rect(x, y, 136, 24, RED)
        d.glyph(str(i + 1), x + 68, y + 40, 28, BLUE)


@scene(149)
def small_pond(d):
    d.outdoor()
    d.ellipse(320, 320, 200, 80, "#3aa0a8", INK, 5)
    d.ellipse(270, 300, 40, 16, GREEN, INK, 3)
    d.circle(400, 330, 22, GREEN, INK, 3)
    d.circle(392, 324, 4, INK)
    d.circle(408, 324, 4, WHITE)
    d.flower(100, 370, PINK, 0.75)
    d.circle(180, 300, 8, WHITE)


@scene(150)
def swimming_pool(d):
    d.rect(0, 0, 640, 480, "#e5f6ff")
    d.rrect(70, 70, 500, 320, 24, "#3d98e0", INK, 6)
    for x in (180, 310, 440):
        d.line([(x, 90), (x, 370)], WHITE, 4)
    d.line([(100, 220), (150, 140)], "#d9dee6", 8)
    d.circle(150, 140, 10, "#d9dee6", INK, 3)
    d.ellipse(500, 250, 36, 14, SKIN, INK, 3)


@scene(151)
def tangled_knot(d):
    d.rect(0, 0, 640, 480, "#fff6ea")
    d.path("M70 150 C220 20 160 340 320 190 C480 40 360 420 570 170", stroke=ORANGE, sw=18)
    d.path("M110 330 C270 470 420 40 530 350", stroke=BLUE, sw=14)
    d.path("M180 200 C260 260 300 120 400 240", stroke=RED, sw=10)
    d.circle(300, 230, 18, YELLOW, INK, 4)
    d.glyph("?", 320, 36, 48, RED)
    d.person(90, 450, 0.45, mood="think", shirt=BLUE)


@scene(152)
def tree_rings(d):
    d.rect(0, 0, 640, 480, "#f6f1e8")
    d.tree(120, 400, 0.55, "#8fb86a")
    d.arrow(180, 300, 230, 260, GREY, 6)
    d.rrect(250, 300, 18, 120, 6, BROWN, INK, 3)
    d.path("M259 180 Q300 120 280 220", stroke=BROWN, sw=8)
    d.circle(300, 140, 36, "#6a8f55", INK, 3)
    for i, r in enumerate((70, 52, 34, 16)):
        d.circle(480, 250, r, "none", BROWN if i % 2 == 0 else "#e0b44a", 7)


@scene(153)
def mirage(d):
    d.rect(0, 0, 640, 300, "#f6e2b8")
    d.rect(0, 300, 640, 180, "#e7c98a")
    d.sun(80, 80, 36, face=True)
    d.path("M40 250 Q200 230 320 250 T600 250", stroke="rgba(255,255,255,0.85)", sw=8)
    d.tree(420, 250, 0.7, "rgba(46,154,92,0.35)")
    d.person(160, 430, 0.9, mood="think", pose="think", shirt=ORANGE)
    d.path("M200 160 Q230 140 220 180", stroke=INK, sw=3)


@scene(154)
def sudden_burst(d):
    d.rect(0, 0, 640, 480, "#fff6e4")
    d.circle(300, 250, 50, PINK, INK, 4)
    d.path("M250 250 Q200 180 160 220", stroke=PINK, sw=6)
    d.path("M350 240 Q420 180 450 230", stroke=PINK, sw=6)
    d.star(320, 200, 70, YELLOW)
    for ang in range(0, 360, 30):
        rad = math.radians(ang)
        d.line([
            (320 + math.cos(rad) * 90, 210 + math.sin(rad) * 90),
            (320 + math.cos(rad) * 150, 210 + math.sin(rad) * 150),
        ], ORANGE, 6)
    d.glyph("!", 320, 175, 40, RED)


@scene(155)
def closed_door(d):
    d.indoor()
    d.door(200, 440, 240, 340, open_=False)
    d.path("M160 200 C200 160 230 200 210 240", stroke=SKIN, sw=16)
    d.circle(230, 220, 14, SKIN, INK, 3)
    d.arrow(120, 160, 190, 200, BLUE, 6)


@scene(156)
def storage_shelves(d):
    d.indoor(wall="#f4efe6")
    d.rect(60, 60, 18, 360, BROWN, INK, 3)
    d.rect(560, 60, 18, 360, BROWN, INK, 3)
    colors = (BLUE, GREEN, ORANGE, RED, PURPLE, TEAL)
    for row, y in enumerate((140, 260, 380)):
        d.rect(60, y, 516, 18, BROWN, INK, 4)
        for i in range(4):
            d.rrect(100 + i * 120, y - 70, 80, 70, 8, colors[(row + i) % 6], INK, 3)


@scene(157)
def certain_check(d):
    d.rect(0, 0, 640, 480, "#e7f8ee")
    d.rrect(160, 60, 320, 360, 16, WHITE, INK, 5)
    for i, w in enumerate((220, 180, 200)):
        d.rect(200, 100 + i * 36, w, 12, GREY)
    d.circle(320, 280, 90, WHITE, GREEN, 12)
    d.check(320, 280, 2.2, GREEN)


@scene(158)
def overlapping_circles(d):
    d.outdoor()
    d.person(180, 420, 0.95, mood="smile", shirt=BLUE)
    d.person(460, 420, 0.95, mood="smile", shirt=GREEN, flip=True)
    ball(d, 320, 230, 36, RED)
    d.line([(230, 250), (290, 230)], INK, 4)
    d.line([(410, 250), (350, 230)], INK, 4)


@scene(159)
def finish_flag(d):
    d.outdoor()
    d.rect(450, 70, 14, 320, INK)
    d.rrect(180, 70, 270, 140, 8, WHITE, INK, 4)
    for i in range(5):
        for j in range(4):
            if (i + j) % 2 == 0:
                d.rect(190 + i * 50, 80 + j * 30, 50, 30, INK)
    d.person(140, 430, 0.9, mood="happy", pose="run", shirt=RED)


@scene(160)
def important_key(d):
    d.rect(0, 0, 640, 480, "#fff6e4")
    d.circle(200, 220, 70, "#f0d78c", INK, 6)
    d.circle(200, 220, 28, "#fff6e4", INK, 5)
    d.rect(260, 200, 220, 36, "#f0d78c", INK, 5)
    d.rect(400, 236, 24, 46, "#f0d78c", INK, 4)
    d.rect(450, 236, 24, 32, "#f0d78c", INK, 4)
    d.star(520, 100, 32)
    d.glyph("!", 120, 80, 48, RED)


@scene(161)
def nodding_sure(d):
    d.outdoor()
    d.person(280, 440, 1.35, mood="confident", shirt=GREEN)
    d.check(500, 140, 1.8)
    d.arrow(430, 240, 390, 180, GREEN, 7)


@scene(162)
def hammer_wrench(d):
    d.rect(0, 0, 640, 480, "#f3f6fb")
    d.rect(120, 160, 220, 36, BROWN, INK, 5)
    d.rrect(310, 120, 110, 120, 10, "#9aa8b8", INK, 5)
    d.path("M140 340 Q250 240 380 360", stroke="#7f8ea3", sw=16)
    d.circle(380, 360, 28, "none", INK, 8)
    d.rrect(400, 300, 70, 22, 6, "#9aa8b8", INK, 3)


@scene(163)
def unit_blocks(d):
    d.rect(0, 0, 640, 480, "#f5f9ff")
    colors = (BLUE, GREEN, ORANGE, PURPLE)
    for i, color in enumerate(colors):
        d.rrect(70 + i * 145, 200, 120, 120, 12, color, INK, 5)
    d.line([(70, 150), (190, 150)], RED, 6)
    d.line([(70, 136), (70, 164)], RED, 5)
    d.line([(190, 136), (190, 164)], RED, 5)
    d.glyph("1", 130, 90, 40, RED)


@scene(164)
def voice_waves(d):
    d.rect(0, 0, 640, 480, "#f5f9ff")
    d.ellipse(190, 250, 90, 50, SKIN, INK, 5)
    d.path("M140 250 Q190 320 240 250", fill="#e86b7a", stroke=INK, sw=4)
    for i, rx in enumerate((50, 90, 130)):
        d.path(
            f"M{n(300)} {n(250 - rx * 0.7)} A {n(rx)} {n(rx * 0.7)} 0 0 1 {n(300)} {n(250 + rx * 0.7)}",
            stroke=BLUE, sw=7,
        )


@scene(165)
def running_action(d):
    d.outdoor()
    d.person(320, 430, 1.4, mood="happy", pose="run", shirt=RED)
    d.speed_lines(30, 180)
    d.speed_lines(50, 240)
    d.speed_lines(40, 300)


@scene(166)
def tied_knot(d):
    d.rect(0, 0, 640, 480, "#fff6ea")
    d.rrect(180, 140, 280, 200, 16, "#e0b44a", INK, 5)
    d.path("M80 240 C160 80 200 400 320 240 C440 80 480 400 560 240", stroke=BROWN, sw=14)
    d.circle(320, 230, 26, "none", BROWN, 10)
    d.line([(250, 140), (250, 340)], BROWN, 6)
    d.line([(390, 140), (390, 340)], BROWN, 6)


@scene(167)
def improvement(d):
    d.rect(0, 0, 640, 480, "#f3faf5")
    d.flower(140, 320, "#b7a48a", 0.85)
    d.path("M110 250 Q140 300 160 270", stroke="#8a7a62", sw=4)
    d.arrow(230, 260, 390, 180, GREEN, 12)
    d.flower(510, 300, PINK, 1.25)
    d.sparkles([(470, 160, 8), (560, 180, 8)])


@scene(168)
def broom_clear(d):
    d.indoor(floor="#e7d8c4")
    d.line([(160, 60), (280, 340)], BROWN, 10)
    d.poly([(220, 310), (360, 300), (340, 400), (190, 390)], "#e0b44a", INK, 5)
    d.ellipse(480, 380, 80, 26, "#c4b49a")
    d.circle(440, 350, 14, "#a89078", INK, 3)
    d.circle(500, 360, 16, "#8a7a62", INK, 3)
    d.rrect(430, 300, 40, 30, 4, GREY, INK, 3)
    d.arrow(360, 180, 450, 280, "#9aa8b8", 6)


@scene(169)
def thumbs_down(d):
    d.rect(0, 0, 640, 480, "#ffecec")
    d.thumb(300, 120, up=False, sc=2.6)
    d.circle(500, 160, 40, RED, INK, 4)
    d.line([(484, 144), (516, 176)], WHITE, 6)
    d.line([(516, 144), (484, 176)], WHITE, 6)


@scene(170)
def different_shapes(d):
    d.rect(0, 0, 640, 480, "#f5f9ff")
    d.circle(150, 250, 90, BLUE, INK, 6)
    d.poly([(430, 90), (590, 400), (280, 400)], ORANGE, INK, 6)
    d.line([(280, 70), (340, 20)], RED, 8)
    d.line([(280, 20), (340, 70)], RED, 8)
    d.rrect(40, 40, 70, 70, 10, GREEN, INK, 4)


def _icon_bag(d):
    d.rrect(270, 330, 100, 110, 16, BLUE, INK, 4)
    d.path("M290 345 Q320 290 350 345", stroke=INK, sw=5)
    d.rect(292, 370, 56, 16, YELLOW)


def _icon_music(d):
    d.circle(280, 390, 18, INK)
    d.circle(360, 400, 18, INK)
    d.line([(296, 384), (296, 310)], INK, 6)
    d.line([(376, 394), (376, 320)], INK, 6)
    d.line([(296, 310), (376, 320)], INK, 6)


def _icon_palette(d):
    d.ellipse(320, 380, 70, 48, WHITE, INK, 4)
    d.circle(350, 390, 14, "#f4f7fb", INK, 3)
    for i, color in enumerate((RED, YELLOW, BLUE, GREEN)):
        d.circle(270 + i * 28, 360, 10, color, INK, 2)


def _icon_book(d):
    d.book(340, 320, 1.2, open_=False)


def _icon_star(d):
    d.star(320, 390, 52)


def _icon_ball(d):
    ball(d, 320, 390, 52, ORANGE)


def _icon_sun(d):
    d.sun(320, 390, 48, face=True)


@scene(171)
def monday(d):
    weekday(d, 0, _icon_bag)


@scene(172)
def tuesday(d):
    weekday(d, 1, _icon_music)


@scene(173)
def wednesday(d):
    weekday(d, 2, _icon_palette)


@scene(174)
def thursday(d):
    weekday(d, 3, _icon_book)


@scene(175)
def friday(d):
    weekday(d, 4, _icon_star)


@scene(176)
def saturday(d):
    weekday(d, 5, _icon_ball)


@scene(177)
def sunday(d):
    weekday(d, 6, _icon_sun)


@scene(178)
def one_month(d):
    d.rect(0, 0, 640, 480, "#f5f9ff")
    d.calendar_base(70, 24, 500, 430)
    d.zh("月", 320, 70, 40, WHITE)
    for r in range(5):
        for c in range(7):
            d.rrect(96 + c * 66, 170 + r * 52, 52, 40, 6, "#f4f7fb", INK, 2)
    d.rrect(96, 170, 52, 40, 6, "#e5f8ee", GREEN, 3)


def _month(name, tint, icon):
    def paint(drawing):
        month_card(drawing, name, icon, tint)
    return paint


def _snow(d):
    d.circle(320, 310, 56, WHITE, INK, 4)
    d.circle(270, 350, 40, WHITE, INK, 4)
    d.circle(380, 355, 34, WHITE, INK, 4)
    d.snowflake(150, 260, 14)
    d.snowflake(500, 250, 16)
    d.snowflake(200, 400, 10)


def _hearts(d):
    d.heart(320, 320, 56, RED)
    d.heart(180, 260, 24, PINK)
    d.heart(470, 270, 22, PINK)


def _wind(d):
    for y in (250, 310, 370):
        d.path(f"M100 {y} Q240 {y - 36} 360 {y} T560 {y}", stroke=BLUE, sw=8)
    d.ellipse(200, 280, 20, 10, GREEN, INK, 2)


def _april_rain(d):
    d.cloud(300, 240, 1.7, "#d5e4f5")
    d.rain(210, 290, 7)
    d.umbrella(340, 360, 0.85)


def _may_flowers(d):
    for i, color in enumerate((PINK, RED, YELLOW, PURPLE, WHITE)):
        d.flower(100 + i * 110, 360, color, 0.9)


def _june_sun(d):
    d.sun(320, 330, 80, face=True)


def _july_fire(d):
    d.star(200, 300, 36, RED)
    d.star(320, 250, 48, YELLOW)
    d.star(450, 310, 32, BLUE)
    d.line([(320, 310), (320, 420)], BROWN, 4)
    d.circle(250, 360, 6, ORANGE)
    d.circle(400, 370, 6, PINK)


def _august_beach(d):
    d.ellipse(320, 390, 240, 46, "#f0d78c")
    d.umbrella(230, 320, 0.85)
    d.sun(500, 250, 40, face=True)
    d.path("M0 400 Q160 370 320 400 T640 400", stroke="#4aa3e8", sw=8)


def _sept_leaves(d):
    for i, color in enumerate((ORANGE, RED, YELLOW, BROWN, "#e07a3d")):
        d.ellipse(110 + i * 100, 320, 42, 22, color, INK, 3)
        d.line([(110 + i * 100, 330), (120 + i * 100, 360)], BROWN, 3)


def _oct_pumpkin(d):
    d.ellipse(320, 340, 110, 84, ORANGE, INK, 6)
    d.rect(304, 250, 32, 28, GREEN_DARK, INK, 3)
    d.line([(280, 310), (360, 310)], "#d64545", 4)
    d.line([(280, 345), (360, 345)], "#d64545", 4)
    d.poly([(320, 250), (300, 230), (330, 240)], GREEN, INK, 2)


def _nov_bird(d):
    d.ellipse(300, 340, 110, 70, BROWN, INK, 5)
    d.circle(400, 290, 36, BROWN, INK, 4)
    d.poly([(430, 290), (480, 300), (428, 314)], ORANGE, INK, 3)
    d.circle(412, 282, 4, INK)
    d.ellipse(230, 320, 50, 18, "#8a5a3b", INK, 3)
    d.line([(250, 400), (280, 370)], BROWN, 4)
    d.line([(340, 400), (330, 370)], BROWN, 4)


def _dec_tree(d):
    d.pine(320, 430, 1.45)
    d.circle(290, 250, 10, RED, INK, 2)
    d.circle(350, 290, 10, YELLOW, INK, 2)
    d.circle(310, 340, 10, BLUE, INK, 2)
    d.star(320, 175, 16)


SCENES_MONTHS = {
    179: ("一月", "#e7f4ff", _snow),
    180: ("二月", "#fff0f4", _hearts),
    181: ("三月", "#e7f6ff", _wind),
    182: ("四月", "#e7f2fb", _april_rain),
    183: ("五月", "#f3faf3", _may_flowers),
    184: ("六月", "#fff6e4", _june_sun),
    185: ("七月", "#1d2a44", _july_fire),
    186: ("八月", "#fff3d2", _august_beach),
    187: ("九月", "#fff1e4", _sept_leaves),
    188: ("十月", "#fff3e6", _oct_pumpkin),
    189: ("十一月", "#f6f1e8", _nov_bird),
    190: ("十二月", "#e7f6ee", _dec_tree),
}
for _num, _args in SCENES_MONTHS.items():
    scene(_num)(_month(*_args))


@scene(191)
def ironing_shirt(d):
    d.indoor()
    d.person(150, 430, 1.0, mood="smile", pose="push", shirt=BLUE)
    d.path("M200 250 L250 200 L520 200 L560 260 Z", fill="#d9dee6", stroke=INK, sw=5)
    d.line([(360, 260), (360, 420)], GREY, 10)
    d.rrect(250, 210, 180, 36, 8, "#7eb6ef", INK, 3)
    d.iron(300, 120, 1.15)
    d.steam(420, 150, 3)


@scene(192)
def joining_group(d):
    d.outdoor()
    for i, x in enumerate((140, 250, 360)):
        d.person(x, 410, 0.78, mood="smile", shirt=BLUE)
    d.person(540, 430, 0.85, mood="happy", pose="run", shirt=ORANGE)
    d.arrow(470, 240, 400, 240, GREEN, 8)


@scene(193)
def making_craft(d):
    d.indoor(wall="#fff6f0")
    d.rrect(140, 280, 380, 26, 8, BROWN, INK, 4)
    d.rrect(200, 160, 110, 100, 8, PINK, INK, 4)
    d.rrect(340, 170, 100, 90, 8, YELLOW, INK, 4)
    d.path("M90 240 C170 150 230 200 280 190", stroke=SKIN, sw=16)
    d.circle(270, 180, 14, SKIN, INK, 3)
    d.line([(460, 130), (520, 220)], "#c5ced8", 8)


@scene(194)
def planting(d):
    d.outdoor(ground="#8a5a3b", horizon=280)
    d.person(160, 420, 1.05, mood="smile", pose="push", shirt=GREEN)
    d.ellipse(450, 360, 90, 28, "#6b4428")
    d.rrect(440, 230, 16, 120, 6, GREEN_DARK)
    d.ellipse(424, 230, 28, 14, GREEN, INK, 3)
    d.ellipse(470, 224, 28, 14, GREEN, INK, 3)
    d.circle(400, 300, 10, "#6b4428")


@scene(195)
def reaching(d):
    d.outdoor()
    d.path("M40 400 Q200 360 340 300 T560 200", stroke="#e0b44a", sw=8)
    d.person(160, 430, 1.1, mood="smile", pose="point", shirt=BLUE)
    d.star(540, 150, 40)
    d.circle(540, 220, 10, RED, INK, 3)
    d.arrow(280, 220, 470, 170, ORANGE, 7)


@scene(196)
def crying_face(d):
    face(d, "cry", "#e5f1fb", shirt=BLUE)


@scene(197)
def flexing(d):
    d.rect(0, 0, 640, 480, "#fff2e8")
    d.person(300, 455, 1.4, mood="confident", pose="flex", shirt=RED)
    d.circle(150, 200, 36, SKIN, INK, 5)
    d.path("M120 190 Q150 150 180 190", stroke=SKIN, sw=10)
    d.sparkles([(100, 120, 10), (520, 130, 12)])


@scene(198)
def apology_bow(d):
    d.indoor()
    with d.g("translate(340 440) rotate(20)"):
        d.person(0, 0, 1.25, mood="sad", pose="bow", shirt=BLUE)
    d.heart(120, 120, 22, PINK)
    d.person(140, 450, 0.6, mood="smile", shirt=GREEN)


@scene(199)
def short_and_tall(d):
    d.outdoor()
    d.person(170, 440, 0.62, mood="smile", shirt=ORANGE)
    d.person(430, 430, 1.35, mood="smile", shirt=BLUE)
    d.line([(90, 160), (90, 440)], GREY, 4)
    d.line([(70, 300), (110, 300)], RED, 5)
    d.line([(500, 80), (500, 430)], GREY, 4)
    d.line([(480, 160), (520, 160)], BLUE, 5)


@scene(200)
def empty_gauge(d):
    d.rect(0, 0, 640, 480, "#f6f4f1")
    d.rrect(160, 60, 320, 200, 20, "#2c3e50", INK, 5)
    d.path("M200 300 A140 140 0 0 1 440 300", stroke=GREY, sw=22)
    d.path("M200 300 A140 140 0 0 1 250 190", stroke=RED, sw=22)
    d.line([(320, 300), (230, 190)], INK, 8)
    d.circle(320, 300, 16, YELLOW, INK, 3)
    d.glyph("0", 180, 340, 36, RED)
    d.rrect(250, 380, 140, 36, 8, RED, INK, 3)


@scene(201)
def eagle_bird(d):
    d.rect(0, 0, 640, 480, "#d4efff")
    d.cloud(90, 80, 0.9)
    d.cloud(520, 120, 0.7)
    d.eagle(320, 260, 1.25)
    d.sun(540, 60, 28)


@scene(202)
def fact_document(d):
    d.rect(0, 0, 640, 480, "#f5f9ff")
    d.rrect(150, 40, 340, 400, 14, WHITE, INK, 5)
    d.rect(180, 70, 120, 80, "#d7e6f5", INK, 3)
    d.circle(230, 105, 16, YELLOW, INK, 2)
    for i, w in enumerate((240, 200, 220, 160)):
        d.rect(190, 180 + i * 36, w, 14, GREY)
    d.circle(320, 360, 36, "none", BLUE, 6)
    d.check(320, 360, 0.9)


@scene(203)
def farmer(d):
    d.outdoor()
    d.person(280, 440, 1.25, mood="smile", shirt="#2e9a5c", pants=BROWN)
    hx, hy = world(280, 440, 1.25, HEAD)
    d.ellipse(hx, hy - 40, 70, 16, "#f0d78c", INK, 3)
    d.ellipse(hx, hy - 52, 40, 10, "#e0b44a")
    d.line([(450, 150), (500, 380)], BROWN, 8)
    d.line([(470, 160), (540, 190)], "#c5ced8", 8)
    d.line([(470, 175), (530, 205)], "#c5ced8", 6)


@scene(204)
def piggy_bank(d):
    d.rect(0, 0, 640, 480, "#ffeef3")
    d.ellipse(320, 270, 160, 100, PINK, INK, 6)
    d.circle(450, 230, 36, PINK, INK, 4)
    d.circle(462, 222, 5, INK)
    d.ellipse(230, 260, 26, 16, PINK, INK, 3)
    d.rect(290, 180, 50, 14, INK)
    d.circle(160, 140, 28, "#f0d78c", INK, 4)
    d.arrow(180, 165, 270, 210, ORANGE, 6)
    d.rrect(250, 360, 30, 24, 6, PINK, INK, 3)
    d.rrect(360, 360, 30, 24, 6, PINK, INK, 3)


@scene(205)
def sending_envelope(d):
    d.rect(0, 0, 640, 480, "#f3f6ff")
    d.rrect(140, 160, 280, 180, 10, WHITE, INK, 5)
    d.poly([(140, 160), (280, 270), (420, 160)], "none", INK, 5)
    d.arrow(450, 250, 590, 140, BLUE, 10)
    d.path("M500 180 Q540 140 560 190", stroke="#9fd4ff", sw=4)


@scene(206)
def teaching(d):
    d.indoor(wall="#f4f8ff")
    d.rrect(40, 50, 280, 200, 10, "#243044", INK, 5)
    d.circle(120, 130, 30, WHITE, INK, 3)
    d.poly([(190, 180), (250, 90), (280, 190)], YELLOW, INK, 3)
    d.person(460, 420, 1.05, mood="smile", pose="point", shirt=TEAL)
    d.circle(160, 380, 26, SKIN, INK, 3)
    d.circle(230, 400, 26, SKIN, INK, 3)
    d.rrect(140, 400, 40, 30, 6, BLUE, INK, 2)
    d.rrect(210, 420, 40, 30, 6, GREEN, INK, 2)


@scene(207)
def understanding(d):
    d.rect(0, 0, 640, 480, "#fffbe8")
    d.path("M80 300 C160 180 200 340 280 220", stroke=GREY, sw=8)
    d.arrow(300, 240, 380, 200, GREEN, 8)
    d.line([(400, 220), (520, 220)], GREEN, 8)
    d.bulb(460, 120, 1.5, on=True)
    d.person(160, 450, 0.7, mood="wow", pose="wave")


@scene(208)
def open_gate(d):
    d.outdoor()
    d.rect(80, 120, 20, 280, BROWN, INK, 4)
    d.rect(220, 120, 20, 280, BROWN, INK, 4)
    d.rrect(220, 150, 140, 200, 8, "#c9854a", INK, 4)
    d.person(460, 430, 1.0, mood="smile", pose="run", shirt=GREEN)
    d.arrow(300, 70, 430, 70, GREEN, 8)


@scene(209)
def listening_ear(d):
    d.rect(0, 0, 640, 480, "#f5f9ff")
    d.ear_icon(230, 250, 1.8)
    for rx in (36, 64, 92):
        d.path(
            f"M{n(430)} {n(220 - rx)} A {n(rx)} {n(rx)} 0 0 1 {n(430)} {n(220 + rx)}",
            stroke=BLUE, sw=7,
        )


@scene(210)
def shiny_new(d):
    d.rect(0, 0, 640, 480, "#f4f8ff")
    d.rrect(170, 160, 280, 200, 18, WHITE, INK, 6)
    d.star(320, 110, 42)
    d.sparkles([(120, 120, 14), (530, 140, 14), (100, 320, 10), (540, 340, 12)])
    d.poly([(360, 150), (430, 190), (400, 210), (450, 250), (360, 220)], YELLOW, INK, 3)


@scene(211)
def left_arrow(d):
    d.rect(0, 0, 640, 480, "#f2f6ff")
    d.arrow(540, 220, 80, 220, BLUE, 20)
    d.person(500, 420, 0.7, mood="smile", pose="point", flip=True)


@scene(212)
def passport_stamps(d):
    d.rect(0, 0, 640, 480, "#f3f6fb")
    d.rrect(170, 40, 300, 400, 16, "#7d3c4a", INK, 6)
    d.rrect(195, 80, 250, 320, 10, CREAM, INK, 4)
    d.circle(270, 170, 36, "none", BLUE, 5)
    d.rect(340, 150, 60, 44, "none", RED, 5)
    d.poly([(280, 260), (340, 230), (350, 300)], "none", GREEN, 5)
    d.circle(400, 300, 26, "none", ORANGE, 5)
    d.ellipse(300, 340, 40, 22, "none", PURPLE, 4)


@scene(213)
def ice_cubes(d):
    d.rect(0, 0, 640, 480, "#e4f5ff")
    d.rrect(140, 120, 150, 150, 16, "rgba(186,224,255,0.9)", INK, 5)
    d.rrect(280, 180, 150, 150, 16, "rgba(255,255,255,0.95)", BLUE, 5)
    d.rrect(220, 250, 120, 120, 14, "rgba(210,236,255,0.9)", INK, 4)
    d.line([(160, 150), (250, 230)], WHITE, 6)
    d.line([(310, 210), (390, 290)], WHITE, 6)
    d.sparkles([(120, 90, 8), (500, 120, 10)])


@scene(214)
def shopping_cart(d):
    d.rect(0, 0, 640, 480, "#f5f9ff")
    d.path("M140 120 H340 L390 320 H190 Z", fill="#e7eef6", stroke=INK, sw=6)
    d.line([(340, 150), (460, 90)], INK, 8)
    d.line([(430, 90), (480, 90)], INK, 8)
    d.circle(230, 360, 28, NAVY, INK, 4)
    d.circle(350, 360, 28, NAVY, INK, 4)
    d.circle(230, 200, 22, RED, INK, 3)
    d.circle(290, 210, 18, GREEN, INK, 3)
    d.rrect(250, 240, 40, 30, 6, YELLOW, INK, 3)


@scene(215)
def looking_eye(d):
    d.rect(0, 0, 640, 480, "#f4f8ff")
    d.eye_icon(280, 240, 2.15)
    d.flower(520, 250, PINK, 0.7)
    d.arrow(400, 180, 470, 210, BLUE, 5)


@scene(216)
def free_tag(d):
    d.rect(0, 0, 640, 480, "#e7f8ee")
    d.poly([(200, 70), (480, 70), (440, 230), (160, 230)], WHITE, INK, 5)
    d.circle(230, 140, 16, "#e7f8ee", INK, 4)
    d.line([(250, 150), (400, 110)], GREY, 4)
    d.glyph("0", 340, 120, 72, GREEN)
    d.zh("免費", 320, 175, 36, GREEN_DARK)
    d.gift(320, 370, 1.05)


@scene(217)
def spirit_level(d):
    d.rect(0, 0, 640, 480, "#f3f6fb")
    d.line([(40, 280), (600, 280)], GREEN, 4)
    d.rrect(40, 180, 560, 80, 24, "#f0d78c", INK, 6)
    d.rrect(230, 196, 180, 48, 22, "#e5f6ff", INK, 4)
    d.circle(320, 220, 16, GREEN, INK, 3)
    d.line([(80, 206), (80, 234)], INK, 3)
    d.line([(560, 206), (560, 234)], INK, 3)


@scene(218)
def child_playing(d):
    d.outdoor()
    d.sun(80, 70, 36, face=True)
    d.person(240, 430, 0.9, mood="happy", pose="run", shirt=ORANGE)
    ball(d, 450, 300, 42, RED)
    d.rrect(500, 180, 16, 160, 6, BROWN)
    d.path("M516 180 Q580 220 516 260", stroke=YELLOW, sw=6)


@scene(219)
def leader_group(d):
    d.outdoor()
    d.person(150, 420, 1.15, mood="confident", pose="point", shirt=RED)
    d.rect(120, 130, 10, 90, BROWN, INK, 3)
    d.poly([(130, 130), (210, 150), (130, 172)], YELLOW, INK, 3)
    d.person(340, 440, 0.75, mood="smile", shirt=BLUE)
    d.person(450, 450, 0.7, mood="smile", shirt=GREEN)
    d.person(550, 440, 0.65, mood="smile", shirt=ORANGE)


@scene(220)
def quality_meter(d):
    d.rect(0, 0, 640, 480, "#f5f9ff")
    d.rrect(120, 80, 400, 300, 20, WHITE, INK, 5)
    for i in range(5):
        d.star(180 + i * 70, 150, 22, YELLOW if i < 4 else GREY)
    d.rrect(180, 220, 280, 36, 12, "#e7eef6", INK, 3)
    d.rect(180, 220, 220, 36, GREEN)
    d.line([(400, 200), (400, 270)], INK, 4)
    d.circle(320, 330, 28, GREEN, INK, 4)
    d.check(320, 330, 0.7)


@scene(221)
def setting_pot(d):
    d.indoor()
    d.rrect(100, 300, 440, 28, 8, BROWN, INK, 4)
    d.path("M300 290 L270 180 L450 180 L420 290 Z", fill="#c9854a", stroke=INK, sw=5)
    d.flower(360, 140, PINK, 0.85)
    d.path("M80 220 C160 120 240 180 290 190", stroke=SKIN, sw=16)
    d.circle(280, 180, 16, SKIN, INK, 3)
    d.arrow(120, 100, 200, 150, BLUE, 6)


@scene(222)
def spelling_tiles(d):
    d.rect(0, 0, 640, 480, "#fff6e4")
    letters = ("A", "B", "C")
    colors = (RED, BLUE, GREEN)
    for i, letter in enumerate(letters):
        x = 70 + i * 150
        d.rrect(x, 250, 120, 50, 8, "#efe6d4", INK, 3)
        d.rrect(x, 150, 120, 120, 14, colors[i], INK, 5)
        d.glyph(letter, x + 60, 185, 52, WHITE)
    d.line([(140, 400), (470, 330)], YELLOW, 10)
    d.poly([(470, 330), (455, 318), (460, 348)], "#e0b44a", INK, 3)
