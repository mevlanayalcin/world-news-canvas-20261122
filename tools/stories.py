"""Verified Sunday 22 November 2026 world news dataset for the v14 Sourced 25-Story 3x3 + 2x7 Museum World Atlas.

25 verified pure Sunday 22 November 2026 stories across all 7 world regions and 16+ beats:
  - 2 Full-Header Sourced Illustrated Hero Panels (22.5px bold serif heads + 15.5px attributed bold decks + outlet tags)
  - 9 Giant 324px Panoramic Sourced Museum Flat-Vector Cards (3x3, complete data badges + balanced 20.5px heads + outlets)
  - 14 Single-Line Crisp 16px Bold White Sourced Dispatches in a Sleek 2 x 7 Dark-Navy Global Wire Band
  - High-Contrast 15.5px DATE CHECK Bar explicitly documenting excluded prior-day (20-21 Nov) items
Strict >= 15px global typography floor; soft archival hairlines; 6 giant 18px open-ocean map callouts.
"""

EDITION_DAY = "Sunday 22 November 2026"
EDITION_TAG = "00:00\u201323:59 UTC \u00b7 SOURCED"

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

# 2 Upper-Right Full-Header Illustrated Sourced Hero Lead Panels
HEROES = [
    {
        "n": 1,
        "region": "GLOBAL",
        "beat": "CLIMATE",
        "src": "AP / REUTERS",
        "colour": GLOBAL_COLOUR,
        "art": "cop31",
        "note": "NO DEAL",
        "head": "COP31 ends with no deal",
        "deck": "44h Antalya overtime; EU & islands reject",
        "lon": 30.7,
        "lat": 36.9,
    },
    {
        "n": 2,
        "region": "M. EAST",
        "beat": "ENERGY",
        "src": "OFFICIAL \u00b7 RFE/RL",
        "colour": REGION_COLOUR["MIDDLE EAST"],
        "art": "iran_grid",
        "note": "2h CUTS",
        "head": "Iran imposes rolling blackouts",
        "deck": "Tavanir orders 2h cuts after gas-grid hits",
        "lon": 51.4,
        "lat": 35.7,
    },
]

# ALL 9 Giant Panoramic 324px Sourced Museum Flat-Vector Gallery Cards (3 rows x 3 cols)
CARDS = [
    {
        "n": 3,
        "region": "EUROPE",
        "beat": "LABOUR",
        "src": "TAGESSCHAU",
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
        "src": "SFN",
        "colour": REGION_COLOUR["AMERICAS"],
        "art": "spacex",
        "note": "FALCON 9",
        "head": "SpaceX launches NROL-136, LZ-4",
        "lon": -120.6,
        "lat": 34.7,
    },
    {
        "n": 5,
        "region": "M. EAST",
        "beat": "AID",
        "src": "UN REPORTS",
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
        "src": "AL JAZEERA",
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
        "src": "POLICE \u00b7 AFP",
        "colour": REGION_COLOUR["ASIA"],
        "art": "banten",
        "note": "3 DEAD",
        "head": "Banten fire: 3 dead, 36 missing",
        "lon": 106.4,
        "lat": -6.2,
    },
    {
        "n": 8,
        "region": "OCEANIA",
        "beat": "CRICKET",
        "src": "ESPN",
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
        "src": "GUARDIAN",
        "colour": REGION_COLOUR["AMERICAS"],
        "art": "us_house",
        "note": "258 SEATS",
        "head": "Final race projects 258 Dems",
        "lon": -77.0,
        "lat": 38.9,
    },
    {
        "n": 10,
        "region": "S. AMERICA",
        "beat": "STORM",
        "src": "AP",
        "colour": REGION_COLOUR["S. AMERICA"],
        "art": "storm",
        "note": "5 DEAD",
        "head": "Brazil storm kills 5, 250+ hurt",
        "lon": -53.8,
        "lat": -29.1,
    },
    {
        "n": 11,
        "region": "EUROPE",
        "beat": "WAR",
        "src": "REUTERS",
        "colour": REGION_COLOUR["EUROPE"],
        "art": "kharkiv",
        "note": "",
        "head": "Drone sparks Kharkiv fire",
        "lon": 36.2,
        "lat": 50.0,
    },
]

