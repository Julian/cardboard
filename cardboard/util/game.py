"""
Utilities of use for the creation of game objects.

"""

from functools import wraps

from cardboard import exceptions

def check_started(fn):
    """
    Check if the game has started before allowing the function to be run.

    """

    @wraps(fn)
    def _check_started(self, *args, **kwargs):
        if not self.started:
            raise exceptions.RuntimeError("{} has not started.".format(self))
        return fn(self, *args, **kwargs)

    return _check_started
