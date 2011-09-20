# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import urwid

from cardboard.frontend import util


# TODO: Configure mana costs symbols via configparser
#                 display name, abilities
#       animated panes
#       highlight currently selected player in sidebar
#       don't show player changer if only one team member


palette = [
    ("default", "default", "default"),

    ("battlefield", "black", "dark gray"),
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

    ("dialog frame", "black", "light blue"),
    ("dialog", "black", "dark gray"),
]


class UrwidFrontend(object):
    def __init__(self, to):
        super(UrwidFrontend, self).__init__()

        # XXX: Remove, debug
        to.game.start()

        self._debug = False

        self.game = to.game
        self.player = to

        self.layout = Layout(self)
        self.loop = None

    def __repr__(self):
        return "<UrwidFrontend to {.name}>".format(self.player)

    def priority_granted(self):
        pass

    def prompt(self, *args, **kwargs):
        return self.layout.prompt(*args, **kwargs)

    def select_range(self, start, stop, how_many=1):
        pass

    def select_cards(*matchers, **kwargs):
        pass

    def select_players(*matchers, **kwargs):
        pass

    def run(self):
        self.loop = urwid.MainLoop(self.layout.frame,
                                   palette=palette,
                                   unhandled_input=self.layout.unhandled_input)

        self.loop.screen.set_terminal_properties(colors=256)
        self.loop.run()

    def card_info(self, card):
        return self.layout.card_info(card)


