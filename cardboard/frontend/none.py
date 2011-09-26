"""
A frontend that represents the lack of a connected frontend to a player.

"""

from cardboard import exceptions


class NoFrontend(object):
    def __init__(self, player, debug=False):
        super(NoFrontend, self).__init__()

        self._debug = debug

        self.game = player.game
        self.player = player

    def __repr__(self):
        return "<No Frontend Connected>"

    def __getattr__(self, attr):
        raise exceptions.NoFrontendConnected(self.player)
