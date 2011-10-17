from functools import wraps
from textwrap import dedent

from zope.interface import Attribute, Interface, implements

from cardboard.util import ANY, requirements


__all__ = ["IFrontend", "IRunnable", "FrontendMixin", "validate_selection"]


class IFrontend(Interface):
    """
    A frontend is a frontend.

    Frontends should implement a few simple methods for displaying and querying
    the player, which will be called when they are attached to a player.

    In general, the backend will attempt to call the most specific display and
    query methods that are appropriate. If a frontend does not wish to provide
    any additional behavior in the more specific methods, it is free to fall
    back on whatever more general methods it wishes.

    """

    _debug = Attribute("Designates whether the frontend is in debug mode")
    running = Attribute("Specifies if the frontend is currently running")

    game = Attribute("The game object which the frontend is currently attached"
                     "to")
    player = Attribute("The player who the frontend is attached to")

    def priority_granted():
        """
        :term:`Priority` was granted to the player.

        """

    def prompt(msg):
        """
        Show a message to the player.

        """

    def select(choices, how_many=1, duplicates=False):
        """
        Select from a given set of choices.

        * choices : an iterable of selections to choose from
        * how_many : how many selections to request (default=1)
        * duplicates : allow duplicates (default=False)

        """

    def select_cards(zone, match=ANY, how_many=1, duplicates=False):
        """
        Select cards from a given zone.

        * zone : the zone to select cards from
        * match : filter cards by a callable (default no filtering)
        * how_many : how many selections to request (default=1)
        * duplicates : allow duplicates (default=False)

        """

    def select_players(match=ANY, how_many=1, duplicates=False):
        """
        Select a matching player.

        * match : filter players by a callable (default no filtering)
        * how_many : how many selections to request (default=1)
        * duplicates : allow duplicates (default=False)

        """

    def select_combined(zone, match_cards=ANY, how_many_cards=1,
                        duplicate_cards=False, match_players=ANY,
                        how_many_players=1, duplicate_players=False):
        """
        Simultaneously select from a given set of cards and a set of players.

        * zone : the zone to select cards from
        * match_cards : filter cards by a callable (default no filtering)
        * how_many_cards : how many card selections to request (default=1)
        * duplicate_cards : allow duplicate cards (default=False)

        * match_players : filter players by a callable (default no filtering)
        * how_many_players : how many player selections to request (default=1)
        * duplicate_players : allow duplicate players (default=False)

        """

    def select_range(start, stop, how_many=1, duplicates=False):
        """
        Select from a given range of numbers.

        Like Python's range() function, stop is *exclusive*.

        * start, stop : the start and stop of the range.
        * how_many : how many selections to request (default=1)
        * duplicates : allow duplicates (default=False)

        """


class IRunnable(Interface):
    """
    A runnable frontend.

    """

    def run():
        """
        Start running the frontend if it is not yet running.

        Expected to raise an exception if the frontend is already running.

        """


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
