from cardboard.card import Ability
from cardboard.cards import card, common


@card("Brainstorm")
def brainstorm(card, abilities):
    @Ability.spell(description=abilities[0])
    def ability():
        return common.draw_discard(card.owner, 3, 2, card.owner.library)

    return [ability]
