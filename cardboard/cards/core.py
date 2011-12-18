"""
Contains functionality to map a card name to functions implementing behavior.

"""

from cardboard.util import populate


__all__ = ["cards", "card"]

cards = {}
card = populate(cards, allow_overwrite=False)
