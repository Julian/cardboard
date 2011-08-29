from operator import attrgetter

from cardboard import exceptions, types
from cardboard.db import models, Session
from cardboard.events import events
from cardboard.util import check_started


COLORS = {"B" : "black",
          "G" : "green",
          "R" : "red",
          "U" : "blue",
          "W" : "white"}


class Card(object):

    def __init__(self, db_card):
        super(Card, self).__init__()

        self.game = None
        self.controller = None
        self.owner = None
        self.zone = None

        for attr in {"name", "type", "subtypes", "mana_cost", "abilities"}:
            setattr(self, attr, getattr(db_card, attr))

        self.power = self.base_power = db_card.power
        self.toughness = self.base_toughness = db_card.toughness
        self.damage = 0

        self._changed_colors = set()

        self._tapped = None
        self._flipped = None
        self._face_up = None
        self._phased_in = None

    def __lt__(self, other):
        """
        Sort two cards alphabetically.

        """

        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.name < other.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Card: {}>".format(self)

    @classmethod
    def load(cls, name, session=None):
        if session is None:
            session = Session()

        db_card = session.query(models.Card).filter_by(name=name).one()
        return cls(db_card)

    @property
    def colors(self):
        return (self._changed_colors or
                {COLORS[i] for i in self.mana_cost if i.isalpha()})

    @property
    def is_permanent(self):
        return self.type.is_permanent

    @property
    def tapped(self):
        return self._tapped

    def cast(self):
        """
        Cast a card.

        """

        check_started(self.game)

        if self.is_permanent:
            self.game.battlefield.move(self)
        else:
            self.controller.graveyard.move(self)

        self.game.events.trigger(event=events["card"]["cast"])

    def tap(self):
        check_started(self.game)

        if self.zone != self.game.battlefield:
            raise exceptions.RuntimeError("{} is not in play.".format(self))
        elif self._tapped:
            raise exceptions.RuntimeError("{} is already tapped.".format(self))

        self._tapped = True
        self.game.events.trigger(event=events["card"]["tapped"])

    def untap(self):
        check_started(self.game)

        if self.zone != self.game.battlefield:
            raise exceptions.InvalidAction("{} is not in play.".format(self))
        elif self._tapped is not None and not self._tapped:
            err = "{} is already untapped.".format(self)
            raise exceptions.InvalidAction(err)

        self._tapped = False
        self.game.events.trigger(event=events["card"]["untapped"])
