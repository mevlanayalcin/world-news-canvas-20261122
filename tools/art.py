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
    """COP31 Antalya plenary: uncrossed draft omitting fossil fuels, Earth globe, 1.5C thermometer & gavel."""
    a.bg("#0E5560")
    for i in range(1, 8):
        a.rect(i * 44 - 0.6, 0, i * 44 + 0.6, 86, "#126572")
    a.rect(0, 86, 352, 100, "#093E46")
    a.rect(14, 29, 126, 95, "#072F35")
    a.rect(10, 26, 122, 92, "#FBFAF4")
    a.label(66, 44, "FOSSIL FUELS", 12.5, "#141923", "black", "mm")
    a.rect(18, 56, 114, 79, "#C0271B")
    a.label(66, 67.5, "OMITTED", 12.5, "#FFFFFF", "black", "mm")
    a.rect(18, 84, 88, 87, "#C4CBD3")
    a.disc(174, 52, 33, "#093B43")
    a.disc(174, 51, 31, "#3D94D6")
    a.poly([(160, 34), (171, 30), (180, 33), (182, 41), (175, 45), (177, 54), (170, 65), (162, 57), (157, 48), (153, 43)], "#7DC98B")
    a.poly([(184, 35), (194, 32), (200, 41), (197, 51), (189, 55), (184, 47)], "#7DC98B")
    a.poly([(186, 60), (193, 58), (196, 65), (191, 71), (185, 68)], "#7DC98B")
    a.rect(222, 16, 232, 74, "#FBFAF4")
    a.disc(227, 16, 5.0, "#FBFAF4")
    a.disc(227, 77, 10.5, "#FBFAF4")
    a.disc(227, 77, 7.6, "#D92D20")
    a.rect(224.5, 28, 229.5, 75, "#D92D20")
    for y in (26, 38, 50, 62):
        a.rect(232, y - 0.6, 237, y + 0.6, "#FBFAF4")
    a.label(240, 34, "1.5\u00b0C", 16.5, "#FFFFFF", "black", "ls")
    a.label(240, 56, "NO DEAL", 12.5, "#FDE68A", "black", "ls")
    a.rect(294, 77, 346, 84, "#5B3413")
    a.rect(290, 83, 349, 87, "#7A4A1E")
    a.rotbox(332, 56, 8.0, 42, 38, "#B7772F")
    a.rotbox(316, 39, 34, 17, 38, "#8A5422")
    a.rotbox(316, 39, 34, 4.8, 38, "#C98B3C")
    a.line(ellipse_points(315, 48, 19, 17, 208, 248, 12), "#FDE68A", 1.5)
    a.line(ellipse_points(315, 48, 24, 22, 212, 244, 12), "#FDE68A", 1.1)


