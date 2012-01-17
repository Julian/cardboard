"""
Implementations of common card mechanics.

"""


def destroy(card):
    """
    Destroy a card.

    """

    card.owner.graveyard.move(card)


def draw_discard(player, draw=1, discard=1, to=None):
    """
    Draw cards then select cards to discard to a given zone.

    """

    if to is None:
        to = player.graveyard

    player.draw(draw)
    discarded = player.frontend.select_cards(player.hand, how_many=discard)

    for card in discarded:
        to.move(card)
