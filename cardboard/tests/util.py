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

    def assertLastEventWas(self, event, request=True):
        evt = pool(event=event)
        rq = pool(request=event)

        if not request:
            return self.events.trigger.assert_called_with(**e)
        else:
            args = [[rq], [evt]]
            self.assertEqual(self.events.trigger.call_args_list[-2:], args)

    def assertLastEventWasnt(self, event, request=True):
        try:
            self.assertLastEventWas(event, request)
        except (AssertionError, IndexError):
            return
        else:
            # TODO: Make this look nicer by giving it a nice diff
            self.fail("{} was triggered by {}.".format(event, self.events))

    def assertLastEventsWere(self, *events):
        events = [[i] for i in events]
        self.assertEqual(events, self.trigger.call_args_list[-len(events):])

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


def pool(**kwargs):
    kwargs["pool"] = ANY
    return kwargs
