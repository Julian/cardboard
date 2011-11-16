from cardboard import types
from cardboard.card import Ability
from cardboard.cards import card, common


spell = Ability.spell
activated = Ability.activated
triggered = Ability.triggered
static = Ability.static


@card("Brand")
def brand(card, abilities):

    @spell(description=abilities[0])
    def brand():
        for kard in card.game.battlefield:
            if kard.owner == card.owner:
                kard.controller = kard.owner

    # XXX: Cycling 2

    return brand,


@card("Catalog")
def catalog(card, abilities):

    @spell(description=abilities[0])
    def catalog():
        return draw_discard(card.owner, draw=2, discard=1)

    return catalog,


@card("Clear")
def clear(card, abilities):

    @spell(description=abilities[0])
    def clear():
        target, = card.owner.frontend.select.card(
            match=lambda c : types.enchantment in c.types
        )
        common.destroy(target)

    # XXX: Cycling 2

    return clear,


@card("Congregate")
def congregate(card, abilities):

    @spell(description=abilities[0])
    def congregate():
        target, = card.owner.frontend.select.player(bad=False)
        target.life += sum(2 for c in battlefield if types.creature in c.types)

    return congregate,


@card("Curfew")
def curfew(card, abilities):

    @spell(description=abilities[0])
    def curfew():
        for player in card.game.turn.order:
            selection = player.frontend.select.card(match=is_creature)

            if selection:
                player.hand.move(selection[0])

    return curfew,


@card("Expunge")
def expunge(card, abilities):

    @spell(description=abilities[0])
    def expunge():
        target, = card.owner.frontend.select.card(
            match=lambda c : types.creature in c.types and
                             types.artifact not in c.types and
                             "B" not in c.colors
        )
        common.destroy(target)

    # XXX: Can't Regenerate
    # XXX: Cycling 2

    return expunge,


@card("Hibernation")
def hibernation(card, abilities):

    @spell(description=abilities[0])
    def hibernation():
        for card in card.game.battlefield:
            if card.is_permanent and "G" in card.colors:
                card.owner.hand.move(card)

    return hibernation,
