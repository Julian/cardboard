import unittest

from cardboard import types as t

class TestTypes(unittest.TestCase):
    def test_is_permanent(self):
        for type in t.PERMANENTS:
            self.assertTrue(t.is_permanent(type))

        for type in t.NONPERMANENTS:
            self.assertFalse(t.is_permanent(type))

    def test_PERMANENTS_NONPERMANENTS(self):
        self.assertEqual(t.PERMANENTS, {u"Artifact", u"Creature",
                                        u"Enchantment", u"Land",
                                        u"Planeswalker"})

        self.assertEqual(t.NONPERMANENTS, {u"Instant", u"Sorcery"})

    def test_TYPES(self):
        self.assertEqual(t.TYPES, t.PERMANENTS | t.NONPERMANENTS)
