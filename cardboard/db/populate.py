"""
Database utitilty functions, mostly used for repopulating it.

The source for most of this is assumed to be an oracle card listing file from

    http://www.yawgatog.com/resources/oracle/

See the file cards.txt in this directory for what is (hopefully) the most
recent one.

"""

import codecs
import itertools

from cardboard import types
from cardboard.db import models as m, Session


DEFAULT_CARDS_FILE = "cards.txt"
SET_ABBR = {
        u"A" : u"Limited Edition Alpha",
        u"B" : u"Limited Edition Beta",
        u"U" : u"Unlimited",
        u"RV" : u"Revised",
        u"4E" : u"Fourth Edition",
        u"5E" : u"Fifth Edition",
        u"6E" : u"Classic (Sixth Edition)",
        u"7E" : u"Seventh Edition",
        u"8ED" : u"Core Set - Eighth Edition",
        u"9ED" : u"Core Set - Ninth Edition",
        u"10E" : u"Core Set - Tenth Edition",

        u"M10" : u"Magic 2010",
        u"M11" : u"Magic 2011",
        u"M12" : u"Magic 2012",

        u"AN" : u"Arabian Nights",
        u"AQ" : u"Antiquities",
        u"LE" : u"Legends",
        u"DK" : u"The Dark",
        u"FE" : u"Fallen Empires",
        u"HL" : u"Homelands",

        u"IA" : u"Ice Age",
        u"AI" : u"Alliances",
        u"CSP" : u"Coldsnap",

        u"MI" : u"Mirage",
        u"VI" : u"Visions",
        u"WL" : u"Weatherlight",

        u"TE" : u"Tempest",
        u"ST" : u"Stronghold",
        u"EX" : u"Exodus",

        u"US" : u"Urza's Saga",
        u"UL" : u"Urza's Legacy",
        u"UD" : u"Urza's Destiny",

        u"MM" : u"Mercadian Masques",
        u"NE" : u"Nemesis",
        u"PR" : u"Prophecy",

        u"IN" : u"Invasion",
        u"PS" : u"Planeshift",
        u"AP" : u"Apocalypse",

        u"OD" : u"Odyssey",
        u"TOR" : u"Torment",
        u"JUD" : u"Judgement",

        u"ONS" : u"Onslaught",
        u"LGN" : u"Legion",
        u"SCG" : u"Scourge",

        u"MRD" : u"Mirrodin",
        u"DST" : u"Darksteel",
        u"5DN" : u"Fifth Dawn",

        u"CHK" : u"Champions of Kamigawa",
        u"BOK" : u"Betrayers of Kamigawa",
        u"SOK" : u"Saviors of Kamigawa",

        u"RAV" : u"Ravnica: City of Guilds",
        u"GPT" : u"Guildpact",
        u"DIS" : u"Dissension",

        u"TSP" : u"Time Spiral",
        u"PLC" : u"Planar Chaos",
        u"FUT" : u"Future Sight",

        u"LRW" : u"Lorwyn",
        u"MOR" : u"Morningtide",

        u"SHM" : u"Shadowmoor",
        u"EVE" : u"Eventide",

        u"ALA" : u"Shards of Alara",
        u"CON" : u"Conflux",
        u"ARB" : u"Alara Reborn",

        u"ZEN" : u"Zendikar",
        u"WWK" : u"Worldwake",
        u"ROE" : u"Rise of the Eldrazi",

        u"SOM" : u"Scars of Mirrodin",
        u"MBS" : u"Mirrodin Besieged",
        u"NPH" : u"New Phyrexia",

        u"ARC" : u"Archenemy",
        u"CH" : u"Chronicles",
        u"CMD" : u"Commander",
        u"HOP" : u"Planechase",
        u"PROMO" : u"Media Inserts",
        u"S99" : u"Starter 1999",
        u"S00" : u"Starter 2000",

        u"P1" : u"Portal",
        u"P2" : u"Portal Second Age",
        u"P3K" : u"Portal Three Kingdoms",

        }
