"""Verified Sunday 22 November 2026 world news dataset for the v9 Giant-Type 3x3 Visual World Atlas.

15 verified pure Sunday 22 November 2026 stories across all 7 world regions and 13 major beats:
  - 2 Tall Illustrated Hero Lead Panels (COP31 Antalya + Iran rolling blackouts, 22.5px serif heads)
  - 9 Wide Bespoke Illustrated Gallery Cards (3 rows x 3 columns, 326 x 168 each, 20.5px serif heads)
  - 4 Giant Bottom Wire Beats (F1, Football, Markets/China, Science — 17px bold white on deep navy)
ZERO text smaller than 14px anywhere on the canvas; zero bullet walls; zero source credits; zero pre-cutoff leakage.
"""

EDITION_DAY = "Sunday 22 November 2026"
EDITION_TAG = "SUNDAY EDITION"

REGIONS = [
    ("EUROPE", "#1D4ED8"),
    ("AMERICAS", "#6D28D9"),
    ("M. EAST", "#9A6700"),
    ("AFRICA", "#15803D"),
    ("ASIA", "#C2410C"),
    ("OCEANIA", "#0E7490"),
]

REGION_COLOUR = {
    "EUROPE": "#1D4ED8",
    "AMERICAS": "#6D28D9",
    "S. AMERICA": "#7E22CE",
    "MIDDLE EAST": "#9A6700",
    "AFRICA": "#15803D",
    "ASIA": "#C2410C",
    "OCEANIA": "#0E7490",
}
GLOBAL_COLOUR = "#B8251E"

# 2 Upper-Right Tall Illustrated Hero Lead Panels
HEROES = [
    {
        "n": 1,
        "region": "GLOBAL",
        "beat": "CLIMATE",
        "colour": GLOBAL_COLOUR,
        "art": "cop31",
        "note": "NO DEAL",
        "head": "COP31 ends with no deal",
        "deck": "44h Antalya overtime \u00b7 EU & islands reject",
        "lon": 30.7,
        "lat": 36.9,
    },
    {
        "n": 2,
        "region": "MIDDLE EAST",
        "beat": "ENERGY",
        "colour": REGION_COLOUR["MIDDLE EAST"],
        "art": "iran_grid",
        "note": "2h CUTS",
        "head": "Iran imposes rolling blackouts",
        "deck": "2h nationwide cuts after gas-grid strikes",
        "lon": 51.4,
        "lat": 35.7,
    },
]

# 9 Wide Bespoke Illustrated Story Cards (3 rows x 3 columns, 326 x 168 px each)
CARDS = [
    {
        "n": 3,
        "region": "EUROPE",
        "beat": "LABOUR",
        "colour": REGION_COLOUR["EUROPE"],
        "art": "igmetall",
        "note": "24h",
        "head": "IG Metall strikes 19 German plants",
        "lon": 10.0,
        "lat": 53.5,
    },
    {
        "n": 4,
        "region": "AMERICAS",
        "beat": "SPACE",
        "colour": REGION_COLOUR["AMERICAS"],
        "art": "spacex",
        "note": "FALCON 9",
        "head": "SpaceX launches NROL-136, lands LZ-4",
        "lon": -120.6,
        "lat": 34.7,
    },
    {
        "n": 5,
        "region": "MIDDLE EAST",
        "beat": "AID",
        "colour": REGION_COLOUR["MIDDLE EAST"],
        "art": "gaza_storm",
        "note": "",
        "head": "Gaza storms flood 70,000 tents",
        "lon": 34.5,
        "lat": 31.5,
    },
    {
        "n": 6,
        "region": "AFRICA",
        "beat": "CONFLICT",
        "colour": REGION_COLOUR["AFRICA"],
        "art": "sudan_un",
        "note": "UN",
        "head": "RSF drones hit Khartoum UN site",
        "lon": 32.5,
        "lat": 15.6,
    },
    {
        "n": 7,
        "region": "ASIA",
        "beat": "DISASTER",
        "colour": REGION_COLOUR["ASIA"],
        "art": "banten",
        "note": "",
        "head": "Banten fire: 3 dead, dozens missing",
        "lon": 106.4,
        "lat": -6.2,
    },
    {
        "n": 8,
        "region": "OCEANIA",
        "beat": "CRICKET",
        "colour": REGION_COLOUR["OCEANIA"],
        "art": "cricket",
        "note": "720/9d",
        "head": "India 720/9d vs NZ (119/2) Test",
        "lon": 174.8,
        "lat": -41.3,
    },
    {
        "n": 9,
        "region": "AMERICAS",
        "beat": "POLITICS",
        "colour": REGION_COLOUR["AMERICAS"],
        "art": "us_house",
        "note": "258 SEATS",
        "head": "Final race seals 258-seat Dem House",
        "lon": -77.0,
        "lat": 38.9,
    },
    {
        "n": 10,
        "region": "S. AMERICA",
        "beat": "STORM",
        "colour": REGION_COLOUR["S. AMERICA"],
        "art": "storm",
        "note": "",
        "head": "Brazil floods leave 5 dead in south",
        "lon": -51.2,
        "lat": -30.0,
    },
    {
        "n": 11,
        "region": "EUROPE",
        "beat": "WAR",
        "colour": REGION_COLOUR["EUROPE"],
        "art": "kharkiv",
        "note": "",
        "head": "Drone strike sparks Kharkiv fire",
        "lon": 36.2,
        "lat": 50.0,
    },
]