def art_iran_grid(a):
    """Twilight Tehran skyline: half-lit, half-blacked-out blocks under a faulted power pylon and Milad Tower."""
    a.bg("#101730")
    a.rect(0, 50, 352, 100, "#172140")
    a.poly([(0, 72), (48, 44), (104, 56), (168, 34), (232, 52), (294, 40), (352, 56), (352, 100), (0, 100)], "#1F2B4E")
    a.poly([(148, 42), (168, 34), (186, 41), (174, 44), (168, 40), (158, 44)], "#475982")
    a.poly([(208, 86), (213, 34), (219, 34), (224, 86)], "#0B1124")
    a.poly([(205, 34), (227, 34), (223, 24), (209, 24)], "#131C38")
    a.rect(207, 29, 225, 31.5, "#334155")
    a.rect(215.2, 8, 216.8, 24, "#1E293B")
    a.disc(216, 8, 2.2, "#EF4444")
    a.line([(72, 90), (88, 28), (94, 28), (110, 90)], "#94A3B8", 2.2)
    a.line([(78, 66), (104, 66)], "#94A3B8", 1.7)
    a.line([(83, 47), (99, 47)], "#94A3B8", 1.7)
    a.line([(76, 76), (102, 57)], "#64748B", 1.3)
    a.line([(106, 76), (80, 57)], "#64748B", 1.3)
    a.line([(62, 38), (120, 38)], "#CBD5E1", 2.3)
    a.line([(54, 51), (128, 51)], "#CBD5E1", 2.3)
    a.line([(0, 45), (30, 49), (62, 41)], "#FBBF24", 1.7)
    a.line([(0, 60), (26, 63), (54, 54)], "#FBBF24", 1.7)
    a.line([(120, 41), (146, 46), (170, 42)], "#F59E0B", 1.7)
    a.dash([(178, 43), (206, 50), (232, 48)], "#475569", 1.2, 3.5, 3.5)
    a.star(172, 42, 16, 6.0, 7, 14, "#F59E0B")
    a.star(172, 42, 8.5, 3.2, 7, 36, "#FEF08A")
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
    a.rect(232, 12, 346, 58, "#475569")
    a.rect(234, 14, 344, 56, "#0B1124")
    a.rect(234, 14, 241, 56, "#EF4444")
    a.label(292, 29, a.note or "2h CUTS", 16.5, "#FDE68A", "black", "mm")
    a.label(292, 47, "BLACKOUTS", 11.5, "#FFFFFF", "black", "mm")


# ---------------------------------------------------------- 12 gallery scenes


def art_igmetall(a):
    """German industrial plant halted by 24h union strikes: chimneys, barred gearwheel, crimson picket banners."""
    a.bg("#DCE6F0")
    a.rect(0, 78, 352, 100, "#7C8794")
    a.rect(0, 76, 352, 79, "#4B5563")
    a.poly([(38, 52), (43, 16), (53, 16), (58, 52)], "#475569")
    a.poly([(68, 52), (73, 22), (83, 22), (88, 52)], "#475569")
    a.rect(42, 22, 54, 27, "#C81E1E")
    a.rect(72, 28, 84, 33, "#C81E1E")
    a.rect(18, 52, 198, 78, "#334155")
    for i in range(4):
        x = 18 + i * 44
        a.poly([(x, 52), (x, 37), (x + 44, 52)], "#1E293B")
    for x in (30, 64, 98, 132, 166):
        a.rect(x, 60, x + 20, 70, "#94A3B8")
    a.disc(142, 48, 19, "#475569")
    for i in range(8):
        a.rotbox(142, 48, 44, 6.5, i * 22.5, "#475569")
    a.disc(142, 48, 8.5, "#DCE6F0")
    a.rotbox(142, 48, 46, 5.8, -35, "#C81E1E")
    for x, top in ((212, 28), (242, 36), (270, 30)):
        a.rect(x, top, x + 2.8, 84, "#1E293B")
        a.poly([(x + 2.8, top), (x + 30, top + 6), (x + 2.8, top + 20)], "#C81E1E")
    for sx in (208, 234, 260, 286):
        a.disc(sx, 72, 6.0, "#141923")
        a.poly([(sx - 7.5, 95), (sx - 6, 78), (sx + 6, 78), (sx + 7.5, 95)], "#141923")
    a.rect(294, 34, 346, 70, "#141923")
    a.rect(296, 36, 344, 68, "#C81E1E")
    a.rect(318.8, 70, 321.2, 92, "#141923")
    a.label(320, 52, a.note or "24h", 14, "#FFFFFF", "black", "mm")


