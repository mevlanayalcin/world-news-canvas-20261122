"""Bespoke vector illustrations and Natural Earth world atlas for the Sunday 22 November 2026 visual front page.

Every scene is drawn with Pillow vector primitives on a 4x supersampled canvas and box-filtered down so edges
stay razor sharp without photos or external assets. Circles, stars and rotated bars use pixel-isotropic radii
so globes, wheels, domes and blasts remain strictly round at every hero and gallery-card aspect ratio.
"""

import json
import math
import os

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
        self.compact = height < 140
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
    a.poly(
        [
            (cx - width, base),
            (cx - width * 0.55, base - height * 0.55),
            (cx - width * 0.2, base - height * 0.3),
            (cx, base - height),
            (cx + width * 0.3, base - height * 0.4),
            (cx + width * 0.6, base - height * 0.62),
            (cx + width, base),
        ],
        "#E4572E",
    )
    a.poly(
        [
            (cx - width * 0.6, base),
            (cx - width * 0.25, base - height * 0.4),
            (cx, base - height * 0.68),
            (cx + width * 0.35, base - height * 0.36),
            (cx + width * 0.6, base),
        ],
        "#F6A21B",
    )
    a.poly([(cx - width * 0.28, base), (cx, base - height * 0.36), (cx + width * 0.28, base)], "#FFE08A")


# ---------------------------------------------------------------- hero scenes


def art_cop31(a):
    """COP31 Antalya plenary: unsigned draft omitting fossil fuels, Earth globe, 1.5C thermometer & gavel."""
    a.bg("#0C4C56")
    a.rect(0, 0, 352, 26, "#0A3F48")
    for i in range(1, 8):
        a.rect(i * 44 - 0.6, 0, i * 44 + 0.6, 84, "#136573")
    a.rect(0, 84, 352, 100, "#08353D")
    a.rect(0, 82, 352, 84.5, "#1E7F8F")
    # Unsigned draft document (full visibility, no hero pill overlap!)
    a.rect(12, 18, 136, 86, "#062A30")
    a.rect(8, 14, 132, 82, "#FBFAF4")
    a.rect(8, 14, 132, 18, "#E7E1D3")
    a.label(70, 36, "FOSSIL FUELS", 15.5, "#141923", "black", "mm")
    a.rect(16, 50, 124, 74, "#C0271B")
    a.label(70, 62, "OMITTED", 15.5, "#FFFFFF", "black", "mm")
    # Earth globe with crisp ocean halo & continents
    a.disc(175, 50, 32, "#073038")
    a.disc(175, 49, 29.5, "#2E86CC")
    a.ring(175, 49, 29.5, "#60B5F2", 1.1)
    a.poly([(161, 32), (172, 28), (181, 31), (183, 39), (176, 43), (178, 52), (171, 63), (163, 55), (158, 46), (154, 41)], "#6FC480")
    a.poly([(185, 33), (195, 30), (201, 39), (198, 49), (190, 53), (185, 45)], "#6FC480")
    a.poly([(187, 58), (194, 56), (197, 63), (192, 69), (186, 66)], "#6FC480")
    # 1.5C thermometer + NO DEAL readout
    a.rect(218, 13, 228, 72, "#FBFAF4")
    a.disc(223, 13, 5.0, "#FBFAF4")
    a.disc(223, 75, 10.5, "#FBFAF4")
    a.disc(223, 75, 7.6, "#DC2626")
    a.rect(220.5, 25, 225.5, 73, "#DC2626")
    for y in (24, 36, 48, 60):
        a.rect(228, y - 0.6, 233, y + 0.6, "#FBFAF4")
    a.label(236, 33, "1.5\u00b0C", 18.5, "#FFFFFF", "black", "ls")
    a.label(236, 60, "NO DEAL", 15.5, "#FDE68A", "black", "ls")
    # Wooden gavel + brass band + sound block
    a.rect(298, 75, 346, 82, "#5B3413")
    a.rect(294, 81, 349, 86, "#7A4A1E")
    a.rotbox(334, 54, 8.0, 40, 38, "#B7772F")
    a.rotbox(320, 37, 32, 16, 38, "#8A5422")
    a.rotbox(320, 37, 32, 5.0, 38, "#E5B454")
    a.line(ellipse_points(319, 46, 18, 16, 208, 248, 12), "#FDE68A", 1.6)