class Layout(object):
    def __init__(self, frontend):
        super(Layout, self).__init__()

        self.frontend = frontend

        self.active_card = Card(next(iter(self.frontend.player.hand)))
        self.sidebar = sidebar(self)

        self.top = urwid.Columns([
            PlayerPane(player, top=True) for player in self.top_players
        ])

        notifications = urwid.Text("Notifications", align="center")
        self.notification_area = urwid.Filler(notifications)

        self.bottom = urwid.Columns([
            PlayerPane(player, top=False) for player in self.bottom_players
        ])

        field = urwid.Pile([self.top, self.notification_area, self.bottom])
        self.battlefield = pad(field, 2)

        self.columns = urwid.Columns([("weight", .25, self.sidebar),
                                      ("weight", 1, self.battlefield)])

        self.frame = urwid.Frame(self.columns)

    @property
    def top_players(self):
        # FIXME
        opponents = self.frontend.player.opponents
        return (p for p in self.frontend.game.turn.order if p in opponents)

    @property
    def bottom_players(self):
        # FIXME
        teammates = self.frontend.player.teammates
        order = [p for p in self.frontend.game.turn.order if p in teammates]
        order.insert(len(order) // 2, self.frontend.player)
        return order

    def unhandled_input(self, key):
        if key in {"q", "Q"}:
            raise urwid.ExitMainLoop()
        elif key in {"o", "O"}:
            class VoltaicKey(object):
                name = u"Voltaic Key"
                mana_cost = u"2WUUBRRRG"
                type = u"Artifact"
                subtypes = set()
                power = toughness = 1
                abilities = [u"1, T: Untap target artifact."]
                colors = set()

            self.card_info(VoltaicKey)

    def prompt(self, msg, title=None, *args, **kwargs):
        text = urwid.Text(msg, align="center")
        body = urwid.AttrMap(urwid.Filler(text), "dialog")
        self.show_dialog(body, title=title, *args, **kwargs)

    def show_dialog(self, content, title=None, width=50, height=50,
                    focus_buttons=True):

        if title is not None:
            title = urwid.Text(title, align="center")
            title = urwid.AttrMap(title, "dialog frame")

        ok = urwid.Button("OK", on_press=self._exit_dialog)
        buttons = urwid.GridFlow([ok], cell_width=10, h_sep=3, v_sep=1,
                                 align="center")
        footer = urwid.AttrMap(buttons, "dialog frame")

        dialog = urwid.Frame(header=title, body=content, footer=footer)

        if focus_buttons:
            dialog.set_focus("footer")

        overlay = urwid.Overlay(dialog, self.frame, align="center",
                                valign="middle", width=("relative", width),
                                height=("relative", height))

        self.frontend.loop.widget = overlay

    def _exit_dialog(self, button):
        self.frontend.loop.widget = self.frame

    def card_info(self, card):
        title = "Card: {.name}".format(card)
        self.show_dialog(Card(card), title=title, width=40, height=60)


class Slider(urwid.WidgetWrap):
    """
    Slide across a series of widgets showing one column at a time.

    Arguments
    ---------

    * slides: An iterable of 2-tuples containing a slide name (or None) and a
              widget to display in the slide

    * show_header: whether to render the header (default: True)

    * tabbed: If True, show all slide names as tabs in the header.  Otherwise,
              only the current slide's name is shown (default: False)

    """

    slider_left = urwid.Text("◀")
    slider_right = urwid.Text("▶")

    def __init__(self, slides, show_header=True, tabbed=False):
        frames = urwid.Columns([
            urwid.Frame(
                slide, header=urwid.Columns([("fixed", 1, self.slider_left),
                                             urwid.Text(name, align="center"),
                                             ("fixed", 1, self.slider_right)],
                                            dividechars=1)
            )
            for name, slide in slides
        ])

        super(Slider, self).__init__(frames)

        self.show_header = show_header
        self.tabbed_header = tabbed

    def render(self, size, focus=False):
        current_column = self._w.get_focus()

        if self.show_header:
            return current_column.render(size, focus=focus)
        else:
            return current_column.body.render(size, focus=focus)

    def sizing(self):
        return {urwid.BOX}


class PlayerPane(urwid.WidgetWrap):
    def __init__(self, player, top):
        self.player = player

        self.battlefield = urwid.Filler(
            urwid.Text("Battlefield for {}".format(self.player))
        )

        self.vitals = urwid.Columns([
            urwid.Text("Life: {.life}".format(self.player)),
            urwid.Text("Hand: {}".format(len(self.player.hand))),
            urwid.Text("Library: {}".format(len(self.player.library))),
        ])

        self.mana_pool = urwid.Columns([
            urwid.Text((attr, "● {}".format(color)))
            for attr, color in zip("WUBRGC", self.player.mana_pool)
        ])


        self.status_bar = urwid.Columns([
            self.vitals,
            ("weight", 2, urwid.Text(self.player.name, align="center")),
            self.mana_pool
        ])

        pile = [("flow", self.status_bar), self.battlefield]
        pile = urwid.Pile(pile if top else pile[::-1])

        super(PlayerPane, self).__init__(pile)


    def __repr__(self):
        return "<PlayerPane: {.name}>".format(self.player)


class Card(urwid.WidgetWrap):
    def __init__(self, card):
        self.card = card

        name = urwid.Text(card.name)
        mana_cost = color_cost(card.mana_cost, align="right")
        name_line = rounded_box(name, mana_cost)
        name_line = urwid.AttrMap(name_line, self._color + " light tint")

        picture = pad(urwid.LineBox(urwid.Divider(top=3)))
        picture = urwid.AttrMap(urwid.Filler(picture), "default")

        type = rounded_box(urwid.Text(util.type_line(card)))
        type = urwid.AttrMap(type, self._color + " light tint")

        abilities = [focus(urwid.Text(abil)) for abil in card.abilities]
        abilities = urwid.ListBox(urwid.SimpleListWalker(abilities))
        abilities = urwid.AttrMap(abilities, self._color + " light tint")

        if card.power or card.toughness:
            pt = "{0.power}/{0.toughness}".format(card)
            pt = urwid.Filler(urwid.Text(pt, align="right"))
            pt = urwid.AttrMap(pt, self._color + " light tint")
        else:
            pt = urwid.Filler(urwid.Divider())

        pile = pad(urwid.Pile([name_line, picture, type, abilities, pt]))
        pile = urwid.AttrMap(pile, self._color + " background")

        info = pad(urwid.LineBox(pile))
        box = urwid.LineBox(urwid.AttrMap(info, "card border"))

        padding = urwid.Padding(box, align="center", width=("relative", 90))

        super(Card, self).__init__(padding)

    @property
    def _color(self):
        colors = self.card.colors

        if len(colors) > 1:
            return "multicolor"
        elif not colors:
            return "C"
        else:
            color, = colors
            return color


class ListCard(urwid.Text):

    _selectable = True

    def __init__(self, card, hidden=False):
        super(ListCard, self).__init__(card.name)

        self.card = card
        self.hidden = hidden

    def get_text(self):
        if self.hidden:
            text = "- Hidden -"
        else:
            text = self._text

        return text, self._attrib

    def keypress(self, size, key):
        return key


def zone_slider(player, revealed=False):
    zones = []

    for zone in player.hand, player.graveyard, player.exile:
        if not zone.ordered:
            cards = [focus(ListCard(card)) for card in sorted(zone)]
        else:
            cards = [focus(ListCard(card)) for card in zone]

        walker = urwid.SimpleListWalker(cards)
        title = "{.name}'s {.name}".format(player, zone)
        zones.append((title, urwid.ListBox(walker)))

    library = [focus(ListCard(card, hidden=True)) for card in player.library]
    title = "{.name}'s {.name}".format(player, player.library)
    zones.append((title, urwid.ListBox(urwid.SimpleListWalker(library))))

    return Slider(zones)


def focus(widget, unfocused=None):
    return urwid.AttrMap(widget, unfocused, "focus")


def sidebar(layout):
    zones = urwid.AttrMap(zone_slider(layout.frontend.player), "battlefield")
    step = urwid.Filler(urwid.Text(layout.frontend.game.turn.step.__name__))
    content = urwid.Pile([("weight", 2, layout.active_card),
                          urwid.Filler(urwid.Divider()),
                          ("weight", 1, zones),
                          ("weight", 1, step)])
    return urwid.AttrMap(content, "sidebar")


def pad(widget, n=1):
    return urwid.Padding(widget, ("fixed left", n), ("fixed right", n))


def rounded_box(*widgets):
    # TODO: urwid tip just replace with linebox
    #   corners = {"tlcorner" : u"╭", "trcorner" : u"╮",
    #              "blcorner" : u"╰", "brcorner" : u"╯"}

    top = pad(urwid.Divider(u"_"))
    left = ("fixed", 2, urwid.Text(u"("))
    right = ("fixed", 2, urwid.Text(u")", align="right"))
    bottom = pad(urwid.Divider(u"‾"))

    sides = urwid.Columns((left,) + widgets + (right,))
    border = urwid.Pile([top, sides, bottom])

    return urwid.Filler(border)


def color_cost(mana_cost, *args, **kwargs):
    colored = [(c if c.isalpha() else "colorless", c) for c in mana_cost or ""]
    return urwid.Text(colored, *args, **kwargs)
