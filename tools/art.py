"""Vector illustrations for the World Ledger front page.

Every scene is drawn with plain Pillow shapes on an oversized canvas and box-filtered down, so edges come out
smooth without any photo or outside artwork. Scenes are described in a 352 x 100 unit box; the caller decides
how many pixels that box covers (a lead card is larger than a secondary card). Text inside a scene is not drawn
here: each scene returns a list of labels that the page renderer sets at final resolution so glyphs stay crisp.
"""

import json
import math
import os

from PIL import Image, ImageDraw

UNITS_W = 352.0
UNITS_H = 100.0


class Art:
    """A small drawing surface that speaks in scene units."""

    def __init__(self, width, height, scale, note=""):
        self.width = width
        self.height = height
        self.scale = scale
        self.note = note
        self.lead = width > 250
        self.image = Image.new("RGB", (width * scale, height * scale), "#000000")
        self.draw = ImageDraw.Draw(self.image)
        self.kx = width * scale / UNITS_W
        self.ky = height * scale / UNITS_H
        self.labels = []

    def pt(self, x, y):
        return (x * self.kx, y * self.ky)

    def bg(self, colour):
        self.draw.rectangle([0, 0, self.image.width, self.image.height], fill=colour)

    def rect(self, x0, y0, x1, y1, colour):
        self.draw.rectangle([x0 * self.kx, y0 * self.ky, x1 * self.kx, y1 * self.ky], fill=colour)

    def poly(self, points, colour):
        self.draw.polygon([self.pt(x, y) for x, y in points], fill=colour)

    def disc(self, cx, cy, radius, colour):
        self.oval(cx, cy, radius, radius, colour)

    def oval(self, cx, cy, rx, ry, colour):
        self.draw.ellipse(
            [(cx - rx) * self.kx, (cy - ry) * self.ky, (cx + rx) * self.kx, (cy + ry) * self.ky], fill=colour
        )

    def ring(self, cx, cy, radius, colour, width=1.0):
        self.draw.ellipse(
            [(cx - radius) * self.kx, (cy - radius) * self.ky, (cx + radius) * self.kx, (cy + radius) * self.ky],
            outline=colour,
            width=max(1, int(round(width * self.ky))),
        )

    def line(self, points, colour, width=1.0):
        self.draw.line(
            [self.pt(x, y) for x, y in points], fill=colour, width=max(1, int(round(width * self.ky))), joint="curve"
        )

    def dash(self, points, colour, width=1.0, on=4.0, off=3.0):
        """Dashed polyline: walk the path and draw every other stretch."""
        travelled = 0.0
        period = on + off
        for (x0, y0), (x1, y1) in zip(points, points[1:]):
            length = math.hypot(x1 - x0, y1 - y0)
            if length == 0:
                continue
            steps = max(1, int(length / 0.5))
            for i in range(steps):
                t0, t1 = i / steps, (i + 1) / steps
                if (travelled + t0 * length) % period < on:
                    self.line(
                        [(x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0), (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)],
                        colour,
                        width,
                    )
            travelled += length

    def label(self, x, y, text, size, colour, font="bold", anchor="ls"):
        """Queue a text label; x and y are scene units, size is final pixels."""
        self.labels.append((x * self.width / UNITS_W, y * self.height / UNITS_H, text, size, colour, font, anchor))

    def finish(self):
        return self.image.resize((self.width, self.height), Image.BOX), self.labels


def ellipse_points(cx, cy, rx, ry, start_deg, end_deg, count=48):
    points = []
    for i in range(count + 1):
        t = math.radians(start_deg + (end_deg - start_deg) * i / count)
        points.append((cx + rx * math.cos(t), cy + ry * math.sin(t)))
    return points


def turned_box(cx, cy, width, height, degrees):
    """Corners of a rectangle turned about its centre."""
    t = math.radians(degrees)
    c, s = math.cos(t), math.sin(t)
    corners = []
    for dx, dy in ((-width / 2, -height / 2), (width / 2, -height / 2), (width / 2, height / 2), (-width / 2, height / 2)):
        corners.append((cx + dx * c - dy * s, cy + dx * s + dy * c))
    return corners


def star_points(cx, cy, outer, inner, spikes, turn=0.0):
    points = []
    for i in range(spikes * 2):
        radius = outer if i % 2 == 0 else inner
        t = math.radians(turn + i * 180.0 / spikes)
        points.append((cx + radius * math.cos(t), cy + radius * math.sin(t)))
    return points


def sprinkle(count, seed):
    """Deterministic scatter in the unit square (no random module, same output every run)."""
    state = seed
    out = []
    for _ in range(count):
        state = (state * 1103515245 + 12345) % 2147483648
        x = state / 2147483648.0
        state = (state * 1103515245 + 12345) % 2147483648
        y = state / 2147483648.0
        out.append((x, y))
    return out


def smoke(a, puffs, colour):
    for cx, cy, radius in puffs:
        a.disc(cx, cy, radius, colour)