def art_iran_grid(a):
    """Twilight Tehran skyline: half-lit, half-blacked-out blocks under faulted power pylon & unobstructed Milad Tower."""
    a.bg("#0E152C")
    a.rect(0, 26, 352, 52, "#152042")
    a.rect(0, 48, 352, 74, "#1F2D54")
    a.poly([(0, 72), (48, 42), (104, 54), (166, 32), (232, 50), (294, 38), (352, 54), (352, 100), (0, 100)], "#192445")
    a.poly([(146, 40), (166, 32), (184, 39), (172, 42), (166, 38), (156, 42)], "#5C719C")
    # Unobstructed Milad Tower
    a.poly([(196, 86), (201, 30), (207, 30), (212, 86)], "#0A1022")
    a.poly([(193, 30), (215, 30), (211, 20), (197, 20)], "#172242")
    a.rect(195, 25, 213, 27.5, "#60A5FA")
    a.rect(203.2, 5, 204.8, 20, "#334155")
    a.disc(204, 5, 2.3, "#EF4444")
    # High-voltage lattice pylon + glowing spark fault
    a.line([(64, 90), (80, 24), (86, 24), (102, 90)], "#94A3B8", 2.3)
    a.line([(70, 64), (96, 64)], "#94A3B8", 1.8)
    a.line([(75, 45), (91, 45)], "#94A3B8", 1.8)
    a.line([(68, 74), (94, 55)], "#64748B", 1.3)
    a.line([(98, 74), (72, 55)], "#64748B", 1.3)
    a.line([(54, 34), (112, 34)], "#CBD5E1", 2.4)
    a.line([(46, 48), (120, 48)], "#CBD5E1", 2.4)
    a.line([(0, 42), (26, 46), (54, 37)], "#FBBF24", 1.8)
    a.line([(0, 57), (22, 60), (46, 51)], "#FBBF24", 1.8)
    a.line([(112, 37), (138, 43), (164, 39)], "#F59E0B", 1.9)
    a.dash([(172, 40), (196, 48), (216, 46)], "#475569", 1.3, 3.5, 3.5)
    a.star(166, 39, 17, 6.4, 7, 14, "#F59E0B")
    a.star(166, 39, 9.0, 3.4, 7, 36, "#FEF08A")
    lit_blocks = ((4, 70, 26), (34, 62, 24), (62, 74, 24), (92, 66, 28), (124, 60, 28), (156, 72, 24))
    for index, (x, top, width) in enumerate(lit_blocks):
        a.rect(x, top, x + width, 100, "#0A0F1F")
        for row in range(int((96 - top) // 8)):
            for col in range(int((width - 4) // 7)):
                if (row * 3 + col * 5 + index) % 3 != 0:
                    a.rect(x + 3 + col * 7, top + 4 + row * 8, x + 6.5 + col * 7, top + 7.5 + row * 8, "#FDE047")
    dark_blocks = ((184, 64, 30), (218, 72, 26), (248, 60, 30), (282, 68, 28), (314, 58, 34))
    for index, (x, top, width) in enumerate(dark_blocks):
        a.rect(x, top, x + width, 100, "#070B16")
        for row in range(int((96 - top) // 8)):
            for col in range(int((width - 4) // 7)):
                if (row * 2 + col * 3 + index) % 4 == 0:
                    a.rect(x + 3 + col * 7, top + 4 + row * 8, x + 6.5 + col * 7, top + 7.5 + row * 8, "#1E293B")
    a.rect(222, 10, 346, 66, "#64748B")
    a.rect(224, 12, 344, 64, "#0B1124")
    a.rect(224, 12, 231, 64, "#EF4444")
    a.label(288, 29, a.note or "2h CUTS", 18.5, "#FDE68A", "black", "mm")
    a.label(288, 53, "BLACKOUTS", 15.5, "#FFFFFF", "black", "mm")


# ---------------------------------------------------------- gallery scenes


def art_igmetall(a):
    """German industrial plant halted by 24h union strikes: chimneys, barred gearwheel, crimson banners & 24h STRIKE sign."""
    a.bg("#CFE0EE")
    a.rect(0, 38, 352, 78, "#E3ECF5")
    a.rect(0, 78, 352, 100, "#64748B")
    a.rect(0, 76, 352, 79, "#334155")
    a.poly([(32, 52), (37, 14), (47, 14), (52, 52)], "#475569")
    a.poly([(62, 52), (67, 20), (77, 20), (82, 52)], "#475569")
    a.rect(36, 20, 48, 25, "#C81E1E")
    a.rect(66, 26, 78, 31, "#C81E1E")
    a.rect(14, 52, 178, 78, "#334155")
    for i in range(4):
        x = 14 + i * 40
        a.poly([(x, 52), (x, 36), (x + 40, 52)], "#1E293B")
    for x in (24, 54, 84, 114, 144):
        a.rect(x, 60, x + 18, 70, "#94A3B8")
    a.disc(132, 48, 19, "#475569")
    for i in range(8):
        a.rotbox(132, 48, 44, 6.5, i * 22.5, "#475569")
    a.disc(132, 48, 8.5, "#E3ECF5")
    a.rotbox(132, 48, 46, 6.0, -35, "#DC2626")
    for x, top in ((198, 26), (226, 34)):
        a.rect(x, top, x + 2.8, 84, "#1E293B")
        a.poly([(x + 2.8, top), (x + 28, top + 6), (x + 2.8, top + 20)], "#C81E1E")
    for sx in (194, 218, 242, 266):
        a.disc(sx, 72, 5.8, "#0F172A")
        a.poly([(sx - 7, 95), (sx - 5.5, 78), (sx + 5.5, 78), (sx + 7, 95)], "#0F172A")
    # Crisp 24h STRIKE badge with generous margins
    a.rect(240, 14, 348, 56, "#0F172A")
    a.rect(242, 16, 346, 54, "#B8251E")
    a.rect(292.5, 56, 295.5, 92, "#0F172A")
    a.label(294, 35, a.note or "24h STRIKE", 15, "#FFFFFF", "black", "mm")


def art_spacex(a):
    """Vandenberg SLC-4E dawn liftoff: Falcon 9 rising on radiant flame above launch tower."""
    a.bg("#12233E")
    a.rect(0, 34, 352, 62, "#243F68")
    a.rect(0, 58, 352, 82, "#C97841")
    a.rect(0, 74, 352, 100, "#E5A05E")
    a.poly([(0, 100), (0, 82), (76, 76), (146, 84), (240, 78), (352, 85), (352, 100)], "#161E2E")
    a.rect(98, 32, 104, 86, "#475569")
    a.rect(112, 38, 116, 86, "#334155")
    for y in (42, 52, 62, 72):
        a.line([(100, y), (114, y + 6)], "#64748B", 1.3)
        a.line([(114, y), (100, y + 6)], "#64748B", 1.3)
    a.line([(116, 44), (138, 50)], "#94A3B8", 2.0)
    smoke(a, ((142, 86, 17), (164, 84, 19), (188, 86, 18), (212, 88, 16), (122, 90, 14)), "#E2E8F0")
    smoke(a, ((154, 82, 12), (180, 82, 13), (202, 86, 11)), "#FFFFFF")
    a.poly([(162, 56), (178, 56), (194, 88), (146, 88)], "#F97316")
    a.poly([(165, 56), (175, 56), (185, 86), (155, 86)], "#FACC15")
    a.poly([(168, 56), (172, 56), (177, 80), (163, 80)], "#FFFBEB")
    a.poly([(164, 15), (170, 4), (176, 15)], "#FFFFFF")
    a.rect(164, 15, 176, 25, "#FFFFFF")
    a.rect(166, 25, 174, 56, "#F1F5F9")
    a.rect(166, 30, 174, 35, "#1E293B")
    a.rect(162.5, 31, 166, 34, "#334155")
    a.rect(174, 31, 177.5, 34, "#334155")
    a.rect(220, 14, 344, 52, "#64748B")
    a.rect(222, 16, 342, 50, "#0F172A")
    a.rect(222, 16, 229, 50, "#38BDF8")
    a.label(286, 33, a.note or "FALCON 9", 15.5, "#FDE68A", "black", "mm")


def art_gaza_storm(a):
    """Winter storm over flooded Gaza displacement tents with urgent medical-aid cross & 70K TENTS badge."""
    a.bg("#3B495E")
    a.rect(0, 34, 352, 76, "#516178")
    smoke(a, ((38, 10, 24), (94, 6, 28), (154, 10, 30), (216, 6, 28), (278, 10, 26), (332, 12, 22)), "#232D3F")
    for x0 in range(12, 352, 20):
        a.line([(x0 + 14, 34), (x0, 74)], "#93C5FD", 1.2)
    a.rect(0, 74, 352, 100, "#174275")
    a.rect(0, 74, 352, 76.5, "#60A5FA")
    for y, x0, x1 in ((82, 16, 90), (88, 130, 220), (93, 250, 336), (84, 240, 310)):
        a.rect(x0, y, x1, y + 1.8, "#60A5FA")
    for tx, tw, th, col in ((18, 66, 28, "#E2E8F0"), (90, 78, 35, "#FFFFFF"), (174, 70, 33, "#CBD5E1")):
        a.poly([(tx, 76), (tx + tw / 2, 76 - th), (tx + tw, 76)], col)
        a.poly([(tx + tw * 0.36, 76), (tx + tw / 2, 76 - th * 0.56), (tx + tw * 0.64, 76)], "#1E293B")
    a.disc(300, 50, 24, "#FFFFFF")
    a.rect(292.5, 34, 307.5, 66, "#DC2626")
    a.rect(283, 43, 317, 57, "#DC2626")
    # Crisp 70K TENTS badge top-left (clear of tents)
    a.rect(8, 6, 128, 38, "#64748B")
    a.rect(10, 8, 126, 36, "#0F172A")
    a.rect(10, 8, 16, 36, "#DC2626")
    a.label(71, 22, a.note or "70K TENTS", 15, "#FDE68A", "black", "mm")


def art_sudan_un(a):
    """Khartoum skyline: damaged UN humanitarian compound under smoke plume with attack drone overhead."""
    a.bg("#DFB880")
    a.rect(0, 44, 352, 84, "#ECCE9E")
    a.disc(46, 26, 12, "#FFF4D6")
    a.rect(0, 82, 352, 100, "#9E825E")
    for x, top, width in ((8, 56, 38), (52, 48, 38), (226, 52, 44), (276, 46, 42), (322, 58, 26)):
        a.rect(x, top, x + width, 84, "#665441")
    a.rect(96, 38, 214, 84, "#F8FAFC")
    a.rect(96, 38, 214, 49, "#1D6FA5")
    for wx in (148, 172):
        a.rect(wx, 55, wx + 14, 67, "#CBD5E1")
    a.rect(144, 71, 166, 84, "#475569")
    a.disc(122, 66, 16, "#FFFFFF")
    a.disc(122, 66, 14.5, "#1D6FA5")
    a.label(122, 66, a.note or "UN", 16, "#FFFFFF", "black", "mm")
    smoke(a, ((204, 34, 17), (226, 22, 19), (252, 14, 17), (278, 10, 14)), "#3F3F46")
    a.star(198, 46, 22, 9.8, 8, 12, "#E4572E")
    a.star(198, 46, 13.5, 6.2, 8, 34, "#F6A21B")
    a.star(198, 46, 6.8, 3.2, 8, 12, "#FFE08A")
    # Crisp dark delta-wing drone
    a.poly([(276, 26), (316, 15), (308, 27), (320, 38)], "#0F172A")
    a.dash([(272, 28), (244, 35), (220, 42)], "#1E293B", 1.6, 3.8, 3.2)


def art_banten(a):
    """Saw-tooth Indonesian factory ablaze under dark smoke column, fire engine playing water arc & 3 DEAD badge."""
    a.bg("#E6D2BC")
    a.rect(0, 44, 352, 84, "#F3E5D5")
    smoke(a, ((88, 34, 20), (118, 22, 22), (152, 14, 21), (188, 10, 19), (224, 8, 17)), "#474A54")
    a.rect(0, 84, 352, 100, "#A8967D")
    a.rect(18, 54, 208, 84, "#64748B")
    for i in range(5):
        x = 18 + i * 38
        a.poly([(x, 54), (x, 38), (x + 38, 54)], "#475569")
    for x in (34, 72, 110, 148):
        a.rect(x, 64, x + 20, 76, "#1E293B")
    flame(a, 66, 54, 23, 30)
    flame(a, 114, 54, 17, 23)
    # Detailed red fire truck + bright water arc
    a.rect(254, 60, 326, 82, "#C81E1E")
    a.rect(306, 52, 336, 82, "#C81E1E")
    a.rect(313, 56, 330, 67, "#BAE6FD")
    a.rect(254, 73, 336, 76, "#FFFFFF")
    a.rect(316, 48, 324, 52, "#38BDF8")
    a.disc(274, 84, 8.2, "#0F172A")
    a.disc(274, 84, 3.4, "#CBD5E1")
    a.disc(316, 84, 8.2, "#0F172A")
    a.disc(316, 84, 3.4, "#CBD5E1")
    a.line(ellipse_points(198, 62, 64, 28, 0, -112, 26), "#2563EB", 3.0)
    a.line(ellipse_points(198, 60, 64, 28, 0, -112, 26), "#93C5FD", 1.1)
    # Crisp 3 DEAD badge top-right
    a.rect(248, 8, 344, 40, "#64748B")
    a.rect(250, 10, 342, 38, "#0F172A")
    a.rect(250, 10, 256, 38, "#EA580C")
    a.label(299, 24, a.note or "3 DEAD", 15.5, "#FDE68A", "black", "mm")


def art_cricket(a):
    """Wellington Basin Reserve pitch: pavilion, stumps, bat, crimson ball and bold 720/9d scoreboard."""
    a.bg("#278246")
    for i in range(0, 8, 2):
        a.rect(i * 44, 0, i * 44 + 44, 100, "#319953")
    a.rect(0, 0, 352, 20, "#BCE2F2")
    a.rect(24, 8, 108, 20, "#F8FAFC")
    a.poly([(20, 8), (66, 2), (112, 8)], "#334155")
    a.rect(0, 18, 352, 22, "#1E6336")
    a.poly([(114, 100), (146, 34), (198, 34), (230, 100)], "#DEC99D")
    a.rect(136, 56, 208, 58.5, "#FFFFFF")
    for x in (160, 172, 184):
        a.rect(x - 2.0, 38, x + 2.0, 84, "#F5C86A")
    a.rect(157, 36, 187, 40, "#8A5422")
    a.rotbox(94, 40, 5.5, 20, 24, "#334155")
    a.rotbox(82, 62, 15, 52, 24, "#E6C994")
    a.disc(116, 84, 9.0, "#B91C1C")
    a.line(ellipse_points(116, 84, 7.5, 3.0, 200, 340, 10), "#FFFFFF", 1.3)
    a.rect(228, 18, 344, 68, "#64748B")
    a.rect(230, 20, 342, 66, "#0F172A")
    a.rect(230, 20, 236, 66, "#0E7490")
    a.rect(283, 68, 291, 90, "#0F172A")
    a.label(289, 43, a.note or "720/9d", 17.5, "#FDE68A", "black", "mm")


def art_us_house(a):
    """U.S. Capitol dome silhouetted on evening navy + crisp 258-seat blue majority gauge above 218 threshold."""
    a.bg("#102247")
    a.rect(0, 44, 352, 100, "#1A3263")
    for sx, sy in ((26, 16), (62, 26), (176, 16), (192, 32)):
        a.disc(sx, sy, 1.8, "#FDE68A")
    a.rect(18, 66, 186, 100, "#E2E8F0")
    a.rect(24, 74, 180, 96, "#CBD5E1")
    for cx in range(32, 176, 14):
        a.rect(cx, 74, cx + 6, 94, "#94A3B8")
    a.rect(70, 50, 134, 66, "#F8FAFC")
    for cx in range(76, 130, 10):
        a.rect(cx, 53, cx + 4, 64, "#94A3B8")
    a.poly(ellipse_points(102, 50, 30, 26, 180, 360, 24), "#FFFFFF")
    a.rect(96, 16, 108, 25, "#F8FAFC")
    a.rect(100.5, 7, 103.5, 16, "#FDE68A")
    a.rect(198, 10, 344, 88, "#64748B")
    a.rect(200, 12, 342, 86, "#0F172A")
    a.label(271, 33, a.note or "258 SEATS", 16.5, "#FDE68A", "black", "mm")
    a.rect(212, 54, 330, 74, "#B91C1C")
    a.rect(212, 54, 286, 74, "#2563EB")
    a.rect(271, 47, 274, 80, "#FFFFFF")


def art_storm(a):
    """Southern Brazil severe floods: dark storm clouds, golden lightning, submerged red-roofed homes & 5 DEAD badge."""
    a.bg("#3D4B63")
    a.rect(0, 34, 352, 72, "#51627E")
    smoke(a, ((38, 10, 24), (86, 6, 26), (140, 10, 28), (196, 4, 26), (250, 10, 28), (306, 6, 24), (340, 12, 20)), "#273142")
    for x0 in range(-8, 352, 18):
        a.line([(x0 + 14, 36), (x0, 74)], "#93C5FD", 1.1)
    # Blazing yellow lightning bolts
    a.poly([(136, 26), (154, 26), (143, 46), (156, 46), (130, 74), (139, 51), (128, 51)], "#FDE047")
    a.poly([(228, 24), (242, 24), (234, 42), (244, 42), (222, 68), (230, 47), (220, 47)], "#FDE047")
    # Red-tiled Brazilian houses half-submerged in floodwater!
    for x, width in ((16, 48), (74, 46), (166, 48), (242, 48)):
        a.rect(x, 60, x + width, 80, "#E5D3B3")
        a.rect(x + 8, 66, x + 17, 74, "#334155")
        a.rect(x + width - 17, 66, x + width - 8, 74, "#334155")
        a.poly([(x - 4, 60), (x + width / 2, 45), (x + width + 4, 60)], "#B45309")
    # Rising floodwater covering lower half of houses with bright wave ripples
    a.rect(0, 74, 352, 100, "#1D4E89")
    a.rect(0, 74, 352, 76.5, "#60A5FA")
    for y, x0, x1 in ((81, 14, 96), (86, 124, 214), (92, 236, 336), (84, 250, 324), (91, 34, 118)):
        a.rect(x0, y, x1, y + 2.0, "#93C5FD")
    # Crisp 5 DEAD badge top-right (clear of roof peaks)
    a.rect(252, 6, 344, 38, "#64748B")
    a.rect(254, 8, 342, 36, "#0F172A")
    a.rect(254, 8, 260, 36, "#7E22CE")
    a.label(301, 22, a.note or "5 DEAD", 15.5, "#FDE68A", "black", "mm")


def art_kharkiv(a):
    """Pre-dawn Kharkiv blocks ablaze under rising smoke with unmistakable swept delta-wing attack drone overhead."""
    a.bg("#13203B")
    a.rect(0, 42, 352, 100, "#1C2E52")
    a.poly([(210, 100), (232, 28), (252, 28), (268, 100)], "#263B66")
    a.poly([(118, 100), (94, 30), (112, 26), (158, 100)], "#263B66")
    blocks = ((8, 54, 46), (60, 40, 40), (104, 60, 34), (144, 46, 52), (202, 58, 40), (248, 42, 44), (298, 56, 48))
    for index, (x, top, width) in enumerate(blocks):
        a.rect(x, top, x + width, 100, "#0C1324")
        for row in range(int((96 - top) // 9)):
            for column in range(int((width - 6) // 9)):
                if (row * 5 + column * 3 + index * 2) % 5 < 2:
                    a.rect(x + 5 + column * 9, top + 6 + row * 9, x + 9 + column * 9, top + 10.5 + row * 9, "#FDE047")
    smoke(a, ((172, 28, 15), (192, 20, 17), (214, 14, 16), (236, 11, 14), (160, 38, 11)), "#4E5B75")
    flame(a, 170, 47, 20, 30)
    flame(a, 152, 60, 10, 15)
    # Crisp unmistakable swept delta-wing drone (zero meteor ambiguity!)
    a.poly([(276, 26), (324, 13), (314, 27), (328, 41)], "#F1F5F9")
    a.poly([(292, 25), (312, 20), (308, 28)], "#94A3B8")
    a.dash([(272, 28), (246, 35), (222, 44)], "#CBD5E1", 1.7, 4.0, 3.0)


def art_china_market(a):
    """Shanghai/Shenzhen equities rebound chart on deep crimson-navy with bold 80% margin-cut plaque."""
    a.bg("#1B1426")
    for gy in (25, 50, 75):
        a.rect(0, gy, 352, gy + 0.8, "#2F2640")
    for gx in (56, 112, 168, 224):
        a.rect(gx, 0, gx + 0.8, 100, "#2F2640")
    # Volume bars bottom
    vols = ((16, 20), (38, 28), (60, 24), (82, 34), (104, 26), (126, 32), (148, 42), (170, 50), (192, 56))
    for i, (vx, vh) in enumerate(vols):
        a.rect(vx, 100 - vh * 0.55, vx + 14, 100, "#DC2626" if i < 4 else "#16A34A")
    # Rebound trend line + glowing arrow
    pts = [(16, 62), (46, 72), (76, 78), (108, 66), (140, 52), (172, 34), (206, 20)]
    a.line(pts, "#22C55E", 3.2)
    a.poly([(206, 20), (190, 22), (202, 35)], "#22C55E")
    a.disc(108, 66, 4.2, "#FDE68A")
    # Crisp 80% margin cut plaque right
    a.rect(220, 14, 342, 84, "#DC2626")
    a.rect(223, 17, 339, 81, "#0F172A")
    a.rect(223, 17, 339, 25, "#DC2626")
    a.label(281, 47, a.note or "80%", 18, "#FDE68A", "black", "mm")
    a.label(281, 69, "MARGIN", 12, "#FFFFFF", "black", "mm")


def art_anfield(a):
    """Floodlit Anfield night match: green pitch, goal net, football, red card and LIV 4-0 MUN scoreboard."""
    a.bg("#0E1729")
    a.poly([(24, 14), (72, 42), (44, 42)], "#1E2E4D")
    a.poly([(328, 14), (308, 42), (280, 42)], "#1E2E4D")
    a.rect(18, 10, 32, 16, "#E2E8F0")
    a.rect(320, 10, 334, 16, "#E2E8F0")
    a.rect(0, 40, 352, 100, "#1D703E")
    for i in range(0, 8, 2):
        a.rect(i * 44, 40, i * 44 + 44, 100, "#24834A")
    a.rect(0, 38, 352, 41, "#B8251E")
    a.poly([(30, 86), (62, 56), (178, 56), (210, 86)], "#1D703E")
    a.line([(30, 86), (62, 56), (178, 56), (210, 86), (30, 86)], "#FFFFFF", 1.5)
    a.rect(76, 30, 164, 56, "#163B2A")
    for gx in range(84, 164, 10):
        a.line([(gx, 32), (gx, 56)], "#94A3B8", 0.7)
    for gy in (38, 45, 51):
        a.line([(76, gy), (164, gy)], "#94A3B8", 0.7)
    a.line([(76, 56), (76, 30), (164, 30), (164, 56)], "#FFFFFF", 2.5)
    a.dash([(108, 76), (124, 62), (140, 44)], "#FDE68A", 1.8, 4, 3)
    a.disc(144, 41, 8.0, "#FFFFFF")
    a.star(144, 41, 3.8, 2.3, 5, -90, "#141923")
    a.rotbox(40, 62, 15, 21, -12, "#DC2626")
    a.rect(192, 20, 346, 66, "#141923")
    a.rect(194, 22, 344, 64, "#1F2937")
    a.rect(194, 22, 344, 29, "#C81E1E")
    a.rect(264, 66, 274, 92, "#141923")
    a.label(269, 47, a.note or "LIV 4\u20130 MUN", 12.5, "#FDE68A", "black", "mm")


def art_vegas(a):
    """Las Vegas GP night race: neon Strip skyline, glowing Sphere, F1 car at speed and chequered flag."""
    a.bg("#140E2C")
    for x, y in sprinkle(24, 23):
        a.disc(4 + x * 344, 2 + y * 30, 0.9, "#B9B4E8")
    towers = ((6, 42, 24), (32, 30, 20), (54, 46, 30), (86, 36, 18), (228, 32, 22), (252, 44, 26), (306, 36, 18), (326, 26, 22))
    neon = ("#F472B6", "#22D3EE", "#FBBF24", "#A78BFA")
    for index, (x, top, width) in enumerate(towers):
        a.rect(x, top, x + width, 70, "#2B2056")
        a.rect(x, top, x + width, top + 1.8, neon[index % 4])
        for row in range(int((66 - top) // 7)):
            for column in range(int(width // 6)):
                if (row * 3 + column * 5 + index) % 4 != 0:
                    a.rect(x + 2.2 + column * 6, top + 5 + row * 7, x + 4.6 + column * 6, top + 8 + row * 7, neon[(row + column + index) % 4])
    a.rect(144, 6, 274, 28, "#F472B6")
    a.rect(146, 8, 272, 26, "#231848")
    a.label(209, 17, "LAS VEGAS", 12.5, "#FDE68A", "black", "mm")
    a.disc(286, 52, 18, "#D9770B")
    a.disc(286, 52, 15.5, "#F59E0B")
    a.disc(281, 48, 8.5, "#FCD34D")
    a.rect(0, 68, 352, 100, "#23262F")
    for i in range(22):
        a.rect(i * 16, 66, i * 16 + 8, 69.5, "#E11D48" if i % 2 == 0 else "#F8FAFC")
    a.rect(94, 55, 114, 59, "#E11D48")
    a.rect(94, 55, 98, 76, "#1B2B6B")
    a.poly([(102, 78), (104, 68), (126, 62), (146, 58), (152, 52), (158, 52), (160, 58), (176, 62), (196, 68), (224, 76), (226, 80), (102, 80)], "#1B2B6B")
    a.poly([(126, 66), (176, 66), (196, 71), (126, 71)], "#E11D48")
    a.poly([(196, 71), (224, 76), (226, 80), (206, 80)], "#FBBF24")
    a.disc(163, 57, 4.8, "#FBBF24")
    for cx in (122, 198):
        a.disc(cx, 78, 11.5, "#0B0D14")
        a.disc(cx, 78, 5.2, "#8B93A7")
        a.disc(cx, 78, 2.2, "#FBBF24")
    a.rect(329, 30, 331.4, 90, "#C7CBD6")
    for row in range(4):
        for column in range(5):
            a.rect(
                331.4 - (column + 1) * 5.8,
                30 + row * 5.6,
                331.4 - column * 5.8,
                35.6 + row * 5.6,
                "#F8FAFC" if (row + column) % 2 == 0 else "#0B0D14",
            )


SCENES = {
    "cop31": art_cop31,
    "iran_grid": art_iran_grid,
    "igmetall": art_igmetall,
    "spacex": art_spacex,
    "gaza_storm": art_gaza_storm,
    "sudan_un": art_sudan_un,
    "banten": art_banten,
    "cricket": art_cricket,
    "us_house": art_us_house,
    "storm": art_storm,
    "kharkiv": art_kharkiv,
    "china_market": art_china_market,
    "anfield": art_anfield,
    "vegas": art_vegas,
}


def render_scene(name, width, height, scale=4, note=""):
    surface = Art(width, height, scale, note)
    SCENES[name](surface)
    return surface.finish()


# ---------------------------------------------------------- Natural Earth atlas

LAT_SOUTH = -55.0
LAT_NORTH = 78.0


def natural_earth(lon_deg, lat_deg):
    """Natural Earth projection (Savric, Patterson, Jenny, 2011): balanced pseudocylindrical world map."""
    lam = math.radians(lon_deg)
    phi = math.radians(lat_deg)
    p2 = phi * phi
    p4 = p2 * p2
    x = lam * (0.8707 - 0.131979 * p2 + p4 * (-0.013791 + p4 * (0.003971 * p2 - 0.001529 * p4)))
    y = phi * (1.007226 + p2 * (0.015085 + p4 * (-0.044475 + 0.028874 * p2 - 0.005916 * p4)))
    return x, y


class Atlas:
    """High-contrast Natural Earth world map built from repo's atlas_land.json (1:110m thinned land rings)."""

    def __init__(
        self,
        width,
        height,
        scale=4,
        sea="#D8E8F5",
        sea_edge="#7E9EB9",
        land="#ECE1C7",
        coast="#8B7E66",
        paper="#FAF6EE",
        grid="#C3D8EA",
    ):
        self.width, self.height, self.scale = width, height, scale
        x_edge, _ = natural_earth(180.0, 0.0)
        _, y_top = natural_earth(0.0, LAT_NORTH)
        _, y_bottom = natural_earth(0.0, LAT_SOUTH)
        pad_x, pad_y = 6.0, 6.0
        self.k = min((width - 2 * pad_x) / (2 * x_edge), (height - 2 * pad_y) / (y_top - y_bottom))
        self.x_mid = width / 2.0
        self.y_mid = height / 2.0 + self.k * (y_top + y_bottom) / 2.0
        self.image = Image.new("RGB", (width * scale, height * scale), paper)
        self.draw = ImageDraw.Draw(self.image)

        outline = [self.big(180.0, lat) for lat in self.steps(LAT_SOUTH, LAT_NORTH, 2.5)]
        outline += [self.big(-180.0, lat) for lat in self.steps(LAT_NORTH, LAT_SOUTH, -2.5)]
        self.draw.polygon(outline, fill=sea)

        g_w = max(1, int(round(0.6 * scale)))
        for lon in range(-150, 180, 30):
            self.draw.line([self.big(lon, lat) for lat in self.steps(LAT_SOUTH, LAT_NORTH, 3.0)], fill=grid, width=g_w)
        for lat in (-30, 0, 30, 60):
            self.draw.line([self.big(lon, lat) for lon in range(-180, 181, 6)], fill=grid, width=g_w)

        self.draw.line(outline + [outline[0]], fill=sea_edge, width=max(1, int(round(1.3 * scale))))

        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "atlas_land.json")
        with open(path, encoding="utf-8") as handle:
            rings = json.load(handle)
        c_w = max(1, int(round(0.85 * scale)))
        for ring in rings:
            points = []
            for i in range(0, len(ring), 2):
                lon, lat = ring[i] / 10.0, ring[i + 1] / 10.0
                points.append(self.big(lon, max(LAT_SOUTH, min(LAT_NORTH, lat))))
            if len(points) >= 3:
                self.draw.polygon(points, fill=land)
                self.draw.line(points + [points[0]], fill=coast, width=c_w)

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
        x, y = natural_earth(lon, lat)
        return self.x_mid + self.k * x, self.y_mid - self.k * y

    def big(self, lon, lat):
        x, y = self.spot(lon, lat)
        return x * self.scale, y * self.scale

    def dot(self, lon, lat, colour, radius=5.4, halo="#FFFFFF"):
        s = self.scale
        x, y = self.spot(lon, lat)
        self.draw.ellipse(
            [(x - radius - 1.5) * s, (y - radius - 1.5) * s, (x + radius + 1.5) * s, (y + radius + 1.5) * s],
            fill=halo,
        )
        self.draw.ellipse([(x - radius) * s, (y - radius) * s, (x + radius) * s, (y + radius) * s], fill=colour)
        return x, y

    def hero_pin(self, lon, lat, colour, radius=9.4):
        s = self.scale
        x, y = self.spot(lon, lat)
        self.draw.ellipse(
            [(x - radius - 2.0) * s, (y - radius - 2.0) * s, (x + radius + 2.0) * s, (y + radius + 2.0) * s],
            fill="#FFFFFF",
        )
        self.draw.ellipse(
            [(x - radius - 0.8) * s, (y - radius - 0.8) * s, (x + radius + 0.8) * s, (y + radius + 0.8) * s],
            fill="#0F172A",
        )
        self.draw.ellipse(
            [(x - radius + 0.6) * s, (y - radius + 0.6) * s, (x + radius - 0.6) * s, (y + radius - 0.6) * s],
            fill=colour,
        )
        return x, y

    def leader(self, lon, lat, tx, ty, colour="#0F172A"):
        s = self.scale
        x, y = self.spot(lon, lat)
        self.draw.line([x * s, y * s, tx * s, ty * s], fill="#FFFFFF", width=max(2, int(round(3.0 * s))))
        self.draw.line([x * s, y * s, tx * s, ty * s], fill=colour, width=max(1, int(round(1.5 * s))))
        self.draw.ellipse([(x - 3.4) * s, (y - 3.4) * s, (x + 3.4) * s, (y + 3.4) * s], fill="#FFFFFF")
        self.draw.ellipse([(x - 2.2) * s, (y - 2.2) * s, (x + 2.2) * s, (y + 2.2) * s], fill=colour)
        return x, y

    def finish(self):
        return self.image.resize((self.width, self.height), Image.BOX)
