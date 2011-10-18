from functools import wraps

from zope.interface import implements

from cardboard import exceptions
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
    def validated(*args, **kwargs):
        how_many = kwargs.setdefault("how_many", 1)
        duplicates = kwargs.setdefault("duplicates", False)

        selections = fn(*args, **kwargs)
        got = len(selections)

        if how_many is not None and got != how_many:
            raise exceptions.BadSelection(
                "Expected {} selections, got {}.".format(how_many, got)
            )

        if not duplicates:
            if len(set(selections)) != got:
                raise exceptions.BadSelection("Cannot duplicate selections.")

        return selections

    return validated
