from cardboard import types
from cardboard.card import Ability
from cardboard.cards import card, common


@card("Brand")
def brand(self, abilities):

    @Ability.spell(description=abilities[0])
    def ability():
        for card in self.game.battlefield:
            if card.owner == self.owner:
                card.controller = card.owner

    # XXX: Cycling 2

    return [ability]


@card("Catalog")
def catalog(self, abilities):

    @Ability.spell(description=abilities[0])
    def ability():
        return common.draw_discard(self.owner, 2, 1)

    return [ability]


@card("Clear")
def clear(self, abilities):

    @Ability.spell(description=abilities[0])
    def ability():
        target, = self.owner.frontend.select.card(match=is_enchantment)
        target.owner.graveyard.move(target)

    # XXX: Cycling 2

    return [ability]


@card("Congregate")
def congregate(self, abilities):

    @Ability.spell(description=abilities[0])
    def ability():
        target, = self.owner.frontend.select.player(bad=False)
        target.life += sum(2 for c in battlefield if c.type == types.CREATURE)

    return [ability]


@card("Curfew")
def curfew(self, abilities):

    @Ability.spell(description=abilities[0])
    def ability():
        for player in self.game.turn.order:
            selection = player.frontend.select.card(match=is_creature)

            if selection:
                player.hand.move(selection[0])

    return [ability]


@card("Expunge")
def expunge(self, abilities):

    @Ability.spell(description=abilities[0])
    def ability():
        target, = self.owner.frontend.select.card(
            match=lambda c : types.CREATURE in c.type and
                             types.ARTIFACT not in c.type and
                             "B" not in c.colors
        )
        target.owner.graveyard.move(target)

    # XXX: Can't Regenerate
    # XXX: Cycling 2

    return [ability]


@card("Hibernation")
def hibernation(self, abilities):

    @Ability.spell(description=abilities[0])
    def ability():
        for card in self.game.battlefield:
            if card.is_permanent and "G" in card.colors:
                card.owner.hand.move(card)

    return [ability]
