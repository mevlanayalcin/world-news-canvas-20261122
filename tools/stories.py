"""The edition's content: forty stories dated Sunday 22 November 2026, each with its time, sources and grade.

Nothing here is computed from the network at render time. Every line was checked by hand against the named
outlets while the edition was compiled, and the page's counters are derived from these lists so they cannot
disagree with what is printed.

Grades:  CONFIRMED  two or more independent outlets
         OFFICIAL   an authority speaking on the record
         REPORTED   one outlet
         CLAIM      an unverified claim by an interested party
"""

EDITION_DAY = "Sunday 22 November 2026"
EDITION_CLOSE = "05:50"  # UTC time at which the edition closed
LEAD_SUMMARY = (
    "COP31 text omits fossil fuels  \u00b7  Iran starts rolling power cuts  \u00b7  "
    "Verstappen wins Las Vegas GP  \u00b7  IG Metall hits 19 German plants"
)

# Chronological Sunday 22 Nov 2026 UTC strip (every timestamp matches the cards below).
TIMELINE = [
    ("01:04Z", "Banten SAR"),
    ("02:08Z", "Benghazi blast"),
    ("02:26Z", "AU peptides"),
    ("02:30Z", "India 720/9d"),
    ("03:00Z", "COP31 draft"),
    ("03:50Z", "IG Metall"),
    ("04:00Z", "HK 83%"),
    ("05:35Z", "Vegas GP"),
]

# Six real Sunday 22 Nov 2026 news-stat tiles: (big figure, label, region, emphasis)
NEWS_STATS = [
    ("03:00 UTC", "COP31 draft objections shut", "GLOBAL", False),
    ("2h CUTS", "Iran nationwide power cuts", "MIDDLE EAST", True),
    ("83%", "Hong Kong noon turnout", "ASIA", False),
    ("19 PLANTS", "IG Metall 24-hr strikes", "EUROPE", False),
    ("720/9d", "India record Test in NZ", "OCEANIA", False),
    ("36 MISSING", "Banten Sunday SAR search", "ASIA", True),
]

# name, three-letter code, colour
REGIONS = [
    ("EUROPE", "EUR", "#2B5C9E"),
    ("ASIA", "ASI", "#B4551A"),
    ("MIDDLE EAST", "MDE", "#8A6A12"),
    ("AMERICAS", "AMR", "#7A3E9D"),
    ("AFRICA", "AFR", "#1E7A4C"),
    ("OCEANIA", "OCE", "#0E7C86"),
    ("GLOBAL", "GLO", "#4A5568"),
]

GRADES = [
    ("CONFIRMED", "C", "#1B7F4B", "2+ independent outlets"),
    ("OFFICIAL", "O", "#1F5FBF", "authority on the record"),
    ("REPORTED", "R", "#B7791F", "single outlet"),
    ("CLAIM", "X", "#B3261E", "unverified party claim"),
]

