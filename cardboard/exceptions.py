class RuntimeError(Exception):
    """
    The base class for all cardboard exceptions.

    """

class InvalidAction(RuntimeError):
    """
    An action was attempted with incorrect parameters.

    This exception is raised if no more specific error is appropriate.

    It (and its subclasses) should generally be considered recoverable,
    specifically by catching  and retrying the action after the requirements
    have been verified.

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
        return self.MSG.format(self)
