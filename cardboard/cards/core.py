"""
Contains functionality to map a card name to functions implementing behavior.

"""

from cardboard import exceptions


cards = {}


def ability(card, ability_text):
    if card.abilities[ability_text] not in {None, not_implemented}:
        raise ValueError("Ability was already added.")

    def add_ability(ability_fn):
        card.abilities[ability_text] = ability_fn
        return ability_fn
    return add_ability


def card(name, destination=cards):
    if name in destination:
        raise ValueError("'{}' was already added.".format(name))

    def add_card(card_fn):
        destination[name] = card_fn
        return card_fn
    return add_card


def not_implemented(not_implemented_thing, *args, **kwargs):
    raise exceptions.NotImplemented(not_implemented_thing)
