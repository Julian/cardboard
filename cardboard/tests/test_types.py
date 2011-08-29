import unittest

from cardboard import types as t

class TestType(unittest.TestCase):
    def test_init(self):
        y = t.Type("Foo")
        self.assertEqual(y.name, "Foo")

    def test_str_repr(self):
        y = t.Type("Foo")
        self.assertEqual(str(y), y.name)
        self.assertEqual(repr(y), "<Type: Foo>")

    def test_hash_eq(self):
        x = t.Type("Foo")
        y = t.Type("Foo")
        z = t.Type("Bar")

        self.assertEqual(x, y)
        self.assertEqual(hash(x), hash(y))

        self.assertNotEqual(x, z)
        self.assertNotEqual(hash(x), hash(z))

        self.assertIs(NotImplemented, x.__eq__(object()))

    def test_is_permanent(self):
        for type in t.PERMANENTS:
            self.assertTrue(type.is_permanent)

        for type in t.NONPERMANENTS:
            self.assertFalse(type.is_permanent)

    def test_PERMANENTS_NONPERMANENTS(self):
        self.assertEqual({type.name for type in t.PERMANENTS},
                         {"Artifact", "Creature", "Enchantment",
                          "Land", "Planeswalker"})

        self.assertEqual({type.name for type in t.NONPERMANENTS},
                         {"Instant", "Sorcery"})

    def test_TYPES(self):
        self.assertEqual(t.TYPES, t.PERMANENTS | t.NONPERMANENTS)
