"""
Cardboard core

"""

from operator import attrgetter, methodcaller
import itertools

from cardboard.events import collaborate, events

PHASES = [("beginning", ["untap", "draw", "upkeep"]),
          ("first main", []),
          ("combat", ["beginning", "declare attackers", "declare blockers",
                      "combat damage", "end"]),
          ("second main", []),
          ("ending", ["end", "cleanup"])]


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
        self.game = self.owner.game

        for color in self.COLORS:
            setattr(self, "_" + color, 0)

    def __repr__(self):
        pool = (getattr(self, c) for c in self.COLORS)
        return "[{}B, {}G, {}R, {}U, {}W, {}]".format(*pool)


def _make_player_factory(game_state):

    e = events

    class Player(object):
        """
        A player.

        """

        game = game_state

        def __init__(self, library, hand_size=7, life=20):
            super(Player, self).__init__()

            self.dead = False
            self._life = int(life)

            self.hand = set()
            self.library = library
            self.draw(hand_size)

            self.exiled = set()
            self.graveyard = []
            self.mana_pool = ManaPool(self)

        def __repr__(self):
            return "<Player: {} Life>".format(self.life)

        @property
        def life(self):
            return self._life

        @life.setter
        @collaborate()
        def life(self, amount):

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

            # TODO: Reason
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

            yield events.player.draw
            yield

            card = pool["source_get"](pool["source"])
            pool["destination_add"](pool["destination"])(card)

            yield events.player.draw

        @collaborate()
        def cast(self, card):
            """
            Cast a card.

            """

            if card.is_permanent:
                destination = self.put_into_play
            else:
                destination = self.move_to_graveyard

            pool = (yield)
            pool.update(owner=self, target=card, destination=destination)

            yield events.card.cast
            yield

            pool["destination"](pool["target"])
            yield events.card.cast

        @collaborate()
        def put_into_play(self, card):
            """
            Add a card to the play field.

            """

            pool = (yield)
            pool.update(owner=self, target=card, destination=self.game.field,
                        destination_add=attrgetter("add"))

            yield events.card.field.entered
            yield

            pool["destination_add"](pool["destination"])(pool["target"])

            if pool["destination"] is self.game.field:
                pool["target"].owner = pool["owner"]

            yield events.card.field.entered

        @collaborate()
        def move_to_graveyard(self, card):
            """
            Move a card to the graveyard.

            """

            # TODO: remove from source, include in pool (also in rem_from_game)
            pool = (yield)
            pool.update(target=card, destination=self.graveyard,
                        destination_add=attrgetter("append"))

            yield events.card.graveyard.entered
            yield

            pool["destination_add"](pool["destination"])(pool["target"])
            yield events.card.graveyard.entered

        @collaborate()
        def remove_from_game(self, card):
            """
            Remove a card from the game.

            """

            pool = (yield)
            pool.update(player=self, target=card, destination=self.exiled,
                        destination_add=attrgetter("add"))

            yield events.card.removed_from_game
            yield

            pool["destination_add"](pool["destination"])(pool["target"])
            yield events.card.removed_from_game

    return Player


def _game_ender(game):
    @game.events.subscribe(event=events.player.died, needs=["pool"])
    @collaborate()
    def end_game(pangler, pool):
        """
        End the game if there is only one living player left.

        """

        if sum(1 for player in game.players if player.dead) > 1:
            return

        # TODO: Stop all other events
        pool = (yield)

        yield events.game.ended
        yield

        self.game_over = True
        yield events.game.ended

    return end_game


class Game(object):
    """
    The Game object maintains information about the current game state.

    """

    def __init__(self, handler):
        """
        Initialize a new game state object.

        """

        super(Game, self).__init__()

        self.events = handler

        self.field = set()
        self.players = []
        self.Player = _make_player_factory(self)

        self.end_game = _game_ender(self)

    def __repr__(self):
        return "<{} Player Game>".format(len(self.players))

    def add_player(self, *args, **kwargs):
        player = self.Player(*args, **kwargs)
        self.players.append(player)
        return player

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

    def start(self):
        self.events.trigger(events.game.started)

        self.game_over = False

        self._turn = itertools.cycle(self.players)
        self._phase = itertools.cycle(PHASES)
        self._subphase = iter([])  # Default value for first advance

        self.advance()
