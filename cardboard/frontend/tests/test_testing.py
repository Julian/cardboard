import unittest

from cardboard.frontend import testing as t


class TestSelector(unittest.TestCase):
    def test_selector(self):
        class Foo(object):
            foo = t.selector("foo")

        f = Foo()

        with f.foo.will_return(10, 11, 12):
            self.assertEqual(f.foo(how_many=3), (10, 11, 12))

            with f.foo.will_return("a"):
                self.assertEqual(f.foo(how_many=1), ("a",))

            self.assertEqual(f.foo(how_many=3), (10, 11, 12))

        # arbitrary selection doesn't check return value
        with f.foo.will_return(10, 11, 12):
            self.assertEqual(f.foo(), (10, 11, 12))
            self.assertEqual(f.foo(how_many=None), (10, 11, 12))

        # can't select without setting a selection return value
        with self.assertRaises(t.SelectionError):
            f.foo()

        # can't return more selections than how_many
        with self.assertRaises(t.SelectionError):
            with f.foo.will_return(10, 11, 12):
                s = f.foo(how_many=2)

        self.assertEqual(f.foo.__name__, "foo")
