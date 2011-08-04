from collections import MutableMapping
from functools import wraps
import itertools


__all__ = ["Pool", "Event", "EventStore", "announce", "events"]


class Pool(MutableMapping):
    def __init__(self, *args, **kwargs):
        self._parameters = dict(*args, **kwargs)

    def __contains__(self, k):
        return k in self._parameters

    def __iter__(self):
        return iter(self._parameters)

    def __len__(self):
        return len(self._parameters)

    def __getitem__(self, k):
        return self._parameters[k]

    def __setitem__(self, k, v):
        self._parameters[k] = v

    def __delitem__(self, k):
        del self._parameters[k]

    def __repr__(self):
        return "Pool({})".format(self._parameters.keys())


class Event(object):
    def __init__(self, description):
        super(Event, self).__init__()
        self.description = description

    def __repr__(self):
        return "<Event: {}>".format(self.description)


class EventStore(MutableMapping):
    def __init__(self, *args, **kwargs):
        self._substores = {}
        self._events = dict(*args, **kwargs)

    def __contains__(self, k):
        return k in self._events

    def __iter__(self):
        return iter(self._events)

    def __len__(self):
        return len(self._events)

    def __getattr__(self, attr):
        return self._substores.setdefault(attr, EventStore())

    def __getitem__(self, k):
        return self._events[k]

    def __setitem__(self, k, v):
        self._events[k] = v

    def __delitem__(self, k):
        del self._events[k]

    def __repr__(self):
        return "EventStore({})".format(self._events)

    @property
    def substores(self):
        return self._substores.viewkeys()


def announce(handler=None, handler_attr="events", store=None, **add_events):
    """
    Create an announcing action.

    Callables using this decorator should conform to the following pattern:

        @announce()
        def action(<arguments>):

            <setup>

            pool = (yield)   # receive a pool for communicating with listeners

            <populate pool>  # anything that listeners may need to modify

            <yield events>   # ask listeners if they need to participate

            yield            # tell listeners pool is ready for modification

            <body>           # check pool for denials and do work

            <yield events>   # signal listeners that want to know what was done

            <cleanup>

    Events will be triggered by the handler along with the pool by:

        event_handler.trigger(request=event, pool=pool)

    during the first round of yields to the listeners, and by:

        event_handler.trigger(event=event, pool=pool)

    when yielding for the listeners waiting for notifications.

    """

    if store is None:
        store = events

    for k, v in add_events.iteritems():
        store[k] = Event(v)

    def _announce(fn):

        def broadcast_events(handler, event_key, source, initial=(), **kwargs):
            for event in itertools.chain(initial, source):
                if event is None:
                    return

                kwargs[event_key] = store[event]
                handler.trigger(**kwargs)

        @wraps(fn)
        def announced(*args, **kwargs):
            if handler is None:
                self = args[0]
                # nonlocal :/
                handle = getattr(self, handler_attr)
            else:
                handle = handler

            action = fn(*args, **kwargs)

            try:
                next(action)
            except StopIteration:
                return  # action cancelled itself
            else:
                pool = Pool()

            # just grab the next yield so that an extra yield isn't required
            next_yield = [action.send(pool)]
            broadcast_events(handle, "request", action, next_yield, pool=pool)
            broadcast_events(handle, "event", action, pool=pool)

        return announced
    return _announce

events = EventStore()
