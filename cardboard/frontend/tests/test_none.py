import unittest

from zope.interface import interface, verify
import mock

from cardboard import exceptions
from cardboard.frontend.interfaces import IFrontend
from cardboard.frontend import _none as n


class TestNoFrontend(unittest.TestCase):
    def test_repr(self):
        g = mock.Mock()
        f = n.NoFrontend(g)
        self.assertEqual(repr(f), "<No Frontend connected to {}>".format(g))

    def test_no_frontend(self):
        verify.verifyClass(IFrontend, n.NoFrontend)

        # attributes raise NoFrontendConnected
        f = n.NoFrontend(mock.Mock())

        # some attributes we actually do want to have
        DONT_FAIL = {"_debug", "game", "player"}

        for k in DONT_FAIL:
            getattr(f, k)

        for k, v in IFrontend.namesAndDescriptions():
            if not isinstance(v, interface.Method) and k not in DONT_FAIL:
                with self.assertRaises(exceptions.NoFrontendConnected):
                    getattr(f, k)
