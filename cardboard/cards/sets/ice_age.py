from cardboard.card import Ability
from cardboard.cards import card, common


@card("Brainstorm")
def brainstorm(self, abilities):

    @Ability.spell(description=abilities[0])
    def ability():
        return common.draw_discard(self.owner, 3, 2, self.owner.library)

    return [ability]
