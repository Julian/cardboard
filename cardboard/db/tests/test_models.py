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

    def test_sets(self):
        c = m.Card()
        s = m.Set()
        c.sets.add(s)
        self.assertEqual(c.sets, {s})


class TestSet(unittest.TestCase):
    def test_repr(self):
        s = m.Set(name="Test", code="TE")
        self.assertEqual(repr(s), "<Set Model: Test>")

    def test_init(self):
        s = m.Set(name="Test", code="TE")
        self.assertEqual(s.name, "Test")
        self.assertEqual(s.code, "TE")

    def test_cards(self):
        s = m.Set()
        c = m.Card()
        s.cards.add(c)
        self.assertEqual(s.cards, {c})


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
        t = m.Type(name="Goblin")
        self.assertEqual(repr(t), "<Type Model: Goblin>")


class TestSupertype(unittest.TestCase):
    def test_repr(self):
        s = m.Supertype(name="Goblin")
        self.assertEqual(repr(s), "<Supertype Model: Goblin>")


class TestSubtype(unittest.TestCase):
    def test_repr(self):
        s = m.Subtype(name="Goblin")
        self.assertEqual(repr(s), "<Subtype Model: Goblin>")
