from operator import attrgetter

from cardboard import cards, exceptions, types
from cardboard.core import COLORS_ABBR
from cardboard.db import models, Session
from cardboard.events import events
from cardboard.util import requirements


__all__ = ["Card", "Spell"]


def status(name, on_event, off_event, default=True):
    """
    Create a status attribute with togglers.

    """

    stupid_nonlocal = [default]

    @property
    def get(self):
        return stupid_nonlocal[0]

    def toggle(turn_on):
        if turn_on:
            event = on_event
        else:
            event = off_event

        def setter(self):
            self.game.require(started=True)
            self.require(zone=self.game.battlefield, **{name : not turn_on})

            stupid_nonlocal[0] = turn_on

            self.game.events.trigger(event=events["card"]["status"][event])

        return setter

    return get, toggle(turn_on=True), toggle(turn_on=False)


class Card(object):

    is_tapped, tap, untap = status(name="is_tapped", on_event="tapped",
                                   off_event="untapped", default=False)

    is_flipped, flip, unflip = status(name="is_flipped", on_event="flipped",
                                      off_event="unflipped", default=False)

    is_face_up, turn_face_up, turn_face_down = status("is_face_up",
                                                      "turned_face_up",
                                                      "turned_face_down",
                                                      default=True)

    is_phased_in, phase_in, phase_out = status("is_phased_in", "phased_in",
                                               "phased_out", default=True)

    require = requirements(
        {"zone" : {"default" : "{self} was expected to be in a {expected.name}"
                               " zone, not '{got}'."}},
    )

    def __init__(self, db_card, _card_behaviors=cards.cards):
        super(Card, self).__init__()

        self.game = None

        self.controller = None
        self.owner = None
        self._zone = None

        for attr in {"name", "type", "subtypes", "mana_cost", "abilities"}:
            setattr(self, attr, getattr(db_card, attr))

        self.power = self.base_power = db_card.power
        self.toughness = self.base_toughness = db_card.toughness

        self.damage = 0
        self._changed_colors = set()

        # XXX: Overly simplistic, this will evolve as I write more cards
        self._execute = _card_behaviors.get(self.name, cards.not_implemented)

    def __lt__(self, other):
        """
        Sort two cards alphabetically.

        """

        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.name < other.name

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return unicode(self.name)

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
                {i for i in self.mana_cost or "" if i.isalpha()})

    @property
    def is_permanent(self):
        return self.type.is_permanent

    @property
    def zone(self):
        if self.game is None or not self.game.started:
            return

        if self._zone is None or self not in self._zone:
            for zone in (self.controller.exile, self.controller.hand,
                         self.game.battlefield, self.game.stack,
                         self.controller.graveyard, self.controller.library):

                if self in zone:
                    self._zone = zone

        return self._zone

    def play(self):
        """
        Play the card.

        For a spell, this is equivalent to casting the spell. For a land,
        playing it is a special action that places the land on the battlefield.

        See :term:`playing` and :term:`cast` in the glossary.

        """

        self.game.require(started=True)

        if self.type == types.LAND:
            if self.owner.lands_this_turn < self.owner.lands_per_turn:
                self.owner.lands_this_turn += 1
                # TODO: event trigger?
                return self.game.battlefield.move(self)
            else:
                err = "{} cannot play another land this turn."
                raise exceptions.InvalidAction(err.format(self.owner))

        self.game.stack.add(Spell(self))
        self.game.events.trigger(event=events["card"]["cast"])


class Spell(object):
    """
    A spell is a card or copy of a card that is placed on the stack.

    """

    def __init__(self, card=None):
        super(Spell, self).__init__()

        self.card = card

    def __str__(self):
        return str(self.card)

    def __unicode__(self):
        return unicode(self.card)

    def __repr__(self):
        return "<Spell: {}>".format(self.card)
