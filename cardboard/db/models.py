import os.path

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import backref, reconstructor, relationship

from cardboard.db import Base, Session

cardsubtype_table = Table("cardsubtypes", Base.metadata,
    Column("card_id", Integer, ForeignKey("cards.id"), primary_key=True),
    Column("subtype_id", Integer, ForeignKey("subtypes.id"), primary_key=True),
)

cardsupertype_table = Table("cardsupertypes", Base.metadata,
    Column("card_id", Integer, ForeignKey("cards.id"), primary_key=True),
    Column("supertype_id", Integer, ForeignKey("supertypes.id"),
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
        elip = " ... " if len(self.description) > 50 else ""
        return "<Ability Model: {.description:.50}{}>".format(self, elip)


class Card(Base):

    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    mana_cost = Column(String)
    name = Column(String, nullable=False, unique=True)
    type = Column(String, nullable=False)

    power = Column(String(3))
    toughness = Column(String(3))
    loyalty = Column(Integer)

    ability_objects = relationship("Ability", backref="card")

    subtype_objects = relationship("Subtype", secondary=cardsubtype_table,
                                   backref="cards")

    supertype_objects = relationship("Supertype",
                                     secondary=cardsupertype_table,
                                     backref="cards")

    abilities = association_proxy("ability_objects", "description")
    decks = association_proxy("deck_appearances", "deck")
    sets = association_proxy("set_appearances", "set")
    subtypes = association_proxy("subtype_objects", "name")
    supertypes = association_proxy("supertype_objects", "name")

    def __init__(self, name, type, mana_cost=None, abilities=(), subtypes=(),
                 supertypes=(), power=None, toughness=None, loyalty=None):
        super(Card, self).__init__()

        self.abilities = list(abilities)
        self.mana_cost = mana_cost
        self.name = name
        self.subtypes = set(subtypes)
        self.supertypes = set(supertypes)
        self.type = type

        self.power = power
        self.toughness = toughness
        self.loyalty = loyalty

    def __repr__(self):
        return "<Card Model: {.name}>".format(self)


class Deck(Base):

    __tablename__ = "decks"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    cards = association_proxy("card_appearances", "card")

    def __init__(self, name, cards=()):
        super(Deck, self).__init__()

        self.name = name
        self.cards = list(cards)

    def __repr__(self):
        return "<Deck Model: {.name}>".format(self)

    @classmethod
    def load(cls, session, f, name=None):
        """
        Load a deck from a file.

        """

        if name is None:
            name = os.path.splitext(os.path.basename(f.name))[0]

        deck = cls(name)

        for line in f:

            line = line.strip()

            if line == "Sideboard":
                # TODO: Sideboard
                return deck
            else:
                q, c = line.split(None, 1)

                quantity = int(q)
                card = session.query(Card).filter_by(name=c).one()
                appearance = DeckAppearance(card, deck, quantity)

        return deck


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
        return "<{0.deck.name}: {0.card.name} ({0.quantity})>".format(self)


class Set(Base):

    __tablename__ = "sets"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    code = Column(String(2), nullable=False, unique=True)

    cards = association_proxy("card_appearances", "card")

    def __init__(self, name, code, cards=()):
        super(Set, self).__init__()

        self.name = name
        self.code = code
        self.card_appearances = [SetAppearance(c, self, r) for c, r in cards]

    def __repr__(self):
        return "<Set Model: {.name}>".format(self)


class SetAppearance(Base):

    __tablename__ = "appearances"

    rarity = Column(String(1))

    card_id = Column(Integer, ForeignKey("cards.id"), primary_key=True)
    set_id = Column(Integer, ForeignKey("sets.id"), primary_key=True)

    card = relationship("Card", backref="set_appearances")
    set = relationship("Set", backref="card_appearances")

    def __init__(self, card, set, rarity=None):
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
        return "<Subtype Model: {0.name}>".format(self)


class Supertype(Base):

    __tablename__ = "supertypes"

    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey("cards.id"))
    name = Column(String)

    def __init__(self, name):
        super(Supertype, self).__init__()
        self.name = name

    def __repr__(self):
        return "<Supertype Model: {0.name}>".format(self)


Base.metadata.create_all()
