"""
Cardboard core

"""

from operator import attrgetter, methodcaller
import itertools

from cardboard import exceptions
from cardboard.collaborate import collaborate
from cardboard.events import events
from cardboard.util.game import check_started
from cardboard.zones import zone


__all__ = ["Game", "ManaPool", "Player"]


def _make_color(name):

    _color = "_" + name
    negative_error = "{} mana pool would be negative.".format(name.title())
    color_events = getattr(events.player.mana, name)

    @property
    def color(self):
        return getattr(self, _color)

    @color.setter
    @collaborate()
    def color(self, amount):
        """
        Set the number of mana in the {color} mana pool.

        """.format(color=name)

        current = getattr(self, name)

        if amount < 0:
            raise ValueError(negative_error)
        elif amount == current:
            return

        pool = (yield)
        pool.update(amount=amount, color=name)

        if amount > current:
            event = color_events.added
        else:
            event = color_events.removed

        yield event
        yield
        setattr(self, "_" + pool["color"], pool["amount"])
        yield event

    return color


class ManaPool(object):
    """
    A player's mana pool.

    """

    COLORS = ("black", "green", "red", "blue", "white", "colorless")

    black = _make_color("black")
    green = _make_color("green")
    red = _make_color("red")
    blue = _make_color("blue")
    white = _make_color("white")
    colorless = _make_color("colorless")

    def __init__(self, owner):
        super(ManaPool, self).__init__()
        self.owner = owner

        for color in self.COLORS:
            setattr(self, "_" + color, 0)

    def __repr__(self):
        pool = (getattr(self, c) for c in self.COLORS)
        return "[{}B, {}G, {}R, {}U, {}W, {}]".format(*pool)

    @property
    def game(self):
        return self.owner.game


class Player(object):
    """
    A player.

    """

    def __init__(self, library, hand_size=7, life=20, name=""):
        super(Player, self).__init__()

        self.name = name

        self.game = None  # set when a Game adds the player

        self.dead = False
        self.hand_size = hand_size
        self._life = int(life)

        self.exiled = zone("Exile")
        self.graveyard = zone("Graveyard", ordered=True)
        self.hand = zone("Hand")
        self.library = zone("Library", library, ordered=True)

        self.mana_pool = ManaPool(self)

    def __repr__(self):
        if self.game is None:
            number = "(not yet in game)"
        else:
            number = self.game.players.index(self) + 1

        sep = ": " if self.name else ""
        return "<Player {}{}{.name}>".format(number, sep, self)

    @property
    def life(self):
        return self._life

    @life.setter
    @collaborate()
    def life(self, amount):
        """
        Set the player's life total.

        """

        if amount == self.life:
            return

        pool = (yield)
        pool.update(player=self, amount=amount)

        if amount > self.life:
            event = events.player.life.gained
        else:
            event = events.player.life.lost

        yield event
        yield

        pool["player"]._life = amount
        yield event

        if pool["player"].life <= 0:
            pool["player"].die()

    @collaborate()
    def die(self, reason="life"):
        """
        End the player's sorrowful life.

        Arguments:

            * reason (default="life")
                * one of: "life", "library", "poison", <a card>

        """

        # FIXME: Make card valid, maybe by a check if reason is on the stack
        if reason not in {"life", "library", "poison"}:
            raise ValueError("You can't die from '{}'.".format(reason))

        pool = (yield)
        pool.update(player=self, reason=reason)

        yield events.player.died
        yield

        self.dead = True
        yield events.player.died

    @collaborate()
    def draw(self, cards=1):
        """
        Draw cards from the library.


        """

        cards = int(cards)

        if cards == 0:
            return
        elif cards < 0:
            raise ValueError("Can't draw a negative number of cards.")
        elif cards > len(self.library):
            self.die(reason="library")
            return
        elif cards > 1:
            # do draw 1 multiple times so that each draw triggers a draw event
            for i in range(cards):
                self.draw()
            return

        pool = (yield)
        pool.update(player=self, target=self.library[-1])

        yield events.player.draw
        yield

        pool["target"].location = "hand"
        yield events.player.draw


