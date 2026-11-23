"""Verified Sunday 22 November 2026 world news dataset for the v15 Chronicle Front Page (36 sourced stories).

All 36 stories occurred or first broke on Sunday 22 November 2026 (00:00-23:59 UTC), spanning all 7 regions
and 16 beats with multi-outlet sources and explicit verification stamps (CONFIRMED / OFFICIAL / REPORTED / CLAIM):
  - 3 Flagship Illustrated Lead Stories (#1-#3) with concrete 2-3 line factual sub-decks
  - 10 Illustrated Feature Cards (#4-#13, 2 rows x 5 cols) with focal stat badges & factual sub-decks
  - 23 Single-Line Sourced Wire Dispatches (#14-#36) in a crisp 2-column light-ivory ledger beside the world map
  - Explicit DATE CHECK audit box listing intentionally excluded Sat 21 Nov (or earlier) & Mon 23 Nov items
"""

EDITION_DAY = "Sunday 22 November 2026"
EDITION_TITLE = "WORLD NEWS CHRONICLE"
EDITION_SUB = "ONE DAY IN ONE PICTURE"

REGION_ORDER = ("Europe", "Americas", "Asia", "M. East", "Africa", "Global", "Oceania")

REGION_COLOUR = {
    "Global": "#B8251E",
    "Europe": "#1D4ED8",
    "Americas": "#6D28D9",
    "M. East": "#9A6700",
    "Africa": "#15803D",
    "Asia": "#C2410C",
    "Oceania": "#0E7490",
}

VERIFY_COLOUR = {
    "CONFIRMED": "#15803D",
    "OFFICIAL": "#1D4ED8",
    "REPORTED": "#9A6700",
    "CLAIM": "#B8251E",
    "C": "#15803D",
    "O": "#1D4ED8",
    "R": "#9A6700",
}

# Chronological Sunday 22 Nov 2026 UTC anchor milestones (00:00 -> 23:59 UTC)
TIMELINE = [
    ("04:00Z", "Vegas F1 GP", "Americas"),
    ("09:00Z", "COP31 no deal", "Global"),
    ("12:00Z", "UNIFIL handover", "M. East"),
    ("15:15Z", "Liverpool 4\u20130", "Europe"),
    ("18:30Z", "Alcaraz ATP title", "Europe"),
    ("21:40Z", "Co-op Live evac", "Europe"),
]

# Band 3: Top 3 Flagship Illustrated Lead Stories (#1-#3)
LEADS = [
    {
        "n": 1,
        "region": "Global",
        "kicker": "GLOBAL \u00b7 CLIMATE",
        "verify": "CONFIRMED",
        "art": "cop31",
        "note": "NO DEAL",
        "head": "COP31 collapses with no deal after 44h",
        "deck": "Antalya UN summit breaks down at ~09:00 UTC as EU, Panama & island states reject draft omitting fossil-fuel phaseout and adaptation finance.",
        "src": "AP, Reuters, WRI",
        "lon": 30.7,
        "lat": 36.9,
    },
    {
        "n": 2,
        "region": "Europe",
        "kicker": "EUROPE \u00b7 UKRAINE WAR",
        "verify": "CONFIRMED",
        "art": "dymer",
        "note": "11 KILLED",
        "head": "Russian strike hits Dymer block near Kyiv",
        "deck": "Drone and missile attack tears through a five-story residential building north of Kyiv, killing at least 11 as crews search rubble; drone sparks Kharkiv fire.",
        "src": "Guardian, Kyiv Ind., RFE/RL",
        "lon": 30.3,
        "lat": 50.8,
    },
    {
        "n": 3,
        "region": "M. East",
        "kicker": "M. EAST \u00b7 ENERGY & GULF",
        "verify": "OFFICIAL",
        "art": "iran_grid",
        "note": "2h CUTS",
        "head": "Iran imposes 2h cuts as Gulf tensions flare",
        "deck": "State utility Tavanir orders rolling blackouts after gas-grid hits; Bahrain confirms 2 hurt as Houthis target Saudi Rabigh refinery & Riyadh radar.",
        "src": "Tavanir, ISW, Bahrain",
        "lon": 51.4,
        "lat": 35.7,
    },
]

