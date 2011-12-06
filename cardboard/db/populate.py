"""
Database utitilty functions, mostly used for repopulating it.

The source for most of this is assumed to be an oracle card listing file from

    http://www.yawgatog.com/resources/oracle/

See the file cards.txt in this directory for what is (hopefully) the most
recent one.

"""

import csv
import codecs
import datetime
import itertools
import os.path
import string
import textwrap

from cardboard import types
from cardboard.db import models as m, Session
from cardboard.util import unicode_csv_reader, sanitize


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DEFAULT_CARDS_FILE = os.path.join(DATA_DIR, "cards.txt")
DEFAULT_SETS_FILE = os.path.join(DATA_DIR, "sets.csv")
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
    is to look for a cards file in the `DEFAULT_CARDS_FILE` location. The file
    will be closed after iteration.

    """

    if in_file is None:
        in_file = codecs.open(DEFAULT_CARDS_FILE, encoding="utf-8")

    for from_old_block, block in itertools.groupby(in_file, key=_is_new_block):
        if not from_old_block:
            parsed = _parse(line.rstrip() for line in block)
            if parsed is not None:
                yield parsed

    in_file.close()


def populate(cards_info, sets_file=None, session=Session):
    """
    Populate the database using a collection of cards.

    cards_info: an iterable of dict-like objects in the format returned by
                `parse` each containing the information about a given card

    sets_file: a unicode yielding file-like object containing comma-separated
               information about the sets that are used in `cards_info`.
               If unspecified, `DEFAULT_SETS_FILE` is used. The file will be
               closed after iteration.

    """

    s = session()

    with sets_file or codecs.open(DEFAULT_SETS_FILE, encoding="utf-8") as file:
        reader = unicode_csv_reader(file, reader=csv.DictReader)
        sets = {}
        for row in reader:
            row["released"] = datetime.datetime.strptime(
                row["released"], u"%Y/%m/%d"
            )
            sets[row["code"]] = m.Set(**row)

    sts = itertools.chain.from_iterable(types.subtypes.itervalues())

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


def write_cards(to_path="sets"):
    test_path = os.path.join(to_path, "tests")

    os.mkdir(to_path)
    os.mkdir(test_path)

    open(os.path.join(to_path, "__init__.py"), "a")
    open(os.path.join(test_path, "__init__.py"), "a")

    ABIL = "def {}():\n                        return Ability.NotImplemented\n"

    IMPORTS = "\n".join([
        "from cardboard import types",
        "from cardboard.ability import (",
        "    AbilityNotImplemented, spell, activated, triggered, static",
        ")",
        "from cardboard.cards import card, common, keywords, match",
    ])

    for set in m.Set.query:
        filename = sanitize(set.name) + ".py"

        with open(os.path.join(to_path, filename), "w") as set_file:
            set_file.write(IMPORTS)

            for card in set.new_cards:
                if card.abilities:
                    name = sanitize(card.name)
                    set_file.write(
                        textwrap.dedent("""


                        @card("{card.name}")
                        def {sanitized_name}(card, abilities):
                        """.format(card=card, sanitized_name=name)
                        )
                    )

                    for ability in card.abilities:
                        set_file.write(
                            "\n    "
                            "def {}():\n    "
                            "    return AbilityNotImplemented\n".format(name)
                        )

                    set_file.write("\n    return {},".format(
                        ", ".join(name for _ in card.abilities)
                    ))

        with open(os.path.join(test_path, "test_" + filename), "w") as test:
            test.write("import mock")
