"""Character/vehicle builders. Each takes (cx, cy, scale, c).
c=None -> pure line art (white fill, black stroke) for interior coloring pages.
c={...} -> colored version for the cover.
All coordinates are authored for scale=1.0 around the given center, then the
whole group is translated+scaled via an SVG transform so callers just pick a
placement.
"""

import math
from lib import (_fill, circle, ellipse, rrect, poly, path, line, star, face,
                  blush_marks, group, STROKE)


def _wrap(cx, cy, scale, body):
    return f'<g transform="translate({cx} {cy}) scale({scale})">{body}</g>'


# ---------------------------------------------------------------- dinos ----

def dino_round(cx, cy, scale, c=None):
    body = _fill(c, "body", "#6FCF63")
    belly = _fill(c, "belly", "#DFF7C8")
    spike = _fill(c, "spike", "#4CAF50")
    snout = _fill(c, "snout", "#DFF7C8")
    o = []
    o.append(ellipse(-95, 60, 65, 26, fill=body, rot=-18))          # tail
    o.append(ellipse(-50, 130, 38, 19, fill=body))                  # feet
    o.append(ellipse(50, 130, 38, 19, fill=body))
    o.append(ellipse(0, 0, 125, 145, fill=body))                    # body
    o.append(ellipse(-95, -35, 32, 19, fill=body))                  # arms
    o.append(ellipse(95, -35, 32, 19, fill=body))
    o.append(circle(-40, -190, 98, fill=body))                      # head
    o.append(poly([(2, -205), (25, -260), (42, -202)], fill=spike))
    o.append(poly([(32, -145), (58, -200), (76, -140)], fill=spike))
    o.append(poly([(54, -85), (82, -140), (98, -80)], fill=spike))
    o.append(ellipse(-90, -162, 48, 36, fill=snout))
    o.append(circle(-122, -162, 6, fill="#000"))
    o.append(circle(-60, -220, 24, fill="#FFFFFF", sw=7))
    o.append(circle(-15, -226, 24, fill="#FFFFFF", sw=7))
    o.append(circle(-54, -216, 10, fill="#000"))
    o.append(circle(-9, -222, 10, fill="#000"))
    o.append(path("M-120,-145 Q-100,-130 -80,-143"))
    o.append(blush_marks(-90, -172, 0, -8))
    return _wrap(cx, cy, scale, "".join(o))


def triceratops(cx, cy, scale, c=None):
    body = _fill(c, "body", "#8FD3E8")
    frill = _fill(c, "frill", "#5FB8D6")
    horn = _fill(c, "horn", "#FFFFFF")
    o = []
    o.append(ellipse(-90, 70, 55, 24, fill=body, rot=8))            # tail
    o.append(ellipse(-55, 140, 36, 18, fill=body))
    o.append(ellipse(60, 140, 36, 18, fill=body))
    o.append(ellipse(0, 20, 135, 120, fill=body))                   # body
    o.append(circle(90, -70, 46, fill=frill))                       # frill back
    for a in (-70, -35, 0, 35, 70):
        ax = 90 + 78 * math.sin(math.radians(a))
        ay = -70 - 78 * math.cos(math.radians(a))
        o.append(circle(ax, ay, 16, fill=frill))
    o.append(circle(80, -75, 88, fill=body))                        # head
    o.append(poly([(70, -170), (85, -230), (100, -172)], fill=horn))
    o.append(poly([(35, -140), (10, -190), (58, -155)], fill=horn))
    o.append(poly([(110, -145), (145, -188), (122, -130)], fill=horn))
    o.append(ellipse(120, -60, 34, 24, fill=body))                  # snout
    o.append(circle(148, -55, 6, fill="#000"))
    o.append(circle(65, -95, 22, fill="#FFFFFF", sw=7))
    o.append(circle(108, -100, 22, fill="#FFFFFF", sw=7))
    o.append(circle(70, -90, 9, fill="#000"))
    o.append(circle(113, -95, 9, fill="#000"))
    o.append(path("M95,-45 Q112,-32 130,-44"))
    o.append(blush_marks(88, -68, -26, 10))
    return _wrap(cx, cy, scale, "".join(o))