# Band 4: 10 Illustrated Feature Cards (#4-#13, 2 rows x 5 equal columns)
FEATURES = [
    {
        "n": 4,
        "region": "Europe",
        "kicker": "UK \u00b7 INCIDENT",
        "verify": "CONFIRMED",
        "art": "manchester_evac",
        "note": "12,000 EVAC",
        "head": "12,000 evacuated at Manchester Co-op Live",
        "deck": "Suspected tear gas halts Don Toliver concert; dozens treated for eye & breathing issues.",
        "src": "Guardian, NME",
        "lon": -2.2,
        "lat": 53.5,
    },
    {
        "n": 5,
        "region": "Asia",
        "kicker": "S. KOREA \u00b7 POLITICS",
        "verify": "CONFIRMED",
        "art": "korea_resign",
        "note": "RESIGNS",
        "head": "Education Minister Choi Kyo-jin resigns",
        "deck": "Quits amid uproar over rushed Suneung exam anti-cheating rules after AI scandal.",
        "src": "Guardian, AA",
        "lon": 127.0,
        "lat": 37.6,
    },
    {
        "n": 6,
        "region": "Europe",
        "kicker": "GERMANY \u00b7 LABOUR",
        "verify": "OFFICIAL",
        "art": "igmetall",
        "note": "19 PLANTS",
        "head": "IG Metall strikes halt 19 German plants",
        "deck": "24h warning walkouts hit metal & auto factories over wage and job-security talks.",
        "src": "Tagesschau, Reuters",
        "lon": 10.0,
        "lat": 53.5,
    },
    {
        "n": 7,
        "region": "Americas",
        "kicker": "US \u00b7 SPACE",
        "verify": "OFFICIAL",
        "art": "spacex",
        "note": "FALCON 9",
        "head": "SpaceX launches NROL-136, lands LZ-4",
        "deck": "Falcon 9 lifts off from Vandenberg, Calif., returning booster safely to coastal pad.",
        "src": "Spaceflight Now",
        "lon": -120.6,
        "lat": 34.7,
    },
    {
        "n": 8,
        "region": "Africa",
        "kicker": "SUDAN \u00b7 CONFLICT",
        "verify": "CONFIRMED",
        "art": "sudan_un",
        "note": "4 KILLED",
        "head": "RSF drones hit Khartoum UN site, kill 4",
        "deck": "Paramilitary strikes damage UN building, airport site & homes, officials say.",
        "src": "Al Jazeera, UN",
        "lon": 32.5,
        "lat": 15.6,
    },
    {
        "n": 9,
        "region": "M. East",
        "kicker": "GAZA \u00b7 AID",
        "verify": "OFFICIAL",
        "art": "gaza_storm",
        "note": "70K TENTS",
        "head": "Winter storms flood 70,000 Gaza tents",
        "deck": "Heavy rain inundates coastal displacement camps, worsening shelter & aid crisis.",
        "src": "UN, OCHA",
        "lon": 34.5,
        "lat": 31.5,
    },
    {
        "n": 10,
        "region": "Europe",
        "kicker": "TENNIS \u00b7 TURIN",
        "verify": "OFFICIAL",
        "art": "tennis_atp",
        "note": "6\u20132, 7\u20136",
        "head": "Alcaraz beats Zverev for ATP title",
        "deck": "Spaniard takes second-set tiebreak 9\u20137 to claim maiden year-end championship.",
        "src": "ATP, Al Jazeera",
        "lon": 7.7,
        "lat": 45.1,
    },
    {
        "n": 11,
        "region": "Americas",
        "kicker": "F1 \u00b7 LAS VEGAS",
        "verify": "OFFICIAL",
        "art": "vegas",
        "note": "LAS VEGAS GP",
        "head": "Verstappen wins chaotic Las Vegas GP",
        "deck": "Beats Lando Norris and Oscar Piastri under neon lights on the Strip.",
        "src": "F1, Al Jazeera",
        "lon": -115.1,
        "lat": 36.2,
    },
    {
        "n": 12,
        "region": "Europe",
        "kicker": "FOOTBALL \u00b7 UK",
        "verify": "OFFICIAL",
        "art": "anfield",
        "note": "4\u20130 ANFIELD",
        "head": "Liverpool rout 10-man Man Utd 4\u20130",
        "deck": "Szoboszlai, Wirtz, Ngumoha & Mu\u00f1oz score after Yoro red, spoiling Pochettino debut.",
        "src": "BBC, Man Utd",
        "lon": -3.0,
        "lat": 53.4,
    },
    {
        "n": 13,
        "region": "Oceania",
        "kicker": "CRICKET \u00b7 NZ",
        "verify": "OFFICIAL",
        "art": "cricket",
        "note": "720/9d",
        "head": "India declare 720/9d against New Zealand",
        "deck": "Massive first-innings total puts tourists firmly in command on day 3 in Wellington.",
        "src": "ESPN, ICC",
        "lon": 174.8,
        "lat": -41.3,
    },
]

