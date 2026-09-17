import os
import lib
import critters as cr

OUT = os.path.join(os.path.dirname(__file__), "pages")

def save(name, body):
    svg = lib.svg_open() + lib.bg() + body + lib.SVG_CLOSE
    with open(os.path.join(OUT, name), "w") as f:
        f.write(svg)
    print("wrote", name)

# -- 00 title page (mirrors the cover in black & white, simple) ------------
title_deco = (lib.star(90, 90, 24, 11) + lib.star(910, 90, 24, 11) +
              lib.flower(90, 900, 1.0) + lib.flower(910, 900, 1.0))
title = (
    lib.text(500, 300, "MY FIRST", size=44, weight=900) +
    lib.text(500, 400, "COLORING BOOK", size=76, weight=900) +
    lib.text(500, 462, "Dinosaurs, Animals &amp; Fun!", size=30, weight=700, fill="#555555") +
    cr.dino_round(320, 760, 0.72) + cr.bunny(680, 775, 0.68) +
    title_deco
)
save("00_title.svg", title)

# -- 000 copyright page -------------------------------------------------
copyright_body = (
    lib.text(500, 380, "My First Coloring Book", size=34, weight=900) +
    lib.text(500, 420, "Dinosaurs, Animals &amp; Fun!", size=22, weight=700, fill="#555555") +
    lib.text(500, 500, "Copyright © 2026 Your Name", size=22, weight=700) +
    lib.text(500, 540, "All rights reserved.", size=18, weight=400, fill="#666666") +
    lib.text(500, 570,
        "No part of this book may be reproduced, stored, or transmitted", size=15, weight=400, fill="#888888") +
    lib.text(500, 592,
        "in any form without prior written permission of the copyright owner,", size=15, weight=400, fill="#888888") +
    lib.text(500, 614,
        "except for personal, non-commercial use.", size=15, weight=400, fill="#888888") +
    lib.text(500, 680, "Illustrations designed for early learners, ages 2–6.", size=16, weight=400, fill="#888888") +
    lib.star(500, 780, 20, 9)
)
save("000_copyright.svg", copyright_body)

# -- 001 belongs-to page --------------------------------------------------
frame = lib.rrect(70, 70, 860, 860, 40, fill="#FFFFFF", sw=13)
belongs = (
    frame +
    lib.star(140, 140, 22, 10) + lib.star(860, 140, 22, 10) +
    lib.star(140, 860, 22, 10) + lib.star(860, 860, 22, 10) +
    lib.text(500, 300, "This Coloring Book", size=44, weight=900) +
    lib.text(500, 360, "Belongs To:", size=44, weight=900) +
    lib.path("M220,470 L780,470", sw=8) +
    cr.dino_round(280, 700, 0.9) + cr.bunny(560, 720, 0.7) +
    lib.flower(760, 640, 1.1) + lib.flower(190, 620, 0.9)
)
save("001_belongs.svg", belongs)

print("front matter done")