def longneck(cx, cy, scale, c=None):
    body = _fill(c, "body", "#8FE0A6")
    spot = _fill(c, "spot", "#5FCB84")
    o = []
    o.append(ellipse(-150, 150, 45, 22, fill=body, rot=15))         # tail
    o.append(ellipse(-70, 215, 32, 18, fill=body))                  # legs
    o.append(ellipse(20, 225, 32, 18, fill=body))
    o.append(ellipse(110, 215, 32, 18, fill=body))
    o.append(ellipse(20, 140, 175, 110, fill=body))                 # body
    o.append(circle(-60, 20, 20, fill=spot))
    o.append(circle(70, 80, 16, fill=spot))
    o.append(f'<path d="M-90,60 C-125,-30 -115,-110 -95,-155 L-25,-155 C-48,-110 -52,-30 -18,60 Z" fill="{body}" stroke="#000" stroke-width="13" stroke-linejoin="round"/>')
    o.append(circle(-60, -190, 62, fill=body))                      # head
    o.append(ellipse(-105, -175, 24, 16, fill=body))                # snout
    o.append(circle(-125, -175, 5, fill="#000"))
    o.append(circle(-78, -208, 15, fill="#FFFFFF", sw=6))
    o.append(circle(-78, -208, 6, fill="#000"))
    o.append(path("M-112,-165 Q-98,-157 -87,-166"))
    o.append(blush_marks(-90, -185, -14, 12, r=9))
    return _wrap(cx, cy, scale, "".join(o))


def stegosaurus(cx, cy, scale, c=None):
    body = _fill(c, "body", "#B6A6E8")
    plate = _fill(c, "plate", "#8F79D6")
    o = []
    o.append(poly([(-195, 55), (-150, 20), (-150, 90)], fill=body))  # tail point
    o.append(ellipse(-95, 145, 30, 19, fill=body))                   # legs
    o.append(ellipse(-30, 150, 30, 19, fill=body))
    o.append(ellipse(35, 150, 30, 19, fill=body))
    o.append(ellipse(100, 145, 30, 19, fill=body))
    o.append(ellipse(0, 40, 160, 105, fill=body))                    # body
    for i, px in enumerate((-95, -40, 15, 72)):
        h = [62, 82, 78, 52][i]
        o.append(poly([(px-26, -50), (px, -50-h), (px+26, -50)], fill=plate))
    o.append(circle(150, 5, 66, fill=body))                          # head
    o.append(ellipse(197, 18, 26, 18, fill=body))                    # snout
    o.append(circle(215, 13, 5, fill="#000"))
    o.append(circle(140, -22, 17, fill="#FFFFFF", sw=6))
    o.append(circle(140, -22, 7, fill="#000"))
    o.append(path("M160,35 Q175,45 190,37"))
    o.append(blush_marks(133, 5, -16, 8, r=10))
    return _wrap(cx, cy, scale, "".join(o))


def dino_egg(cx, cy, scale, c=None):
    shell = _fill(c, "shell", "#FFF3D6")
    baby = _fill(c, "baby", "#9BE39B")
    o = []
    o.append(f'<path d="M-130,60 C-130,-80 130,-80 130,60 C130,150 -130,150 -130,60 Z" fill="{shell}" stroke="#000" stroke-width="13"/>')
    o.append(path("M-80,-35 L-42,15 L-8,-25 L22,22 L58,-15", fill="none", sw=8))
    o.append(circle(0, -140, 68, fill=baby))
    o.append(poly([(-28, -205), (-14, -245), (0, -203)], fill=baby))
    o.append(poly([(8, -208), (26, -248), (34, -200)], fill=baby))
    o.append(circle(-22, -150, 15, fill="#FFFFFF", sw=6))
    o.append(circle(20, -150, 15, fill="#FFFFFF", sw=6))
    o.append(circle(-18, -147, 6, fill="#000"))
    o.append(circle(24, -147, 6, fill="#000"))
    o.append(path("M-16,-118 Q0,-107 16,-118"))
    o.append(blush_marks(0, -135, 32,10, r=9))
    return _wrap(cx, cy, scale, "".join(o))


