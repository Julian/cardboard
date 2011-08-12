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
import panglery


class EventHandlerTestCase(unittest.TestCase):
    def setUp(self):
        super(EventHandlerTestCase, self).setUp()
        self.events = mock.Mock(spec=panglery.Pangler)
        self.trigger = self.events.trigger

    def failUnexpectedEvents(self, *events):
        # TODO: Make this look nicer by giving it a nice diff
        verb = "was" if len(events) == 1 else "were"
        self.fail("{} {} triggered by {}.".format(events, verb, self.events))

    def assertLastEventsWere(self, *events):
        events = [((), {"event" : event}) for event in events]
        self.assertEqual(events, self.trigger.call_args_list[-len(events):])

    def assertLastEventsWereNot(self, *events):
        try:
            self.assertLastEventsWere(*events)
        except (AssertionError, IndexError):
            return
        else:
            self.failUnexpectedEvents(*events)

    def assertSubscribed(self, fn, **kwargs):
        self.assertIn(((fn,), kwargs), self.events.subscribe.call_args_list)


def last_events(game):
    logger = logging.getLogger("event_logger")
    for args, kwargs in game.events.trigger.call_args_list:
        logging.debug("Called with:\n\targs: {}\n\tkwargs: {}".format(args,
                                                                      kwargs))
