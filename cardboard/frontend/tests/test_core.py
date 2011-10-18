import unittest

import mock

from cardboard import exceptions
from cardboard.frontend import core as c


class TestFrontend(c.FrontendMixin):
    info = mock.Mock()
    select = mock.Mock()


class TestFrontendMixin(unittest.TestCase):
    def setUp(self):
        super(TestFrontendMixin, self).setUp()

        self.player = mock.Mock()
        self.frontend = TestFrontend(self.player)

    def test_repr(self):
        self.assertEqual(repr(self.frontend),
                         "<TestFrontend connected to {}>".format(self.player))

    def test_init(self):
        self.assertIs(self.frontend.player, self.player)
        self.assertIs(self.frontend.game, self.player.game)

        self.assertIs(
            self.frontend.info, self.frontend.__class__.info.return_value
        )

        self.assertIs(
            self.frontend.select, self.frontend.__class__.select.return_value
        )

        self.assertFalse(self.frontend._debug)

        f = TestFrontend(self.player, debug=True)
        self.assertTrue(f._debug)

    def test_running(self):
        self.assertFalse(self.frontend.running)
        self.frontend.run()
        self.assertTrue(self.frontend.running)

        # can't run a running frontend
        with self.assertRaises(exceptions.RequirementNotMet):
            self.frontend.run()


class TestValidate(unittest.TestCase):

    @c.validate_selection
    def select(self, whatever, how_many, duplicates):
        return whatever

    def test_how_many(self):
        self.select([2])
        self.select([2], how_many=1)
        self.select([2, 3, 4], how_many=3)

        with self.assertRaises(exceptions.BadSelection):
            self.select([2, 3])

        with self.assertRaises(exceptions.BadSelection):
            self.select([2, 3], how_many=1)

        with self.assertRaises(exceptions.BadSelection):
            self.select([2, 3, 4], how_many=2)

    def test_duplicates(self):
        self.select([2, 2], how_many=2, duplicates=True)
        self.select([2, 3, 3, 5, 2], how_many=5, duplicates=True)

        with self.assertRaisesRegexp(exceptions.BadSelection, "duplicate"):
            self.select([2, 2], how_many=2)

        with self.assertRaisesRegexp(exceptions.BadSelection, "duplicate"):
            self.select([2, 2], how_many=2, duplicates=False)

        with self.assertRaisesRegexp(exceptions.BadSelection, "duplicate"):
            self.select([2, 3, 3, 2], how_many=4)

    def test_arbitrary_selection(self):
        self.select([], how_many=None)
        self.select([2], how_many=None)
        self.select([2, 3], how_many=None)

        self.select([2, 2], how_many=None, duplicates=True)
        self.select([2, 3, 3, 5, 2], how_many=None, duplicates=True)
