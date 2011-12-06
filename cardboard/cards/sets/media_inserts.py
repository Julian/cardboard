from cardboard import types
from cardboard.ability import (
    AbilityNotImplemented, spell, activated, triggered, static
)
from cardboard.cards import card, common, keywords, match


@card("Arena")
def arena(card, abilities):

    def arena():
        return AbilityNotImplemented

    return arena,


@card("Giant Badger")
def giant_badger(card, abilities):

    def giant_badger():
        return AbilityNotImplemented

    return giant_badger,