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

import logging
import unittest

import mock


class EventHandlerTestCase(unittest.TestCase):
    def setUp(self):
        super(EventHandlerTestCase, self).setUp()
        self.events = mock.Mock()
        self.trigger = self.events.trigger

    def failUnexpectedEvents(self, *events):
        # TODO: Make this look nicer by giving it a nice diff
        verb = "was" if len(events) == 1 else "were"
        self.fail("{} {} triggered by {}.".format(events, verb, self.events))

    def assertLastRequestedEventWas(self, e):
        self.assertLastEventsWere(request(e), event(e))

    def assertLastRequestedEventWasNot(self, e):
        return self.assertLastEventsWereNot(request(e), event(e))

    def assertLastEventsWere(self, *events):
        events = [[i] for i in events]
        self.assertEqual(events, self.trigger.call_args_list[-len(events):])

    def assertLastEventsWereNot(self, *events):
        try:
            self.assertLastEventsWere(*events)
        except (AssertionError, IndexError):
            return
        else:
            self.failUnexpectedEvents(*events)

    def assertSubscribed(self, fn, pool=True, **kwargs):
        if pool:
            kwargs.update(needs=["pool"])

        self.assertIn(((fn,), kwargs), self.events.subscribe.call_args_list)


class _ANY(object):
    def __eq__(self, other):
        return True

    def __repr__(self):
        return "<any>"

ANY = _ANY()


def last_events(game):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("event_logger")

    for _, kwargs in game.events.trigger.call_args_list:
        logger.debug({k : v for k, v in kwargs.iteritems() if k != "pool"})


def request(event):
    return {"request" : event, "pool" : ANY}

def event(event):
    return {"event" : event, "pool" : ANY}
