"""
A frontend for use when testing.

"""

import contextlib

from twisted.python import log
from zope.interface import implements

from cardboard.frontend import FrontendMixin, IFrontend


def mock_selector(name):

    selections = [()]

    @contextlib.contextmanager
    def will_return(*selection):
        selections.append(selection)
        yield
        selections.pop()

    def select(self, *args, **kwargs):
        return selections[-1]

    select.__name__ = name
    select.will_return = will_return

    return select


class TestingFrontend(FrontendMixin):

    implements(IFrontend)

    select = mock_selector("select")
    select_cards = mock_selector("select_cards")
    select_players = mock_selector("select_players")
    select_combined = mock_selector("select_combined")
    select_range = mock_selector("select_range")

    def prompt(self, msg):
        log.msg(msg)

    def priority_granted(self):
        pass
