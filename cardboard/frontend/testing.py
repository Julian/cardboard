"""
A frontend for use when testing.

"""

import contextlib
import functools
import logging


class SelectionError(Exception):
    pass


def selector(name):

    selections = []

    @contextlib.contextmanager
    def will_return(*selection):
        selections.append(selection)
        yield
        selections.pop()

    def select(self, source=(), *args, **kwargs):
        how_many = kwargs.get("how_many")

        try:
            selection = selections[-1]
        except IndexError:
            raise SelectionError("No selection was set.")
        else:
            if how_many is not None and len(selection) != how_many:
                raise SelectionError("Expected {} selections".format(how_many))
            return selection

    select.__name__ = name
    select.will_return = will_return

    return select


class TestingFrontend(object):

    select = selector("select")
    select_cards = selector("select_cards")
    select_range = selector("select_range")
    select_players = selector("select_players")

    def __init__(self, player, debug=False):
        super(TestingFrontend, self).__init__()

        self._debug = debug

        self.game = player.game
        self.player = player

        self._logger = logging.getLogger(self.player.name)

        if debug:
            self._logger.setLevel(logging.DEBUG)

    def __repr__(self):
        return "<Testing Frontend to {.name}>".format(self.player)

    def prompt(self, msg, *args, **kwargs):
        self._logger.info(msg, *args, **kwargs)
