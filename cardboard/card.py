from operator import attrgetter

from cardboard import exceptions
from cardboard.collaborate import collaborate
from cardboard.events import events


class Card(object):
    def __init__(self, db_card, controller, zone="library"):
        super(Card, self).__init__()

        self.game = controller.game

        self.controller = controller
        self.owner = controller
        self._zone = zone
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
    def zone(self):
        return self._zone

    @zone.setter
    @collaborate()
    def zone(self, to):
        """
        Move the card to a new zone.

        Arguments
        ---------

            * to: the new zone (one of: {})

        """.format(_zones.keys())

        if to not in _zones:
            raise ValueError("'{}' is not a valid zone".format(to))
        elif to == self.zone:
            return

        source_info = _zones[self.zone]
        destination_info = _zones[to]

        pool = (yield)
        pool.update(target=self, to=to)

        yield source_info["removed"]
        yield destination_info["added"]
        yield

        if pool["to"] not in _zones:
            raise ValueError("'{}' is not a valid zone".format(pool["to"]))

        # TODO log here any unforseen error by a somehow miskept zone
        destination_info = _zones[pool["to"]]

        source = source_info["get"](self)
        destination = destination_info["get"](self)

        self._zone = pool["to"]
        source_info["remove"](source)(self)
        destination_info["add"](destination)(self)

        yield source_info["removed"]
        yield destination_info["added"]

        if pool["to"] == "battlefield":
            pool["target"].tapped = False

    @property
    def tapped(self):
        return self._tapped

    @tapped.setter
    @collaborate()
    def tapped(self, t):
        if self.zone != "battlefield":
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
            pool["target"].zone = "graveyard"
            return

        if pool["target"].is_permanent:
            pool["target"].zone = "battlefield"
        else:
            pool["target"].zone = "graveyard"

        yield events.card.cast

_zones = {"battlefield" : {"add" : attrgetter("add"),
                          "added" : events.card.zones.battlefield.entered,
                          "get" : attrgetter("game.battlefield"),
                          "remove" : attrgetter("remove"),
                          "removed" : events.card.zones.battlefield.left},

          "exile" : {"add" : attrgetter("add"),
                      "added" : events.card.zones.exile.entered,
                      "get" : attrgetter("controller.exiled"),
                      "remove" : attrgetter("remove"),
                      "removed" : events.card.zones.exile.left},

          "graveyard" : {"add" : attrgetter("append"),
                          "added" : events.card.zones.graveyard.entered,
                          "get" : attrgetter("controller.graveyard"),
                          "remove" : attrgetter("remove"),
                          "removed" : events.card.zones.graveyard.left},

          "hand" : {"add" : attrgetter("add"),
                  "added" : events.card.zones.hand.entered,
                  "get" : attrgetter("controller.hand"),
                  "remove" : attrgetter("remove"),
                  "removed" : events.card.zones.hand.left},

          "library" : {"add" : attrgetter("append"),
                      "added" : events.card.zones.library.entered,
                      "get" : attrgetter("controller.library"),
                      "remove" : attrgetter("remove"),
                      "removed" : events.card.zones.library.left}}
