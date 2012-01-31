"""
Cardboard core

"""

from collections import deque
from random import shuffle

from cardboard import events, exceptions, types
from cardboard.phases import phases
from cardboard.util import requirements
from cardboard.zone import zone


__all__ = ["COLORS", "COLORS_ABBR",
           "Game", "ManaPool", "Player", "TurnManager"]

COLORS = ("white", "blue", "black", "red", "green")
COLORS_ABBR = dict(zip("WUBRG", COLORS))


class Game(object):
    """
    The Game object maintains information about the current game state.

    """

    require = requirements({"started" : {True : "{self} has already started.",
                                         False : "{self} has not started."}})

    def __init__(self, handler):
        """
        Initialize a new game state object.

        """

        self.events = handler

        self.ended = None

        self.battlefield = zone["battlefield"](game=self)
        self.stack = zone["stack"](game=self)

        self.teams = []
        self.turn = TurnManager(self)

    def __repr__(self):
        return "<{} Player Game>".format(len(self.players))

    @property
    def players(self):
        return set().union(*self.teams)

    @property
    def started(self):
        return self.ended is not None

    @property
    def zones(self):
        """
        Get all of the zones present in the game.

        Returns a dict of dicts, where the keys are all of the game's players
        and the values are a dict mapping the names of each zone to the
        player's zone object of that zone. The game's battlefield and stack
        zones are also present in a top level key named "shared".

        """

        zones = {
            p : {z.name : z for z in {p.exile, p.graveyard, p.hand, p.library}}
            for p in self.players
        }
        zones["shared"] = dict(battlefield=self.battlefield, stack=self.stack)
        return zones

    def add_player(self, team=None, **kwargs):
        """
        Add a new player to the game.

        """

        player = Player(game=self, **kwargs)
        self.add_existing_player(player, team)
        return player

    def add_existing_player(self, player, team=None):
        """
        Add an existing player to the game.

        """

        self.require(started=False)

        if team is None:
            self.teams.append({player})
        else:
            if team not in self.teams:
                raise ValueError("{} has no such team {}".format(self, team))

            team.add(player)

    def _start(self):
        """
        Perform the internal steps necessary to get the game ready to start.

        """

        self.require(
            self.players, msg="Starting the game requires at least one player."
        )

        self.ended = False
        self.turn._start()  # Tell the turn manager that the game is starting.

    def start(self):
        """
        Start the game.

        """

        self.require(started=False)
        self.events.trigger(event=events.GAME_BEGAN, game=self)
        self._start()

        for player in self.players:
            player.library.shuffle()
            player.draw(player.hand_size)

    def _check_for_win(self):
        """
        Check if there is a player that has won the game via last man standing.

        """

        for player in self.players:
            if all(opponent.dead for opponent in player.opponents):
                # XXX: Simultaneous victory
                self.end()

    def end(self):
        """
        End the game unconditionally.

        """

        self.ended = True
        # TODO: Stop all other events
        self.events.trigger(event=events.GAME_ENDED, game=self)

    def grant_priority(self, to=None):
        """
        Grant priority to a player.

        .. seealso::
            :ref:`grant-priority`

        """

        if to is None:
            to = self.turn.active_player

        self._check_state_based_actions()
        # TODO: Put triggered abilities on the stack
        to.user.priority_granted()

    def _check_state_based_actions(self):
        """
        Check for state based actions.

        .. seealso::
            :ref:`sba-list`

        """

        for player in self.players:
            if player.life <= 0:
                player.die(reason="life")
            elif player._drew_from_empty_library:
                player.die(reason="library")
            elif player.poison >= 10:
                player.die(reason="poison")

        # TODO: if any spells are anywhere but the stack: cease to exist
        #       if any cards are anywhere but battlefield or stack: ""
        #       :ref:`planeswalker-uniqueness-rule`
        #       :ref:`legend-rule`
        #       :ref:`world-rule`
        #       The rest of them in :ref:`sba-list`
        #
        #       As per :ref:`sba-replacement` and the rest of the section,
        #           these should not be iterative, and should check replacement

        for card in self.battlefield:

            if card.type == types.CREATURE:
                if card.toughness <= 0:
                    card.owner.graveyard.move(card)
                elif card.damage >= card.toughness or card._deathtouch_damage:
                    # TODO: Regenerate
                    card.owner.graveyard.move(card)

            elif card.type == types.PLANESWALKER:
                if not card.loyalty:
                    card.owner.graveyard.move(card)
            elif card.type == types.ENCHANTMENT:
                # if types.enchantment.subtypes["Aura"] in card.subtypes:
                if card.attached_to is None:
                    card.owner.graveyard.move(card)


