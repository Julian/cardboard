from operator import attrgetter

from cardboard import exceptions
from cardboard.collaborate import collaborate
from cardboard.events import events


class Card(object):
    def __init__(self, db_card, controller, location="library"):
        super(Card, self).__init__()

        self.game = controller.game

        self.controller = controller
        self._location = location
        self._tapped = None

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
    def location(self):
        return self._location

    @location.setter
    @collaborate()
    def location(self, to):
        """
        Move the card to a new location.

        Arguments
        ---------

            * to: the new location (one of: {})

        """.format(_locations.keys())

        if to not in _locations:
            raise ValueError("'{}' is not a valid location".format(to))
        elif to == self.location:
            return

        source_info = _locations[self.location]
        destination_info = _locations[to]

        pool = (yield)
        pool.update(target=self, to=to)

        yield source_info["removed"]
        yield destination_info["added"]
        yield

        if pool["to"] not in _locations:
            raise ValueError("'{}' is not a valid location".format(pool["to"]))

        # TODO log here any unforseen error by a somehow miskept location
        destination_info = _locations[pool["to"]]

        source = source_info["get"](self)
        destination = destination_info["get"](self)

        self._location = pool["to"]
        source_info["remove"](source)(self)
        destination_info["add"](destination)(self)

        yield source_info["removed"]
        yield destination_info["added"]

        if pool["to"] == "field":
            pool["target"].tapped = False

    @property
    def tapped(self):
        return self._tapped

    @tapped.setter
    @collaborate()
    def tapped(self, t):
        if self.location != "field":
            raise exceptions.RuntimeError("{} is not in play.".format(self))

        if t:
            event = events.card.tapped
        else:
            event = events.card.untapped

        pool = (yield)
        pool.update(target=self)

        yield event
        yield

        self._tapped = bool(t)

        yield event

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

        if pool["countered"]:
            yield events.card.countered
            pool["target"].location = "graveyard"
            return

        if pool["target"].is_permanent:
            pool["target"].location = "field"
        else:
            pool["target"].location = "graveyard"

        yield events.card.cast

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
