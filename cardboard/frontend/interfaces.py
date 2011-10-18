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
    running = Attribute("Specifies if the frontend is currently running")

    info = Attribute(
        "A provider of {IInfoDisplay} to be instantiated for each instance."
    )
    select = Attribute(
        "A provider of {ISelector} to be instantiated for each instance."
    )

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


class IInfoDisplay(Interface):
    """
    Interface for information displays.

    An information display knows how to manipulate a particular frontend to
    display information about different game objects.

    """

    @property
    def player_overview():
        """
        Display an overview of all players' information.

        """

    @property
    def turn():
        """
        Display information about the current turn and phase.

        """

    @property
    def zone_overview():
        """
        Display an overview of all zones' contents.

        """

    def card(card):
        """
        Display a card.

        """

    def player(player):
        """
        Display a player's information.

        """

    def zone(zone):
        """
        Display a zone's contents.

        """


class ISelector(Interface):
    """
    Interface for selectors.

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