def flame(a, cx, base, width, height):
    """A three-tone tongue of fire standing on y = base."""
    a.poly([(cx - width, base), (cx - width * 0.55, base - height * 0.55), (cx - width * 0.2, base - height * 0.3),
            (cx, base - height), (cx + width * 0.3, base - height * 0.4), (cx + width * 0.6, base - height * 0.62),
            (cx + width, base)], "#E4572E")
    a.poly([(cx - width * 0.6, base), (cx - width * 0.25, base - height * 0.4), (cx, base - height * 0.68),
            (cx + width * 0.35, base - height * 0.36), (cx + width * 0.6, base)], "#F6A21B")
    a.poly([(cx - width * 0.28, base), (cx, base - height * 0.36), (cx + width * 0.28, base)], "#FFE08A")


# ---------------------------------------------------------------- lead scenes


def art_cop31(a):
    """Plenary stage: the third draft with the fossil-fuel line struck, a warming globe, and a waiting gavel."""
    a.bg("#0E5560")
    for i in range(1, 8):
        a.rect(i * 44 - 0.6, 0, i * 44 + 0.6, 84, "#126572")
    a.rect(0, 84, 352, 100, "#093E46")
    # the draft decision
    a.rect(21, 13, 115, 93, "#083238")
    a.rect(17, 9, 111, 89, "#FBFAF4")
    a.rect(25, 16, 103, 27, "#141923")
    a.label(64, 21.5, "FINAL DRAFT 3", 9.5, "#FFFFFF", "bold", "mm")
    for y, length in ((33, 74), (39, 60), (45, 70)):
        a.rect(25, y, 25 + length, y + 2.6, "#B9C0C8")
    a.label(25, 60, "fossil fuels", 11.5, "#141923", "bold", "ls")
    a.line([(22, 55.5), (99, 55.5)], "#D92D20", 2.0)
    a.label(25, 71.5, "NOT IN THE TEXT", 9, "#C0271B", "heavy", "ls")
    for y, length in ((77, 66), (83, 44)):
        a.rect(25, y, 25 + length, y + 2.6, "#B9C0C8")
    # the globe
    a.disc(172, 49, 32, "#0A3F47")
    a.disc(172, 48, 30, "#3D94D6")
    a.poly([(156, 30), (167, 25), (177, 28), (180, 36), (172, 40), (174, 50), (167, 62), (159, 54), (154, 44), (149, 38)], "#7DC98B")
    a.poly([(182, 30), (194, 27), (201, 36), (198, 47), (189, 52), (182, 44)], "#7DC98B")
    a.poly([(186, 58), (194, 56), (198, 63), (192, 70), (185, 66)], "#7DC98B")
    a.poly([(146, 52), (152, 56), (150, 66), (145, 60)], "#7DC98B")
    # the thermometer
    a.rect(220, 14, 230, 72, "#FBFAF4")
    a.disc(225, 14, 5, "#FBFAF4")
    a.disc(225, 76, 10, "#FBFAF4")
    a.disc(225, 76, 7.4, "#D92D20")
    a.rect(222.6, 26, 227.4, 74, "#D92D20")
    for y in (22, 32, 42, 52, 62):
        a.rect(230, y - 0.5, 235, y + 0.5, "#FBFAF4")
    a.label(236, 30, "1.5\u00b0C", 14.5, "#FFFFFF", "black", "ls")
    a.label(236, 44, "overshoot", 10, "#FDE68A", "bold", "ls")
    # the gavel, raised
    a.rect(291, 77, 344, 84, "#5B3413")
    a.rect(287, 83, 348, 87, "#7A4A1E")
    a.poly(turned_box(330, 57, 7, 42, 38), "#B7772F")
    a.poly(turned_box(312, 39, 32, 16, 38), "#8A5422")
    a.poly(turned_box(312, 39, 32, 4.5, 38), "#C98B3C")
    a.line(ellipse_points(309, 48, 21, 19, 206, 248, 12), "#FDE68A", 1.2)
    a.line(ellipse_points(309, 48, 26, 24, 210, 244, 12), "#FDE68A", 0.9)
    if a.note:
        a.label(346, 96.5, a.note, 9.5, "#FFFFFF", "bold", "rs")


