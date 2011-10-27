from collections import Set
import random

from cardboard.events import events


__all__ = ["UnorderedZone", "OrderedZone", "zone"]


# TODO: Clarify / make zone operations atomic
#       Write a Mixin


def _zone(name):
    """
    Create a zone classmethod from the zone name.

    """

    _events = events["card"]["zones"][name]

    @classmethod
    def zone(cls, game, contents=(), owner=None):
        return cls(game, name, contents, owner=owner, _events=_events)
    return zone


class ZoneMixin(object):
    def __init__(self, game, name, contents=(), owner=None, _events=None):
        super(ZoneMixin, self).__init__()

        if _events is None:
            _events = events

        self._events = _events

        self.game = game
        self.name = name
        self.owner = owner

        self._contents = set(contents)

    def __contains__(self, e):
        return e in self._contents

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Zone: {}>".format(self)

    def update(self, i, silent=False):
        """
        Add multiple elements at the same time.

        Analogous to list.extend and set.update.
        """

        for e in i:
            self.add(e, silent=silent)

    def move(self, e, silent=False):
        """
        Remove a card from its current zone and place it in this zone.

        Raises a ValueError for cards that are already present.

        """

        if e in self:
            raise ValueError("'{}' is already in the {} zone.".format(e, self))

        e.zone.remove(e, silent=silent)
        self.add(e, silent=silent)


class UnorderedZone(ZoneMixin):

    battlefield = _zone(u"battlefield")
    exile = _zone(u"exile")
    hand = _zone(u"hand")

    ordered = False

    def __iter__(self):
        return iter(self._contents)

    def __len__(self):
        return len(self._contents)

    def add(self, e, silent=False):
        if not silent and self.owner is not None and self.owner != e.owner:
            # TODO: log things that misbehaved
            return getattr(e.owner, self.name).add(e)

        if e in self:
            if self.owner is not None:
                s = "in {}'s {}".format(self.owner, self.name)
            else:
                s = "on the {}".format(self.name)

            raise ValueError("{} is already {}.".format(e, s))

        self._contents.add(e)

        if not silent:
            self.game.events.trigger(event=self._events["entered"], card=e)

    def pop(self, silent=False):
        try:
            e = self._contents.pop()
            return e
        finally:
            if not silent:
                self.game.events.trigger(event=self._events["left"], card=e)

    def remove(self, e, silent=False):
        try:
            self._contents.remove(e)
        except KeyError:
            raise ValueError("'{}' is not in the {} zone.".format(e, self))
        else:
            if not silent:
                self.game.events.trigger(event=self._events["left"], card=e)


class OrderedZone(ZoneMixin):

    graveyard = _zone(u"graveyard")
    library = _zone(u"library")
    stack = _zone(u"stack")

    ordered = True

    def __init__(self, game, name, contents=(), owner=None, _events=None):
        self._order = list(contents)

        super(OrderedZone, self).__init__(
            game=game, name=name, contents=self._order,
            owner=owner, _events=_events
        )

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

    def add(self, e, silent=False):
        # a safeguard against cards that are accidentally being moved to
        # another zone other than their owners (TODO: log misbehavers)
        if not silent and self.owner is not None and self.owner != e.owner:
            return getattr(e.owner, self.name).add(e)

        if e in self:
            if self.owner is not None:
                s = "in {}'s {}".format(self.owner, self.name)
            else:
                s = "on the {}".format(self.name)

            raise ValueError("{} is already {}.".format(e, s))

        self._contents.add(e)
        self._order.append(e)

        if not silent:
            self.game.events.trigger(event=self._events["entered"], card=e)

    def count(self, e):
        return self._order.count(e)

    def index(self, e):
        return self._order.index(e)

    def pop(self, i=None, silent=False):
        if i is None:
            e = self._order.pop()
        else:
            e = self._order.pop(i)

        self._contents.remove(e)

        if not silent:
            self.game.events.trigger(event=self._events["left"], card=e)

        return e

    def remove(self, e, silent=False):
        if e not in self:
            raise ValueError("'{}' is not in the {} zone.".format(e, self))

        self._contents.remove(e)
        self._order.remove(e)

        if not silent:
            self.game.events.trigger(event=self._events["left"], card=e)

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
