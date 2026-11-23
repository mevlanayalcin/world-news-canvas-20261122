"""Draw the v11 Museum Flat-Vector 3x3 Visual World Atlas for Sunday 22 November 2026 (1024 x 1024, RGB PNG).

    python3 tools/render.py            # writes ../entry.png
    python3 tools/render.py out.png    # writes somewhere else

Unified museum-grade flat-vector editorial composition with soft archival hairlines & strict >= 15px floor:
  - Giant broadsheet serif date masthead (50px C059-Bold) + clean 7-region 18-story top ribbon
  - High-contrast Natural Earth World Hotspots Map (584 x 306) with 6 giant 18px callouts & uncovered Java dot
  - 2 Full-Header Illustrated Hero Panels (unobstructed art + 23.5px bold serif heads + 16.5px bold decks)
  - 3 x 3 Gallery of 9 Wide Panoramic Museum Vector Cards (balanced zero-widow 21.5px Lato-Black heads + crisp badges)
  - Deep-navy 2 x 2 Giant Wire Footer (15px jewel badges + 18.5px bold pure white lines)
Every text placement is strictly audited for >= 15px floor, exact bounds, and zero overlap before saving.
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
MARGIN = 14
MIN_FONT_PX = 15.0
PAPER = "#FAF6EE"
CARD_BG = "#FFFFFF"
NAVY = "#0F172A"
INK = "#0B1220"
WHITE = "#FFFFFF"
RED = "#B8251E"
GOLD = "#FDE68A"
HAIRLINE = "#D6CCBA"

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


def wrap_balanced(text, name, size, width, max_lines):
    """Wrap text cleanly up to max_lines with visually balanced line widths (zero 1-word widows)."""
    if width_of(text, name, size) <= width:
        return [text]
    words = text.split()
    if max_lines >= 2:
        best = None
        for i in range(1, len(words)):
            l1 = " ".join(words[:i])
            l2 = " ".join(words[i:])
            w1, w2 = width_of(l1, name, size), width_of(l2, name, size)
            if w1 <= width and w2 <= width:
                score = abs(w1 - w2) + (8 if w2 > w1 + 12 else 0)
                if best is None or score < best[0]:
                    best = (score, [l1, l2])
        if best is not None:
            return best[1]
    return wrap_plain(text, name, size, width, max_lines)


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
        if size < MIN_FONT_PX:
            self.problems.append(f"TOO SMALL ({size}px < {MIN_FONT_PX}px): {string!r}")
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
    page.box(0, 0, SIDE, 27, NAVY)
    t_end = page.text(MARGIN, 13.5, "WORLD NEWS ATLAS", "black", 15.5, WHITE, "lm", within=(0, 0, 280, 27))
    page.text(
        t_end[2] + 10,
        13.5,
        f"\u00b7  {stories.EDITION_TAG}",
        "bold",
        15,
        GOLD,
        "lm",
        within=(140, 0, 560, 27),
    )
    pill_txt = f"7 REGIONS \u00b7 {stories.total_stories()} STORIES"
    pill_w = int(width_of(pill_txt, "black", 15)) + 24
    px0 = SIDE - MARGIN - pill_w
    page.box(px0, 2, SIDE - MARGIN, 25, RED)
    page.text(px0 + pill_w / 2, 13.5, pill_txt, "black", 15, WHITE, "mm", within=(px0, 2, SIDE - MARGIN, 25))

    page.text(SIDE / 2, 53, stories.EDITION_DAY, "serif", 50, INK, "mm", within=(MARGIN, 28, SIDE - MARGIN, 78))
    page.box(MARGIN, 77, SIDE - MARGIN, 79, NAVY)
    page.box(MARGIN, 80, SIDE - MARGIN, 81, HAIRLINE)
    return 81


def atlas_panel(page, x, y, width, height):
    """Left centerpiece: open archival Natural Earth map with ONLY 6 giant 18px callouts & 15px legend."""
    page.outline_box(x, y, x + width, y + height, CARD_BG, HAIRLINE)
    header_h = 26
    legend_h = 30
    map_h = height - header_h - legend_h - 2
    map_w = width - 2

    # Open archival cream header strip (no heavy black cage!)
    page.box(x + 1, y + 1, x + width - 1, y + header_h, PAPER)
    page.box(x + 1, y + header_h, x + width - 1, y + header_h + 1, HAIRLINE)
    page.text(x + 10, y + header_h / 2, "WORLD HOTSPOTS", "black", 15, NAVY, "lm", within=(x, y, x + 280, y + header_h))
    page.text(
        x + width - 10,
        y + header_h / 2,
        "ALL 7 REGIONS",
        "black",
        15,
        RED,
        "rm",
        within=(x + 280, y, x + width, y + header_h),
    )

    atlas = art.Atlas(map_w, map_h, scale=4)
    for label, lon, lat, bcx, bcy, colour in stories.MAP_CALLOUTS:
        atlas.leader(lon, lat, bcx, bcy, colour="#1E293B")
    for _, _, _badge, map_col, lon, lat in stories.GLOBAL_STRIP:
        if lon is not None and lat is not None:
            atlas.dot(lon, lat, map_col, radius=5.6)
    for card in stories.CARDS:
        atlas.dot(card["lon"], card["lat"], card["colour"], radius=6.0)
    hero_spots = []
    for h in stories.HEROES:
        hx, hy = atlas.hero_pin(h["lon"], h["lat"], h["colour"], radius=10.4)
        hero_spots.append((hx, hy, str(h["n"])))

    map_img = atlas.finish()
    map_x0 = x + 1
    map_y0 = y + header_h + 1
    page.image.paste(map_img, (map_x0, map_y0))

    for hx, hy, num_str in hero_spots:
        page.text(
            map_x0 + hx,
            map_y0 + hy,
            num_str,
            "black",
            15,
            WHITE,
            "mm",
            within=(map_x0, map_y0, map_x0 + map_w, map_y0 + map_h),
        )

    # ONLY 6 GIANT 18px BOLD OPEN-OCEAN CALLOUTS — zero blur even at 300px!
    pill_h = 28
    for label, lon, lat, bcx, bcy, colour in stories.MAP_CALLOUTS:
        tw = int(width_of(label, "black", 18))
        pw = tw + 22
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
        page.box(px0, py0, px0 + 7, py1, colour)
        page.text(
            px0 + 12,
            (py0 + py1) / 2,
            label,
            "black",
            18,
            WHITE,
            "lm",
            within=(px0 + 7, py0, px1, py1),
        )

    # Clean 15px 6-region color legend strip
    leg_y = y + height - legend_h - 1
    page.box(x + 1, leg_y, x + width - 1, y + height - 1, CARD_BG)
    page.box(x + 1, leg_y, x + width - 1, leg_y + 1, HAIRLINE)
    cy = leg_y + legend_h / 2
    items = stories.REGIONS
    item_widths = [10 + 4 + width_of(name, "black", 15) for name, _ in items]
    pad_l, pad_r = x + 10, x + width - 10
    gap = (pad_r - pad_l - sum(item_widths)) / (len(items) - 1)
    cx = pad_l
    for name, col in items:
        page.box(int(round(cx)), int(round(cy - 5)), int(round(cx + 10)), int(round(cy + 5)), col)
        end = page.text(
            cx + 13,
            cy,
            name,
            "black",
            15,
            INK,
            "lm",
            within=(x + 4, leg_y, x + width - 4, y + height - 1),
        )
        cx = end[2] + gap


def hero_panel(page, story, x, y, width, height):
    """Upper-right illustrated hero panel: clean full-width header + unobstructed vector art + 23.5px head + 16.5px deck."""
    header_h = 22
    art_h = 72
    page.outline_box(x, y, x + width, y + height, CARD_BG, HAIRLINE)

    colour = story["colour"]
    page.box(x, y, x + width, y + header_h, colour)
    pill = f"#{story['n']} {story['region']} \u00b7 {story['beat']}"
    page.text(
        x + 10,
        y + header_h / 2,
        pill,
        "black",
        15,
        WHITE,
        "lm",
        within=(x + 2, y, x + width - 2, y + header_h),
    )

    ax0, ay0 = x + 1, y + header_h
    picture, labels = art.render_scene(story["art"], width - 2, art_h, 4, story.get("note", ""))
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

    top = ay0 + art_h + 2
    pad = 10
    inner = (x + pad - 2, top, x + width - pad + 2, y + height - 2)
    h_size = 23.5 if width_of(story["head"], "serif", 23.5) <= width - 2 * pad else 23.0
    head_lines = wrap_plain(story["head"], "serif", h_size, width - 2 * pad, 1)
    page.text(x + pad, top + 24, head_lines[0], "serif", h_size, INK, within=inner)
    page.text(x + pad, top + 46, story["deck"], "bold", 16.5, INK, within=inner)


def gallery_card(page, card, x, y, width, height):
    """Wide 324 x 168 museum vector card: 15px ribbon + layered vector art + balanced zero-widow 21.5px Lato-Black head."""
    header_h = 24
    art_h = 80
    page.outline_box(x, y, x + width, y + height, CARD_BG, HAIRLINE)
    colour = card["colour"]
    page.box(x, y, x + width, y + header_h, colour)
    strip_txt = f"{card['region']} \u00b7 {card['beat']}"
    page.text(
        x + 10,
        y + header_h / 2,
        strip_txt,
        "black",
        15,
        WHITE,
        "lm",
        within=(x + 2, y, x + width - 2, y + header_h),
    )

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

    # ONE giant 21.5px Lato-Black sans-serif headline (balanced 1-2 lines, ZERO widows, razor-sharp at 300px!)
    text_top = ay0 + art_h + 2
    text_h = (y + height - 2) - text_top
    pad = 10
    text_w = width - 2 * pad
    font_size = 21.5
    line_step = 25.5
    lines = wrap_balanced(card["head"], "black", font_size, text_w, 2)
    block_h = font_size + (len(lines) - 1) * line_step
    first_base = text_top + (text_h - block_h) / 2 + font_size * 0.84
    inner = (x + pad - 2, text_top, x + width - pad + 2, y + height - 2)
    for li, ln in enumerate(lines):
        page.text(x + pad, first_base + li * line_step, ln, "black", font_size, INK, within=inner)


def global_bottom_strip(page, items, top, height):
    """Deep-navy giant 2x2 wire footer: 15px jewel badges + 17.5px bold pure white lines."""
    left, right = MARGIN, SIDE - MARGIN
    width = right - left
    page.box(left, top, right, top + height, NAVY)
    mid_x = left + width // 2
    mid_y = top + height // 2
    page.box(mid_x, top + 6, mid_x + 1, top + height - 6, "#334155")
    page.box(left + 12, mid_y, right - 12, mid_y + 1, "#253147")

    for idx, (tag, text, badge_col, _map_col, _lon, _lat) in enumerate(items):
        row, col = divmod(idx, 2)
        cx0 = left if col == 0 else mid_x + 2
        cx1 = mid_x - 2 if col == 0 else right
        cy0 = top if row == 0 else mid_y + 1
        cy1 = mid_y if row == 0 else top + height
        cy = (cy0 + cy1) / 2

        tag_w = 100
        page.box(cx0 + 10, int(round(cy - 12.5)), cx0 + 10 + tag_w, int(round(cy + 12.5)), badge_col)
        page.text(
            cx0 + 10 + tag_w / 2,
            cy,
            tag,
            "black",
            15,
            WHITE,
            "mm",
            within=(cx0 + 8, cy0, cx0 + 12 + tag_w, cy1),
        )
        page.text(
            cx0 + 10 + tag_w + 11,
            cy,
            text,
            "bold",
            18.5,
            WHITE,
            "lm",
            within=(cx0 + 10 + tag_w + 7, cy0, cx1 - 6, cy1),
        )


def paint():
    stories.check()
    page = Page()
    y = masthead(page)

    # Upper Visual Hero (y = 86..392, height = 306): Left Airy Map (584) + Right 2 Hero Cards (400)
    upper_y = y + 5
    upper_h = 306
    map_w = 584
    gap_x = 12
    hero_x = MARGIN + map_w + gap_x
    hero_w = SIDE - MARGIN - hero_x  # 400
    atlas_panel(page, MARGIN, upper_y, map_w, upper_h)

    hero_h = 148
    hero_gap = 10
    for i, hero in enumerate(stories.HEROES):
        hero_panel(page, hero, hero_x, upper_y + i * (hero_h + hero_gap), hero_w, hero_h)

    # Middle Visual Gallery (y = 401..925, height = 524): 3 rows x 3 cols = 9 Wide Cards (324 x 168, 12px gaps)
    grid_y = upper_y + upper_h + 9
    card_w = 324
    card_h = 168
    col_gap = 12
    row_gap = 10
    for idx, card in enumerate(stories.CARDS):
        row, col = divmod(idx, 3)
        cx = MARGIN + col * (card_w + col_gap)
        cy = grid_y + row * (card_h + row_gap)
        gallery_card(page, card, cx, cy, card_w, card_h)

    # Bottom Deep-Navy Giant 2x2 Wire Strip (y = 934..1016, height = 82)
    global_bottom_strip(page, stories.GLOBAL_STRIP, grid_y + 3 * card_h + 2 * row_gap + 9, 82)
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
        f"{os.path.normpath(target)} [v11 / {stories.total_stories()} museum flat-vector stories]: "
        f"{len(data)} bytes, filter plan {plan}, {len(page.placed)} text runs, {len(problems)} problem(s)"
    )
    if problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
