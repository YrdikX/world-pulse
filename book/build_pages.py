import os
import lib
import critters as cr

OUT = os.path.join(os.path.dirname(__file__), "pages")
os.makedirs(OUT, exist_ok=True)

def save(name, body):
    svg = lib.svg_open() + lib.bg() + body + lib.SVG_CLOSE
    with open(os.path.join(OUT, name), "w") as f:
        f.write(svg)
    print("wrote", name)

def deco_corner_flowers():
    return (lib.flower(70, 70, 0.7) + lib.stem(70, 100, 150, leaf=False) +
            lib.flower(930, 70, 0.7) + lib.stem(930, 100, 150, leaf=False))

def footer(n):
    return lib.text(500, 972, str(n), size=26, weight=700, fill="#CCCCCC")

# ---- 1 dino solo -----------------------------------------------------
save("01_dino.svg", cr.dino_round(430, 560, 1.55) + footer(1))

# ---- 2 triceratops -----------------------------------------------------
save("02_triceratops.svg", cr.triceratops(500, 560, 1.55) + footer(2))

# ---- 3 longneck ---------------------------------------------------------
save("03_longneck.svg", cr.longneck(470, 610, 1.25) + footer(3))

# ---- 4 stegosaurus -------------------------------------------------------
save("04_stegosaurus.svg", cr.stegosaurus(490, 610, 1.55) + footer(4))

# ---- 5 dino egg ----------------------------------------------------------
save("05_dino_egg.svg", cr.dino_egg(500, 640, 1.45) +
     lib.flower(160, 860, 1.0) + lib.flower(840, 860, 1.0) + footer(5))

# ---- 6 car -----------------------------------------------------------
save("06_car.svg",
     cr.car(500, 560, 1.85) +
     lib.path("M0,820 L1000,820", sw=8) +
     lib.path("M60,820 L140,820 M260,820 L340,820 M460,820 L540,820 M660,820 L740,820 M860,820 L940,820", sw=8) +
     footer(6))

# ---- 7 fire truck ----------------------------------------------------
save("07_firetruck.svg", cr.firetruck(500, 600, 1.6) + footer(7))

# ---- 8 airplane -------------------------------------------------------
save("08_airplane.svg",
     cr.airplane(520, 480, 1.7) +
     lib.cloud(150, 250, 1.2) + lib.cloud(830, 700, 1.1) +
     lib.star(120, 700, 26, 12) + lib.star(870, 260, 22, 10) + footer(8))

# ---- 9 rocket ----------------------------------------------------------
save("09_rocket.svg",
     cr.rocket(500, 560, 1.55) +
     lib.star(140, 200, 24, 11) + lib.star(860, 250, 20, 9) +
     lib.star(880, 620, 18, 8) + lib.star(120, 650, 22, 10) + footer(9))

# ---- 10 sailboat -------------------------------------------------------
save("10_sailboat.svg", cr.sailboat(500, 560, 1.75) +
     lib.sun(850, 200, 46) + footer(10))

# ---- 11 bunny -----------------------------------------------------------
save("11_bunny.svg", cr.bunny(500, 650, 1.55) + footer(11))

# ---- 12 bear ------------------------------------------------------------
save("12_bear.svg", cr.bear(500, 640, 1.5) + footer(12))

# ---- 13 cat --------------------------------------------------------------
save("13_cat.svg", cr.cat(500, 660, 1.5) + footer(13))

# ---- 14 elephant ---------------------------------------------------------
save("14_elephant.svg", cr.elephant(500, 620, 1.5) + footer(14))

# ---- 15 owl --------------------------------------------------------------
save("15_owl.svg", cr.owl(500, 610, 1.5) + footer(15))

# ---- 16 turtle -----------------------------------------------------------
save("16_turtle.svg", cr.turtle(500, 640, 1.7) + footer(16))

