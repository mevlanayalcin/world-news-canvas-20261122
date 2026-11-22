"""Fourteen verified Sunday 22 November 2026 UTC stories for the World Ledger 18:00 UTC visual front page.

Every story reflects verified full-day Sunday 22 November 2026 UTC outcomes as of 18:00 UTC from 2+ named outlets:
  - 2 giant illustrated Hero cards (COP31 Antalya Collapse, Iran Rolling Power Cuts)
  - 8 illustrated 4x2 Global Grid cards (SpaceX NROL-136, IG Metall Strikes, Hong Kong 98.8% Final Vote,
    Sudan Khartoum/UN Drone Strikes, Liverpool 3-0 Man Utd, Banten Factory SAR, Las Vegas F1 GP, India 720/9d Test)
  - 4 large-type World Briefs (Bitcoin $59.2K Markets, U.S. Embassy Bahrain Alert, Kharkiv Drone Fire, Brazil Flood Alert)
Covers all 7 world regions and all major beats with zero Saturday-21-Nov-UTC leakage.
"""

EDITION_DAY = "Sunday 22 November 2026"
EDITION_CLOSE = "18:00 UTC"

REGIONS = [
    ("GLOBAL", "#334155"),
    ("MIDDLE EAST", "#9A6700"),
    ("AMERICAS", "#6D28D9"),
    ("EUROPE", "#1D4ED8"),
    ("ASIA", "#C2410C"),
    ("AFRICA", "#15803D"),
    ("OCEANIA", "#0E7490"),
]

# Top 2 centerpiece hero stories (492 x 322 px each)
HEROES = [
    {
        "n": 1,
        "region": "GLOBAL",
        "beat": "CLIMATE",
        "art": "cop31",
        "note": "44h OVERTIME · NO DEAL",
        "head": "COP31 collapses in Antalya without a deal",
        "deck": "Record 44h overtime ends as EU & islands reject draft",
        "when": "Antalya · Sun 22 Nov",
        "sources": ["AP", "Reuters", "Guardian"],
    },
    {
        "n": 2,
        "region": "MIDDLE EAST",
        "beat": "ENERGY",
        "art": "iran_grid",
        "note": "2h CUTS",
        "head": "Iran starts nationwide rolling power cuts",
        "deck": "Up to 2-hour blackouts take effect after gas grid damage",
        "when": "Tehran · Sun 22 Nov",
        "sources": ["Tavanir", "RFE/RL", "Shafaq"],
    },
]

# Middle & bottom 4 x 2 illustrated global grid (241 x 230 px each)
CARDS = [
    {
        "n": 3,
        "region": "AMERICAS",
        "beat": "SPACE",
        "art": "spacex",
        "note": "NROL-136",
        "head": "SpaceX launches NROL-136",
        "deck": "Falcon 9 lands at LZ-4; 32h pad record",
        "when": "California · 12:23Z",
        "sources": ["Space.com", "SFN"],
    },
    {
        "n": 4,
        "region": "EUROPE",
        "beat": "LABOUR",
        "art": "igmetall",
        "note": "24h",
        "head": "IG Metall hits 19 German plants",
        "deck": "24-hour wage strikes across north",
        "when": "Germany · 03:50Z",
        "sources": ["tagesschau", "DLF"],
    },
    {
        "n": 5,
        "region": "ASIA",
        "beat": "VOTE",
        "art": "hongkong",
        "note": "98.8%",
        "head": "Hong Kong vote hits 98.8%",
        "deck": "5,640 cast ballots as polls close",
        "when": "Hong Kong · 10:00Z",
        "sources": ["Standard", "HK Govt"],
    },
    {
        "n": 6,
        "region": "AFRICA",
        "beat": "CONFLICT",
        "art": "sudan_un",
        "note": "UN",
        "head": "Drones hit Khartoum & UN site",
        "deck": "RSF strikes kill civilians; UN condemns",
        "when": "Sudan · Sun 22 Nov",
        "sources": ["Al Jazeera", "Xinhua"],
    },
    {
        "n": 7,
        "region": "EUROPE",
        "beat": "FOOTBALL",
        "art": "anfield",
        "note": "LIV 3\u20130 MUN",
        "head": "Liverpool rout Man Utd 3\u20130",
        "deck": "Yoro red; Szoboszlai, Wirtz, Ngumoha",
        "when": "Anfield · Sun 22 Nov",
        "sources": ["Al Jazeera", "beIN"],
    },
    {
        "n": 8,
        "region": "ASIA",
        "beat": "DISASTER",
        "art": "banten",
        "note": "",
        "head": "Banten fire: dozens missing",
        "deck": "3 dead in Sunday Cikande factory SAR",
        "when": "Indonesia · Sun 22 Nov",
        "sources": ["Guardian", "AA"],
    },
    {
        "n": 9,
        "region": "AMERICAS",
        "beat": "F1",
        "art": "vegas",
        "note": "",
        "head": "Verstappen wins Las Vegas GP",
        "deck": "Norris 2nd, Piastri 3rd; FIA checks clear",
        "when": "Las Vegas · 05:35Z",
        "sources": ["F1", "BBC Sport"],
    },
    {
        "n": 10,
        "region": "OCEANIA",
        "beat": "CRICKET",
        "art": "cricket",
        "note": "720/9d",
        "head": "India declare on record 720/9",
        "deck": "NZ reach 119/2 at Day 4 stumps",
        "when": "Wellington · Day 4",
        "sources": ["ICC", "The Hindu"],
    },
]

# Four crisp large-type global briefs covering Markets, Gulf Security, Ukraine War & South America Weather
BRIEFS = [
    {
        "n": 11,
        "region": "GLOBAL",
        "tag": "MARKETS",
        "text": "Bitcoin slides to $59,200 near 52-week low",
        "sources": ["CoinDesk", "Binance"],
    },
    {
        "n": 12,
        "region": "MIDDLE EAST",
        "tag": "GULF ALERT",
        "text": "U.S. Embassy Bahrain warns of Iran/Houthi threats",
        "sources": ["US Emb.", "AA"],
    },
    {
        "n": 13,
        "region": "EUROPE",
        "tag": "UKRAINE",
        "text": "Russian drone hits Kharkiv overnight, sparks fire",
        "sources": ["Interfax-UA", "TSN"],
    },
    {
        "n": 14,
        "region": "AMERICAS",
        "tag": "S. AMERICA",
        "text": "Brazil south on flood alert after 5 die in RS",
        "sources": ["R7", "Cemaden"],
    },
]

# High-profile Saturday 21 Nov UTC events explicitly excluded to preserve strict Sunday UTC purity
EXCLUDED_LINE = (
    "BepiColombo Mercury orbit (18:24Z Sat)  \u00b7  Mecca missile (22:20Z Sat)  \u00b7  "
    "Tasmania shooting (10:40Z Sat)  \u00b7  Peru M6.7 & Maluku M6.8 quakes (Sat)"
)


def all_stories():
    return HEROES + CARDS + BRIEFS


def region_counts():
    counts = {name: 0 for name, _ in REGIONS}
    for s in all_stories():
        counts[s["region"]] += 1
    return counts


def check():
    assert len(HEROES) == 2
    assert len(CARDS) == 8
    assert len(BRIEFS) == 4
    assert [s["n"] for s in all_stories()] == list(range(1, 15))
    counts = region_counts()
    assert all(c >= 1 for c in counts.values()), f"missing region: {counts}"
    for s in all_stories():
        assert len(s["sources"]) >= 2, f"story #{s['n']} needs 2+ named outlets"


if __name__ == "__main__":
    check()
    print("OK:", len(all_stories()), "stories,", region_counts())
