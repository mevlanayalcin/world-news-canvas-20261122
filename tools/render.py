"""Draw the v8 Illustrated Visual World Atlas front page for Sunday 22 November 2026 (1024 x 1024, 8-bit RGB PNG).

    python3 tools/render.py            # writes ../entry.png
    python3 tools/render.py out.png    # writes somewhere else

Zero-text-wall visual composition engineered for effortless 300px legibility AND full global breadth:
  - Giant broadsheet serif date masthead (48px C059-Bold) + 7-region 18-story ribbon
  - Natural Earth World Hotspots Map (602 x 314) with 14 geographic story pins & giant 14.5px callouts
  - 2 Tall Illustrated Hero Lead Panels (COP31 Antalya + Iran rolling blackouts, 21px serif heads)
  - 3 x 4 Gallery of 12 Bespoke Illustrated Visual Story Cards (242 x 174 each: custom vector art +
    giant 17.5px bold serif headline — ZERO tiny sub-captions, ZERO source credits, ZERO bullet walls)
  - Deep-navy Global Wire Strip (4 major beats at 15.5px bold white on jewel-tone badges)
Every text placement is strictly audited for bounds and zero overlap before saving.
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
NAVY = "#0F172A"
INK = "#0B1220"
WHITE = "#FFFFFF"
RED = "#B8251E"
GOLD = "#FDE68A"
RULE = "#C4BBA9"

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


def wrap_plain(text, name, size, width, max_lines):
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if width_of(trial, name, size) <= width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
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

    def outline_box(self, x0, y0, x1, y1, fill, outline):
        self.draw.rectangle([x0, y0, x1 - 1, y1 - 1], fill=fill, outline=outline, width=1)

    def text(self, x, y, string, name, size, colour, anchor="ls", within=None):
        face = font(name, size)
        self.draw.text((x, y), string, font=face, fill=colour, anchor=anchor)
        bbox = self.draw.textbbox((x, y), string, font=face, anchor=anchor)
        self.placed.append((bbox, string, within))
        if within is not None:
            x0, y0, x1, y1 = within
            if bbox[0] < x0 - 0.5 or bbox[1] < y0 - 0.5 or bbox[2] > x1 + 0.5 or bbox[3] > y1 + 0.5:
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


def masthead(page):
    page.box(0, 0, SIDE, 24, NAVY)
    t_end = page.text(MARGIN + 2, 12, "WORLD NEWS ATLAS", "black", 14.5, WHITE, "lm", within=(0, 0, 260, 24))
    page.text(
        t_end[2] + 10,
        12,
        f"\u00b7  {stories.EDITION_TAG}",
        "bold",
        12.5,
        GOLD,
        "lm",
        within=(140, 0, 520, 24),
    )
    pill_txt = f"7 REGIONS  \u00b7  {stories.total_stories()} STORIES"
    pill_w = int(width_of(pill_txt, "black", 12.5)) + 24
    px0 = SIDE - MARGIN - pill_w
    page.box(px0, 2, SIDE - MARGIN, 22, RED)
    page.text(px0 + pill_w / 2, 12, pill_txt, "black", 12.5, WHITE, "mm", within=(px0, 2, SIDE - MARGIN, 22))

    page.text(SIDE / 2, 50, stories.EDITION_DAY, "serif", 48, INK, "mm", within=(MARGIN, 25, SIDE - MARGIN, 75))
    page.box(MARGIN, 74, SIDE - MARGIN, 77, NAVY)
    page.box(MARGIN, 78, SIDE - MARGIN, 79, RED)
    return 79


def atlas_panel(page, x, y, width, height):
    """Left centerpiece: Natural Earth world map with 14 geographic pins, giant 14.5px callouts & legend."""
    page.box(x, y, x + width, y + height, NAVY)
    header_h = 24
    legend_h = 28
    map_h = height - header_h - legend_h - 2
    map_w = width - 2

    page.text(x + 10, y + header_h / 2, "GLOBAL HOTSPOTS MAP", "black", 13, WHITE, "lm", within=(x, y, x + 260, y + header_h))
    page.text(
        x + width - 10,
        y + header_h / 2,
        "PINS MATCH STORY CARDS BELOW",
        "bold",
        11.5,
        GOLD,
        "rm",
        within=(x + 250, y, x + width, y + header_h),
    )

    atlas = art.Atlas(map_w, map_h, scale=4)
    for label, lon, lat, bcx, bcy, colour in stories.MAP_CALLOUTS:
        atlas.leader(lon, lat, bcx, bcy, colour="#0F172A")
    for _, _, col, lon, lat in stories.GLOBAL_STRIP:
        if lon is not None and lat is not None:
            atlas.dot(lon, lat, col, radius=4.8)
    for card in stories.CARDS:
        atlas.dot(card["lon"], card["lat"], card["colour"], radius=5.4)
    hero_spots = []
    for h in stories.HEROES:
        hx, hy = atlas.hero_pin(h["lon"], h["lat"], h["colour"], radius=9.2)
        hero_spots.append((hx, hy, str(h["n"])))

    map_img = atlas.finish()
    map_x0 = x + 1
    map_y0 = y + header_h
    page.image.paste(map_img, (map_x0, map_y0))

    for hx, hy, num_str in hero_spots:
        page.text(
            map_x0 + hx,
            map_y0 + hy,
            num_str,
            "black",
            12,
            WHITE,
            "mm",
            within=(map_x0, map_y0, map_x0 + map_w, map_y0 + map_h),
        )

    # Giant 14px bold open-ocean callouts — crystal clear at 300px!
    pill_h = 24
    for label, lon, lat, bcx, bcy, colour in stories.MAP_CALLOUTS:
        tw = int(width_of(label, "black", 14))
        pw = tw + 18
        px0 = int(round(map_x0 + bcx - pw / 2))
        py0 = int(round(map_y0 + bcy - pill_h / 2))
        px1 = px0 + pw
        py1 = py0 + pill_h
        px0 = max(map_x0 + 3, min(px0, map_x0 + map_w - pw - 3))
        px1 = px0 + pw
        py0 = max(map_y0 + 3, min(py0, map_y0 + map_h - pill_h - 3))
        py1 = py0 + pill_h
        page.box(px0 - 1, py0 - 1, px1 + 1, py1 + 1, WHITE)
        page.box(px0, py0, px1, py1, NAVY)
        page.box(px0, py0, px0 + 6, py1, colour)
        page.text(
            px0 + 10,
            (py0 + py1) / 2,
            label,
            "black",
            14,
            WHITE,
            "lm",
            within=(px0 + 6, py0, px1, py1),
        )

    leg_y = y + height - legend_h - 1
    page.box(x + 1, leg_y, x + width - 1, y + height - 1, CARD_BG)
    page.box(x + 1, leg_y, x + width - 1, leg_y + 1, RULE)
    cy = leg_y + legend_h / 2
    items = stories.REGIONS
    item_widths = [11 + 5 + width_of(name, "black", 12) for name, _ in items]
    pad_l, pad_r = x + 14, x + width - 14
    gap = (pad_r - pad_l - sum(item_widths)) / (len(items) - 1)
    cx = pad_l
    for name, col in items:
        page.box(int(round(cx)), int(round(cy - 5)), int(round(cx + 10)), int(round(cy + 5)), col)
        end = page.text(
            cx + 14,
            cy,
            name,
            "black",
            12,
            INK,
            "lm",
            within=(x + 4, leg_y, x + width - 4, y + height - 1),
        )
        cx = end[2] + gap


def hero_panel(page, story, x, y, width, height):
    """Upper-right tall illustrated hero lead card: bespoke vector art + giant 20.5px serif head + 14px deck."""
    art_h = 86
    page.box(x, y, x + width, y + height, NAVY)
    page.box(x + 1, y + art_h, x + width - 1, y + height - 1, CARD_BG)

    picture, labels = art.render_scene(story["art"], width - 2, art_h - 1, 4, story.get("note", ""))
    page.image.paste(picture, (x + 1, y + 1))
    for lx, ly, string, size, colour, name, anchor in labels:
        page.text(
            x + 1 + lx,
            y + 1 + ly,
            string,
            name,
            size,
            colour,
            anchor,
            within=(x + 1, y + 1, x + width - 1, y + art_h),
        )

    colour = story["colour"]
    page.box(x + 1, y + art_h, x + width - 1, y + art_h + 3, colour)

    pill = f"#{story['n']}  {story['region']} \u00b7 {story['beat']}"
    pill_w = int(width_of(pill, "black", 12)) + 16
    page.box(x + 1, y + 1, x + 1 + pill_w, y + 21, colour)
    page.text(
        x + 1 + pill_w / 2,
        y + 11,
        pill,
        "black",
        12,
        WHITE,
        "mm",
        within=(x + 1, y + 1, x + 1 + pill_w, y + 21),
    )

    top = y + art_h + 3
    pad = 10
    inner = (x + pad - 2, top, x + width - pad + 2, y + height - 2)
    head_lines = wrap_plain(story["head"], "serif", 20.5, width - 2 * pad, 1)
    page.text(x + pad, top + 25, head_lines[0], "serif", 20.5, INK, within=inner)
    page.text(x + pad, top + 48, story["deck"], "bold", 14, INK, within=inner)


def gallery_card(page, card, x, y, width, height):
    """Bespoke illustrated visual story card: color strip + custom vector scene + ONE giant 17px bold headline."""
    header_h = 22
    art_h = 88
    page.outline_box(x, y, x + width, y + height, CARD_BG, RULE)
    colour = card["colour"]
    # Colored top strip
    page.box(x, y, x + width, y + header_h, colour)
    strip_txt = f"{card['region']} \u00b7 {card['beat']}"
    page.text(
        x + 8,
        y + header_h / 2,
        strip_txt,
        "black",
        12.5,
        WHITE,
        "lm",
        within=(x + 2, y, x + width - 2, y + header_h),
    )

    # Custom bespoke vector illustration
    ax0, ay0 = x + 1, y + header_h
    picture, labels = art.render_scene(card["art"], width - 2, art_h, 4, card.get("note", ""))
    page.image.paste(picture, (ax0, ay0))
    for lx, ly, string, size, lcol, lname, lanchor in labels:
        page.text(
            ax0 + lx,
            ay0 + ly,
            string,
            lname,
            size,
            lcol,
            lanchor,
            within=(ax0, ay0, x + width - 1, ay0 + art_h),
        )
    page.box(x + 1, ay0 + art_h, x + width - 1, ay0 + art_h + 2, colour)

    # ONE bold high-contrast headline (17px serif, 2 crisp lines max — ZERO tiny sub-captions or source lines!)
    text_top = ay0 + art_h + 2
    text_h = (y + height - 2) - text_top
    pad = 8
    text_w = width - 2 * pad
    font_size = 17.0
    line_step = 21.0
    lines = wrap_plain(card["head"], "serif", font_size, text_w, 2)
    block_h = font_size + (len(lines) - 1) * line_step
    first_base = text_top + (text_h - block_h) / 2 + font_size * 0.84
    inner = (x + pad - 2, text_top, x + width - pad + 2, y + height - 2)
    for li, ln in enumerate(lines):
        page.text(x + pad, first_base + li * line_step, ln, "serif", font_size, INK, within=inner)


def global_bottom_strip(page, items, top, height):
    """Deep-navy high-contrast 3x2 bottom wire bar for 6 global & regional beats (14.5px bold pure white)."""
    left, right = MARGIN, SIDE - MARGIN
    width = right - left
    page.box(left, top, right, top + height, NAVY)
    mid_x = left + width // 2
    rows = 3
    row_h = height / rows
    page.box(mid_x, top + 5, mid_x + 1, top + height - 5, "#334155")
    for r in range(1, rows):
        ry = int(round(top + r * row_h))
        page.box(left + 10, ry, right - 10, ry + 1, "#253147")

    for idx, (tag, text, badge_col, _lon, _lat) in enumerate(items):
        row, col = divmod(idx, 2)
        cx0 = left if col == 0 else mid_x + 2
        cx1 = mid_x - 2 if col == 0 else right
        cy0 = top + row * row_h
        cy1 = top + (row + 1) * row_h
        cy = (cy0 + cy1) / 2

        tag_w = 82
        page.box(cx0 + 9, int(round(cy - 10)), cx0 + 9 + tag_w, int(round(cy + 10)), badge_col)
        page.text(
            cx0 + 9 + tag_w / 2,
            cy,
            tag,
            "black",
            12,
            WHITE,
            "mm",
            within=(cx0 + 7, cy0, cx0 + 11 + tag_w, cy1),
        )
        page.text(
            cx0 + 9 + tag_w + 10,
            cy,
            text,
            "bold",
            14.5,
            WHITE,
            "lm",
            within=(cx0 + 9 + tag_w + 7, cy0, cx1 - 6, cy1),
        )


def paint():
    stories.check()
    page = Page()
    y = masthead(page)

    # Upper Visual Hero (y = 83..389, height = 306): Left World Map (602) + Right 2 Hero Lead Cards (388)
    upper_y = y + 4
    upper_h = 306
    map_w = 602
    gap_x = 10
    hero_x = MARGIN + map_w + gap_x
    hero_w = SIDE - MARGIN - hero_x  # 388
    atlas_panel(page, MARGIN, upper_y, map_w, upper_h)

    hero_h = 149
    hero_gap = 8
    for i, hero in enumerate(stories.HEROES):
        hero_panel(page, hero, hero_x, upper_y + i * (hero_h + hero_gap), hero_w, hero_h)

    # Middle Visual Story Gallery (y = 396..916, height = 520): 3 rows x 4 cols = 12 Illustrated Cards
    grid_y = upper_y + upper_h + 7
    card_w = 242
    card_h = 168
    col_gap = 10
    row_gap = 8
    grid_x0 = (SIDE - (4 * card_w + 3 * col_gap)) // 2  # 13
    for idx, card in enumerate(stories.CARDS):
        row, col = divmod(idx, 4)
        cx = grid_x0 + col * (card_w + col_gap)
        cy = grid_y + row * (card_h + row_gap)
        gallery_card(page, card, cx, cy, card_w, card_h)

    # Bottom Deep-Navy Global & Regional Wire Strip (y = 923..1017, height = 94)
    global_bottom_strip(page, stories.GLOBAL_STRIP, grid_y + 3 * card_h + 2 * row_gap + 7, 94)
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
    print(
        f"{os.path.normpath(target)} [v8 / {stories.total_stories()} visual stories]: "
        f"{len(data)} bytes, filter plan {plan}, {len(page.placed)} text runs, {len(problems)} problem(s)"
    )
    if problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
