import unittest

import mock

from cardboard import types, exceptions as exc
from cardboard.db import models as m


class TestAbility(unittest.TestCase):
    def test_repr(self):
        a = m.Ability("Does stuff.")
        self.assertEqual(repr(a), "<Ability Model: Does stuff.>")

        s = ("Dum dah dahhh, dah nahhh, dah nahhhh. Ba dum dah dahhhh, da dahh"
             "da dahhh, da dahhh. Ba da ba da padah rdah dah HEY da na na nah")

        b = m.Ability(s)
        self.assertEqual(repr(b), "<Ability Model: {} ... >".format(s[:50]))


class TestCard(unittest.TestCase):
    def test_repr(self):
        c = m.Card("Test Card", "Creature")
        self.assertEqual(repr(c), "<Card Model: Test Card>")

    def test_init(self):
        d = dict(name="Card", type=types.CREATURE, mana_cost="UUWB",
                 abilities=["Does stuff"], subtypes=["Test"],
                 supertypes=["Thing"], power=2, toughness=4, loyalty=4)

        c = m.Card(**d)

        for k, v in d.iteritems():
            self.assertEqual(getattr(c, k), v)


class TestDeck(unittest.TestCase):
    def test_repr(self):
        d = m.Deck("Test", [])
        self.assertEqual(repr(d), "<Deck Model: Test>")

    def test_init(self):
        c = m.Card("Card", "Creature")
        d = m.Deck("Test", [c])
        self.assertEqual(d.name, "Test")
        self.assertEqual(d.cards, [c])

    def test_load(self):
        pass


class TestDeckAppearance(unittest.TestCase):
    def test_repr(self):
        c = m.Card("Test Card", "Creature")
        d = m.Deck("Test Deck")
        a = m.DeckAppearance(c, d, 2)
        self.assertEqual(repr(a), "<Test Deck: Test Card (2)>")

    def test_init(self):
        c = m.Card("Test Card", "Creature")
        d = m.Deck("Test Deck")
        a = m.DeckAppearance(c, d, 3)

        self.assertEqual(a.card, c)
        self.assertEqual(a.deck, d)
        self.assertEqual(a.quantity, 3)


class TestSet(unittest.TestCase):
    def test_repr(self):
        s = m.Set("Test", "Te")
        self.assertEqual(repr(s), "<Set Model: Test>")

    def test_init(self):
        s = m.Set("Test", "Te")
        self.assertEqual(s.name, "Test")
        self.assertEqual(s.code, "Te")

    def test_cards(self):
        c = m.Card("Card", "Creature")
        d = m.Card("Other Card", "Instant")
        s = m.Set("Test", "Te", cards=[(c, "C"), (d, "U")])

        self.assertEqual(s.cards, [c, d])

        self.assertEqual(len(s.card_appearances), 2)
        self.assertEqual(s.card_appearances[0].rarity, "C")
        self.assertEqual(s.card_appearances[1].rarity, "U")


class TestSetAppearance(unittest.TestCase):
    def test_repr(self):
        c = m.Card("Test Card", "Creature")
        s = m.Set("Test Set", "Te")
        a = m.SetAppearance(c, s, "C")
        self.assertEqual(repr(a), "<Test Card (Te-C)>")

    def test_init(self):
        c = m.Card("Test Card", "Creature")
        s = m.Set("Test Set", "Te")
        a = m.SetAppearance(c, s, "R")

        self.assertEqual(a.card, c)
        self.assertEqual(a.set, s)
        self.assertEqual(a.rarity, "R")

    def test_invalid_rarity(self):
        pass


class TestSubtype(unittest.TestCase):
    def test_repr(self):
        c = m.Subtype("Goblin")
        self.assertEqual(repr(c), "<Subtype Model: Goblin>")
