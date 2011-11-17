import unittest

import mock

from cardboard import types
from cardboard.cards import match as m


class TestMatch(unittest.TestCase):
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

    def test_lacks_types(self):
        c = mock.Mock()

        t = m.lacks_types("Foo")
        u = m.lacks_types("Foo", "Bar")

        c.types = {"Foo"}
        self.assertFalse(t(c))
        self.assertFalse(u(c))

        c.types.add("Bar")
        self.assertFalse(t(c))
        self.assertFalse(u(c))

        c.types.remove("Foo")
        self.assertTrue(t(c))
        self.assertFalse(u(c))

        c.types.remove("Bar")
        self.assertTrue(t(c))
        self.assertTrue(u(c))

    def test_is_not_types(self):
        c = mock.Mock()
        c.types = set()

        self.assertTrue(m.is_not_artifact(c))
        self.assertTrue(m.is_not_creature(c))
        self.assertTrue(m.is_not_enchantment(c))
        self.assertTrue(m.is_not_instant(c))
        self.assertTrue(m.is_not_land(c))
        self.assertTrue(m.is_not_planeswalker(c))
        self.assertTrue(m.is_not_sorcery(c))

        c.types.update(types.permanents)

        self.assertFalse(m.is_not_artifact(c))
        self.assertFalse(m.is_not_creature(c))
        self.assertFalse(m.is_not_enchantment(c))
        self.assertTrue(m.is_not_instant(c))
        self.assertFalse(m.is_not_land(c))
        self.assertFalse(m.is_not_planeswalker(c))
        self.assertTrue(m.is_not_sorcery(c))

        c.types.update(types.nonpermanents)

        self.assertFalse(m.is_not_artifact(c))
        self.assertFalse(m.is_not_creature(c))
        self.assertFalse(m.is_not_enchantment(c))
        self.assertFalse(m.is_not_instant(c))
        self.assertFalse(m.is_not_land(c))
        self.assertFalse(m.is_not_planeswalker(c))
        self.assertFalse(m.is_not_sorcery(c))

    def test_is_permanent(self):
        c = mock.Mock()

        for type in types.all:
            c.types = {type}

            if type in types.permanents:
                self.assertTrue(m.is_permanent(c))
                self.assertFalse(m.is_nonpermanent(c))
            else:
                self.assertFalse(m.is_permanent(c))
                self.assertTrue(m.is_nonpermanent(c))

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
