# coding: utf-8
from __future__ import print_function, unicode_literals

import logging
import textwrap


# FIXME : > 2 Players
class TextualFrontend(object):
    def __init__(self, player):
        super(TextualFrontend, self).__init__()

        self._debug = False

        self.game = player.game
        self.player = player

    def __repr__(self):
        return "<TextualFrontend to {}>".format(self.player)

    def priority_granted(self):
        pass

    def prompt(self, *args, **kwargs):
        args = (arg.encode("utf-8") for arg in args)
        print(*args, **kwargs)

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
        mana_cost = card.mana_cost or ""

        subtypes = pt = ""

        if card.subtypes:
            subtypes = " — {}".format(", ".join(card.subtypes))

        if card.power or card.toughness:
            pt = "\n{card.power}/{card.toughness}".format(card=card)

        abilities = "\n".join(
            textwrap.fill(ability, width=28) for ability in card.abilities
        )

        return textwrap.dedent("""
                               {0.name:<20}{mana_cost}
                               {0.type}{subtypes}

                               {abilities}{pt}
                               """).strip("\n").format(card,
                                                       mana_cost=mana_cost,
                                                       subtypes=subtypes,
                                                       abilities=abilities,
                                                       pt=pt)

    def player_info(self):
        self.game.require(started=True)

        s = "s" if len(self.player.opponents) > 1 else ""
        opponents = ", ".join(str(o) for o in self.game.turn.order
                                     if o in self.player.opponents)

        return textwrap.dedent(
            """
            You: {}
            Opponent{}: {}
            """
        ).strip("\n").format(self.player, s, opponents)

    def turn_info(self):
        phase = self.game.turn.phase
        info = ["Phase: {}".format(phase)]

        if len(phase) > 1:
            step = self.game.turn.step.__name__
            info.append("Step: {}".format(step.replace("_", " ").title()))

        return "\n".join(info)

    def zone_info(self):
        choices = {"Field" : set(self.game.battlefield),
                   "Exile" : set(self.player.exile),
                   "Graveyard" : list(self.player.graveyard),
                   "Hand" : set(self.player.hand)}

        if self._debug:
            choices["Library"] = list(self.player.library)

        selection = self.menu("Zone Info", None, *sorted(choices))

        selection = self.menu(selection, None, *choices[selection])
        self.prompt(self.card_info(selection))
