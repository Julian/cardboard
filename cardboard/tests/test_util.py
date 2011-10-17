import unittest

from cardboard import util as u


class TestUtil(unittest.TestCase):
    def test_ANY(self):
        self.assertTrue(u.ANY(object()))
