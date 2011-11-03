import unittest

import mock

from cardboard import types, exceptions as exc
from cardboard.db import models as m


class TestAbility(unittest.TestCase):
    def test_repr(self):
        a = m.Ability(description="Does stuff.")
        self.assertEqual(repr(a), "<Ability Model: Does stuff.>")

        s = ("Dum dah dahhh, dah nahhh, dah nahhhh. Ba dum dah dahhhh, da dahh"
             "da dahhh, da dahhh. Ba da ba da padah rdah dah HEY da na na nah")

        b = m.Ability(description=s)
        self.assertEqual(repr(b), "<Ability Model: {:.50} ... >".format(s))


class TestCard(unittest.TestCase):
    def test_repr(self):
        c = m.Card(name="Test Card")
        self.assertEqual(repr(c), "<Card Model: Test Card>")

    def test_init(self):
        d = dict(
            name="Card", mana_cost="UUWB", power="2", toughness="4", loyalty=4
        )

        c = m.Card(**d)

        for k, v in d.iteritems():
            self.assertEqual(getattr(c, k), v)


class TestDeck(unittest.TestCase):
    def test_repr(self):
        d = m.Deck(name="Test", cards=[])
        self.assertEqual(repr(d), "<Deck Model: Test>")

    def test_init(self):
        c = m.Card()
        d = m.Deck(name="Test", cards=[c])
        self.assertEqual(d.name, "Test")
        self.assertEqual(d.cards, [c])


class TestDeckAppearance(unittest.TestCase):
    def test_repr(self):
        c = m.Card(name="Test Card")
        d = m.Deck(name="Test Deck")
        a = m.DeckAppearance(c, d, 2)
        self.assertEqual(repr(a), "<Test Deck: Test Card (2)>")

    def test_init(self):
        c = m.Card(name="Test Card")
        d = m.Deck(name="Test Deck")
        a = m.DeckAppearance(c, d, 3)

        self.assertEqual(a.card, c)
        self.assertEqual(a.deck, d)
        self.assertEqual(a.quantity, 3)


class TestSet(unittest.TestCase):
    def test_repr(self):
        s = m.Set(name="Test", code="TE")
        self.assertEqual(repr(s), "<Set Model: Test>")

    def test_init(self):
        s = m.Set(name="Test", code="TE")
        self.assertEqual(s.name, "Test")
        self.assertEqual(s.code, "TE")


class TestSetAppearance(unittest.TestCase):
    def test_repr(self):
        c = m.Card(name="Test Card")
        s = m.Set(name="Test Set", code="TE")
        a = m.SetAppearance(card=c, set=s, rarity="C")
        self.assertEqual(repr(a), "<Test Card (TE-C)>")

    def test_init(self):
        c = m.Card(name="Test Card")
        s = m.Set(name="Test Set", code="TE")
        a = m.SetAppearance(card=c, set=s, rarity="R")

        self.assertEqual(a.card, c)
        self.assertEqual(a.set, s)
        self.assertEqual(a.rarity, "R")

    def test_invalid_rarity(self):
        pass


class TestType(unittest.TestCase):
    def test_repr(self):
        c = m.Type(name="Goblin")
        self.assertEqual(repr(c), "<Type Model: Goblin>")


class TestSupertype(unittest.TestCase):
    def test_repr(self):
        c = m.Supertype(name="Goblin")
        self.assertEqual(repr(c), "<Supertype Model: Goblin>")


class TestSubtype(unittest.TestCase):
    def test_repr(self):
        c = m.Subtype(name="Goblin")
        self.assertEqual(repr(c), "<Subtype Model: Goblin>")
