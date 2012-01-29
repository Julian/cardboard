class CardboardRuntimeError(Exception):
    """
    The base class for all cardboard exceptions.

    """


class NotImplemented(CardboardRuntimeError):
    pass


class InvalidAction(CardboardRuntimeError):
    """
    An action was attempted with incorrect parameters.

    This exception is raised if no more specific error is appropriate.

    It (and its subclasses) should generally be raised when an action that is
    being attempted is failing due to something that can be recovered from by
    reselecting or retrying.

    """


class BadSelection(InvalidAction):
    """
    An invalid selection was made.

    """


class NoSuchObject(InvalidAction):
    """
    An action was attempted on an object that does not exist in the game.

    """

    MSG = "{0.looked_in} has no such {0.desired} '{0.object}'"

    def __init__(self, looked_in, desired, object):
        super(NoSuchObject, self).__init__()

        self.looked_in = looked_in
        self.desired = desired
        self.object = object

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        return self.MSG.format(self)


class RequirementNotMet(InvalidAction):
    """
    An action is being attempted when a requirement for it was not met.

    """

    MSG = "{self}.{attr} was {got!r} (expected {expected!r})"

    def __init__(self, instance, attr, got, expected, msg=None):
        super(RequirementNotMet, self).__init__()

        if msg is None:
            msg = self.MSG

        self.self = instance
        self.attr = attr
        self.got = got
        self.expected = expected

        self.msg = msg.format(self=instance, attr=attr,
                              got=got, expected=expected)

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        return self.msg

    @classmethod
    def failed_condition(cls, msg=""):
        """
        An arbitrary condition was not met.

        """
        return cls(instance=None, attr=None, got=None, expected=None, msg=msg)