# ---- 17 flower garden scene ----------------------------------------------
garden = (lib.sun(850, 160, 55) +
          lib.path("M0,830 L1000,830", sw=8) +
          lib.stem(170, 620, 830, sw=12) + lib.flower(170, 590, 2.3) +
          lib.stem(390, 690, 830, sw=12) + lib.flower(390, 650, 1.9) +
          lib.stem(610, 600, 830, sw=12) + lib.flower(610, 560, 2.6) +
          lib.stem(830, 680, 830, sw=12) + lib.flower(830, 645, 2.0) +
          lib.star(80, 220, 22, 10) + lib.star(940, 380, 20, 9))
save("17_garden.svg", garden + footer(17))

# ---- 18 flower bouquet in basket ------------------------------------------
basket = lib.rrect(-150, 50, 300, 140, 22, fill="#FFFFFF", sw=13)
weave = "".join(lib.line(-150, 75+i*26, 150, 75+i*26, sw=6) for i in range(4))
handle = lib.path("M-105, 55 Q0,-110 105,55", sw=13)
bouquet = (
    lib.group(basket + weave + handle, transform="translate(500 760)") +
    lib.stem(390, 470, 720, sw=12, leaf=False) + lib.flower(390, 420, 1.9) +
    lib.stem(500, 400, 715, sw=12, leaf=False) + lib.flower(500, 345, 2.3) +
    lib.stem(610, 470, 720, sw=12, leaf=False) + lib.flower(610, 420, 1.9) +
    lib.stem(300, 540, 715, sw=12, leaf=False) + lib.flower(300, 500, 1.5) +
    lib.stem(700, 540, 715, sw=12, leaf=False) + lib.flower(700, 500, 1.5)
)
save("18_bouquet.svg", bouquet + footer(18))

# ---- 19 sky scene ----------------------------------------------------------
sky = (lib.sun(180, 180, 55) + lib.cloud(650, 150, 1.4) + lib.cloud(830, 350, 1.0) +
       lib.star(500, 600, 42, 20) + lib.star(300, 780, 26, 12) +
       lib.star(750, 720, 30, 14) + lib.star(120, 500, 20, 9) +
       lib.path("M150,850 A350,350 0 0,1 850,850", sw=14))
save("19_sky.svg", sky + footer(19))

# ---- 20 balloons ------------------------------------------------------------
balloons = (cr.balloon(280, 380, 90, string_len=420) +
            cr.balloon(500, 300, 110, string_len=520) +
            cr.balloon(720, 400, 85, string_len=440) +
            cr.balloon(420, 470, 70, string_len=380) +
            cr.balloon(600, 480, 75, string_len=400))
save("20_balloons.svg", balloons + footer(20))

# ---- 21 sweet treats ---------------------------------------------------------
treats = (cr.ice_cream(230, 560, 1.2) + cr.cupcake(560, 640, 1.15) +
          cr.lollipop(800, 500, 0.9))
save("21_treats.svg", treats + footer(21))

# ---- 22 house ------------------------------------------------------------------
house_scene = (cr.house(500, 650, 1.5) + lib.sun(850, 160, 46) +
               lib.star(120, 180, 22, 10) +
               lib.path("M120,900 Q150,760 190,900", sw=10) +
               lib.circle(160, 730, 60, fill="#FFFFFF"))
save("22_house.svg", house_scene + footer(22))

# ---- 23 mixed friends scene (dino + car + bunny, smaller, all together) -------
scene = (cr.dino_round(210, 700, 0.85) + cr.car(500, 720, 0.95) +
         cr.bunny(790, 700, 0.85) + lib.flower(350, 880, 0.8) +
         lib.flower(650, 880, 0.8) + lib.star(80, 200, 22, 10) +
         lib.star(920, 220, 22, 10))
save("23_friends.svg", scene + footer(23))

# ---- 24 big star + heart + circle practice shapes (very first strokes) --------
practice = (
    lib.star(260, 350, 150, 68) +
    lib.circle(500, 720, 150) +
    lib.path("M770,610 C770,540 900,540 900,630 C900,700 800,760 770,800 C740,760 640,700 640,630 C640,540 770,540 770,610 Z", sw=13)
)
save("24_practice.svg", practice + footer(24))

print("DONE:", len(os.listdir(OUT)), "pages")
