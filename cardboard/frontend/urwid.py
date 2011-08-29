# coding: utf-8
from __future__ import absolute_import
import itertools

import urwid


class Player(object):

    count = itertools.count(1)

    def __init__(self):
        self.header = urwid.Text("Player {}".format(next(self.count)))
        self.battlefield = urwid.Edit("Type things here -> ","")
        self.status_bar = urwid.Text("Everything is just great")
        self.footer = urwid.Pile([self.battlefield, self.status_bar], focus_item=0 )
        self.content_list = [urwid.Text("content goes here")]
        self.content = urwid.ListBox(self.content_list)
        self.frame = urwid.Frame(self.content, self.header, self.footer, focus_part='footer')

def exit_on_q(input):
    if input in ('q', 'Q'):
        raise urwid.ExitMainLoop()

p1 = Player()
p2 = Player()

players = urwid.Pile([p2.frame,
                      urwid.Filler(urwid.Text("Notification bar", align="center"), "middle"),
                      p1.frame])

left_column = urwid.Filler(urwid.Edit("Hello world"), "top")
columns = urwid.Columns([
                        ("weight", .25, left_column),
                        ("weight", 1, players),
                        ], dividechars=1)

loop = urwid.MainLoop(columns, unhandled_input=exit_on_q)
loop.screen.set_terminal_properties(colors=256)
loop.run()
