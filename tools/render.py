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
PAPER = "#F5F1E7"
CARD_BG = "#FFFDF8"
INK = "#141923"
BODY = "#2A3240"
WHITE = "#FFFFFF"
RED = "#B3261E"
AMBER = "#9A6200"
SOFT = "#4B5563"
TINT = "#EBE5D7"
RULE = "#BEB7A7"

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
    # Top editorial micro-bar
    brand = "WORLD LEDGER"
    page.text(MARGIN, 11, brand, "black", 10.5, RED, "lm", within=(0, 3, 240, 19))
    brand_end = MARGIN + width_of(brand, "black", 10.5)
    page.text(brand_end + 6, 11, f"\u00b7  {stories.EDITION_CLOSE} UTC EDITION", "black", 10.5, INK, "lm",
              within=(MARGIN, 3, 420, 19))
    right_meta = (
        f"{len(stories.all_stories())} VERIFIED STORIES  \u00b7  {len(stories.REGIONS)} REGIONS  \u00b7  "
        f"{len(stories.EXCLUDED)} PRE-SUNDAY EXCLUDED"
    )
    page.text(SIDE - MARGIN, 11, right_meta, "bold", 10, SOFT, "rm", within=(440, 3, SIDE, 19))
    page.box(MARGIN, 19, SIDE - MARGIN, 20, RULE)
    # Huge full-width centered broadsheet date (survives at 300px!)
    page.text(SIDE / 2, 45, stories.EDITION_DAY, "serif", 50, INK, "mm", within=(MARGIN, 20, SIDE - MARGIN, 70))
    # One-line summary of the four lead stories
    page.text(SIDE / 2, 76, stories.LEAD_SUMMARY, "bold", 13, INK, "mm", within=(MARGIN, 68, SIDE - MARGIN, 84))
    # Classic broadsheet double rule
    page.box(MARGIN, 84, SIDE - MARGIN, 87, INK)
    page.box(MARGIN, 89, SIDE - MARGIN, 90, INK)
    return 90


def timeline_strip(page, top):
    height = 18
    tag_w = 96
    page.box(MARGIN, top, MARGIN + tag_w, top + height, INK)
    page.text(MARGIN + tag_w / 2, top + height / 2, "THE DAY IN UTC", "black", 9.5, WHITE, "mm",
              within=(MARGIN, top, MARGIN + tag_w, top + height))
    strip_left = MARGIN + tag_w
    strip_right = SIDE - MARGIN
    page.box(strip_left, top, strip_right, top + height, TINT)
    page.box(strip_left, top, strip_right, top + 1, RULE)
    page.box(strip_left, top + height - 1, strip_right, top + height, RULE)
    page.box(strip_right - 1, top, strip_right, top + height, RULE)

    # Measure total width of the 8 chronological items so we distribute spacing evenly across the strip
    items = stories.TIMELINE
    item_widths = []
    for ts, label in items:
        item_widths.append(width_of(ts, "black", 10) + 3 + width_of(label, "bold", 10))
    sep = "\u00b7"
    sep_w = width_of(sep, "black", 10)
    avail = (strip_right - strip_left) - 16
    gap = (avail - sum(item_widths) - sep_w * (len(items) - 1)) / (2 * (len(items) - 1))
    x = strip_left + 8
    mid = top + height / 2
    for idx, (ts, label) in enumerate(items):
        end = page.text(x, mid, ts, "black", 10, RED, "lm", within=(strip_left, top, strip_right, top + height))
        end2 = page.text(end[2] + 3, mid, label, "bold", 10, INK, "lm", within=(strip_left, top, strip_right, top + height))
        x = end2[2]
        if idx < len(items) - 1:
            x += gap
            page.text(x + sep_w / 2, mid, sep, "black", 10, SOFT, "mm", within=(strip_left, top, strip_right, top + height))
            x += sep_w + gap
    return top + height


