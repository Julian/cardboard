from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import backref, reconstructor, relationship

from cardboard.db import Base

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
        return "<Ability Model: {}>".format(self.description)


class Card(Base):

    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    casting_cost = Column(String)
    name = Column(String, nullable=False, unique=True)
    type = Column(String, nullable=False)

    base_power = Column(String(3))
    base_toughness = Column(String(3))

    ability_objects = relationship("Ability", backref="card")

    subtype_objects = relationship("Subtype", secondary=cardsubtype_table,
                                   backref="cards")

    abilities = association_proxy("ability_objects", "description")
    decks = association_proxy("deck_appearances", "deck")
    sets = association_proxy("appearances", "set")
    subtypes = association_proxy("subtype_objects", "name")

    def __init__(self, name, type, casting_cost=None, abilities=(),
                 subtypes=(), power=None, toughness=None):
        super(Card, self).__init__()

        self.abilities = list(abilities)
        self.casting_cost = casting_cost
        self.name = name
        self.subtypes = list(subtypes)
        self.type = type

        self.power = power
        self.toughness = toughness

        self._init_()

    def __repr__(self):
        return "<Card Model: {.name}>".format(self)


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
        return "<Deck Model: {.name})>".format(self)


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

    def __repr__(self):
        return "<Set Model: {.name}>".format(self)


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
        return "<{0.card.name} ({0.set.code}-{0.rarity})>".format(self)


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
