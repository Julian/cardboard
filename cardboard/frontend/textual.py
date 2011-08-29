from __future__ import print_function, unicode_literals
from textwrap import dedent
import logging


# FIXME : > 2 Players
class TextualFrontend(object):
    def __init__(self, player, debug=False):
        super(TextualFrontend, self).__init__()

        self.debug = debug

        self.game = player.game
        self.player = player

    def __repr__(self):
        return "<TextualFrontend to {}>".format(self.player)

    def priority_granted(self):
        pass

    def prompt(self, msg, *args, **kwargs):
        print(msg.encode("utf-8"), *args, **kwargs)

    def select(self, choices, how_many=1, duplicates=False):
        choices = {str(k) : v for k, v in choices.iteritems()}

        for index, choice in sorted(choices.iteritems()):
            self.prompt("    {}. {}".format(index, choice))

        self.prompt("\n")

        while True:
            if how_many is not None and how_many != 1:
                self.prompt("Select {} choices.".format(how_many))

            self.prompt(">>|", end=" ")

            selections = [s.strip() for s in raw_input().split(",")]

            # TODO: how_many = None
            if len(selections) < how_many:
                self.prompt("Not enough selections.")
            elif not duplicates and len(set(selections)) < len(selections):
                self.prompt("Can't duplicate selections.")
            else:
                try:
                    return [choices[selection] for selection in selections]
                except KeyError as e:
                    self.prompt("{} is not a valid choice.".format(e[0]))

    def menu(self, title, preamble, *choices):
        self.prompt("\n{}:".format(title), end="\n\n")

        if preamble:
            self.prompt("    {}".format(preamble), end="\n\n")

        selection, = self.select(dict(enumerate(choices, 1)))
        return selection

    def main_menu(self):
        selection = self.menu("Main Menu", self.player_info(), "Zone Info")
        getattr(self, selection.lower().replace(" ", "_"))()

    def card_info(self, card):
        info = ["Name: {0.name}", "Type: {0.type}"]

        for more in ["mana_cost", "abilities", "power", "toughness"]:
            attr = getattr(card, more)

            if attr is not None:
                info.append(
                    "{}: {{0.{}}}".format(more.title().replace("_", " "), more)
                )

        return "\n".join(info).format(card)

    def player_info(self):
        opponents = (str(p) for p in self.game.players - {self.player})
        return dedent("""
                      You: {.player}
                      Opponent: {}
                      """.strip("\n").format(self, ", ".join(opponents)))

    def turn_info(self):
        return dedent("""
                      Phase: {0.game.turn.phase}
                      Step: {0.game.turn.step}
                      """.strip("\n").format(self))

    def zone_info(self):
        choices = {"Field" : set(self.game.battlefield),
                   "Exile" : set(self.player.exile),
                   "Graveyard" : list(self.player.graveyard),
                   "Hand" : set(self.player.hand)}

        if self.debug:
            choices["library"] = list(self.player.library)

        selection = self.menu("Zone Info", None, *choices)

        selection = self.menu(selection, None, *choices[selection])
        self.prompt(self.card_info(selection))
