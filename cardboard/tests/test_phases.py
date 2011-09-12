import unittest

from cardboard import phases as p
from cardboard.tests.util import GameTestCase


class TestPhase(unittest.TestCase):
    def test_init(self):
        h = p.Phase("Foo", [1, 2, 3])

        self.assertEqual(h.name, "Foo")
        self.assertEqual(h.steps, [1, 2, 3])

    def test_iter(self):
        h = p.Phase("Foo", [1, 2, 3])
        self.assertEqual(list(h), [1, 2, 3])

    def test_getitem(self):
        h = p.Phase("Foo", [1, 2, 3])

        self.assertEqual(h[0], 1)
        self.assertEqual(h[1], 2)
        self.assertEqual(h[2], 3)

    def test_len(self):
        h = p.Phase("Foo", [1, 2, 3])
        self.assertEqual(len(h), 3)

    def test_repr_str(self):
        h = p.Phase("foo_bar", [1, 2, 3])
        self.assertEqual(repr(h), "<Phase: Foo Bar>")
        self.assertEqual(str(h), "Foo Bar")


class TestPhaseMechanics(GameTestCase):
    pass