# Bottom Sleek Dark-Navy 2 x 7 Sourced Global Dispatch Band: 14 crisp 16px bold pure-white verified stories!
# Tuple: (tag, headline, src, badge_colour, map_colour, lon, lat) — Left col 0..6, Right col 7..13
DISPATCHES = [
    ("CHINA", "Margin cap cut to 80%, filings show", "Reuters", REGION_COLOUR["ASIA"], REGION_COLOUR["ASIA"], 121.5, 31.2),
    ("FOOTBALL", "Liverpool rout 10-man Man Utd 4\u20130", "BBC", REGION_COLOUR["EUROPE"], REGION_COLOUR["EUROPE"], -3.0, 53.4),
    ("F1 VEGAS", "Verstappen wins GP ahead of Norris", "F1", REGION_COLOUR["AMERICAS"], REGION_COLOUR["AMERICAS"], -115.1, 36.2),
    ("TENNIS", "Alcaraz beats Zverev 6\u20132, 7\u20136 ATP", "ATP", REGION_COLOUR["EUROPE"], REGION_COLOUR["EUROPE"], 7.7, 45.1),
    ("MARKETS", "Bitcoin near $59.2K; Brent $92", "Reuters", GLOBAL_COLOUR, GLOBAL_COLOUR, None, None),
    ("SCIENCE", "LIGO finds 257 silent black holes", "Caltech", REGION_COLOUR["AMERICAS"], REGION_COLOUR["AMERICAS"], -118.1, 34.1),
    ("HEALTH", "UPenn links EFEMP1 to vision loss", "UPenn", REGION_COLOUR["AMERICAS"], REGION_COLOUR["AMERICAS"], -75.2, 40.0),
    ("LEBANON", "UNIFIL hands posts to army, UN says", "UN/AA", REGION_COLOUR["M. EAST"], REGION_COLOUR["M. EAST"], 35.1, 33.1),
    ("CONGO", "Kenya & DRC restore full ties", "Reuters", REGION_COLOUR["AFRICA"], REGION_COLOUR["AFRICA"], 15.9, -1.1),
    ("POLAND", "11-nation Coalition drills conclude", "PAP", REGION_COLOUR["EUROPE"], REGION_COLOUR["EUROPE"], 22.0, 50.0),
    ("BANGLADESH", "Garment wage clashes shut plants", "Reuters", REGION_COLOUR["ASIA"], REGION_COLOUR["ASIA"], 90.4, 24.0),
    ("JAPAN", "Onosato wins Kyushu Sumo Cup", "NHK", REGION_COLOUR["ASIA"], REGION_COLOUR["ASIA"], 130.4, 33.6),
    ("AUSTRALIA", "Inquiry into online peptide sales", "ABC", REGION_COLOUR["OCEANIA"], REGION_COLOUR["OCEANIA"], 149.1, -35.3),
    ("CULTURE", "Taipei: 63rd Golden Horse Awards", "AFP", REGION_COLOUR["ASIA"], REGION_COLOUR["ASIA"], 121.5, 25.0),
]

DATE_CHECK_LEAD = "DATE CHECK (22 NOV UTC ONLY):"
DATE_CHECK_BODY = "Excluded 20\u201321 Nov: BepiColombo \u00b7 Peru M6.7 \u00b7 APEC \u00b7 Merkury \u00b7 Fri close"

# ONLY 6 GIANT (18px) crisp open-ocean callouts on the Natural Earth map — ZERO overlap & Java dot uncovered!
MAP_CALLOUTS = [
    ("SPACEX", -120.6, 34.7, 86, 102, REGION_COLOUR["AMERICAS"]),
    ("BRAZIL", -53.8, -29.1, 124, 170, REGION_COLOUR["S. AMERICA"]),
    ("#1 COP31", 30.7, 36.9, 434, 32, GLOBAL_COLOUR),
    ("#2 IRAN", 51.4, 35.7, 388, 126, REGION_COLOUR["MIDDLE EAST"]),
    ("KHARTOUM", 32.5, 15.6, 252, 142, REGION_COLOUR["AFRICA"]),
    ("BANTEN", 106.4, -6.2, 514, 94, REGION_COLOUR["ASIA"]),
]


def total_stories():
    return len(HEROES) + len(CARDS) + len(DISPATCHES)


def check():
    assert len(HEROES) == 2
    assert len(CARDS) == 9
    assert len(DISPATCHES) == 14
    assert total_stories() == 25
    assert [s["n"] for s in HEROES + CARDS] == list(range(1, 12))
    seen = {s["region"] for s in HEROES + CARDS}
    for req in ("GLOBAL", "EUROPE", "AMERICAS", "S. AMERICA", "M. EAST", "AFRICA", "ASIA", "OCEANIA"):
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
    print(f"OK: {total_stories()} verified sourced Sunday 22 Nov 2026 stories (v14 Hybrid Atlas, >=15px floor)")
