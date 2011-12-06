from cardboard import types
from cardboard.ability import (
    AbilityNotImplemented, spell, activated, triggered, static
)
from cardboard.cards import card, common, keywords, match


@card("Chandra's Outrage")
def chandras_outrage(card, abilities):

    def chandras_outrage():
        return AbilityNotImplemented

    return chandras_outrage,


@card("Sorcerer's Strongbox")
def sorcerers_strongbox(card, abilities):

    def sorcerers_strongbox():
        return AbilityNotImplemented

    return sorcerers_strongbox,


@card("Plummet")
def plummet(card, abilities):

    def plummet():
        return AbilityNotImplemented

    return plummet,


@card("Reassembling Skeleton")
def reassembling_skeleton(card, abilities):

    def reassembling_skeleton():
        return AbilityNotImplemented

    return reassembling_skeleton,