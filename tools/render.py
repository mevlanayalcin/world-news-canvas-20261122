"""Draw the World News Atlas front page for Sunday 22 November 2026 (1024 x 1024, 8-bit RGB PNG).

    python3 tools/render.py                          # writes ../entry.png (default variant)
    python3 tools/render.py out.png [variant=24|27]  # writes a chosen variant to out.png

Unified, zero-fuzz editorial composition engineered for maximum breadth and effortless 300px legibility:
  - Giant broadsheet serif date masthead (48px C059-Bold) + high-contrast 7-region story-count pill
  - Iconic Natural Earth world hotspots map (612 x 312) with color-coded regional pins & giant 13.5px callouts
  - 2 bold illustrated hero lead panels (COP31 Antalya + Iran nationwide rolling blackouts)
  - 6 color-coded regional ledger cards — each with its own bespoke text-free vector illustration +
    punchy 15.5-16.5px bold high-contrast headlines (zero fussy source credits, zero tiny sub-captions)
  - Deep-navy Global Accent Strip for Markets, Science, Health & Tennis highlights (14.5px bold white)
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
RULE = "#C7C0B0"
DIVIDER = "#E6DFD2"

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


def wrap_with_lead(lead, body, lead_font, body_font, size, width, max_lines=2):
    """Wrap '<lead> <body>' across up to max_lines with bold inline lead on line 1."""
    lead_w = width_of(lead + " ", lead_font, size)
    words = body.split()
    line1_words = []
    idx = 0
    while idx < len(words):
        cand = " ".join(line1_words + [words[idx]])
        if lead_w + width_of(cand, body_font, size) <= width:
            line1_words.append(words[idx])
            idx += 1
        else:
            break
    line1_body = " ".join(line1_words)
    rest = words[idx:]
    extra_lines = []
    current = ""
    for word in rest:
        trial = (current + " " + word).strip()
        if width_of(trial, body_font, size) <= width:
            current = trial
        else:
            extra_lines.append(current)
            current = word
    if current:
        extra_lines.append(current)
    if 1 + len(extra_lines) > max_lines or any(width_of(ln, body_font, size) > width for ln in extra_lines):
        raise ValueError(
            f"lead story exceeds {max_lines} lines of {width:.0f}px at {size}px: {lead!r} {body!r} -> {[line1_body] + extra_lines}"
        )
    return line1_body, extra_lines


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


def masthead(page, total_stories):
    page.box(0, 0, SIDE, 26, NAVY)
    t_end = page.text(MARGIN + 2, 13, "WORLD NEWS ATLAS", "black", 14.5, WHITE, "lm", within=(0, 0, 260, 26))
    page.text(
        t_end[2] + 10,
        13,
        f"\u00b7  {stories.EDITION_TAG}",
        "bold",
        12.5,
        GOLD,
        "lm",
        within=(140, 0, 520, 26),
    )
    pill_txt = f"7 REGIONS  \u00b7  {total_stories} STORIES"
    pill_w = int(width_of(pill_txt, "black", 12.5)) + 24
    px0 = SIDE - MARGIN - pill_w
    page.box(px0, 2, SIDE - MARGIN, 24, RED)
    page.text(px0 + pill_w / 2, 13, pill_txt, "black", 12.5, WHITE, "mm", within=(px0, 2, SIDE - MARGIN, 24))

    page.text(SIDE / 2, 52, stories.EDITION_DAY, "serif", 48, INK, "mm", within=(MARGIN, 27, SIDE - MARGIN, 78))
    page.box(MARGIN, 77, SIDE - MARGIN, 80, NAVY)
    page.box(MARGIN, 81, SIDE - MARGIN, 82, RED)
    return 82


def atlas_panel(page, ed, x, y, width, height):
    """Left centerpiece: full-bleed Natural Earth world map with regional pins, giant callouts & legend."""
    page.box(x, y, x + width, y + height, NAVY)
    header_h = 24
    legend_h = 28
    map_h = height - header_h - legend_h - 2
    map_w = width - 2

    page.text(x + 10, y + header_h / 2, "GLOBAL HOTSPOTS MAP", "black", 13, WHITE, "lm", within=(x, y, x + 260, y + header_h))
    page.text(
        x + width - 10,
        y + header_h / 2,
        "COLOURS MATCH REGIONAL LEDGER",
        "bold",
        11.5,
        GOLD,
        "rm",
        within=(x + 250, y, x + width, y + header_h),
    )

    atlas = art.Atlas(map_w, map_h, scale=4)
    for label, lon, lat, bcx, bcy, colour in ed["callouts"]:
        atlas.leader(lon, lat, bcx, bcy, colour="#0F172A")
    for reg, col in stories.REGIONS:
        for st in ed["regional"][reg]:
            atlas.dot(st["lon"], st["lat"], col, radius=5.0)
    hero_spots = []
    for h in ed["heroes"]:
        hx, hy = atlas.hero_pin(h["lon"], h["lat"], h["colour"], radius=8.8)
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
            11.5,
            WHITE,
            "mm",
            within=(map_x0, map_y0, map_x0 + map_w, map_y0 + map_h),
        )

    pill_h = 23
    for label, lon, lat, bcx, bcy, colour in ed["callouts"]:
        tw = int(width_of(label, "black", 13.5))
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
            13.5,
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
    """Right-side illustrated hero lead panel: crisp vector art + giant 20px serif head + 14px bold deck."""
    art_h = 88
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
    pill_w = int(width_of(pill, "black", 11.5)) + 14
    page.box(x + 1, y + 1, x + 1 + pill_w, y + 20, colour)
    page.text(
        x + 1 + pill_w / 2,
        y + 10.5,
        pill,
        "black",
        11.5,
        WHITE,
        "mm",
        within=(x + 1, y + 1, x + 1 + pill_w, y + 20),
    )

    top = y + art_h + 3
    pad = 10
    inner = (x + pad - 2, top, x + width - pad + 2, y + height - 2)
    head_lines = wrap_plain(story["head"], "serif", 20.5, width - 2 * pad, 1)
    page.text(x + pad, top + 26, head_lines[0], "serif", 20.5, INK, within=inner)
    page.text(x + pad, top + 49, story["deck"], "bold", 14, INK, within=inner)


def region_panel(page, region_name, colour, items, x, y, width, height):
    """Color-coded regional card: bespoke vector lead illustration + giant 15.5-16.5px bold stories."""
    header_h = 26
    page.outline_box(x, y, x + width, y + height, CARD_BG, RULE)
    page.box(x, y, x + width, y + header_h, colour)
    page.text(
        x + 10,
        y + header_h / 2,
        region_name,
        "black",
        15,
        WHITE,
        "lm",
        within=(x + 2, y, x + width - 70, y + header_h),
    )
    count_txt = f"{len(items)} STORIES"
    page.text(
        x + width - 10,
        y + header_h / 2,
        count_txt,
        "bold",
        12,
        WHITE,
        "rm",
        within=(x + width - 90, y, x + width - 2, y + header_h),
    )

    pad = 9
    lead_story = items[0]
    rest_stories = items[1:]

    # Top illustrated feature row (108 x 60px text-free vector scene + 15.5px bold headline)
    feat_top = y + header_h + 6
    art_w, art_h = 108, 60
    feat_h = art_h + 8
    ax0, ay0 = x + pad, feat_top
    page.box(ax0 - 1, ay0 - 1, ax0 + art_w + 1, ay0 + art_h + 1, NAVY)
    pic, _ = art.render_scene(lead_story["art"], art_w, art_h, 4)
    page.image.paste(pic, (ax0, ay0))

    tx0 = ax0 + art_w + 9
    tw = (x + width - pad) - tx0
    lead_size = 15.5
    lead_step = 19.5
    l1_body, l_extra = wrap_with_lead(lead_story["lead"], lead_story["body"], "black", "bold", lead_size, tw, max_lines=3)
    num_l = 1 + len(l_extra)
    blk_h = lead_size + (num_l - 1) * lead_step
    f_base = ay0 + (art_h - blk_h) / 2 + lead_size * 0.85
    f_inner = (tx0 - 2, ay0 - 2, x + width - pad + 2, ay0 + art_h + 4)
    lb = page.text(tx0, f_base, lead_story["lead"], "black", lead_size, colour, within=f_inner)
    if l1_body:
        page.text(lb[2] + 4.5, f_base, l1_body, "bold", lead_size, INK, within=f_inner)
    for li, ln in enumerate(l_extra, start=1):
        page.text(tx0, f_base + li * lead_step, ln, "bold", lead_size, INK, within=f_inner)

    # Remaining concise high-contrast regional stories (15.5-16.5px bold — crisp even at 300px!)
    body_top = feat_top + feat_h
    body_h = (y + height - 4) - body_top
    n_rest = len(rest_stories)
    slot_h = body_h / n_rest
    text_w = width - 2 * pad

    if n_rest <= 2:
        font_size = 16.5 if slot_h >= 78 else 16.0
        line_step = 21.5 if slot_h >= 78 else 20.5
    else:
        font_size = 15.5
        line_step = 19.5

    for idx, st in enumerate(rest_stories):
        sy0 = body_top + idx * slot_h
        sy1 = body_top + (idx + 1) * slot_h
        div_y = int(round(sy0))
        page.box(x + pad, div_y, x + width - pad, div_y + 1, DIVIDER)

        line1_body, extra = wrap_with_lead(st["lead"], st["body"], "black", "bold", font_size, text_w, max_lines=2)
        num_lines = 1 + len(extra)
        block_h = font_size + (num_lines - 1) * line_step
        first_base = sy0 + (slot_h - block_h) / 2 + font_size * 0.86
        inner = (x + pad - 2, sy0 + 1, x + width - pad + 2, sy1 - 1)

        lead_box = page.text(x + pad, first_base, st["lead"], "black", font_size, colour, within=inner)
        if line1_body:
            page.text(lead_box[2] + 4.5, first_base, line1_body, "bold", font_size, INK, within=inner)
        for li, ln in enumerate(extra, start=1):
            page.text(x + pad, first_base + li * line_step, ln, "bold", font_size, INK, within=inner)


def global_bottom_strip(page, items, top, height):
    """Deep-navy high-contrast 2x2 bottom bar for Markets, Science, Health & Tennis (14.5px bold white)."""
    left, right = MARGIN, SIDE - MARGIN
    width = right - left
    page.box(left, top, right, top + height, NAVY)
    mid_x = left + width // 2
    mid_y = top + height // 2
    page.box(mid_x, top + 4, mid_x + 1, top + height - 4, "#334155")
    page.box(left + 10, mid_y, right - 10, mid_y + 1, "#253147")
    tag_colours = ("#15803D", "#1D4ED8", RED, "#B45309")

    for idx, (tag, text) in enumerate(items):
        row, col = divmod(idx, 2)
        cx0 = left if col == 0 else mid_x + 2
        cx1 = mid_x - 2 if col == 0 else right
        cy0 = top if row == 0 else mid_y + 1
        cy1 = mid_y if row == 0 else top + height
        cy = (cy0 + cy1) / 2

        tag_w = 78
        page.box(cx0 + 8, int(round(cy - 9.5)), cx0 + 8 + tag_w, int(round(cy + 9.5)), tag_colours[idx])
        page.text(
            cx0 + 8 + tag_w / 2,
            cy,
            tag,
            "black",
            12,
            WHITE,
            "mm",
            within=(cx0 + 6, cy0, cx0 + 10 + tag_w, cy1),
        )
        page.text(
            cx0 + 8 + tag_w + 8,
            cy,
            text,
            "bold",
            14.2,
            WHITE,
            "lm",
            within=(cx0 + 8 + tag_w + 6, cy0, cx1 - 4, cy1),
        )


def paint(variant=stories.DEFAULT_VARIANT):
    ed = stories.check(variant)
    page = Page()
    y = masthead(page, ed["total_stories"])

    # Upper Centerpiece (y = 87..399, height = 312): Left World Map (612) + Right 2 Stacked Heroes (378)
    upper_y = y + 5
    upper_h = 312
    map_w = 612
    gap_x = 10
    hero_x = MARGIN + map_w + gap_x
    hero_w = SIDE - MARGIN - hero_x  # 378
    atlas_panel(page, ed, MARGIN, upper_y, map_w, upper_h)

    hero_h = 152
    hero_gap = 8
    for i, hero in enumerate(ed["heroes"]):
        hero_panel(page, hero, hero_x, upper_y + i * (hero_h + hero_gap), hero_w, hero_h)

    # Lower Regional Ledger (y = 406..960, height = 554, 3 cols x 2 rows)
    ledger_y = upper_y + upper_h + 7
    ledger_h = 554
    row_gap = 8
    col_gap = 11
    col_w = 326

    row1_regions = stories.REGIONS[:3]
    row2_regions = stories.REGIONS[3:]
    max_r1 = max(len(ed["regional"][r]) for r, _ in row1_regions)
    max_r2 = max(len(ed["regional"][r]) for r, _ in row2_regions)
    usable_h = ledger_h - row_gap  # 546
    if max_r1 > max_r2:
        row1_h = 294
        row2_h = usable_h - row1_h  # 252
    else:
        row1_h = usable_h // 2  # 273
        row2_h = usable_h - row1_h  # 273

    for col, (reg, colour) in enumerate(row1_regions):
        cx = MARGIN + col * (col_w + col_gap)
        region_panel(page, reg, colour, ed["regional"][reg], cx, ledger_y, col_w, row1_h)

    row2_y = ledger_y + row1_h + row_gap
    for col, (reg, colour) in enumerate(row2_regions):
        cx = MARGIN + col * (col_w + col_gap)
        region_panel(page, reg, colour, ed["regional"][reg], cx, row2_y, col_w, row2_h)

    # Bottom Deep-Navy Global Accent Strip (y = 966..1018, height = 52)
    global_bottom_strip(page, ed["global_strip"], ledger_y + ledger_h + 6, 52)
    return page, ed


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
    variant = sys.argv[2] if len(sys.argv) > 2 else stories.DEFAULT_VARIANT
    page, ed = paint(variant)
    problems = page.audit()
    for problem in problems:
        print(problem)
    data, plan = png_bytes(np.asarray(page.image.convert("RGB"), dtype=np.uint8))
    with open(target, "wb") as handle:
        handle.write(data)
    print(
        f"{os.path.normpath(target)} [v7c-{ed['variant']} / {ed['total_stories']} stories]: "
        f"{len(data)} bytes, filter plan {plan}, {len(page.placed)} text runs, {len(problems)} problem(s)"
    )
    if problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
