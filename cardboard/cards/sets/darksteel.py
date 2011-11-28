from cardboard import types
from cardboard.ability import spell, activated, triggered, static
from cardboard.cards import card, common


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