# ------------------------------------------------------------- vehicles ----

def car(cx, cy, scale, c=None):
    body = _fill(c, "body", "#FFB84C")
    window = _fill(c, "window", "#BEE7FF")
    wheel = _fill(c, "wheel", "#333333")
    hub = _fill(c, "hub", "#CFCFCF")
    bump = _fill(c, "bumper", "#FF6B6B")
    o = []
    o.append(rrect(-170, 30, 340, 110, 42, fill=body))
    o.append(rrect(-70, -55, 190, 100, 32, fill=body))
    o.append(rrect(-48, -38, 145, 62, 18, fill=window))
    o.append(line(24, -38, 24, 24, sw=7))
    o.append(rrect(-170, 118, 340, 24, 12, fill=bump))
    o.append(circle(-105, 162, 46, fill=wheel))
    o.append(circle(-105, 162, 18, fill=hub))
    o.append(circle(90, 162, 46, fill=wheel))
    o.append(circle(90, 162, 18, fill=hub))
    o.append(circle(150, 90, 20, fill="#FFF6B0"))
    o.append(path("M120,150 Q145,164 170,150"))
    return _wrap(cx, cy, scale, "".join(o))


def firetruck(cx, cy, scale, c=None):
    body = _fill(c, "body", "#FF6B6B")
    window = _fill(c, "window", "#BEE7FF")
    wheel = _fill(c, "wheel", "#333333")
    hub = _fill(c, "hub", "#CFCFCF")
    ladder = _fill(c, "ladder", "#FFD23F")
    o = []
    o.append(rrect(-200, 10, 400, 120, 30, fill=body))
    o.append(rrect(-200, -70, 150, 100, 26, fill=body))
    o.append(rrect(-180, -50, 100, 55, 16, fill=window))
    o.append(rrect(-190, -140, 360, 24, 10, fill=ladder, rot=0))
    for i in range(-160, 170, 40):
        o.append(line(i, -140, i, -116, sw=6))
    o.append(circle(150, -40, 26, fill="#FFE27A"))
    o.append(circle(150, -40, 10, fill="#FFC24B"))
    o.append(circle(-110, 175, 48, fill=wheel))
    o.append(circle(-110, 175, 19, fill=hub))
    o.append(circle(100, 175, 48, fill=wheel))
    o.append(circle(100, 175, 19, fill=hub))
    o.append(rrect(170, 40, 26, 40, 8, fill="#FFFFFF"))
    return _wrap(cx, cy, scale, "".join(o))


def airplane(cx, cy, scale, c=None):
    body = _fill(c, "body", "#7EC8E3")
    window = _fill(c, "window", "#FFFFFF")
    prop = _fill(c, "prop", "#FFD23F")
    tail = _fill(c, "tail", "#FF6FA0")
    o = []
    o.append(ellipse(0, 0, 190, 75, fill=body))
    o.append(poly([(-40, -60), (10, -160), (60, -55)], fill=tail))
    o.append(poly([(-30, 45), (30, 150), (85, 45)], fill=tail))
    o.append(ellipse(-40, 0, 130, 40, fill="none", sw=0))
    o.append(circle(-60, -5, 28, fill=window, sw=9))
    o.append(circle(10, -5, 28, fill=window, sw=9))
    o.append(circle(80, -5, 28, fill=window, sw=9))
    o.append(rrect(180, -18, 30, 36, 10, fill=body))
    o.append(circle(215, 0, 26, fill=prop))
    o.append(path("M215,-40 L215,40 M182,0 L248,0", sw=8))
    o.append(path("M-100,40 Q-70,10 -40,40 Q-10,60 20,40", sw=7))
    return _wrap(cx, cy, scale, "".join(o))


