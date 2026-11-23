#!/usr/bin/env python3
"""Draw the entry image for make.fun news-image-20261122.

A newspaper front page, 1024x1024, summarising the world news of
Sunday, 22 November 2026. Deterministic: fixed palette, fonts, layout
and text; Pillow only; no network, no timestamps, no randomness.
Run: python3 draw.py  -> writes entry.png next to this script.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 233)
INK = (20, 20, 20)
RED = (179, 39, 30)
BLUE = (27, 58, 92)
ORANGE = (214, 96, 20)
GREY = (110, 108, 100)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def wrap(text, fnt, width):
    """Greedy word wrap to a pixel width."""
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for w in words:
            trial = (cur + " " + w).strip()
            if d.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def text_block(x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = fnt.size + 6
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def rule(y, x0=28, x1=996, width=2, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- masthead
d.text((28, 30), "THE WORLD IN ONE DAY", font=SERIF_B(56), fill=INK)
d.text((28, 104), "SUNDAY, 22 NOVEMBER 2026", font=SANS_B(25), fill=RED)
d.text((560, 108), "Six stories that defined the day", font=SANS(22), fill=GREY)
rule(142, width=4)
rule(148, width=1)

# ---------------------------------------------------------------- lead: COP31
LX, LY = 28, 166
d.text((LX, LY), "CLIMATE  •  ANTALYA, TURKEY", font=SANS_B(20), fill=RED)
y = LY + 30
y = text_block(LX, y, ["COP31", "COLLAPSES"], SERIF_B(56), leading=60)
y += 6
y = text_block(
    LX, y,
    wrap("No deal on fossil fuels as the longest climate summit in history ends in failure.",
         SANS_B(22), 560), SANS_B(22), leading=27)
y += 8
y = text_block(
    LX, y,
    wrap("After two weeks of talks and two days of overtime, the EU and others rejected the "
         "final pact — it did not even mention fossil fuels. The first climate summit to "
         "collapse without a deal since Copenhagen in 2009.", SANS(19), 560),
    SANS(19), leading=24)

# Lead illustration: cracked globe + NO DEAL stamp (right of lead text)
GX, GY, GR = 800, 300, 118
d.ellipse([GX - GR, GY - GR, GX + GR, GY + GR], fill=(58, 110, 160), outline=INK, width=3)
d.ellipse([GX - 85, GY - 70, GX - 10, GY - 5], fill=(76, 140, 74))
d.ellipse([GX - 15, GY + 20, GX + 70, GY + 80], fill=(76, 140, 74))
d.ellipse([GX + 30, GY - 85, GX + 85, GY - 30], fill=(96, 155, 88))
d.arc([GX - GR, GY - GR, GX + GR, GY + GR], 200, 330, fill=(255, 255, 255), width=6)
d.arc([GX - GR, GY - GR, GX + GR, GY + GR], 20, 110, fill=(255, 255, 255), width=6)
# red crack across the globe
d.line([(GX - 70, GY - 95), (GX - 30, GY - 30), (GX - 55, GY + 10),
        (GX + 5, GY + 55), (GX - 10, GY + 100)], fill=RED, width=7, joint="curve")
# NO DEAL stamp
d.rectangle([GX - 118, GY + 52, GX + 118, GY + 96], fill=RED)
d.text((GX - 100, GY + 60), "NO DEAL", font=SANS_B(30), fill=(255, 255, 255))

rule(486, width=2)

# ---------------------------------------------------------------- row 2: two stories
def story2(x, y, w, kicker, color, headline, body, draw_icon):
    d.text((x, y), kicker, font=SANS_B(17), fill=color)
    yy = y + 26
    yy = text_block(x, yy, wrap(headline, SANS_B(24), w - 132), SANS_B(24), leading=28)
    yy += 4
    yy = text_block(x, yy, wrap(body, SANS(18), w - 132), SANS(18), leading=22)
    draw_icon(x + w - 118, y + 30)
    return yy

def icon_ukraine(ix, iy):
    # apartment block, one section collapsed, smoke and flame on top
    d.polygon([(ix + 20, iy), (ix + 34, iy + 16), (ix + 48, iy), (ix + 62, iy + 16),
               (ix + 76, iy)], fill=ORANGE)
    d.rectangle([ix, iy + 16, ix + 110, iy + 106], fill=(200, 190, 170), outline=INK, width=2)
    for r in range(3):
        for c in range(3):
            d.rectangle([ix + 12 + c * 32, iy + 28 + r * 26, ix + 30 + c * 32, iy + 46 + r * 26],
                        fill=(90, 90, 100), outline=INK, width=1)
    # collapsed corner: jagged dark polygon
    d.polygon([(ix + 78, iy + 16), (ix + 110, iy + 16), (ix + 110, iy + 106),
               (ix + 92, iy + 84), (ix + 100, iy + 58), (ix + 82, iy + 38)],
              fill=(60, 55, 50))
    d.ellipse([ix + 70, iy - 2, ix + 95, iy + 20], fill=(150, 148, 140))
    d.ellipse([ix + 88, iy - 12, ix + 112, iy + 10], fill=(170, 168, 160))

def icon_bahrain(ix, iy):
    # missile streak + flame burst over a base
    d.rectangle([ix, iy + 78, ix + 110, iy + 106], fill=(200, 190, 170), outline=INK, width=2)
    d.rectangle([ix + 14, iy + 88, ix + 30, iy + 106], fill=GREY)
    d.rectangle([ix + 80, iy + 88, ix + 96, iy + 106], fill=GREY)
    d.polygon([(ix + 18, iy + 6), (ix + 34, iy + 32), (ix + 52, iy + 58), (ix + 40, iy + 64),
               (ix + 24, iy + 38)], fill=(60, 60, 70))
    d.polygon([(ix + 34, iy + 32), (ix + 44, iy + 50), (ix + 30, iy + 46)], fill=RED)
    d.polygon([(ix + 52, iy + 58), (ix + 66, iy + 76), (ix + 78, iy + 60), (ix + 92, iy + 72),
               (ix + 84, iy + 54), (ix + 96, iy + 60), (ix + 80, iy + 42)],
              fill=ORANGE)

story2(28, 506, 470, "WAR IN UKRAINE  •  DYMER, NEAR KYIV", RED,
       "Drone hits Kyiv flats — 14 missing",
       "A Russian drone collapsed part of a five-storey block; nine people were evacuated. "
       "Hours later rescuers pulled a boy, 7, alive from the rubble.",
       icon_ukraine)
story2(528, 506, 468, "GULF  •  BAHRAIN", RED,
       "Iran strikes Bahrain — two hurt",
       "Missiles and drones hit US bases and a civilian plant on Sitra island. Bahrain says "
       "two people were injured; Gulf states condemned the attacks.",
       icon_bahrain)

rule(700, width=2)

# ---------------------------------------------------------------- row 3: three stories
def story3(x, y, w, kicker, color, headline, body):
    d.rectangle([x, y + 2, x + 10, y + 12], fill=color)
    d.text((x + 16, y), kicker, font=SANS_B(16), fill=color)
    yy = y + 26
    yy = text_block(x, yy, wrap(headline, SANS_B(21), w), SANS_B(21), leading=25)
    yy += 4
    yy = text_block(x, yy, wrap(body, SANS(17), w), SANS(17), leading=21)
    return yy

story3(28, 720, 300, "INDONESIA  •  CIKANDE, BANTEN", RED,
       "Factory fire: 3 dead, 36 missing",
       "Rescuers searched the burned candy factory on Sunday, a day after the blaze. "
       "Dozens of body bags were recovered; DNA tests will identify the victims.")
story3(362, 720, 300, "SPACE  •  MERCURY", BLUE,
       "BepiColombo reaches Mercury",
       "After an eight-year journey, the European-Japanese craft entered orbit around "
       "Mercury. A thruster glitch cut the burn short; the craft is safe.")
story3(696, 720, 300, "NATO  •  POLAND", RED,
       "Three Russian missiles entered Poland",
       "Prosecutors confirmed on Sunday that three Russian Kh-101 missiles flew into Polish "
       "airspace on Friday. NATO meets in Brussels on Monday.")

# ---------------------------------------------------------------- footer
rule(956, width=2)
d.text((28, 968), "Sources: Reuters  •  AP  •  CNN  •  ESA  •  Le Monde  —  Events reported on Sunday, 22 November 2026.",
       font=SANS(16), fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
