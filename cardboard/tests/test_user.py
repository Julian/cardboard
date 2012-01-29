import unittest

import mock

from cardboard.tests import user as t
from cardboard.tests.util import GameTestCase


class TestMockSelector(unittest.TestCase):
    def test_mock_selector(self):
        class Foo(object):
            foo = t.mock_selector("foo")

        f = Foo()

        with f.foo.will_return(10, 11, 12):
            self.assertEqual(f.foo(how_many=3), (10, 11, 12))

            with f.foo.will_return("a"):
                self.assertEqual(f.foo(how_many=1), ("a",))

            with f.foo.will_return():
                self.assertEqual(f.foo(how_many=0), ())

            self.assertEqual(f.foo(how_many=3), (10, 11, 12))

        self.assertEqual(f.foo.__name__, "foo")


class TestTestingUser(GameTestCase):
    def test_prompt(self):
        with mock.patch("cardboard.tests.user.log") as log:
            self.p1.user.prompt("Testing 123")

        log.msg.assert_called_once_with("Testing 123")
