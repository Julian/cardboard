from cStringIO import StringIO
import itertools
import os.path
import unittest

import mock

import cardboard.db.populate as p


class TestParser(unittest.TestCase):
    def test_parse(self):
        examples = [
            ["WUG", "Instant", "Foo", "UG-R"],
            ["RG", "Enchantment", "Bar", "ST-C"],
            ["BR", "Sorcery", "Foo", "Bar", "Baz", "UG-R"],
            ["10GGG", "Creature", "1/1", "Bar", "UG-R, US-U, ST-C"],
            ["1G", "Creature", "2/*", "ST-C"],
            ["U", "Legendary Artifact Creature -- Foo", "*/*", "Baz", "US-U"],
            ["0", "Artifact -- Thing", "Bar", "US-U"],
            ["2", "Legendary Enchantment -- Aura", "SS-R"],
            ["3", "Artifact -- Other Thing", "US-U"],
            ["Land", "Do something.", "US-C"],
            ["Land", "US-C"],
            ["Basic Land", "Do something.", "US-C"],
            ["1WU", "Planeswalker", "3", "Bar", "Baz", "ST-C"],
        ]

        answers = [
            {
                "mana_cost" : "WUG", "types" : ["Instant"],
                "abilities" : ["Foo"], "appearances" : [["UG", "R"]]
            },

            {
                "mana_cost" : "RG", "types" : ["Enchantment"],
                "abilities" : ["Bar"], "appearances" : [["ST", "C"]]},

            {
                "mana_cost" : "BR", "types" : ["Sorcery"],
                "abilities" : ["Foo", "Bar", "Baz"],
                "appearances" : [["UG", "R"]]
            },

            {
                "mana_cost" : "10GGG", "types" : ["Creature"], "power" : "1",
                "toughness" : "1", "abilities" : ["Bar"],
                "appearances" : [["UG", "R"], ["US", "U"], ["ST", "C"]]
            },

            {
                "mana_cost" : "1G", "types" : ["Creature"], "power" : "2",
                "toughness" : "*", "appearances" : [["ST", "C"]]
            },

            {
                "mana_cost" : "U", "supertypes" : ["Legendary"],
                "types" : ["Artifact", "Creature"], "power" : "*",
                "toughness" : "*", "subtypes" : ["Foo"], "abilities" : ["Baz"],
                "appearances" : [["US", "U"]]
            },

            {
                "mana_cost" : "0", "types" : ["Artifact"],
                "subtypes" : ["Thing"], "abilities" : ["Bar"],
                "appearances" : [["US", "U"]]
            },

            {
                "mana_cost" : "2", "supertypes" : ["Legendary"],
                "types" : ["Enchantment"], "subtypes" : ["Aura"],
                "appearances" : [["SS", "R"]]
            },

            {
                "mana_cost" : "3", "types" : ["Artifact"],
                "subtypes" : ["Other", "Thing"], "appearances" : [["US", "U"]]
            },

            {
                "types" : ["Land"], "abilities" : ["Do something."],
                "appearances" : [["US", "C"]]
            },

            {
                "types" : ["Land"], "appearances" : [["US", "C"]]
            },

            {
                "supertypes" : ["Basic"], "types" : ["Land"],
                "abilities" : ["Do something."], "appearances" : [["US", "C"]]
            },

            {
                "mana_cost" : "1WU", "types" : ["Planeswalker"],
                "loyalty" : "3", "abilities" : ["Bar", "Baz"],
                "appearances" : [["ST", "C"]]
            },

        ]

        for example, answer in itertools.izip_longest(examples, answers):
            answer["name"] = "Test Card"
            self.assertEqual(p.parse(["Test Card"] + example), answer)

    def test_parse_ignore(self):
        self.assertEqual(
            p.IGNORE_TYPES, {"Plane", "Scheme", "Tribal", "Vanguard"}
        )

        for type in p.IGNORE_TYPES:
            self.assertIsNone(p.parse(["Test", "UU", type, "TE-R"]))

    def test_load(self):
        fbb = ["Foo", "Bar", "Baz"]

        parse = mock.mocksignature(p.parse)

        for l, f in itertools.izip_longest(p.load(S, _parse=parse), fbb):
            self.assertEqual(list(parse.mock.call_args[0][0]), [f] * 3)

    def test_load_default_file(self):
        with mock.patch("cardboard.db.populate.open", create=True) as m:
            m.return_value = mock.MagicMock(spec=file)
            cards = list(p.load(_parse=mock.Mock()))

        path = os.path.dirname(p.__file__)
        m.assert_called_once_with(os.path.join(path, "cards.txt"))
        self.assertTrue(m.return_value.close.called)


class LoadIntegrationTest(unittest.TestCase):
    def test_load(self):
        parsed = p.load(SAMPLE)

        self.assertEqual(
            next(parsed),
            {
                "name" : "AErathi Berserker",
                "mana_cost" : "2RRR",
                "types" : ["Creature"],
                "subtypes" : ["Human", "Berserker"],
                "power" : "2",
                "toughness" : "4",
                "abilities" : [
                    "Rampage 3 (Whenever this creature becomes blocked, it "
                    "gets +3/+3 until end of turn for each creature blocking "
                    "it beyond the first.)"
                ],
                "appearances" : [["LE", "U"]],
            }
        )

        self.assertEqual(
            next(parsed),
            {
                "name" : "AEther Adept",
                "mana_cost" : "1UU",
                "types" : ["Creature"],
                "subtypes" : ["Human", "Wizard"],
                "power" : "2",
                "toughness" : "2",
                "abilities" : [
                    "When AEther Adept enters the battlefield, return target "
                    "creature to its owner's hand."
                ],
                "appearances" : [["M11", "C"], ["M12", "C"]],
            }
        )


S = StringIO("""
# Ignore
# the
# header

Foo
Foo
Foo

# Ignore
# comment
# block

Bar
Bar
Bar

Baz
Baz
Baz
""")


SAMPLE = StringIO("""
#
# Card Listing File
#
# Source: http://www.yawgatog.com/resources/oracle/
# Last Updated: 2011-07-15

A Display of My Dark Power
Scheme
When you set this scheme in motion, until your next turn, whenever a player taps a land for mana, that player adds one mana to his or her mana pool of any type that land produced.
ARC-C

AErathi Berserker
2RRR
Creature -- Human Berserker
2/4
Rampage 3 (Whenever this creature becomes blocked, it gets +3/+3 until end of turn for each creature blocking it beyond the first.)
LE-U

AEther Adept
1UU
Creature -- Human Wizard
2/2
When AEther Adept enters the battlefield, return target creature to its owner's hand.
M11-C, M12-C
"""
)
