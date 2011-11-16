from cardboard.cards import card, common, spell, triggered, activated, static


@card("Echoing Truth")
def echoing_truth(card, abilities):

    @spell(description=abilities[0])
    def echoing_truth():

        target, = card.owner.frontend.select.cards(match=common.is_nonland)
        targets = [c for c in card.game.battlefield if c.name == target.name]

        for target in targets:
            target.owner.hand.move(target)

    return echoing_truth
