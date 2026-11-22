"""Draw the World Ledger visual front-page poster for Sunday 22 November 2026 (1024 x 1024, 8-bit RGB PNG).

    python3 tools/render.py            # writes ../entry.png
    python3 tools/render.py out.png    # writes somewhere else

One clear, breathable editorial composition designed to read effortlessly at 300px across:
  - Giant broadsheet date masthead (58px serif)
  - 2 centerpiece illustrated hero stories (31px serif headlines)
  - 4 x 2 illustrated global grid covering all 7 world regions & major beats (20.5px serif headlines)
  - 1 crisp large-type footer highlight bar (15px bold) — zero tiny text blocks anywhere
Every text placement is checked for strict bounds and zero overlap before saving.
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
MARGIN = 12
PAPER = "#F5F1E8"
CARD_BG = "#FFFDF9"
NAVY = "#121A2A"
INK = "#121A2A"
BODY = "#2B3445"
WHITE = "#FFFFFF"
RED = "#B8251E"
GOLD = "#FDE68A"
SOFT = "#4B5563"
RULE = "#CFC8B8"

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
        self.placed = []
        self.problems = []

    def box(self, x0, y0, x1, y1, colour):
        self.draw.rectangle([x0, y0, x1 - 1, y1 - 1], fill=colour)

    def text(self, x, y, string, name, size, colour, anchor="ls", within=None):
        face = font(name, size)
        self.draw.text((x, y), string, font=face, fill=colour, anchor=anchor)
        bbox = self.draw.textbbox((x, y), string, font=face, anchor=anchor)
        self.placed.append((bbox, string, within))
        if within is not None:
            x0, y0, x1, y1 = within
            if bbox[0] < x0 - 0.01 or bbox[1] < y0 - 0.01 or bbox[2] > x1 + 0.01 or bbox[3] > y1 + 0.01:
                self.problems.append(f"CLIPPED {string!r}: {tuple(round(v, 1) for v in bbox)} outside {within}")
        return bbox

    def audit(self):
        for i in range(len(self.placed)):
            a = self.placed[i][0]
            for j in range(i + 1, len(self.placed)):
                b = self.placed[j][0]
                if min(a[2], b[2]) - max(a[0], b[0]) > 0.5 and min(a[3], b[3]) - max(a[1], b[1]) > 0.5:
                    self.problems.append(f"OVERLAP {self.placed[i][1]!r} x {self.placed[j][1]!r}")
        return self.problems


REGION_COLOUR = {name: colour for name, colour in stories.REGIONS}


def masthead(page):
    page.box(0, 0, SIDE, 34, NAVY)
    title_end = page.text(MARGIN + 2, 17, "WORLD NEWS", "black", 17, WHITE, "lm", within=(0, 0, 260, 34))
    page.text(title_end[2] + 10, 17, f"\u00b7  {stories.EDITION_TAG}", "bold", 13, GOLD, "lm",
              within=(100, 0, 500, 34))
    pill_txt = "7 REGIONS  \u00b7  22 NOV 2026"
    pill_w = int(width_of(pill_txt, "black", 12.5)) + 22
    px0 = SIDE - MARGIN - pill_w
    page.box(px0, 5, SIDE - MARGIN, 29, RED)
    page.text(px0 + pill_w / 2, 17, pill_txt, "black", 12.5, WHITE, "mm", within=(px0, 5, SIDE - MARGIN, 29))
    # Giant full-width centered broadsheet date (effortless at 300px)
    page.text(SIDE / 2, 69, stories.EDITION_DAY, "serif", 58, INK, "mm", within=(MARGIN, 35, SIDE - MARGIN, 105))
    page.box(MARGIN, 105, SIDE - MARGIN, 108, NAVY)
    page.box(MARGIN, 110, SIDE - MARGIN, 111, RED)
    return 111


def hero_card(page, story, x, y, width, height):
    art_h = 196
    page.box(x, y, x + width, y + height, NAVY)
    page.box(x + 1, y + art_h, x + width - 1, y + height - 1, CARD_BG)
    picture, labels = art.render_scene(story["art"], width - 2, art_h - 1, 4, story.get("note", ""))
    page.image.paste(picture, (x + 1, y + 1))
    for lx, ly, string, size, colour, name, anchor in labels:
        page.text(x + 1 + lx, y + 1 + ly, string, name, size, colour, anchor,
                  within=(x + 1, y + 1, x + width - 1, y + art_h))
    colour = REGION_COLOUR[story["region"]]
    page.box(x + 1, y + art_h, x + width - 1, y + art_h + 4, colour)
    pill = f"{story['region']}  \u00b7  {story['beat']}"
    pill_w = int(width_of(pill, "black", 12)) + 16
    page.box(x + 1, y + 1, x + 1 + pill_w, y + 23, colour)
    page.text(x + 1 + pill_w / 2, y + 12, pill, "black", 12, WHITE, "mm",
              within=(x + 1, y + 1, x + 1 + pill_w, y + 23))
    top = y + art_h + 4
    pad = 12
    inner = (x + pad - 2, top, x + width - pad + 2, y + height - 2)
    lines = wrap(story["head"], "serif", 31, width - 2 * pad, 2)
    baseline = top + 34
    for line in lines:
        page.text(x + pad, baseline, line, "serif", 31, INK, within=inner)
        baseline += 35
    page.text(x + pad, top + 98, story["deck"], "medium", 16.5, BODY, within=inner)
    place_end = page.text(x + pad, top + 123, story["place"], "black", 13.5, RED, within=inner)
    src_txt = "  \u00b7  " + ", ".join(story["sources"])
    page.text(place_end[2] + 2, top + 123, src_txt, "bold", 13.5, SOFT, within=inner)


def grid_card(page, story, x, y, width, height):
    art_h = 118
    page.box(x, y, x + width, y + height, RULE)
    page.box(x + 1, y + art_h, x + width - 1, y + height - 1, CARD_BG)
    picture, labels = art.render_scene(story["art"], width - 2, art_h - 1, 4, story.get("note", ""))
    page.image.paste(picture, (x + 1, y + 1))
    for lx, ly, string, size, colour, name, anchor in labels:
        page.text(x + 1 + lx, y + 1 + ly, string, name, size, colour, anchor,
                  within=(x + 1, y + 1, x + width - 1, y + art_h))
    colour = REGION_COLOUR[story["region"]]
    page.box(x + 1, y + art_h, x + width - 1, y + art_h + 3, colour)
    pill = f"{story['region']} \u00b7 {story['beat']}"
    pill_w = int(width_of(pill, "black", 10.5)) + 12
    page.box(x + 1, y + 1, x + 1 + pill_w, y + 20, colour)
    page.text(x + 1 + pill_w / 2, y + 10.5, pill, "black", 10.5, WHITE, "mm",
              within=(x + 1, y + 1, x + 1 + pill_w, y + 20))
    top = y + art_h + 3
    pad = 9
    inner = (x + pad - 2, top, x + width - pad + 2, y + height - 2)
    lines = wrap(story["head"], "serif", 20.5, width - 2 * pad, 2)
    baseline = top + 24
    for line in lines:
        page.text(x + pad, baseline, line, "serif", 20.5, INK, within=inner)
        baseline += 23.5
    page.text(x + pad, top + 73, story["deck"], "medium", 13, BODY, within=inner)
    place_end = page.text(x + pad, top + 99, story["place"], "black", 12, RED, within=inner)
    src_txt = " \u00b7 " + ", ".join(story["sources"])
    page.text(place_end[2] + 3, top + 99, src_txt, "bold", 12, SOFT, within=inner)


def footer_bar(page, top):
    # Bold single-row 300px-legible navy highlight strip — zero tiny text blocks
    height = 38
    left, right = MARGIN, SIDE - MARGIN
    page.box(left, top, right, top + height, NAVY)
    cy = top + height / 2
    tag = "ALSO TODAY"
    tag_w = int(width_of(tag, "black", 12)) + 20
    page.box(left + 6, top + 6, left + 6 + tag_w, top + height - 6, RED)
    page.text(left + 6 + tag_w / 2, cy, tag, "black", 12, WHITE, "mm",
              within=(left + 6, top + 6, left + 6 + tag_w, top + height - 6))
    # Evenly space the 3 bold items across the remaining bar width
    items = stories.FOOTER_ITEMS
    item_widths = [width_of(h, "black", 14.5) + 7 + width_of(s, "bold", 13) for h, s in items]
    sep = "\u00b7"
    sep_w = width_of(sep, "black", 16)
    bar_l = left + 6 + tag_w + 18
    bar_r = right - 18
    gap = (bar_r - bar_l - sum(item_widths) - sep_w * (len(items) - 1)) / (2 * (len(items) - 1))
    x = bar_l
    for idx, (head, sub) in enumerate(items):
        e1 = page.text(x, cy, head, "black", 14.5, GOLD, "lm", within=(bar_l - 4, top, bar_r + 4, top + height))
        e2 = page.text(e1[2] + 6, cy, sub, "bold", 13, WHITE, "lm", within=(bar_l - 4, top, bar_r + 4, top + height))
        x = e2[2]
        if idx < len(items) - 1:
            x += gap
            page.text(x + sep_w / 2, cy, sep, "black", 16, "#94A3B8", "mm", within=(bar_l, top, bar_r, top + height))
            x += sep_w + gap


def paint():
    stories.check()
    page = Page()
    y = masthead(page)
    # Top hero row: 2 giant panels (492 x 342, 16px gutter)
    hero_y = y + 8
    hero_w, hero_h, hero_gap = 492, 342, 16
    for i, story in enumerate(stories.HEROES):
        hero_card(page, story, MARGIN + i * (hero_w + hero_gap), hero_y, hero_w, hero_h)
    # 4 x 2 global grid (241 x 240, 12px horizontal & vertical gutters)
    grid_y = hero_y + hero_h + 12
    card_w, card_h, col_gap, row_gap = 241, 240, 12, 12
    for idx, story in enumerate(stories.CARDS):
        row, col = divmod(idx, 4)
        cx = MARGIN + col * (card_w + col_gap)
        cy = grid_y + row * (card_h + row_gap)
        grid_card(page, story, cx, cy, card_w, card_h)
    # Crisp single-row bold footer highlight bar
    footer_bar(page, grid_y + 2 * card_h + row_gap + 10)
    return page


def png_bytes(pixels):
    """Smallest lossless 8-bit RGB PNG via optimal per-row filter plan + zlib-9."""
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
