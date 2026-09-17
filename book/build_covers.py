import os
import lib
import critters as cr

OUT = os.path.join(os.path.dirname(__file__), "..")

def save(name, body, vb=1000):
    svg = lib.svg_open(vb) + lib.bg(vb) + body + lib.SVG_CLOSE
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        f.write(svg)
    print("wrote", path)

COVER_C = dict(
    body="#6FCF63", belly="#DFF7C8", spike="#4CAF50", snout="#DFF7C8",
)
CAR_C = dict(body="#FFB84C", window="#BEE7FF", wheel="#333333", hub="#CFCFCF", bumper="#FF6B6B")
BUNNY_C = dict(fur="#FFF4E3", inner_ear="#FFC2DD")

def rainbow_title(y0=165, y1=255, size=98):
    colors = ["#FF5C5C", "#FF9F45", "#FFD23F", "#3FC97A", "#3FA9F5", "#7E6FE0", "#FF6FA0"]
    word1, word2 = "COLORING", "BOOK"
    out = f'<g font-family="\'Arial Black\', Arial, sans-serif" font-weight="900" text-anchor="middle" paint-order="stroke fill" stroke="#000" stroke-linejoin="round">'
    out += lib.text(500, 70, "MY FIRST", size=40, weight=900, fill="#3FA9F5", extra='stroke-width="0"')
    out += f'<text x="500" y="{y0}" font-size="{size}" stroke-width="9">'
    for i, ch in enumerate(word1):
        out += f'<tspan fill="{colors[i % len(colors)]}">{ch}</tspan>'
    out += '</text>'
    out += f'<text x="500" y="{y1}" font-size="{size}" stroke-width="9">'
    for i, ch in enumerate(word2):
        out += f'<tspan fill="{colors[(i+1) % len(colors)]}">{ch}</tspan>'
    out += '</text></g>'
    return out

def ribbon(text_str, y=330):
    return (f'<path d="M210,{y-35} L790,{y-35} L825,{y} L790,{y+35} L210,{y+35} L175,{y} Z" '
            f'fill="#3FA9F5" stroke="#000" stroke-width="9" stroke-linejoin="round"/>' +
            lib.text(500, y+13, text_str, size=27, weight=900, fill="#FFFFFF"))

def age_badge(cx=130, cy=900, rot=-8):
    return lib.group(
        lib.circle(cx, cy, 72, fill="#FF6B6B", sw=11) +
        lib.text(cx, cy-10, "AGES", size=28, weight=900, fill="#FFFFFF") +
        lib.text(cx, cy+25, "2-6", size=30, weight=900, fill="#FFFFFF"),
        transform=f"rotate({rot} {cx} {cy})")

PINK = dict(petal="#FF6FA0", flower_center="#FFD23F")
PURPLE = dict(petal="#B57EDC", flower_center="#FFD23F")
ORANGE = dict(petal="#FFA94D", flower_center="#FFD23F")
RED = dict(petal="#FF6B6B", flower_center="#FFD23F")

front = (
    lib.cloud(70, 55, 1.1) +
    lib.sun(900, 120, 52) +
    lib.star(40, 230, 27, 12, fill="#FF6FA0") +
    lib.star(935, 300, 22, 10, fill="#3FA9F5") +
    lib.star(55, 640, 17, 8, fill="#FFD23F") +
    rainbow_title() +
    ribbon("Dinosaurs, Animals &amp; Fun!") +
    lib.grass(y_base=800) +
    lib.flower(70, 855, 1.1, PINK) + lib.stem(70, 885, 918, leaf=False) +
    lib.flower(945, 820, 1.1, RED) + lib.stem(945, 850, 918, leaf=False) +
    cr.dino_round(225, 640, 1.05, COVER_C) +
    cr.car(500, 650, 1.0, CAR_C) +
    cr.bunny(815, 650, 1.0, BUNNY_C) +
    lib.flower(320, 875, 0.85, PURPLE) + lib.stem(320, 900, 940, leaf=False) +
    lib.flower(660, 880, 0.85, ORANGE) + lib.stem(660, 905, 940, leaf=False) +
    lib.flower(495, 905, 0.7, RED) + lib.stem(495, 925, 955, leaf=False) +
    age_badge() +
    lib.rrect(760, 930, 200, 46, 23, fill="#FFFFFF", sw=7) +
    lib.text(860, 961, "by Your Name", size=24, weight=700, fill="#555555")
)
save("cover_front.svg", front)

# ----------------------------------------------------------- BACK COVER ----
blurb_lines = [
    "Climb aboard for a color-filled adventure!",
    "Meet a friendly dinosaur, a happy little car,",
    "and a bouncy bunny — plus 20+ more big,",
    "bold pictures of animals, dinosaurs, cars,",
    "flowers and stars, made just for little hands.",
]
back = (
    lib.cloud(80, 60, 1.0) +
    lib.star(60, 470, 20, 9, fill="#FF6FA0") +
    lib.text(500, 130, "MY FIRST COLORING BOOK", size=34, weight=900) +
    ribbon("Big Pictures, Big Fun!", y=210)
)
ty = 300
for ln in blurb_lines:
    back += lib.text(500, ty, ln, size=25, weight=700, fill="#444444")
    ty += 38

back += (
    lib.text(500, ty + 30, "✨ 27 extra-large, easy-to-color pages", size=22, weight=700, fill="#3FA9F5") +
    lib.text(500, ty + 66, "✨ Thick outlines, perfect for little hands", size=22, weight=700, fill="#FF6FA0") +
    lib.text(500, ty + 102, "✨ Original, cheerful designs", size=22, weight=700, fill="#5FB85A")
)

back += (
    lib.flower(90, 850, 1.0, PINK) + cr.dino_round(190, 870, 0.5, COVER_C) +
    cr.bunny(500, 870, 0.5, BUNNY_C) + cr.car(800, 870, 0.5, CAR_C) +
    lib.flower(910, 850, 1.0, ORANGE)
)
back += lib.rrect(770, 40, 175, 90, 8, fill="#FFFFFF", sw=6)
back += lib.text(857, 70, "ISBN / Barcode", size=15, weight=700, fill="#AAAAAA")
for i, x in enumerate(range(780, 930, 6)):
    if i % 3 != 0:
        back += lib.line(x, 82, x, 115, sw=2, stroke="#222222")
save("cover_back.svg", back)

print("covers done")
