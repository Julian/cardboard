from StringIO import StringIO
import codecs
import itertools
import unittest

import mock

from cardboard import types
from cardboard.db import populate as p


class TestParser(unittest.TestCase):
    def test_parse(self):
        examples = [
            [u"WUG", u"Instant", u"Foo", u"UG-R"],
            [u"RG", u"Enchantment", u"Bar", u"ST-C"],
            [u"BR", u"Sorcery", u"Foo", u"Bar", u"Baz", u"UG-R"],
            [u"10GGG", u"Creature", u"1/1", u"Bar", u"UG-R, US-U, ST-C"],
            [u"1G", u"Creature", u"2/*", u"ST-C"],
            [u"Land", u"Do something.", u"US-C"],
            [u"Land", u"US-C"],
            [u"Basic Land", u"Do something.", u"US-C"],
            [u"1WU", u"Planeswalker", u"3", u"Bar", u"Baz", u"ST-C"],
            [u"Legendary Land Creature", u"1/1", u"Baz", u"US-U"],

            # subtypes are a bit stupid. Rule 205.3b and c mean that whether a
            # card has multiple types decides if each subtype is correlated to
            # the type or not (see the rules for examples)
            [u"U", u"Artifact Creature -- Foo", u"*/*", u"Baz", u"US-U"],
            [u"0", u"Artifact -- Thing", u"Bar", u"US-U"],
            [u"2", u"Legendary Enchantment -- Aura", u"SS-R"],
            [u"3", u"Artifact -- Other Thing", u"US-U"],
            [u"Land Creature -- Foo Bar", u"2/1+*", u"US-U"],

        ]

        answers = [
            {
                u"mana_cost" : u"WUG", u"types" : {u"Instant"},
                u"abilities" : [u"Foo"], u"appearances" : {(u"UG", u"R")}
            },

            {
                u"mana_cost" : u"RG", u"types" : {u"Enchantment"},
                u"abilities" : [u"Bar"], u"appearances" : {(u"ST", u"C")},
            },

            {
                u"mana_cost" : u"BR", u"types" : {u"Sorcery"},
                u"abilities" : [u"Foo", u"Bar", u"Baz"],
                u"appearances" : {(u"UG", u"R")}
            },

            {
                u"mana_cost" : u"10GGG", u"types" : {u"Creature"},
                u"power" : u"1", u"toughness" : u"1", u"abilities" : [u"Bar"],
                u"appearances" : {(u"UG", u"R"), (u"US", u"U"), (u"ST", u"C")}
            },

            {
                u"mana_cost" : u"1G", u"types" : {u"Creature"},
                u"power" : u"2", u"toughness" : u"*",
                u"appearances" : {(u"ST", u"C")}
            },

            {
                u"types" : {u"Land"}, u"abilities" : [u"Do something."],
                u"appearances" : {(u"US", u"C")}
            },

            {
                u"types" : {u"Land"}, u"appearances" : {(u"US", u"C")}
            },

            {
                u"supertypes" : {u"Basic"}, u"types" : {u"Land"},
                u"abilities" : [u"Do something."],
                u"appearances" : {(u"US", u"C")}
            },

            {
                u"mana_cost" : u"1WU", u"types" : {u"Planeswalker"},
                u"loyalty" : u"3", u"abilities" : [u"Bar", u"Baz"],
                u"appearances" : {(u"ST", u"C")}
            },

            {
                u"supertypes" : {u"Legendary"}, u"abilities" : [u"Baz"],
                u"types" : {u"Land", u"Creature"}, u"power" : u"1",
                u"toughness" : u"1", u"appearances" : {(u"US", u"U")}
            },

            {
                u"mana_cost" : u"U", u"types" : {u"Artifact", u"Creature"},
                u"power" : u"*", u"toughness" : u"*", u"abilities" : [u"Baz"],
                u"subtypes" : {u"Foo"}, u"appearances" : {(u"US", u"U")}
            },

            {
                u"mana_cost" : u"0", u"types" : {u"Artifact"},
                u"subtypes" : {u"Thing"}, u"abilities" : [u"Bar"],
                u"appearances" : {(u"US", u"U")}
            },

            {
                u"mana_cost" : u"2", u"supertypes" : {u"Legendary"},
                u"types" : {u"Enchantment"}, u"appearances" : {(u"SS", u"R")},
                u"subtypes" : {u"Aura"},
            },

            {
                u"mana_cost" : u"3", u"types" : {u"Artifact"},
                u"subtypes" : {u"Other", u"Thing"},
                u"appearances" : {(u"US", u"U")}
            },

            {
                u"types" : {u"Land", u"Creature"}, u"power" : "2",
                u"toughness" : "1+*", u"subtypes" : {u"Foo", u"Bar"},
                u"appearances" : {(u"US", u"U")}
            },

        ]

        defaults = {
            u"types" : set(), u"supertypes" : set(), u"subtypes" : set(),
            u"appearances" : set(), u"abilities" : [],

            u"mana_cost" : None, u"loyalty" : None, u"power" : None,
            u"toughness" : None,

            u"name" : u"Test Card",
        }

        for example, answer in itertools.izip_longest(examples, answers):
            expected = dict(defaults)
            expected.update(answer)
            self.assertEqual(p.parse([u"Test Card"] + example), expected)

    def test_parse_ignore(self):
        for type in types.unimplemented:
            self.assertIsNone(p.parse([u"Test", u"UU", type, u"TE-R"]))

    def test_load_cards(self):
        fbb = [u"Foo", u"Bar", u"Baz"]

        parse = mock.mocksignature(p.parse)

        for l, f in itertools.izip_longest(p.load_cards(S, _parse=parse), fbb):
            self.assertEqual(list(parse.mock.call_args[0][0]), [f] * 3)

    def test_load_cards_default_file(self):
        codecs_open = u"cardboard.db.populate.codecs.open"

        with mock.patch(codecs_open, create=True) as m:
            m.return_value = mock.MagicMock(spec=file)
            cards = list(p.load_cards(_parse=mock.Mock()))

        m.assert_called_once_with(u"cards.txt", encoding=u"utf-8")
        self.assertTrue(m.return_value.close.called)


class LoadIntegrationTest(unittest.TestCase):
    def test_load_cards(self):
        parsed = p.load_cards(SAMPLE)

        self.assertEqual(
            next(parsed),
            {
                u"name" : u"AErathi Berserker",
                u"mana_cost" : u"2RRR",
                u"types" : {u"Creature"},
                u"subtypes" : {u"Human", u"Berserker"},
                u"supertypes" : set(),
                u"power" : u"2",
                u"toughness" : u"4",
                u"loyalty" : None,
                u"abilities" : [
                    u"Rampage 3 (Whenever this creature becomes blocked, it "
                    u"gets +3/+3 until end of turn for each creature blocking "
                    u"it beyond the first.)"
                ],
                u"appearances" : {(u"LE", u"U")},
            }
        )

        self.assertEqual(
            next(parsed),
            {
                u"name" : u"AEther Adept",
                u"mana_cost" : u"1UU",
                u"types" : {u"Creature"},
                u"subtypes" : {u"Human", u"Wizard"},
                u"supertypes" : set(),
                u"power" : u"2",
                u"toughness" : u"2",
                u"loyalty" : None,
                u"abilities" : [
                    u"When AEther Adept enters the battlefield, return target "
                    u"creature to its owner's hand."
                ],
                u"appearances" : {(u"M11", u"C"), (u"M12", u"C")},
            }
        )


S = codecs.getreader("utf-8")(StringIO(u"""
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
"""
))

SAMPLE = codecs.getreader("utf-8")(StringIO(u"""
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
))