def _make_color(name):

    _color = "_" + name

    @property
    def color(self):
        return getattr(self, _color)

    @color.setter
    def color(self, amount):

        self.owner.game.require(started=True)
        current = getattr(self, name)

        if amount < 0:
            err = "{} mana pool would be negative."
            raise ValueError(err.format(name.title()))
        elif amount == current:
            return
        elif amount > current:
            event = events.MANA_ADDED
        elif amount < current:
            event = events.MANA_REMOVED

        self.owner.game.events.trigger(
            event=event, color=name, player=self.owner, amount=abs(amount)
        )

        setattr(self, _color, amount)

    return color


class ManaPool(object):
    """
    A player's mana pool.

    """

    POOLS = ("colorless",) + COLORS

    _white = _blue = _black = _red = _green = _colorless = 0
    colorless, white, blue, black, red, green = (_make_color(p) for p in POOLS)

    def __init__(self, owner):
        self.owner = owner

    def __iter__(self):
        return iter(self.contents)

    def __repr__(self):
        return "({}, {}W, {}U, {}B, {}R, {}G)".format(*self.contents)

    @property
    def contents(self):
        return tuple(getattr(self, color) for color in self.POOLS)

    @property
    def is_empty(self):
        return not any(self.contents)

    def add(self, colorless=0, white=0, blue=0, black=0, red=0, green=0):
        self.colorless += colorless
        self.white += white
        self.blue += blue
        self.black += black
        self.red += red
        self.green += green

    def empty(self):
        for color in self.POOLS:
            setattr(self, color, 0)

    def can_pay(self, colorless=0, white=0, blue=0, black=0, red=0, green=0):
        payment = (colorless, white, blue, black, red, green)
        return all(int(i) <= j for i, j in zip(payment, self.contents))

    def pay(self, colorless=0, white=0, blue=0, black=0, red=0, green=0):
        if not self.can_pay(colorless, white, blue, black, red, green):
            raise exceptions.InvalidAction("Not enough mana for payment.")
        return self.add(-colorless, -white, -blue, -black, -red, -green)


