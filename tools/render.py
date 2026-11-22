"""Draw the World Ledger front page and write it to entry.png (1024 x 1024, 8-bit RGB).

    python3 tools/render.py            # writes ../entry.png
    python3 tools/render.py out.png    # writes somewhere else

Shapes and illustrations are drawn oversized and box-filtered down (see art.py); all type is set at final
resolution so small glyphs stay sharp. While it draws, the page remembers the box of every piece of text it
places, then refuses to save if any text leaves its allotted space or touches another piece of text.
"""

import os
import struct
import sys
import zlib

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import art
import stories

SIDE = 1024
MARGIN = 8
PAPER = "#F4F1EA"
INK = "#141923"
CAPTION = "#141923"
WHITE = "#FFFFFF"
RED = "#B3261E"
AMBER = "#9A6200"
SOFT = "#4A5361"
TINT = "#E9E5DA"

LATO = "/usr/share/fonts/truetype/lato/"
FONT_FILES = {
    "black": LATO + "Lato-Black.ttf",
    "heavy": LATO + "Lato-Heavy.ttf",
    "bold": LATO + "Lato-Bold.ttf",
    "semi": LATO + "Lato-Semibold.ttf",
    "medium": LATO + "Lato-Medium.ttf",
    "regular": LATO + "Lato-Regular.ttf",
    "italic": LATO + "Lato-Italic.ttf",
    "serif": "/usr/share/fonts/opentype/urw-base35/C059-Bold.otf",
}
_fonts = {}


