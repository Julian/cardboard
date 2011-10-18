from functools import wraps

from zope.interface import implements

from cardboard.util import requirements
from cardboard.frontend.interfaces import IRunnable


__all__ = ["FrontendMixin", "validate_selection"]


class FrontendMixin(object):

    implements(IRunnable)

    _require = requirements({"running" : {True : "{self} is already running.",
                                          False : "{self} is not running."}})

    def __init__(self, player, debug=False):
        super(FrontendMixin, self).__init__()

        self._debug = debug
        self.running = False

        self.game = player.game
        self.player = player

        # info and select should be set to factories for the proper providers
        self.info, self.select = self.info(self), self.select(self)

    def __repr__(self):
        return "<{0.__class__.__name__} connected to {0.player}>".format(self)

    def run(self):
        self._require(running=False)
        self.running = True
        getattr(self, "started_running", lambda : None)()


def validate_selection(fn):
    @wraps(fn)
    def validate(*args, **kwargs):
        # TODO: how_many = None
        if len(selections) < how_many:
            self.prompt("Not enough selections.")
        elif not duplicates and len(set(selections)) < len(selections):
            self.prompt("Can't duplicate selections.")
        else:
            try:
                return [choices[selection] for selection in selections]
            except KeyError as e:
                self.prompt("{} is not a valid choice.".format(e[0]))
    return validate
