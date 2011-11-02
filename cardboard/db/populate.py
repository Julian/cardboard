"""
Database utitilty functions, mostly used for repopulating it.

The source for most of this is assumed to be an oracle card listing file from

    http://www.yawgatog.com/resources/oracle/

See the file cards.txt in this directory for what is (hopefully) the most
recent one.

"""

import itertools
import os.path

from cardboard import types
from cardboard.db import models, Session


DEFAULT_CARDS_FILE = os.path.join(os.path.dirname(__file__), "cards.txt")

IGNORE_TYPES = {"Plane", "Scheme", "Tribal", "Vanguard"}
TYPES = types.TYPES | IGNORE_TYPES
SET_ABBR = {
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


def parse(card_info, ignore=IGNORE_TYPES):
    """
    Parse an iterable containing the lines of a single card into a dict.

    The format of the lines should be:

        Name
        Mana Cost
        Supertype Type -- Subtype
        Abilities (one per line)
        Set Appearances (comma separated, with rarity)

    Any missing fields will be left out of the resulting information dict.

        >>> s = ["Voltaic Key",
        ...      "1",
        ...      "Artifact",
        ...      "{1}, {T}: Untap target artifact.",
        ...      "US-U, M11-U"]

        >>> parse(s) == {"name" : "Voltaic Key",
        ...              "types" : ["Artifact"],
        ...              "mana_cost" : "1",
        ...              "abilities" : ["{1}, {T}: Untap target artifact."],
        ...              "appearances" : [("US", "U"), ("M11", "U")]}
        True

    The `ignore` argument specifies card types to ignore. This function will
    return None if a card is parsed that is of an ignored type.

    """

    card = {}
    lines = iter(card_info)
    card["name"] = next(lines)
    return _parse_mana_cost(next(lines), lines, card)


def _parse_mana_cost(line, rest, card):
    # not a type line?
    if line not in TYPES and " " not in line:
        card["mana_cost"] = line
        line = next(rest)
    return _parse_type_line(line, rest, card)


def _parse_type_line(line, rest, card):
    super_and_types, _, subtypes = line.partition(" -- ")

    if subtypes:
        card["subtypes"] = subtypes.split()

    super_and_types = iter(super_and_types.split())

    for token in super_and_types:
        if token not in types.SUPERTYPES:
            super_and_types = itertools.chain([token], super_and_types)
            break
        card.setdefault("supertypes", []).append(token)
    return _parse_types(super_and_types, rest, card)


def _parse_types(card_types, rest, card):
    for type in card_types:
        if type in IGNORE_TYPES:
            return
        elif type == types.CREATURE:
            card["power"], card["toughness"] = next(rest).split("/")
        elif type == types.PLANESWALKER:
            card["loyalty"] = next(rest)

        card.setdefault("types", []).append(type)

    return _parse_rest(rest, card)


def _parse_rest(rest, card):
    rest = list(rest)
    card["appearances"] = [app.split("-") for app in rest.pop().split(", ")]

    if rest:
        card["abilities"] = rest

    return card


def _is_new_block(line):
    return line.isspace() or line.startswith("#")


def load(in_file=None, _parse=parse):
    """
    Lazily yields each parsed card from a card listing file.

    Chunks the file into blocks delimited by newlines that are parsed into
    dicts.

    """

    responsible_for_closing = False

    if in_file is None:
        responsible_for_closing = True
        in_file = open(DEFAULT_CARDS_FILE)

    for from_old_block, block in itertools.groupby(in_file, key=_is_new_block):
        if not from_old_block:
            parsed = _parse(line.rstrip() for line in block)
            if parsed is not None:
                yield parsed

    if responsible_for_closing:
        in_file.close()


def populate(using, session=None):
    if session is None:
        session = Session()

    sets = {}

    for card in using:
        appearances = card.pop("appearances")
        card = models.Card(**card)
        session.add(card)

        for set, rarity in appearances:
            set = sets.setdefault(set, models.Set(name=SET_ABBR[set], code=set))
            session.add(models.SetAppearance(card, set, rarity))

    return session