class Game(object):
    """
    The Game object maintains information about the current game state.

    """

    _subscriptions = {

        "end_if_dead" : {"event" : events.player.died, "needs" : ["pool"]},

    }

    def __init__(self, handler):
        """
        Initialize a new game state object.

        """

        super(Game, self).__init__()

        self.events = handler

        for method, subscription_opts in self._subscriptions.iteritems():
            self.events.subscribe(getattr(self, method), **subscription_opts)

        self._phases = itertools.cycle(p.name for p in events.game.phases)
        self._subphases = iter([])  # Default value for first advance

        self._phase = None
        self._subphase = None
        self._turn = None

        self.ended = None

        self.field = set()
        self.tapped = set()
        self.players = []

    def __repr__(self):
        return "<{} Player Game>".format(len(self.players))

    @property
    def phase(self):
        if self._phase is not None:
            return self._phase.name

    @phase.setter
    @collaborate()
    @check_started
    def phase(self, new):
        """
        Set the current turn's phase.

        """

        phase = getattr(events.game.phases, str(new), None)

        if phase is None:
            raise ValueError("No phase named {}".format(new))

        pool = (yield)
        yield phase
        yield

        while next(self._phases) != phase.name:
            pass

        self._phase = phase

        yield phase

        self._subphases = iter(s.name for s in phase)
        self.subphase = next(self._subphases, None)

    @property
    def subphase(self):
        if self._subphase is not None:
            return self._subphase.name

    @subphase.setter
    @collaborate()
    @check_started
    def subphase(self, new):
        """
        Set the current subphase.

        """

        if new is None:
            self._subphase = None
            return

        subphase = getattr(self._phase, str(new))

        pool = (yield)
        yield subphase
        yield

        self._subphase = subphase

        yield subphase

    @property
    def turn(self):
        return self._turn

    @turn.setter
    @collaborate()
    @check_started
    def turn(self, player):
        """
        Set the current turn to a given player.

        """

        if player not in self.players:
            raise ValueError("{} has no player '{}'".format(self, player))

        pool = (yield)
        pool.update(player=player)

        yield events.game.turn.changed
        yield

        self._turn = player

        yield events.game.turn.changed

        self.phase = "beginning"

    def add_player(self, **kwargs):
        """
        Add a new player to the game.

        """

        player = Player(**kwargs)
        self.add_existing_player(player)
        return player

    def add_existing_player(self, player):
        """
        Add an existing Player object to the game.

        """

        player.game = self
        self.players.append(player)

    def next_phase(self):
        """
        Advance a turn to the next phase.

        """

        if self.phase == "ending" and self.subphase == "cleanup":
            self.next_turn()
            return

        try:
            self.subphase = next(self._subphases)
        except StopIteration:
            self.phase = next(self._phases)

    @check_started
    def next_turn(self):
        """
        Advance the game to the next player's turn.

        """

        self.turn = next(self._turns)

    @property
    def started(self):
        return self.ended is not None

    def start(self):
        """
        Start the game.

        """

        if not self.players:
            raise exceptions.RuntimeError("Starting the game requires at least"
                                          " one player.")

        self.events.trigger(event=events.game.started)

        self._turns = itertools.cycle(self.players)
        self.ended = False

        for player in self.players:
            player.draw(player.hand_size)

        self.next_turn()

    # @subscribed to: events.player.died
    def end_if_dead(self, pangler=None, pool=None):
        """
        End the game if there is only one living player left.

        """

        if sum(1 for player in self.players if not player.dead) <= 1:
            self.end()

    @collaborate()
    def end(self):
        """
        End the game unconditionally.

        """

        # TODO: Stop all other events
        pool = (yield)

        yield events.game.ended
        yield

        self.ended = True
        yield events.game.ended
