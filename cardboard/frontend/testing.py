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


class TestingSelector(object):

    choice = mock_selector("choice")
    cards = mock_selector("cards")
    players = mock_selector("players")
    combined = mock_selector("combined")
    range = mock_selector("range")

    def __init__(self, frontend):
        super(TestingSelector, self).__init__()


class TestingFrontend(FrontendMixin):

    implements(IFrontend)

    info = lambda _, __ : None
    select = TestingSelector

    def prompt(self, msg):
        log.msg(msg)

    def priority_granted(self):
        pass
