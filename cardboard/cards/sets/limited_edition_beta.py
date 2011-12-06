from cardboard import types
from cardboard.ability import (
    AbilityNotImplemented, spell, activated, triggered, static
)
from cardboard.cards import card, common, keywords, match


@card("Circle of Protection: Black")
def circle_of_protection_black(card, abilities):

    def circle_of_protection_black():
        return AbilityNotImplemented

    return circle_of_protection_black,