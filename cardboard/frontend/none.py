"""
A frontend that represents the lack of a connected frontend to a player.

"""

from cardboard import exceptions
from cardboard.frontend import FrontendMixin


class NoFrontend(FrontendMixin):
    def __getattr__(self, attr):
        raise exceptions.NoFrontendConnected(self.player)