# Band 5: 23 Single-Line Sourced Wire Dispatches (#14-#36) — 12 left + 11 right on warm archival ivory
# Dict: n, region, lead, body, src, code (O/C/R), lon, lat
WIRE = [
    {"n": 14, "region": "M. East", "lead": "Lebanon:", "body": "UNIFIL transfers southern posts to army (Dec 31)", "src": "UN/AA", "code": "O", "lon": 35.1, "lat": 33.1},
    {"n": 15, "region": "Africa", "lead": "DR Congo:", "body": "WHO warns Ituri fighting traps Ebola clinic staff", "src": "AJ/WHO", "code": "C", "lon": 30.2, "lat": 1.6},
    {"n": 16, "region": "Americas", "lead": "US House:", "body": "Final race projects 258 Dems; budget talks near", "src": "Guardian", "code": "R", "lon": -77.0, "lat": 38.9},
    {"n": 17, "region": "Americas", "lead": "US Intel:", "body": "DNI Jay Clayton defends Trump Putin remark on TV", "src": "PBS", "code": "O", "lon": -77.1, "lat": 38.9},
    {"n": 18, "region": "Americas", "lead": "US Finance:", "body": "Sec. Bessent addresses bank security glitches", "src": "CBS", "code": "O", "lon": -77.0, "lat": 38.8},
    {"n": 19, "region": "Americas", "lead": "Brazil:", "body": "Severe storm kills 5, injures 250+ in southern towns", "src": "AP", "code": "C", "lon": -53.8, "lat": -29.1},
    {"n": 20, "region": "Asia", "lead": "S. Korea:", "body": "Finance Vice Min. Lee reviews US tech selloff", "src": "MOFE", "code": "O", "lon": 127.0, "lat": 37.5},
    {"n": 21, "region": "Asia", "lead": "China:", "body": "Exchanges cut stock margin cap to 80%, filings show", "src": "Reuters", "code": "R", "lon": 121.5, "lat": 31.2},
    {"n": 22, "region": "Asia", "lead": "Indonesia:", "body": "USGS logs M5.4 quake 44 km deep NE of Bitung", "src": "USGS", "code": "O", "lon": 125.6, "lat": 1.8},
    {"n": 23, "region": "Americas", "lead": "California:", "body": "M3.3 tremor off Manhattan Beach shakes LA", "src": "USGS", "code": "O", "lon": -118.4, "lat": 33.9},
    {"n": 24, "region": "Africa", "lead": "Kenya\u2013DRC:", "body": "Nairobi & Kinshasa restore full diplomatic ties", "src": "Reuters", "code": "C", "lon": 36.8, "lat": -1.3},
    {"n": 25, "region": "Europe", "lead": "Poland:", "body": "11-nation Coalition drills conclude in SE Poland", "src": "PAP", "code": "O", "lon": 22.0, "lat": 50.0},
    {"n": 26, "region": "Asia", "lead": "Bangladesh:", "body": "Garment wage clashes shut plants near Dhaka", "src": "Reuters", "code": "C", "lon": 90.4, "lat": 24.0},
    {"n": 27, "region": "Global", "lead": "Markets:", "body": "Bitcoin near $59.2K; Brent crude holds $92/bbl", "src": "Reuters", "code": "C", "lon": None, "lat": None},
    {"n": 28, "region": "Asia", "lead": "Taiwan:", "body": "'We Are Born Good' wins 63rd Golden Horse prize", "src": "AFP", "code": "O", "lon": 121.5, "lat": 25.0},
    {"n": 29, "region": "Asia", "lead": "Japan:", "body": "Onosato wins Kyushu Grand Sumo Emperor's Cup", "src": "NHK", "code": "O", "lon": 130.4, "lat": 33.6},
    {"n": 30, "region": "Oceania", "lead": "Australia:", "body": "Federal inquiry opens into online peptide sales", "src": "ABC", "code": "O", "lon": 149.1, "lat": -35.3},
    {"n": 31, "region": "Global", "lead": "Science:", "body": "LIGO catalogs 257 silent black-hole merger events", "src": "Caltech", "code": "O", "lon": -118.1, "lat": 34.1},
    {"n": 32, "region": "Americas", "lead": "Health:", "body": "UPenn links EFEMP1 gene variant to vision loss", "src": "UPenn", "code": "O", "lon": -75.2, "lat": 40.0},
    {"n": 33, "region": "M. East", "lead": "US\u2013Iran:", "body": "Trump says he seeks permanent Iran nuclear pact", "src": "AA", "code": "O", "lon": 51.4, "lat": 35.7},
    {"n": 34, "region": "M. East", "lead": "Iraq:", "body": "Asian bodybuilding gold medalist Sajad Jawad dies, 30", "src": "AJ", "code": "R", "lon": 44.4, "lat": 33.3},
    {"n": 35, "region": "Americas", "lead": "NBA:", "body": "New York Knicks beat Indiana Pacers 113\u2013106 Sunday", "src": "NBA", "code": "O", "lon": -74.0, "lat": 40.7},
    {"n": 36, "region": "Americas", "lead": "US Health:", "body": "Lawmakers file Native Health & Wellness Act", "src": "NNO", "code": "R", "lon": -77.0, "lat": 38.9},
]

