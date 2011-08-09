from operator import attrgetter, methodcaller

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import backref, reconstructor, relationship

from cardboard import exceptions
from cardboard.collaborate import collaborate
from cardboard.db import Base
from cardboard.events import events

cardsubtype_table = Table("cardsubtypes", Base.metadata,
        Column("card_id", Integer, ForeignKey("cards.id"), primary_key=True),
        Column("subtype_id", Integer, ForeignKey("subtypes.id"),
               primary_key=True),
)


class Ability(Base):

    __tablename__ = "abilities"

    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey("cards.id"))
    description = Column(String)

    def __init__(self, description):
        super(Ability, self).__init__()
        self.description = description

    def __repr__(self):
        # TODO: Truncate
        return "<Ability: {}>".format(self.description)


class Card(Base):

    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    casting_cost = Column(String)
    name = Column(String, unique=True)
    type = Column(String)

    ability_objects = relationship("Ability", backref="card")

    subtype_objects = relationship("Subtype", secondary=cardsubtype_table,
                                   backref="cards")

    abilities = association_proxy("ability_objects", "description")
    decks = association_proxy("deck_appearances", "deck")
    sets = association_proxy("appearances", "set")
    subtypes = association_proxy("subtype_objects", "name")

    _locations = {"exile" : {"add" : attrgetter("add"),
                             "added" : events.card.exile.entered,
                             "get" : attrgetter("controller.exiled"),
                             "remove" : attrgetter("remove"),
                             "removed" : events.card.exile.left},

                  "field" : {"add" : attrgetter("add"),
                             "added" : events.card.field.entered,
                             "get" : attrgetter("game.field"),
                             "remove" : attrgetter("remove"),
                             "removed" : events.card.field.left},

                  "graveyard" : {"add" : attrgetter("append"),
                                 "added" : events.card.graveyard.entered,
                                 "get" : attrgetter("controller.graveyard"),
                                 "remove" : attrgetter("remove"),
                                 "removed" : events.card.graveyard.left},

                  "hand" : {"add" : attrgetter("add"),
                            "added" : events.card.hand.entered,
                            "get" : attrgetter("controller.hand"),
                            "remove" : attrgetter("remove"),
                            "removed" : events.card.hand.left},

                  "library" : {"add" : attrgetter("append"),
                               "added" : events.card.library.entered,
                               "get" : attrgetter("controller.library"),
                               "remove" : attrgetter("remove"),
                               "removed" : events.card.library.left}}

    def __init__(self, name, type, casting_cost="", abilities=None,
                 subtypes=None):
        super(Card, self).__init__()

        if abilities is None:
            abilities = []
        if subtypes is None:
            subtypes = []

        self.abilities = abilities
        self.casting_cost = casting_cost
        self.name = name
        self.subtypes = subtypes
        self.type = type

        self._init_()

    @reconstructor
    def _init_(self):
        self.game = None

        self.controller = None
        self.tapped = None
        self._location = "library"

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Card: {0} ({0.type})>".format(self)

    @property
    def is_permanent(self):
        return self.type.lower() not in {"sorcery", "instant"}

    @property
    def location(self):
        return self._locations[self._location]["get"](self)

    @collaborate()
    def move_to(self, to):
        """
        Move the card to a new location.

        Arguments
        ---------

            * to: the new location (one of: {})

        """.format(self._locations.keys())

        if to not in self._locations:
            raise ValueError("'{}' is not a valid location".format(to))
        elif to == self._location:
            return

        source_info = self._locations[self._location]
        destination_info = self._locations[to]

        pool = (yield)
        pool.update(target=self, to=to)

        yield source_info["removed"]
        yield destination_info["added"]
        yield

        if pool["to"] not in self._locations:
            raise ValueError("'{}' is not a valid location".format(pool["to"]))

        # TODO log here any unforseen error by a somehow miskept location
        destination_info = self._locations[pool["to"]]

        source = source_info["get"](self)
        destination = destination_info["get"](self)

        self._location = pool["to"]
        source_info["remove"](source)(self)
        destination_info["add"](destination)(self)

        yield source_info["removed"]
        yield destination_info["added"]

        # TODO: Maybe untapping should be done in here if it went to the field

    @collaborate()
    def cast(self):
        """
        Cast a card.

        """

        pool = (yield)
        pool.update(target=self, countered=False)

        # TODO: some form of chaining pools will be needed to handle cards that
        # do things like "whenever a card is put into play as a result of ..."
        yield events.card.cast
        yield

        if not pool["countered"]:

            if pool["target"].is_permanent:
                pool["target"].move_to("field")
                pool["target"].tapped = False
            else:
                pool["target"].move_to("graveyard")

            yield events.card.cast

class Deck(Base):

    __tablename__ = "decks"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    cards = association_proxy("card_appearances", "card")

    def __init__(self, name, cards=None):
        super(Deck, self).__init__()

        self.name = name
        self.cards = cards or []

    def __repr__(self):
        return "<Deck: {0.name} ({0.colors})>".format(self)

    @property
    def colors(self):
        # FIXME: return "".join({card.color for card in self.cards})
        return "UW"


class DeckAppearance(Base):

    __tablename__ = "deck_appearances"

    quantity = Column(Integer)

    card_id = Column(Integer, ForeignKey("cards.id"), primary_key=True)
    deck_id = Column(Integer, ForeignKey("decks.id"), primary_key=True)

    card = relationship("Card", backref="deck_appearances")
    deck = relationship("Deck", backref="card_appearances")

    def __init__(self, card=None, deck=None, quantity=1):
        super(DeckAppearance, self).__init__()

        self.card = card
        self.deck = deck
        self.quantity = quantity

    def __repr__(self):
        return "<{0.deck.name} {0.card} ({0.quantity})>".format(self)


class Set(Base):

    __tablename__ = "sets"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    code = Column(String(2), nullable=False, unique=True)

    cards = association_proxy("appearances", "card")

    def __init__(self, name, code):
        super(Set, self).__init__()

        self.name = name
        self.code = code

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Set: {0}>".format(self)


class SetAppearance(Base):

    __tablename__ = "appearances"

    rarity = Column(String(1))

    card_id = Column(Integer, ForeignKey("cards.id"), primary_key=True)
    set_id = Column(Integer, ForeignKey("sets.id"), primary_key=True)

    card = relationship("Card", backref="appearances")
    set = relationship("Set", backref="appearances")

    def __init__(self, card=None, set=None, rarity=None):
        super(SetAppearance, self).__init__()

        self.card = card
        self.set = set
        self.rarity = rarity

    def __repr__(self):
        return "<{0.card} ({0.set.code}-{0.rarity})>".format(self)


class Creature(Base):

    __tablename__ = "creatures"

    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey("cards.id"))
    base_power = Column(Integer)
    base_toughness = Column(Integer)

    card = relationship("Card", backref=backref("creature", uselist=False))

    def __init__(self, card, power, toughness):
        super(Creature, self).__init__()

        self.card = card

        power, toughness = str(power), str(toughness)

        if "*" not in power:
            power = int(power)
        if "*" not in toughness:
            toughness = int(toughness)

        self.base_power = power
        self.base_toughness = toughness

    def __str__(self):
        return str(self.card)

    def __repr__(self):
        return "<{0.card.type}: {0.card}>".format(self)


class Subtype(Base):

    __tablename__ = "subtypes"

    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey("cards.id"))
    name = Column(String)

    def __init__(self, name):
        super(Subtype, self).__init__()
        self.name = name

    def __repr__(self):
        return "<{0.__class__.__name__}: {0.name}>".format(self)

Base.metadata.create_all()
