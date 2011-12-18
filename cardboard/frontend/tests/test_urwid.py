# -*- coding: utf-8 -*-

import unittest

import mock
import urwid

from cardboard.core import Player
from cardboard.frontend import urwid as u
from cardboard.tests.util import GameTestCase


class TestLayout(unittest.TestCase):
    def setUp(self):
        super(TestLayout, self).setUp()
        self.frontend = mock.Mock(spec=u.UrwidFrontend)
        self.u = u.Layout(frontend=self.frontend)

    def test_run(self):
        self.assertIsInstance(self.u.loop, urwid.MainLoop)

        # we don't want the main loop to actually run
        with mock.patch(u.__name__ + ".urwid.MainLoop.run") as mock_run:
            self.u.run()
            self.assertIs(self.u.loop.widget, self.u.frame)

    def test_unhandled_input(self):
        self.assertTrue(self.u.show_sidebar)
        self.u.unhandled_input("meta s")
        self.assertFalse(self.u.show_sidebar)

    def test_show_overlay(self):
        # the loop must be running already to show an overlay
        with mock.patch(u.__name__ + ".urwid.MainLoop.run") as mock_run:
            self.u.run()

        text = urwid.Text(u"Hello")
        self.u.show_overlay(text)
        overlay = self.u.loop.widget

        self.assertIsInstance(overlay, urwid.Overlay)
        self.assertIs(overlay.top_w.body, text)
        self.assertIsNone(overlay.top_w.header)

        # focus is on the buttons by default
        self.assertIs(overlay.top_w.focus_part, "footer")

        # clicking the button exits the overlay
        overlay.top_w.footer.base_widget.cells[0].keypress((15,), "enter")
        self.assertIs(self.u.loop.widget, self.u.frame)

        edit = urwid.Edit(">>> ")
        self.u.show_overlay(edit, title=u"Hey", focus_buttons=False)

        overlay = self.u.loop.widget
        self.assertIs(overlay.top_w.focus_part, "body")
        self.assertEqual(overlay.top_w.header.base_widget.text, u"Hey")

    def test_active_card(self):
        self.assertIsNone(self.u.active_card)
        self.assertIsInstance(self.u.active_card_widget, urwid.Filler)

    def test_show_sidebar(self):
        self.assertTrue(self.u.show_sidebar)
        self.assertIs(self.u._columns.widget_list[0], self.u.sidebar)
        self.assertIsInstance(self.u._columns.widget_list, urwid.MonitoredList)

        self.u.show_sidebar = False
        self.assertFalse(self.u.show_sidebar)
        self.assertEqual(self.u._columns.widget_list, [self.u.battlefield])
        self.assertIsInstance(self.u._columns.widget_list, urwid.MonitoredList)

        self.u.show_sidebar = True
        self.assertTrue(self.u.show_sidebar)
        self.assertIs(self.u._columns.widget_list[0], self.u.sidebar)
        self.assertIsInstance(self.u._columns.widget_list, urwid.MonitoredList)


class TestUrwidInfoDisplay(unittest.TestCase):
    def setUp(self):
        super(TestUrwidInfoDisplay, self).setUp()
        self.layout = mock.Mock(spec=u.Layout)
        self.layout.frontend = self.frontend = mock.Mock()
        self.i = u.UrwidInfoDisplay(frontend=self.layout.frontend)

    def test_turn(self):
        # start on untap step even when the game hasn't started yet
        self.frontend.game.turn.info = None
        self.frontend.game.started = False
        turn = [w.text for w in self.i.turn.base_widget.widget_list]
        self.assertEqual(turn, ["Beginning", "Untap"])

        self.frontend.game.started = True
        self.frontend.game.turn.info = "Foo", "Bar"
        turn = [w.text for w in self.i.turn.base_widget.widget_list]
        self.assertEqual(turn, ["Foo", "Bar"])

        self.frontend.game.turn.info = "Foo", None
        turn = [w.text for w in self.i.turn.base_widget.widget_list]
        self.assertEqual(turn, ["Foo"])


class TestUrwidSelector(unittest.TestCase):
    def setUp(self):
        super(TestUrwidSelector, self).setUp()
        self.layout = mock.Mock(spec=u.Layout)
        self.layout.frontend = self.frontend = mock.Mock()
        self.s = u.UrwidSelector(frontend=self.layout.frontend)


class TestUrwidFrontend(GameTestCase):
    def setUp(self):
        super(TestUrwidFrontend, self).setUp()
        self.f = u.UrwidFrontend(self.p1)
        self.f.layout = self.layout = mock.Mock(spec=u.Layout)

    def test_prompt(self):
        self.f.prompt(u"Hello World")
        (w,), kwargs = self.layout.show_overlay.call_args
        self.assertEqual(w.base_widget.text, u"Hello World")
        self.assertEqual(kwargs, {"title" : None})

        self.f.prompt(u"Hello", title=u"World")
        (w,), kwargs = self.layout.show_overlay.call_args
        self.assertEqual(kwargs, {"title" : u"World"})

    def test_started_running(self):
        self.f.started_running()
        self.layout.run.assert_called_once_with()
