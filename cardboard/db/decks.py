import collections
import glob
import json
import os.path

from cardboard.config import USER_DATA


DECKS_DIR = os.path.join(USER_DATA, "Decks")


def from_cards(cards, sideboard=()):
    """
    Create a deck from an iterable of cards with an optional sideboard.

    * cards : an iterable of cards
    * sideboard : an optional iterable of cards for the deck's sideboard

    """

    return {
        u"cards" : collections.Counter(card.name for card in cards),
        u"sideboard" : collections.Counter(card.name for card in sideboard)
    }


def load(file, format=None):
    """
    Load a previously saved deck.

    * name : the deck's name (required if loading without a provided file)
    * from_file : a file-like object to load from, or None (default) to load
                  from the default decks folder
    * format : the format of the deck (default is to guess from the extension)

    """

    if format is None:
        extension = file.name.rpartition(".")[2]
        format = {
            "deck" : "deck", "dec" : "apprentice", "txt" : "mtgo"
        }.get(extension)

    if format not in {"deck", "apprentice", "mtgo"}:
        raise ValueError("Unknown format for {}".format(file.name))

    if format == "deck":
        return json.load(file)
    else:
        deck = {u"cards" : {}, u"sideboard" : {}}
        put_into = deck[u"cards"]

        for line in file:
            line = line.strip()

            # parse both file formats as if they were the same, since who cares
            if not line or line.startswith("//"):
                continue
            elif line == "Sideboard":
                put_into = deck[u"sideboard"]
            else:
                quantity, card = line.lstrip("SB: ").split(None, 1)
                put_into[card] = int(quantity)

        return deck


def export(deck, format="mtgo"):
    """
    Export a deck to a supported external format.

    Supported formats are: mtgo, apprentice

    * deck : a deck
    * format : a supported format (default is mtgo)

    Returns a generator yielding lines of the output.

    """

    for card, quantity in sorted(deck["cards"].iteritems()):
        yield u"{} {}".format(quantity, card)

    yield ""

    if format == "mtgo":
        yield u"Sideboard"

    for card, quantity in sorted(deck["sideboard"].iteritems()):
        if format == "mtgo":
            yield u"{} {}".format(quantity, card)
        else:
            yield u"SB: {} {}".format(quantity, card)


def save(name, deck, to=None):
    """
    Save a deck to the decks folder.

    * name : a name
    * deck : a deck
    * to : a file-like object, or None (default) to save to the default folder

    """

    if to is None:
        with open(os.path.join(DECKS_DIR, name + ".deck"), "w") as f:
            json.dump(deck, f)
    else:
        json.dump(deck, to)
