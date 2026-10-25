"""Flat drawing helpers for original vocab illustrations (CC0).

Coordinates are SVG user space, 640×480, y downward. Scenes compose these
helpers; they never embed the English answer.
"""

import html
import math
from contextlib import contextmanager

INK = "#243044"
WHITE = "#ffffff"
SKIN = "#f6c7a1"
SKIN_DEEP = "#e8b48a"
HAIR = "#3a322c"
HAIR_GREY = "#d5dbe3"
SKY = "#d7f0ff"
GRASS = "#7dce6a"
GRASS_DARK = "#5eae4e"
BLUE = "#4c8dff"
BLUE_DARK = "#2f6fe0"
RED = "#ef5b5b"
RED_DARK = "#d64545"
YELLOW = "#ffd34d"
ORANGE = "#f5a524"
GREEN = "#3cb371"
GREEN_DARK = "#2e9a5c"
PURPLE = "#7d5cc7"
PINK = "#ff8fab"
BROWN = "#8a5a3b"
CREAM = "#fff6e4"
NAVY = "#2c3e50"
GREY = "#c5ced8"
TEAL = "#3aa8a0"

# Local offsets from a person's feet, before scale.
HEAD = (0, -214)
HEAD_TOP = (0, -268)


def n(value):
    return round(float(value), 1)


def world(x, y, scale, local, flip=False):
    lx = -local[0] if flip else local[0]
    return x + lx * scale, y + local[1] * scale


