import unittest

import mock

from cardboard import exceptions
from cardboard.cards import core as c


class TestCards(unittest.TestCase):
    def test_card(self):
        cards = {}

        foo = object()
        c.card("foo", destination=cards)(foo)

        self.assertIs(cards["foo"], foo)

        with self.assertRaises(ValueError):
            duplicate_foo = object()
            c.card("foo", destination=cards)(duplicate_foo)
