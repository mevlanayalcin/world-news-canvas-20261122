"""Fourteen verified Sunday 22 November 2026 UTC stories for the World Ledger visual front page.

Every story is verified against 2+ named outlets as of 12:00 UTC Sunday 22 November 2026:
  - 2 giant illustrated Hero cards (Climate Diplomacy, Energy/Geopolitics)
  - 8 illustrated 4x2 Global Grid cards (Sport, Labour, Elections, Security, War, Disaster, Cricket, Weather)
  - 4 large-type World Briefs (Markets/Finance, Diplomacy, African Politics, Health Policy)
Balanced to exactly 2 stories across every one of all 7 world regions, with zero Saturday-21-Nov-UTC leakage.
"""

EDITION_DAY = "Sunday 22 November 2026"
EDITION_CLOSE = "12:00 UTC"

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
        "note": "EU OBJECTS · OVERTIME",
        "head": "COP31 draft omits fossil fuels; EU objects",
        "deck": "Antalya final text sparks overtime deadlock at closing plenary",
        "when": "Antalya · Sun 22 Nov",
        "sources": ["AP", "Guardian", "Reuters"],
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
        "beat": "F1",
        "art": "vegas",
        "note": "",
        "head": "Verstappen wins Las Vegas GP",
        "deck": "Norris 2nd, Piastri 3rd; FIA checks clear",
        "when": "Las Vegas · 05:35Z",
        "sources": ["F1", "BBC Sport"],
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
        "beat": "SECURITY",
        "art": "benghazi",
        "note": "",
        "head": "Blast hits Benghazi naval base",
        "deck": "Ammo depot fire rocks Libyan port",
        "when": "Libya · 02:08Z",
        "sources": ["AA", "CGTN"],
    },
    {
        "n": 7,
        "region": "EUROPE",
        "beat": "WAR",
        "art": "kharkiv",
        "note": "",
        "head": "Drone strike sparks Kharkiv fire",
        "deck": "Russian UAV hits city overnight",
        "when": "Ukraine · 03:22Z",
        "sources": ["Interfax-UA", "TSN"],
    },
    {
        "n": 8,
        "region": "ASIA",
        "beat": "DISASTER",
        "art": "banten",
        "note": "",
        "head": "Banten fire: 36 still missing",
        "deck": "Sunday rescue after 3 die in plant",
        "when": "Indonesia · 01:04Z",
        "sources": ["Kompas", "Antara"],
    },
    {
        "n": 9,
        "region": "OCEANIA",
        "beat": "CRICKET",
        "art": "cricket",
        "note": "720/9d",
        "head": "India declare on record 720/9",
        "deck": "NZ reach 119/2 at Day 4 stumps",
        "when": "Wellington · Day 4",
        "sources": ["ICC", "The Hindu"],
    },
    {
        "n": 10,
        "region": "AMERICAS",
        "beat": "WEATHER",
        "art": "storm",
        "note": "",
        "head": "Storm alert in southern Brazil",
        "deck": "Flood warnings after 5 die in RS",
        "when": "Brazil · 05:00Z",
        "sources": ["R7", "Cemaden"],
    },
]

# Four crisp large-type global briefs completing Finance, Diplomacy, African Politics & Health Policy (2 per region)
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
        "tag": "DIPLOMACY",
        "text": "Israel: Eisenkot team opens coalition talks with Likud",
        "sources": ["ToI", "AA"],
    },
    {
        "n": 13,
        "region": "AFRICA",
        "tag": "POLITICS",
        "text": "S. Africa: ANC, ActionSA, EFF, MK near 3-metro pact",
        "sources": ["News24", "IOL"],
    },
    {
        "n": 14,
        "region": "OCEANIA",
        "tag": "HEALTH",
        "text": "Australia orders urgent inquiry on unapproved peptides",
        "sources": ["ABC News", "SBS"],
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
    assert all(c == 2 for c in counts.values()), f"expected 2 per region: {counts}"
    for s in all_stories():
        assert len(s["sources"]) >= 2, f"story #{s['n']} needs 2+ named outlets"


if __name__ == "__main__":
    check()
    print("OK:", len(all_stories()), "stories,", region_counts())
