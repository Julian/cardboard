"""
Contains functionality to map a card name to functions implementing behavior.

"""

from cardboard.card import Ability


__all__ = ["cards", "spell", "activated", "triggered", "static", "card"]

cards = {}

spell = Ability.spell
activated = Ability.activated
triggered = Ability.triggered
static = Ability.static


def card(name, destination=cards):
    if name in destination:
        raise ValueError("'{}' was already added.".format(name))

    def add_card(card_fn):
        destination[name] = card_fn
        return card_fn
    return add_card
