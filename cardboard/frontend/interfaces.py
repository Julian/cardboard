from textwrap import dedent

from zope.interface import Attribute, Interface

from cardboard.util import ANY


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

    game = Attribute("The attached game object")
    player = Attribute("The attached player")
    running = Attribute("Specifies if the frontend is currently running")

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

    def select_cards(
        zone=None, match=ANY, how_many=1, duplicates=False, bad=True
    ):
        """
        Select cards from a given zone.

        * zone : the zone to select cards from (default=self.game.battlefield)
        * match : filter cards by a callable (default no filtering)
        * how_many : how many selections to request (default=1)
        * duplicates : allow duplicates (default=False)
        * bad : is this selection for something "bad" (default=True)

        """

    def select_players(match=ANY, how_many=1, duplicates=False, bad=True):
        """
        Select a matching player.

        * match : filter players by a callable (default no filtering)
        * how_many : how many selections to request (default=1)
        * duplicates : allow duplicates (default=False)
        * bad : is this selection for something "bad" (default=True)

        """

    def select_combined(zone=None, match_cards=ANY, how_many_cards=1,
                 duplicate_cards=False, match_players=ANY, how_many_players=1,
                 duplicate_players=False, bad=True):
        """
        Simultaneously select from a given set of cards and a set of players.

        * zone : the zone to select cards from (default=self.game.battlefield)
        * match_cards : filter cards by a callable (default no filtering)
        * how_many_cards : how many card selections to request (default=1)
        * duplicate_cards : allow duplicate cards (default=False)

        * match_players : filter players by a callable (default no filtering)
        * how_many_players : how many player selections to request (default=1)
        * duplicate_players : allow duplicate players (default=False)

        * bad : is this selection for something "bad" (default=True)

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
