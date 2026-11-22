"""Bespoke vector illustrations for the World Ledger Sunday 22 November 2026 visual poster.

Every scene is drawn with Pillow vector primitives on a 4x supersampled canvas and box-filtered down so edges
stay razor sharp without photos or external assets. Circles and stars use pixel-uniform radii so globes, wheels,
spheres and blasts remain strictly round at both hero (490x200) and grid-card (239x126) aspect ratios.
"""

import math

from PIL import Image, ImageDraw

UNITS_W = 352.0
UNITS_H = 100.0


class Art:
    """Drawing surface in 352 x 100 scene units with pixel-round radial primitives."""

    def __init__(self, width, height, scale=4, note=""):
        self.width = width
        self.height = height
        self.scale = scale
        self.note = note
        self.hero = width > 300
        self.image = Image.new("RGB", (width * scale, height * scale), "#000000")
        self.draw = ImageDraw.Draw(self.image)
        self.kx = width * scale / UNITS_W
        self.ky = height * scale / UNITS_H
        self.kr = min(self.kx * 1.15, self.ky)
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
        """Strictly round circle in output pixels."""
        px, py = cx * self.kx, cy * self.ky
        r = radius * self.kr
        self.draw.ellipse([px - r, py - r, px + r, py + r], fill=colour)

    def oval(self, cx, cy, rx, ry, colour):
        self.draw.ellipse(
            [(cx - rx) * self.kx, (cy - ry) * self.ky, (cx + rx) * self.kx, (cy + ry) * self.ky], fill=colour
        )

    def ring(self, cx, cy, radius, colour, width=1.0):
        px, py = cx * self.kx, cy * self.ky
        r = radius * self.kr
        self.draw.ellipse(
            [px - r, py - r, px + r, py + r],
            outline=colour,
            width=max(1, int(round(width * self.kr))),
        )

    def star(self, cx, cy, outer, inner, spikes, turn, colour):
        """Strictly isotropic star polygon in output pixels."""
        px, py = cx * self.kx, cy * self.ky
        pts = []
        for i in range(spikes * 2):
            r = (outer if i % 2 == 0 else inner) * self.kr
            t = math.radians(turn + i * 180.0 / spikes)
            pts.append((px + r * math.cos(t), py + r * math.sin(t)))
        self.draw.polygon(pts, fill=colour)

    def rotbox(self, cx, cy, width, height, degrees, colour):
        """Rectangle rotated in isotropic output-pixel space so angles stay crisp."""
        px, py = cx * self.kx, cy * self.ky
        t = math.radians(degrees)
        c, s = math.cos(t), math.sin(t)
        hw, hh = width * self.kr / 2.0, height * self.kr / 2.0
        pts = []
        for dx, dy in ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)):
            pts.append((px + dx * c - dy * s, py + dx * s + dy * c))
        self.draw.polygon(pts, fill=colour)

    def line(self, points, colour, width=1.0):
        self.draw.line(
            [self.pt(x, y) for x, y in points], fill=colour, width=max(1, int(round(width * self.kr))), joint="curve"
        )

    def dash(self, points, colour, width=1.0, on=4.0, off=3.0):
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
        self.labels.append((x * self.width / UNITS_W, y * self.height / UNITS_H, text, size, colour, font, anchor))

    def finish(self):
        return self.image.resize((self.width, self.height), Image.BOX), self.labels


def ellipse_points(cx, cy, rx, ry, start_deg, end_deg, count=48):
    points = []
    for i in range(count + 1):
        t = math.radians(start_deg + (end_deg - start_deg) * i / count)
        points.append((cx + rx * math.cos(t), cy + ry * math.sin(t)))
    return points


def sprinkle(count, seed):
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
    a.poly([(cx - width, base), (cx - width * 0.55, base - height * 0.55), (cx - width * 0.2, base - height * 0.3),
            (cx, base - height), (cx + width * 0.3, base - height * 0.4), (cx + width * 0.6, base - height * 0.62),
            (cx + width, base)], "#E4572E")
    a.poly([(cx - width * 0.6, base), (cx - width * 0.25, base - height * 0.4), (cx, base - height * 0.68),
            (cx + width * 0.35, base - height * 0.36), (cx + width * 0.6, base)], "#F6A21B")
    a.poly([(cx - width * 0.28, base), (cx, base - height * 0.36), (cx + width * 0.28, base)], "#FFE08A")


