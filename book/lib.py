"""
Shared shape/character library for the coloring book.
Every builder returns an SVG fragment (string of elements, no <svg> wrapper).

Two render modes:
  - color mode: pass a `c` dict of fill colors -> used for the cover
  - line mode (c=None): all fills become white (so KDP interior pages stay
    print-cheap pure line art), all strokes stay black. This is the actual
    "coloring page" mode.

Canvas convention: every page is a 1000x1000 viewBox.
"""

import math

STROKE = "#000000"
SW_MAIN = 13
SW_DETAIL = 8

def _fill(c, key, default="#FFFFFF"):
    if c is None:
        return "#FFFFFF"
    return c.get(key, default)

def svg_open(vb=1000):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb} {vb}" width="{vb}" height="{vb}">'

SVG_CLOSE = "</svg>"

def bg(vb=1000, color="#FFFFFF"):
    return f'<rect x="0" y="0" width="{vb}" height="{vb}" fill="{color}"/>'

def circle(cx, cy, r, fill="#FFFFFF", sw=SW_MAIN, stroke=STROKE):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'

def ellipse(cx, cy, rx, ry, fill="#FFFFFF", sw=SW_MAIN, rot=0, stroke=STROKE):
    t = f' transform="rotate({rot} {cx} {cy})"' if rot else ""
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{t}/>'

def rrect(x, y, w, h, rx, fill="#FFFFFF", sw=SW_MAIN, rot=0, stroke=STROKE):
    cx, cy = x + w / 2, y + h / 2
    t = f' transform="rotate({rot} {cx} {cy})"' if rot else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{t}/>'

def poly(points, fill="#FFFFFF", sw=SW_DETAIL, stroke=STROKE):
    pts = " ".join(f"{x},{y}" for x, y in points)
    return f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'

def path(d, fill="none", sw=SW_DETAIL, cap="round", stroke=STROKE):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}" stroke-linejoin="round"/>'

def line(x1, y1, x2, y2, sw=SW_DETAIL, cap="round", stroke=STROKE):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}"/>'

def star(cx, cy, r_out, r_in, fill="#FFFFFF", sw=SW_DETAIL, points=5, rot=-90):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 360 / (points * 2))
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return poly(pts, fill=fill, sw=sw)

def text(x, y, s, size=40, weight=900, fill="#000000", anchor="middle", family="'Arial Black', Arial, sans-serif", extra=""):
    return f'<text x="{x}" y="{y}" font-family="{family}" font-weight="{weight}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>'

def group(inner, transform=None):
    t = f' transform="{transform}"' if transform else ""
    return f'<g{t}>{inner}</g>'


# ---------------------------------------------------------------- decor ----

def face(cx, cy, eye_dx, eye_dy, eye_r=20, pupil_r=9, mouth="smile", blush=True,
         mouth_w=34, mouth_y_off=34, closed_eyes=False):
    """A friendly face: two eyes + mouth, centered around (cx, cy)."""
    out = []
    ex1, ex2 = cx - eye_dx, cx + eye_dx
    ey = cy + eye_dy
    if closed_eyes:
        out.append(path(f"M{ex1-16},{ey} Q{ex1},{ey-14} {ex1+16},{ey}", sw=7))
        out.append(path(f"M{ex2-16},{ey} Q{ex2},{ey-14} {ex2+16},{ey}", sw=7))
    else:
        out.append(circle(ex1, ey, eye_r, fill="#FFFFFF", sw=7))
        out.append(circle(ex2, ey, eye_r, fill="#FFFFFF", sw=7))
        out.append(circle(ex1, ey, pupil_r, fill="#000000", sw=0))
        out.append(circle(ex2, ey, pupil_r, fill="#000000", sw=0))
    my = cy + mouth_y_off
    if mouth == "smile":
        out.append(path(f"M{cx-mouth_w/2},{my} Q{cx},{my+22} {cx+mouth_w/2},{my}", sw=7))
    elif mouth == "open":
        out.append(path(f"M{cx-mouth_w/2},{my} Q{cx},{my+30} {cx+mouth_w/2},{my} Q{cx},{my+14} {cx-mouth_w/2},{my} Z", fill="#FFFFFF", sw=7))
    if blush:
        out.append(f'<circle cx="{ex1-8}" cy="{ey+26}" r="13" fill="#FFAFC5" opacity="0.0" />' if False else "")
    return "".join(out)

