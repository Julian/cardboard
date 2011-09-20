from collections import Set
import random

from cardboard.events import events


__all__ = ["UnorderedZone", "OrderedZone", "zone"]


def _zone(name):
    @classmethod
    def zone(cls, game, contents=()):
        return cls(game, name, contents, events["card"]["zones"][name.lower()])
    return zone


class UnorderedZone(Set):

    battlefield = _zone(u"Battlefield")
    exile = _zone(u"Exile")
    hand = _zone(u"Hand")

    ordered = False

    def __init__(self, game, name, contents=(), _events=None):
        super(UnorderedZone, self).__init__()

        if _events is None:
            _events = events

        self.game = game
        self.name = name

        self._contents = set(contents)
        self._events = _events

    def __contains__(self, e):
        return e in self._contents

    def __iter__(self):
        return iter(self._contents)

    def __len__(self):
        return len(self._contents)

    def __repr__(self):
        return "<Zone: {.name}>".format(self)

    def add(self, e, silent=False):
        if e in self:
            raise ValueError("{} is already in {}".format(e, self))

        self._contents.add(e)

        if not silent:
            self.game.events.trigger(event=self._events["entered"])

    def move(self, e):
        if e in self:
            return

        e.zone.remove(e)
        self.add(e)

    def pop(self, silent=False):
        try:
            return self._contents.pop()
        finally:
            if not silent:
                self.game.events.trigger(event=self._events["left"])

    def remove(self, e, silent=False):
        try:
            self._contents.remove(e)
        except KeyError:
            raise ValueError("{} not in zone.".format(e))
        else:
            if not silent:
                self.game.events.trigger(event=self._events["left"])


class OrderedZone(Set):

    graveyard = _zone(u"Graveyard")
    library = _zone(u"Library")
    stack = _zone(u"Stack")

    ordered = True

    def __init__(self, game, name, contents=(), _events=None):
        super(OrderedZone, self).__init__()

        if _events is None:
            _events = events

        self.game = game
        self.name = name

        self._order = list(contents)
        self._contents = set(self._order)

        self._events = _events

    def __contains__(self, e):
        return e in self._contents

    def __getitem__(self, i):
        # TODO / Beware: Zone slicing
        return self._order[i]

    def __iter__(self):
        return iter(self._order)

    def __len__(self):
        # don't plan on allowing duplicates, but just in case, use order
        return len(self._order)

    def __reversed__(self):
        return reversed(self._order)

    def __repr__(self):
        return "<Zone: {.name}>".format(self)

    def add(self, e, silent=False):
        if e in self:
            raise ValueError("{} is already in {}".format(e, self))

        self._contents.add(e)
        self._order.append(e)

        if not silent:
            self.game.events.trigger(event=self._events["entered"])

    def count(self, e):
        return self._order.count(e)

    def extend(self, i):
        for e in i:
            self.add(e)

    def index(self, e):
        return self._order.index(e)

    def move(self, e):
        if e in self:
            return

        e.zone.remove(e)
        self.add(e)

    def pop(self, i=None, silent=False):
        if i is None:
            e = self._order.pop()
        else:
            e = self._order.pop(i)

        self._contents.remove(e)

        if not silent:
            self.game.events.trigger(event=self._events["left"])

        return e

    def remove(self, e, silent=False):
        if e not in self:
            raise ValueError("{} not in zone.".format(e))

        self._contents.remove(e)
        self._order.remove(e)

        if not silent:
            self.game.events.trigger(event=self._events["left"])

    def reverse(self):
        self._order.reverse()

    def shuffle(self):
        random.shuffle(self._order)


zone = {"battlefield" : UnorderedZone.battlefield,
        "exile" : UnorderedZone.exile,
        "graveyard" : OrderedZone.graveyard,
        "hand" : UnorderedZone.hand,
        "library" : OrderedZone.library,
        "stack" : OrderedZone.stack}