class Player(object):
    """
    A player.

    """

    require = requirements({"dead" : {True : "{self} is dead.",
                                      False : "{self} is alive."}})

    def __init__(self, game, library, user, name=""):
        self.game = game
        self.user = user
        self.name = name

        self.death_by = None

        self.hand_size = 7
        self._life = 20
        self.poison = 0

        self.lands_per_turn = 1
        self.lands_this_turn = 0

        self.mana_pool = ManaPool(self)

        self.exile = zone["exile"](game=game, owner=self)
        self.graveyard = zone["graveyard"](game=game, owner=self)
        self.hand = zone["hand"](game=game, owner=self)
        self.library = zone["library"](game=game, contents=library, owner=self)

        for card in self.library:
            card.game = self.game
            card.controller = card.owner = self

        self._drew_from_empty_library = False

    def __repr__(self):
        return "<Player{}>".format(self.name and ": " + self.name)

    @property
    def battlefield(self):
        """
        Get the cards on the battlefield currently under the player's control.

        """

        return {c for c in self.game.battlefield if c.controller == self}

    @property
    def dead(self):
        """
        Am... am I... dead?

        """

        return self.death_by is not None

    @property
    def life(self):
        """
        Get the current life total.

        """

        return self._life

    @life.setter
    def life(self, amount):
        if amount == self.life:
            return
        elif amount > self.life:
            event = events.LIFE_GAINED
        else:
            event = events.LIFE_LOST

        self.game.events.trigger(
            event=event, player=self, amount=abs(amount - self.life)
        )
        self._life = amount

    @property
    def opponents(self):
        """
        The player's opponents (not subdivided into teams).

        """

        return set().union(*(t for t in self.game.teams if self not in t))

    @property
    def team(self):
        """
        The player's entire team.

        """

        team, = (team for team in self.game.teams if self in team)
        return team

    def concede(self):
        """
        I can go on no longer.

        """

        self.game.events.trigger(event=events.PLAYER_CONCEDED, player=self)
        self.die(reason="concede")

    def die(self, reason):
        """
        End the player's sorrowful life.

        Arguments:

            * reason
                * concede
                * life: life total was <= 0
                * library: drew from an empty library
                * poison: 10 or more poison counters
                * <an effect>

                .. seealso::
                    :ref:`losing`

        """

        self.require(dead=False)

        self.death_by = reason
        self.game.events.trigger(
            event=events.PLAYER_DIED, player=self, reason=reason
        )
        self.game._check_for_win()

    def draw(self, cards=1):
        """
        Draw cards from the library.

        """

        cards = int(cards)

        if cards == 0:
            return
        elif cards < 0:
            raise ValueError("Cannot draw a negative number of cards.")
        elif cards > len(self.library):
            self._drew_from_empty_library = True
            return self.draw(len(self.library))
        else:
            for i in range(cards):
                self.hand.add(self.library.pop())
                self.game.events.trigger(event=events.DRAW, player=self)


class TurnManager(object):
    def __init__(self, game):
        self.game = game

        self._first = None
        self.number = None
        self.order = None

        self._phases = deque(phases)
        self._steps = iter(self._phases[0])
        self._step = next(self._steps)

    @property
    def active_player(self):
        if self.game.started:
            return self.order[0]

    @property
    def info(self):
        """
        Return displayable information about the current turn.

        """

        phase, step = self.phase, self.step

        if len(phase) == 1:
            step = None

        if phase is not None:
            phase = phase.name.title().replace("_", " ")
        if step is not None:
            step = step.__name__.title().replace("_", " ").replace("Of", "of")

        return phase, step

    @property
    def phase(self):
        if self.game.started:
            return self._phases[0]

    @property
    def step(self):
        if self.game.started:
            return self._step

    def _start(self):
        self.order = deque(self.game.players)
        shuffle(self.order)
        self._first = self.active_player
        self.number = 1

        self.game.events.trigger(
            event=events.PHASE_BEGAN, phase=self.phase.name.lower(),
            player=self.active_player,
        )

        self.step(self.game)

    def next(self):
        """
        Advance a turn to the next phase or step.

        """

        self.game.require(started=True)

        try:
            next_step = next(self._steps)
        except StopIteration:

            self.game.events.trigger(
                event=events.PHASE_ENDED, phase=self.phase.name.lower(),
                player=self.active_player,
            )

            self._phases.rotate(-1)
            self._steps = iter(self.phase)
            self._step = next(self._steps)

            self.game.events.trigger(
                event=events.PHASE_BEGAN, phase=self.phase.name.lower(),
                player=self.active_player,
            )

        else:
            self._step = next_step
        finally:
            self.step(self.game)

            for player in self.game.players:
                player.mana_pool.empty()

        # is it the last step of the last phase?
        if self.phase == phases[0] and self.step == phases[0][0]:
            self.end()

    def end(self):
        """
        End the current turn and advance the game to the next player's turn.

        """

        self.game.require(started=True)

        self.game.events.trigger(
            event=events.TURN_ENDED, player=self.active_player,
            number=self.number
        )
        self.order.rotate(-1)

        if self.active_player == self._first:
            self.number += 1

        self.game.events.trigger(
            event=events.TURN_BEGAN, player=self.active_player,
            number=self.number
        )

        # XXX: end from middle of a turn
