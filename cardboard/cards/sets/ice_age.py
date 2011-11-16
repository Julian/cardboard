from cardboard.cards import card, common, spell, triggered, activated, static


@card("Brainstorm")
def brainstorm(card, abilities):

    @spell(description=abilities[0])
    def brainstorm():
        return common.draw_discard(card.owner, 3, 2, card.owner.library)

    return brainstorm,