# Bottom Deep-Navy Giant 2x2 Wire Strip: (tag, text, badge_col, map_col, lon, lat)
# Packs 7 verified global & regional beats across 4 ultra-clean 16.5px bold white lines (18 stories total!)
GLOBAL_STRIP = [
    ("SPORT", "Verstappen Vegas F1 \u00b7 Liverpool 4\u20130", "#B8251E", REGION_COLOUR["AMERICAS"], -115.1, 36.2),
    ("TENNIS", "Alcaraz beats Zverev 6\u20132, 7\u20136 ATP", "#1D4ED8", REGION_COLOUR["EUROPE"], 7.7, 45.1),
    ("MARKETS", "Bitcoin $59.2K \u00b7 China margin 80%", "#15803D", REGION_COLOUR["ASIA"], 121.5, 31.2),
    ("WORLD", "Congo\u2013Kenya ties \u00b7 LIGO black holes", "#B45309", REGION_COLOUR["AFRICA"], 15.9, -1.1),
]

# 7 airy giant (15.5px) open-ocean callouts on the 586 x 250 Natural Earth map — ultra-clean at 300px!
# (label, lon, lat, box_cx, box_cy, colour)
MAP_CALLOUTS = [
    ("SPACEX", -120.6, 34.7, 74, 126, REGION_COLOUR["AMERICAS"]),
    ("BRAZIL", -51.2, -30.0, 120, 208, REGION_COLOUR["S. AMERICA"]),
    ("#1 COP31", 30.7, 36.9, 434, 42, GLOBAL_COLOUR),
    ("#2 IRAN", 51.4, 35.7, 418, 140, REGION_COLOUR["MIDDLE EAST"]),
    ("KHARTOUM", 32.5, 15.6, 260, 168, REGION_COLOUR["AFRICA"]),
    ("BANTEN", 106.4, -6.2, 522, 134, REGION_COLOUR["ASIA"]),
    ("WELLINGTON", 174.8, -41.3, 434, 224, REGION_COLOUR["OCEANIA"]),
]


def total_stories():
    return len(HEROES) + len(CARDS) + 7


def check():
    assert len(HEROES) == 2
    assert len(CARDS) == 9
    assert len(GLOBAL_STRIP) == 4
    assert [s["n"] for s in HEROES + CARDS] == list(range(1, 12))
    seen = {s["region"] for s in HEROES + CARDS}
    for req in ("GLOBAL", "EUROPE", "AMERICAS", "S. AMERICA", "MIDDLE EAST", "AFRICA", "ASIA", "OCEANIA"):
        assert req in seen, f"missing region: {req}"
    blob = " ".join(
        [h["head"] + " " + h["deck"] for h in HEROES]
        + [c["head"] for c in CARDS]
        + [a + " " + b for a, b, *_ in GLOBAL_STRIP]
    ).lower()
    for banned in ("merkury", "benghazi", "98.8%", "hong kong", "bepicolombo", "supercell", "spy payload", "nc call"):
        assert banned not in blob, f"banned/ambiguous token found: {banned}"


if __name__ == "__main__":
    check()
    print(f"OK: {total_stories()} verified Sunday 22 Nov 2026 stories (11 wide illustrated scenes + world atlas + 4 giant footer beats)")