def art_iran_grid(a):
    """Twilight Tehran skyline: half-lit, half-blacked-out blocks under a faulted power pylon and Milad Tower."""
    a.bg("#101730")
    # subtle twilight horizon glow + Alborz mountain ridge
    a.rect(0, 52, 352, 100, "#172140")
    a.poly([(0, 74), (48, 46), (104, 58), (168, 36), (232, 54), (294, 42), (352, 58), (352, 100), (0, 100)], "#1F2B4E")
    a.poly([(148, 44), (168, 36), (186, 43), (174, 46), (168, 42), (158, 46)], "#475982")
    # Milad Tower silhouette (right of centre)
    a.poly([(222, 86), (227, 34), (233, 34), (238, 86)], "#0B1124")
    a.poly([(219, 34), (241, 34), (237, 24), (223, 24)], "#131C38")
    a.rect(221, 29, 239, 31.5, "#334155")
    a.rect(229.2, 8, 230.8, 24, "#1E293B")
    a.disc(230, 8, 1.8, "#EF4444")
    # high-voltage transmission pylon (left-centre, clear of top-left badge)
    a.line([(76, 90), (92, 22), (98, 22), (114, 90)], "#94A3B8", 2.0)
    a.line([(82, 66), (108, 66)], "#94A3B8", 1.5)
    a.line([(87, 46), (103, 46)], "#94A3B8", 1.5)
    a.line([(80, 76), (106, 56)], "#64748B", 1.1)
    a.line([(110, 76), (84, 56)], "#64748B", 1.1)
    a.line([(86, 56), (102, 38)], "#64748B", 1.0)
    a.line([(104, 56), (88, 38)], "#64748B", 1.0)
    # cross-arms
    a.line([(66, 35), (124, 35)], "#CBD5E1", 2.0)
    a.line([(58, 48), (132, 48)], "#CBD5E1", 2.0)
    for ix, iy in ((66, 37), (124, 37), (58, 50), (132, 50)):
        a.rect(ix - 1.2, iy - 1.5, ix + 1.2, iy + 3.5, "#E2E8F0")
    # live incoming cables on the left, snapped/faulted cable on the right
    a.line([(0, 42), (32, 46), (66, 38)], "#FBBF24", 1.3)
    a.line([(0, 57), (28, 60), (58, 51)], "#FBBF24", 1.3)
    a.line([(124, 38), (152, 43), (178, 39)], "#F59E0B", 1.3)
    a.line([(132, 51), (156, 56), (172, 51)], "#64748B", 1.1)
    a.dash([(186, 40), (218, 47), (248, 46)], "#475569", 1.0, 3.5, 3.5)
    # electrical arc burst at the cut
    a.poly(star_points(180, 39, 12, 4.5, 7, 14), "#F59E0B")
    a.poly(star_points(180, 39, 6.5, 2.5, 7, 36), "#FEF08A")
    # skyline blocks: left half lit, right half blacked out
    lit_blocks = ((4, 70, 26), (34, 62, 24), (62, 74, 24), (92, 66, 28), (124, 60, 28), (156, 72, 24))
    for index, (x, top, width) in enumerate(lit_blocks):
        a.rect(x, top, x + width, 100, "#0A0F1F")
        for row in range(int((96 - top) // 8)):
            for col in range(int((width - 4) // 7)):
                if (row * 3 + col * 5 + index) % 3 != 0:
                    a.rect(x + 3 + col * 7, top + 4 + row * 8, x + 6.5 + col * 7, top + 7.5 + row * 8, "#F5D76E")
    dark_blocks = ((184, 64, 30), (218, 72, 26), (248, 60, 30), (282, 68, 28), (314, 58, 34))
    for index, (x, top, width) in enumerate(dark_blocks):
        a.rect(x, top, x + width, 100, "#080C18")
        for row in range(int((96 - top) // 8)):
            for col in range(int((width - 4) // 7)):
                if (row * 2 + col * 3 + index) % 4 == 0:
                    a.rect(x + 3 + col * 7, top + 4 + row * 8, x + 6.5 + col * 7, top + 7.5 + row * 8, "#1E293B")
    # power-cut status plaque (generous padding, clear of top-right CONFIRMED badge)
    a.rect(246, 22, 346, 56, "#334155")
    a.rect(248, 24, 344, 54, "#0B1124")
    a.rect(248, 24, 253, 54, "#EF4444")
    a.label(299, 34.5, a.note or "2h CUTS", 13.5, "#FDE68A", "black", "mm")
    a.label(299, 47.5, "GRID RATIONING", 8.5, "#E2E8F0", "bold", "mm")


def art_vegas(a):
    """Night race on the Strip: neon skyline, the Sphere, a single-seater at speed and the chequered flag."""
    a.bg("#140E2C")
    for x, y in sprinkle(26, 23):
        a.disc(4 + x * 344, 2 + y * 30, 0.5, "#B9B4E8")
    towers = ((6, 40, 24), (32, 28, 20), (54, 46, 30), (86, 34, 18), (228, 30, 22), (252, 44, 26), (306, 36, 18), (326, 26, 22))
    neon = ("#F472B6", "#22D3EE", "#FBBF24", "#A78BFA")
    for index, (x, top, width) in enumerate(towers):
        a.rect(x, top, x + width, 70, "#2B2056")
        a.rect(x, top, x + width, top + 1.6, neon[index % 4])
        for row in range(int((66 - top) // 7)):
            for column in range(int(width // 6)):
                if (row * 3 + column * 5 + index) % 4 != 0:
                    a.rect(x + 2.2 + column * 6, top + 5 + row * 7, x + 4.6 + column * 6, top + 8 + row * 7, neon[(row + column + index) % 4])
    # billboard
    a.rect(118, 6, 214, 28, "#F472B6")
    a.rect(120, 8, 212, 26, "#231848")
    a.label(166, 17.5, "LAS VEGAS", 12.5, "#FDE68A", "black", "mm")
    a.rect(134, 28, 137, 70, "#3A2D6B")
    a.rect(195, 28, 198, 70, "#3A2D6B")
    # the Sphere
    a.disc(286, 52, 17, "#D9770B")
    a.disc(286, 52, 15, "#F59E0B")
    a.disc(281, 47, 8.5, "#FCD34D")
    # track
    a.rect(0, 68, 352, 100, "#23262F")
    for i in range(22):
        a.rect(i * 16, 66, i * 16 + 8, 69.5, "#E11D48" if i % 2 == 0 else "#F8FAFC")
    for i in range(9):
        a.rect(10 + i * 42, 94, 30 + i * 42, 95.6, "#F8FAFC")
    for y, x0, x1 in ((73, 30, 86), (78, 14, 78), (83, 40, 92)):
        a.rect(x0, y, x1, y + 0.9, "#8B93A7")
    # the car
    a.rect(97, 55, 115, 59, "#E11D48")
    a.rect(97, 55, 101, 76, "#1B2B6B")
    a.poly([(104, 78), (106, 68), (126, 62), (146, 58), (152, 52), (158, 52), (160, 58), (176, 62), (196, 68), (224, 76), (226, 80), (104, 80)], "#1B2B6B")
    a.poly([(126, 66), (176, 66), (196, 71), (126, 71)], "#E11D48")
    a.poly([(196, 71), (224, 76), (226, 80), (206, 80)], "#FBBF24")
    a.disc(163, 57, 4.2, "#FBBF24")
    a.line([(152, 55), (160, 51), (170, 56), (174, 62)], "#0B1020", 1.6)
    a.rect(214, 79, 238, 82.5, "#0B1020")
    for cx in (122, 198):
        a.disc(cx, 78, 10, "#0B0D14")
        a.disc(cx, 78, 4.4, "#8B93A7")
        a.disc(cx, 78, 1.8, "#FBBF24")
    # chequered flag
    a.rect(329, 30, 331.4, 90, "#C7CBD6")
    for row in range(4):
        for column in range(5):
            a.rect(331.4 - (column + 1) * 5.6, 30 + row * 5.6, 331.4 - column * 5.6, 35.6 + row * 5.6,
                   "#F8FAFC" if (row + column) % 2 == 0 else "#0B0D14")


# ----------------------------------------------------------- secondary scenes


def art_igmetall(a):
    """German industrial plant halted by a 24-hour union strike: idle stacks, gearwheel, red picket banners."""
    a.bg("#DCE6F0")
    # overcast band & ground
    a.rect(0, 78, 352, 100, "#7C8794")
    a.rect(0, 76, 352, 79, "#4B5563")
    # twin idle factory chimneys (left-centre)
    a.poly([(46, 52), (50, 14), (58, 14), (62, 52)], "#475569")
    a.poly([(72, 52), (76, 20), (84, 20), (88, 52)], "#475569")
    a.rect(49, 20, 59, 24, "#C81E1E")
    a.rect(75, 26, 85, 30, "#C81E1E")
    # sawtooth industrial plant hall
    a.rect(24, 52, 202, 78, "#334155")
    for i in range(4):
        x = 24 + i * 44
        a.poly([(x, 52), (x, 38), (x + 44, 52)], "#1E293B")
    for x in (36, 70, 104, 138, 172):
        a.rect(x, 60, x + 20, 70, "#94A3B8")
    # steel cogwheel with strike halt bar (right-centre)
    a.disc(142, 48, 16, "#475569")
    for i in range(8):
        a.poly(turned_box(142, 48, 38, 5.5, i * 22.5), "#475569")
    a.disc(142, 48, 7.5, "#DCE6F0")
    a.poly(turned_box(142, 48, 40, 4.5, -35), "#C81E1E")
    # red union picket flags & banners outside closed gate
    for x, top in ((214, 34), (242, 42), (268, 36)):
        a.rect(x, top, x + 2.2, 84, "#1E293B")
        a.poly([(x + 2.2, top), (x + 26, top + 5), (x + 2.2, top + 18)], "#C81E1E")
    # strikers silhouettes
    for sx in (208, 232, 256, 280):
        a.disc(sx, 72, 5.2, "#141923")
        a.poly([(sx - 7, 94), (sx - 5.5, 78), (sx + 5.5, 78), (sx + 7, 94)], "#141923")
    # bold 24h strike placard (wide padding, well below top badges)
    a.rect(294, 42, 346, 74, "#141923")
    a.rect(296, 44, 344, 72, "#C81E1E")
    a.rect(318.8, 74, 321.2, 92, "#141923")
    a.label(320, 58, a.note or "24h", 11, "#FFFFFF", "black", "mm")


def art_kharkiv(a):
    """Pre-dawn city blocks, one on fire, with a delta-wing attack drone overhead."""
    a.bg("#1A2947")
    a.poly([(210, 100), (232, 30), (252, 30), (268, 100)], "#22355C")
    a.poly([(120, 100), (96, 34), (114, 30), (160, 100)], "#22355C")
    blocks = ((8, 54, 46), (60, 40, 40), (104, 60, 34), (144, 46, 52), (202, 58, 40), (248, 42, 44), (298, 56, 48))
    for index, (x, top, width) in enumerate(blocks):
        a.rect(x, top, x + width, 100, "#0E1629")
        for row in range(int((96 - top) // 9)):
            for column in range(int((width - 6) // 9)):
                if (row * 5 + column * 3 + index * 2) % 5 < 2:
                    a.rect(x + 5 + column * 9, top + 6 + row * 9, x + 9 + column * 9, top + 10.5 + row * 9, "#F5D76E")
    # the burning block
    smoke(a, ((172, 30, 13), (190, 22, 15), (212, 16, 14), (234, 13, 12), (160, 40, 9)), "#55607A")
    smoke(a, ((176, 34, 9), (194, 27, 10), (214, 22, 9)), "#6D7890")
    flame(a, 170, 47, 17, 26)
    flame(a, 152, 60, 8, 13)
    # the drone
    a.poly([(286, 30), (318, 20), (312, 31), (322, 41)], "#C9D2E3")
    a.poly([(286, 30), (308, 28.5), (312, 31), (308, 33)], "#8D99B3")
    a.dash([(284, 31), (262, 37), (240, 44)], "#C9D2E3", 1.1, 3.5, 3)


def art_benghazi(a):
    """Harbour quay: a depot blast plume over warehouses, with a moored patrol ship."""
    a.bg("#F3D9A8")
    a.disc(300, 30, 13, "#FBEFC9")
    a.rect(0, 72, 352, 100, "#2F6F8F")
    for y, x0, x1 in ((80, 20, 70), (86, 190, 250), (92, 60, 130), (84, 290, 340)):
        a.rect(x0, y, x1, y + 1.2, "#5E9AB5")
    a.rect(0, 62, 236, 74, "#8B7E66")
    a.rect(0, 62, 236, 64.5, "#A2957C")
    for x, top, width in ((12, 46, 40), (60, 50, 34), (172, 48, 44)):
        a.rect(x, top, x + width, 62, "#6B5E4B")
        a.poly([(x - 2, top), (x + width / 2, top - 8), (x + width + 2, top)], "#4F4537")
        a.rect(x + width / 2 - 5, 54, x + width / 2 + 5, 62, "#3F372C")
    # the plume
    smoke(a, ((132, 40, 20), (112, 28, 16), (150, 24, 18), (128, 12, 15), (166, 10, 13), (190, 6, 11)), "#3F3F46")
    smoke(a, ((124, 32, 11), (146, 20, 12), (168, 12, 8)), "#5B5B63")
    a.poly(star_points(132, 50, 26, 11, 9, 8), "#E4572E")
    a.poly(star_points(132, 51, 17, 7.5, 9, 28), "#F6A21B")
    a.poly(star_points(132, 52, 9, 4, 9, 8), "#FFE08A")
    for x0, y0, x1, y1 in ((100, 36, 92, 28), (164, 40, 174, 33), (96, 52, 86, 50)):
        a.line([(x0, y0), (x1, y1)], "#E4572E", 1.4)
    # patrol ship
    a.poly([(246, 70), (340, 70), (332, 82), (254, 82)], "#374151")
    a.rect(270, 58, 312, 70, "#4B5563")
    a.rect(282, 50, 300, 58, "#6B7280")
    a.rect(290, 34, 292, 50, "#374151")
    a.rect(284, 40, 298, 41.5, "#374151")
    a.rect(254, 66, 264, 70, "#4B5563")
    a.line([(258, 66), (268, 61)], "#374151", 1.6)


def art_hongkong(a):
    """A ballot dropping into a box in front of the harbour skyline, with the midday turnout gauge."""
    a.bg("#E3ECF5")
    a.rect(0, 80, 352, 100, "#9CC4DE")
    a.poly([(150, 80), (190, 58), (240, 50), (300, 60), (352, 54), (352, 80)], "#B7C6D6")
    towers = ((176, 46, 14), (194, 30, 12), (210, 52, 16), (230, 22, 13), (247, 44, 18), (269, 34, 12), (285, 50, 20), (309, 40, 14), (327, 56, 18))
    for index, (x, top, width) in enumerate(towers):
        a.rect(x, top, x + width, 80, "#5E738E" if index % 2 == 0 else "#7388A3")
    a.poly([(230, 22), (236.5, 8), (243, 22)], "#7388A3")
    a.poly([(194, 30), (206, 30), (206, 20)], "#5E738E")
    a.rect(236, 2, 237, 9, "#5E738E")
    # ballot box
    a.rect(30, 44, 106, 92, "#B4232C")
    a.rect(26, 40, 110, 48, "#8E1B22")
    a.rect(50, 42.5, 86, 45.5, "#3A0D10")
    a.poly(turned_box(68, 28, 26, 32, -10), "#FFFFFF")
    a.line([(60, 26), (65, 32), (76, 18)], "#1B7F4B", 2.4)
    a.disc(68, 70, 11, "#FFFFFF")
    a.poly(star_points(68, 70, 8.5, 3.6, 5, -90), "#B4232C")
    # turnout gauge
    a.label(122, 46, "83%", 15, "#141923", "black", "ls")
    a.rect(122, 52, 166, 59, "#FFFFFF")
    a.rect(122, 52, 158.5, 59, "#1B7F4B")


def art_peptides(a):
    """Australia parliamentary inquiry into unapproved peptides: glass vial, warning alert, Canberra Parliament mast."""
    a.bg("#E5EEF4")
    # lawn & horizon
    a.poly([(0, 100), (0, 74), (160, 70), (252, 60), (352, 74), (352, 100)], "#77A88D")
    # Canberra Parliament House silhouette (right)
    a.rect(226, 64, 342, 82, "#F8FAFC")
    for x in range(234, 336, 14):
        a.rect(x, 68, x + 7, 79, "#94A3B8")
    a.poly([(242, 64), (284, 24), (326, 64), (320, 64), (284, 31), (248, 64)], "#64748B")
    a.rect(282.5, 10, 285.5, 64, "#475569")
    # small flag
    a.rect(285.5, 11, 304, 22, "#1E3A8A")
    a.rect(285.5, 15.5, 296, 17.5, "#DC2626")
    a.rect(289.5, 11, 291.5, 22, "#DC2626")
    # medical peptide vial (left)
    a.rect(24, 42, 66, 88, "#FFFFFF")
    a.rect(26, 62, 64, 86, "#38BDF8")
    a.rect(30, 36, 60, 42, "#CBD5E1")
    a.rect(28, 28, 62, 36, "#0E7C86")
    a.rect(24, 42, 66, 44, "#94A3B8")
    a.rect(31, 53, 59, 68, "#F8FAFC")
    a.rect(35, 57, 55, 60, "#0E7C86")
    a.rect(35, 63, 50, 65.5, "#64748B")
    # warning alert triangle next to vial
    a.poly([(78, 82), (124, 82), (101, 38)], "#F59E0B")
    a.poly([(84, 79), (118, 79), (101, 45)], "#FEF08A")
    a.rect(99, 54, 103, 68, "#141923")
    a.rect(99, 71, 103, 75, "#141923")
    # crisp inquiry pill (generous dark box around text, clear of top badges)
    a.rect(134, 44, 222, 68, "#141923")
    a.label(178, 56, "INQUIRY", 9.5, "#FFFFFF", "black", "mm")


def art_banten(a):
    """Saw-tooth factory on fire under a long smoke column, with a fire engine playing water on it."""
    a.bg("#F1E2D0")
    smoke(a, ((92, 34, 18), (120, 22, 20), (154, 14, 19), (190, 10, 17), (224, 8, 15), (256, 8, 13), (288, 10, 11)), "#4B4B55")
    smoke(a, ((100, 38, 11), (128, 28, 13), (160, 20, 12), (196, 16, 10)), "#6A6A75")
    a.rect(0, 84, 352, 100, "#B9A88F")
    a.rect(24, 54, 214, 84, "#7C8794")
    for i in range(5):
        x = 24 + i * 38
        a.poly([(x, 54), (x, 40), (x + 38, 54)], "#5E6875")
        a.poly([(x, 54), (x, 40), (x + 6, 42.2), (x + 6, 54)], "#D5DBE2")
    a.rect(186, 26, 198, 54, "#5E6875")
    for x in (40, 78, 116, 154):
        a.rect(x, 64, x + 20, 76, "#2A2F38")
    flame(a, 70, 54, 20, 26)
    flame(a, 112, 54, 15, 20)
    flame(a, 50, 76, 9, 11)
    flame(a, 126, 76, 9, 11)
    # fire engine and water arc
    a.rect(262, 62, 330, 82, "#C81E1E")
    a.rect(312, 54, 336, 82, "#C81E1E")
    a.rect(318, 58, 332, 68, "#CFE8FF")
    a.rect(262, 74, 336, 76.5, "#FFFFFF")
    a.disc(280, 84, 6.5, "#141923")
    a.disc(318, 84, 6.5, "#141923")
    a.disc(280, 84, 2.6, "#9AA3B2")
    a.disc(318, 84, 2.6, "#9AA3B2")
    a.line(ellipse_points(204, 62, 62, 28, 0, -112, 26), "#3B9BE8", 2.2)


def art_coalition(a):
    """City skyline behind four party-coloured puzzle pieces, the last one still to be pressed home."""
    a.bg("#E9F0E3")
    a.rect(0, 82, 352, 100, "#C9D4BE")
    for x, top, width in ((14, 50, 22), (40, 38, 16), (60, 56, 26), (240, 44, 20), (264, 58, 28), (296, 34, 18), (318, 52, 24)):
        a.rect(x, top, x + width, 82, "#A9B5AD")
    a.rect(302.5, 8, 307.5, 34, "#A9B5AD")
    a.disc(305, 16, 6.5, "#A9B5AD")
    a.oval(47.5, 38, 8, 3.5, "#93A097")
    colours = ("#007A4D", "#FFB612", "#DE3831", "#1F2937")
    lefts = (62, 112, 162, 226)
    for left, colour in zip(lefts, colours):
        a.rect(left, 30, left + 50, 80, colour)
    for left, colour in zip(lefts[:3], colours[:3]):
        a.disc(left + 55, 55, 9, colour)
    a.disc(226, 55, 9, "#E9F0E3")
    a.rect(216, 80, 226, 82, "#E9F0E3")
    # arrows closing the last gap
    a.line([(292, 55), (282, 55)], "#141923", 2.2)
    a.poly([(279, 55), (286, 50), (286, 60)], "#141923")
    # mayoral chain
    a.line(ellipse_points(137, 30, 40, 13, 200, 340, 24), "#C9A227", 2.0)
    a.disc(137, 18.5, 5.5, "#C9A227")
    a.disc(137, 18.5, 2.6, "#FDE68A")


def art_knesset(a):
    """The flat-roofed parliament on its hill, and two delegations facing each other across a table."""
    a.bg("#EDF1F6")
    a.poly([(0, 62), (90, 50), (200, 46), (300, 52), (352, 60), (352, 100), (0, 100)], "#C7D3C0")
    a.rect(96, 22, 256, 30, "#B9A888")
    a.rect(104, 30, 248, 50, "#E4D9BF")
    for i in range(12):
        a.rect(108 + i * 12, 30, 112 + i * 12, 50, "#B9A888")
    a.rect(92, 50, 260, 54, "#A3936F")
    # flag
    a.rect(280, 10, 281.6, 52, "#6B7280")
    a.rect(281.6, 11, 312, 31, "#FFFFFF")
    a.rect(281.6, 13.5, 312, 16.5, "#1F5FBF")
    a.rect(281.6, 25.5, 312, 28.5, "#1F5FBF")
    a.poly(star_points(296.8, 21, 3.6, 3.6, 3, -90)[::2], "#1F5FBF")
    a.poly(star_points(296.8, 21, 3.6, 3.6, 3, 90)[::2], "#1F5FBF")
    # table and delegations
    a.oval(176, 82, 74, 12, "#7A4A1E")
    a.oval(176, 80, 74, 12, "#A9713A")
    for x in (126, 150, 202, 226):
        a.poly(turned_box(x, 79, 14, 6, 0), "#FFFFFF")
    for index, x in enumerate((112, 138, 164)):
        a.disc(x, 62, 6.2, "#0E7C86")
        a.poly([(x - 8, 78), (x - 6, 69), (x + 6, 69), (x + 8, 78)], "#0E7C86")
    for index, x in enumerate((188, 214, 240)):
        a.disc(x, 62, 6.2, "#B4551A")
        a.poly([(x - 8, 78), (x - 6, 69), (x + 6, 69), (x + 8, 78)], "#B4551A")
    # speech marks
    a.poly([(40, 60), (84, 60), (84, 80), (72, 80), (78, 88), (62, 80), (40, 80)], "#0E7C86")
    a.poly([(268, 62), (312, 62), (312, 82), (290, 82), (274, 90), (280, 82), (268, 82)], "#B4551A")
    for y in (66, 71.5):
        a.rect(46, y, 78, y + 2.2, "#FFFFFF")
        a.rect(274, y + 2, 306, y + 4.2, "#FFFFFF")


def art_storm(a):
    """A supercell with lightning over small houses, roofing sheets lifting in the wind."""
    a.bg("#5A6880")
    smoke(a, ((40, 12, 24), (86, 6, 26), (140, 10, 28), (196, 4, 26), (250, 10, 28), (306, 6, 24), (340, 14, 20)), "#333D50")
    smoke(a, ((70, 22, 16), (128, 26, 18), (190, 22, 17), (248, 27, 16), (300, 22, 15)), "#414C62")
    a.poly([(96, 36), (120, 36), (240, 36), (212, 52), (132, 52)], "#333D50")
    for x0 in range(-10, 352, 15):
        a.line([(x0 + 14, 40), (x0, 84)], "#8FA6C4", 0.7)
    a.poly([(166, 30), (182, 30), (172, 50), (184, 50), (158, 82), (168, 56), (156, 56)], "#FDE047")
    a.poly([(268, 28), (280, 28), (273, 44), (282, 44), (262, 70), (269, 49), (260, 49)], "#FDE047")
    a.rect(0, 84, 352, 100, "#3E5A3A")
    for index, (x, width) in enumerate(((22, 46), (90, 40), (212, 44), (284, 46))):
        a.rect(x, 66, x + width, 86, "#D9C3A3")
        a.rect(x + width / 2 - 4, 74, x + width / 2 + 4, 86, "#6B4A2B")
        if index == 1:
            a.poly([(x - 4, 66), (x + 12, 54), (x + 20, 60), (x + 12, 66)], "#9A4A12")
        else:
            a.poly([(x - 4, 66), (x + width / 2, 52), (x + width + 4, 66)], "#9A4A12")
    for cx, cy, turn in ((142, 48, -24), (126, 40, 18), (150, 60, -40)):
        a.poly(turned_box(cx, cy, 13, 4, turn), "#9A4A12")
    # warning sign
    a.poly([(316, 46), (336, 46), (326, 28)], "#F97316")
    a.rect(325, 33.5, 327, 40, "#141923")
    a.rect(325, 41.5, 327, 43.5, "#141923")


def art_cricket(a):
    """Stumps, bat and ball on a mown outfield, with the day's innings total on the board."""
    a.bg("#2F8F4E")
    for i in range(0, 8, 2):
        a.rect(i * 44, 0, i * 44 + 44, 100, "#37A05A")
    a.rect(0, 0, 352, 16, "#BFE3F2")
    a.rect(0, 14, 352, 18, "#256F3D")
    a.poly([(120, 100), (150, 34), (202, 34), (232, 100)], "#D9C59A")
    a.rect(140, 56, 212, 57.6, "#FFFFFF")
    for x in (164, 176, 188):
        a.rect(x - 1.8, 40, x + 1.8, 84, "#F0C36A")
    a.rect(161, 38, 191, 41, "#8A5422")
    # bat and ball
    a.poly(turned_box(84, 60, 13, 52, 24), "#E3C58F")
    a.poly(turned_box(98.5, 27.5, 5, 22, 24), "#334155")
    a.disc(118, 84, 8, "#A01818")
    a.line(ellipse_points(118, 84, 8, 3, 200, 340, 10), "#FFFFFF", 0.9)
    # scoreboard
    a.rect(246, 22, 342, 60, "#141923")
    a.rect(250, 26, 338, 56, "#1F2937")
    a.rect(290, 60, 298, 84, "#141923")
    a.label(294, 41.5, a.note or "", 12, "#FDE68A", "black", "mm")


SCENES = {
    "cop31": art_cop31,
    "iran_grid": art_iran_grid,
    "vegas": art_vegas,
    "igmetall": art_igmetall,
    "kharkiv": art_kharkiv,
    "benghazi": art_benghazi,
    "hongkong": art_hongkong,
    "peptides": art_peptides,
    "banten": art_banten,
    "coalition": art_coalition,
    "knesset": art_knesset,
    "storm": art_storm,
    "cricket": art_cricket,
}


def render_scene(name, width, height, scale=4, note=""):
    """Return (image, labels) for one card illustration at final pixel size."""
    surface = Art(width, height, scale, note)
    SCENES[name](surface)
    return surface.finish()


# ----------------------------------------------------------------------- atlas

LAT_SOUTH = -57.0
LAT_NORTH = 84.0


def natural_earth(lon_deg, lat_deg):
    """Natural Earth projection (Savric, Patterson, Jenny, 2011): a compromise pseudocylindrical world map."""
    lam = math.radians(lon_deg)
    phi = math.radians(lat_deg)
    p2 = phi * phi
    p4 = p2 * p2
    x = lam * (0.8707 - 0.131979 * p2 + p4 * (-0.013791 + p4 * (0.003971 * p2 - 0.001529 * p4)))
    y = phi * (1.007226 + p2 * (0.015085 + p4 * (-0.044475 + 0.028874 * p2 - 0.005916 * p4)))
    return x, y


class Atlas:
    """World map panel: land from Natural Earth 1:110m, drawn in the Natural Earth projection."""

    def __init__(self, width, height, scale=4, sea="#D5E3EC", land="#B9B19E", paper="#F4F1EA", grid="#C3D4DF"):
        self.width, self.height, self.scale = width, height, scale
        x_edge, _ = natural_earth(180.0, 0.0)
        _, y_top = natural_earth(0.0, LAT_NORTH)
        _, y_bottom = natural_earth(0.0, LAT_SOUTH)
        self.k = min(width / (2 * x_edge), height / (y_top - y_bottom))
        self.x_mid = width / 2.0
        self.y_mid = height / 2.0 + self.k * (y_top + y_bottom) / 2.0
        self.image = Image.new("RGB", (width * scale, height * scale), paper)
        self.draw = ImageDraw.Draw(self.image)
        # sea, bounded by the curved edge of the projection
        outline = [self.big(180.0, lat) for lat in self.steps(LAT_SOUTH, LAT_NORTH, 3.0)]
        outline += [self.big(-180.0, lat) for lat in self.steps(LAT_NORTH, LAT_SOUTH, -3.0)]
        self.draw.polygon(outline, fill=sea)
        for lon in range(-150, 180, 30):
            self.draw.line([self.big(lon, lat) for lat in self.steps(LAT_SOUTH, LAT_NORTH, 3.0)], fill=grid, width=max(1, scale // 2))
        for lat in (-30, 0, 30, 60):
            self.draw.line([self.big(lon, lat) for lon in range(-180, 181, 6)], fill=grid, width=max(1, scale // 2))
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "atlas_land.json")
        with open(path, encoding="utf-8") as handle:
            rings = json.load(handle)
        for ring in rings:
            points = []
            for i in range(0, len(ring), 2):
                lon, lat = ring[i] / 10.0, ring[i + 1] / 10.0
                points.append(self.big(lon, max(LAT_SOUTH, min(LAT_NORTH, lat))))
            if len(points) >= 3:
                self.draw.polygon(points, fill=land)

    @staticmethod
    def steps(start, stop, step):
        values = []
        value = start
        while (step > 0 and value < stop) or (step < 0 and value > stop):
            values.append(value)
            value += step
        values.append(stop)
        return values

    def spot(self, lon, lat):
        """Final-pixel position of a place."""
        x, y = natural_earth(lon, lat)
        return self.x_mid + self.k * x, self.y_mid - self.k * y

    def big(self, lon, lat):
        x, y = self.spot(lon, lat)
        return x * self.scale, y * self.scale

    def pin(self, lon, lat, dx, dy, colour, radius=7.0):
        """Mark the true place with a dot, and hang a numbered bubble off it; returns the bubble centre."""
        s = self.scale
        x, y = self.spot(lon, lat)
        bx, by = x + dx, y + dy
        self.draw.line([x * s, y * s, bx * s, by * s], fill="#141923", width=max(1, int(round(1.1 * s))))
        self.draw.ellipse([(x - 2.3) * s, (y - 2.3) * s, (x + 2.3) * s, (y + 2.3) * s], fill="#141923")
        self.draw.ellipse([(bx - radius - 1) * s, (by - radius - 1) * s, (bx + radius + 1) * s, (by + radius + 1) * s], fill="#FFFFFF")
        self.draw.ellipse([(bx - radius) * s, (by - radius) * s, (bx + radius) * s, (by + radius) * s], fill=colour)
        return bx, by

    def finish(self):
        return self.image.resize((self.width, self.height), Image.BOX)
