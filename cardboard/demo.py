from panglery import Pangler

from cardboard import Game
from cardboard.card import Card
from cardboard.db import Session
from cardboard.db.models import Deck
from cardboard.frontend.textual import TextualFrontend
from cardboard.util import log

def build_deck(deck):
    # TODO: This needs to be moved into the codebase
    cards = []

    for c in deck.card_appearances:
        cards.extend(Card(c.card) for _ in range(c.quantity))

    return cards

events = Pangler()
game = Game(events)
log(game)

s = Session()
d1 = s.query(Deck).filter_by(name="MonoBlueControl").one()
d2 = s.query(Deck).filter_by(name="TokenAscension").one()

# with open("/Users/Julian/Desktop/MonoBlueControl.txt") as mbc, open("/Users/Julian/Desktop/TokenAscension.txt") as ta:
#     d1 = Deck.load(s, mbc)
#     d2 = Deck.load(s, ta)

p1 = game.add_player(library=build_deck(d1), name="Julian")
p2 = game.add_player(library=build_deck(d2), name="Opponent")

p1.frontend = TextualFrontend(p1)
game.start()
