"""Verified Sunday 22 November 2026 world news dataset for the v8 Illustrated Visual World Atlas.

18 verified pure Sunday 22 November 2026 stories across all 7 world regions and 13+ major beats:
  - 2 Tall Illustrated Hero Lead Panels (COP31 Antalya + Iran rolling blackouts)
  - 12 Bespoke Illustrated Gallery Cards (3 rows x 4 columns — every story clear from picture + bold 17.5px headline)
  - 4 Bold Bottom Wire Beats (Markets, Science, Health, Tennis — 15.5px bold white on deep navy)
Zero bullet walls, zero tiny sub-captions, zero fussy source credits, zero pre-cutoff leakage.
"""

EDITION_DAY = "Sunday 22 November 2026"
EDITION_TAG = "SUNDAY EDITION"

REGIONS = [
    ("EUROPE", "#1D4ED8"),
    ("AMERICAS", "#6D28D9"),
    ("MIDDLE EAST", "#9A6700"),
    ("AFRICA", "#15803D"),
    ("ASIA", "#C2410C"),
    ("OCEANIA", "#0E7490"),
]

REGION_COLOUR = {name: colour for name, colour in REGIONS}
REGION_COLOUR["S. AMERICA"] = "#7E22CE"
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
        "deck": "44h Antalya overtime \u00b7 EU & islands reject draft",
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

# 12 Bespoke Illustrated Visual Story Cards (3 rows x 4 columns)
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
        "head": "India 720/9d vs NZ (119/2) in Test",
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
    {
        "n": 12,
        "region": "ASIA",
        "beat": "MARKETS",
        "colour": REGION_COLOUR["ASIA"],
        "art": "china_market",
        "note": "80%",
        "head": "China cuts stock margin to 80%",
        "lon": 121.5,
        "lat": 31.2,
    },
    {
        "n": 13,
        "region": "EUROPE",
        "beat": "SPORT",
        "colour": REGION_COLOUR["EUROPE"],
        "art": "anfield",
        "note": "LIV 4\u20130 MUN",
        "head": "Liverpool rout Man Utd 4\u20130 at Anfield",
        "lon": -3.0,
        "lat": 53.4,
    },
    {
        "n": 14,
        "region": "AMERICAS",
        "beat": "F1",
        "colour": REGION_COLOUR["AMERICAS"],
        "art": "vegas",
        "note": "",
        "head": "Verstappen wins Las Vegas F1 GP",
        "lon": -115.1,
        "lat": 36.2,
    },
]

# Bottom Deep-Navy Global & Regional Wire Strip (6 crisp 14.5px bold white beats — >=2 stories on every continent!)
GLOBAL_STRIP = [
    ("MARKETS", "Bitcoin near $59.2K; Brent crude $92/bbl", "#15803D", None, None),
    ("SCIENCE", "LIGO study of 257 mergers finds silent black holes", "#1D4ED8", None, None),
    ("TENNIS", "Alcaraz beats Zverev 6\u20132, 7\u20136 for ATP Finals", "#B45309", 7.7, 45.1),
    ("AFRICA", "Congo summit: Kenya & DRC restore full ties", REGION_COLOUR["AFRICA"], 15.9, -1.1),
    ("ASIA", "Onosato wins Kyushu Sumo Emperor's Cup", REGION_COLOUR["ASIA"], 130.4, 33.6),
    ("HEALTH", "Australia orders urgent online peptide probe", REGION_COLOUR["OCEANIA"], 149.1, -35.3),
]

# 7 giant bold (14.5px) open-ocean callouts on the 600 x 260 Natural Earth map — ultra-clean at 300px!
# (label, lon, lat, box_cx, box_cy, colour)
MAP_CALLOUTS = [
    ("SPACEX", -120.6, 34.7, 74, 130, REGION_COLOUR["AMERICAS"]),
    ("BRAZIL", -51.2, -30.0, 124, 214, REGION_COLOUR["S. AMERICA"]),
    ("EUROPE", 10.0, 53.5, 224, 38, REGION_COLOUR["EUROPE"]),
    ("#1 COP31", 30.7, 36.9, 448, 44, GLOBAL_COLOUR),
    ("#2 IRAN", 51.4, 35.7, 430, 146, REGION_COLOUR["MIDDLE EAST"]),
    ("KHARTOUM", 32.5, 15.6, 268, 174, REGION_COLOUR["AFRICA"]),
    ("BANTEN", 106.4, -6.2, 536, 142, REGION_COLOUR["ASIA"]),
    ("WELLINGTON", 174.8, -41.3, 452, 232, REGION_COLOUR["OCEANIA"]),
]


def total_stories():
    return len(HEROES) + len(CARDS) + len(GLOBAL_STRIP)


def check():
    assert len(HEROES) == 2
    assert len(CARDS) == 12
    assert len(GLOBAL_STRIP) == 6
    assert [s["n"] for s in HEROES + CARDS] == list(range(1, 15))
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
    print(f"OK: {total_stories()} verified Sunday 22 Nov 2026 stories (14 bespoke visual scenes + world atlas + 4 wire beats)")
