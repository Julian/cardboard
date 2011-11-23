import collections
import json
import os.path

from cardboard.config import USER_DATA


def load(name=None, from_file=None):
    """
    Load a previously saved deck.

    * name : the deck's name (required if loading without a provided file)
    * from_file : a file-like object to load from, or None (default) to load
                  from the default decks folder
    """

    if from_file is None:
        if name is None:
            raise TypeError("load() takes at least 1 argument (0 given)")
        from_file = open(os.path.join(USER_DATA, "Decks", name + ".deck"))
    return json.load(from_file)


def parse(deck_list):
    """
    Parse a deck from a string.

    """

    deck = {"cards" : {}, "name" : None, "sideboard" : {}}
    put_into = deck["cards"]

    for line in deck_list.splitlines():
        if not line:
            continue
        elif line == "Sideboard":
            put_into = deck["sideboard"]
        else:
            quantity, card = line.split(None, 1)
            put_into[card] = int(quantity)

    return deck


def save(name, cards, sideboard=(), to=None):
    """
    Save a deck to the decks folder.

    * name : a deck name
    * cards : an iterable of cards
    * sideboard : an optional iterable of sideboard cards
    * to : a file-like object to write to, or None (default) to save
                to the default decks folder

    """

    deck = {
        "name" : name,
        "cards" : collections.Counter(card.name for card in cards),
        "sideboard" : collections.Counter(card.name for card in sideboard)
    }

    if to is None:
        with open(os.path.join(USER_DATA, "Decks", name + ".deck"), "w") as f:
            json.dump(deck, f)
    else:
        json.dump(deck, to)