DATE_CHECK_SAT = (
    "Left out on purpose \u2014 Sat 21 Nov or earlier: BepiColombo Mercury burn \u00b7 Peru M6.7 & Banda Sea M6.8 quakes \u00b7 "
    "Banten candy-factory fire start \u00b7 Sparta II ship fire \u00b7 El Chapo Isidro raid \u00b7 EU\u2013Indonesia trade pact \u00b7 "
    "UN killer-robot talks \u00b7 Nigeria funeral boat \u00b7 Friday Wall St close."
)
DATE_CHECK_MON = (
    "Not yet (Mon 23 Nov): Spain Puigdemont amnesty \u00b7 EU \u20ac7.9B Ukraine tranche \u00b7 Belgium national air strike \u00b7 "
    "Europe school bomb-threat hoaxes."
)


def all_stories():
    return LEADS + FEATURES + WIRE


def total_stories():
    return len(all_stories())


def region_counts():
    counts = {r: 0 for r in REGION_ORDER}
    for s in all_stories():
        counts[s["region"]] += 1
    return counts


def check():
    assert len(LEADS) == 3
    assert len(FEATURES) == 10
    assert len(WIRE) == 23
    assert total_stories() == 36
    assert [s["n"] for s in all_stories()] == list(range(1, 37))
    counts = region_counts()
    assert sum(counts.values()) == 36
    for r in REGION_ORDER:
        assert counts[r] >= 2, f"low coverage for {r}: {counts[r]}"
    # Strictly forbid Merkury/Benghazi anywhere (even DATE CHECK), and forbid Banten/Sat-21 items in stories 1-36
    all_blob = (
        " ".join(
            [s["head"] + " " + s["deck"] for s in LEADS + FEATURES]
            + [w["lead"] + " " + w["body"] for w in WIRE]
            + [DATE_CHECK_SAT, DATE_CHECK_MON]
        ).lower()
    )
    for never_any in ("merkury", "benghazi"):
        assert never_any not in all_blob, f"forbidden token anywhere: {never_any}"
    story_blob = " ".join(
        [s["head"] + " " + s["deck"] for s in LEADS + FEATURES]
        + [w["lead"] + " " + w["body"] for w in WIRE]
    ).lower()
    for excluded in ("banten", "bepicolombo", "sparta ii", "puigdemont", "tajikistan", "nc call", "supercell"):
        assert excluded not in story_blob, f"excluded prior/next-day token in stories: {excluded}"


if __name__ == "__main__":
    check()
    print(f"OK: {total_stories()} verified Sunday 22 Nov 2026 stories | {region_counts()}")