TYPES = types.all | types.unimplemented


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

        >>> s = [u"Voltaic Key",
        ...      u"1",
        ...      u"Artifact",
        ...      u"{1}, {T}: Untap target artifact.",
        ...      u"US-U, M11-U"]

        >>> parse(s) == {u"name" : u"Voltaic Key",
        ...              u"types" : [u"Artifact"],
        ...              u"mana_cost" : u"1",
        ...              u"abilities" : [u"{1}, {T}: Untap target artifact."],
        ...              u"appearances" : [(u"US", u"U"), (u"M11", u"U")]}
        True

    Returns None if a card is parsed that is of an unimplemented type.

    """

    card = {
        u"types" : set(), u"supertypes" : set(), u"subtypes" : set(),
        u"appearances" : set(), u"abilities" : [], u"mana_cost" : None,
        u"loyalty" : None, u"power" : None, u"toughness" : None,
    }

    lines = iter(card_info)
    card[u"name"] = next(lines)
    return _parse_mana_cost(next(lines), lines, card)


def _parse_mana_cost(line, rest, card):
    # not a type line?
    if line not in TYPES and " " not in line:
        card[u"mana_cost"] = line
        line = next(rest)
    return _parse_type_line(line, rest, card)


def _parse_type_line(line, rest, card):
    supertypes, _, subtypes = line.partition(u" -- ")
    supertypes, sepyt, subtypes = supertypes.split(), [], subtypes.split()

    for type in reversed(supertypes):
        if type not in TYPES:
            break
        elif type in types.unimplemented:
            return
        elif type == types.creature:
            card[u"power"], card[u"toughness"] = next(rest).split(u"/")
        elif type == types.planeswalker:
            card[u"loyalty"] = next(rest)
        sepyt.append(supertypes.pop())

    card[u"supertypes"] = set(supertypes)
    card[u"types"] = set(sepyt)
    card[u"subtypes"] = set(subtypes)

    return _parse_rest(rest, card)


def _parse_rest(rest, card):
    r = list(rest)
    card[u"appearances"] = {tuple(a.split(u"-")) for a in r.pop().split(u", ")}
    card[u"abilities"] = r
    return card


def _is_new_block(line):
    return line.isspace() or line.startswith(u"#")


def load_cards(in_file=None, _parse=parse):
    """
    Lazily yields each parsed card from a card listing file.

    Chunks the file into blocks delimited by newlines that are parsed into
    dicts.

    `in_file` is the sole public argument and should be a `codecs.open` wrapped
    file (or some other file-like object) yielding unicode lines. The default
    is to look for a cards file in the `DEFAULT_CARDS_FILE` location.

    """

    responsible_for_closing = False

    if in_file is None:
        in_file = codecs.open(DEFAULT_CARDS_FILE, encoding="utf-8")
        responsible_for_closing = True

    for from_old_block, block in itertools.groupby(in_file, key=_is_new_block):
        if not from_old_block:
            parsed = _parse(line.rstrip() for line in block)
            if parsed is not None:
                yield parsed

    if responsible_for_closing:
        in_file.close()


def populate(cards_info, session=Session):
    """
    Populate the database using a collection of cards.

    cards_info: an iterable of dict-like objects in the format returned by
                `parse` each containing the information about a given card

    """

    s = session()

    sts = itertools.chain.from_iterable(types.subtypes.itervalues())

    sets = {c : m.Set(code=c, name=n) for c, n in SET_ABBR.iteritems()}

    types_ = {type : m.Type(name=type) for type in types.all}
    supertypes = {st : m.Supertype(name=st) for st in types.supertypes}
    subtypes = {st : m.Subtype(name=st) for st in sts}

    s.add_all(
        itertools.chain.from_iterable(
            i.itervalues() for i in (sets, types_, supertypes, subtypes)
        )
    )

    for card in cards_info:
        # XXX: Split cards / Stupid multiple ability
        if " // " in card[u"name"] or card[u"name"] == u"Seeds of Strength":
            continue

        t, u, v = (card.pop(k) for k in [u"supertypes", u"types", u"subtypes"])

        card[u"ability_objects"] = [
            s.query(m.Ability).filter_by(description=d).first() or
            m.Ability(description=d) for d in card.pop(u"abilities")
        ]

        card[u"supertype_objects"] = {supertypes[st] for st in t}
        card[u"type_objects"] = {types_[type] for type in u}
        card[u"subtype_objects"] = {subtypes[st] for st in v}

        appearances = {
            m.SetAppearance(set=sets[set], rarity=rarity)
            for set, rarity in card.pop(u"appearances")
        }

        card = m.Card(**card)
        card.set_appearances.update(appearances)

        s.add(card)

    s.commit()
