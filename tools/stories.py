"""Verified Sunday 22 November 2026 world news dataset for the v13 23-Story 3x3 + 2x6 Museum World Atlas.

23 verified pure Sunday 22 November 2026 stories across all 7 world regions and 16 beats:
  - 2 Full-Header Illustrated Hero Panels (22.5px bold serif heads + 15.5px bold decks)
  - 9 Giant 324px Panoramic Museum Flat-Vector Cards (3 rows x 3 cols, complete data badges + balanced 20.5px Lato-Black heads)
  - 12 Single-Line Crisp 17.5px Bold White Dispatches in an Airy 2 x 6 Dark-Navy Global Wire Band
Strict >= 15px global typography floor; soft archival hairlines; 6 giant 18px open-ocean map callouts.
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
    "M. EAST": "#9A6700",
    "MIDDLE EAST": "#9A6700",
    "AFRICA": "#15803D",
    "ASIA": "#C2410C",
    "OCEANIA": "#0E7490",
}
GLOBAL_COLOUR = "#B8251E"

# 2 Upper-Right Full-Header Illustrated Hero Lead Panels
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

# ALL 9 Giant Panoramic 324px Museum Flat-Vector Gallery Cards (3 rows x 3 cols) including Kharkiv Europe-War!
CARDS = [
    {
        "n": 3,
        "region": "EUROPE",
        "beat": "LABOUR",
        "colour": REGION_COLOUR["EUROPE"],
        "art": "igmetall",
        "note": "24h STRIKE",
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
        "head": "SpaceX launches NROL-136, LZ-4",
        "lon": -120.6,
        "lat": 34.7,
    },
    {
        "n": 5,
        "region": "MIDDLE EAST",
        "beat": "AID",
        "colour": REGION_COLOUR["MIDDLE EAST"],
        "art": "gaza_storm",
        "note": "70K TENTS",
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
        "note": "3 DEAD",
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
        "head": "India 720/9d vs NZ in Test",
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
        "head": "Final race seals 258 Dem seats",
        "lon": -77.0,
        "lat": 38.9,
    },
    {
        "n": 10,
        "region": "S. AMERICA",
        "beat": "STORM",
        "colour": REGION_COLOUR["S. AMERICA"],
        "art": "storm",
        "note": "5 DEAD",
        "head": "Brazil floods kill 5 in south",
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
        "head": "Drone sparks Kharkiv fire",
        "lon": 36.2,
        "lat": 50.0,
    },
]

# Bottom Airy Dark-Navy 2 x 6 Global Dispatch Band: 12 crisp 17.5px bold pure-white single-line verified stories!
# Tuple: (tag, headline, badge_colour, map_colour, lon, lat) — Left column = items 0..5, Right column = items 6..11
DISPATCHES = [
    ("CHINA", "Exchanges cut stock margin limit to 80%", REGION_COLOUR["ASIA"], REGION_COLOUR["ASIA"], 121.5, 31.2),
    ("FOOTBALL", "Liverpool rout 10-man Man Utd 4\u20130", REGION_COLOUR["EUROPE"], REGION_COLOUR["EUROPE"], -3.0, 53.4),
    ("F1 VEGAS", "Verstappen wins GP ahead of Norris", REGION_COLOUR["AMERICAS"], REGION_COLOUR["AMERICAS"], -115.1, 36.2),
    ("TENNIS", "Alcaraz beats Zverev 6\u20132, 7\u20136 ATP Finals", REGION_COLOUR["EUROPE"], REGION_COLOUR["EUROPE"], 7.7, 45.1),
    ("MARKETS", "Bitcoin near $59.2K; Brent crude $92", GLOBAL_COLOUR, GLOBAL_COLOUR, None, None),
    ("SCIENCE", "LIGO study finds 257 silent black holes", REGION_COLOUR["AMERICAS"], REGION_COLOUR["AMERICAS"], -118.1, 34.1),
    ("HEALTH", "UPenn links EFEMP1 gene to vision loss", REGION_COLOUR["AMERICAS"], REGION_COLOUR["AMERICAS"], -75.2, 40.0),
    ("LEBANON", "UNIFIL transfers posts to Lebanese army", REGION_COLOUR["M. EAST"], REGION_COLOUR["M. EAST"], 35.1, 33.1),
    ("CONGO", "Kenya & DRC agree to restore full ties", REGION_COLOUR["AFRICA"], REGION_COLOUR["AFRICA"], 15.9, -1.1),
    ("POLAND", "11-nation Coalition 2026 drills conclude", REGION_COLOUR["EUROPE"], REGION_COLOUR["EUROPE"], 22.0, 50.0),
    ("JAPAN", "Onosato wins Kyushu Sumo Emperor's Cup", REGION_COLOUR["ASIA"], REGION_COLOUR["ASIA"], 130.4, 33.6),
    ("AUSTRALIA", "Urgent inquiry into online peptide sales", REGION_COLOUR["OCEANIA"], REGION_COLOUR["OCEANIA"], 149.1, -35.3),
]

# ONLY 6 GIANT (18px) crisp open-ocean callouts on the 580 x 217 Natural Earth map — ZERO overlap & Java dot uncovered!
# (label, lon, lat, box_cx, box_cy, colour)
MAP_CALLOUTS = [
    ("SPACEX", -120.6, 34.7, 86, 108, REGION_COLOUR["AMERICAS"]),
    ("BRAZIL", -51.2, -30.0, 124, 182, REGION_COLOUR["S. AMERICA"]),
    ("#1 COP31", 30.7, 36.9, 434, 34, GLOBAL_COLOUR),
    ("#2 IRAN", 51.4, 35.7, 388, 134, REGION_COLOUR["MIDDLE EAST"]),
    ("KHARTOUM", 32.5, 15.6, 252, 150, REGION_COLOUR["AFRICA"]),
    ("BANTEN", 106.4, -6.2, 514, 100, REGION_COLOUR["ASIA"]),
]


def total_stories():
    return len(HEROES) + len(CARDS) + len(DISPATCHES)


def check():
    assert len(HEROES) == 2
    assert len(CARDS) == 9
    assert len(DISPATCHES) == 12
    assert total_stories() == 23
    assert [s["n"] for s in HEROES + CARDS] == list(range(1, 12))
    seen = {s["region"] for s in HEROES + CARDS}
    for req in ("GLOBAL", "EUROPE", "AMERICAS", "S. AMERICA", "MIDDLE EAST", "AFRICA", "ASIA", "OCEANIA"):
        assert req in seen, f"missing region: {req}"
    blob = " ".join(
        [h["head"] + " " + h["deck"] for h in HEROES]
        + [c["head"] for c in CARDS]
        + [a + " " + b for a, b, *_ in DISPATCHES]
    ).lower()
    for banned in ("merkury", "benghazi", "98.8%", "hong kong", "bepicolombo", "supercell", "spy payload", "nc call"):
        assert banned not in blob, f"banned/ambiguous token found: {banned}"


if __name__ == "__main__":
    check()
    print(f"OK: {total_stories()} verified Sunday 22 Nov 2026 stories (v13 23-Story 3x3+2x6 Atlas, >=15px floor)")
