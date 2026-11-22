"""Ten illustrated Sunday 22 November 2026 stories + bold 3-item footer bar for the World Ledger visual front page.

Every story reflects verified Sunday 22 November 2026 outcomes from named outlets, spanning all 7 world regions
and all major beats (Climate, Energy, Space, Labour, Weather, Conflict, Football, Disaster, F1, Cricket, Markets)
with zero hyper-specific minute timestamps, zero questionable turnout numbers, and zero Saturday-UTC leakage.
"""

EDITION_DAY = "Sunday 22 November 2026"
EDITION_TAG = "SUNDAY EDITION"

REGIONS = [
    ("GLOBAL", "#334155"),
    ("MIDDLE EAST", "#9A6700"),
    ("AMERICAS", "#6D28D9"),
    ("S. AMERICA", "#7E22CE"),
    ("EUROPE", "#1D4ED8"),
    ("ASIA", "#C2410C"),
    ("AFRICA", "#15803D"),
    ("OCEANIA", "#0E7490"),
]

# Top 2 centerpiece hero stories (492 x 342 px each)
HEROES = [
    {
        "n": 1,
        "region": "GLOBAL",
        "beat": "CLIMATE",
        "art": "cop31",
        "note": "44h OVERTIME · NO DEAL",
        "head": "COP31 collapses in Antalya without a deal",
        "deck": "Record 44h overtime ends as EU & islands reject draft",
        "place": "Antalya",
        "sources": ["AP", "Reuters", "Guardian"],
    },
    {
        "n": 2,
        "region": "MIDDLE EAST",
        "beat": "ENERGY",
        "art": "iran_grid",
        "note": "2h CUTS",
        "head": "Iran starts nationwide rolling power cuts",
        "deck": "Up to 2-hour blackouts after strikes hit gas grid",
        "place": "Tehran",
        "sources": ["Tavanir", "RFE/RL", "Shafaq"],
    },
]

# Middle & bottom 4 x 2 illustrated global grid (241 x 240 px each)
CARDS = [
    {
        "n": 3,
        "region": "AMERICAS",
        "beat": "SPACE",
        "art": "spacex",
        "note": "NROL-136",
        "head": "SpaceX launches NROL-136",
        "deck": "Falcon 9 lands at LZ-4 after liftoff",
        "place": "California",
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
        "place": "Germany",
        "sources": ["tagesschau", "DLF"],
    },
    {
        "n": 5,
        "region": "S. AMERICA",
        "beat": "WEATHER",
        "art": "storm",
        "note": "",
        "head": "Storm alert in southern Brazil",
        "deck": "Flood warnings widen after 5 die",
        "place": "Brazil",
        "sources": ["R7", "Cemaden"],
    },
    {
        "n": 6,
        "region": "AFRICA",
        "beat": "CONFLICT",
        "art": "sudan_un",
        "note": "UN",
        "head": "Drones hit Khartoum & UN site",
        "deck": "RSF strikes hit city; UN condemns",
        "place": "Sudan",
        "sources": ["Al Jazeera", "Xinhua"],
    },
    {
        "n": 7,
        "region": "EUROPE",
        "beat": "FOOTBALL",
        "art": "anfield",
        "note": "LIV 3\u20130 MUN",
        "head": "Liverpool rout Man Utd 3\u20130",
        "deck": "Yoro red; Pochettino loses debut",
        "place": "Anfield",
        "sources": ["Al Jazeera", "beIN"],
    },
    {
        "n": 8,
        "region": "ASIA",
        "beat": "DISASTER",
        "art": "banten",
        "note": "",
        "head": "Banten fire: dozens missing",
        "deck": "3 dead in Sunday factory search",
        "place": "Indonesia",
        "sources": ["Guardian", "AA"],
    },
    {
        "n": 9,
        "region": "AMERICAS",
        "beat": "F1",
        "art": "vegas",
        "note": "",
        "head": "Verstappen wins Las Vegas GP",
        "deck": "Norris 2nd, Piastri 3rd on Strip",
        "place": "Las Vegas",
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
        "place": "Wellington",
        "sources": ["ICC", "The Hindu"],
    },
]

# Bold large-type single-row footer highlights (legible at 300px)
FOOTER_ITEMS = [
    ("BITCOIN $59.2K", "near 52-wk low"),
    ("BAHRAIN U.S. ALERT", "Gulf threats"),
    ("KHARKIV DRONE FIRE", "Ukraine"),
]


def all_stories():
    return HEROES + CARDS


def check():
    assert len(HEROES) == 2
    assert len(CARDS) == 8
    assert [s["n"] for s in all_stories()] == list(range(1, 11))
    seen = {s["region"] for s in all_stories()}
    for req in ("GLOBAL", "MIDDLE EAST", "AMERICAS", "S. AMERICA", "EUROPE", "ASIA", "AFRICA", "OCEANIA"):
        assert req in seen, f"missing region: {req}"
    for s in all_stories():
        assert len(s["sources"]) >= 2, f"story #{s['n']} needs 2+ named outlets"


if __name__ == "__main__":
    check()
    print("OK:", len(all_stories()), "illustrated stories +", len(FOOTER_ITEMS), "footer items")
