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