def blush_marks(cx, cy, dx, dy, r=14, color="#FFB3C6"):
    return (f'<circle cx="{cx-dx}" cy="{cy+dy}" r="{r}" fill="{color}" opacity="0.85"/>'
            f'<circle cx="{cx+dx}" cy="{cy+dy}" r="{r}" fill="{color}" opacity="0.85"/>')

def flower(cx, cy, scale, c=None, key="petal"):
    fill = _fill(c, key, "#FF6FA0")
    center = _fill(c, "flower_center", "#FFD23F") if c else "#FFFFFF"
    pts = [(0, -22), (0, 22), (-22, 0), (22, 0), (-15, -15), (15, 15), (-15, 15), (15, -15)]
    out = []
    for (dx, dy) in pts:
        out.append(circle(cx + dx * scale, cy + dy * scale, 15 * scale, fill=fill, sw=6))
    out.append(circle(cx, cy, 16 * scale, fill=center, sw=6))
    return "".join(out)

def stem(x, y1, y2, sw=8, leaf=True, color=STROKE):
    out = [line(x, y1, x, y2, sw=sw, stroke=color)]
    if leaf:
        my = (y1 + y2) / 2
        out.append(path(f"M{x},{my} Q{x+28},{my-8} {x+6},{my+18} Z", fill="#FFFFFF", sw=6))
    return "".join(out)

def cloud(cx, cy, scale=1.0, fill="#FFFFFF"):
    s = scale
    return (rrect(cx-45*s, cy+2*s, 90*s, 22*s, 11*s, fill=fill, sw=7) +
            circle(cx-25*s, cy+5*s, 18*s, fill=fill, sw=7) +
            circle(cx+8*s, cy-8*s, 24*s, fill=fill, sw=7) +
            circle(cx+32*s, cy+6*s, 15*s, fill=fill, sw=7))

def sun(cx, cy, r=52, fill="#FFD23F", rays=True, ray_color=None):
    out = [circle(cx, cy, r, fill=fill, sw=9)]
    if rays:
        rc = ray_color or fill
        for i in range(8):
            a = math.radians(i * 45)
            x1, y1 = cx + (r+18)*math.cos(a), cy + (r+18)*math.sin(a)
            x2, y2 = cx + (r+40)*math.cos(a), cy + (r+40)*math.sin(a)
            out.append(line(x1, y1, x2, y2, sw=11, stroke=rc if c_is_stroke(rc) else STROKE))
    return "".join(out)

def c_is_stroke(v):
    return True

def grass(y_base=800, dark="#6FBF3E", light="#8BD450"):
    top, front = dark, light
    d1 = f"M0,{y_base-40} C120,{y_base-90} 220,{y_base-10} 340,{y_base-60} C460,{y_base-110} 560,{y_base-20} 680,{y_base-65} C800,{y_base-110} 900,{y_base-30} 1000,{y_base-65} L1000,1000 L0,1000 Z"
    d2 = f"M0,{y_base-10} C130,{y_base-55} 230,{y_base+20} 350,{y_base-20} C470,{y_base-65} 570,{y_base+15} 690,{y_base-25} C810,{y_base-70} 900,{y_base+5} 1000,{y_base-25} L1000,1000 L0,1000 Z"
    return f'<path d="{d1}" fill="{top}" stroke="none"/><path d="{d2}" fill="{front}" stroke="#000" stroke-width="14" stroke-linejoin="round"/>'

def page_chrome(number, section, vb=1000):
    """Small consistent corner branding + page number for interior pages."""
    out = []
    out.append(star(56, 56, 22, 10, fill="#FFFFFF", sw=7))
    out.append(text(vb/2, vb-28, str(number), size=26, weight=700, fill="#BBBBBB"))
    return "".join(out)