def art_spacex(a):
    """Vandenberg SLC-4E dawn liftoff: Falcon 9 rising on radiant flame above launch tower."""
    a.bg("#162844")
    a.rect(0, 44, 352, 74, "#2B466E")
    a.rect(0, 68, 352, 100, "#D98A4E")
    a.poly([(0, 100), (0, 82), (76, 76), (146, 84), (240, 78), (352, 85), (352, 100)], "#1A2234")
    a.rect(104, 34, 110, 86, "#475569")
    a.rect(118, 40, 122, 86, "#334155")
    for y in (44, 54, 64, 74):
        a.line([(106, y), (120, y + 6)], "#64748B", 1.3)
        a.line([(120, y), (106, y + 6)], "#64748B", 1.3)
    a.line([(122, 46), (144, 52)], "#94A3B8", 2.0)
    smoke(a, ((148, 86, 17), (170, 84, 19), (194, 86, 18), (218, 88, 16), (128, 90, 14)), "#E2E8F0")
    smoke(a, ((160, 82, 12), (186, 82, 13), (208, 86, 11)), "#FFFFFF")
    a.poly([(168, 56), (184, 56), (198, 88), (154, 88)], "#F97316")
    a.poly([(171, 56), (181, 56), (190, 86), (162, 86)], "#FACC15")
    a.poly([(174, 56), (178, 56), (182, 80), (170, 80)], "#FFFBEB")
    a.poly([(170, 16), (176, 5), (182, 16)], "#FFFFFF")
    a.rect(170, 16, 182, 26, "#FFFFFF")
    a.rect(172, 26, 180, 56, "#F1F5F9")
    a.rect(172, 31, 180, 36, "#1E293B")
    a.rect(168.5, 32, 172, 35, "#334155")
    a.rect(180, 32, 183.5, 35, "#334155")
    a.rect(224, 18, 342, 48, "#0F172A")
    a.rect(226, 20, 340, 46, "#1E293B")
    a.rect(226, 20, 232, 46, "#38BDF8")
    a.label(286, 33, a.note or "NROL-136", 12.5, "#FDE68A", "black", "mm")


def art_gaza_storm(a):
    """Winter storm over flooded Gaza displacement tents with urgent white & crimson medical-aid badge."""
    a.bg("#475569")
    smoke(a, ((38, 12, 24), (94, 8, 28), (154, 12, 30), (216, 6, 28), (278, 12, 26), (332, 14, 22)), "#273142")
    for x0 in range(12, 352, 20):
        a.line([(x0 + 14, 34), (x0, 74)], "#93C5FD", 1.1)
    a.rect(0, 76, 352, 100, "#1D4E89")
    for y, x0, x1 in ((82, 16, 90), (88, 130, 220), (93, 250, 336), (84, 240, 310)):
        a.rect(x0, y, x1, y + 1.8, "#60A5FA")
    for tx, tw, th, col in ((20, 68, 32, "#E2E8F0"), (94, 78, 36, "#F8FAFC"), (178, 72, 34, "#CBD5E1")):
        a.poly([(tx, 78), (tx + tw / 2, 78 - th), (tx + tw, 78)], col)
        a.poly([(tx + tw * 0.36, 78), (tx + tw / 2, 78 - th * 0.55), (tx + tw * 0.64, 78)], "#334155")
    a.disc(300, 52, 24, "#FFFFFF")
    a.rect(292.5, 36, 307.5, 68, "#DC2626")
    a.rect(283, 45, 317, 59, "#DC2626")


def art_sudan_un(a):
    """Khartoum skyline: damaged UN humanitarian compound under smoke plume with attack drone overhead."""
    a.bg("#E6C697")
    a.disc(52, 28, 12, "#FAF0D7")
    a.rect(0, 82, 352, 100, "#A98F6B")
    for x, top, width in ((8, 56, 38), (52, 48, 38), (226, 52, 44), (276, 46, 42), (322, 58, 26)):
        a.rect(x, top, x + width, 84, "#6C5B48")
    a.rect(96, 40, 214, 84, "#F8FAFC")
    a.rect(96, 40, 214, 50, "#2574B9")
    for wx in (106, 130, 154, 178):
        a.rect(wx, 56, wx + 14, 68, "#CBD5E1")
    a.rect(144, 71, 166, 84, "#475569")
    a.disc(124, 71, 11, "#2574B9")
    a.label(124, 71, a.note or "UN", 10, "#FFFFFF", "black", "mm")
    smoke(a, ((204, 34, 17), (226, 22, 19), (252, 14, 17), (278, 10, 14)), "#3F3F46")
    a.star(198, 46, 21, 9.5, 8, 12, "#E4572E")
    a.star(198, 46, 13, 6.0, 8, 34, "#F6A21B")
    a.star(198, 46, 6.5, 3.2, 8, 12, "#FFE08A")
    a.poly([(276, 26), (314, 16), (306, 28), (318, 38)], "#1E293B")
    a.dash([(272, 28), (244, 35), (220, 42)], "#334155", 1.5, 3.8, 3.2)