def rocket(cx, cy, scale, c=None):
    body = _fill(c, "body", "#FF6B6B")
    window = _fill(c, "window", "#8FE0F5")
    fin = _fill(c, "fin", "#FFD23F")
    flame = _fill(c, "flame", "#FFB74C")
    o = []
    o.append(poly([(-40, 190), (-80, 260), (-15, 220)], fill=fin))
    o.append(poly([(40, 190), (80, 260), (15, 220)], fill=fin))
    o.append(f'<path d="M0,-230 C90,-160 90,110 40,190 L-40,190 C-90,110 -90,-160 0,-230 Z" fill="{body}" stroke="#000" stroke-width="13"/>')
    o.append(circle(0, -40, 55, fill=window))
    o.append(circle(0, -40, 22, fill="#FFFFFF"))
    o.append(poly([(-35, 200), (0, 300), (35, 200)], fill=flame))
    return _wrap(cx, cy, scale, "".join(o))


def sailboat(cx, cy, scale, c=None):
    hull = _fill(c, "hull", "#FFB84C")
    sail = _fill(c, "sail", "#FFFFFF")
    sail2 = _fill(c, "sail2", "#FFE8B0")
    wave = _fill(c, "wave", "#8FD3E8")
    o = []
    o.append(poly([(-160, 40), (160, 40), (110, 130), (-110, 130)], fill=hull))
    o.append(line(0, 40, 0, -190, sw=12))
    o.append(poly([(4, -190), (4, 20), (135, 20)], fill=sail))
    o.append(poly([(-4, -140), (-4, 20), (-110, 20)], fill=sail2))
    o.append(circle(0, -205, 16, fill="#FFD23F"))
    o.append(f'<path d="M-190,150 Q-140,120 -90,150 Q-40,180 10,150 Q60,120 110,150 Q160,180 210,150" fill="none" stroke="#000" stroke-width="10"/>')
    return _wrap(cx, cy, scale, "".join(o))


# --------------------------------------------------------------- animals ----

def bunny(cx, cy, scale, c=None):
    fur = _fill(c, "fur", "#FFF4E3")
    inner = _fill(c, "inner_ear", "#FFC2DD")
    o = []
    o.append(circle(130, 15, 26, fill=fur))
    o.append(ellipse(-30, -180, 24, 68, fill=fur, rot=-14))
    o.append(ellipse(-30, -180, 12, 46, fill=inner, rot=-14))
    o.append(ellipse(30, -180, 24, 68, fill=fur, rot=14))
    o.append(ellipse(30, -180, 12, 46, fill=inner, rot=14))
    o.append(ellipse(0, 25, 115, 130, fill=fur))
    o.append(ellipse(-50, 145, 36, 24, fill=fur))
    o.append(ellipse(50, 145, 36, 24, fill=fur))
    o.append(ellipse(-90, -5, 28, 17, fill=fur))
    o.append(circle(0, -165, 92, fill=fur))
    o.append(circle(-33, -185, 15, fill="#000"))
    o.append(circle(27, -185, 15, fill="#000"))
    o.append(circle(-28, -191, 5, fill="#FFF"))
    o.append(circle(32, -191, 5, fill="#FFF"))
    o.append(ellipse(-3, -157, 11, 7, fill=inner))
    o.append(blush_marks(0, -150, 55, 8))
    o.append(path("M-55,-150 L-95,-158 M-55,-142 L-97,-138 M55,-150 L95,-158 M55,-142 L97,-138", sw=4))
    return _wrap(cx, cy, scale, "".join(o))