# Cards 1-3 are the lead row, 4-13 the two secondary rows. "place" is (longitude, latitude) for the atlas pin and
# "hang" is where the numbered bubble sits relative to the true spot, in pixels.
CARDS = [
    {
        "n": 1, "region": "GLOBAL", "art": "cop31", "note": "PLENARY 06:00 UTC",
        "head": "COP31 at the wire: \u2018final\u2019 text omits fossil fuels",
        "deck": "Third draft issued overnight; objections shut 03:00 UTC",
        "when": "Antalya \u00b7 03:00 UTC", "sources": ["AP", "BBC", "Reuters"], "grade": "CONFIRMED",
        "place": (30.7, 36.9), "hang": (-2, -17),
    },
    {
        "n": 2, "region": "MIDDLE EAST", "art": "iran_grid", "note": "2h CUTS",
        "head": "Iran starts nationwide rolling power cuts today",
        "deck": "Up to 2-hour blackouts after strikes crippled gas output",
        "when": "Tehran \u00b7 Sun 22 Nov", "sources": ["Tavanir", "RFE/RL", "Shafaq"], "grade": "CONFIRMED",
        "place": (51.39, 35.69), "hang": (17, -6),
    },
    {
        "n": 3, "region": "AMERICAS", "art": "vegas", "note": "",
        "head": "Verstappen wins Las Vegas GP; McLarens on podium",
        "deck": "Norris 2nd, Piastri 3rd, Antonelli 4th; result provisional",
        "when": "Las Vegas \u00b7 05:35 UTC", "sources": ["BBC Sport", "Guardian"], "grade": "CONFIRMED",
        "place": (-115.17, 36.11), "hang": (-16, -10),
    },
    {
        "n": 4, "region": "EUROPE", "art": "igmetall", "note": "24h",
        "head": "IG Metall calls 24h strikes at 19 German plants",
        "when": "03:50 UTC", "sources": ["tagesschau", "DLF"], "grade": "CONFIRMED",
        "place": (10.0, 53.55), "hang": (-17, -6),
    },
    {
        "n": 5, "region": "EUROPE", "art": "kharkiv", "note": "",
        "head": "Russian drone hits Kharkiv, starts fire: mayor",
        "when": "03:22 UTC", "sources": ["Interfax-UA", "TSN"], "grade": "OFFICIAL",
        "place": (36.23, 49.99), "hang": (14, -12),
    },
    {
        "n": 6, "region": "AFRICA", "art": "benghazi", "note": "",
        "head": "Blast rips ammo depot at Benghazi naval base",
        "when": "02:08 UTC", "sources": ["AA", "CGTN"], "grade": "CONFIRMED",
        "place": (20.07, 32.12), "hang": (-15, 10),
    },
    {
        "n": 7, "region": "ASIA", "art": "hongkong", "note": "",
        "head": "Hong Kong committee vote hits 83% by noon",
        "when": "04:00 UTC", "sources": ["SCMP", "Standard"], "grade": "CONFIRMED",
        "place": (114.17, 22.3), "hang": (14, -12),
    },
    {
        "n": 8, "region": "OCEANIA", "art": "peptides", "note": "",
        "head": "Australia orders urgent inquiry on peptides",
        "when": "02:26 UTC", "sources": ["ABC News", "SBS"], "grade": "CONFIRMED",
        "place": (149.13, -35.28), "hang": (-16, 8),
    },
    {
        "n": 9, "region": "ASIA", "art": "banten", "note": "",
        "head": "Banten fire: Sunday SAR hunts 36 missing, 3 dead",
        "when": "01:04 UTC", "sources": ["Kompas", "Antara"], "grade": "CONFIRMED",
        "place": (106.35, -6.2), "hang": (-14, 12),
    },
    {
        "n": 10, "region": "AFRICA", "art": "coalition", "note": "",
        "head": "ANC, ActionSA, EFF, MK near 3-metro pact",
        "when": "S. Africa \u00b7 Sun", "sources": ["News24", "IOL"], "grade": "CONFIRMED",
        "place": (28.05, -26.2), "hang": (16, 8),
    },
    {
        "n": 11, "region": "MIDDLE EAST", "art": "knesset", "note": "",
        "head": "Israel: Eisenkot set for talks with Likud",
        "when": "Sun, Jerusalem", "sources": ["ToI", "AA"], "grade": "CONFIRMED",
        "place": (35.22, 31.78), "hang": (10, 12),
    },
    {
        "n": 12, "region": "AMERICAS", "art": "storm", "note": "",
        "head": "Brazil\u2019s south on storm alert after 5 die in RS",
        "when": "05:00 UTC", "sources": ["R7", "Cemaden"], "grade": "OFFICIAL",
        "place": (-53.84, -29.08), "hang": (16, 6),
    },
    {
        "n": 13, "region": "OCEANIA", "art": "cricket", "note": "720/9d",
        "head": "India declare on record 720/9 in Wellington",
        "when": "02:30 UTC", "sources": ["The Hindu", "Cricbuzz"], "grade": "CONFIRMED",
        "place": (174.78, -41.29), "hang": (12, -13),
    },
]

