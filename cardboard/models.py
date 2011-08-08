from operator import attrgetter, methodcaller

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import backref, relationship

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
    sets = association_proxy("appearances", "set")
    subtypes = association_proxy("subtype_objects", "name")

    def __init__(self, name, type, casting_cost=None, abilities=None,
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

        self.game = None
        self.owner = None
        self.tapped = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Card: {0} ({0.type})>".format(self)

    @property
    def is_permanent(self):
        return self.type.lower() not in {"sorcery", "instant"}

    @collaborate()
    def cast(self):
        """
        Cast a card.

        """

        if self.is_permanent:
            destination = methodcaller("put_into_play")
        else:
            destination = methodcaller("move_to_graveyard")

        pool = (yield)
        pool.update(target=self, destination=destination)

        yield events.card.cast
        yield

        pool["destination"](pool["target"])
        yield events.card.cast

    @collaborate()
    def put_into_play(self):
        """
        Add a card to the play field.

        """

        pool = (yield)
        pool.update(target=self, owner=self.owner, destination=self.game.field,
                    destination_add=attrgetter("add"))

        yield events.card.field.entered
        yield

        pool["destination_add"](pool["destination"])(pool["target"])

        if pool["destination"] is self.game.field:
            pool["target"].owner = pool["owner"]

        yield events.card.field.entered

    @collaborate()
    def move_to_graveyard(self):
        """
        Move a card to the graveyard.

        """

        # TODO: remove from source, include in pool (also in rem_from_game)
        pool = (yield)
        pool.update(target=self, destination=self.owner.graveyard,
                    destination_add=attrgetter("append"))

        yield events.card.graveyard.entered
        yield

        pool["destination_add"](pool["destination"])(pool["target"])
        yield events.card.graveyard.entered

    @collaborate()
    def remove_from_game(self):
        """
        Remove a card from the game.

        """

        pool = (yield)
        pool.update(target=self, player=self.owner,
                    destination=self.owner.exiled,
                    destination_add=attrgetter("add"))

        yield events.card.removed_from_game
        yield

        pool["destination_add"](pool["destination"])(pool["target"])
        yield events.card.removed_from_game


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

    card = relationship("Card",
                        backref=backref("creature", uselist=False))

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
