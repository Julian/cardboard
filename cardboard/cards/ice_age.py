from cardboard.cards import card

@card("Brainstorm")
def brainstorm(self):
    self.owner.draw(3)
    discard = self.owner.frontend.select_cards(self.owner.hand,
                                               how_many=2, ordered=True)
    self.owner.library.move(*discard)
