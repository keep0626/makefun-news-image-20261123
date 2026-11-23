"""Draw Monday 23 November 2026 world news as one 1024x1024 front page.

Reads stories.json next to this file and writes entry.png next to it.
Standard library + Pillow only. Output is deterministic: same input bytes
always produce the same PNG bytes.
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (253, 248, 239)
INK = (17, 17, 17)
RED = (185, 28, 28)
NAVY = (30, 58, 95)
TEAL = (15, 118, 110)
GOLD = (180, 83, 9)
GREY = (90, 90, 90)
LIGHT_BLUE = (207, 227, 240)
LAND = (232, 220, 195)
CARD_BG = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SERIF_I = lambda s: font("DejaVuSerif.ttf", s)  # no italic face installed
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_one_line(draw, text, fnt, max_w):
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    while text and draw.textlength(text + "...", font=fnt) > max_w:
        text = text[:-1]
    return text + "..."


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, spacing=4):
    lines = wrap(draw, text, fnt, max_w)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


# ---------------- flat picture panels (all drawn in code) ----------------

def pic_hormuz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(23, 78, 130))
    d.rectangle([x + 18, y + h * 0.42, x + w - 18, y + h * 0.62], fill=(40, 40, 40))
    for i in range(4):
        cx = x + 34 + i * 62
        d.rectangle([cx, y + h * 0.28, cx + 44, y + h * 0.42], fill=(180, 83, 9))
    d.rectangle([x + w - 52, y + h * 0.18, x + w - 38, y + h * 0.42], fill=(220, 220, 220))
    for cx, cy, r in ((x + 62, y + 26, 10), (x + 150, y + 18, 8), (x + 250, y + 30, 9)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(250, 160, 40))
        d.ellipse([cx - r * 2, cy - r * 2, cx + r * 2, cy + r * 2],
                  outline=(250, 200, 80), width=2)
    d.ellipse([x + 205, y + h - 26, x + 225, y + h - 6], fill=(20, 20, 20))
    d.ellipse([x + 215, y + h - 16, x + 235, y + h + 4], fill=(20, 20, 20))
    d.text((x + 10, y + h - 22), "STRAIT OF HORMUZ", font=SANS_B(13), fill=(255, 255, 255))


def pic_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 240, 228))
    d.ellipse([x + 24, y + 14, x + 104, y + 94], fill=(46, 125, 70))
    d.ellipse([x + 40, y + 30, x + 70, y + 52], fill=(120, 180, 120))
    d.ellipse([x + 66, y + 58, x + 96, y + 82], fill=(120, 180, 120))
    d.rectangle([x + 150, y + 18, x + 164, y + 78], fill=(200, 200, 200),
                outline=RED, width=2)
    d.ellipse([x + 144, y + 74, x + 170, y + 100], fill=RED)
    d.rectangle([x + 150, y + 34, x + 164, y + 62], fill=RED)
    d.text((x + 186, y + 22), "FOSSIL", font=SANS_B(22), fill=INK)
    d.text((x + 186, y + 48), "FUELS", font=SANS_B(22), fill=INK)
    d.line([x + 180, y + 34, x + 268, y + 66], fill=RED, width=5)
    d.line([x + 180, y + 66, x + 268, y + 34], fill=RED, width=5)
    d.text((x + 10, y + h - 22), "ANTALYA · NO DEAL", font=SANS_B(13), fill=RED)


def pic_libya(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 235))
    d.rectangle([x, y + h * 0.66, x + w, y + h], fill=(90, 130, 170))
    d.polygon([(x + 30, y + h * 0.66), (x + 60, y + h * 0.40),
               (x + 240, y + h * 0.40), (x + 280, y + h * 0.66)],
              fill=(70, 70, 78))
    d.rectangle([x + 90, y + h * 0.26, x + 170, y + h * 0.40], fill=(70, 70, 78))
    d.rectangle([x + 185, y + h * 0.18, x + 195, y + h * 0.40], fill=(70, 70, 78))
    d.polygon([(x + 120, y + h * 0.66), (x + 150, y + h * 0.80),
               (x + 190, y + h * 0.66)], fill=(60, 60, 66))
    for cx, cy in ((x + 130, y + 22), (x + 165, y + 14), (x + 200, y + 24)):
        d.ellipse([cx - 12, cy - 8, cx + 12, cy + 8], fill=(120, 120, 120))
    d.rectangle([x + 235, y + 16, x + 265, y + 26], fill=(40, 40, 40))
    d.line([x + 250, y + 26, x + 250, y + 40], fill=(40, 40, 40), width=3)
    d.ellipse([x + 238, y + 38, x + 262, y + 48], fill=(40, 40, 40))
    d.text((x + 10, y + h - 22), "BENGHAZI NAVAL BASE", font=SANS_B(13), fill=INK)


def pic_dymer(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 225, 210))
    d.rectangle([x + 14, y + 12, x + 52, y + h - 8], fill=(120, 110, 100))
    for row in range(4):
        for col in range(2):
            wx = x + 19 + col * 17
            wy = y + 18 + row * 15
            d.rectangle([wx, wy, wx + 11, wy + 9], fill=(250, 220, 90))
    d.polygon([(x + 14, y + 12), (x + 33, y - 2), (x + 52, y + 12)], fill=(90, 80, 70))
    d.ellipse([x + 58, y + 10, x + 74, y + 26], fill=(150, 150, 150))
    d.ellipse([x + 66, y + 4, x + 80, y + 18], fill=(170, 170, 170))


def pic_poland(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 240))
    d.polygon([(x + 8, y + 40), (x + 48, y + 22), (x + 62, y + 30),
               (x + 62, y + 50), (x + 48, y + 58)], fill=(90, 90, 96))
    d.ellipse([x + 54, y + 34, x + 62, y + 46], fill=RED)
    for i in range(3):
        d.line([x + 8 - i * 4, y + 44, x + 14 - i * 4, y + 44],
               fill=(200, 120, 40), width=2)


def pic_mexico(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 232, 214))
    d.ellipse([x + 18, y + 16, x + 62, y + 60], outline=(60, 60, 60), width=5)
    d.ellipse([x + 34, y + 32, x + 78, y + 76], outline=(60, 60, 60), width=5)
    d.line([x + 40, y + 38, x + 56, y + 54], fill=(60, 60, 60), width=4)


def pic_markets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    pts = [(x + 8, y + 14), (x + 24, y + 26), (x + 40, y + 22),
           (x + 56, y + 44), (x + 72, y + 60), (x + 86, y + 78)]
    d.line(pts, fill=(250, 80, 80), width=4, joint="curve")
    d.polygon(pts + [(x + 86, y + h - 6), (x + 8, y + h - 6)],
              fill=(250, 80, 80, 90))


def pic_space(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 16, 32))
    d.ellipse([x + 8, y + 18, x + 52, y + 62], fill=(200, 170, 140))
    d.ellipse([x + 16, y + 26, x + 28, y + 38], fill=(170, 140, 110))
    d.ellipse([x + 34, y + 42, x + 44, y + 52], fill=(170, 140, 110))
    d.rectangle([x + 58, y + 34, x + 76, y + 46], fill=(220, 220, 220))
    d.rectangle([x + 76, y + 28, x + 92, y + 52], fill=(120, 160, 220))
    for sx, sy in ((x + 80, y + 12), (x + 92, y + 60), (x + 60, y + 66)):
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))


def pic_alcaraz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 240, 200))
    d.polygon([(x + 34, y + 14), (x + 62, y + 14), (x + 58, y + 44),
               (x + 38, y + 44)], fill=(212, 175, 55))
    d.ellipse([x + 28, y + 18, x + 40, y + 36], outline=(212, 175, 55), width=4)
    d.ellipse([x + 56, y + 18, x + 68, y + 36], outline=(212, 175, 55), width=4)
    d.rectangle([x + 44, y + 44, x + 52, y + 56], fill=(212, 175, 55))
    d.rectangle([x + 34, y + 56, x + 62, y + 62], fill=(212, 175, 55))


PICS = {1: pic_hormuz, 2: pic_cop, 3: pic_libya, 4: pic_dymer,
        5: pic_poland, 6: pic_mexico, 7: pic_markets, 8: pic_space,
        9: pic_alcaraz}

# ---------------- page layout ----------------

REGION_COUNTS = [("ASIA", 5, (180, 83, 9)), ("MIDDLE EAST", 4, RED),
                 ("EUROPE", 7, NAVY), ("AMERICAS", 6, TEAL),
                 ("AFRICA", 2, (120, 90, 40)), ("GLOBAL", 8, (90, 60, 140))]
NUMBERS = [("6", "tankers hit mines\nSun-Mon, Hormuz"),
           ("128", "nations back killer-\nrobot rules by 2028"),
           ("24", "bodies found in\nIndonesia factory fire"),
           ("538", "Lahore AQI, worst\nin the world"),
           ("-17.5%", "Taiwan stocks\nin one week"),
           ("2 / 11", "dead / missing in\nKyiv-area strike")]
REGION_COLORS = {"Middle East": RED, "Africa": (120, 90, 40),
                 "Europe": NAVY, "Asia": (180, 83, 9),
                 "Americas": TEAL, "Global": (90, 60, 140)}


def draw_region_bar(d, y):
    x = 24
    total_w = W - 48
    for name, count, color in REGION_COUNTS:
        seg_w = int(total_w * count / 32)
        d.rectangle([x, y, x + seg_w - 2, y + 26], fill=color)
        label = "%s %d" % (name, count)
        tw = d.textlength(label, font=SANS_B(13))
        d.text((x + (seg_w - 2 - tw) / 2, y + 6), label,
               font=SANS_B(13), fill=(255, 255, 255))
        x += seg_w
    return y + 26


def draw_numbers(d, y):
    box_w = (W - 48 - 5 * 8) / 6
    x = 24
    for num, cap in NUMBERS:
        d.rectangle([x, y, x + box_w, y + 52], outline=(200, 190, 175), width=1)
        nw = d.textlength(num, font=SANS_B(24))
        d.text((x + (box_w - nw) / 2, y + 3), num, font=SANS_B(24), fill=RED)
        for i, line in enumerate(cap.split("\n")):
            lw = d.textlength(line, font=SANS(10))
            d.text((x + (box_w - lw) / 2, y + 30 + i * 12), line,
                   font=SANS(10), fill=GREY)
        x += box_w + 8
    return y + 52


def draw_lead(d, story, x, y, w):
    PICS[story["n"]](d, x, y, w, 118)
    y += 124
    tag = "%d · %s" % (story["n"], story["place"])
    d.text((x, y), tag, font=SANS_B(13), fill=RED)
    y += 18
    y = draw_wrapped(d, x, y, story["headline"], SERIF_B(23), w, spacing=2)
    y += 2
    y = draw_wrapped(d, x, y, story["deck"], SANS(13), w, spacing=2)
    y += 4
    d.text((x, y), story["source"], font=SANS_B(10), fill=GREY)
    return y


def draw_card(d, story, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=(210, 200, 185),
                width=1)
    PICS[story["n"]](d, x + 6, y + 6, 84, h - 12)
    tx = x + 98
    tw = w - 106
    tag = "%d · %s" % (story["n"], story["place"])
    d.text((tx, y + 6), fit_one_line(d, tag, SANS_B(11), tw),
           font=SANS_B(11), fill=RED)
    hy = draw_wrapped(d, tx, y + 22, story["headline"], SANS_B(14), tw,
                      spacing=1)
    draw_wrapped(d, tx, hy + 1, story["deck"], SANS(11), tw, spacing=1,
                 fill=(60, 60, 60))


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=LIGHT_BLUE, outline=(180, 190, 200),
                width=1)
    polys = [
        [(28, 22), (88, 16), (108, 30), (96, 54), (62, 58), (42, 44), (24, 36)],
        [(72, 76), (94, 70), (104, 94), (86, 124), (74, 100)],
        [(138, 26), (162, 20), (172, 40), (154, 50), (140, 40)],
        [(138, 60), (168, 55), (178, 84), (160, 114), (144, 90)],
        [(174, 20), (248, 14), (268, 44), (238, 68), (200, 58), (178, 44)],
        [(232, 104), (262, 100), (268, 118), (240, 124)],
    ]
    for poly in polys:
        d.polygon([(x + px * w / 276, y + py * h / 262) for px, py in poly],
                  fill=LAND)
    pins = {1: (216, 56), 2: (168, 50), 3: (146, 70), 4: (180, 32),
            5: (158, 26), 6: (50, 56), 7: (56, 36), 8: (250, 18), 9: (128, 48)}
    for n, (px, py) in pins.items():
        px, py = px * w / 276, py * h / 262
        d.ellipse([x + px - 8, y + py - 8, x + px + 8, y + py + 8],
                  fill=RED, outline=(255, 255, 255), width=1)
        tw = d.textlength(str(n), font=SANS_B(10))
        d.text((x + px - tw / 2, y + py - 6), str(n), font=SANS_B(10),
               fill=(255, 255, 255))
    d.text((x + 8, y + h - 18), "PINS 1-9 = PICTURED STORIES",
           font=SANS_B(10), fill=NAVY)


def build():
    with open(os.path.join(HERE, "stories.json"), encoding="utf-8") as f:
        data = json.load(f)
    stories = {s["n"]: s for s in data["stories"]}
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 4], fill=RED)

    # masthead: the date is the biggest element on the page
    kicker = "32 STORIES  ·  6 REGIONS  ·  EVERY ONE FROM THIS MONDAY"
    kw = d.textlength(kicker, font=SANS_B(14))
    d.text(((W - kw) / 2, 10), kicker, font=SANS_B(14), fill=RED)
    date = "Monday 23 November 2026"
    dw = d.textlength(date, font=SERIF_B(60))
    d.text(((W - dw) / 2, 28), date, font=SERIF_B(60), fill=INK)
    sub = "Hormuz tankers hit mines  ·  COP31 collapses  ·  Russian warship sunk off Libya"
    sw = d.textlength(sub, font=SERIF_I(16))
    d.text(((W - sw) / 2, 96), sub, font=SERIF_I(16), fill=RED)
    d.line([24, 118, W - 24, 118], fill=INK, width=2)

    y = draw_region_bar(d, 124)
    y = draw_numbers(d, y + 6)

    # three lead stories
    lead_y = y + 10
    for i, n in enumerate((1, 2, 3)):
        draw_lead(d, stories[n], 24 + i * 328, lead_y, 312)
    d.line([24, lead_y + 252, W - 24, lead_y + 252], fill=(200, 190, 175),
           width=1)

    # six picture cards, two rows of three
    card_y = lead_y + 262
    for row, nums in enumerate(((4, 5, 6), (7, 8, 9))):
        for i, n in enumerate(nums):
            draw_card(d, stories[n], 24 + i * 328, card_y + row * 92, 312, 86)

    # map + numbered briefs
    by = card_y + 190
    d.text((24, by), "ALSO ON MONDAY 23 NOVEMBER",
           font=SANS_B(14), fill=INK)
    d.line([24, by + 20, W - 24, by + 20], fill=INK, width=1)
    map_y = by + 26
    draw_map(d, 24, map_y, 240, 262)
    briefs = [s for s in data["stories"] if "brief" in s]
    col_w = 354
    for idx, s in enumerate(briefs):
        col = idx // 12
        row = idx % 12
        bx = 280 + col * (col_w + 12)
        yy = map_y + row * 22
        num = "%d." % s["n"]
        d.text((bx, yy), num, font=SANS_B(11), fill=RED)
        nw = d.textlength(num + " ", font=SANS_B(11))
        label = "%s — %s" % (s["place"], s["brief"])
        d.text((bx + nw, yy),
               fit_one_line(d, label, SANS(11), col_w - nw),
               font=SANS(11), fill=INK)

    # DATE CHECK box
    cy = map_y + 268
    d.rectangle([24, cy, W - 24, cy + 44], outline=RED, width=2)
    check = ("DATE CHECK — Left out as other days' news: Friday's US market slide "
             "(20 Nov) and the 20 Nov Poland impacts themselves — today's news is the "
             "Kh-101 confirmation and NATO's meeting. Not yet: the outcome of NATO's "
             "Monday council; COP31's formal closing papers.")
    draw_wrapped(d, 34, cy + 5, check, SANS(11), W - 68, fill=INK, spacing=1)

    # footer
    fy = cy + 50
    foot = ("Sources: AP · Reuters · CNN · WSJ · Al Jazeera · BBC · ESA/JAXA · ATP · official statements. "
            "CONFIRMED = on the record · REPORTED = as reported · CLAIM = one side's account.")
    d.text((24, fy), fit_one_line(d, foot, SANS(10), W - 48), font=SANS(10),
           fill=GREY)
    img.save(os.path.join(HERE, "entry.png"), "PNG", optimize=True)


if __name__ == "__main__":
    build()
