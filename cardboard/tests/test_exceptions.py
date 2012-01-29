import unittest

from cardboard import exceptions


class TestNoSuchObject(unittest.TestCase):
    def test_str(self):
        n = exceptions.NoSuchObject("blablabla", "foo", 0)
        self.assertEqual(str(n), "blablabla has no such foo '0'")


class TestRequirementNotMet(unittest.TestCase):
    def test_str(self):
        r = exceptions.RequirementNotMet(instance=None, attr=None, got=None,
                                         expected=None, msg="foo bar")
        self.assertEqual(str(r), "foo bar")
