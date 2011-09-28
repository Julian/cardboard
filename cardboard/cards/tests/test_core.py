import unittest

import mock

from cardboard import exceptions
from cardboard.cards import core as c


class TestCards(unittest.TestCase):
    def test_ability(self):
        card = mock.Mock()
        card.abilities = {"foo" : None, "bar" : c.not_implemented, "baz" : 0}

        foo, bar, baz = object(), object(), object()

        c.ability(card, "foo")(foo)
        c.ability(card, "bar")(bar)

        self.assertIs(card.abilities["foo"], foo)
        self.assertIs(card.abilities["bar"], bar)

        with self.assertRaises(ValueError):
            c.ability(card, "baz")(baz)

        # didn't modify the dict
        self.assertEqual(card.abilities["baz"], 0)

    def test_card(self):
        cards = {}

        foo = object()
        c.card("foo", destination=cards)(foo)

        self.assertIs(cards["foo"], foo)

        with self.assertRaises(ValueError):
            duplicate_foo = object()
            c.card("foo", destination=cards)(duplicate_foo)

    def test_not_implemented(self):
        with self.assertRaises(exceptions.NotImplemented):
            c.not_implemented(object())
