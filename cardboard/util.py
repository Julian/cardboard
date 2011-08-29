"""
Utilities of use for the creation of game objects.

"""

import logging

from cardboard import exceptions


def check_started(game):
    """
    Check if the game has started before allowing the function to be run.

    """

    if game is None or not game.started:
        err = "Game '{}' has not started.".format(game)
        raise exceptions.InvalidAction(err)


def do_subscriptions(self, game=None):
    """
    Subscribe any of the class' instance methods to events.

    """

    if game is None:
        game = self

    subscriptions = {getattr(self, k) : v for k, v in self._subscriptions}

    for method, subscription_options in subscriptions.iteritems():
        game.events.subscribe(method, **subscription_options)

def log(game):
    event_log = logging.getLogger("Event Logger")
