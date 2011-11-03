import os.path

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import backref, reconstructor, relationship

from cardboard.db import Base, Session


card_ability = Table("card_ability", Base.metadata,
    Column("card", String, ForeignKey("card.name"), primary_key=True),
    Column("ability", Integer, ForeignKey("ability.id"), primary_key=True),
)


card_type = Table("card_type", Base.metadata,
    Column("card", String, ForeignKey("card.name"), primary_key=True),
    Column("type", Integer, ForeignKey("type.name"), primary_key=True),
)


card_subtype = Table("card_subtype", Base.metadata,
    Column("card", String, ForeignKey("card.name"), primary_key=True),
    Column("subtype", Integer, ForeignKey("subtype.name"), primary_key=True),
)


card_supertype = Table("card_supertype", Base.metadata,
    Column("card", String, ForeignKey("card.name"), primary_key=True),
    Column(
        "supertype", Integer, ForeignKey("supertype.name"), primary_key=True
    ),
)


class Ability(Base):

    id = Column(Integer, primary_key=True)
    description = Column(String, unique=True)

    def __repr__(self):
        elip = " ... " if len(self.description) > 50 else ""
        return "<Ability Model: {.description:.50}{}>".format(self, elip)


class Card(Base):

    name = Column(String, nullable=False, primary_key=True)
    mana_cost = Column(String)

    types = relationship("Type", backref="cards", secondary=card_type)
    subtypes = relationship("Subtype", backref="cards", secondary=card_subtype)
    supertypes = relationship(
        "Supertype", backref="cards", secondary=card_supertype
    )

    abilities = relationship(
        "Ability", backref="cards", secondary=card_ability
    )

    power = Column(String(3))
    toughness = Column(String(3))
    loyalty = Column(Integer)

    def __repr__(self):
        return "<Card Model: {.name}>".format(self)


class Deck(Base):

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    cards = association_proxy("card_appearances", "card")

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

    quantity = Column(Integer)

    card_name = Column(String, ForeignKey("card.name"), primary_key=True)
    deck_id = Column(Integer, ForeignKey("deck.id"), primary_key=True)

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

    code = Column(String(2), nullable=False, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    cards = association_proxy("card_appearances", "card")

    def __repr__(self):
        return "<Set Model: {.name}>".format(self)


class SetAppearance(Base):

    rarity = Column(String(1))

    card_name = Column(Integer, ForeignKey("card.name"), primary_key=True)
    set_code = Column(Integer, ForeignKey("set.code"), primary_key=True)

    card = relationship("Card", backref="set_appearances")
    set = relationship("Set", backref="card_appearances")

    def __repr__(self):
        return "<{0.card.name} ({0.set.code}-{0.rarity})>".format(self)


class Type(Base):

    name = Column(String, primary_key=True)

    def __repr__(self):
        return "<Type Model: {0.name}>".format(self)


class Subtype(Base):

    name = Column(String, primary_key=True)

    def __repr__(self):
        return "<Subtype Model: {0.name}>".format(self)


class Supertype(Base):

    name = Column(String, primary_key=True)

    def __repr__(self):
        return "<Supertype Model: {0.name}>".format(self)


Base.metadata.create_all()
