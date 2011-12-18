import unittest

from cardboard import util as u


class TestUtil(unittest.TestCase):
    def test_ANY(self):
        self.assertTrue(u.ANY(object()))

    def test_populate(self):
        d = {}
        p = u.populate(d)

        @p("Foo")
        def foo():
            pass

        self.assertIs(d["Foo"], foo)

        p = u.populate(d, allow_overwrite=False)

        with self.assertRaises(ValueError):
            @p("Foo")
            def foo():
                pass

    def test_sanitize(self):
        self.assertEqual(u.sanitize("foo"), "foo")
        self.assertEqual(u.sanitize("Foo"), "foo")
        self.assertEqual(u.sanitize("Foo Bar"), "foo_bar")
        self.assertEqual(u.sanitize("Foo's Bar"), "foos_bar")

        self.assertEqual(u.sanitize("Foo", ignore_case=False), "Foo")
        self.assertEqual(u.sanitize("Fo's Bar", ignore_case=False), "Fos_Bar")
