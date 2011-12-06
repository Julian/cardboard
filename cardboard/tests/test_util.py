import unittest

from cardboard import util as u


class TestUtil(unittest.TestCase):
    def test_ANY(self):
        self.assertTrue(u.ANY(object()))

    def test_sanitize(self):
        self.assertEqual(u.sanitize("foo"), "foo")
        self.assertEqual(u.sanitize("Foo"), "foo")
        self.assertEqual(u.sanitize("Foo Bar"), "foo_bar")
        self.assertEqual(u.sanitize("Foo's Bar"), "foos_bar")

        self.assertEqual(u.sanitize("Foo", ignore_case=False), "Foo")
        self.assertEqual(u.sanitize("Fo's Bar", ignore_case=False), "Fos_Bar")
