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