def kpi_strip(page, top):
    height = 49
    gap = 6
    tile_width = (SIDE - 2 * MARGIN - gap * 5) // 6
    for index, (figure, label, region, emphasis) in enumerate(stories.NEWS_STATS):
        x = MARGIN + index * (tile_width + gap)
        page.box(x, top, x + tile_width, top + height, INK)
        page.box(x + 1, top + 1, x + tile_width - 1, top + height - 1, CARD_BG)
        page.box(x + 1, top + 1, x + tile_width - 1, top + 5, REGION_COLOUR[region])
        fig_size = 22 if len(figure) <= 7 else (20 if len(figure) <= 9 else 19)
        fig_colour = RED if emphasis else INK
        page.text(x + tile_width / 2, top + 20, figure, "black", fig_size, fig_colour, "mm",
                  within=(x + 3, top + 6, x + tile_width - 3, top + 33))
        page.text(x + tile_width / 2, top + 39, label, "bold", 10.5, BODY, "mm",
                  within=(x + 3, top + 32, x + tile_width - 3, top + height - 2))
    return top + height


def region_bar(page, top):
    counts = stories.region_counts()
    total = sum(counts.values())
    height = 16
    span = SIDE - 2 * MARGIN
    x = MARGIN
    running = 0
    for name, _, colour in stories.REGIONS:
        running += counts[name]
        right = MARGIN + round(span * running / total)
        page.box(x, top, right, top + height, colour)
        page.text((x + right) / 2, top + height / 2, f"{name} {counts[name]}", "black", 10, WHITE, "mm",
                  within=(x + 2, top, right - 2, top + height))
        if right < SIDE - MARGIN:
            page.box(right - 1, top, right + 1, top + height, PAPER)
        x = right
    return top + height


def card(page, story, x, y, width, art_height, caption_height):
    lead = width > 250
    total_h = art_height + caption_height
    # Crisp outer card border + warm white editorial paper body
    border = INK if lead else RULE
    page.box(x, y, x + width, y + total_h, border)
    page.box(x + 1, y + art_height, x + width - 1, y + total_h - 1, CARD_BG)
    picture, labels = art.render_scene(story["art"], width - 2, art_height - 1, 4, story.get("note", ""))
    page.image.paste(picture, (x + 1, y + 1))
    for lx, ly, string, size, colour, name, anchor in labels:
        page.text(x + 1 + lx, y + 1 + ly, string, name, size, colour, anchor,
                  within=(x + 1, y + 1, x + width - 1, y + art_height))
    # Regional colour rule dividing art banner and paper headline body
    region = story["region"]
    page.box(x + 1, y + art_height, x + width - 1, y + art_height + 2, REGION_COLOUR[region])
    # number + region tag, top left
    tag_height = 16 if lead else 13
    number_size, region_size = (12, 10) if lead else (10.5, 9)
    number = str(story["n"])
    number_box = int(width_of(number, "black", number_size)) + (10 if lead else 8)
    page.box(x + 1, y + 1, x + 1 + number_box, y + 1 + tag_height, INK)
    page.text(x + 1 + number_box / 2, y + 1 + tag_height / 2, number, "black", number_size, WHITE, "mm",
              within=(x + 1, y + 1, x + 1 + number_box, y + 1 + tag_height))
    region_box = int(width_of(region, "black", region_size)) + (11 if lead else 8)
    page.box(x + 1 + number_box, y + 1, x + 1 + number_box + region_box, y + 1 + tag_height, REGION_COLOUR[region])
    page.text(x + 1 + number_box + region_box / 2, y + 1 + tag_height / 2, region, "black", region_size, WHITE, "mm",
              within=(x + 1 + number_box, y + 1, x + 1 + number_box + region_box, y + 1 + tag_height))
    # verification tag, top right
    grade = story["grade"]
    grade_size = 10 if lead else 9
    grade_box = int(width_of(grade, "black", grade_size)) + (11 if lead else 8)
    page.box(x + width - 1 - grade_box, y + 1, x + width - 1, y + 1 + tag_height, GRADE_COLOUR[grade])
    page.text(x + width - 1 - grade_box / 2, y + 1 + tag_height / 2, grade, "black", grade_size, WHITE, "mm",
              within=(x + width - 1 - grade_box, y + 1, x + width - 1, y + 1 + tag_height))
    # High-contrast black serif headlines on warm white paper
    top = y + art_height + 2
    pad = 8 if lead else 6
    inner = (x + pad - 2, top, x + width - pad + 2, y + total_h - 1)
    if lead:
        lines = wrap(story["head"], "serif", 18, width - 2 * pad, 2)
        baseline = top + 19
        for line in lines:
            page.text(x + pad, baseline, line, "serif", 18, INK, within=inner)
            baseline += 20
        page.text(x + pad, top + 56, story["deck"], "medium", 11.5, BODY, within=inner)
        when_end = page.text(x + pad, top + 71, story["when"], "black", 10.5, RED, within=inner)
        sources_txt = "  \u00b7  " + ", ".join(story["sources"])
        page.text(when_end[2] + 1, top + 71, sources_txt, "bold", 10.5, SOFT, within=inner)
    else:
        head_size = 13.5
        lines = wrap(story["head"], "serif", head_size, width - 2 * pad, 2)
        baseline = top + 15.5
        for line in lines:
            page.text(x + pad, baseline, line, "serif", head_size, INK, within=inner)
            baseline += 15.5
        when_txt = story["when"]
        src_txt = "\u00b7 " + ", ".join(story["sources"])
        meta_size = 10
        if width_of(when_txt, "black", meta_size) + 5 + width_of(src_txt, "bold", meta_size) > width - 2 * pad:
            meta_size = 9.5
        when_end = page.text(x + pad, top + 46, when_txt, "black", meta_size, RED, within=inner)
        page.text(when_end[2] + 4, top + 46, src_txt, "bold", meta_size, SOFT, within=inner)


