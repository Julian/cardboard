"""
Utilities for testing.

Notes
-----

To test if an object with a stubbed out pangler is working properly, check
that:

    * The function that should trigger the event
        * does

    * The function that should be subscribed to the event
        * is
        * performs correctly when called manually

"""

import unittest

import mock
import panglery

from cardboard.core import Game, Player
from cardboard.card import Card


class EventHandlerTestCase(unittest.TestCase):

    MSG = "Events failed to match a subset of the triggered events (heard {})"

    def setUp(self):
        super(EventHandlerTestCase, self).setUp()
        self.events = mock.Mock(spec=panglery.Pangler)

    def failUnexpectedEvents(self, events):
        # TODO: Make this look nicer by giving it a nice diff
        verb = "was" if len(events) == 1 else "were"
        self.fail("{} {} triggered by {}.".format(events, verb, self.events))

    def assertTriggered(self, events, of=None):
        """
        Assert that `events` is a non-contiguous ordered subset of the events.

        Events should be an iterable of dicts containing each of the desired
        keyword-params that should have been triggered by the event trigger.

        The default place to check as a superset is the call args to the event
        trigger (i.e. self.events.trigger.call_args_list).

            >>> class Example(EventHandlerTestCase):
            ...     def test_example(self):
            ...         s = [1, 2, 6, 8]
            ...         self.assertTriggered(s, range(10))

            >>> suite = unittest.TestLoader().loadTestsFromTestCase(Example)
            >>> unittest.TextTestRunner().run(suite)
            <unittest.runner.TextTestResult run=1 errors=0 failures=0>

        """

        if of is None:
            of = self.events.trigger.call_args_list

        of = (kwargs for args, kwargs in of)
        found = []

        for index, event in enumerate(events):

            if not isinstance(event, dict):
                event = {"event" : event}

            current_finds = []

            for each in of:
                if each == event:
                    found.extend("\x2e    {}".format(e) for e in current_finds)
                    found.append("=    {}".format(each))
                    current_finds = []
                    break
                else:
                    current_finds.append(each)
            else:
                found.extend("<    {!r}".format(e) for e in events[index:])
                found.extend(">    {}".format(e) for e in current_finds)

                heard = len(self.events.trigger.call_args_list)
                found_msg = "\n" + "\n".join(found)
                msg = self._truncateMessage(self.MSG.format(heard), found_msg)

                self.fail(msg)

    def assertLastEventsWere(self, events):
        last_events = self.events.trigger.call_args_list[-len(events):]
        self.assertTriggered(events, last_events)

    def assertLastEventsWereNot(self, events):
        try:
            self.assertLastEventsWere(events)
        except AssertionError:
            return
        else:
            self.failUnexpectedEvents(events)

    def assertSubscribed(self, fn, **kwargs):
        self.assertIn(((fn,), kwargs), self.events.subscribe.call_args_list)

    def resetEvents(self):
        self.events.trigger.call_args_list[:] = []


class GameTestCase(EventHandlerTestCase):
    def setUp(self):
        super(GameTestCase, self).setUp()
        self.game = Game(self.events)

        i, j, k = [[mock.Mock(spec=Card) for _ in range(60)] for _ in range(3)]

        self.library = k

        self.p1 = self.game.add_player(library=i, name="1")
        self.p2 = self.game.add_player(library=j, name="2")
        self.p3 = Player(game=self.game, library=k, name="3")