def art_banten(a):
    """Saw-tooth Indonesian factory ablaze under dark smoke column, fire engine playing water arc."""
    a.bg("#F1E2D0")
    smoke(a, ((94, 34, 20), (124, 22, 22), (158, 14, 21), (194, 10, 19), (230, 8, 17), (264, 8, 14)), "#4B4B55")
    a.rect(0, 84, 352, 100, "#B9A88F")
    a.rect(20, 54, 214, 84, "#7C8794")
    for i in range(5):
        x = 20 + i * 38
        a.poly([(x, 54), (x, 38), (x + 38, 54)], "#5E6875")
    for x in (36, 74, 112, 150):
        a.rect(x, 64, x + 20, 76, "#2A2F38")
    flame(a, 68, 54, 22, 28)
    flame(a, 114, 54, 16, 22)
    a.rect(258, 60, 330, 82, "#C81E1E")
    a.rect(310, 52, 338, 82, "#C81E1E")
    a.rect(316, 56, 332, 67, "#CFE8FF")
    a.rect(258, 73, 338, 76, "#FFFFFF")
    a.disc(278, 84, 8.0, "#141923")
    a.disc(318, 84, 8.0, "#141923")
    a.line(ellipse_points(202, 62, 64, 28, 0, -112, 26), "#2563EB", 2.8)


def art_cricket(a):
    """Wellington Basin Reserve pitch: stumps, bat, crimson ball and bold 720/9d scoreboard."""
    a.bg("#2F8F4E")
    for i in range(0, 8, 2):
        a.rect(i * 44, 0, i * 44 + 44, 100, "#37A05A")
    a.rect(0, 0, 352, 16, "#BFE3F2")
    a.rect(0, 14, 352, 18, "#256F3D")
    a.poly([(114, 100), (146, 34), (198, 34), (230, 100)], "#D9C59A")
    a.rect(136, 56, 208, 58, "#FFFFFF")
    for x in (160, 172, 184):
        a.rect(x - 2.0, 38, x + 2.0, 84, "#F0C36A")
    a.rect(157, 36, 187, 40, "#8A5422")
    a.rotbox(94, 40, 5.5, 20, 24, "#334155")
    a.rotbox(82, 62, 15, 52, 24, "#E3C58F")
    a.disc(116, 84, 9.0, "#A01818")
    a.line(ellipse_points(116, 84, 7.5, 3.0, 200, 340, 10), "#FFFFFF", 1.2)
    a.rect(232, 22, 344, 66, "#141923")
    a.rect(236, 26, 340, 62, "#1F2937")
    a.rect(284, 66, 292, 90, "#141923")
    a.label(288, 44, a.note or "720/9d", 14.5, "#FDE68A", "black", "mm")


