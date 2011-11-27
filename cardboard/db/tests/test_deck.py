import json
import os.path
import StringIO
import textwrap
import unittest

import mock

from cardboard.card import Card
from cardboard.db import deck as d


class TestDeck(unittest.TestCase):

    deck = {
        u"cards" : {u"FOO" : 3, u"BAR" : 2, u"BAZ" : 4, u"QUUX" : 1},
        u"sideboard" : {u"SPAM" : 1, u"EGGS" : 1},
    }

    apprentice = textwrap.dedent(
    u"""
    // A comment
    4 Baz
    2 Foo
    2 Foo Bar
    16 Spam Eggs

    SB: 2 Bla
    SB: 2 Foo
    SB: 1 Hey
    """
    ).strip()

    mtgo = textwrap.dedent(
    u"""
    4 Baz
    2 Foo
    2 Foo Bar
    16 Spam Eggs

    Sideboard
    2 Bla
    2 Foo
    1 Hey
    """
    ).strip("\n")

    export_deck = {
        u"cards" : {
            u"Foo" : 2, u"Baz" : 4, u"Foo Bar" : 2, u"Spam Eggs" : 16,
        },
        u"sideboard" : {
            u"Hey" : 1, u"Bla" : 2, u"Foo" : 2,
        },
    }

    export_deck_loaded = {
        u"cards" : {
            k.upper() : v for k, v in export_deck[u"cards"].iteritems()
        },
        u"sideboard" : {
            k.upper() : v for k, v in export_deck[u"sideboard"].iteritems()
        },
    }

    def setUp(self):
        super(TestDeck, self).setUp()
        # mock out the database queries
        self.query_patch = mock.patch.object(d.DBCard, "query")
        self.query = self.query_patch.start()
        self.query.get.side_effect = lambda name : name.upper()

    def tearDown(self):
        self.query_patch.stop()

    def test_from_cards(self):
        cards = [mock.Mock(spec=Card) for _ in range(10)]
        names = [u"FOO"] * 3 + [u"BAR"] * 2 + [u"BAZ"] * 4 + [u"QUUX"]

        sideboard = mock.Mock(), mock.Mock()
        sideboard[0].name, sideboard[1].name = u"SPAM", u"EGGS"

        for card, name in zip(cards, names):
            card.name = name

        deck = d.from_cards(cards=cards, sideboard=sideboard)
        self.assertEqual(deck, self.deck)

    def test_export(self):
        mtgo = self.mtgo.splitlines()
        apprentice = self.apprentice.splitlines()[1:]  # without the comment

        self.assertEqual(list(d.export(self.export_deck, format="mtgo")), mtgo)
        self.assertEqual(
            list(d.export(self.export_deck, format="apprentice")), apprentice
        )

    def test_load(self):
        c = StringIO.StringIO(json.dumps(self.deck))
        c.name = "Foo Deck.deck"
        self.assertEqual(d.load(file=c), self.deck)

        # mtgo
        c = StringIO.StringIO(self.mtgo)
        c.name = "Foo Deck.txt"
        self.assertEqual(d.load(file=c), self.export_deck_loaded)

        # apprentice
        c = StringIO.StringIO(self.mtgo)
        c.name = "Foo Deck.dec"
        self.assertEqual(d.load(file=c), self.export_deck_loaded)

        with self.assertRaises(ValueError):
            d.load(file=c, format="invalid_thing")

    def test_save(self):
        m = mock.Mock(side_effect=lambda name : name)
        to = StringIO.StringIO()

        d.save("Foo Deck", self.deck, to)
        in_file = StringIO.StringIO(to.getvalue())
        in_file.name = "Foo Deck.deck"
        self.assertEqual(d.load(file=in_file), self.deck)

        # saving to default directory
        with mock.patch("cardboard.db.deck.open", create=True) as mock_open:
            mock_open.return_value = mock.MagicMock(spec=file)
            mock_open.return_value.__enter__.return_value = StringIO.StringIO()

            with mock.patch("cardboard.db.deck.DECKS_DIR", "bar"):
                d.save("Foo Deck", self.deck)
                to = mock_open.return_value.__enter__.return_value

        in_file = StringIO.StringIO(to.getvalue())
        in_file.name = "Foo Deck.deck"
        self.assertEqual(d.load(file=in_file), self.deck)

        path = os.path.join("bar", "Foo Deck.deck")
        mock_open.assert_called_once_with(path, "w")
