import unittest

from cardboard.cards import core as c

class TestCard(unittest.TestCase):
    def test_card(self):
        cards = {}

        self.called = False

        foo = object()
        c.card("foo", destination=cards)(foo)

        self.assertIs(cards["foo"], foo)

        with self.assertRaises(ValueError):
            duplicate_foo = object()
            c.card("foo", destination=cards)(duplicate_foo)
