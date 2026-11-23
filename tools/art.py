"""Bespoke vector illustrations and Natural Earth world atlas for the Sunday 22 November 2026 front page.

Every graphic is drawn with Pillow vector primitives on a 4x supersampled canvas and box-filtered down so edges
stay razor sharp without photos or external assets. Hero scenes adapt cleanly to compact side-panel ratios,
and regional mini-illustrations suppress micro-labels so every icon reads cleanly at 300px thumbnail size.
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
        self.mini = width < 180
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
        if not self.mini:
            self.labels.append((x * self.width / UNITS_W, y * self.height / UNITS_H, text, size, colour, font, anchor))

    def finish(self):
        return self.image.resize((self.width, self.height), Image.BOX), self.labels


def ellipse_points(cx, cy, rx, ry, start_deg, end_deg, count=48):
    points = []
    for i in range(count + 1):
        t = math.radians(start_deg + (end_deg - start_deg) * i / count)
        points.append((cx + rx * math.cos(t), cy + ry * math.sin(t)))
    return points


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
    """COP31 Antalya collapse: uncrossed draft omitting fossil fuels, Earth globe, 1.5C thermometer & gavel."""
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
    # Round Earth globe
    a.disc(174, 52, 33, "#093B43")
    a.disc(174, 51, 31, "#3D94D6")
    a.poly([(160, 34), (171, 30), (180, 33), (182, 41), (175, 45), (177, 54), (170, 65), (162, 57), (157, 48), (153, 43)], "#7DC98B")
    a.poly([(184, 35), (194, 32), (200, 41), (197, 51), (189, 55), (184, 47)], "#7DC98B")
    a.poly([(186, 60), (193, 58), (196, 65), (191, 71), (185, 68)], "#7DC98B")
    # Thermometer
    a.rect(222, 16, 232, 74, "#FBFAF4")
    a.disc(227, 16, 5.0, "#FBFAF4")
    a.disc(227, 77, 10.5, "#FBFAF4")
    a.disc(227, 77, 7.6, "#D92D20")
    a.rect(224.5, 28, 229.5, 75, "#D92D20")
    for y in (26, 38, 50, 62):
        a.rect(232, y - 0.6, 237, y + 0.6, "#FBFAF4")
    a.label(240, 34, "1.5\u00b0C", 16.5, "#FFFFFF", "black", "ls")
    a.label(240, 56, "NO DEAL", 12.5, "#FDE68A", "black", "ls")
    # Raised gavel
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
    # Milad Tower silhouette
    a.poly([(208, 86), (213, 34), (219, 34), (224, 86)], "#0B1124")
    a.poly([(205, 34), (227, 34), (223, 24), (209, 24)], "#131C38")
    a.rect(207, 29, 225, 31.5, "#334155")
    a.rect(215.2, 8, 216.8, 24, "#1E293B")
    a.disc(216, 8, 2.2, "#EF4444")
    # High-voltage steel lattice pylon
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
    # Half-lit, half-blacked-out blocks
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


# --------------------------------------------------- regional lead mini-scenes


def art_igmetall(a):
    """German industrial plant halted by 24h union strikes: chimneys, barred gearwheel & crimson picket flags."""
    a.bg("#D9E5F0")
    a.rect(0, 78, 352, 100, "#7C8794")
    a.rect(0, 76, 352, 79, "#4B5563")
    a.poly([(36, 52), (41, 14), (52, 14), (57, 52)], "#475569")
    a.poly([(68, 52), (73, 20), (84, 20), (89, 52)], "#475569")
    a.rect(40, 21, 53, 27, "#C81E1E")
    a.rect(72, 27, 85, 33, "#C81E1E")
    a.rect(14, 52, 212, 78, "#334155")
    for i in range(4):
        x = 14 + i * 48
        a.poly([(x, 52), (x, 36), (x + 48, 52)], "#1E293B")
    for x in (28, 66, 104, 142, 180):
        a.rect(x, 60, x + 22, 71, "#94A3B8")
    # Bold cogwheel with red halt slash
    a.disc(154, 46, 20, "#475569")
    for i in range(8):
        a.rotbox(154, 46, 46, 7.0, i * 22.5, "#475569")
    a.disc(154, 46, 9.5, "#D9E5F0")
    a.rotbox(154, 46, 50, 6.5, -35, "#C81E1E")
    # Crimson picket flags & strikers
    for x, top in ((232, 22), (268, 30), (304, 24)):
        a.rect(x, top, x + 3.5, 86, "#1E293B")
        a.poly([(x + 3.5, top), (x + 38, top + 7), (x + 3.5, top + 24)], "#C81E1E")
    for sx in (228, 260, 294, 326):
        a.disc(sx, 72, 7.0, "#141923")
        a.poly([(sx - 9, 96), (sx - 7, 79), (sx + 7, 79), (sx + 9, 96)], "#141923")


def art_spacex(a):
    """Vandenberg SLC-4E dawn liftoff: Falcon 9 rising on radiant gold flame above coastal ridge."""
    a.bg("#142642")
    a.rect(0, 44, 352, 72, "#29466E")
    a.rect(0, 66, 352, 100, "#DF8B49")
    a.poly([(0, 100), (0, 82), (82, 76), (156, 84), (246, 77), (352, 84), (352, 100)], "#182234")
    # Launch tower
    a.rect(92, 30, 100, 86, "#475569")
    a.rect(108, 38, 114, 86, "#334155")
    a.line([(114, 42), (144, 50)], "#94A3B8", 2.4)
    # Steam cloud
    smoke(a, ((148, 86, 20), (178, 84, 22), (210, 86, 20), (240, 88, 17), (122, 90, 16)), "#E2E8F0")
    smoke(a, ((166, 82, 14), (198, 82, 15)), "#FFFFFF")
    # Exhaust flame
    a.poly([(168, 54), (192, 54), (210, 90), (150, 90)], "#F97316")
    a.poly([(172, 54), (188, 54), (198, 86), (162, 86)], "#FACC15")
    a.poly([(176, 54), (184, 54), (189, 80), (171, 80)], "#FFFBEB")
    # Falcon 9
    a.poly([(172, 18), (180, 4), (188, 18)], "#FFFFFF")
    a.rect(172, 18, 188, 28, "#FFFFFF")
    a.rect(174, 28, 186, 56, "#F1F5F9")
    a.rect(174, 33, 186, 38, "#1E293B")
    # Bright stars top-right
    for sx, sy in ((264, 20), (298, 32), (324, 16), (48, 22)):
        a.disc(sx, sy, 2.2, "#FDE68A")


def art_gaza_storm(a):
    """Winter storm over flooded Gaza displacement tents with urgent medical-aid cross symbol."""
    a.bg("#475569")
    smoke(a, ((38, 12, 26), (94, 8, 30), (154, 12, 32), (216, 6, 30), (278, 12, 28), (332, 14, 24)), "#273142")
    for x0 in range(12, 352, 22):
        a.line([(x0 + 14, 34), (x0, 74)], "#93C5FD", 1.3)
    # Flooded water basin
    a.rect(0, 76, 352, 100, "#1D4E89")
    for y, x0, x1 in ((82, 16, 90), (88, 130, 220), (93, 250, 336), (84, 240, 310)):
        a.rect(x0, y, x1, y + 2.0, "#60A5FA")
    # Tents standing in floodwater
    for tx, tw, th, col in ((22, 68, 32, "#E2E8F0"), (96, 78, 36, "#F8FAFC"), (180, 72, 34, "#CBD5E1")):
        a.poly([(tx, 78), (tx + tw / 2, 78 - th), (tx + tw, 78)], col)
        a.poly([(tx + tw * 0.36, 78), (tx + tw / 2, 78 - th * 0.55), (tx + tw * 0.64, 78)], "#334155")
    # Crisp white & crimson medical aid cross badge (insulin crisis)
    a.disc(302, 54, 25, "#FFFFFF")
    a.rect(294, 38, 310, 70, "#DC2626")
    a.rect(284, 47, 320, 61, "#DC2626")


def art_sudan_un(a):
    """Khartoum skyline: damaged UN humanitarian compound under smoke plume with attack drone overhead."""
    a.bg("#E6C697")
    a.disc(48, 28, 13, "#FAF0D7")
    a.rect(0, 82, 352, 100, "#A98F6B")
    for x, top, width in ((8, 56, 40), (54, 48, 38), (234, 52, 46), (288, 46, 52)):
        a.rect(x, top, x + width, 84, "#6C5B48")
    # UN compound
    a.rect(98, 40, 224, 84, "#F8FAFC")
    a.rect(98, 40, 224, 52, "#2574B9")
    for wx in (110, 138, 166):
        a.rect(wx, 58, wx + 16, 70, "#CBD5E1")
    a.disc(132, 68, 12, "#2574B9")
    # Blast & smoke plume
    smoke(a, ((212, 34, 20), (238, 22, 22), (266, 14, 20), (296, 10, 17)), "#3F3F46")
    a.star(206, 46, 24, 11, 8, 12, "#E4572E")
    a.star(206, 46, 14, 6.5, 8, 34, "#F6A21B")
    a.star(206, 46, 7, 3.5, 8, 12, "#FFE08A")
    # Attack drone
    a.poly([(280, 26), (324, 14), (316, 28), (328, 40)], "#1E293B")
    a.dash([(276, 28), (246, 36), (222, 42)], "#334155", 1.8, 4.0, 3.5)


def art_banten(a):
    """Saw-tooth Indonesian factory ablaze under dark smoke column, fire engine spraying water arc."""
    a.bg("#F1E2D0")
    smoke(a, ((92, 32, 22), (126, 20, 24), (164, 12, 23), (206, 8, 21), (248, 8, 18), (288, 10, 15)), "#4B4B55")
    a.rect(0, 84, 352, 100, "#B9A88F")
    a.rect(18, 52, 216, 84, "#7C8794")
    for i in range(5):
        x = 18 + i * 40
        a.poly([(x, 52), (x, 36), (x + 40, 52)], "#5E6875")
    for x in (34, 76, 118, 160):
        a.rect(x, 62, x + 22, 76, "#2A2F38")
    flame(a, 68, 52, 24, 32)
    flame(a, 118, 52, 18, 24)
    # Red fire engine & blue water stream
    a.rect(254, 58, 332, 82, "#C81E1E")
    a.rect(310, 48, 340, 82, "#C81E1E")
    a.rect(316, 54, 334, 66, "#CFE8FF")
    a.rect(254, 72, 340, 76, "#FFFFFF")
    a.disc(276, 84, 9.0, "#141923")
    a.disc(318, 84, 9.0, "#141923")
    a.line(ellipse_points(200, 60, 66, 30, 0, -112, 26), "#2563EB", 3.5)


def art_cricket(a):
    """Wellington Basin Reserve pitch: sunlit green outfield, stumps, bat & crimson cricket ball."""
    a.bg("#2F8F4E")
    for i in range(0, 8, 2):
        a.rect(i * 44, 0, i * 44 + 44, 100, "#37A05A")
    a.rect(0, 0, 352, 18, "#BFE3F2")
    a.rect(0, 16, 352, 21, "#256F3D")
    a.poly([(114, 100), (154, 32), (214, 32), (254, 100)], "#D9C59A")
    a.rect(140, 58, 228, 60.5, "#FFFFFF")
    for x in (168, 184, 200):
        a.rect(x - 2.6, 34, x + 2.6, 86, "#F0C36A")
    a.rect(164, 31, 204, 36, "#8A5422")
    a.rotbox(96, 38, 6.5, 22, 24, "#334155")
    a.rotbox(82, 62, 18, 56, 24, "#E3C58F")
    a.disc(278, 70, 16, "#B91C1C")
    a.line(ellipse_points(278, 70, 13, 5.0, 200, 340, 12), "#FFFFFF", 1.8)


SCENES = {
    "cop31": art_cop31,
    "iran_grid": art_iran_grid,
    "igmetall": art_igmetall,
    "spacex": art_spacex,
    "gaza_storm": art_gaza_storm,
    "sudan_un": art_sudan_un,
    "banten": art_banten,
    "cricket": art_cricket,
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

    def dot(self, lon, lat, colour, radius=5.0, halo="#FFFFFF"):
        s = self.scale
        x, y = self.spot(lon, lat)
        self.draw.ellipse(
            [(x - radius - 1.4) * s, (y - radius - 1.4) * s, (x + radius + 1.4) * s, (y + radius + 1.4) * s],
            fill=halo,
        )
        self.draw.ellipse([(x - radius) * s, (y - radius) * s, (x + radius) * s, (y + radius) * s], fill=colour)
        return x, y

    def hero_pin(self, lon, lat, colour, radius=9.2):
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
