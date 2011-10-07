from cardboard.cards import card

@card("Echoing Truth")
def echoing_truth(self):
    target = self.owner.frontend.select_cards(self.game.battlefield,
                                              match=m.nonland)
    target.owner.hand.move(target)

    for card in self.game.battlefield:
        if card.name == target.name:
            target.owner.hand.move(card)