def bear(cx, cy, scale, c=None):
    fur = _fill(c, "fur", "#C99A6B")
    muzzle = _fill(c, "muzzle", "#F2E0C5")
    bow = _fill(c, "bow", "#FF6FA0")
    o = []
    o.append(circle(-90, -180, 40, fill=fur))
    o.append(circle(90, -180, 40, fill=fur))
    o.append(ellipse(0, 30, 125, 140, fill=fur))
    o.append(ellipse(-55, 150, 38, 24, fill=fur))
    o.append(ellipse(55, 150, 38, 24, fill=fur))
    o.append(ellipse(-100, -10, 30, 18, fill=fur))
    o.append(ellipse(100, -10, 30, 18, fill=fur))
    o.append(circle(0, -140, 95, fill=fur))
    o.append(ellipse(0, -110, 46, 34, fill=muzzle))
    o.append(circle(0, -128, 12, fill="#000"))
    o.append(circle(-36, -160, 15, fill="#FFFFFF", sw=6))
    o.append(circle(36, -160, 15, fill="#FFFFFF", sw=6))
    o.append(circle(-32, -157, 6, fill="#000"))
    o.append(circle(40, -157, 6, fill="#000"))
    o.append(path("M-24,-95 Q0,-78 24,-95"))
    o.append(blush_marks(0, -110, 48, 10))
    o.append(poly([(-26, -35), (0, -10), (26, -35), (0, -55)], fill=bow))
    return _wrap(cx, cy, scale, "".join(o))


def cat(cx, cy, scale, c=None):
    fur = _fill(c, "fur", "#F5B971")
    inner = _fill(c, "inner_ear", "#FF9FC7")
    stripe = _fill(c, "stripe", "#E39A4C")
    o = []
    o.append(ellipse(70, 150, 55, 22, fill=fur, rot=-35))
    o.append(ellipse(0, 30, 110, 130, fill=fur))
    o.append(ellipse(-48, 148, 34, 22, fill=fur))
    o.append(ellipse(48, 148, 34, 22, fill=fur))
    o.append(poly([(-90, -170), (-115, -250), (-55, -195)], fill=fur))
    o.append(poly([(-88, -190), (-100, -235), (-70, -200)], fill=inner))
    o.append(poly([(90, -170), (115, -250), (55, -195)], fill=fur))
    o.append(poly([(88, -190), (100, -235), (70, -200)], fill=inner))
    o.append(circle(0, -145, 92, fill=fur))
    o.append(circle(-32, -160, 15, fill="#FFFFFF", sw=6))
    o.append(circle(32, -160, 15, fill="#FFFFFF", sw=6))
    o.append(circle(-28, -157, 6, fill="#000"))
    o.append(circle(36, -157, 6, fill="#000"))
    o.append(poly([(-8, -128), (8, -128), (0, -115)], fill=stripe))
    o.append(path("M0,-115 Q-18,-100 -34,-108 M0,-115 Q18,-100 34,-108"))
    o.append(path("M-10,-130 L-60,-140 M-10,-122 L-62,-116 M10,-130 L60,-140 M10,-122 L62,-116", sw=4))
    o.append(blush_marks(0, -125, 48, 10))
    return _wrap(cx, cy, scale, "".join(o))


def elephant(cx, cy, scale, c=None):
    skin = _fill(c, "skin", "#B9CBE0")
    inner = _fill(c, "inner_ear", "#DCE7F5")
    o = []
    o.append(ellipse(-135, -95, 75, 90, fill=skin))
    o.append(ellipse(-135, -95, 48, 62, fill=inner))
    o.append(ellipse(135, -95, 75, 90, fill=skin))
    o.append(ellipse(135, -95, 48, 62, fill=inner))
    o.append(ellipse(0, 40, 140, 130, fill=skin))
    o.append(ellipse(-60, 160, 38, 22, fill=skin))
    o.append(ellipse(60, 160, 38, 22, fill=skin))
    o.append(circle(0, -110, 100, fill=skin))
    o.append(f'<path d="M-30,-40 C-55,20 -50,80 -20,95 C0,105 15,90 5,70" fill="{skin}" stroke="#000" stroke-width="13" stroke-linecap="round"/>')
    o.append(circle(-38, -130, 16, fill="#FFFFFF", sw=6))
    o.append(circle(30, -130, 16, fill="#FFFFFF", sw=6))
    o.append(circle(-33, -127, 7, fill="#000"))
    o.append(circle(35, -127, 7, fill="#000"))
    o.append(blush_marks(-4, -100, 55, 15))
    return _wrap(cx, cy, scale, "".join(o))


