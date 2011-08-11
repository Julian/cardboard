from collections import MutableSet, Set, deque


class Zone(MutableSet):

    ordered = False

    def __init__(self, name, contents=()):
        super(Zone, self).__init__()

        self.name = name
        self._contents = set(contents)

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

    def discard(self, e):
        self._contents.discard(e)


class OrderedZone(Set):

    ordered = True

    def __init__(self, name, contents=()):
        super(OrderedZone, self).__init__()

        self.name = name
        self._order = list(contents)
        self._contents = set(self._order)

    def __contains__(self, e):
        return e in self._contents

    def __getitem__(self, i):
        return self._order[i]

    def __iter__(self):
        return iter(self._order)

    def __len__(self):
        # don't plan on allowing duplicates, but just in case, use order
        return len(self._order)

    def __reversed__(self):
        return reversed(self._order)

    def __repr__(self):
        return "<OrderedZone: {.name}>".format(self)

    def add(self, e):
        self._contents.add(e)
        self._order.append(e)

    append = add

    def clear(self):
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

    def pop(self, i=None):
        if i is None:
            e = self._order.pop()
        else:
            e = self._order.pop(i)

        self._contents.remove(e)
        return e

    def remove(self, e):
        # order matters here, we want ValueError not KeyError
        self._order.remove(e)
        self._contents.remove(e)

    def reverse(self):
        self._order.reverse()


def zone(name, contents=(), ordered=False):
    cls = Zone if not ordered else OrderedZone
    return cls(name, contents)
