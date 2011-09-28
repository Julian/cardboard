from cardboard.cards import card, ability

@card("Brainstorm")
def brainstorm(card):

    @ability
    def ability(self):
        self.owner.draw(3)
        discard = self.owner.frontend.select_cards(self.owner.hand,
                                                   how_many=2, ordered=True)
        self.owner.library.move(*discard)
