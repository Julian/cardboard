"""
A frontend that represents the lack of a connected frontend to a player.

"""

from zope.interface import implements

from cardboard import exceptions
from cardboard.frontend.interfaces import IFrontend


class NoFrontend(object):

    implements(IFrontend)

    def __init__(self, player, debug=False):
        super(NoFrontend, self).__init__()

        self._debug = debug
        self.game = player.game
        self.player = player

    def __repr__(self):
        return "<No Frontend connected to {.player}>".format(self)

    def _not_connected(self, *args, **kwargs):
        raise exceptions.NoFrontendConnected(self.player)

    priority_granted = prompt = _not_connected
    info = running = select = property(_not_connected)
