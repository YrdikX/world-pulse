import os
from PIL import Image

BASE = os.path.dirname(__file__)
OUT = os.path.join(BASE, "out")

order = [
    "00_title.png", "000_copyright.png", "001_belongs.png",
    "01_dino.png", "02_triceratops.png", "03_longneck.png", "04_stegosaurus.png", "05_dino_egg.png",
    "06_car.png", "07_firetruck.png", "08_airplane.png", "09_rocket.png", "10_sailboat.png",
    "11_bunny.png", "12_bear.png", "13_cat.png", "14_elephant.png", "15_owl.png", "16_turtle.png",
    "17_garden.png", "18_bouquet.png", "19_sky.png", "20_balloons.png", "21_treats.png", "22_house.png",
    "23_friends.png", "24_practice.png",
]

DPI = 300
images = []
for name in order:
    im = Image.open(os.path.join(OUT, name)).convert("RGB")
    assert im.size == (2550, 2550), f"{name} wrong size: {im.size}"
    images.append(im)

pdf_path = os.path.join(BASE, "..", "interior.pdf")
images[0].save(pdf_path, save_all=True, append_images=images[1:], resolution=DPI)
print("wrote", pdf_path, "pages:", len(images))

sz = os.path.getsize(pdf_path)
print("size MB:", round(sz / 1024 / 1024, 2))