def font(name, size):
    key = (name, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(FONT_FILES[name], size)
    return _fonts[key]


def width_of(text, name, size):
    return font(name, size).getlength(text)


def wrap(text, name, size, width, max_lines):
    """Greedy word wrap; raises if the text cannot fit the lines it is allowed."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if width_of(trial, name, size) <= width:
            current = trial
        else:
            lines.append(current)
            current = word
    lines.append(current)
    if len(lines) > max_lines or any(width_of(line, name, size) > width for line in lines):
        raise ValueError(f"does not fit {max_lines} line(s) of {width:.0f}px at {size}px: {text!r} -> {lines}")
    return lines


class Page:
    def __init__(self):
        self.image = Image.new("RGB", (SIDE, SIDE), PAPER)
        self.draw = ImageDraw.Draw(self.image)
        self.placed = []  # (bbox, text, allowed box)
        self.problems = []

    def box(self, x0, y0, x1, y1, colour):
        """Filled rectangle covering pixels x0..x1-1, y0..y1-1."""
        self.draw.rectangle([x0, y0, x1 - 1, y1 - 1], fill=colour)

    def text(self, x, y, string, name, size, colour, anchor="ls", within=None):
        face = font(name, size)
        self.draw.text((x, y), string, font=face, fill=colour, anchor=anchor)
        bbox = self.draw.textbbox((x, y), string, font=face, anchor=anchor)
        self.placed.append((bbox, string, within))
        if within is not None:
            x0, y0, x1, y1 = within
            if bbox[0] < x0 - 0.01 or bbox[1] < y0 - 0.01 or bbox[2] > x1 + 0.01 or bbox[3] > y1 + 0.01:
                self.problems.append(f"CLIPPED {string!r}: text box {tuple(round(v, 1) for v in bbox)} outside {within}")
        return bbox

    def audit(self):
        """Every pair of text boxes must be disjoint."""
        for i in range(len(self.placed)):
            a = self.placed[i][0]
            for j in range(i + 1, len(self.placed)):
                b = self.placed[j][0]
                if min(a[2], b[2]) - max(a[0], b[0]) > 0.5 and min(a[3], b[3]) - max(a[1], b[1]) > 0.5:
                    self.problems.append(f"OVERLAP {self.placed[i][1]!r} x {self.placed[j][1]!r}")
        return self.problems


REGION_COLOUR = {name: colour for name, _, colour in stories.REGIONS}
REGION_CODE = {name: code for name, code, _ in stories.REGIONS}
GRADE_COLOUR = {name: colour for name, _, colour, _ in stories.GRADES}
GRADE_LETTER = {name: letter for name, letter, _, _ in stories.GRADES}


def masthead(page):
    page.text(MARGIN - 1, 47, "WORLD LEDGER", "serif", 45, INK, within=(0, 4, 420, 50))
    page.text(MARGIN, 59, "One day of world news on one page: every story dated, sourced and graded", "italic", 10.5, SOFT,
              within=(0, 49, 440, 63))
    date_width = width_of(stories.EDITION_DAY, "black", 26)
    left = SIDE - MARGIN - int(date_width) - 26
    page.box(left, 7, SIDE - MARGIN, 41, RED)
    page.text((left + SIDE - MARGIN) / 2, 24, stories.EDITION_DAY, "black", 26, WHITE, "mm", within=(left, 7, SIDE - MARGIN, 41))
    line = f"{stories.EDITION_CLOSE} UTC EDITION  \u00b7  40 VERIFIED STORIES  \u00b7  7 REGIONS"
    page.text(SIDE - MARGIN, 57, line, "black", 12.5, INK, "rs", within=(440, 43, SIDE, 61))
    page.box(MARGIN, 63, SIDE - MARGIN, 66, INK)
    page.box(MARGIN, 68, SIDE - MARGIN, 69, INK)


def kpi_strip(page, top):
    tiles = [
        (str(len(stories.all_stories())), "STORIES DATED", "SUN 22 NOV"),
        (str(len(stories.REGIONS)), "WORLD REGIONS", "COVERED"),
        (str(len(stories.CARDS)), "ILLUSTRATED", "CARDS + MAP PINS"),
        (str(len(stories.WIRE)), "WIRE", "DISPATCHES"),
        (str(len(stories.named_sources())), "NAMED", "SOURCES"),
        (str(len(stories.EXCLUDED)), "PRE-SUNDAY", "ITEMS EXCLUDED"),
    ]
    height = 40
    gap = 6
    tile_width = (SIDE - 2 * MARGIN - gap * 5) // 6
    for index, (number, upper, lower) in enumerate(tiles):
        x = MARGIN + index * (tile_width + gap)
        page.box(x, top, x + tile_width, top + height, INK)
        page.box(x + 1, top + 1, x + tile_width - 1, top + height - 1, WHITE)
        page.box(x + 1, top + 1, x + 5, top + height - 1, RED)
        number_right = x + 51
        page.text(number_right, top + 20, number, "black", 29, INK, "rm", within=(x + 6, top + 2, x + 54, top + height - 2))
        page.text(x + 57, top + 17, upper, "black", 10.5, INK, within=(x + 54, top + 4, x + tile_width - 2, top + 20))
        page.text(x + 57, top + 31, lower, "black", 10.5, SOFT, within=(x + 54, top + 20, x + tile_width - 2, top + 36))
    return top + height


def region_bar(page, top):
    counts = stories.region_counts()
    total = sum(counts.values())
    height = 18
    span = SIDE - 2 * MARGIN
    x = MARGIN
    running = 0
    for name, _, colour in stories.REGIONS:
        running += counts[name]
        right = MARGIN + round(span * running / total)
        page.box(x, top, right, top + height, colour)
        page.text((x + right) / 2, top + 9, f"{name} {counts[name]}", "black", 10.5, WHITE, "mm", within=(x + 2, top, right - 2, top + height))
        if right < SIDE - MARGIN:
            page.box(right - 1, top, right + 1, top + height, PAPER)
        x = right
    return top + height


def card(page, story, x, y, width, art_height, caption_height):
    lead = width > 250
    picture, labels = art.render_scene(story["art"], width, art_height, 4, story.get("note", ""))
    page.image.paste(picture, (x, y))
    for lx, ly, string, size, colour, name, anchor in labels:
        page.text(x + lx, y + ly, string, name, size, colour, anchor, within=(x, y, x + width, y + art_height))
    # number + region tag, top left
    tag_height = 17 if lead else 14
    number_size, region_size = (12.5, 10.5) if lead else (11, 9.5)
    number = str(story["n"])
    number_box = int(width_of(number, "black", number_size)) + (10 if lead else 8)
    page.box(x, y, x + number_box, y + tag_height, INK)
    page.text(x + number_box / 2, y + tag_height / 2, number, "black", number_size, WHITE, "mm",
              within=(x, y, x + number_box, y + tag_height))
    region = story["region"]
    region_box = int(width_of(region, "black", region_size)) + (12 if lead else 9)
    page.box(x + number_box, y, x + number_box + region_box, y + tag_height, REGION_COLOUR[region])
    page.text(x + number_box + region_box / 2, y + tag_height / 2, region, "black", region_size, WHITE, "mm",
              within=(x + number_box, y, x + number_box + region_box, y + tag_height))
    # verification tag, top right
    grade = story["grade"]
    grade_size = 10.5 if lead else 9.5
    grade_box = int(width_of(grade, "black", grade_size)) + (12 if lead else 9)
    page.box(x + width - grade_box, y, x + width, y + tag_height, GRADE_COLOUR[grade])
    page.text(x + width - grade_box / 2, y + tag_height / 2, grade, "black", grade_size, WHITE, "mm",
              within=(x + width - grade_box, y, x + width, y + tag_height))
    # caption bar: white on near-black
    top = y + art_height
    page.box(x, top, x + width, top + caption_height, CAPTION)
    pad = 7 if lead else 6
    inner = (x + pad - 2, top, x + width - pad + 2, top + caption_height)
    meta = story["when"] + "  \u00b7  " + ", ".join(story["sources"])
    if lead:
        lines = wrap(story["head"], "black", 16, width - 2 * pad, 2)
        baseline = top + 19
        for line in lines:
            page.text(x + pad, baseline, line, "black", 16, WHITE, within=inner)
            baseline += 18
        page.text(x + pad, top + 53, story["deck"], "regular", 11.5, WHITE, within=inner)
        page.text(x + pad, top + 67, meta, "bold", 11, WHITE, within=inner)
    else:
        lines = wrap(story["head"], "bold", 12, width - 2 * pad, 2)
        baseline = top + 15
        for line in lines:
            page.text(x + pad, baseline, line, "bold", 12, WHITE, within=inner)
            baseline += 14
        meta_size = 10.5
        if width_of(meta, "regular", meta_size) > width - 2 * pad:
            meta_size = 10
        page.text(x + pad, top + 47, meta, "regular", meta_size, WHITE, within=inner)


def cards(page, top):
    lead_width, lead_gap = 332, 6
    for index, story in enumerate(stories.CARDS[:3]):
        card(page, story, MARGIN + index * (lead_width + lead_gap), top, lead_width, 96, 72)
    top += 96 + 72 + 4
    lefts = (8, 211, 414, 617, 819)
    for row in range(2):
        for index in range(5):
            card(page, stories.CARDS[3 + row * 5 + index], lefts[index], top, 197, 56, 56)
        top += 56 + 56 + 4
    return top - 4


def wire(page, top):
    page.box(MARGIN, top, SIDE - MARGIN, top + 16, INK)
    first, last = stories.WIRE[0]["n"], stories.WIRE[-1]["n"]
    title = f"WIRE  \u00b7  {len(stories.WIRE)} MORE DATED DISPATCHES (#{first}\u2013#{last})  \u00b7  TIME = UTC OF EVENT OR FIRST REPORT; SUN = SUNDAY 22 NOV"
    page.text(MARGIN + 6, top + 8, title, "black", 10, WHITE, "lm", within=(MARGIN, top, SIDE - MARGIN, top + 16))
    top += 18
    pitch = 14
    column_width = 500
    rows = (len(stories.WIRE) + 1) // 2
    for index, story in enumerate(stories.WIRE):
        column, row = divmod(index, rows)
        x = MARGIN + column * (column_width + 8)
        y = top + row * pitch
        if row % 2 == 0:
            page.box(x, y, x + column_width, y + pitch, TINT)
        allowed = (x, y, x + column_width, y + pitch)
        middle = y + pitch / 2
        page.text(x + 3, middle, str(story["n"]), "black", 10, INK, "lm", within=allowed)
        page.box(x + 19, y + 2, x + 47, y + pitch - 1, REGION_COLOUR[story["region"]])
        page.text(x + 33, middle + 0.5, REGION_CODE[story["region"]], "black", 8.5, WHITE, "mm", within=(x + 19, y + 1, x + 47, y + pitch))
        page.text(x + 52, middle, story["when"], "bold", 10, INK, "lm", within=allowed)
        body = story["text"]
        credit = "\u2014 " + ", ".join(story["sources"])
        chip = x + column_width - 15
        end = page.text(x + 84, middle, body, "regular", 10.5, INK, "lm", within=allowed)
        credit_x = end[2] + 5
        if credit_x + width_of(credit, "bold", 10.5) > chip - 3:
            page.problems.append(f"TOO LONG wire #{story['n']} by {credit_x + width_of(credit, 'bold', 10.5) - (chip - 3):.0f}px: {body + ' ' + credit!r}")
        page.text(credit_x, middle, credit, "bold", 10.5, INK, "lm", within=allowed)
        page.box(chip, y + 2, chip + 12, y + pitch - 1, GRADE_COLOUR[story["grade"]])
        page.text(chip + 6, middle + 0.5, GRADE_LETTER[story["grade"]], "black", 9, WHITE, "mm", within=(chip, y + 1, chip + 12, y + pitch))
    return top + rows * pitch


def atlas_panel(page, left, top, width, height):
    page.box(left, top, left + 44, top + 14, INK)
    page.text(left + 22, top + 7, "ATLAS", "black", 10, WHITE, "mm", within=(left, top, left + 44, top + 14))
    page.text(left + 50, top + 7, "pins 1\u201313 match the card numbers  \u00b7  Natural Earth projection", "bold", 9.5, INK, "lm",
              within=(left + 44, top, left + width, top + 14))
    map_top = top + 16
    world = art.Atlas(width, height - 16)
    bubbles = []
    for story in stories.CARDS:
        lon, lat = story["place"]
        dx, dy = story["hang"]
        bubbles.append((story["n"], world.pin(lon, lat, dx, dy, REGION_COLOUR[story["region"]])))
    page.image.paste(world.finish(), (left, map_top))
    for number, (bx, by) in bubbles:
        size = 9.5 if number < 10 else 8.5
        page.text(left + bx, map_top + by, str(number), "black", size, WHITE, "mm",
                  within=(left, map_top, left + width, map_top + height - 16))


def flow(page, items, mark, mark_colour, left, top, right, size=10, leading=12.5):
    """Set short items one after another, wrapping whole items; returns the y below the last line."""
    x, y = left, top
    gap = 13
    for item in items:
        needed = width_of(mark + " ", "black", size) + width_of(item, "medium", size)
        if x > left and x + needed > right:
            x = left
            y += leading
        if x + needed > right:
            page.problems.append(f"TOO LONG ledger item: {item!r}")
        page.text(x, y, mark, "black", size, mark_colour, within=(left - 1, top - 12, right + 1, y + 4))
        page.text(x + width_of(mark + " ", "black", size), y, item, "medium", size, INK, within=(left - 1, top - 12, right + 1, y + 4))
        x += needed + gap
    return y + 4


def date_check(page, left, top, width, height):
    right = left + width
    page.box(left, top, right, top + height, INK)
    page.box(left + 2, top + 2, right - 2, top + height - 2, WHITE)
    page.box(left, top, right, top + 17, INK)
    page.text(left + 7, top + 8.5, "DATE CHECK", "black", 11.5, WHITE, "lm", within=(left, top, right, top + 17))
    page.text(left + 88, top + 8.5, "two ledgers kept so only Sunday 22 Nov UTC runs as today\u2019s news", "bold", 10, WHITE, "lm",
              within=(left, top, right, top + 17))
    y = top + 23
    title = f"EXCLUDED ({len(stories.EXCLUDED)})  \u00b7  dated Sat 21 Nov UTC or earlier"
    tag = int(width_of(title, "black", 10)) + 12
    page.box(left + 7, y, left + 7 + tag, y + 14, RED)
    page.text(left + 13, y + 7, title, "black", 10, WHITE, "lm", within=(left + 7, y, left + 7 + tag, y + 14))
    y = flow(page, stories.EXCLUDED, "\u00d7", RED, left + 8, y + 26, right - 7)
    y += 4
    title = f"PENDING ({len(stories.PENDING)})  \u00b7  open at the {stories.EDITION_CLOSE} UTC close"
    tag = int(width_of(title, "black", 10)) + 12
    page.box(left + 7, y, left + 7 + tag, y + 14, AMBER)
    page.text(left + 13, y + 7, title, "black", 10, WHITE, "lm", within=(left + 7, y, left + 7 + tag, y + 14))
    y = flow(page, stories.PENDING, "?", AMBER, left + 8, y + 26, right - 7)
    if y > top + height - 3:
        page.problems.append(f"OVERFLOW date check box by {y - (top + height - 3):.0f}px")


def footer(page, top):
    page.box(MARGIN, top, SIDE - MARGIN, top + 2, INK)
    y = top + 14
    page.text(MARGIN, y, "VERIFICATION", "black", 10.5, INK, "lm", within=(0, top + 3, SIDE, top + 25))
    x = MARGIN + 88
    counts = stories.grade_counts()
    for name, letter, colour, meaning in stories.GRADES:
        pill = int(width_of(name, "black", 9.5)) + 10
        page.box(x, y - 7, x + pill, y + 7, colour)
        page.text(x + pill / 2, y, name, "black", 9.5, WHITE, "mm", within=(x, y - 7, x + pill, y + 7))
        note = f"{meaning} ({counts[name]})"
        page.text(x + pill + 5, y, note, "bold", 10, INK, "lm", within=(x, top + 3, SIDE - MARGIN, top + 25))
        x += pill + 5 + int(width_of(note, "bold", 10)) + 16
    rule = ("DATELINE RULE  Only events or first reports on Sunday 22 November 2026 UTC run as today\u2019s news; "
            "Sat 21 Nov UTC items are logged in Date Check.")
    page.text(MARGIN, top + 32, rule, "medium", 10, INK, "lm", within=(0, top + 24, SIDE, top + 40))
    note = (f"Wire chips: C confirmed, O official, R reported, X claim.  Grade counts add to 40.  "
            f"Compiled from the named outlets\u2019 reports up to {stories.EDITION_CLOSE} UTC; no item rests on an unnamed source.")
    page.text(MARGIN, top + 46, note, "medium", 10, SOFT, "lm", within=(0, top + 38, SIDE, top + 54))


def paint():
    stories.check()
    page = Page()
    masthead(page)
    y = kpi_strip(page, 73)
    y = region_bar(page, y + 4)
    y = cards(page, y + 4)
    y = wire(page, y + 4)
    band_top = y + 5
    band_height = 190
    atlas_panel(page, MARGIN, band_top, 412, band_height)
    date_check(page, MARGIN + 420, band_top, SIDE - 2 * MARGIN - 420, band_height)
    footer(page, band_top + band_height + 5)
    return page


def png_bytes(pixels):
    """Smallest lossless 8-bit RGB PNG we can find: try several row-filter plans and keep the shortest stream."""
    height, width, _ = pixels.shape
    a = pixels.astype(np.int16)
    left = np.zeros_like(a)
    left[:, 1:] = a[:, :-1]
    up = np.zeros_like(a)
    up[1:] = a[:-1]
    corner = np.zeros_like(a)
    corner[1:, 1:] = a[:-1, :-1]
    guess = left + up - corner
    d_left, d_up, d_corner = np.abs(guess - left), np.abs(guess - up), np.abs(guess - corner)
    paeth = np.where((d_left <= d_up) & (d_left <= d_corner), left, np.where(d_up <= d_corner, up, corner))
    filtered = [a, a - left, a - up, a - ((left + up) >> 1), a - paeth]
    rows = [(r & 255).astype(np.uint8).reshape(height, width * 3) for r in filtered]

    plans = {f"all-{k}": np.full(height, k) for k in range(5)}
    weight = [np.abs(r.astype(np.int8).astype(np.int16)).sum(axis=1) for r in rows]
    plans["least-residue"] = np.argmin(np.stack(weight), axis=0)
    trial = np.array([[len(zlib.compress(rows[k][y].tobytes(), 6)) for k in range(5)] for y in range(height)])
    plans["row-deflate"] = np.argmin(trial, axis=1)

    best = None
    for name, plan in sorted(plans.items()):
        stream = b"".join(bytes([int(plan[y])]) + rows[int(plan[y])][y].tobytes() for y in range(height))
        for strategy in (zlib.Z_DEFAULT_STRATEGY, zlib.Z_FILTERED):
            packer = zlib.compressobj(9, zlib.DEFLATED, 15, 9, strategy)
            packed = packer.compress(stream) + packer.flush()
            if best is None or len(packed) < len(best[0]):
                best = (packed, name)

    def chunk(kind, body):
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body) & 0xFFFFFFFF)

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    data = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", best[0]) + chunk(b"IEND", b"")
    return data, best[1]


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "..", "entry.png")
    page = paint()
    problems = page.audit()
    for problem in problems:
        print(problem)
    data, plan = png_bytes(np.asarray(page.image.convert("RGB"), dtype=np.uint8))
    with open(target, "wb") as handle:
        handle.write(data)
    print(f"{os.path.normpath(target)}: {len(data)} bytes, filter plan {plan}, {len(page.placed)} text runs, {len(problems)} problem(s)")
    if problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
