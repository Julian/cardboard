from operator import attrgetter

from sqlalchemy import Column, Date, ForeignKey, Integer, Table, Unicode
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import backref, reconstructor, relationship
from sqlalchemy.orm.collections import MappedCollection
from sqlalchemy.util import OrderedDict

from cardboard.db import Base, Session


card_ability = Table("card_ability", Base.metadata,
    Column("card", Unicode, ForeignKey("card.name"), primary_key=True),
    Column("ability", Integer, ForeignKey("ability.id"), primary_key=True),
)

card_type = Table("card_type", Base.metadata,
    Column("card", Unicode, ForeignKey("card.name"), primary_key=True),
    Column("type", Unicode, ForeignKey("type.name"), primary_key=True),
)

card_subtype = Table("card_subtype", Base.metadata,
    Column("card", Unicode, ForeignKey("card.name"), primary_key=True),
    Column("subtype", Unicode, ForeignKey("subtype.name"), primary_key=True),
)

card_supertype = Table("card_supertype", Base.metadata,
    Column("card", Unicode, ForeignKey("card.name"), primary_key=True),
    Column(
        "supertype", Unicode, ForeignKey("supertype.name"), primary_key=True
    ),
)


class OrderedMappedCollection(OrderedDict, MappedCollection):
    def __init__(self, keyfunc, *args, **kwargs):
        MappedCollection.__init__(self, keyfunc=keyfunc)
        OrderedDict.__init__(self, *args, **kwargs)


class Ability(Base):

    id = Column(Integer, primary_key=True)
    description = Column(Unicode, unique=True)

    def __repr__(self):
        elip = " ... " if len(self.description) > 50 else ""
        return "<Ability Model: {.description:.50}{}>".format(self, elip)


class Card(Base):

    name = Column(Unicode, primary_key=True)
    mana_cost = Column(Unicode)

    type_objects = relationship(
        "Type", secondary=card_type, collection_class=set, backref=backref(
            "cards", lazy="dynamic", collection_class=set,
        ),
    )

    subtype_objects = relationship(
        "Subtype", secondary=card_subtype, collection_class=set,
        backref=backref("cards", lazy="dynamic", collection_class=set),
    )

    supertype_objects = relationship(
        "Supertype", secondary=card_supertype, collection_class=set,
        backref=backref("cards", lazy="dynamic", collection_class=set),
    )

    ability_objects = relationship("Ability",
        backref=backref("cards", lazy="dynamic"), secondary=card_ability
    )

    types = association_proxy(
        "type_objects", "name", creator=lambda name : Type(name=name)
    )
    subtypes = association_proxy(
        "subtype_objects", "name", creator=lambda name : Subtype(name=name)
    )
    supertypes = association_proxy(
        "supertype_objects", "name", creator=lambda name : Supertype(name=name)
    )
    abilities = association_proxy(
        "ability_objects", "description",
        creator=lambda description : Ability(description=description)
    )

    power = Column(Unicode(3))
    toughness = Column(Unicode(3))
    loyalty = Column(Integer)

    sets = association_proxy(
        "set_appearances", "rarity",
        creator=lambda s, r : SetAppearance(set=s, rarity=r)
    )

    def __repr__(self):
        return "<Card Model: {.name}>".format(self)

    @property
    def first_appeared_in(self):
        # XXX: I don't know how to properly do the order_by using SQLAlchemy
        #      yet. See here for an example:
        #      https://groups.google.com/forum/#!topic/sqlalchemy/cQ_Y2gJWj28 
        return min(self.sets, key=attrgetter("released"))

    @property
    def last_appeared_in(self):
        # XXX
        return max(self.sets, key=attrgetter("released"))


class Set(Base):

    code = Column(Unicode(5), primary_key=True)
    name = Column(Unicode, nullable=False, unique=True)
    released = Column(Date, nullable=False)

    cards = association_proxy(
        "card_appearances", "rarity",
        creator=lambda c, r : SetAppearance(card=c, rarity=r),
    )

    def __repr__(self):
        return "<Set Model: {.name}>".format(self)

    @property
    def new_cards(self):
        """
        The cards that first appear in this set, and not in any earlier one.

        """

        # XXX: Once this is worked out on the Card model there will probably be
        #      a better way to do it here too.
        return {card for card in self.cards if card.first_appeared_in == self}

    @property
    def reprints(self):
        """
        The cards that were reprinted from earlier sets.

        """

        return {card for card in self.cards if card.first_appeared_in != self}


class SetAppearance(Base):

    card_name = Column(Integer, ForeignKey("card.name"), primary_key=True)
    set_code = Column(Integer, ForeignKey("set.code"), primary_key=True)
    rarity = Column(Unicode(1), primary_key=True)

    card = relationship(Card,
        backref=backref(
            "set_appearances",
            cascade="all, delete-orphan",
            collection_class=(
                lambda : OrderedMappedCollection(attrgetter("set"))
            ),
        )
    )

    set = relationship(Set,
        backref=backref(
            "card_appearances",
            cascade="all, delete-orphan",
            order_by=set_code,
            collection_class=(
                lambda : OrderedMappedCollection(attrgetter("card"))
            ),
        )
    )

    def __repr__(self):
        name = getattr(self.card, "name", None)
        code = getattr(self.set, "code", None)
        return "<{} ({}-{.rarity})>".format(name, code, self)


class Type(Base):

    name = Column(Unicode, primary_key=True)

    def __repr__(self):
        return "<Type Model: {.name}>".format(self)


class Subtype(Base):

    name = Column(Unicode, primary_key=True)

    def __repr__(self):
        return "<Subtype Model: {.name}>".format(self)


class Supertype(Base):

    name = Column(Unicode, primary_key=True)

    def __repr__(self):
        return "<Supertype Model: {.name}>".format(self)


Base.metadata.create_all()
