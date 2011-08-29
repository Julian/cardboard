import unittest

from cardboard import exceptions as e
from cardboard.tests.util import GameTestCase

class TestNoSuchObject(GameTestCase):
    def test_str(self):
        n = e.NoSuchObject(self.game, "foo", 0)
        self.assertTrue(str(n).endswith("Game> has no such foo '0'"))