# Wire dispatches 14-40. "when" is the UTC time of the event or of the first cited report; "SUN" marks an item
# dated Sunday 22 November 2026 whose exact UTC minute was not published.
WIRE = [
    {"n": 14, "region": "EUROPE", "when": "04:17", "text": "Voronezh governor: 23 drones downed overnight, no one hurt", "sources": ["RIA Novosti"], "grade": "OFFICIAL"},
    {"n": 15, "region": "EUROPE", "when": "01:34", "text": "Krasnodar: OSINT places drone-raid fire at Rosgvardia HQ", "sources": ["Astra", "DW"], "grade": "CLAIM"},
    {"n": 16, "region": "EUROPE", "when": "04:09", "text": "Finland: crews fought fire on drone-hit Sparta II all night", "sources": ["Helsingin Sanomat"], "grade": "OFFICIAL"},
    {"n": 17, "region": "ASIA", "when": "03:42", "text": "Rajasthan: 9 of a family die as van rams parked truck", "sources": ["HT", "Indian Express"], "grade": "CONFIRMED"},
    {"n": 18, "region": "ASIA", "when": "03:43", "text": "Taiwan logs 24 PLA aircraft, 11 warships, 2 balloons in 24 h", "sources": ["Taiwan MND"], "grade": "OFFICIAL"},
    {"n": 19, "region": "ASIA", "when": "SUN", "text": "Japan: top-tier landslide warning in Niigata; heavy snow north", "sources": ["NHK"], "grade": "OFFICIAL"},
    {"n": 20, "region": "ASIA", "when": "02:19", "text": "Malaysia \u2018respects\u2019 ICJ ruling of Myanmar genocide", "sources": ["New Straits Times"], "grade": "OFFICIAL"},
    {"n": 21, "region": "ASIA", "when": "02:04", "text": "South Korea: Gyeongbu line trains normal after derailment", "sources": ["Yonhap"], "grade": "REPORTED"},
    {"n": 22, "region": "ASIA", "when": "SUN", "text": "Philippines: 50\u2013100 mm rain warning for Cagayan, Isabela", "sources": ["PAGASA", "Manila Times"], "grade": "OFFICIAL"},
    {"n": 23, "region": "ASIA", "when": "01:39", "text": "Indian team in Dhaka before Ganga water treaty lapses 12 Dec", "sources": ["The Hindu"], "grade": "REPORTED"},
    {"n": 24, "region": "ASIA", "when": "SUN", "text": "Indonesia: M4.8 shallow quake hits near Sentani, Papua", "sources": ["BMKG", "QNA"], "grade": "OFFICIAL"},
    {"n": 25, "region": "MIDDLE EAST", "when": "04:42", "text": "Bahrain rejects IRGC radar-strike claim, urges UN to act", "sources": ["Iran Intl"], "grade": "REPORTED"},
    {"n": 26, "region": "MIDDLE EAST", "when": "04:14", "text": "\u2018Line-breaker\u2019 tanker signal near Hormuz was fake: trackers", "sources": ["Iran Intl"], "grade": "REPORTED"},
    {"n": 27, "region": "MIDDLE EAST", "when": "SUN", "text": "Syria: Israeli troops detain five in Quneitra night raids", "sources": ["SANA"], "grade": "REPORTED"},
    {"n": 28, "region": "AMERICAS", "when": "05:25", "text": "Sinaloa: 90% of roads blocked after capo\u2019s capture reopen", "sources": ["Sinaloa Govt"], "grade": "OFFICIAL"},
    {"n": 29, "region": "AMERICAS", "when": "03:00", "text": "NBA: Knicks edge Blazers 97\u201396 at buzzer; Spurs, Mavs win", "sources": ["CBS", "RealGM"], "grade": "CONFIRMED"},
    {"n": 30, "region": "AMERICAS", "when": "05:00", "text": "S\u00e3o Paulo runs four metro lines all night in 24-hour trial", "sources": ["Matutino"], "grade": "REPORTED"},
    {"n": 31, "region": "AFRICA", "when": "04:48", "text": "Zimbabwe police: 10 dead in three road crashes in 24 hours", "sources": ["NewZimbabwe"], "grade": "OFFICIAL"},
    {"n": 32, "region": "AFRICA", "when": "04:06", "text": "Mali: JNIM hits army, Africa Corps posts near Niono", "sources": ["RFI"], "grade": "REPORTED"},
    {"n": 33, "region": "AFRICA", "when": "SUN", "text": "Nigeria, 55 days to polls: parties trade blame for attacks", "sources": ["Vanguard"], "grade": "REPORTED"},
    {"n": 34, "region": "OCEANIA", "when": "01:50", "text": "NZ minister Nicola Grigg on leave after cancer diagnosis: PM", "sources": ["RNZ"], "grade": "OFFICIAL"},
    {"n": 35, "region": "OCEANIA", "when": "SUN", "text": "Fiji asks all businesses to cut water use 30% from December", "sources": ["FBC News"], "grade": "REPORTED"},
    {"n": 36, "region": "OCEANIA", "when": "05:11", "text": "Autopilot barred on new Spirit of Tasmania ferries", "sources": ["ABC News"], "grade": "REPORTED"},
    {"n": 37, "region": "OCEANIA", "when": "02:33", "text": "Melbourne marks 70 years since its 1956 Olympics opened", "sources": ["ABC News"], "grade": "REPORTED"},
    {"n": 38, "region": "GLOBAL", "when": "05:00", "text": "Bitcoin slips 1.4% to $59,200, near its 52-week low", "sources": ["CoinDesk", "Binance"], "grade": "CONFIRMED"},
    {"n": 39, "region": "GLOBAL", "when": "SUN", "text": "Pacific island states refuse a \u2018weak\u2019 COP31 text", "sources": ["Fiji Times"], "grade": "REPORTED"},
    {"n": 40, "region": "GLOBAL", "when": "SUN", "text": "COP31 draft backs \u201835 by 35\u2019 grid goal, omits finance floor", "sources": ["Climate Home", "DTE"], "grade": "CONFIRMED"},
]

