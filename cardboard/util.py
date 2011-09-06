"""
Utilities of use for the creation of game objects.

"""

import logging

from cardboard import exceptions


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


def requirements(messages=None):
    """
    Build a `require` function that can check if a set of requirements are met.

    Arguments
    ---------

    * **messages: A mapping of attr names to failure messages for each value

    If a failure message for either an entire attribute or a given value is not
    provided, a default message will be used.

    """

    # TODOC: format string {self} {got} {expected}, example

    if messages is None:
        messages = {}

    def require(self, condition=None, msg="", **attrs):
        """
        Require that a series of conditions be true before proceeding.

        Arguments
        ---------

        * condition / msg: an arbitrary condition and failure msg to verify
        * **atrs: a mapping of attributes to values they are required to have

            >>> require = requirements(imag="{0} had an imaginary component "
                                            "that was not {1} (was: {0.imag})")

            >>> j = 2 + 3j
            >>> require(j, imag=0)
            Traceback (most recent call last):
            ...
            RequirementNotMet: 2 + 3j had an imaginary component that was not 0
            (was: 3.0)

            >>> require(j, "foo" == "bar", msg="Failed the bar test.")
            Traceback (most recent call last):
            ...
            RequirementNotMet: Failed the bar test.

        """

        if condition is not None and not condition:
            raise exceptions.RequirementNotMet.failed_condition(msg)

        for attr, expected in attrs.iteritems():
            got = getattr(self, attr)

            if got != expected:

                msgs = messages.get(attr, {})

                try:
                    msg = msgs[got]
                except (KeyError, TypeError):
                    # not provided or non-hashable
                    msg = msgs.get("default")

                raise exceptions.RequirementNotMet(instance=self, attr=attr,
                                                   got=got, expected=expected,
                                                   msg=msg)

    return require
