from cardboard import types
from cardboard.card import Ability
from cardboard.cards import card, common, match


spell = Ability.spell
activated = Ability.activated
triggered = Ability.triggered
static = Ability.static


@card("Brainstorm")
def brainstorm(card, abilities):

    @spell(description=abilities[0])
    def brainstorm():
        return common.draw_discard(card.owner, 3, 2, card.owner.library)

    return brainstorm,
