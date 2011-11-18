import unittest

import mock

from cardboard import types
from cardboard.cards import match as m


class TestMatch(unittest.TestCase):
    def test_and(self):
        c = mock.Mock()

        t = m.Match(name=u"foo") & m.is_creature

        c.name, c.types = u"" , set()
        self.assertFalse(t(c))

        c.name = u"foo"
        self.assertFalse(t(c))

        c.types.add(u"Creature")
        self.assertTrue(t(c))

        c.types.add(u"bar")
        self.assertTrue(t(c))

    def test_invert(self):
        c = mock.Mock()

        t = ~m.Match(name=u"foo")

        c.name = u"bar"
        self.assertTrue(t(c))

        c.name = u"foo"
        self.assertFalse(t(c))

    def test_or(self):
        c = mock.Mock()

        t = m.Match(lambda obj : u"Flash" in obj.abilities) | m.is_creature

        c.abilities, c.types = set() , set()
        self.assertFalse(t(c))

        c.types.add(u"Creature")
        self.assertTrue(t(c))

        c.types.remove(u"Creature")
        c.abilities.add(u"Flash")
        self.assertTrue(t(c))

        c.types.add(u"Creature")
        self.assertTrue(t(c))


class TestMatchers(unittest.TestCase):
    def test_has_types(self):
        c = mock.Mock()

        t = m.has_types("Foo")
        u = m.has_types("Foo", "Bar")

        c.types = {"Foo"}
        self.assertTrue(t(c))
        self.assertFalse(u(c))

        c.types.add("Bar")
        self.assertTrue(t(c))
        self.assertTrue(u(c))

        c.types.remove("Foo")
        self.assertFalse(t(c))
        self.assertFalse(u(c))

    def test_is_types(self):
        c = mock.Mock()
        c.types = set()

        self.assertFalse(m.is_artifact(c))
        self.assertFalse(m.is_creature(c))
        self.assertFalse(m.is_enchantment(c))
        self.assertFalse(m.is_instant(c))
        self.assertFalse(m.is_land(c))
        self.assertFalse(m.is_planeswalker(c))
        self.assertFalse(m.is_sorcery(c))

        c.types.update(types.permanents)

        self.assertTrue(m.is_artifact(c))
        self.assertTrue(m.is_creature(c))
        self.assertTrue(m.is_enchantment(c))
        self.assertFalse(m.is_instant(c))
        self.assertTrue(m.is_land(c))
        self.assertTrue(m.is_planeswalker(c))
        self.assertFalse(m.is_sorcery(c))

        c.types.update(types.nonpermanents)

        self.assertTrue(m.is_artifact(c))
        self.assertTrue(m.is_creature(c))
        self.assertTrue(m.is_enchantment(c))
        self.assertTrue(m.is_instant(c))
        self.assertTrue(m.is_land(c))
        self.assertTrue(m.is_planeswalker(c))
        self.assertTrue(m.is_sorcery(c))

    def test_is_permanent(self):
        c = mock.Mock()

        for type in types.all:
            c.types = {type}

            if type in types.permanents:
                self.assertTrue(m.is_permanent(c))
            else:
                self.assertFalse(m.is_permanent(c))

    def test_has_subtypes(self):
        c = mock.Mock()

        t = m.has_subtypes("Foo")
        u = m.has_subtypes("Foo", "Bar")

        c.subtypes = {"Foo"}
        self.assertTrue(t(c))
        self.assertFalse(u(c))

        c.subtypes.add("Bar")
        self.assertTrue(t(c))
        self.assertTrue(u(c))

        c.subtypes.remove("Foo")
        self.assertFalse(t(c))
        self.assertFalse(u(c))

    def test_is_basic_land(self):
        c = mock.Mock()
        c.types, c.supertypes = set(), set()

        self.assertFalse(m.is_basic_land(c))
        self.assertFalse(m.is_nonbasic_land(c))

        c.types.add(u"Land")
        self.assertFalse(m.is_basic_land(c))
        self.assertTrue(m.is_nonbasic_land(c))

        c.supertypes.add(u"Basic")
        self.assertTrue(m.is_basic_land(c))
        self.assertFalse(m.is_nonbasic_land(c))

    def test_is_color(self):
        c = mock.Mock()
        c.colors = set()

        self.assertTrue(m.is_colorless(c))

        for fn in m.is_white, m.is_blue, m.is_black, m.is_red, m.is_green:
            self.assertFalse(fn(c))

        c.colors.add("B")
        self.assertTrue(m.is_black(c))
        self.assertFalse(m.is_colorless(c))

        c.colors.update("WURG")

        for fn in m.is_white, m.is_blue, m.is_black, m.is_red, m.is_green:
            self.assertTrue(fn(c))

        self.assertFalse(m.is_colorless(c))
