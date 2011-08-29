import unittest

from cardboard.frontend import none as n
from cardboard.tests.util import GameTestCase

class TestNoFrontend(GameTestCase):
    def test_repr(self):
        self.assertEqual(repr(self.p1.frontend), "<No Frontend Connected>")

    def test_does_nothing(self):
        self.assertIsNone(self.p1.frontend.prompt(""))
        self.assertIsNone(self.p1.frontend.priority_granted())
        self.assertFalse(self.p1.frontend.select(range(3)))
