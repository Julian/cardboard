# -*- coding: utf-8 -*-
from __future__ import absolute_import

from zope.interface import implements
import urwid

from cardboard.frontend import interfaces
from cardboard.frontend.mixin import FrontendMixin, validate_selection
from cardboard.frontend.util import type_line
from cardboard.util import ANY


_ = urwid.AttrMap

ROUND_CORNERS = {
    "tlcorner" : u"╭", "trcorner" : u"╮", "blcorner" : u"╰", "brcorner" : u"╯"
}

NAME_CORNERS = {
    "tline" : u"_", "bline" : u"‾", "lline" : u"❲", "rline" : u"❳",
    "tlcorner" : u"", "trcorner" : u"", "blcorner" : u"", "brcorner" : u"",
}

palette = [
    ("default", "default", "default"),

    ("battlefield", "default", "default"),
    ("sidebar", "light gray", "black"),

    ("W", "white", "default"),
    ("U", "light blue", "default"),
    ("B", "dark gray", "default"),
    ("R", "dark red", "default"),
    ("G", "dark green", "default"),
    ("C", "brown", "default"),
    ("multicolor", "yellow", "default"),

    ("W background", "black", "white"),
    ("U background", "black", "light blue"),
    ("B background", "black", "dark gray"),
    ("R background", "black", "dark red"),
    ("G background", "black", "dark green"),
    ("C background", "black", "brown"),
    ("multicolor background", "black", "yellow"),

    ("W light tint", "default", "default"),
    ("U light tint", "default", "default"),
    ("B light tint", "default", "default"),
    ("R light tint", "default", "default"),
    ("G light tint", "default", "default"),
    ("C light tint", "default", "default"),
    ("multicolor light tint", "default", "default"),

    ("card border", "light gray", "black"),

    ("in focus", "black", "dark gray"),

    ("header", "black", "light blue"),
    ("overlay", "black", "dark gray"),
]


class Layout(object):
    def __init__(self, frontend):
        self.frontend = frontend

        self.active_card = None
        self._show_sidebar = True

        # XXX: Padding
        self.sidebar = _(urwid.Pile([
            ("weight", .4, self.active_card_widget),
            ("weight", .6, self.frontend.info.turn),
        ]), "sidebar")

        self.battlefield = _(urwid.Pile([]), "battlefield")

        self._columns = urwid.Columns([
            ("weight", .25, self.sidebar), ("weight", .75, self.battlefield),
        ])

        self.frame = urwid.Frame(self._columns)

        self.loop = urwid.MainLoop(
            self.frame,
            palette=palette,
            unhandled_input=self.unhandled_input,
            event_loop=urwid.TwistedEventLoop(),
        )

        self.loop.screen.set_terminal_properties(colors=256)

    def run(self):
        """
        Enter the main loop.

        """

        self.loop.run()

    @property
    def active_card_widget(self):
        if self.active_card is None:
            # XXX
            return urwid.Filler(urwid.Divider())
        return self.active_card

    @property
    def show_sidebar(self):
        return self._show_sidebar

    @show_sidebar.setter
    def show_sidebar(self, yesno):
        if yesno:
            # widget_list is a MonitoredList :/ be careful here not to ruin it
            self._columns.widget_list[:] = [self.sidebar, self.battlefield]
        else:
            self._columns.widget_list[:] = [self.battlefield]

        self._show_sidebar = yesno

    def _exit_overlay(self, button):
        self.loop.widget = self.loop.widget.bottom_w

    def show_overlay(
            self, w, title=None, width=50, height=50, focus_buttons=True
        ):
        """
        Show an overlay on top of the current top level widget.

        """

        if title is not None:
            title = _(urwid.Text(title, align="center"), "header")

        ok = urwid.Button("OK", on_press=self._exit_overlay)
        buttons = urwid.GridFlow(
            [ok], cell_width=10, h_sep=3, v_sep=1, align="center"
        )
        footer = _(buttons, "header")

        top = urwid.Frame(header=title, body=w, footer=footer)

        if focus_buttons:
            top.set_focus("footer")

        self.loop.widget = urwid.Overlay(
            top, self.loop.widget, align="center", valign="middle",
            width=("relative", width), height=("relative", height),
        )

    def unhandled_input(self, key):
        if key == "meta s":
            self.show_sidebar = not self.show_sidebar


class UrwidInfoDisplay(object):

    implements(interfaces.IInfoDisplay)

    def __init__(self, frontend):
        self.frontend = frontend
        self.game = frontend.game
        self._turn = frontend.game.turn

    @property
    def turn(self):
        phase, step = (
            self._turn.info if self.game.started else (u"Beginning", u"Untap")
        )
        info = [
            _(urwid.Text(u"Current Turn", align="center"), "header"),
            urwid.Text(phase + u" Phase", align="center")
        ]

        if step is not None:
            info.append(urwid.Text(step + u" Step", align="center"))

        return urwid.Filler(urwid.Pile(info))

    @property
    def player_overview(self):
        pass

    @property
    def zone_overview(self):
        pass

    def card_widget(self, card_widget):
        title = "Card: {.name}".format(card_widget)
        self.frontend.layout.show_overlay(card_widget, title=title)

    def card(self, card):
        return self.card_widget(Card(card))

    def player(self, player):
        title = "Player: {.name}".format(player)

    def zone(self, zone):
        title = zone.name.title()


class UrwidSelector(object):

    implements(interfaces.ISelector)

    def __init__(self, frontend):
        self.frontend = frontend
        self.game = frontend.game

    def choice(choices, how_many=1, duplicates=False):
        pass

    __call__ = choice

    def cards(
        self, zone=None, match=ANY, how_many=1, duplicates=False, bad=True
    ):
        pass

    def players(self, match=ANY, how_many=1, duplicates=False, bad=True):
        pass

    def combined(self, zone=None, match_cards=ANY, how_many_cards=1,
                 duplicate_cards=False, match_players=ANY, how_many_players=1,
                 duplicate_players=False, bad=True):
        pass

    def range(start, stop, how_many=1, duplicates=False):
        pass


class UrwidFrontend(FrontendMixin):

    implements(interfaces.IFrontend)

    info = UrwidInfoDisplay
    select = UrwidSelector

    def __init__(self, player, debug=False):
        super(UrwidFrontend, self).__init__(player=player, debug=debug)
        self.layout = Layout(self)

    def priority_granted(self):
        pass

    def prompt(self, msg, title=None, align="center", *args, **kwargs):
        text = urwid.Filler(urwid.Text(msg, align=align))
        self.layout.show_overlay(text, title=title, *args, **kwargs)

    def started_running(self):
        return self.layout.run()