class Draw:
    def __init__(self, bg=SKY):
        self.p = []
        self.rect(0, 0, 640, 480, bg)

    def svg(self):
        body = "\n".join(self.p)
        return (
            '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="480" '
            'viewBox="0 0 640 480" shape-rendering="geometricPrecision">\n'
            + body
            + "\n</svg>\n"
        )

    def add(self, fragment):
        self.p.append(fragment)
        return self

    @contextmanager
    def g(self, transform):
        self.p.append(f'<g transform="{transform}">')
        try:
            yield self
        finally:
            self.p.append("</g>")

    def _stroke(self, stroke, sw):
        if not stroke or not sw:
            return ""
        return (
            f' stroke="{stroke}" stroke-width="{n(sw)}" '
            'stroke-linejoin="round" stroke-linecap="round"'
        )

    def rect(self, x, y, w, h, fill, stroke=None, sw=0, opacity=None):
        extra = self._stroke(stroke, sw)
        if opacity is not None:
            extra += f' opacity="{opacity}"'
        self.p.append(
            f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" fill="{fill}"{extra}/>'
        )
        return self

    def rrect(self, x, y, w, h, r, fill, stroke=None, sw=0, opacity=None):
        extra = self._stroke(stroke, sw)
        if opacity is not None:
            extra += f' opacity="{opacity}"'
        self.p.append(
            f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" rx="{n(r)}" '
            f'fill="{fill}"{extra}/>'
        )
        return self

    def circle(self, cx, cy, r, fill, stroke=None, sw=0, opacity=None):
        extra = self._stroke(stroke, sw)
        if opacity is not None:
            extra += f' opacity="{opacity}"'
        self.p.append(
            f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="{fill}"{extra}/>'
        )
        return self

    def ellipse(self, cx, cy, rx, ry, fill, stroke=None, sw=0, opacity=None):
        extra = self._stroke(stroke, sw)
        if opacity is not None:
            extra += f' opacity="{opacity}"'
        self.p.append(
            f'<ellipse cx="{n(cx)}" cy="{n(cy)}" rx="{n(rx)}" ry="{n(ry)}" fill="{fill}"{extra}/>'
        )
        return self

    def poly(self, pts, fill, stroke=None, sw=0, opacity=None):
        points = " ".join(f"{n(x)},{n(y)}" for x, y in pts)
        extra = self._stroke(stroke, sw)
        if opacity is not None:
            extra += f' opacity="{opacity}"'
        self.p.append(f'<polygon points="{points}" fill="{fill}"{extra}/>')
        return self

    def line(self, pts, stroke, sw):
        points = " ".join(f"{n(x)},{n(y)}" for x, y in pts)
        self.p.append(
            f'<polyline points="{points}" fill="none" stroke="{stroke}" '
            f'stroke-width="{n(sw)}" stroke-linecap="round" stroke-linejoin="round"/>'
        )
        return self

    def path(self, d, fill="none", stroke="none", sw=0, opacity=None):
        extra = self._stroke(stroke, sw) if sw else ""
        if opacity is not None:
            extra += f' opacity="{opacity}"'
        self.p.append(f'<path d="{d}" fill="{fill}"{extra}/>')
        return self

    def glyph(self, text, x, y, size=36, fill=INK):
        raw = str(text)
        allowed = set("0123456789+?!ABCP")
        if not raw or len(raw) > 2 or any(ch not in allowed for ch in raw):
            raise ValueError("glyph not allowed: " + raw)
        self._text(raw, x, y, size, fill)
        return self

    def zh(self, text, x, y, size=36, fill=INK):
        self._text(text, x, y, size, fill, family=(
            '"PingFang TC","Microsoft JhengHei","Noto Sans CJK TC",'
            '"WenQuanYi Micro Hei",sans-serif'
        ))
        return self

    def _text(self, text, x, y, size, fill, family="Verdana, sans-serif"):
        safe = html.escape(text)
        self.p.append(
            f'<text x="{n(x)}" y="{n(y)}" dy="0.35em" text-anchor="middle" '
            f'font-family=\'{family}\' font-size="{n(size)}" font-weight="700" '
            f'fill="{fill}">{safe}</text>'
        )

    def shadow(self, x, y, rx=48, ry=12):
        self.ellipse(x, y, rx, ry, "rgba(36,48,68,0.13)")
        return self

    def outdoor(self, sky=SKY, ground=GRASS, horizon=348):
        self.rect(0, 0, 640, 480, sky)
        self.rect(0, horizon, 640, 480 - horizon, ground)
        self.rect(0, horizon, 640, 10, GRASS_DARK)
        return self

    def indoor(self, wall="#f3f6fb", floor="#e7d3b0", horizon=340):
        self.rect(0, 0, 640, 480, wall)
        self.rect(0, horizon, 640, 480 - horizon, floor)
        self.rect(0, horizon, 640, 6, "#d2b48c")
        return self

    def night(self):
        self.rect(0, 0, 640, 480, "#1d2a44")
        self.rect(0, 360, 640, 120, "#24344a")
        return self

    def sun(self, x, y, r=54, face=False):
        for i in range(12):
            ang = i * math.pi / 6
            x1 = x + math.cos(ang) * (r + 8)
            y1 = y + math.sin(ang) * (r + 8)
            x2 = x + math.cos(ang) * (r + 26)
            y2 = y + math.sin(ang) * (r + 26)
            self.line([(x1, y1), (x2, y2)], ORANGE, 6)
        self.circle(x, y, r, YELLOW, INK, 4)
        if face:
            self.circle(x - 16, y - 6, 5, INK)
            self.circle(x + 16, y - 6, 5, INK)
            self.path(
                f"M{n(x-18)} {n(y+10)} Q{n(x)} {n(y+28)} {n(x+18)} {n(y+10)}",
                stroke=INK, sw=4,
            )
        return self

    def cloud(self, x, y, s=1, fill=WHITE):
        self.circle(x, y, 26 * s, fill)
        self.circle(x + 28 * s, y + 6 * s, 22 * s, fill)
        self.circle(x - 30 * s, y + 8 * s, 20 * s, fill)
        self.ellipse(x, y + 16 * s, 46 * s, 18 * s, fill)
        return self

    def rain(self, x, y, count=5):
        for i in range(count):
            xx = x + i * 18
            self.line([(xx, y), (xx - 8, y + 22)], "#5aa6e6", 4)
        return self

    def snowflake(self, x, y, r=10):
        self.line([(x - r, y), (x + r, y)], WHITE, 3)
        self.line([(x, y - r), (x, y + r)], WHITE, 3)
        self.line([(x - r * 0.7, y - r * 0.7), (x + r * 0.7, y + r * 0.7)], WHITE, 3)
        self.line([(x - r * 0.7, y + r * 0.7), (x + r * 0.7, y - r * 0.7)], WHITE, 3)
        return self

    def house(self, x, y, sc=1, wall=CREAM, roof=RED, door=BROWN, win="#9fd4ff"):
        w, h = 150 * sc, 104 * sc
        left, top = x - w / 2, y - h
        self.shadow(x, y, 70 * sc, 12 * sc)
        self.rrect(left, top, w, h, 6 * sc, wall, INK, 4)
        self.poly(
            [(left - 16 * sc, top + 6), (x, top - 72 * sc), (left + w + 16 * sc, top + 6)],
            roof, INK, 4,
        )
        self.rrect(x - 16 * sc, y - 58 * sc, 32 * sc, 58 * sc, 4 * sc, door, INK, 3)
        self.circle(x + 8 * sc, y - 28 * sc, 3 * sc, YELLOW)
        self.rrect(left + 16 * sc, top + 22 * sc, 32 * sc, 28 * sc, 3 * sc, win, INK, 3)
        self.rrect(left + w - 48 * sc, top + 22 * sc, 32 * sc, 28 * sc, 3 * sc, win, INK, 3)
        return self

    def tree(self, x, y, sc=1, leaf=GREEN):
        self.rrect(x - 10 * sc, y - 90 * sc, 20 * sc, 90 * sc, 6, BROWN, INK, 3)
        self.circle(x, y - 120 * sc, 46 * sc, leaf, INK, 4)
        self.circle(x - 32 * sc, y - 96 * sc, 32 * sc, leaf, INK, 4)
        self.circle(x + 34 * sc, y - 98 * sc, 30 * sc, leaf, INK, 4)
        return self

    def pine(self, x, y, sc=1):
        self.rrect(x - 8 * sc, y - 36 * sc, 16 * sc, 36 * sc, 4, BROWN)
        self.poly(
            [(x, y - 150 * sc), (x - 50 * sc, y - 70 * sc), (x + 50 * sc, y - 70 * sc)],
            "#2f8f5b", INK, 3,
        )
        self.poly(
            [(x, y - 110 * sc), (x - 62 * sc, y - 30 * sc), (x + 62 * sc, y - 30 * sc)],
            "#237a48", INK, 3,
        )
        return self

    def flower(self, x, y, color=PINK, sc=1):
        for i in range(6):
            ang = i * math.pi / 3
            self.circle(x + math.cos(ang) * 16 * sc, y + math.sin(ang) * 16 * sc, 12 * sc, color, INK, 2)
        self.circle(x, y, 8 * sc, YELLOW, INK, 2)
        self.line([(x, y + 14 * sc), (x, y + 64 * sc)], GREEN_DARK, 4)
        return self

    def person(
        self, x, y, sc=1, mood="smile", shirt=BLUE, hair=HAIR, pants=NAVY,
        skin=SKIN, pose="stand", hair_style="short", flip=False, pale=False,
    ):
        if pale:
            skin = "#f3e2cf"
        sx = -sc if flip else sc
        with self.g(f"translate({n(x)} {n(y)}) scale({n(sx)} {n(sc)})"):
            if pose != "lie":
                self.ellipse(0, 6, 50, 12, "rgba(36,48,68,0.12)")
            self._legs(pose, pants)
            self._arms(pose, skin, shirt)
            self.rrect(-36, -168, 72, 96, 22, shirt, INK, 4)
            self.circle(0, -214, 46, skin, INK, 4)
            self._hair(hair_style, hair)
            self._face(mood)
        return self

    def _limb(self, x, y, w, h, angle, fill):
        self.p.append(
            f'<rect x="{n(-w / 2)}" y="0" width="{n(w)}" height="{n(h)}" rx="{n(w / 2)}" '
            f'fill="{fill}" stroke="{INK}" stroke-width="4" stroke-linejoin="round" '
            f'transform="translate({n(x)} {n(y)}) rotate({n(angle)})"/>'
        )

    def _legs(self, pose, pants):
        shoe = "#2c3e50"
        if pose == "run":
            self._limb(-10, -78, 20, 78, -32, pants)
            self._limb(12, -78, 20, 78, 28, pants)
        elif pose == "sit":
            self._limb(-16, -70, 20, 70, 78, pants)
            self._limb(8, -70, 20, 70, 78, pants)
        elif pose == "lie":
            self._limb(-8, -78, 18, 84, 8, pants)
            self._limb(14, -78, 18, 84, -6, pants)
        elif pose == "slump":
            self._limb(-18, -60, 20, 64, 48, pants)
            self._limb(16, -60, 20, 64, 28, pants)
            self.ellipse(-6, 4, 18, 8, shoe)
            self.ellipse(28, 8, 18, 8, shoe)
        elif pose == "bow":
            self._limb(-12, -78, 20, 78, -8, pants)
            self._limb(14, -78, 20, 78, 10, pants)
        else:
            self.rrect(-26, -86, 20, 82, 10, pants, INK, 4)
            self.rrect(6, -86, 20, 82, 10, pants, INK, 4)
            self.ellipse(-16, -6, 16, 8, shoe)
            self.ellipse(16, -6, 16, 8, shoe)

    def _arms(self, pose, skin, shirt):
        if pose == "run":
            self._limb(-34, -150, 16, 70, 40, shirt)
            self._limb(34, -150, 16, 70, -50, shirt)
        elif pose == "carry":
            self._limb(-38, -150, 16, 62, -150, shirt)
            self._limb(38, -150, 16, 62, 150, shirt)
        elif pose == "wave":
            self._limb(-34, -148, 16, 66, 16, shirt)
            self._limb(36, -150, 16, 72, -150, shirt)
            self.circle(36, -224, 12, skin, INK, 3)
        elif pose == "point":
            self._limb(-34, -148, 16, 64, 18, shirt)
            self._limb(34, -146, 16, 78, -78, shirt)
        elif pose == "push":
            self._limb(-20, -140, 16, 58, -70, shirt)
            self._limb(20, -140, 16, 58, 70, shirt)
        elif pose == "read":
            self._limb(-30, -140, 16, 58, 28, shirt)
            self._limb(30, -140, 16, 58, -28, shirt)
        elif pose == "flex":
            self._limb(-40, -150, 18, 50, -130, shirt)
            self._limb(34, -148, 16, 64, 20, shirt)
        elif pose == "think":
            self._limb(30, -146, 16, 58, -130, shirt)
            self._limb(-34, -148, 16, 64, 14, shirt)
        elif pose == "hug":
            self._limb(-34, -146, 16, 60, -40, shirt)
            self._limb(34, -146, 16, 60, 40, shirt)
        elif pose == "giveup":
            self._limb(-36, -140, 16, 70, 24, shirt)
            self._limb(36, -140, 16, 70, -24, shirt)
        elif pose == "slump":
            self._limb(-34, -130, 16, 72, 36, shirt)
            self._limb(34, -130, 16, 72, -36, shirt)
        elif pose == "plead":
            self._limb(-12, -150, 16, 62, -58, shirt)
            self._limb(12, -150, 16, 62, 58, shirt)
            self.circle(0, -200, 11, skin, INK, 3)
        elif pose == "bow":
            self._limb(-30, -120, 16, 60, 70, shirt)
            self._limb(30, -120, 16, 60, -70, shirt)
        else:
            self._limb(-40, -150, 16, 68, 12, shirt)
            self._limb(40, -150, 16, 68, -12, shirt)
            self.circle(-28, -84, 11, skin, INK, 3)
            self.circle(28, -84, 11, skin, INK, 3)

    def _hair(self, style, color):
        if style == "bald":
            return
        if style == "grey":
            self.path(
                "M-40 -214 Q-44 -268 0 -274 Q44 -268 40 -214 Q22 -230 0 -226 Q-22 -230 -40 -214",
                fill=HAIR_GREY, stroke=INK, sw=3,
            )
            return
        if style == "long":
            self.path(
                "M-42 -200 Q-48 -274 0 -280 Q48 -274 42 -200 L48 -120 Q30 -140 18 -150 L10 -210 "
                "Q0 -230 -10 -210 L-16 -150 Q-28 -140 -46 -120 Z",
                fill=color, stroke=INK, sw=3,
            )
            return
        if style == "wild":
            spikes = [(-40, -230), (-24, -286), (-4, -250), (8, -292), (28, -248), (44, -276), (36, -220)]
            self.poly([(-46, -210)] + spikes + [(46, -210), (0, -230)], color, INK, 3)
            return
        if style == "bun":
            self.circle(0, -262, 16, color, INK, 3)
        self.path(
            "M-42 -206 Q-46 -270 0 -276 Q46 -270 42 -206 Q20 -226 0 -220 Q-20 -226 -42 -206",
            fill=color, stroke=INK, sw=3,
        )

    def _face(self, mood):
        brow = INK
        if mood == "shy":
            self.path("M-22 -224 Q-14 -232 -6 -224", stroke=INK, sw=3)
            self.path("M6 -224 Q14 -232 22 -224", stroke=INK, sw=3)
            self.circle(-18, -198, 8, PINK, opacity=0.8)
            self.circle(18, -198, 8, PINK, opacity=0.8)
        elif mood == "silly":
            self.circle(-14, -220, 7, INK)
            self.circle(16, -220, 7, INK)
            self.circle(-12, -222, 2, WHITE)
            self.circle(18, -222, 2, WHITE)
        elif mood == "shut":
            self.path("M-22 -222 Q-13 -230 -4 -222", stroke=INK, sw=4)
            self.path("M4 -222 Q13 -230 22 -222", stroke=INK, sw=4)
        elif mood == "tired":
            self.line([(-22, -222), (-8, -222)], INK, 4)
            self.line([(8, -222), (22, -222)], INK, 4)
        elif mood == "wild":
            self.circle(-16, -222, 8, WHITE, INK, 3)
            self.circle(16, -222, 8, WHITE, INK, 3)
            self.circle(-16, -222, 3, INK)
            self.circle(16, -222, 3, INK)
        else:
            self.circle(-15, -220, 5.5, INK)
            self.circle(15, -220, 5.5, INK)
            self.circle(-13, -222, 2, WHITE)
            self.circle(17, -222, 2, WHITE)
        if mood == "angry":
            self.line([(-26, -238), (-6, -230)], brow, 4)
            self.line([(6, -230), (26, -238)], brow, 4)
        elif mood in ("sad", "cry"):
            self.line([(-26, -232), (-6, -240)], brow, 4)
            self.line([(6, -240), (26, -232)], brow, 4)
        elif mood == "think":
            self.line([(-24, -236), (-6, -232)], brow, 4)
            self.line([(8, -240), (24, -232)], brow, 4)
        if mood in ("smile", "happy", "confident"):
            self.path("M-16 -196 Q0 -178 16 -196", stroke=INK, sw=4)
        elif mood == "silly":
            self.path("M-14 -196 Q0 -180 12 -196", stroke=INK, sw=4)
            self.ellipse(8, -188, 7, 6, "#e86b7a", INK, 2)
        elif mood in ("sad", "cry"):
            self.path("M-14 -188 Q0 -204 14 -188", stroke=INK, sw=4)
        elif mood == "angry":
            self.path("M-16 -190 Q0 -204 16 -190", stroke=INK, sw=4)
        elif mood == "wow":
            self.ellipse(0, -192, 8, 10, INK)
        elif mood == "shy":
            self.path("M-10 -196 Q0 -188 10 -196", stroke=INK, sw=3)
        elif mood == "tired":
            self.path("M-12 -190 Q0 -198 12 -190", stroke=INK, sw=4)
        elif mood == "wild":
            self.ellipse(0, -188, 12, 14, "#e86b7a", INK, 3)
            self.path("M-8 -186 Q0 -176 10 -188", stroke=INK, sw=3)
        else:
            self.line([(-10, -194), (10, -194)], INK, 4)
        if mood == "cry":
            self.path("M-22 -210 Q-28 -190 -18 -180", stroke="#5aa6e6", sw=4)
            self.path("M20 -210 Q28 -188 18 -176", stroke="#5aa6e6", sw=4)
        if mood == "happy":
            self.path("M-16 -196 Q0 -176 16 -196 Q0 -186 -16 -196", fill="#e86b7a", stroke=INK, sw=3)

    def glasses(self, x, y, sc=1):
        hx, hy = world(x, y, sc, HEAD)
        self.circle(hx - 16 * sc, hy, 16 * sc, "none", INK, 3)
        self.circle(hx + 16 * sc, hy, 16 * sc, "none", INK, 3)
        self.line([(hx - 2 * sc, hy), (hx + 2 * sc, hy)], INK, 3)
        return self

    def cane(self, x, y, sc=1):
        self.line(
            [(x + 40 * sc, y - 150 * sc), (x + 48 * sc, y - 4)],
            BROWN, 6,
        )
        self.path(
            f"M{n(x+40*sc)} {n(y-150*sc)} Q{n(x+70*sc)} {n(y-160*sc)} {n(x+62*sc)} {n(y-130*sc)}",
            stroke=BROWN, sw=6,
        )
        return self

    def book(self, x, y, sc=1, open_=True):
        if not open_:
            self.rrect(x, y, 70 * sc, 90 * sc, 4, "#5b7fd1", INK, 3)
            self.rect(x, y, 8 * sc, 90 * sc, "#3e5eaf")
            return self
        self.poly([(x, y), (x - 70 * sc, y + 18 * sc), (x - 64 * sc, y + 78 * sc), (x, y + 58 * sc)], "#fffdf8", INK, 3)
        self.poly([(x, y), (x + 70 * sc, y + 18 * sc), (x + 64 * sc, y + 78 * sc), (x, y + 58 * sc)], "#fffdf8", INK, 3)
        self.line([(x, y), (x, y + 58 * sc)], BROWN, 4)
        return self

    def gift(self, x, y, sc=1, box="#ef5b5b"):
        s = 70 * sc
        self.rrect(x - s / 2, y - s * 0.7, s, s * 0.75, 6, box, INK, 4)
        self.rect(x - 8 * sc, y - s * 0.7, 16 * sc, s * 0.75, YELLOW)
        self.rect(x - s / 2, y - s * 0.42, s, 14 * sc, YELLOW)
        self.poly(
            [(x, y - s * 0.7), (x - 24 * sc, y - s * 1.05), (x - 8 * sc, y - s * 0.7)],
            YELLOW, INK, 3,
        )
        self.poly(
            [(x, y - s * 0.7), (x + 24 * sc, y - s * 1.05), (x + 8 * sc, y - s * 0.7)],
            "#f0b429", INK, 3,
        )
        self.circle(x, y - s * 0.72, 8 * sc, YELLOW, INK, 3)
        return self

    def sparkles(self, pts, color=YELLOW):
        for x, y, r in pts:
            self.line([(x - r, y), (x + r, y)], color, 3)
            self.line([(x, y - r), (x, y + r)], color, 3)
        return self

    def arrow(self, x1, y1, x2, y2, color=INK, sw=8):
        import math
        self.line([(x1, y1), (x2, y2)], color, sw)
        ang = math.atan2(y2 - y1, x2 - x1)
        a1 = ang + 2.6
        a2 = ang - 2.6
        self.poly(
            [
                (x2, y2),
                (x2 + math.cos(a1) * 18, y2 + math.sin(a1) * 18),
                (x2 + math.cos(a2) * 18, y2 + math.sin(a2) * 18),
            ],
            color,
        )
        return self

    def glass_cup(self, x, y, fill, w=70, h=120, level=0.35):
        self.path(
            f"M{n(x)} {n(y)} L{n(x+14)} {n(y+h)} L{n(x+w-14)} {n(y+h)} L{n(x+w)} {n(y)} Z",
            fill="rgba(255,255,255,0.28)", stroke=INK, sw=5,
        )
        top = y + h * level
        self.path(
            f"M{n(x+8)} {n(top)} L{n(x+16)} {n(y+h-8)} L{n(x+w-16)} {n(y+h-8)} L{n(x+w-8)} {n(top)} Z",
            fill=fill,
        )
        self.ellipse(x + w / 2, y, w / 2, 12, "rgba(255,255,255,0.45)", INK, 4)
        self.ellipse(x + w / 2, top, w * 0.38, 8, fill, INK, 2)
        self.line([(x + 18, y + 16), (x + 24, y + h - 18)], "rgba(255,255,255,0.85)", 6)
        return self

    def bowl(self, x, y, w=160, h=70, inner="#fff"):
        self.path(
            f"M{n(x)} {n(y)} Q{n(x+w/2)} {n(y+h*1.7)} {n(x+w)} {n(y)}",
            fill="#f4f7fb", stroke=INK, sw=4,
        )
        self.ellipse(x + w / 2, y, w * 0.42, 16, inner, INK, 3)
        return self

    def jar(self, x, y, jam="#d63c55"):
        self.rrect(x, y + 30, 110, 130, 12, "rgba(255,255,255,0.45)", INK, 4)
        self.rrect(x + 8, y + 70, 94, 80, 8, jam)
        self.rrect(x + 18, y, 74, 40, 8, "#7dce8a", INK, 3)
        self.ellipse(x + 55, y + 100, 16, 12, "#ffd1dc")
        return self

    def can(self, x, y):
        self.ellipse(x + 40, y, 40, 14, "#ff8b8b", INK, 3)
        self.rect(x, y, 80, 140, RED, INK, 4)
        self.ellipse(x + 40, y + 140, 40, 14, RED_DARK, INK, 3)
        self.rect(x, y + 48, 80, 36, WHITE)
        self.circle(x + 40, y + 66, 10, "#7fd3ff", INK, 2)
        return self

    def banana(self, x, y, sc=1):
        outer = []
        inner = []
        for i in range(31):
            t = i / 30
            ang = math.radians(200 + t * 130)
            outer.append((x + math.cos(ang) * 120 * sc, y + math.sin(ang) * 100 * sc))
            inner.append((x + math.cos(ang) * 78 * sc, y + math.sin(ang) * 62 * sc))
        self.poly(outer + inner[::-1], YELLOW, INK, 4)
        a0 = math.radians(200)
        a1 = math.radians(330)
        self.circle(x + math.cos(a0) * 100 * sc, y + math.sin(a0) * 82 * sc, 10 * sc, BROWN, INK, 2)
        self.circle(x + math.cos(a1) * 100 * sc, y + math.sin(a1) * 82 * sc, 8 * sc, "#e0b44a", INK, 2)
        return self

    def bed(self, x, y, w=280, h=120):
        self.rrect(x, y - h, w, h, 16, "#f7f1e8", INK, 4)
        self.rrect(x + 16, y - h - 10, 70, 48, 12, WHITE, INK, 3)
        self.rrect(x + 8, y - 28, w - 16, 28, 8, "#d7c4a3", INK, 3)
        self.rect(x + 16, y - h + 20, w - 40, 18, "#9fd4ff")
        return self

    def door(self, x, y, w=150, h=230, open_=False, knob=True):
        if open_:
            self.rrect(x, y - h, w, h, 8, "#d8ecff", INK, 4)
            self.poly(
                [(x + w, y - h), (x + w + 70, y - h + 24), (x + w + 70, y - 16), (x + w, y)],
                "#f3e2c8", INK, 4,
            )
        else:
            self.rrect(x, y - h, w, h, 8, "#c9854a", INK, 4)
            self.rrect(x + 16, y - h + 20, w - 32, h - 40, 6, "#e0a56a", INK, 3)
            if knob:
                self.circle(x + w - 28, y - h / 2, 8, YELLOW, INK, 3)
        return self

    def calendar_base(self, x, y, w, h):
        self.rrect(x, y, w, h, 16, WHITE, INK, 4)
        self.rect(x, y, w, 48, RED)
        self.rrect(x, y, w, 48, 16, RED)
        self.rect(x, y + 24, w, 24, RED)
        self.circle(x + 36, y + 8, 8, WHITE)
        self.circle(x + w - 36, y + 8, 8, WHITE)
        return self

    def week_cells(self, x, y, w, active=None, marks=None):
        gap = 8
        cw = (w - gap * 6) / 7
        for i in range(7):
            xx = x + i * (cw + gap)
            fill = "#e8f7f1" if active == i else "#f4f7fb"
            stroke = GREEN_DARK if active == i else INK
            self.rrect(xx, y, cw, 64, 8, fill, stroke, 3)
            if marks and i < len(marks):
                self.zh(marks[i], xx + cw / 2, y + 30, 22, INK)
        return self

    def bulb(self, x, y, sc=1, on=True):
        color = YELLOW if on else GREY
        self.circle(x, y, 28 * sc, color, INK, 4)
        self.rrect(x - 10 * sc, y + 22 * sc, 20 * sc, 16 * sc, 3, "#d9dee6", INK, 3)
        if on:
            self.sparkles([(x + 36 * sc, y - 20 * sc, 8), (x - 34 * sc, y - 10 * sc, 6)])
        return self

    def check(self, x, y, sc=1, color=GREEN):
        s = 20 * sc
        self.line([(x - s, y), (x - s * 0.2, y + s * 0.8), (x + s, y - s * 0.7)], color, 8 * sc)
        return self

    def thumb(self, x, y, up=True, sc=1):
        dy = -1 if up else 1
        self.rrect(x - 22 * sc, y - 10 * sc, 44 * sc, 70 * sc, 16 * sc, SKIN, INK, 4)
        self.rrect(x - 18 * sc, y + dy * 54 * sc, 28 * sc, 48 * sc, 12 * sc, SKIN, INK, 4)
        return self

    def star(self, x, y, r, fill=YELLOW):
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            rad = r if i % 2 == 0 else r * 0.45
            pts.append((x + math.cos(ang) * rad, y + math.sin(ang) * rad))
        self.poly(pts, fill, INK, 3)
        return self

    def heart(self, x, y, s=20, fill=PINK):
        self.path(
            f"M{n(x)} {n(y+s)} "
            f"C{n(x-s*1.6)} {n(y-s*0.2)} {n(x-s*0.8)} {n(y-s*1.3)} {n(x)} {n(y-s*0.4)} "
            f"C{n(x+s*0.8)} {n(y-s*1.3)} {n(x+s*1.6)} {n(y-s*0.2)} {n(x)} {n(y+s)} Z",
            fill=fill, stroke=INK, sw=3,
        )
        return self

    def eye_icon(self, x, y, sc=1):
        self.ellipse(x, y, 70 * sc, 40 * sc, WHITE, INK, 5)
        self.circle(x, y, 22 * sc, "#3aa0e0", INK, 4)
        self.circle(x, y, 10 * sc, INK)
        self.circle(x + 6 * sc, y - 6 * sc, 4 * sc, WHITE)
        return self

    def ear_icon(self, x, y, sc=1):
        self.path(
            f"M{n(x)} {n(y+70*sc)} "
            f"C{n(x-80*sc)} {n(y+40*sc)} {n(x-70*sc)} {n(y-80*sc)} {n(x)} {n(y-70*sc)} "
            f"C{n(x+20*sc)} {n(y-20*sc)} {n(x+10*sc)} {n(y+20*sc)} {n(x)} {n(y+70*sc)} Z",
            fill=SKIN, stroke=INK, sw=5,
        )
        self.path(
            f"M{n(x-4*sc)} {n(y+30*sc)} C{n(x-30*sc)} {n(y+10*sc)} {n(x-24*sc)} {n(y-30*sc)} {n(x)} {n(y-24*sc)}",
            stroke=INK, sw=4,
        )
        return self

    def elephant(self, x, y, sc=1):
        with self.g(f"translate({n(x)} {n(y)}) scale({n(sc)})"):
            self.ellipse(0, 4, 100, 16, "rgba(36,48,68,0.12)")
            for lx in (-58, -24, 16, 48):
                self.rrect(lx, -78, 24, 78, 10, "#b7c3cf", INK, 3)
            self.ellipse(0, -130, 110, 72, "#c5d0da", INK, 4)
            self.circle(95, -160, 52, "#c5d0da", INK, 4)
            self.ellipse(62, -168, 30, 42, "#d5dee6", INK, 4)
            self.path(
                "M120 -140 C160 -120 170 -70 140 -40 C150 -20 120 -24 112 -48 C108 -80 116 -120 90 -140 Z",
                fill="#c5d0da", stroke=INK, sw=4,
            )
            self.circle(112, -168, 5, INK)
            self.path("M124 -130 Q146 -110 136 -88", stroke=WHITE, sw=6)
        return self

    def sheep(self, x, y, sc=1):
        with self.g(f"translate({n(x)} {n(y)}) scale({n(sc)})"):
            self.ellipse(0, 4, 70, 12, "rgba(36,48,68,0.12)")
            for lx in (-40, -10, 16, 40):
                self.rrect(lx, -40, 12, 40, 6, "#2c3e50")
            for cx, cy, r in ((-30, -70, 28), (0, -84, 34), (32, -70, 28), (0, -60, 30)):
                self.circle(cx, cy, r, WHITE, INK, 3)
            self.ellipse(62, -78, 22, 18, "#3a322c", INK, 3)
            self.circle(78, -84, 4, WHITE)
            self.circle(70, -80, 2, INK)
        return self

    def tiger(self, x, y, sc=1):
        with self.g(f"translate({n(x)} {n(y)}) scale({n(sc)})"):
            self.ellipse(0, 6, 90, 14, "rgba(36,48,68,0.12)")
            self.ellipse(-20, -70, 100, 48, ORANGE, INK, 4)
            for sx in (-70, -30, 10, 46):
                self.line([(sx, -96), (sx + 8, -44)], INK, 4)
            self.circle(78, -96, 40, ORANGE, INK, 4)
            self.poly([(60, -120), (70, -160), (96, -118)], ORANGE, INK, 3)
            self.poly([(96, -118), (118, -156), (112, -108)], ORANGE, INK, 3)
            self.circle(90, -100, 5, INK)
            self.circle(92, -102, 2, WHITE)
            self.poly([(100, -86), (112, -80), (100, -74)], PINK)
            self.path("M-110 -60 Q-150 -90 -120 -20", stroke=ORANGE, sw=12)
            for lx in (-70, -30, 10):
                self.rrect(lx, -40, 16, 40, 6, ORANGE, INK, 3)
        return self

    def shark(self, x, y, sc=1):
        with self.g(f"translate({n(x)} {n(y)}) scale({n(sc)})"):
            self.path(
                "M-120 0 C-40 -50 80 -46 150 -10 C90 10 20 24 -120 0 Z",
                fill="#8ea2b5", stroke=INK, sw=4,
            )
            self.poly([(10, -30), (36, -78), (48, -20)], "#7e93a8", INK, 3)
            self.poly([(-20, 10), (-4, 36), (16, 8)], "#7e93a8", INK, 3)
            self.poly([(140, -16), (190, -4), (146, 6)], "#8ea2b5", INK, 3)
            self.circle(86, -16, 5, INK)
            self.circle(88, -18, 2, WHITE)
            self.line([(-40, 0), (-10, 0)], WHITE, 3)
        return self

    def whale(self, x, y, sc=1):
        with self.g(f"translate({n(x)} {n(y)}) scale({n(sc)})"):
            self.path(
                "M-160 10 C-80 -70 120 -80 200 -10 C120 40 -40 46 -160 10 Z",
                fill="#4c8dff", stroke=INK, sw=4,
            )
            self.poly([(20, -48), (70, -110), (80, -30)], "#2f6fe0", INK, 3)
            self.circle(120, -16, 6, INK)
            self.circle(124, -18, 2, WHITE)
            self.path("M150 -20 Q170 -50 160 -70", stroke="#9fd4ff", sw=6)
            self.circle(164, -78, 8, "rgba(255,255,255,0.7)")
        return self

    def eagle(self, x, y, sc=1):
        with self.g(f"translate({n(x)} {n(y)}) scale({n(sc)})"):
            self.path("M0 0 C-40 -30 -140 -20 -190 30 C-100 8 -40 24 0 12 Z", fill="#6b4a2e", stroke=INK, sw=4)
            self.path("M0 0 C40 -30 140 -20 190 30 C100 8 40 24 0 12 Z", fill="#6b4a2e", stroke=INK, sw=4)
            self.path("M-70 -8 L-20 8 L-60 16 Z", fill="#4a301c", stroke=INK, sw=2)
            self.path("M70 -8 L20 8 L60 16 Z", fill="#4a301c", stroke=INK, sw=2)
            self.ellipse(0, 8, 26, 18, "#5a3b24", INK, 3)
            self.circle(36, -10, 20, WHITE, INK, 3)
            self.poly([(50, -12), (78, -4), (50, 4)], YELLOW, INK, 3)
            self.circle(32, -12, 3.5, INK)
            self.path("M-8 16 Q-4 28 2 16", stroke=YELLOW, sw=3)
        return self

    def bee(self, x, y, sc=1):
        with self.g(f"translate({n(x)} {n(y)}) scale({n(sc)})"):
            self.ellipse(-8, -28, 22, 10, "rgba(255,255,255,0.85)", INK, 2)
            self.ellipse(18, -30, 18, 8, "rgba(255,255,255,0.85)", INK, 2)
            self.ellipse(0, 0, 36, 26, YELLOW, INK, 4)
            self.rect(-28, -26, 10, 52, INK)
            self.rect(-6, -26, 10, 52, INK)
            self.rect(14, -22, 8, 44, INK)
            self.circle(34, -4, 14, YELLOW, INK, 3)
            self.circle(40, -8, 3, INK)
            self.line([(30, -16), (24, -36)], INK, 3)
            self.line([(40, -14), (48, -34)], INK, 3)
            self.circle(24, -36, 3, INK)
            self.circle(48, -34, 3, INK)
        return self

    def kitten(self, x, y, sc=1):
        with self.g(f"translate({n(x)} {n(y)}) scale({n(sc)})"):
            self.ellipse(10, 20, 50, 28, "#f4a25a", INK, 4)
            self.circle(-20, -20, 36, "#f4a25a", INK, 4)
            self.poly([(-46, -30), (-34, -78), (-8, -36)], "#f4a25a", INK, 3)
            self.poly([(-8, -36), (8, -76), (16, -24)], "#f4a25a", INK, 3)
            self.poly([(-40, -36), (-32, -64), (-16, -40)], "#ffd0c4")
            self.poly([(-4, -38), (2, -62), (10, -30)], "#ffd0c4")
            self.circle(-32, -22, 4, INK)
            self.circle(-10, -22, 4, INK)
            self.poly([(-24, -12), (-18, -12), (-21, -6)], PINK)
            self.path("M46 10 Q80 0 70 30", stroke="#f4a25a", sw=10)
        return self

    def ant(self, x, y, sc=1):
        with self.g(f"translate({n(x)} {n(y)}) scale({n(sc)})"):
            self.circle(-36, 0, 16, "#3a322c", INK, 3)
            self.circle(0, 0, 20, "#3a322c", INK, 3)
            self.ellipse(40, 0, 28, 20, "#3a322c", INK, 3)
            self.circle(-44, -6, 3, WHITE)
            for ang in (-40, 0, 40):
                self.line([( -10, 0), (-10 + math.cos(math.radians(ang + 180)) * 36, math.sin(math.radians(ang)) * 28)], INK, 3)
                self.line([(16, 0), (16 + math.cos(math.radians(ang)) * 36, math.sin(math.radians(ang)) * 28)], INK, 3)
            self.line([(-48, -8), (-60, -28)], INK, 3)
            self.line([(-42, -10), (-40, -32)], INK, 3)
        return self

    def bat(self, x, y, sc=1):
        with self.g(f"translate({n(x)} {n(y)}) scale({n(sc)})"):
            self.path("M0 0 C-30 -20 -90 -10 -130 30 C-70 10 -30 20 0 8 Z", fill="#3a4254", stroke=INK, sw=3)
            self.path("M0 0 C30 -20 90 -10 130 30 C70 10 30 20 0 8 Z", fill="#3a4254", stroke=INK, sw=3)
            self.circle(0, 0, 18, "#4a5568", INK, 3)
            self.poly([(-8, -14), (0, -32), (8, -14)], "#4a5568", INK, 2)
            self.circle(-6, -2, 3, WHITE)
            self.circle(6, -2, 3, WHITE)
            self.circle(-6, -2, 1.5, INK)
            self.circle(6, -2, 1.5, INK)
        return self

    def cheetah(self, x, y, sc=1):
        with self.g(f"translate({n(x)} {n(y)}) scale({n(sc)})"):
            self.ellipse(0, -20, 90, 32, "#e0a85a", INK, 4)
            for dx, dy in ((-40, -28), (-10, -36), (20, -24), (50, -30), (-20, -8)):
                self.circle(dx, dy, 5, "#3a322c")
            self.circle(78, -36, 26, "#e0a85a", INK, 3)
            self.circle(88, -40, 3, INK)
            self.path("M-80 -10 Q-120 -30 -100 10", stroke="#e0a85a", sw=8)
            self.line([(-40, 0), (-60, 30)], "#c4844a", 6)
            self.line([(10, 4), (0, 34)], "#c4844a", 6)
            self.line([(40, 0), (70, 24)], "#c4844a", 6)
        return self

    def speed_lines(self, x, y):
        for i, yy in enumerate((y, y + 18, y + 36)):
            self.line([(x, yy), (x + 50 + i * 10, yy)], "#9aa8b8", 4)
        return self

    def plate(self, x, y, w=180):
        self.ellipse(x, y, w / 2, 28, WHITE, INK, 4)
        self.ellipse(x, y, w / 2 - 16, 16, "#f4f7fb", INK, 2)
        return self

    def butterfly(self, x, y, sc=1):
        with self.g(f"translate({n(x)} {n(y)}) scale({n(sc)})"):
            self.ellipse(-38, -28, 42, 28, "#7eb6ef", INK, 4)
            self.ellipse(38, -28, 42, 28, "#7eb6ef", INK, 4)
            self.ellipse(-34, 22, 28, 36, PINK, INK, 4)
            self.ellipse(34, 22, 28, 36, PINK, INK, 4)
            self.circle(-28, -24, 8, YELLOW, INK, 2)
            self.circle(28, -24, 8, YELLOW, INK, 2)
            self.ellipse(0, 0, 8, 36, "#3a322c", INK, 3)
            self.line([(0, -34), (-16, -58)], INK, 3)
            self.line([(0, -34), (16, -58)], INK, 3)
            self.circle(-16, -58, 4, INK)
            self.circle(16, -58, 4, INK)
        return self

    def knife(self, x, y, sc=1):
        with self.g(f"translate({n(x)} {n(y)}) scale({n(sc)})"):
            self.poly([(0, -18), (210, -6), (210, 8), (0, 18)], "#e8eef5", INK, 4)
            self.line([(16, -4), (180, 0)], WHITE, 4)
            self.rrect(200, -22, 78, 44, 10, BROWN, INK, 4)
            self.circle(230, 0, 5, YELLOW)
            self.sparkles([(40, -28, 7), (120, -24, 5)])
        return self

    def iron(self, x, y, sc=1):
        with self.g(f"translate({n(x)} {n(y)}) scale({n(sc)})"):
            self.path("M-20 40 L10 -20 L150 -20 L190 40 Z", fill="#d5dde6", stroke=INK, sw=5)
            self.rrect(20, -48, 120, 36, 12, "#8ea0b4", INK, 4)
            self.circle(50, 10, 7, BLUE)
            self.path("M150 -40 C190 -70 210 -20 180 -10", stroke=INK, sw=4)
            self.ellipse(80, 52, 110, 12, "rgba(36,48,68,0.12)")
        return self

    def popcorn_bucket(self, x, y, sc=1):
        with self.g(f"translate({n(x)} {n(y)}) scale({n(sc)})"):
            self.path("M-70 20 L-50 150 L50 150 L70 20 Z", fill=RED, stroke=INK, sw=4)
            for i, xx in enumerate((-40, -10, 20)):
                self.rect(xx, 20, 16, 130, WHITE)
            for cx, cy, r in (
                (-30, -10, 22), (0, -28, 26), (34, -8, 20),
                (-10, 8, 18), (24, 16, 16), (-46, 16, 14), (8, -4, 14),
            ):
                self.circle(cx, cy, r, "#fffdf6", INK, 3)
        return self

    def steam(self, x, y, count=3):
        for i in range(count):
            self.path(
                f"M{n(x + i * 18)} {n(y)} Q{n(x + 16 + i * 18)} {n(y - 24)} {n(x + i * 18)} {n(y - 48)}",
                stroke="#c5d4e4", sw=5,
            )
        return self

    def umbrella(self, x, y, sc=1):
        self.path(
            f"M{n(x-90*sc)} {n(y)} Q{n(x)} {n(y-110*sc)} {n(x+90*sc)} {n(y)} Z",
            fill=RED, stroke=INK, sw=4,
        )
        self.line([(x, y), (x, y + 90 * sc)], INK, 4)
        self.path(f"M{n(x)} {n(y+90*sc)} Q{n(x+20*sc)} {n(y+110*sc)} {n(x+8*sc)} {n(y+90*sc)}", stroke=INK, sw=4)
        return self
