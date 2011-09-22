"""
Contains functionality to map a card name to functions implementing behavior.

"""

from cardboard import exceptions


cards = {}


def card(name, destination=cards):
    if name in destination:
        raise ValueError("'{}' was already added.".format(name))

    def add_card(fn):
        destination[name] = fn
        return fn
    return add_card


def not_implemented(card, *args, **kwargs):
    raise exceptions.CardNotImplemented(card)
