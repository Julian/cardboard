"""
A frontend for use when testing.

"""

import contextlib

from twisted.python import log


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


class TestingFrontend(object):

    select = mock_selector("choice")
    select_cards = mock_selector("cards")
    select_players = mock_selector("players")
    select_combined = mock_selector("combined")
    select_range = mock_selector("range")

    def prompt(self, msg):
        log.msg(msg)

    def priority_granted(self):
        pass
