# coding: utf-8
import sys
from textwrap import dedent

import zope.interface

from cardboard.card import characteristics
from cardboard.frontend import FrontendMixin
from cardboard.frontend.interfaces import IFrontend, IInfoDisplay, ISelector
from cardboard.util import ANY


class TextualInfoDisplay(object):

    zope.interface.implements(IInfoDisplay)

    def __init__(self, frontend):
        super(TextualInfoDisplay, self).__init__()

        self.frontend = frontend
        self.game = frontend.game

    def card(self, card):
        info = {k : v or u"" for k, v in characteristics(card).iteritems()}

        if card.mana_cost:
            info["name"] = info["name"].ljust(20)
            info["mana_cost"] = info["mana_cost"].rjust(5)

        if card.subtypes:
            info["subtypes"] = u" — {}".format(", ".join(card.subtypes))

        if card.power or card.toughness:
            info["pt"] = u"{power}/{toughness}".format(**info).rjust(25)
        else:
            info["pt"] = u""

        info["abilities"] = u"\n\n".join(info["abilities"])

        return dedent(u"""
                       {name}{mana_cost}
                       {type}{subtypes}

                       {abilities}

                       {pt}
                       """).format(**info).strip()

    @property
    def player_overview(self):
        self.game.require(started=True)

        s = "s" if len(self.frontend.player.opponents) > 1 else ""
        opponents = ", ".join(str(o) for o in self.game.turn.order
                                     if o in self.frontend.player.opponents)

        return dedent("""
                      You: {}
                      Opponent{}: {}
                      """).format(self.frontend.player, s, opponents).strip()

    @property
    def turn(self):
        phase = self.game.turn.phase
        info = ["Phase: {}".format(phase)]

        if len(phase) > 1:
            step = self.game.turn.step.__name__
            info.append("Step: {}".format(step.replace("_", " ").title()))

        return "\n".join(info)

    def zone(self, zone):
        return "\n".join(str(card) for card in zone)


class TextualSelector(object):

    zope.interface.implements(ISelector)

    def __init__(self, frontend):
        super(TextualSelector, self).__init__()

        self.frontend = frontend
        self.game = frontend.game

    def choice(self, choices, how_many=1, duplicates=False):
        num = u"your" if how_many is None else how_many
        s = u"s" if how_many is not None and how_many != 1 else ""

        self.frontend.formatted_prompt(
            header=u"Select {} choice{}.".format(num, s),
            body=(u"{}. {}".format(i, c) for i, c in enumerate(choices, 1)),
            end="\n"
        )

        selections = [int(s) for s in self.frontend.input().split(",")]
        return [choices[i - 1] for i in selections]

    __call__ = choice

    def cards(self, zone, match=ANY, how_many=1, duplicates=False):
        return self.choice(
            choices=(card for card in zone if match(card)),
            how_many=how_many,
            duplicates=duplicates,
        )

    def players(self, match=ANY, how_many=1, duplicates=False):
        return self.choice(
            choices=(player for player in self.game.players if match(player)),
            how_many=how_many,
            duplicates=duplicates,
        )

    def range(self, start, stop, how_many=1, duplicates=False):
        if how_many is None:
            num = u"some"
            s = u"s"
        elif how_many == 1:
            num = u"a"
            s = u""
        else:
            num = how_many
            s = u"s"

        prompt = u"Select {} number{} between {} and {}."
        self.frontend.prompt(prompt.format(num, s, start, stop - 1))
        return [int(s) for s in self.frontend.input().split(",")]


class TextualFrontend(FrontendMixin):

    zope.interface.implements(ISelector)

    info = TextualInfoDisplay
    select = TextualSelector

    PS1 = u"▸▸▸ "
    in_file, out_file = sys.stdin, sys.stdout

    def input(self):
        self.prompt(self.PS1, end="")
        return self.in_file.readline().rstrip()

    def priority_granted(self):
        pass

    def prompt(self, msg, end=u"\n"):
        self.out_file.write(msg.encode("utf-8"))
        self.out_file.write(end.encode("utf-8"))

    def formatted_prompt(self, body, header=None, footer=None, end=""):
        if header is not None:
            self.prompt(header, end=u"\n\n")
        if header or footer:
            body = (u"    " + line for line in body)
        for line in body:
            self.prompt(line)
        if footer is not None:
            self.prompt(u"\n" + footer)
        self.prompt(end, end="")

    def started_running(self):
        return self.main_menu()

    def main_menu(self):
        selection = self.formatted_prompt("Main Menu", self.player_info(), "Zone Info")
        getattr(self, selection.lower().replace(" ", "_"))()
