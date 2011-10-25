import functools

from cardboard import exceptions, types
from cardboard.cards import cards
from cardboard.core import COLORS_ABBR
from cardboard.db import models, Session
from cardboard.events import events
from cardboard.util import requirements


__all__ = ["Card", "Spell", "Token", "characteristics"]


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


_tap = status("is_tapped", "tapped", "untapped", default=False)
_flip = status("is_flipped", "flipped", "unflipped", default=False)
_turn = status("is_face_up", "turned_face_up", "turned_face_down", True)
_phase = status("is_phased_in", "phased_in", "phased_out", default=True)


class Card(object):

    is_tapped, tap, untap = _tap
    is_flipped, flip, unflip = _flip
    is_face_up, turn_face_up, turn_face_down = _turn
    is_phased_in, phase_in, phase_out = _phase

    require = requirements(
        {"zone" : {"default" : "{self} was expected to be in a {expected.name}"
                               " zone, not '{got}'."}},
    )

    def __init__(self, db_card, _cards=cards):
        super(Card, self).__init__()

        self.game = None

        self.controller = None
        self.owner = None
        self._zone = None

        for attr in {"name", "loyalty", "mana_cost",
                     "types", "subtypes", "supertypes"}:
            setattr(self, attr, getattr(db_card, attr))

        if self.name in _cards:
            self.abilities = _cards[self.name](self, db_card.abilities)
        else:
            self.abilities = [Ability.NotImplemented] * len(db_card.abilities)

        self.power = self.base_power = db_card.power
        self.toughness = self.base_toughness = db_card.toughness

        self.damage = 0
        self._changed_colors = set()

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

        if types.LAND in self.types:
            if self.owner.lands_this_turn < self.owner.lands_per_turn:
                self.owner.lands_this_turn += 1
                # TODO: event trigger?
                return self.game.battlefield.move(self)
            else:
                err = "{} cannot play another land this turn."
                raise exceptions.InvalidAction(err.format(self.owner))

        self.game.stack.add(Spell(self))
        self.game.events.trigger(event=events["card"]["cast"])


class _AbilityNotImplemented(object):
    def __call__(self):
        raise exceptions.NotImplemented("Ability is not implemented.")

    def __repr__(self):
        return "<Ability Not Implemented>"


class Ability(object):

    TYPES = frozenset({"spell", "activated", "triggered", "static"})
    NotImplemented = _AbilityNotImplemented()

    def __init__(self, action, description, type):
        super(Ability, self).__init__()

        self.action = action
        self.description = description
        self.type = type

    def __call__(self):
        self.action()

    def __repr__(self):
        elipsis = " ... " if len(self.description) > 40 else ""
        type = self.type.title()
        return "<{} Ability: {.description:.40}{}>".format(type, self, elipsis)

    def __str__(self):
        return self.description

    @classmethod
    def spell(cls, description):
        return functools.partial(cls, description=description, type="spell")

    @classmethod
    def activated(cls, cost, description):
        @functools.wraps(cls)
        def activated_ability(action):
            a = cls(action=action, description=description, type="activated")
            a.cost = cost
            return a
        return activated_ability

    @classmethod
    def triggered(cls, description, **event_params):
        @functools.wraps(cls)
        def triggered_ability(action):
            a = cls(action=action, description=description, type="triggered")
            a.trigger = event_params
            return a
        return triggered_ability

    @classmethod
    def static(cls, description):
        return functools.partial(cls, description=description, type="static")


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


class Token(object):
    """
    A token is a marker for an object on the battlefield that is not a card.

    .. seealso::
        :ref:`tokens`

    """

    def __init__(self, name="", mana_cost="", colors=(), abilities=None,
                 types=(), subtypes=(), supertypes=(),
                 power=None, toughness=None, loyalty=None):

        super(Token, self).__init__()

        if abilities is None:
            abilities = {}

        self.name = name
        self.mana_cost = str(mana_cost)
        self.colors = set(colors)
        self.abilities = list(abilities)
        self.types = set(types)
        self.subtypes, self.supertypes = set(subtypes), set(supertypes)
        self.power, self.toughness = power, toughness
        self.loyalty = loyalty

    @classmethod
    def from_card(cls, card, **new_characteristics):
        card_chars = characteristics(card)

        # tokens don't have expansions or rules text
        card_chars.pop("expansion")
        card_chars.pop("rules_text")

        card_chars.update(**new_characteristics)
        return cls(**card_chars)


def characteristics(mtg_object):
    """
    Return the characteristics of a M:TG object.

    .. seealso::
        :ref:`characteristics`

    """

    CHARS = ["name", "mana_cost", "colors", "types", "subtypes", "supertypes",
             "abilities", "power", "toughness", "loyalty"]

    chars = {c : getattr(mtg_object, c) for c in CHARS}
    chars["expansion"] = getattr(mtg_object, "expansion", "")
    chars["rules_text"] = getattr(mtg_object, "rules_text", "")

    return chars
