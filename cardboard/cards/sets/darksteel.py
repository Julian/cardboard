from cardboard import types
from cardboard.card import Ability
from cardboard.cards import card, common


spell = Ability.spell
activated = Ability.activated
triggered = Ability.triggered
static = Ability.static


@card("Echoing Truth")
def echoing_truth(card, abilities):

    @spell(description=abilities[0])
    def echoing_truth():

        target, = card.owner.frontend.select.cards(
            match=lambda card : types.land not in card.types
        )
        targets = [c for c in card.game.battlefield if c.name == target.name]

        for target in targets:
            target.owner.hand.move(target)

    return echoing_truth,
