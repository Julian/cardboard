import collections
import random
import unittest

from cardboard import zones as z


class TestZone(unittest.TestCase):
    def test_name(self):
        n = z.Zone("Casino Night")
        self.assertEqual(n.name, "Casino Night")

    def test_ordered(self):
        n = z.Zone("Casino Night")
        self.assertFalse(n.ordered)

    def test_repr(self):
        n = z.Zone("Casino Night")
        self.assertEqual(repr(n), "<Zone: Casino Night>")

    def test_contains(self):
        n = z.Zone("Casino Night", range(3))

        for i in range(3):
            self.assertIn(i, n)

        self.assertNotIn(4, n)

    def test_iter(self):
        noise = [random.random() for _ in range(30)]
        n = z.Zone("Casino Night", noise)
        self.assertEqual(set(n), set(noise))

    def test_len(self):
        n = z.Zone("Casino Night", range(30))
        self.assertEqual(len(n), 30)

    def test_add(self):
        n = z.Zone("Casino Night", range(30))
        n.add(30)
        self.assertEqual(set(n), set(range(31)))

    def test_discard(self):
        n = z.Zone("Casino Night", range(30))
        n.discard(21)
        n.discard(object())
        self.assertEqual(len(n), 29)
        self.assertEqual(n, set(n) - {21})


class TestOrderedZone(unittest.TestCase):
    def setUp(self):
        self.noise = [random.random() for _ in range(30)]

    def test_name(self):
        n = z.OrderedZone("Emerald Hill")
        self.assertEqual(n.name, "Emerald Hill")

    def test_ordered(self):
        n = z.OrderedZone("Emerald Hill")
        self.assertTrue(n.ordered)

    def test_repr(self):
        o = z.OrderedZone("Emerald Hill")
        self.assertEqual(repr(o), "<OrderedZone: Emerald Hill>")

    def test_contains(self):
        o = z.OrderedZone("Emerald Hill", self.noise)

        for i in self.noise:
            self.assertIn(i, o)

    def test_iter(self):
        o = z.OrderedZone("Emerald Hill", self.noise)
        self.assertEqual(list(o), self.noise)

    def test_reversed(self):
        o = z.OrderedZone("Emerald Hill", self.noise)
        self.assertEqual(list(reversed(o)), list(reversed(self.noise)))

    def test_len(self):
        o = z.OrderedZone("Emerald Hill", self.noise)
        self.assertEqual(len(o), len(self.noise))

    def test_getitem(self):
        o = z.OrderedZone("Emerald Hill", self.noise)
        for i, e in enumerate(self.noise):
            self.assertEqual(o[i], e)

        self.assertEqual(o[2:7:2], self.noise[2:7:2])

    def test_set_del_item(self):
        o = z.OrderedZone("Emerald Hill", self.noise)
        self.assertRaises(AttributeError, getattr, o, "__setitem__")
        self.assertRaises(AttributeError, getattr, o, "__delitem__")

    def test_add(self):
        o = z.OrderedZone("Emerald Hill", self.noise)
        o.add(42)
        self.assertEqual(list(o), self.noise + [42])

    def test_discard(self):
        o = z.OrderedZone("Emerald Hill", self.noise)
        e = self.noise[17]
        o.discard(e)
        o.discard(object())
        self.assertEqual(len(o), len(self.noise) - 1)
        self.assertEqual(set(o), set(self.noise) - {e})

    def test_clear(self):
        o = z.OrderedZone("Emerald Hill", self.noise)
        o.clear()
        self.assertFalse(o)

    def test_append(self):
        o = z.OrderedZone("Emerald Hill", self.noise)
        o.append(2)
        self.assertEqual(o[-1], 2)
        self.assertEqual(len(o), len(self.noise) + 1)

    def test_extend(self):
        o = z.OrderedZone("Emerald Hill", self.noise)
        o.extend(range(4))
        self.assertEqual(o[-4:], range(4))
        self.assertEqual(len(o), len(self.noise) + 4)

    def test_remove(self):
        o = z.OrderedZone("Emerald Hill", self.noise)
        e = self.noise[-7]
        self.noise.remove(e)
        o.remove(e)

        self.assertEqual(list(o), self.noise)
        self.assertRaises(ValueError, o.remove, object())

    def test_reverse(self):
        o = z.OrderedZone("Emerald Hill", self.noise)
        o.reverse()
        self.assertEqual(list(o), list(reversed(self.noise)))

    def test_index(self):
        o = z.OrderedZone("Emerald Hill", self.noise)
        e = self.noise[13]
        self.assertEqual(o.index(e), 13)

    def test_count(self):
        o = z.OrderedZone("Emerald Hill", [1, 1, 1, 2, 2, 3])

        for i, e in enumerate(range(3, 0, -1), 1):
            self.assertEqual(o.count(e), i)

    def test_pop(self):
        o = z.OrderedZone("Emerald Hill", range(40))
        o.pop()
        self.assertEqual(len(o), 39)
        self.assertEqual(list(o), range(39))

    def test_pop_index(self):
        r = range(1, 40)
        r.pop(38)

        o = z.OrderedZone("Emerald Hill", range(40))
        o.pop(0)
        o.pop(38)
        self.assertEqual(list(o), r)

    def test_iterable(self):
        # TODO: This is incomplete, all the methods don't take iterables
        o = z.OrderedZone("Emerald Hill", iter(range(40)))
        self.assertIn(2, o)
        self.assertTrue(list(o))


class TestZoneOZone(unittest.TestCase):
    def test_zone(self):
        n = z.zone("Foo", contents=range(3), ordered=False)
        self.assertEqual("Foo", n.name)
        self.assertEqual(list(n), range(3))
        self.assertIsInstance(n, z.Zone)

        o = z.zone("Bar", contents=range(3), ordered=True)
        self.assertEqual("Bar", o.name)
        self.assertEqual(list(o), range(3))
        self.assertIsInstance(o, z.OrderedZone)