def owl(cx, cy, scale, c=None):
    body = _fill(c, "body", "#B08968")
    belly = _fill(c, "belly", "#F1E1C6")
    wing = _fill(c, "wing", "#8F6B49")
    beak = _fill(c, "beak", "#FFB84C")
    o = []
    o.append(poly([(-90, -70), (-150, -10), (-90, 40)], fill=body))
    o.append(poly([(90, -70), (150, -10), (90, 40)], fill=body))
    o.append(ellipse(0, 40, 135, 155, fill=body))
    o.append(ellipse(0, 70, 78, 100, fill=belly))
    o.append(path("M-40,20 Q0,45 40,20 M-35,60 Q0,82 35,60 M-30,100 Q0,120 30,100", fill="none", sw=6))
    o.append(poly([(-70, -150), (-40, -195), (-20, -150)], fill=body))
    o.append(poly([(70, -150), (40, -195), (20, -150)], fill=body))
    o.append(circle(0, -100, 105, fill=body))
    o.append(circle(-42, -105, 42, fill="#FFFFFF", sw=8))
    o.append(circle(42, -105, 42, fill="#FFFFFF", sw=8))
    o.append(circle(-38, -100, 16, fill="#000"))
    o.append(circle(46, -100, 16, fill="#000"))
    o.append(poly([(-12, -75), (12, -75), (0, -55)], fill=beak))
    o.append(ellipse(-70, 140, 24, 14, fill=beak))
    o.append(ellipse(70, 140, 24, 14, fill=beak))
    return _wrap(cx, cy, scale, "".join(o))


def turtle(cx, cy, scale, c=None):
    shell = _fill(c, "shell", "#8FD37E")
    plate = _fill(c, "plate", "#5FB35A")
    skin = _fill(c, "skin", "#C8E896")
    o = []
    o.append(ellipse(-135, 40, 44, 30, fill=skin, rot=-10))
    o.append(ellipse(-70, 145, 34, 22, fill=skin))
    o.append(ellipse(70, 145, 34, 22, fill=skin))
    o.append(ellipse(-100, 130, 32, 22, fill=skin, rot=20))
    o.append(ellipse(100, 130, 32, 22, fill=skin, rot=-20))
    o.append(ellipse(0, 40, 165, 130, fill=shell))
    o.append(circle(0, 40, 42, fill=plate))
    for a in range(0, 360, 60):
        x = 90 * math.cos(math.radians(a))
        y = 40 + 70 * math.sin(math.radians(a))
        o.append(circle(x, y, 34, fill=plate))
    o.append(circle(-150, -70, 68, fill=skin))
    o.append(circle(-172, -85, 10, fill="#FFFFFF", sw=6))
    o.append(circle(-172, -85, 4, fill="#000"))
    o.append(path("M-190,-55 Q-172,-46 -158,-54"))
    return _wrap(cx, cy, scale, "".join(o))


# -------------------------------------------------------------- objects ----

def house(cx, cy, scale, c=None):
    wall = _fill(c, "wall", "#FFE8B0")
    roof = _fill(c, "roof", "#FF6B6B")
    door = _fill(c, "door", "#8F6B49")
    window = _fill(c, "window", "#BEE7FF")
    o = []
    o.append(rrect(-140, 0, 280, 190, 14, fill=wall))
    o.append(poly([(-170, 10), (0, -160), (170, 10)], fill=roof))
    o.append(rrect(-35, 80, 70, 110, 10, fill=door))
    o.append(circle(20, 135, 6, fill="#000"))
    o.append(rrect(-115, 40, 55, 55, 8, fill=window))
    o.append(line(-87, 40, -87, 95, sw=6))
    o.append(line(-115, 67, -60, 67, sw=6))
    o.append(rrect(60, 40, 55, 55, 8, fill=window))
    o.append(line(88, 40, 88, 95, sw=6))
    o.append(line(60, 67, 115, 67, sw=6))
    o.append(rrect(90, -140, 26, 60, 6, fill=wall))
    return _wrap(cx, cy, scale, "".join(o))


