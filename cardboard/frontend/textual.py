# coding: utf-8
import sys
import textwrap

import zope.interface

from cardboard.frontend import FrontendMixin, IFrontend


# FIXME : > 2 Players
class TextualFrontend(FrontendMixin):

    zope.interface.implements(IFrontend)

    in_file, out_file = sys.stdin, sys.stdout

    def input(self):
        return self.in_file.readline().rstrip()

    def priority_granted(self):
        pass

    def prompt(self, msg, end=u"\n"):
        if not msg:
            return

        self.out_file.write(msg.encode("utf-8"))
        self.out_file.write(end.encode("utf-8"))

    def formatted_prompt(self, body, header="", footer="", end="\n"):
        if header:
            header = header + u"\n"
        if footer:
            footer = u"\n" + footer
        if header or footer:
            body = (u"    " + line for line in body)

        self.prompt(header)
        for line in body:
            self.prompt(line)
        self.prompt(footer, end=end)

    def select(self, choices, how_many=1, duplicates=False):
        choices = sorted(choices, key=str)
        num = u"your" if how_many is None else how_many
        s = u"s" if how_many is not None and how_many != 1 else ""

        self.formatted_prompt(
            header=u"Select {} choice{}.".format(num, s),
            body=(u"{}. {}".format(i, c) for i, c in enumerate(choices, 1)),
            footer=u"▸▸▸ ",
            end="",
        )

        selections = [int(s) for s in self.input().split(",")]
        return [choices[i - 1] for i in selections]

    def started_running(self):
        return self.main_menu()

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
        mana_cost = card.mana_cost or u""
        subtypes = pt = u""

        if card.subtypes:
            subtypes = u" — {}".format(", ".join(card.subtypes))

        if card.power or card.toughness:
            pt = u"\n{card.power}/{card.toughness}".format(card=card)

        abilities = "\n".join(card.abilities)

        return textwrap.dedent(u"""
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
