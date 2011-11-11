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
from cardboard.db import models as m, Session, get_or_create


DEFAULT_CARDS_FILE = "cards.txt"

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


def parse(card_info):
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

    Returns None if a card is parsed that is of an unimplemented type.

    """

    card = dict(
        types=[], supertypes=[], subtypes=[], appearances=[], abilities=[],
        mana_cost=None, loyalty=None, power=None, toughness=None,
    )

    lines = iter(card_info)
    card["name"] = next(lines)
    return _parse_mana_cost(next(lines), lines, card)


def _parse_mana_cost(line, rest, card):
    # not a type line?
    if line not in types.all | types.unimplemented and " " not in line:
        card["mana_cost"] = line
        line = next(rest)
    return _parse_type_line(line, rest, card)


def _parse_type_line(line, rest, card):
    super_and_types, _, subtypes = line.partition(" -- ")

    if subtypes:
        card["subtypes"] = subtypes.split()

    super_and_types = iter(super_and_types.split())

    for token in super_and_types:
        if token not in types.supertypes:
            super_and_types = itertools.chain([token], super_and_types)
            break
        card["supertypes"].append(token)
    return _parse_types(super_and_types, rest, card)


def _parse_types(card_types, rest, card):
    for type in card_types:
        if type in types.unimplemented:
            return
        elif type == types.creature:
            card["power"], card["toughness"] = next(rest).split("/")
        elif type == types.planeswalker:
            card["loyalty"] = next(rest)

        card["types"].append(type)

    return _parse_rest(rest, card)


def _parse_rest(rest, card):
    rest = list(rest)
    card["appearances"] = [app.split("-") for app in rest.pop().split(", ")]

    if rest:
        card["abilities"] = rest

    return card


def _is_new_block(line):
    return line.isspace() or line.startswith("#")


def load_cards(in_file=None, _parse=parse):
    """
    Lazily yields each parsed card from a card listing file.

    Chunks the file into blocks delimited by newlines that are parsed into
    dicts.

    """

    responsible_for_closing = False

    if in_file is None:
        in_file = open(DEFAULT_CARDS_FILE)
        responsible_for_closing = True

    for from_old_block, block in itertools.groupby(in_file, key=_is_new_block):
        if not from_old_block:
            parsed = _parse(line.rstrip() for line in block)
            if parsed is not None:
                yield parsed

    if responsible_for_closing:
        in_file.close()


def populate(cards_info):
    """
    Populate the database using a collection of cards.

    cards_info: an iterable of dict-like objects in the format returned by
                `parse` each containing the information about a given card

    """

    s = Session()

    for card in cards_info:
        appearances = card.pop("appearances")

        card["types"] = [s.query(m.Type).get(name) for name in card["types"]]
        card["supertypes"] = [
            s.query(m.Supertype).get(name) for name in card["supertypes"]
        ]

        # TODO: this is slightly borked in theory due to needing to match type
        card["subtypes"] = [
            s.query(m.Subtype).get((name, next(iter(card["types"])).name))
            for name in card["subtypes"]
        ]

        card = m.Card(**card)
        s.add(card)

        card.sets.extend(
            (s.query(m.Set).get(set), rarity) for set, rarity in appearances
        )

    s.commit()


def populate_fixtures():
    """
    Populate the tables in the db that contain static data.

    """

    s = Session()

    s.add_all(m.Set(code=c, name=n) for n, c in SET_ABBR.iteritems())

    s.add_all(m.Type(name=type) for type in types.all)
    s.add_all(m.Supertype(name=supertype) for supertype in types.supertypes)

    for type in types.all:
        s.add_all(
            m.Subtype(name=subtype, type_name=type)
            for subtype in types.subtypes[type]
        )

    s.commit()