# ---------------------------------------------------------------- hero scenes


def art_cop31(a):
    """COP31 Antalya plenary: clean uncrossed draft omitting fossil fuels, Earth globe, 1.5C thermometer & gavel."""
    a.bg("#0E5560")
    for i in range(1, 8):
        a.rect(i * 44 - 0.6, 0, i * 44 + 0.6, 84, "#126572")
    a.rect(0, 84, 352, 100, "#093E46")
    # Draft decision paper (zero strikethrough lines so OCR & 300px readers read effortlessly)
    a.rect(17, 19, 127, 94, "#072F35")
    a.rect(13, 16, 123, 91, "#FBFAF4")
    a.rect(19, 23, 117, 34, "#141923")
    a.label(68, 28.5, "FINAL DRAFT 3", 12, "#FFFFFF", "black", "mm")
    for y, length in ((40, 86), (45.5, 64)):
        a.rect(22, y, 22 + length, y + 2.2, "#C4CBD3")
    a.label(68, 59, "FOSSIL FUELS", 15, "#141923", "black", "mm")
    a.rect(22, 68, 114, 82, "#C0271B")
    a.label(68, 75, "OMITTED", 14, "#FFFFFF", "black", "mm")
    a.rect(22, 85.5, 84, 87.5, "#C4CBD3")
    # Round Earth globe
    a.disc(178, 50, 31, "#093B43")
    a.disc(178, 49, 29, "#3D94D6")
    a.poly([(164, 34), (174, 30), (183, 33), (185, 40), (178, 44), (180, 52), (173, 62), (166, 55), (161, 47), (157, 42)], "#7DC98B")
    a.poly([(187, 35), (197, 32), (203, 40), (200, 49), (192, 53), (187, 46)], "#7DC98B")
    a.poly([(189, 58), (196, 56), (199, 62), (194, 68), (188, 65)], "#7DC98B")
    a.poly([(155, 52), (160, 56), (158, 64), (154, 59)], "#7DC98B")
    # Thermometer
    a.rect(224, 16, 234, 72, "#FBFAF4")
    a.disc(229, 16, 4.8, "#FBFAF4")
    a.disc(229, 75, 9.5, "#FBFAF4")
    a.disc(229, 75, 7.0, "#D92D20")
    a.rect(226.6, 28, 231.4, 73, "#D92D20")
    for y in (24, 34, 44, 54, 64):
        a.rect(234, y - 0.5, 239, y + 0.5, "#FBFAF4")
    a.label(240, 31, "1.5\u00b0C", 21, "#FFFFFF", "black", "ls")
    a.label(240, 43, "overshoot", 13.5, "#FDE68A", "bold", "ls")
    # Raised gavel
    a.rect(294, 76, 346, 83, "#5B3413")
    a.rect(290, 82, 349, 86, "#7A4A1E")
    a.rotbox(332, 56, 7.5, 42, 38, "#B7772F")
    a.rotbox(316, 39, 32, 16, 38, "#8A5422")
    a.rotbox(316, 39, 32, 4.5, 38, "#C98B3C")
    a.line(ellipse_points(315, 48, 19, 17, 208, 248, 12), "#FDE68A", 1.3)
    a.line(ellipse_points(315, 48, 24, 22, 212, 244, 12), "#FDE68A", 1.0)
    if a.note:
        a.label(346, 95, a.note, 13, "#FFFFFF", "black", "rs")


