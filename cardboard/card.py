from operator import attrgetter

from cardboard import exceptions, models
from cardboard.events import events
from cardboard.db import Session


class Card(object):

    def __init__(self, db_card, controller):
        super(Card, self).__init__()

        self.game = controller.game

        self.controller = controller
        self.owner = controller
        self._tapped = None
        self._zone = self.controller.library

        for attr in {"name", "type", "subtypes", "casting_cost", "abilities"}:
            setattr(self, attr, getattr(db_card, attr))

        self.base_power = db_card.power
        self.base_toughness = db_card.toughness

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Card: {}>".format(self)

    @property
    def is_permanent(self):
        return self.type.lower() not in {"sorcery", "instant"}

    @property
    def zone(self):
        return self._zone

    @zone.setter
    def zone(self, to):
        """
        Move the card to a new zone.

        Arguments
        ---------

            * to: valid zones are the battlefield, or the controller's exile,
                  hand, graveyard or library

        """

        if to not in [self.game.battlefield, self.controller.hand,
                      self.controller.exile, self.controller.graveyard,
                      self.controller.library]:
            raise ValueError("'{}' is not a valid zone".format(to))
        elif to == self.zone:
            return

        self._zone.remove(self)

        event = events["card"]["zones"][self._zone.name]["left"]
        self.game.events.trigger(event=event)

        self._zone = to

        event = events["card"]["zones"][self._zone.name]["entered"]
        self.game.events.trigger(event=event)

        self._zone.add(self)

        if to == self.game.battlefield:
            self.tapped = False

    @classmethod
    def load(cls, name, controller, session=None):
        if session is None:
            session = Session()

        db_card = session.query(models.Card).filter_by(name=name).one()
        return cls(db_card, controller)

    @property
    def tapped(self):
        return self._tapped

    @tapped.setter
    def tapped(self, t):
        if self.zone != self.game.battlefield:
            raise exceptions.RuntimeError("{} is not in play.".format(self))

        self._tapped = bool(t)

        if t:
            self.game.events.trigger(event=events["card"]["tapped"])
        else:
            self.game.events.trigger(event=events["card"]["untapped"])

    def cast(self):
        """
        Cast a card.

        """

        if self.is_permanent:
            self.zone = self.game.battlefield
        else:
            self.zone = self.controller.graveyard

        self.game.events.trigger(event=events["card"]["cast"])
