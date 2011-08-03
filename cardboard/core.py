"""
Cardboard core

"""

import itertools

import panglery

from cardboard.events import events

PHASES = [("beginning", ["untap", "draw", "upkeep"]),
          ("first main", []),
          ("combat", ["beginning", "declare attackers", "declare blockers",
                      "combat damage", "end"]),
          ("second main", []),
          ("ending", ["end", "cleanup"])]


class Player(object):
    """
    A player in a game.

    """

    def __init__(self, event_handler, deck, name="", hand_size=7, life=20):
        super(Player, self).__init__()

        self.events = event_handler

        self.name = str(name)
        self._life = int(life)
        self.deck = deck
        self.graveyard = []

        # bypass events for first draw
        self.hand = {self.deck.pop() for _ in range(hand_size)} 

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Player: {}>".format(self.name or "Unnamed")

    @property
    def life(self):
        return self._life

    @life.setter
    def life(self, amount):
        amount = int(amount)

        if amount > self.life:
            event = events["life gained"]
        elif amount == self.life:
            return
        else:
            event = events["life lost"]

        self._life = amount
        self.events.trigger(event=event, player=self)

        if self.life <= 0:
            self.events.trigger(event=events["player died"], player=self)

    def draw(self, cards=1):
        """
        Draw cards from the deck.

        """

        if cards > len(self.deck):
            self.life -= cards - len(self.deck)
            self.draw(len(self.deck))
        else:
            for i in range(cards):
                self.events.trigger(event=events["card drawn"], player=self)
            drawn = [self.deck.pop() for _ in range(cards)]
            self.hand.update(drawn)
            return drawn

    def move_to_graveyard(self, card):
        self.graveyard.append(card)
        self.events.trigger(event=events["card added to graveyard"], card=card)

class State(object):
    """
    The State object maintains information about the current game state.

    """

    def __init__(self, event_handler, players):
        """
        Initialize a new game state object.

        """

        super(State, self).__init__()

        if not players:
            raise ValueError("At least one player is required.")

        self.events = event_handler
        self.players = list(players)

        self._turn = itertools.cycle(self.players)
        self._phase = itertools.cycle(PHASES)
        self._subphase = iter([])  # Default value for first advance

        self.advance()

        self.events.subscribe(self._check_game_over,
                              event=events["player died"])

    def __repr__(self):
        return "<{} Player Game>".format(len(self.players))

    def _check_game_over(self, pangler):
        if self.game_over:
            self.events.trigger(event=events["game over"])

    @property
    def game_over(self):
        return sum(1 for player in self.players if player.life > 0) == 1

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
