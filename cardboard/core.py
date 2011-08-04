"""
Cardboard core

"""

from operator import attrgetter, methodcaller
import itertools

from cardboard.events import announce, events

PHASES = [("beginning", ["untap", "draw", "upkeep"]),
          ("first main", []),
          ("combat", ["beginning", "declare attackers", "declare blockers",
                      "combat damage", "end"]),
          ("second main", []),
          ("ending", ["end", "cleanup"])]


def _make_color(name):

    _color = "_" + name
    negative_error = "{} mana pool would be negative.".format(name.title())
    store = getattr(events.player.mana, name)

    @property
    def color(self):
        return getattr(self, _color)

    @color.setter
    @announce(added="{} mana entered pool".format(name),
              left="{} mana left pool".format(name), store=store)
    def color(self, amount):
        """
        Set the number of mana in the {color} mana pool.

        """.format(color=name)

        if amount < 0:
            raise ValueError(negative_error)

        pool = (yield)
        pool.update(amount=amount, color=name)

        current = getattr(self, name)

        if amount == current:
            return
        elif amount > current:
            event = "added"
        else:
            event = "left"

        yield event
        yield
        setattr(self, "_" + pool["color"], pool["amount"])
        yield event

    return color


class ManaPool(object):
    COLORS = ("black", "blue", "green", "red", "white", "colorless")

    black = _make_color("black")
    blue = _make_color("blue")
    green = _make_color("green")
    red = _make_color("red")
    white = _make_color("white")
    colorless = _make_color("colorless")

    def __init__(self, for_player):
        super(ManaPool, self).__init__()

        self.player = for_player
        self.events = self.player.events

        for color in self.COLORS:
            setattr(self, "_" + color, 0)

    def __iter__(self):
        return iter(self.pool)

    def __repr__(self):
        pool = (getattr(self, c) for c in self.COLORS)
        return "[{}B, {}U, {}G, {}R, {}W, {}]".format(*pool)


class Player(object):
    """
    A player.

    """

    def __init__(self, handler, deck, name="", hand_size=7, life=20):
        super(Player, self).__init__()

        self.events = handler

        self.name = str(name)
        self.dead = False
        self._life = int(life)
        self.library = deck

        self.hand = set()
        self.draw(hand_size)

        self.exiled = set()
        self.graveyard = []
        self.mana_pool = ManaPool(self)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Player: {}>".format(self.name or "Unnamed")

    @property
    def life(self):
        return self._life

    @life.setter
    @announce(gained="gained life", lost="lost life", store=events.player.life)
    def life(self, amount):

        pool = (yield)
        pool.update(player=self, amount=amount)

        if amount == self.life:
            return
        elif amount > self.life:
            event = "gained"
        else:
            event = "lost"

        yield event
        yield
        pool["player"]._life = amount
        yield event

        if pool["player"].life <= 0:
            pool["player"].die()

    @announce(died="player died", store=events.player)
    def die(self, reason="life"):
        """
        End the player's sorrowful life.

        Arguments:

            * reason (default="life")
                * valid reasons: "life", "library empty", "poison", <a card>

        """

        # TODO: Reason
        pool = (yield)
        pool.update(player=self, reason=reason)

        yield "died"
        yield

        self.dead = True
        yield "died"

    @announce(draw="card drawn", store=events.player)
    def draw(self, cards=1):
        """
        Draw cards from the library.


        """

        if not cards:
            return
        elif cards < 0:
            raise ValueError("Can't draw a negative number of cards.")

        if not self.library:
            self.die(reason="library")
            return

        # FIXME: die ^
        if cards > 1:
            for i in range(cards):
                self.draw()
            return

        pool = (yield)
        pool.update(player=self, source=self.library,
                    destination=self.hand,
                    source_get=methodcaller("pop"),
                    destination_add=attrgetter("add"))

        yield "draw"
        yield

        card = pool["source_get"](pool["source"])
        pool["destination_add"](pool["destination"])(card)

        yield "draw"

    @announce(entered="card entered graveyard", store=events.card.graveyard)
    def move_to_graveyard(self, card):
        """
        Move a card to the graveyard.

        """

        pool = (yield)
        pool.update(player=self, target=card, destination=self.graveyard,
                    destination_add=attrgetter("append"))

        yield "entered"
        yield

        pool["destination_add"](pool["destination"])(pool["target"])
        yield "entered"

    @announce(removed_from_game="card removed from game", store=events.card)
    def remove_from_game(self, card):
        """
        Remove a card from the game.

        """

        pool = (yield)
        pool.update(player=self, target=card, destination=self.exiled,
                    destination_add=attrgetter("add"))

        yield "removed_from_game"
        yield

        pool["destination_add"](pool["destination"])(pool["target"])
        yield "removed_from_game"


def _game_ender(state):
    @state.events.subscribe(event=events.player["died"], needs=["pool"])
    @announce(handler=state.events, ended="game over", store=events.game)
    def end_game(pangler, pool):
        """
        End the game if there is only one living player left.

        """

        if sum(1 for player in state.players if player.dead) > 1:
            return

        # TODO: Stop all other events
        pool = (yield)

        yield "ended"
        yield

        self.game_over = True
        yield "ended"

    return end_game


class State(object):
    """
    The State object maintains information about the current game state.

    """

    def __init__(self, handler, players):
        """
        Initialize a new game state object.

        """

        super(State, self).__init__()

        if not players:
            raise ValueError("At least one player is required.")

        self.events = handler
        self.players = list(players)
        self.stack = []

        self._turn = itertools.cycle(self.players)
        self._phase = itertools.cycle(PHASES)
        self._subphase = iter([])  # Default value for first advance
        self.end_game = _game_ender(self)
        self.game_over = False

        self.advance()

    def __repr__(self):
        return "<{} Player Game State>".format(len(self.players))

    def advance(self):
        """
        Advance a turn to the next phase.

        """

        try:
            self.subphase = next(self._subphase)
        except StopIteration:
            self.phase, subphase = next(self._phase)
            self._subphase = iter(subphase)
            self.subphase = next(self._subphase, None)
        finally:
            if self.phase == PHASES[0][0] and self.subphase == PHASES[0][1][0]:
                self.turn = next(self._turn)
