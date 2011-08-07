import collections
import functools
import itertools

__all__ = ["Pool", "collaborate"]


class Pool(collections.MutableMapping):
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


def broadcast_events(handler, event_key, source, initial=(), **kwargs):
    for event in itertools.chain(initial, source):
        if event is None:
            return

        kwargs[event_key] = event
        handler.trigger(**kwargs)


def collaborate(game=None):
    """
    Create a collaborating action that can be listened for and modified.

    Callables using this decorator should conform to the following pattern:

        @collaborate()
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

    def _collaborate(fn):

        @functools.wraps(fn)
        def collaborating(*args, **kwargs):

            # nonlocal :/
            if game is None:
                self = args[0]
                state = getattr(self, "game", self)
            else:
                state = game

            handler = state.events
            action = fn(*args, **kwargs)

            try:
                next(action)  # action is doing setup
            except StopIteration:
                return  # action cancelled itself
            else:
                pool = Pool(game=state)

            # just grab the next yield so that an extra yield isn't required
            next_yield = [action.send(pool)]
            broadcast_events(handler, "request", action, next_yield, pool=pool)
            broadcast_events(handler, "event", action, pool=pool)

        return collaborating
    return _collaborate