def art_iran_grid(a):
    """Twilight Tehran skyline: half-lit, half-blacked-out blocks under a faulted power pylon and Milad Tower."""
    a.bg("#101730")
    a.rect(0, 50, 352, 100, "#172140")
    a.poly([(0, 72), (48, 44), (104, 56), (168, 34), (232, 52), (294, 40), (352, 56), (352, 100), (0, 100)], "#1F2B4E")
    a.poly([(148, 42), (168, 34), (186, 41), (174, 44), (168, 40), (158, 44)], "#475982")
    # Milad Tower silhouette
    a.poly([(215, 86), (220, 34), (226, 34), (231, 86)], "#0B1124")
    a.poly([(212, 34), (234, 34), (230, 24), (216, 24)], "#131C38")
    a.rect(214, 29, 232, 31.5, "#334155")
    a.rect(222.2, 8, 223.8, 24, "#1E293B")
    a.disc(223, 8, 2.0, "#EF4444")
    # High-voltage steel lattice pylon
    a.line([(72, 90), (88, 24), (94, 24), (110, 90)], "#94A3B8", 2.1)
    a.line([(78, 66), (104, 66)], "#94A3B8", 1.6)
    a.line([(83, 47), (99, 47)], "#94A3B8", 1.6)
    a.line([(76, 76), (102, 57)], "#64748B", 1.2)
    a.line([(106, 76), (80, 57)], "#64748B", 1.2)
    a.line([(82, 57), (98, 39)], "#64748B", 1.1)
    a.line([(100, 57), (84, 39)], "#64748B", 1.1)
    a.line([(62, 36), (120, 36)], "#CBD5E1", 2.2)
    a.line([(54, 49), (128, 49)], "#CBD5E1", 2.2)
    for ix, iy in ((62, 38), (120, 38), (54, 51), (128, 51)):
        a.rect(ix - 1.2, iy - 1.5, ix + 1.2, iy + 3.5, "#E2E8F0")
    # Live cables left, faulted snapped cable right
    a.line([(0, 43), (30, 47), (62, 39)], "#FBBF24", 1.5)
    a.line([(0, 58), (26, 61), (54, 52)], "#FBBF24", 1.5)
    a.line([(120, 39), (148, 44), (174, 40)], "#F59E0B", 1.5)
    a.line([(128, 52), (152, 57), (168, 52)], "#64748B", 1.2)
    a.dash([(182, 41), (212, 48), (240, 46)], "#475569", 1.1, 3.5, 3.5)
    a.star(176, 40, 14, 5.2, 7, 14, "#F59E0B")
    a.star(176, 40, 7.5, 2.8, 7, 36, "#FEF08A")
    # Half-lit, half-blacked-out city blocks
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
    # Prominent power-cut status plaque
    a.rect(236, 16, 346, 54, "#334155")
    a.rect(238, 18, 344, 52, "#0B1124")
    a.rect(238, 18, 244, 52, "#EF4444")
    a.label(294, 30, a.note or "2h CUTS", 20, "#FDE68A", "black", "mm")
    a.label(294, 44, "GRID RATIONING", 12, "#E2E8F0", "bold", "mm")


# ---------------------------------------------------------------- grid scenes


