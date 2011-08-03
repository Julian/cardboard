from collections import deque

from cardboard import db

CARD_TYPES = {"Land", "Creature", "Enchantment", "Instant", "Sorcery",
              "Artifact", "Planeswalker", "Scheme", "Vanguard", "Plane"}

ABBR = {
        "A" : "Limited Edition Alpha",
        "B" : "Limited Edition Beta",
        "U" : "Unlimited",
        "RV" : "Revised",
        "4E" : "Fourth Edition",
        "5E" : "Fifth Edition",
        "6E" : "Classic (Sixth Edition)",
        "7E" : "Seventh Edition",
        "8ED" : "Core Set - Eighth Edition",
        "9ED" : "Core Set - Ninth Edition",
        "10E" : "Core Set - Tenth Edition",

        "M10" : "Magic 2010",
        "M11" : "Magic 2011",
        "M12" : "Magic 2012",

        "AN" : "Arabian Nights",
        "AQ" : "Antiquities",
        "LE" : "Legends",
        "DK" : "The Dark",
        "FE" : "Fallen Empires",
        "HL" : "Homelands",

        "IA" : "Ice Age",
        "AI" : "Alliances",
        "CSP" : "Coldsnap",

        "MI" : "Mirage",
        "VI" : "Visions",
        "WL" : "Weatherlight",

        "TE" : "Tempest",
        "ST" : "Stronghold",
        "EX" : "Exodus",

        "US" : "Urza's Saga",
        "UL" : "Urza's Legacy",
        "UD" : "Urza's Destiny",

        "MM" : "Mercadian Masques",
        "NE" : "Nemesis",
        "PR" : "Prophecy",

        "IN" : "Invasion",
        "PS" : "Planeshift",
        "AP" : "Apocalypse",

        "OD" : "Odyssey",
        "TOR" : "Torment",
        "JUD" : "Judgement",

        "ONS" : "Onslaught",
        "LGN" : "Legion",
        "SCG" : "Scourge",

        "MRD" : "Mirrodin",
        "DST" : "Darksteel",
        "5DN" : "Fifth Dawn",

        "CHK" : "Champions of Kamigawa",
        "BOK" : "Betrayers of Kamigawa",
        "SOK" : "Saviors of Kamigawa",

        "RAV" : "Ravnica: City of Guilds",
        "GPT" : "Guildpact",
        "DIS" : "Dissension",

        "TSP" : "Time Spiral",
        "PLC" : "Planar Chaos",
        "FUT" : "Future Sight",

        "LRW" : "Lorwyn",
        "MOR" : "Morningtide",

        "SHM" : "Shadowmoor",
        "EVE" : "Eventide",

        "ALA" : "Shards of Alara",
        "CON" : "Conflux",
        "ARB" : "Alara Reborn",

        "ZEN" : "Zendikar",
        "WWK" : "Worldwake",
        "ROE" : "Rise of the Eldrazi",

        "SOM" : "Scars of Mirrodin",
        "MBS" : "Mirrodin Besieged",
        "NPH" : "New Phyrexia",

        "ARC" : "Archenemy",
        "CH" : "Chronicles",
        "CMD" : "Commander",
        "HOP" : "Planechase",
        "PROMO" : "Media Inserts",
        "S99" : "Starter 1999",
        "S00" : "Starter 2000",

        "P1" : "Portal",
        "P2" : "Portal Second Age",
        "P3K" : "Portal Three Kingdoms",

        }

def load(f):
    """
    Parse a file containing a list of cards separated by newlines.

    """

    buffer = deque()
    for line in f:
        line = line.strip()

        if not line:
            card_dict = parse(buffer)
            if card_dict is not None:
                yield card_dict
            buffer = deque()
        else:
            buffer.append(line)

    last_one = parse(buffer)
    if last_one is not None:
        yield last_one

def parse(c):
    if not c:
        return

    card = {}
    card["name"] = c.popleft()
    card["appearances"] = [tuple(set_rarity.split("-"))
                    for set_rarity in c.pop().split(", ")]

    if not any(type in c[0] for type in CARD_TYPES):
        card["casting_cost"] = c.popleft()

    type, _, subtypes = c.popleft().partition(" -- ")

    card["type"] = type

    if subtypes:
        subtypes = subtypes.split(", ")
        card["subtypes"] = subtypes

    # Be careful with .startswith(Plane)
    if any(type.startswith(t) for t in {"Scheme", "Vanguard", "Plane "}):
        return
    elif "Creature" in type and not type.startswith("Enchant"):
        power, toughness = c.popleft().split("/")
        card["creature"] = {"power" : power, "toughness" : toughness}

    card["abilities"] = list(c)

    return card

def populate(using):
    seen = {}
    s = db.Session()

    for card in load(using):
        appearances = card.pop("appearances")
        creature = card.pop("creature", None)

        card = db.Card(**card)
        s.add(card)

        for set, rarity in appearances:
            set = seen.setdefault(set, db.Set(name=set, code=ABBR[set]))
            s.add(db.SetAppearance(card, set, rarity))

        if creature is not None:
            s.add(db.Creature(card=card, **creature))

    return s