def art_us_house(a):
    """U.S. Capitol dome silhouetted on evening navy + crisp 258-seat blue majority gauge above 218 threshold."""
    a.bg("#162B54")
    for sx, sy in ((26, 16), (62, 26), (178, 16), (206, 28)):
        a.disc(sx, sy, 1.8, "#FDE68A")
    # Capitol silhouette left-centre
    a.rect(18, 66, 186, 100, "#E2E8F0")
    a.rect(24, 74, 180, 96, "#CBD5E1")
    for cx in range(32, 176, 14):
        a.rect(cx, 74, cx + 6, 94, "#94A3B8")
    # Dome tiers
    a.rect(70, 50, 134, 66, "#F8FAFC")
    for cx in range(76, 130, 10):
        a.rect(cx, 53, cx + 4, 64, "#94A3B8")
    a.poly(ellipse_points(102, 50, 30, 26, 180, 360, 24), "#FFFFFF")
    a.rect(96, 16, 108, 25, "#F8FAFC")
    a.rect(100.5, 7, 103.5, 16, "#FDE68A")
    # Bold 258-seat majority bar card right
    a.rect(202, 14, 342, 86, "#0B1328")
    a.rect(204, 16, 340, 84, "#1E293B")
    a.label(272, 34, a.note or "258 SEATS", 13.5, "#FDE68A", "black", "mm")
    # Progress bar (258 / 435 = 59.3% blue; 218 threshold white tick)
    a.rect(214, 54, 330, 72, "#B91C1C")
    a.rect(214, 54, 286, 72, "#2563EB")
    a.rect(271, 48, 274, 78, "#FFFFFF")


def art_storm(a):
    """Southern Brazil supercell: storm clouds, lightning bolts, houses with lifting roofs and hazard triangle."""
    a.bg("#5A6880")
    smoke(a, ((40, 12, 24), (86, 6, 26), (140, 10, 28), (196, 4, 26), (250, 10, 28), (306, 6, 24), (340, 14, 20)), "#333D50")
    smoke(a, ((70, 22, 16), (128, 26, 18), (190, 22, 17), (248, 27, 16), (300, 22, 15)), "#414C62")
    for x0 in range(-10, 352, 16):
        a.line([(x0 + 14, 40), (x0, 84)], "#93B4D8", 0.9)
    a.poly([(164, 28), (182, 28), (171, 50), (184, 50), (156, 84), (167, 56), (154, 56)], "#FDE047")
    a.poly([(268, 26), (282, 26), (274, 44), (284, 44), (262, 72), (270, 49), (260, 49)], "#FDE047")
    a.rect(0, 84, 352, 100, "#3E5A3A")
    for index, (x, width) in enumerate(((20, 48), (90, 42), (212, 46), (284, 48))):
        a.rect(x, 66, x + width, 86, "#D9C3A3")
        a.rect(x + width / 2 - 4, 74, x + width / 2 + 4, 86, "#6B4A2B")
        if index == 1:
            a.poly([(x - 4, 66), (x + 12, 54), (x + 20, 60), (x + 12, 66)], "#9A4A12")
        else:
            a.poly([(x - 4, 66), (x + width / 2, 50), (x + width + 4, 66)], "#9A4A12")
    a.poly([(308, 48), (342, 48), (325, 22)], "#F97316")
    a.rect(323.5, 30, 326.5, 40, "#141923")
    a.rect(323.5, 42, 326.5, 45, "#141923")


def art_kharkiv(a):
    """Pre-dawn Kharkiv blocks ablaze under rising smoke with delta-wing attack drone overhead."""
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
    smoke(a, ((172, 30, 15), (192, 22, 17), (214, 16, 16), (236, 13, 14), (160, 40, 11)), "#55607A")
    flame(a, 170, 47, 19, 28)
    flame(a, 152, 60, 9, 14)
    a.poly([(284, 28), (322, 18), (314, 30), (326, 41)], "#D7DFEE")
    a.dash([(280, 30), (256, 36), (234, 44)], "#C9D2E3", 1.5, 3.8, 3.0)


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
        sea="#BFD8EA",
        sea_edge="#6B8CA6",
        land="#EAE0C8",
        coast="#8A7E66",
        paper="#F5F1E8",
        grid="#A8C6DC",
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
