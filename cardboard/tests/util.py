import logging

class _ANY(object):
    def __eq__(self, other):
        return True

    def __repr__(self):
        return "<any>"

ANY = _ANY()


def last_events(events):
    for event in events:
        logging.debug({k : v for k, v in events[1].iteritems() if k != "pool"})