def art_vegas(a):
    """Las Vegas GP night race: neon Strip skyline, glowing Sphere, F1 car at speed and chequered flag."""
    a.bg("#140E2C")
    for x, y in sprinkle(24, 23):
        a.disc(4 + x * 344, 2 + y * 30, 0.8, "#B9B4E8")
    towers = ((6, 42, 24), (32, 30, 20), (54, 46, 30), (86, 36, 18), (228, 32, 22), (252, 44, 26), (306, 36, 18), (326, 26, 22))
    neon = ("#F472B6", "#22D3EE", "#FBBF24", "#A78BFA")
    for index, (x, top, width) in enumerate(towers):
        a.rect(x, top, x + width, 70, "#2B2056")
        a.rect(x, top, x + width, top + 1.6, neon[index % 4])
        for row in range(int((66 - top) // 7)):
            for column in range(int(width // 6)):
                if (row * 3 + column * 5 + index) % 4 != 0:
                    a.rect(x + 2.2 + column * 6, top + 5 + row * 7, x + 4.6 + column * 6, top + 8 + row * 7, neon[(row + column + index) % 4])
    # Billboard shifted right of top-left pill
    a.rect(162, 6, 286, 26, "#F472B6")
    a.rect(164, 8, 284, 24, "#231848")
    a.label(224, 16, "LAS VEGAS", 13.5, "#FDE68A", "black", "mm")
    a.rect(182, 26, 185, 70, "#3A2D6B")
    a.rect(262, 26, 265, 70, "#3A2D6B")
    # Glowing Sphere
    a.disc(286, 52, 18, "#D9770B")
    a.disc(286, 52, 15.5, "#F59E0B")
    a.disc(281, 48, 8.5, "#FCD34D")
    # Track
    a.rect(0, 68, 352, 100, "#23262F")
    for i in range(22):
        a.rect(i * 16, 66, i * 16 + 8, 69.5, "#E11D48" if i % 2 == 0 else "#F8FAFC")
    for i in range(9):
        a.rect(10 + i * 42, 94, 30 + i * 42, 95.6, "#F8FAFC")
    for y, x0, x1 in ((73, 26, 84), (78, 12, 74), (83, 36, 88)):
        a.rect(x0, y, x1, y + 1.0, "#8B93A7")
    # F1 Car
    a.rect(94, 55, 114, 59, "#E11D48")
    a.rect(94, 55, 98, 76, "#1B2B6B")
    a.poly([(102, 78), (104, 68), (126, 62), (146, 58), (152, 52), (158, 52), (160, 58), (176, 62), (196, 68), (224, 76), (226, 80), (102, 80)], "#1B2B6B")
    a.poly([(126, 66), (176, 66), (196, 71), (126, 71)], "#E11D48")
    a.poly([(196, 71), (224, 76), (226, 80), (206, 80)], "#FBBF24")
    a.disc(163, 57, 4.8, "#FBBF24")
    a.line([(152, 55), (160, 51), (170, 56), (174, 62)], "#0B1020", 1.8)
    a.rect(214, 79, 238, 82.5, "#0B1020")
    for cx in (122, 198):
        a.disc(cx, 78, 11, "#0B0D14")
        a.disc(cx, 78, 5.0, "#8B93A7")
        a.disc(cx, 78, 2.0, "#FBBF24")
    # Chequered flag
    a.rect(329, 30, 331.4, 90, "#C7CBD6")
    for row in range(4):
        for column in range(5):
            a.rect(331.4 - (column + 1) * 5.8, 30 + row * 5.6, 331.4 - column * 5.8, 35.6 + row * 5.6,
                   "#F8FAFC" if (row + column) % 2 == 0 else "#0B0D14")


def art_igmetall(a):
    """German industrial plant halted by 24-hour union strikes: idle chimneys, gearwheel, crimson picket banners."""
    a.bg("#DCE6F0")
    a.rect(0, 78, 352, 100, "#7C8794")
    a.rect(0, 76, 352, 79, "#4B5563")
    a.poly([(40, 52), (44, 20), (52, 20), (56, 52)], "#475569")
    a.poly([(66, 52), (70, 24), (78, 24), (82, 52)], "#475569")
    a.rect(43, 25, 53, 29, "#C81E1E")
    a.rect(69, 29, 79, 33, "#C81E1E")
    a.rect(20, 52, 198, 78, "#334155")
    for i in range(4):
        x = 20 + i * 44
        a.poly([(x, 52), (x, 38), (x + 44, 52)], "#1E293B")
    for x in (32, 66, 100, 134, 168):
        a.rect(x, 60, x + 20, 70, "#94A3B8")
    # Isotropic cogwheel with halt bar
    a.disc(142, 48, 17, "#475569")
    for i in range(8):
        a.rotbox(142, 48, 40, 6.0, i * 22.5, "#475569")
    a.disc(142, 48, 8.0, "#DCE6F0")
    a.rotbox(142, 48, 42, 5.0, -35, "#C81E1E")
    # Picket flags & strikers
    for x, top in ((210, 32), (238, 40), (264, 34)):
        a.rect(x, top, x + 2.4, 84, "#1E293B")
        a.poly([(x + 2.4, top), (x + 28, top + 5), (x + 2.4, top + 18)], "#C81E1E")
    for sx in (206, 230, 254, 278):
        a.disc(sx, 72, 5.6, "#141923")
        a.poly([(sx - 7, 94), (sx - 5.5, 78), (sx + 5.5, 78), (sx + 7, 94)], "#141923")
    # Bold 24h strike placard
    a.rect(290, 38, 346, 72, "#141923")
    a.rect(292, 40, 344, 70, "#C81E1E")
    a.rect(316.8, 72, 319.2, 92, "#141923")
    a.label(318, 55, a.note or "24h", 14.5, "#FFFFFF", "black", "mm")


def art_hongkong(a):
    """Hong Kong Election Committee: ballot box, Victoria Harbour skyline, and 98.8% final turnout gauge."""
    a.bg("#E3ECF5")
    a.rect(0, 80, 352, 100, "#9CC4DE")
    a.poly([(150, 80), (190, 58), (240, 50), (300, 60), (352, 54), (352, 80)], "#B7C6D6")
    towers = ((188, 46, 14), (206, 30, 12), (222, 52, 16), (242, 22, 13), (259, 44, 18), (281, 34, 12), (297, 50, 20), (321, 40, 14), (336, 56, 14))
    for index, (x, top, width) in enumerate(towers):
        a.rect(x, top, x + width, 80, "#5E738E" if index % 2 == 0 else "#7388A3")
    a.poly([(242, 22), (248.5, 8), (255, 22)], "#7388A3")
    a.poly([(206, 30), (218, 30), (218, 20)], "#5E738E")
    a.rect(248, 2, 249, 9, "#5E738E")
    # Ballot box
    a.rect(26, 46, 102, 92, "#B4232C")
    a.rect(22, 42, 106, 50, "#8E1B22")
    a.rect(46, 44.5, 82, 47.5, "#3A0D10")
    a.rotbox(64, 31, 28, 30, -10, "#FFFFFF")
    a.line([(56, 29), (61, 35), (72, 22)], "#1B7F4B", 2.6)
    a.disc(64, 71, 12, "#FFFFFF")
    a.star(64, 71, 9.0, 3.8, 5, -90, "#B4232C")
    # 98.8% final turnout readout & nearly full bar
    a.label(110, 46, a.note or "98.8%", 17.5, "#141923", "black", "ls")
    a.rect(110, 53, 178, 62, "#FFFFFF")
    a.rect(110, 53, 177, 62, "#15803D")


def art_benghazi(a):
    """Benghazi naval base quay: ammunition depot explosion plume over harbour warehouses and patrol ship."""
    a.bg("#F3D9A8")
    a.disc(304, 28, 14, "#FBEFC9")
    a.rect(0, 72, 352, 100, "#2F6F8F")
    for y, x0, x1 in ((80, 20, 70), (86, 190, 250), (92, 60, 130), (84, 290, 340)):
        a.rect(x0, y, x1, y + 1.3, "#5E9AB5")
    a.rect(0, 62, 236, 74, "#8B7E66")
    a.rect(0, 62, 236, 64.5, "#A2957C")
    for x, top, width in ((12, 46, 40), (60, 50, 34), (172, 48, 44)):
        a.rect(x, top, x + width, 62, "#6B5E4B")
        a.poly([(x - 2, top), (x + width / 2, top - 8), (x + width + 2, top)], "#4F4537")
        a.rect(x + width / 2 - 5, 54, x + width / 2 + 5, 62, "#3F372C")
    # Plume & blast
    smoke(a, ((132, 40, 22), (112, 28, 17), (150, 24, 19), (128, 14, 16), (166, 12, 14), (190, 8, 12)), "#3F3F46")
    smoke(a, ((124, 32, 12), (146, 20, 13), (168, 14, 9)), "#5B5B63")
    a.star(132, 50, 28, 12, 9, 8, "#E4572E")
    a.star(132, 51, 18, 8, 9, 28, "#F6A21B")
    a.star(132, 52, 10, 4.5, 9, 8, "#FFE08A")
    for x0, y0, x1, y1 in ((100, 36, 92, 28), (164, 40, 174, 33), (96, 52, 86, 50)):
        a.line([(x0, y0), (x1, y1)], "#E4572E", 1.5)
    # Moored naval patrol ship
    a.poly([(246, 70), (340, 70), (332, 82), (254, 82)], "#374151")
    a.rect(270, 58, 312, 70, "#4B5563")
    a.rect(282, 50, 300, 58, "#6B7280")
    a.rect(290, 34, 292, 50, "#374151")
    a.rect(284, 40, 298, 41.5, "#374151")
    a.rect(254, 66, 264, 70, "#4B5563")
    a.line([(258, 66), (268, 61)], "#374151", 1.8)


def art_kharkiv(a):
    """Pre-dawn Kharkiv blocks, one ablaze under rising smoke, with a delta-wing attack drone overhead."""
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
    smoke(a, ((172, 30, 14), (190, 22, 16), (212, 16, 15), (234, 13, 13), (160, 40, 10)), "#55607A")
    smoke(a, ((176, 34, 10), (194, 27, 11), (214, 22, 10)), "#6D7890")
    flame(a, 170, 47, 17, 26)
    flame(a, 152, 60, 8, 13)
    # Drone
    a.poly([(286, 30), (320, 20), (314, 31), (324, 41)], "#D7DFEE")
    a.poly([(286, 30), (310, 28.5), (314, 31), (310, 33)], "#8D99B3")
    a.dash([(284, 31), (262, 37), (240, 44)], "#C9D2E3", 1.3, 3.5, 3)


def art_banten(a):
    """Saw-tooth Indonesian factory ablaze under a long dark smoke column, fire engine playing water arc."""
    a.bg("#F1E2D0")
    smoke(a, ((96, 34, 19), (124, 22, 21), (156, 14, 20), (192, 10, 18), (226, 8, 16), (258, 8, 14), (290, 10, 12)), "#4B4B55")
    smoke(a, ((104, 38, 12), (132, 28, 14), (164, 20, 13), (198, 16, 11)), "#6A6A75")
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
    # Fire engine & water stream
    a.rect(262, 62, 330, 82, "#C81E1E")
    a.rect(312, 54, 336, 82, "#C81E1E")
    a.rect(318, 58, 332, 68, "#CFE8FF")
    a.rect(262, 74, 336, 76.5, "#FFFFFF")
    a.disc(280, 84, 7.2, "#141923")
    a.disc(318, 84, 7.2, "#141923")
    a.disc(280, 84, 3.0, "#9AA3B2")
    a.disc(318, 84, 3.0, "#9AA3B2")
    a.line(ellipse_points(204, 62, 62, 28, 0, -112, 26), "#3B9BE8", 2.5)


def art_cricket(a):
    """Wellington Basin Reserve pitch: stumps, bat, red ball and bold 720/9d record scoreboard."""
    a.bg("#2F8F4E")
    for i in range(0, 8, 2):
        a.rect(i * 44, 0, i * 44 + 44, 100, "#37A05A")
    a.rect(0, 0, 352, 16, "#BFE3F2")
    a.rect(0, 14, 352, 18, "#256F3D")
    a.poly([(118, 100), (148, 34), (200, 34), (230, 100)], "#D9C59A")
    a.rect(138, 56, 210, 57.6, "#FFFFFF")
    for x in (162, 174, 186):
        a.rect(x - 1.8, 40, x + 1.8, 84, "#F0C36A")
    a.rect(159, 38, 189, 41, "#8A5422")
    a.rotbox(95, 42, 5.2, 20, 24, "#334155")
    a.rotbox(84, 62, 14, 52, 24, "#E3C58F")
    a.disc(118, 84, 8.5, "#A01818")
    a.line(ellipse_points(118, 84, 7, 2.8, 200, 340, 10), "#FFFFFF", 1.0)
    # Scoreboard
    a.rect(236, 26, 344, 64, "#141923")
    a.rect(240, 30, 340, 60, "#1F2937")
    a.rect(286, 64, 294, 88, "#141923")
    a.label(290, 45, a.note or "720/9d", 15, "#FDE68A", "black", "mm")


def art_storm(a):
    """Southern Brazil supercell: storm clouds, lightning bolts, houses with lifting roofs and hazard triangle."""
    a.bg("#5A6880")
    smoke(a, ((40, 12, 24), (86, 6, 26), (140, 10, 28), (196, 4, 26), (250, 10, 28), (306, 6, 24), (340, 14, 20)), "#333D50")
    smoke(a, ((70, 22, 16), (128, 26, 18), (190, 22, 17), (248, 27, 16), (300, 22, 15)), "#414C62")
    a.poly([(96, 36), (120, 36), (240, 36), (212, 52), (132, 52)], "#333D50")
    for x0 in range(-10, 352, 15):
        a.line([(x0 + 14, 40), (x0, 84)], "#8FA6C4", 0.8)
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
        a.rotbox(cx, cy, 14, 4.5, turn, "#9A4A12")
    a.poly([(310, 48), (340, 48), (325, 24)], "#F97316")
    a.rect(323.5, 31, 326.5, 40, "#141923")
    a.rect(323.5, 42, 326.5, 44.5, "#141923")


def art_spacex(a):
    """Vandenberg SLC-4E dawn liftoff: Falcon 9 rising on gold flame above coastal ridge and launch tower."""
    a.bg("#162844")
    a.rect(0, 44, 352, 74, "#2B466E")
    a.rect(0, 68, 352, 100, "#D98A4E")
    # Coastal ridge silhouette
    a.poly([(0, 100), (0, 82), (76, 76), (146, 84), (240, 78), (352, 85), (352, 100)], "#1A2234")
    # Launch tower & strongback (left of rocket)
    a.rect(108, 36, 113, 86, "#475569")
    a.rect(120, 42, 124, 86, "#334155")
    for y in (44, 54, 64, 74):
        a.line([(110, y), (122, y + 6)], "#64748B", 1.2)
        a.line([(122, y), (110, y + 6)], "#64748B", 1.2)
    a.line([(124, 46), (144, 52)], "#94A3B8", 1.8)
    # Expanding launchpad steam plumes
    smoke(a, ((148, 86, 16), (170, 84, 18), (194, 86, 17), (218, 88, 15), (128, 90, 13)), "#E2E8F0")
    smoke(a, ((160, 82, 11), (186, 82, 12), (208, 86, 10)), "#F8FAFC")
    # Radiant rocket exhaust flame
    a.poly([(168, 56), (184, 56), (196, 88), (156, 88)], "#F97316")
    a.poly([(171, 56), (181, 56), (189, 86), (163, 86)], "#FACC15")
    a.poly([(174, 56), (178, 56), (182, 80), (170, 80)], "#FFFBEB")
    # Falcon 9 vehicle (clean vertical white cylinder, dark interstage, fairing)
    a.poly([(171, 16), (176, 6), (181, 16)], "#F8FAFC")
    a.rect(171, 16, 181, 26, "#F8FAFC")
    a.rect(172.5, 26, 179.5, 56, "#F1F5F9")
    a.rect(172.5, 31, 179.5, 35, "#1E293B")
    a.rect(169.5, 32, 172.5, 34.5, "#334155")
    a.rect(179.5, 32, 182.5, 34.5, "#334155")
    a.rect(171.5, 53, 180.5, 56.5, "#334155")
    # Crisp mission plaque right
    a.rect(226, 20, 340, 48, "#0F172A")
    a.rect(228, 22, 338, 46, "#1E293B")
    a.rect(228, 22, 233, 46, "#38BDF8")
    a.label(285, 34, a.note or "NROL-136", 13.5, "#FDE68A", "black", "mm")


def art_sudan_un(a):
    """Khartoum dawn skyline: damaged UN humanitarian compound under smoke plume with RSF drone overhead."""
    a.bg("#E6C697")
    a.disc(56, 30, 11, "#FAF0D7")
    a.rect(0, 82, 352, 100, "#A98F6B")
    # Surrounding Khartoum skyline silhouettes
    for x, top, width in ((8, 58, 36), (50, 50, 38), (222, 54, 42), (270, 48, 38), (314, 60, 32)):
        a.rect(x, top, x + width, 84, "#6C5B48")
        a.rect(x + 4, top + 6, x + width - 4, top + 11, "#4E4133")
    # UN compound building (centre-left)
    a.rect(96, 42, 212, 84, "#F8FAFC")
    a.rect(96, 42, 212, 51, "#2574B9")
    for wx in (106, 128, 150, 172):
        a.rect(wx, 57, wx + 13, 68, "#CBD5E1")
    a.rect(144, 71, 164, 84, "#475569")
    # UN blue emblem disc on facade
    a.disc(124, 71, 10, "#2574B9")
    a.label(124, 71, a.note or "UN", 10, "#FFFFFF", "black", "mm")
    # Blast damage & rising dark smoke on right corner of UN building
    smoke(a, ((202, 36, 16), (222, 24, 18), (246, 16, 16), (270, 12, 13)), "#3F3F46")
    smoke(a, ((208, 32, 10), (228, 22, 11)), "#5B5B63")
    a.star(198, 46, 20, 9, 8, 12, "#E4572E")
    a.star(198, 46, 12, 5.5, 8, 34, "#F6A21B")
    a.star(198, 46, 6, 3, 8, 12, "#FFE08A")
    # Attack drone & trajectory upper-right
    a.poly([(272, 28), (304, 18), (298, 29), (308, 38)], "#1E293B")
    a.dash([(268, 30), (242, 36), (218, 42)], "#334155", 1.3, 3.5, 3)


def art_anfield(a):
    """Floodlit Anfield night match: pitch, goal net, football, red card icon, and LIV 3-0 MUN scoreboard."""
    a.bg("#0E1729")
    # Floodlight glow beams
    a.poly([(24, 14), (72, 42), (44, 42)], "#1E2E4D")
    a.poly([(328, 14), (308, 42), (280, 42)], "#1E2E4D")
    a.rect(18, 10, 32, 16, "#E2E8F0")
    a.rect(320, 10, 334, 16, "#E2E8F0")
    # Mown green pitch
    a.rect(0, 40, 352, 100, "#1D703E")
    for i in range(0, 8, 2):
        a.rect(i * 44, 40, i * 44 + 44, 100, "#24834A")
    a.rect(0, 38, 352, 41, "#B8251E")
    # Penalty area & goal frame (left-centre)
    a.poly([(30, 86), (62, 56), (178, 56), (210, 86)], "#1D703E")
    a.line([(30, 86), (62, 56), (178, 56), (210, 86), (30, 86)], "#FFFFFF", 1.5)
    a.rect(76, 30, 164, 56, "#163B2A")
    for gx in range(84, 164, 10):
        a.line([(gx, 32), (gx, 56)], "#94A3B8", 0.7)
    for gy in (38, 45, 51):
        a.line([(76, gy), (164, gy)], "#94A3B8", 0.7)
    a.line([(76, 56), (76, 30), (164, 30), (164, 56)], "#FFFFFF", 2.4)
    # Football striking top corner with trail
    a.dash([(108, 76), (124, 62), (140, 44)], "#FDE68A", 1.6, 4, 3)
    a.disc(144, 41, 7.5, "#FFFFFF")
    a.star(144, 41, 3.6, 2.2, 5, -90, "#141923")
    # Red card badge (Yoro 8')
    a.rotbox(40, 62, 14, 20, -12, "#DC2626")
    # Prominent Anfield scoreboard right (generous padding around LIV 3-0 MUN)
    a.rect(196, 22, 346, 64, "#141923")
    a.rect(198, 24, 344, 62, "#1F2937")
    a.rect(198, 24, 344, 30, "#C81E1E")
    a.rect(266, 64, 276, 90, "#141923")
    a.label(271, 47, a.note or "LIV 3\u20130 MUN", 12.8, "#FDE68A", "black", "mm")


SCENES = {
    "cop31": art_cop31,
    "iran_grid": art_iran_grid,
    "spacex": art_spacex,
    "igmetall": art_igmetall,
    "storm": art_storm,
    "sudan_un": art_sudan_un,
    "anfield": art_anfield,
    "banten": art_banten,
    "vegas": art_vegas,
    "cricket": art_cricket,
}


def render_scene(name, width, height, scale=4, note=""):
    surface = Art(width, height, scale, note)
    SCENES[name](surface)
    return surface.finish()