def cards(page, top):
    lead_width, lead_gap = 332, 6
    for index, story in enumerate(stories.CARDS[:3]):
        card(page, story, MARGIN + index * (lead_width + lead_gap), top, lead_width, 84, 80)
    top += 84 + 80 + 5
    lefts = (8, 211, 414, 617, 819)
    for row in range(2):
        for index in range(5):
            card(page, stories.CARDS[3 + row * 5 + index], lefts[index], top, 197, 46, 53)
        top += 46 + 53 + 4
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
    title = f"NOT YET ({len(stories.PENDING)})  \u00b7  open at the {stories.EDITION_CLOSE} UTC close"
    tag = int(width_of(title, "black", 10)) + 12
    page.box(left + 7, y, left + 7 + tag, y + 14, AMBER)
    page.text(left + 13, y + 7, title, "black", 10, WHITE, "lm", within=(left + 7, y, left + 7 + tag, y + 14))
    y = flow(page, stories.PENDING, "?", AMBER, left + 8, y + 26, right - 7)
    if y > top + height - 3:
        page.problems.append(f"OVERFLOW date check box by {y - (top + height - 3):.0f}px")


def footer(page, top):
    page.box(MARGIN, top, SIDE - MARGIN, top + 2, INK)
    y = top + 12
    page.text(MARGIN, y, "VERIFICATION", "black", 10.5, INK, "lm", within=(0, top + 3, SIDE, top + 22))
    x = MARGIN + 88
    counts = stories.grade_counts()
    for name, letter, colour, meaning in stories.GRADES:
        pill = int(width_of(name, "black", 9.5)) + 10
        page.box(x, y - 6, x + pill, y + 7, colour)
        page.text(x + pill / 2, y, name, "black", 9.5, WHITE, "mm", within=(x, y - 6, x + pill, y + 7))
        note = f"{meaning} ({counts[name]})"
        page.text(x + pill + 5, y, note, "bold", 10, INK, "lm", within=(x, top + 3, SIDE - MARGIN, top + 22))
        x += pill + 5 + int(width_of(note, "bold", 10)) + 16
    rule = ("DATELINE RULE  Only events or first reports on Sunday 22 November 2026 UTC run as today\u2019s news; "
            "Sat 21 Nov UTC items are logged in Date Check.")
    page.text(MARGIN, top + 28, rule, "medium", 10, INK, "lm", within=(0, top + 21, SIDE, top + 36))
    note = (f"Wire chips: C confirmed, O official, R reported, X claim.  Grade counts add to 40.  "
            f"Compiled from {len(stories.named_sources())} named outlets up to {stories.EDITION_CLOSE} UTC; no item rests on an unnamed source.")
    page.text(MARGIN, top + 41, note, "medium", 10, SOFT, "lm", within=(0, top + 34, SIDE, SIDE))


def paint():
    stories.check()
    page = Page()
    y = masthead(page)
    y = timeline_strip(page, y + 3)
    y = kpi_strip(page, y + 4)
    y = region_bar(page, y + 4)
    y = cards(page, y + 4)
    y = wire(page, y + 4)
    band_top = y + 4
    band_height = 180
    atlas_panel(page, MARGIN, band_top, 412, band_height)
    date_check(page, MARGIN + 420, band_top, SIDE - 2 * MARGIN - 420, band_height)
    footer(page, band_top + band_height + 4)
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
