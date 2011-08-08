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