def balloon(cx, cy, r=70, fill="#FFFFFF", string_len=120):
    o = []
    o.append(f'<path d="M0,{-r} C{r*0.9},{-r} {r},{-r*0.2} {r*0.55},{r*0.6} C{r*0.3},{r*1.05} {-r*0.3},{r*1.05} {-r*0.55},{r*0.6} C{-r},{-r*0.2} {-r*0.9},{-r} 0,{-r} Z" fill="{fill}" stroke="#000" stroke-width="10"/>')
    o.append(poly([(-10, r*0.75), (10, r*0.75), (0, r*0.95)], fill=fill, sw=6))
    o.append(path(f"M0,{r*0.95} Q20,{r*0.95+string_len*0.5} 0,{r*0.95+string_len}", sw=5))
    return _wrap(cx, cy, 1.0, "".join(o))


def cupcake(cx, cy, scale, c=None):
    wrap = _fill(c, "wrap", "#FF9FC7")
    icing = _fill(c, "icing", "#FFFFFF")
    cherry = _fill(c, "cherry", "#FF4C6A")
    o = []
    o.append(poly([(-90, 120), (90, 120), (65, 20), (-65, 20)], fill=wrap))
    for x in range(-80, 90, 20):
        o.append(line(x, 20, x+12, 120, sw=5, stroke="#00000055"))
    o.append(f'<path d="M-75,20 C-75,-70 -40,-40 -30,-90 C-10,-50 10,-50 30,-90 C40,-40 75,-70 75,20 Z" fill="{icing}" stroke="#000" stroke-width="12"/>')
    o.append(circle(0, -95, 20, fill=cherry))
    return _wrap(cx, cy, scale, "".join(o))


def lollipop(cx, cy, scale, c=None):
    candy = _fill(c, "candy", "#FF6FA0")
    swirl = _fill(c, "swirl", "#FFFFFF")
    o = []
    o.append(line(0, 40, 0, 220, sw=10))
    o.append(circle(0, 0, 90, fill=candy))
    o.append(f'<path d="M0,0 m-70,0 a70,70 0 0,1 140,0" fill="none" stroke="{swirl}" stroke-width="10"/>')
    o.append(f'<path d="M0,0 m-45,0 a45,45 0 0,0 90,0" fill="none" stroke="{swirl}" stroke-width="10"/>')
    o.append(f'<path d="M0,0 m-20,0 a20,20 0 0,1 40,0" fill="none" stroke="{swirl}" stroke-width="10"/>')
    return _wrap(cx, cy, scale, "".join(o))


def ice_cream(cx, cy, scale, c=None):
    scoop1 = _fill(c, "scoop1", "#FFF4E3")
    scoop2 = _fill(c, "scoop2", "#FFB3C6")
    cone = _fill(c, "cone", "#E3A857")
    o = []
    o.append(poly([(-55, 60), (55, 60), (0, 220)], fill=cone))
    o.append(path("M-45,80 L45,190 M-25,60 L45,150 M-55,140 L15,190", sw=5))
    o.append(circle(0, 10, 70, fill=scoop2))
    o.append(circle(-45, -60, 55, fill=scoop1))
    o.append(circle(45, -60, 55, fill=scoop1))
    o.append(circle(0, -100, 55, fill=scoop2))
    o.append(circle(0, -155, 14, fill="#FF4C6A"))
    return _wrap(cx, cy, scale, "".join(o))