# Ledger one: real stories that broke on Saturday 21 November UTC or earlier and are therefore NOT carried as
# Sunday UTC news, each with the verified UTC date/time and source.
EXCLUDED = [
    "BepiColombo Mercury orbit \u2013 18:24 UTC Sat (ESA)",
    "Houthi missile near Mecca \u2013 ~22:20 UTC Sat (AA)",
    "Tasmania island shooting \u2013 10:40 UTC Sat (ABC)",
    "UNIFIL Lebanon handover \u2013 Sat (AA)",
    "Peru M6.7 quake \u2013 00:09 UTC Sat (USGS)",
    "Maluku Sea M6.8 quake \u2013 09:42 UTC Sat (USGS)",
    "\u2018Chapo Isidro\u2019 capture \u2013 Fri/Sat (AP)",
    "Sparta II drone strike \u2013 Sat (Border Guard)",
    "Hormuz tanker strikes \u2013 Sat (UKMTO)",
    "Newcastle 2\u20132 Arsenal \u2013 Sat (AA)",
    "Bahrain site fire \u2013 late Sat (MoI)",
    "UN \u2018killer robots\u2019 talks end \u2013 Sat (Reuters)",
]

# Ledger two: Sunday items still open when the edition closed.
PENDING = [
    "COP31 closing plenary vote (from 06:00 UTC)",
    "F1 final classification after post-race checks",
    "Hong Kong results (polls close 10:00 UTC)",
    "Sumo: Onosato, Wakamotoharu level at 12\u20132, final day",
    "ATP Finals: Zverev v Alcaraz (17:00 UTC)",
    "SpaceX NROL-136 launch (12:23 UTC)",
    "Eisenkot\u2013Likud talks outcome",
    "Banten: fate of 36 missing workers",
    "Benghazi: cause and casualties",
]


def all_stories():
    return CARDS + WIRE


def region_counts():
    counts = {name: 0 for name, _, _ in REGIONS}
    for story in all_stories():
        counts[story["region"]] += 1
    return counts


def grade_counts():
    counts = {name: 0 for name, _, _, _ in GRADES}
    for story in all_stories():
        counts[story["grade"]] += 1
    return counts


def named_sources():
    names = set()
    for story in all_stories():
        names.update(story["sources"])
    return sorted(names)


def check():
    """Fail loudly if the lists stop adding up."""
    assert len(CARDS) == 13, len(CARDS)
    assert len(WIRE) == 27, len(WIRE)
    assert [s["n"] for s in all_stories()] == list(range(1, 41))
    assert sum(region_counts().values()) == 40
    assert sum(grade_counts().values()) == 40
    assert all(count >= 4 for count in region_counts().values()), region_counts()
    for story in all_stories():
        assert story["sources"], story["n"]
        if story["grade"] == "CONFIRMED":
            assert len(story["sources"]) >= 2, ("CONFIRMED needs two outlets", story["n"])


if __name__ == "__main__":
    check()
    print("regions", region_counts())
    print("grades ", grade_counts())
    print("sources", len(named_sources()), named_sources())
