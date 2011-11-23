import json
import os.path
import StringIO
import textwrap
import unittest

import mock

from cardboard.card import Card
from cardboard.db import decks as d


class TestDeck(unittest.TestCase):

    deck = {
        "name" : "Foo Deck",
        "cards" : {"Foo" : 3, "Bar" : 2, "Baz" : 4, "Quux" : 1},
        "sideboard" : {"Spam" : 1, "Eggs" : 1},
    }

    def test_parse(self):
        s = textwrap.dedent(
        """
        2 Foo
        4 Baz
        2 Quux
        2 Foo Bar
        16 Spam Eggs
        Sideboard
        1 Hey
        2 Bla
        2 Foo
        """
        )

        self.assertEqual(d.parse(s), {
            "name" : None,
            "cards" : {
                "Foo" : 2, "Baz" : 4, "Quux" : 2,
                "Foo Bar" : 2, "Spam Eggs" : 16,
            },
            "sideboard" : {
                "Hey" : 1, "Bla" : 2, "Foo" : 2,
            },
        })

    def test_load(self):
        c = StringIO.StringIO(json.dumps(self.deck))
        self.assertEqual(d.load(from_file=c), self.deck)

        # loading from default directory
        with mock.patch("cardboard.db.decks.open", create=True) as mock_open:
            mock_open.return_value = StringIO.StringIO(c.getvalue())

            with mock.patch("cardboard.db.decks.USER_DATA", "bar"):
                self.assertEqual(d.load("foo"), self.deck)

        path = os.path.join("bar", "Decks", "foo.deck")
        mock_open.assert_called_once_with(path)

        self.assertRaises(TypeError, d.load)

    def test_save(self):
        to = StringIO.StringIO()
        cards = [mock.Mock(spec=Card) for _ in range(10)]
        names = ["Foo"] * 3 + ["Bar"] * 2 + ["Baz"] * 4 + ["Quux"]

        sideboard = mock.Mock(), mock.Mock()
        sideboard[0].name, sideboard[1].name = "Spam", "Eggs"

        for card, name in zip(cards, names):
            card.name = name

        d.save("Foo Deck", cards, sideboard, to)
        from_file = StringIO.StringIO(to.getvalue())
        self.assertEqual(d.load(from_file=from_file), self.deck)

        # saving to default directory
        with mock.patch("cardboard.db.decks.open", create=True) as mock_open:
            mock_open.return_value = mock.MagicMock(spec=file)
            mock_open.return_value.__enter__.return_value = StringIO.StringIO()

            with mock.patch("cardboard.db.decks.USER_DATA", "bar"):
                d.save("Foo Deck", cards, sideboard)
                to = mock_open.return_value.__enter__.return_value
                from_file = StringIO.StringIO(to.getvalue())

        self.assertEqual(d.load(from_file=from_file), self.deck)
        path = os.path.join("bar", "Decks", "Foo Deck.deck")
        mock_open.assert_called_once_with(path, "w")
