from collections import MutableSet, Set
import random

from cardboard.events import events


__all__ = ["UnorderedZone", "OrderedZone", "zone"]


def _zone(name):
    @classmethod
    def zone(cls, game, contents=()):
        return cls(game, name, contents, events["card"]["zones"][name])
    return zone


class UnorderedZone(MutableSet):

    battlefield = _zone("battlefield")
    exile = _zone("exile")
    hand = _zone("hand")

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

    def add(self, e):
        self._contents.add(e)
        self.game.events.trigger(event=self._events["entered"])

    def discard(self, e):
        try:
            self._contents.remove(e)
        except KeyError:
            pass
        else:
            self.game.events.trigger(event=self._events["left"])

    def move(self, e):
        e.zone.remove(e)
        self.add(e)
        e.zone = self

    def remove(self, e):
        try:
            self._contents.remove(e)
        except KeyError:
            raise ValueError(e)
        else:
            self.game.events.trigger(event=self._events["left"])


class OrderedZone(Set):

    graveyard = _zone("graveyard")
    library = _zone("library")
    stack = _zone("stack")

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

    def add(self, e):
        self._contents.add(e)
        self._order.append(e)
        self.game.events.trigger(event=self._events["entered"])

    def clear(self):
        for i in self:
            self.game.events.trigger(event=self._events["left"])

        self._contents.clear()
        self._order = []

    def count(self, e):
        return self._order.count(e)

    def discard(self, e):
        self._contents.discard(e)

        try:
            self._order.remove(e)
        except ValueError:
            pass

    def extend(self, i):
        self._contents.update(i)
        self._order.extend(i)

    def index(self, e):
        return self._order.index(e)

    def move(self, e):
        e.zone.remove(e)
        self.add(e)
        e.zone = self

    def pop(self, i=None):
        if i is None:
            e = self._order.pop()
        else:
            e = self._order.pop(i)

        self._contents.remove(e)
        self.game.events.trigger(event=self._events["left"])
        return e

    def remove(self, e):
        # order matters here, we want ValueError not KeyError
        self._order.remove(e)
        self._contents.remove(e)
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
