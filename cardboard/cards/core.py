"""
Contains functionality to map a card name to functions implementing behavior.

"""

__all__ = ["cards", "card"]

cards = {}

def card(name, destination=cards):
    if name in destination:
        raise ValueError("'{}' was already added.".format(name))

    def add_card(card_fn):
        destination[name] = card_fn
        return card_fn
    return add_card
