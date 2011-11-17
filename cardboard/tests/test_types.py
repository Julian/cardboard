import unittest

from cardboard import types as t

class TestTypes(unittest.TestCase):
    def test_permanents_nonpermanents(self):
        self.assertEqual(t.permanents, {u"Artifact", u"Creature",
                                        u"Enchantment", u"Land",
                                        u"Planeswalker"})

        self.assertEqual(t.nonpermanents, {u"Instant", u"Sorcery"})

    def test_types(self):
        self.assertEqual(t.all, t.permanents | t.nonpermanents)
