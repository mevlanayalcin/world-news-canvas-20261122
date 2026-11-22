"""Draw the World Ledger visual front-page poster for Sunday 22 November 2026 (1024 x 1024, 8-bit RGB PNG).

    python3 tools/render.py            # writes ../entry.png
    python3 tools/render.py out.png    # writes somewhere else

One clear, breathable editorial composition designed to excel at both full resolution and 300px thumbnails:
  - Giant broadsheet date masthead (56px serif)
  - 2 centerpiece illustrated hero stories (30px serif headlines)
  - 4 x 2 illustrated global grid (19.5px serif headlines)
  - Clean large-type World Briefs + explicit Sat-21-Nov-UTC Exclusion strip (14 verified stories, 2 per region)
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
TINT = "#EFE9DB"
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
    page.box(0, 0, SIDE, 32, NAVY)
    title_end = page.text(MARGIN + 2, 16, "WORLD NEWS", "black", 16.5, WHITE, "lm", within=(0, 0, 260, 32))
    page.text(title_end[2] + 10, 16, f"\u00b7  {stories.EDITION_CLOSE} EDITION", "bold", 12.5, GOLD, "lm",
              within=(100, 0, 500, 32))
    pill_txt = f"7 REGIONS  \u00b7  {len(stories.all_stories())} VERIFIED STORIES  \u00b7  22 NOV UTC"
    pill_w = int(width_of(pill_txt, "black", 11.5)) + 20
    px0 = SIDE - MARGIN - pill_w
    page.box(px0, 5, SIDE - MARGIN, 27, RED)
    page.text(px0 + pill_w / 2, 16, pill_txt, "black", 11.5, WHITE, "mm", within=(px0, 5, SIDE - MARGIN, 27))
    # Giant full-width centered broadsheet date (unmistakable even at 250px wide)
    page.text(SIDE / 2, 67, stories.EDITION_DAY, "serif", 56, INK, "mm", within=(MARGIN, 33, SIDE - MARGIN, 102))
    # Classic broadsheet double rule
    page.box(MARGIN, 102, SIDE - MARGIN, 105, NAVY)
    page.box(MARGIN, 107, SIDE - MARGIN, 108, RED)
    return 108


def hero_card(page, story, x, y, width, height):
    art_h = 186
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
    lines = wrap(story["head"], "serif", 30, width - 2 * pad, 2)
    baseline = top + 32
    for line in lines:
        page.text(x + pad, baseline, line, "serif", 30, INK, within=inner)
        baseline += 34
    page.text(x + pad, top + 93, story["deck"], "medium", 15.5, BODY, within=inner)
    when_end = page.text(x + pad, top + 117, story["when"], "black", 13, RED, within=inner)
    src_txt = "  \u00b7  " + ", ".join(story["sources"])
    page.text(when_end[2] + 2, top + 117, src_txt, "bold", 13, SOFT, within=inner)


def grid_card(page, story, x, y, width, height):
    art_h = 112
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
    lines = wrap(story["head"], "serif", 19.5, width - 2 * pad, 2)
    baseline = top + 23
    for line in lines:
        page.text(x + pad, baseline, line, "serif", 19.5, INK, within=inner)
        baseline += 22.5
    page.text(x + pad, top + 70, story["deck"], "medium", 12.5, BODY, within=inner)
    when_txt = story["when"]
    src_txt = "\u00b7 " + ", ".join(story["sources"])
    meta_size = 11.5
    if width_of(when_txt, "black", meta_size) + 5 + width_of(src_txt, "bold", meta_size) > width - 2 * pad:
        meta_size = 11
    when_end = page.text(x + pad, top + 95, when_txt, "black", meta_size, RED, within=inner)
    page.text(when_end[2] + 4, top + 95, src_txt, "bold", meta_size, SOFT, within=inner)


def briefs_and_datecheck(page, top):
    # Clean, high-legibility 2x2 World Briefs panel (Finance, Diplomacy, African Politics, Health) + Sat UTC Date Check
    height = 90
    left, right = MARGIN, SIDE - MARGIN
    page.box(left, top, right, top + height, NAVY)
    page.box(left + 1, top + 1, right - 1, top + height - 1, CARD_BG)
    # 2 rows of 2 spacious briefs (each row 30px tall, >= 13px crisp type!)
    row_h = 30
    page.box(left + 1, top + row_h, right - 1, top + row_h + 1, RULE)
    page.box(SIDE // 2, top + 1, SIDE // 2 + 1, top + 2 * row_h, RULE)
    col_starts = (left + 10, SIDE // 2 + 10)
    col_ends = (SIDE // 2 - 8, right - 8)
    for idx, b in enumerate(stories.BRIEFS):
        row, col = divmod(idx, 2)
        cy = top + row * row_h + row_h / 2
        x0, x1 = col_starts[col], col_ends[col]
        colour = REGION_COLOUR[b["region"]]
        tag_w = int(width_of(b["tag"], "black", 10)) + 12
        page.box(x0, cy - 8, x0 + tag_w, cy + 8, colour)
        page.text(x0 + tag_w / 2, cy, b["tag"], "black", 10, WHITE, "mm", within=(x0, cy - 9, x0 + tag_w, cy + 9))
        tx = x0 + tag_w + 8
        src = " \u00b7 " + ", ".join(b["sources"])
        t_size = 12.5
        if width_of(b["text"], "bold", t_size) + width_of(src, "medium", 11.5) > (x1 - tx):
            t_size = 12
        end = page.text(tx, cy, b["text"], "bold", t_size, INK, "lm", within=(tx - 1, cy - 12, x1, cy + 12))
        page.text(end[2] + 2, cy, src, "medium", 11.5, SOFT, "lm", within=(tx - 1, cy - 12, x1 + 2, cy + 12))
    # Bottom explicit Sunday-UTC Date Check bar inside the panel (y = top + 61 .. top + 89)
    bar_y = top + 2 * row_h + 1
    bar_h = height - 2 * row_h - 2
    page.box(left + 1, bar_y, right - 1, top + height - 1, TINT)
    page.box(left + 1, bar_y, right - 1, bar_y + 1, RULE)
    cy = bar_y + bar_h / 2
    excl_tag = "EXCLUDED (SAT 21 NOV UTC)"
    et_w = int(width_of(excl_tag, "black", 10.5)) + 14
    page.box(left + 10, cy - 9, left + 10 + et_w, cy + 9, RED)
    page.text(left + 10 + et_w / 2, cy, excl_tag, "black", 10.5, WHITE, "mm",
              within=(left + 10, cy - 9, left + 10 + et_w, cy + 9))
    page.text(left + 10 + et_w + 10, cy, stories.EXCLUDED_LINE, "bold", 12, BODY, "lm",
              within=(left + 10 + et_w + 6, bar_y, right - 8, top + height - 1))


def paint():
    stories.check()
    page = Page()
    y = masthead(page)
    # Top hero row: 2 giant panels (492 x 322, 16px gutter)
    hero_y = y + 8
    hero_w, hero_h, hero_gap = 492, 322, 16
    for i, story in enumerate(stories.HEROES):
        hero_card(page, story, MARGIN + i * (hero_w + hero_gap), hero_y, hero_w, hero_h)
    # 4 x 2 global grid (241 x 230, 12px horizontal gutter, 10px vertical gutter)
    grid_y = hero_y + hero_h + 10
    card_w, card_h, col_gap, row_gap = 241, 230, 12, 10
    for idx, story in enumerate(stories.CARDS):
        row, col = divmod(idx, 4)
        cx = MARGIN + col * (card_w + col_gap)
        cy = grid_y + row * (card_h + row_gap)
        grid_card(page, story, cx, cy, card_w, card_h)
    # Clean World Briefs (Finance, Diplomacy, Africa, Health) + Sat-UTC Date Check bar
    briefs_and_datecheck(page, grid_y + 2 * card_h + row_gap + 10)
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
