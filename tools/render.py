"""Draw the v15 Chronicle Front Page for Sunday 22 November 2026 (2x supersampled 2048x2048 -> 1024x1024 RGB PNG).

    python3 tools/render.py /tmp/news22_v15_cand.png   # render candidate without touching entry.png
    python3 tools/render.py                            # writes ../entry.png

All-ivory archival broadsheet combining 13 richly illustrated stories with a 23-item light-ivory sourced wire:
  - Band 1 (0..60): Editorial masthead ribbon + 38px C059-Bold serif Sunday 22 November 2026
  - Band 2 (63..99): THE DAY IN UTC chronological timeline strip (04:00Z -> 21:40Z, 6 verified milestones)
  - Band 3 (104..332): Top 3 flagship illustrated lead stories (#1-#3) with verification badges & 3-line factual decks
  - Band 4 (338..678): 10 illustrated feature cards (#4-#13, 2 rows x 5 cols) with stat plaques & factual decks
  - Band 5 (684..932): Bottom-left Natural Earth map (1-13 deconflicted pins + counts) + 23-story light-ivory wire
  - Band 6 (937..1018): Crimson-bordered DATE CHECK audit box + verification stamp legend & method footer
Every text placement is strictly audited in logical 1024x1024 coordinates for zero overlap and zero clipping.
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
SCALE = 2
MARGIN = 12

IVORY = "#FAF8F3"
CARD_BG = "#FFFFFF"
TIMELINE_BG = "#F2EDE2"
AUDIT_BG = "#FFFDF8"
NAVY = "#0F172A"
INK = "#0B1220"
BODY_INK = "#1E293B"
MUTED = "#475569"
WHITE = "#FFFFFF"
RED = "#B8251E"
GOLD = "#FDE68A"
HAIRLINE = "#D6CEBF"
ROW_RULE = "#E8E2D5"

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
    key = (name, round(float(size), 2))
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(FONT_FILES[name], size)
    return _fonts[key]


def width_of(text, name, size):
    """Logical width (in 1024px coordinates) measured at render scale."""
    return font(name, size * SCALE).getlength(text) / SCALE


def wrap_lines(text, name, size, max_w, max_lines):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if width_of(trial, name, size) <= max_w:
            cur = trial
        else:
            if not cur:
                raise ValueError(f"word too wide ({width_of(w, name, size):.1f} > {max_w:.1f}): {w!r}")
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        raise ValueError(f"wrapped to {len(lines)} > {max_lines} lines at {size}px in {max_w:.1f}px: {text!r} -> {lines}")
    return lines


def fit_wrap(text, name, sizes, max_w, max_lines):
    for sz in sizes:
        try:
            return sz, wrap_lines(text, name, sz, max_w, max_lines)
        except ValueError:
            continue
    raise ValueError(f"cannot fit {text!r} in {max_lines} lines of {max_w:.1f}px at {sizes}")


class Page:
    """2x supersampled drawing surface with strict logical-coordinate (1024x1024) overlap & bounds audit."""

    def __init__(self):
        self.image = Image.new("RGB", (SIDE * SCALE, SIDE * SCALE), IVORY)
        self.draw = ImageDraw.Draw(self.image)
        self.placed = []
        self.problems = []

    def box(self, x0, y0, x1, y1, colour):
        self.draw.rectangle([x0 * SCALE, y0 * SCALE, x1 * SCALE - 1, y1 * SCALE - 1], fill=colour)

    def outline_box(self, x0, y0, x1, y1, fill, outline, width=1.0):
        self.draw.rectangle(
            [x0 * SCALE, y0 * SCALE, x1 * SCALE - 1, y1 * SCALE - 1],
            fill=fill,
            outline=outline,
            width=max(1, int(round(width * SCALE))),
        )

    def circle(self, cx, cy, r, fill, outline=None, width=1.0):
        self.draw.ellipse(
            [(cx - r) * SCALE, (cy - r) * SCALE, (cx + r) * SCALE, (cy + r) * SCALE],
            fill=fill,
            outline=outline,
            width=max(1, int(round(width * SCALE))) if outline else 0,
        )

    def pill(self, x0, y0, x1, y1, radius, fill):
        self.draw.rounded_rectangle(
            [x0 * SCALE, y0 * SCALE, x1 * SCALE - 1, y1 * SCALE - 1],
            radius=radius * SCALE,
            fill=fill,
        )

    def paste_hi(self, img, x, y):
        """Paste an already-2x-resolution image onto the 2x surface at logical (x, y)."""
        self.image.paste(img, (int(round(x * SCALE)), int(round(y * SCALE))))

    def text(self, x, y, string, name, size, colour, anchor="ls", within=None, audit_overlap=True):
        face = font(name, size * SCALE)
        self.draw.text((x * SCALE, y * SCALE), string, font=face, fill=colour, anchor=anchor)
        raw_bb = self.draw.textbbox((x * SCALE, y * SCALE), string, font=face, anchor=anchor)
        bbox = tuple(v / SCALE for v in raw_bb)
        if audit_overlap:
            self.placed.append((bbox, string, within))
        if within is not None:
            x0, y0, x1, y1 = within
            if bbox[0] < x0 - 0.6 or bbox[1] < y0 - 0.6 or bbox[2] > x1 + 0.6 or bbox[3] > y1 + 0.6:
                self.problems.append(f"CLIPPED {string!r}: {tuple(round(v, 1) for v in bbox)} outside {within}")
        return bbox

    def audit(self):
        for i in range(len(self.placed)):
            a = self.placed[i][0]
            for j in range(i + 1, len(self.placed)):
                b = self.placed[j][0]
                if min(a[2], b[2]) - max(a[0], b[0]) > 0.6 and min(a[3], b[3]) - max(a[1], b[1]) > 0.6:
                    self.problems.append(f"OVERLAP {self.placed[i][1]!r} x {self.placed[j][1]!r}")
        return self.problems

    def finish(self):
        return self.image.resize((SIDE, SIDE), Image.Resampling.LANCZOS)


def masthead(page):
    """Band 1 (y=0..60): crisp editorial ribbon + 38px serif Sunday 22 November 2026 + double archival rule."""
    page.box(0, 0, SIDE, 20, NAVY)
    t_end = page.text(MARGIN, 10, stories.EDITION_TITLE, "black", 11.8, WHITE, "lm", within=(0, 0, 260, 20))
    page.text(
        t_end[2] + 8,
        10,
        f"\u00b7  {stories.EDITION_SUB}",
        "bold",
        11.2,
        GOLD,
        "lm",
        within=(140, 0, 560, 20),
    )
    pill_txt = f"{stories.total_stories()} STORIES \u00b7 7 REGIONS \u00b7 16 BEATS \u00b7 ALL SOURCED"
    pill_w = width_of(pill_txt, "black", 11.0) + 18
    px0 = SIDE - MARGIN - pill_w
    page.box(px0, 2, SIDE - MARGIN, 18, RED)
    page.text(px0 + pill_w / 2, 10, pill_txt, "black", 11.0, WHITE, "mm", within=(px0, 2, SIDE - MARGIN, 18))

    page.text(SIDE / 2, 39, stories.EDITION_DAY, "serif", 37.5, INK, "mm", within=(MARGIN, 20, SIDE - MARGIN, 58))
    page.box(MARGIN, 57, SIDE - MARGIN, 59, NAVY)
    page.box(MARGIN, 60, SIDE - MARGIN, 61, HAIRLINE)
    return 61


def timeline_band(page, top, height):
    """Band 2 (y=63..99): chronological THE DAY IN UTC ribbon with 6 pill-masked milestones."""
    left, right = MARGIN, SIDE - MARGIN
    page.outline_box(left, top, right, top + height, TIMELINE_BG, HAIRLINE)
    badge_w = 82
    page.box(left + 1, top + 1, left + badge_w, top + height - 1, NAVY)
    page.text(left + badge_w / 2, top + 11.5, "THE DAY", "black", 10.5, GOLD, "mm", within=(left, top, left + badge_w, top + 20))
    page.text(left + badge_w / 2, top + 25.0, "IN UTC", "black", 10.5, WHITE, "mm", within=(left, top + 16, left + badge_w, top + height))

    track_x0 = left + badge_w + 12
    track_x1 = right - 10
    track_y = top + 12
    page.box(track_x0, track_y, track_x1, track_y + 1.5, "#B5AEA0")

    n = len(stories.TIMELINE)
    slot_w = (track_x1 - track_x0) / n
    for idx, (utc, label, region) in enumerate(stories.TIMELINE):
        col = stories.REGION_COLOUR[region]
        sx0 = track_x0 + idx * slot_w
        dot_x = sx0 + 6
        tw = width_of(utc, "black", 10.8)
        page.box(dot_x + 4, top + 4, dot_x + 12 + tw, top + 19, TIMELINE_BG)
        page.circle(dot_x, track_y + 0.75, 4.2, WHITE, outline=col, width=1.6)
        page.circle(dot_x, track_y + 0.75, 2.0, col)
        page.text(
            dot_x + 8,
            track_y + 0.8,
            utc,
            "black",
            10.8,
            col,
            "lm",
            within=(sx0, top + 1, sx0 + slot_w - 2, top + 20),
        )
        page.text(
            sx0 + 2,
            top + 27.5,
            label,
            "bold",
            11.0,
            INK,
            "lm",
            within=(sx0, top + 18, sx0 + slot_w - 2, top + height - 1),
        )


def draw_lead_card(page, story, x, y, width, height):
    """Band 3: Flagship lead story card (326 x 228) with bespoke vector art, verification badge, headline & 3-line deck."""
    col = stories.REGION_COLOUR[story["region"]]
    vcol = stories.VERIFY_COLOUR[story["verify"]]
    page.outline_box(x, y, x + width, y + height, CARD_BG, HAIRLINE)
    page.box(x, y, x + width, y + 3, col)

    # Top metadata strip (y+3..y+23)
    hdr_y0, hdr_y1 = y + 3, y + 23
    hdr_cy = (hdr_y0 + hdr_y1) / 2
    page.box(x + 1, hdr_y0, x + width - 1, hdr_y1, IVORY)
    page.circle(x + 12, hdr_cy, 7.2, col)
    page.text(x + 12, hdr_cy, str(story["n"]), "black", 10.5, WHITE, "mm", within=(x + 3, hdr_y0, x + 21, hdr_y1))
    page.text(
        x + 23,
        hdr_cy,
        story["kicker"],
        "black",
        10.8,
        col,
        "lm",
        within=(x + 21, hdr_y0, x + width - 82, hdr_y1),
    )
    vw = width_of(story["verify"], "black", 9.2) + 10
    vx0 = x + width - 6 - vw
    page.pill(vx0, hdr_cy - 6.5, x + width - 6, hdr_cy + 6.5, 3, vcol)
    page.text(vx0 + vw / 2, hdr_cy, story["verify"], "black", 9.2, WHITE, "mm", within=(vx0 - 1, hdr_y0, x + width - 4, hdr_y1))

    # Crisp 2x vector illustration (324 x 92 logical -> 648 x 184 px)
    ax0, ay0 = x + 1, hdr_y1
    aw, ah = width - 2, 92
    pic, labels = art.render_scene(story["art"], int(round(aw * SCALE)), int(round(ah * SCALE)), scale=2, note=story["note"])
    page.paste_hi(pic, ax0, ay0)
    for lx, ly, string, size, lcol, lname, lanchor in labels:
        # art.render_scene returns label coords in pic's pixels (2x), so divide by SCALE for logical coords
        sz = max(10.5, round(float(size) * 0.90, 1))
        page.text(
            ax0 + lx / SCALE,
            ay0 + ly / SCALE,
            string,
            lname,
            sz,
            lcol,
            lanchor,
            within=(ax0, ay0, ax0 + aw, ay0 + ah),
        )
    page.box(x + 1, ay0 + ah, x + width - 1, ay0 + ah + 2, col)

    # Editorial text block (y+117..y+227, height=110)
    top = ay0 + ah + 2
    pad = 8
    text_w = width - 2 * pad
    inner = (x + pad - 1, top, x + width - pad + 1, y + height - 2)

    h_sz, h_lines = fit_wrap(story["head"], "black", (15.8, 15.2, 14.5), text_w, 2)
    h_step = 18.0
    cy = top + 16.5
    for ln in h_lines:
        page.text(x + pad, cy, ln, "black", h_sz, INK, "ls", within=inner)
        cy += h_step

    d_sz, d_lines = fit_wrap(story["deck"], "semi", (11.2, 10.8, 10.4), text_w, 3)
    d_step = 13.6
    dy = cy + 1.5
    for ln in d_lines:
        page.text(x + pad, dy, ln, "semi", d_sz, BODY_INK, "ls", within=inner)
        dy += d_step

    page.text(x + pad, y + height - 6.5, f"Sources: {story['src']}", "bold", 9.8, MUTED, "ls", within=inner)


def draw_feature_card(page, card, x, y, width, height):
    """Band 4: Illustrated feature card (194 x 166) with focal vector panel, verification pill, headline & sub-deck."""
    col = stories.REGION_COLOUR[card["region"]]
    vcol = stories.VERIFY_COLOUR[card["verify"]]
    page.outline_box(x, y, x + width, y + height, CARD_BG, HAIRLINE)
    page.box(x, y, x + width, y + 2.5, col)

    hdr_y0, hdr_y1 = y + 2.5, y + 20.5
    hdr_cy = (hdr_y0 + hdr_y1) / 2
    page.box(x + 1, hdr_y0, x + width - 1, hdr_y1, IVORY)
    page.circle(x + 10.5, hdr_cy, 6.8, col)
    page.text(x + 10.5, hdr_cy, str(card["n"]), "black", 9.5, WHITE, "mm", within=(x + 2, hdr_y0, x + 19, hdr_y1))
    page.text(
        x + 20,
        hdr_cy,
        card["kicker"],
        "black",
        9.4,
        col,
        "lm",
        within=(x + 18, hdr_y0, x + width - 22, hdr_y1),
    )
    vcode = card["verify"][0]  # C or O
    page.pill(x + width - 19, hdr_cy - 6.0, x + width - 4, hdr_cy + 6.0, 2.5, vcol)
    page.text(x + width - 11.5, hdr_cy, vcode, "black", 9.0, WHITE, "mm", within=(x + width - 20, hdr_y0, x + width - 3, hdr_y1))

    # 2x supersampled crisp vector art (192 x 52 logical -> 384 x 104 px)
    ax0, ay0 = x + 1, hdr_y1
    aw, ah = width - 2, 52
    pic, labels = art.render_scene(card["art"], int(round(aw * SCALE)), int(round(ah * SCALE)), scale=2, note=card["note"])
    page.paste_hi(pic, ax0, ay0)
    for lx, ly, string, size, lcol, lname, lanchor in labels:
        # Scale art plaque label cleanly for compact 192x52 panel
        sz = max(9.2, min(11.2, round(float(size) * 0.66, 1)))
        # Clamp label center inside panel so nothing clips on narrow cards
        tw_half = width_of(string, lname, sz) / 2.0 + 2.0
        px = ax0 + lx / SCALE
        if lanchor == "mm":
            px = max(ax0 + tw_half, min(px, ax0 + aw - tw_half))
        page.text(
            px,
            ay0 + ly / SCALE,
            string,
            lname,
            sz,
            lcol,
            lanchor,
            within=(ax0, ay0, ax0 + aw, ay0 + ah),
        )
    page.box(x + 1, ay0 + ah, x + width - 1, ay0 + ah + 1.5, col)

    # Headline + factual sub-deck + source (y+74..y+165, height=91)
    top = ay0 + ah + 1.5
    pad = 6
    text_w = width - 2 * pad
    inner = (x + pad - 1, top, x + width - pad + 1, y + height - 2)

    h_sz, h_lines = fit_wrap(card["head"], "black", (12.4, 11.9, 11.4), text_w, 2)
    h_step = 13.8
    cy = top + 13.5
    for ln in h_lines:
        page.text(x + pad, cy, ln, "black", h_sz, INK, "ls", within=inner)
        cy += h_step

    d_sz, d_lines = fit_wrap(card["deck"], "semi", (10.3, 9.9, 9.5), text_w, 3)
    d_step = 11.8
    dy = cy + 0.5
    for ln in d_lines:
        page.text(x + pad, dy, ln, "semi", d_sz, BODY_INK, "ls", within=inner)
        dy += d_step

    page.text(x + pad, y + height - 5.0, card["src"], "bold", 9.2, MUTED, "ls", within=inner)


# Small visual de-confliction offsets (in degrees) ONLY where two pins sit <100 km apart on the 274px map
MAP_PIN_NUDGE = {
    1: (-5.0, 2.5),    # Antalya clear NW of Gaza
    2: (2.0, 6.0),     # Kyiv/Dymer clear N
    4: (2.0, 9.0),     # Manchester clear N of Liverpool
    6: (10.0, 5.0),    # Germany clear E of UK
    7: (-8.0, -4.0),   # Vandenberg SpaceX SW of Vegas
    9: (4.0, -7.0),    # Gaza clear SE of Antalya
    10: (4.0, -5.0),   # Turin clear S of Germany
    11: (8.0, 6.0),    # Las Vegas NE of Vandenberg
    12: (-11.0, -4.0), # Liverpool clear SW of Manchester
}


def draw_map_panel(page, x, y, width, height):
    """Band 5 Left (276 x 248): Natural Earth map with deconflicted numbered pins 1-13 + wire dots + region counts."""
    page.outline_box(x, y, x + width, y + height, CARD_BG, HAIRLINE)
    hdr_h = 20
    leg_h = 38
    map_h = height - hdr_h - leg_h - 2
    map_w = width - 2

    page.box(x + 1, y + 1, x + width - 1, y + hdr_h, NAVY)
    page.text(x + 7, y + hdr_h / 2, "WHERE IT HAPPENED", "black", 10.5, WHITE, "lm", within=(x, y, x + 170, y + hdr_h))
    page.text(x + width - 7, y + hdr_h / 2, "PINS 1\u201313 + WIRE", "bold", 9.6, GOLD, "rm", within=(x + 145, y, x + width, y + hdr_h))

    atlas = art.Atlas(
        int(round(map_w * SCALE)),
        int(round(map_h * SCALE)),
        scale=2,
        sea="#DCEAF6",
        sea_edge="#8CA8C0",
        land="#EDE3CC",
        coast="#8C7E66",
        paper=IVORY,
        grid="#C7DBEC",
    )
    # Subtle dots for wire items #14-#36
    for w in stories.WIRE:
        if w["lon"] is not None and w["lat"] is not None:
            atlas.dot(w["lon"], w["lat"], stories.REGION_COLOUR[w["region"]], radius=3.4 * SCALE)

    # Numbered pins 1-13 with collision-free nudging
    pin_spots = []
    for s in stories.LEADS + stories.FEATURES:
        dlon, dlat = MAP_PIN_NUDGE.get(s["n"], (0.0, 0.0))
        plon, plat = s["lon"] + dlon, s["lat"] + dlat
        col = stories.REGION_COLOUR[s["region"]]
        hx, hy = atlas.hero_pin(plon, plat, col, radius=6.4 * SCALE)
        pin_spots.append((hx / SCALE, hy / SCALE, str(s["n"])))

    mx0, my0 = x + 1, y + hdr_h + 1
    page.paste_hi(atlas.finish(), mx0, my0)
    for hx, hy, ns in pin_spots:
        page.text(
            mx0 + hx,
            my0 + hy,
            ns,
            "black",
            8.8,
            WHITE,
            "mm",
            within=(mx0, my0, mx0 + map_w, my0 + map_h),
        )

    # 2-row region-count legend computed programmatically from stories.region_counts()
    leg_y = y + height - leg_h - 1
    page.box(x + 1, leg_y, x + width - 1, y + height - 1, IVORY)
    page.box(x + 1, leg_y, x + width - 1, leg_y + 1, HAIRLINE)
    counts = stories.region_counts()
    row1 = ["Americas", "Asia", "Europe", "M. East"]
    row2 = ["Africa", "Global", "Oceania"]
    for r_idx, r_names in enumerate((row1, row2)):
        ry = leg_y + 10.5 + r_idx * 17.0
        labels = [(rn, f"{rn} {counts[rn]}", stories.REGION_COLOUR[rn]) for rn in r_names]
        widths = [7 + 3 + width_of(lbl, "bold", 9.6) for _, lbl, _ in labels]
        pad_l, pad_r = x + 7, x + width - 7
        gap = (pad_r - pad_l - sum(widths)) / max(1, len(labels) - 1) if len(labels) > 1 else 0
        cx = pad_l if r_idx == 0 else x + (width - sum(widths) - 18 * (len(labels) - 1)) / 2
        if r_idx == 1:
            gap = 18
        for _, lbl, col in labels:
            page.box(cx, ry - 3.5, cx + 7, ry + 3.5, col)
            bb = page.text(cx + 9.5, ry, lbl, "bold", 9.6, INK, "lm", within=(x + 3, leg_y, x + width - 3, y + height - 1))
            cx = bb[2] + gap


def draw_wire_panel(page, x, y, width, height):
    """Band 5 Right (716 x 248): Crisp 2-column light-ivory sourced wire list (#14-#36, 12 left + 11 right)."""
    page.outline_box(x, y, x + width, y + height, IVORY, HAIRLINE)
    hdr_h = 20
    page.box(x + 1, y + 1, x + width - 1, y + hdr_h, NAVY)
    page.text(
        x + 8,
        y + hdr_h / 2,
        "ALSO ON SUNDAY 22 NOVEMBER  \u00b7  #14\u2013#36",
        "black",
        10.6,
        WHITE,
        "lm",
        within=(x, y, x + 360, y + hdr_h),
    )
    page.text(
        x + width - 8,
        y + hdr_h / 2,
        "23 SOURCED DISPATCHES  \u00b7  C CONFIRMED  \u00b7  O OFFICIAL  \u00b7  R REPORTED",
        "bold",
        9.6,
        GOLD,
        "rm",
        within=(x + 300, y, x + width, y + hdr_h),
    )

    body_y = y + hdr_h + 1
    body_h = height - hdr_h - 2
    rows = 12
    row_h = body_h / rows
    mid_x = x + width / 2
    page.box(mid_x, body_y + 4, mid_x + 1, y + height - 4, HAIRLINE)

    for idx, item in enumerate(stories.WIRE):
        col_i = 0 if idx < 12 else 1
        row_i = idx if idx < 12 else idx - 12
        cx0 = x + 1 if col_i == 0 else mid_x + 2
        cx1 = mid_x - 2 if col_i == 0 else x + width - 1
        ry0 = body_y + row_i * row_h
        ry1 = ry0 + row_h
        cy = (ry0 + ry1) / 2

        if row_i > 0:
            page.box(cx0 + 5, ry0, cx1 - 5, ry0 + 0.8, ROW_RULE)

        rcol = stories.REGION_COLOUR[item["region"]]
        vcol = stories.VERIFY_COLOUR[item["code"]]
        within = (cx0 + 2, ry0, cx1 - 2, ry1)

        # Crisp region color tick left
        page.box(cx0 + 5, cy - 4.0, cx0 + 8, cy + 4.0, rcol)

        # Right-aligned compact verification chip [C/O/R] + source outlet
        pill_w = 13.0
        px1 = cx1 - 5
        px0 = px1 - pill_w
        page.pill(px0, cy - 5.5, px1, cy + 5.5, 2.2, vcol)
        page.text((px0 + px1) / 2, cy, item["code"], "black", 8.6, WHITE, "mm", within=(px0 - 1, ry0, px1 + 1, ry1))

        src_sz = 9.2
        src_bb = page.text(px0 - 4, cy, item["src"], "bold", src_sz, MUTED, "rm", within=(cx0 + 180, ry0, px0 - 1, ry1))

        # Left-aligned numbered bold lead + crisp single-line body on warm ivory
        prefix = f"{item['n']}. {item['lead']}"
        avail_w = (src_bb[0] - 5) - (cx0 + 11)
        chosen_sz = None
        for sz in (10.6, 10.2, 9.8, 9.4):
            pw = width_of(prefix, "black", sz)
            sp = width_of(" ", "semi", sz)
            bw = width_of(item["body"], "semi", sz)
            if pw + sp + bw <= avail_w:
                chosen_sz = sz
                break
        if chosen_sz is None:
            raise ValueError(f"Wire item #{item['n']} too wide for {avail_w:.1f}px: {prefix} {item['body']}")

        p_bb = page.text(cx0 + 11, cy, prefix, "black", chosen_sz, INK, "lm", within=(cx0 + 9, ry0, src_bb[0] - 2, ry1))
        page.text(
            p_bb[2] + width_of(" ", "semi", chosen_sz),
            cy,
            item["body"],
            "semi",
            chosen_sz,
            BODY_INK,
            "lm",
            within=(p_bb[2], ry0, src_bb[0] - 2, ry1),
        )


def draw_date_check_and_footer(page, top):
    """Band 6 (y=937..1018): Crimson-bordered ivory DATE CHECK audit box + deep-navy verification legend footer."""
    left, right = MARGIN, SIDE - MARGIN
    dc_h = 56
    page.outline_box(left, top, right, top + dc_h, AUDIT_BG, RED, width=1.4)
    page.box(left, top, left + 5, top + dc_h, RED)

    # Crisp crimson DATE CHECK pill on left
    bw = 90
    page.box(left + 10, top + 7, left + 10 + bw, top + 24, RED)
    page.text(left + 10 + bw / 2, top + 15.5, "DATE CHECK", "black", 10.6, WHITE, "mm", within=(left + 9, top + 5, left + 11 + bw, top + 26))
    page.text(left + 10 + bw / 2, top + 39.5, "22 NOV UTC", "black", 10.0, RED, "mm", within=(left + 6, top + 27, left + 14 + bw, top + 52))

    tx0 = left + 10 + bw + 9
    text_w = right - 8 - tx0
    within_dc = (tx0 - 1, top + 2, right - 6, top + dc_h - 2)

    sat_sz, sat_lines = fit_wrap(stories.DATE_CHECK_SAT, "semi", (10.6, 10.2, 9.8), text_w, 2)
    cy = top + 14.5
    for ln in sat_lines:
        page.text(tx0, cy, ln, "semi", sat_sz, INK, "ls", within=within_dc)
        cy += 13.5
    mon_sz, mon_lines = fit_wrap(stories.DATE_CHECK_MON, "bold", (10.4, 10.0, 9.6), text_w, 1)
    page.text(tx0, cy + 2.0, mon_lines[0], "bold", mon_sz, MUTED, "ls", within=within_dc)

    # Bottom micro-footer (y=997..1018, height=21)
    fy = top + dc_h + 4
    fh = 21
    page.box(left, fy, right, fy + fh, NAVY)
    fcy = fy + fh / 2
    cx = left + 8
    legend_items = [
        ("C", "CONFIRMED", "2+ outlets", "#15803D"),
        ("O", "OFFICIAL", "agency/result", "#1D4ED8"),
        ("R", "REPORTED", "1 outlet", "#9A6700"),
        ("!", "CLAIM", "one side says", "#B8251E"),
    ]
    for code, name, desc, col in legend_items:
        page.pill(cx, fcy - 6, cx + 13, fcy + 6, 2, col)
        page.text(cx + 6.5, fcy, code, "black", 8.8, WHITE, "mm", within=(cx - 1, fy, cx + 14, fy + fh))
        b1 = page.text(cx + 16, fcy, name, "black", 9.4, GOLD, "lm", within=(cx + 14, fy, right, fy + fh))
        b2 = page.text(b1[2] + 3.5, fcy, desc, "medium", 9.2, "#CBD5E1", "lm", within=(b1[2], fy, right, fy + fh))
        cx = b2[2] + 11

    page.text(
        right - 8,
        fcy,
        "Every story occurred or broke Sun 22 Nov 2026 (UTC) \u00b7 Sources named per item \u00b7 Original vector art",
        "bold",
        9.4,
        WHITE,
        "rm",
        within=(cx + 4, fy, right - 4, fy + fh),
    )


def paint():
    stories.check()
    page = Page()
    y = masthead(page)

    # Band 2: THE DAY IN UTC Timeline Strip (y=63..99, height=36)
    tl_y = y + 2
    timeline_band(page, tl_y, 36)

    # Band 3: Top 3 Flagship Illustrated Leads (y=104..332, height=228, 3 cols x 326px, 11px gaps)
    lead_y = tl_y + 36 + 5
    lead_w = 326
    lead_h = 228
    lead_gap = 11
    for i, lead in enumerate(stories.LEADS):
        draw_lead_card(page, lead, MARGIN + i * (lead_w + lead_gap), lead_y, lead_w, lead_h)

    # Band 4: 10 Illustrated Feature Cards (y=338..678, height=340 -> 2 rows x 166 + 8 gap; 5 cols x 194 + 7.5 gap)
    feat_y = lead_y + lead_h + 6
    feat_w = 194
    feat_h = 166
    col_gap = 7.5
    row_gap = 8
    for idx, feat in enumerate(stories.FEATURES):
        row, col = divmod(idx, 5)
        fx = MARGIN + col * (feat_w + col_gap)
        fy = feat_y + row * (feat_h + row_gap)
        draw_feature_card(page, feat, fx, fy, feat_w, feat_h)

    # Band 5: Bottom-Left Natural Earth Map (262 x 248) + Bottom-Right 23-Story Light-Ivory Wire (730 x 248)
    b5_y = feat_y + 2 * feat_h + row_gap + 6  # 684
    b5_h = 248
    map_w = 262
    draw_map_panel(page, MARGIN, b5_y, map_w, b5_h)
    draw_wire_panel(page, MARGIN + map_w + 8, b5_y, SIDE - MARGIN - (MARGIN + map_w + 8), b5_h)

    # Band 6: DATE CHECK Box + Verification Legend Footer (y=937..1018)
    draw_date_check_and_footer(page, b5_y + b5_h + 5)
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
    img_1024 = page.finish().convert("RGB")
    data, plan = png_bytes(np.asarray(img_1024, dtype=np.uint8))
    with open(target, "wb") as handle:
        handle.write(data)
    print(
        f"{os.path.normpath(target)} [v15 / {stories.total_stories()} chronicle stories, 2x LANCZOS]: "
        f"{len(data)} bytes, filter plan {plan}, {len(page.placed)} text runs, {len(problems)} problem(s)"
    )
    if problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
