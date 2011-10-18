import unittest

import mock

from cardboard import exceptions
from cardboard.frontend import none as n


class TestNoFrontend(unittest.TestCase):
    def test_repr(self):
        g = mock.Mock()
        f = n.NoFrontend(g)
        self.assertEqual(repr(f), "<No Frontend connected to {}>".format(g))

    def test_no_frontend(self):
        f = n.NoFrontend(mock.Mock())

        for attr in "select", "select_cards", "priority_granted", "foo":
            with self.assertRaises(exceptions.NoFrontendConnected):
                getattr(f, attr)
