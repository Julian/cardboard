# coding: utf-8

from StringIO import StringIO
from textwrap import dedent
import unittest

import mock

from cardboard.card import Card
from cardboard.frontend import textual as t
from cardboard.tests.util import GameTestCase


class TestTextualFrontend(GameTestCase):
    def setUp(self):
        super(TestTextualFrontend, self).setUp()

        self.p1.frontend = self.tf = t.TextualFrontend(self.p1)
        self.f = self.p1.frontend.out_file = StringIO()

    def test_input(self):
        self.p1.frontend.in_file = StringIO(u"hello\n")
        self.assertEqual(self.tf.input(), "hello")
        self.assertEqual(self.f.getvalue(), self.tf.PS1.encode("utf-8"))

    def test_prompt(self):
        msg = u"héllo world"
        self.tf.prompt(msg)
        self.assertEqual(self.f.getvalue(), msg.encode("utf-8") + "\n")

        self.f = self.p1.frontend.out_file = StringIO()
        msg = "hello"
        self.tf.prompt(u"hello", end=u" world\n")
        self.assertEqual(self.f.getvalue(), u"hello world\n".encode("utf-8"))

    def test_formatted_prompt(self):
        msg = [u"foo", u"bar", u"baz"]

        self.tf.formatted_prompt(msg)
        formatted_msg = u"foo\nbar\nbaz\n"
        self.assertEqual(self.f.getvalue(), formatted_msg)

        self.f = self.p1.frontend.out_file = StringIO()
        self.tf.formatted_prompt(msg, header=u"Foo")
        formatted_msg = u"Foo\n\n    foo\n    bar\n    baz\n"
        self.assertEqual(self.f.getvalue(), formatted_msg)

        self.f = self.p1.frontend.out_file = StringIO()
        self.tf.formatted_prompt(msg, header=u"Foo", footer=u"Bla")
        formatted_msg = u"Foo\n\n    foo\n    bar\n    baz\n\nBla\n"
        self.assertEqual(self.f.getvalue(), formatted_msg)

        self.f = self.p1.frontend.out_file = StringIO()
        self.tf.formatted_prompt(msg, footer=u"Bla")
        formatted_msg = u"    foo\n    bar\n    baz\n\nBla\n"
        self.assertEqual(self.f.getvalue(), formatted_msg)


class TestTextualInfoDisplay(unittest.TestCase):

    tf = mock.Mock()
    game = tf.game
    p1, p2 = game.players = game.turn.order = [mock.Mock(), mock.Mock()]
    p1.opponents = [p2]
    tf.player = p1
    info = t.TextualInfoDisplay(tf)

    def test_card_info(self):
        class Bar(mock.Mock):
            name = u"Bar"
            type = u"Land"
            subtypes = []
            supertypes = []
            colors = ""
            mana_cost = None
            abilities = [u"T: Do bar."]
            power = toughness = loyalty = None

        bar_info = u"Bar\nLand\n\nT: Do bar."
        self.assertEqual(self.info.card(Bar), bar_info)

        class Foo(mock.Mock):
            name = u"Foo"
            type = u"Creature"
            subtypes = [u"Thing"]
            supertypes = []
            colors = "B"
            mana_cost = u"2BB"
            abilities = [u"Do foo.", "Do bar."]
            power = 2
            toughness = 3
            loyalty = None

        foo_info = (u"Foo                   2BB\n"
                    u"Creature — Thing\n\n"
                    u"Do foo.\n\n"
                    u"Do bar.\n\n"
                    u"                      2/3")

        self.assertEqual(self.info.card(Foo), foo_info)

    def test_player_overview(self):
        self.assertEqual(
            self.info.player_overview,
            u"You: {0.p1}\nOpponent: {0.p2}".format(self)
        )

    def test_player_overview_multiple_opponents(self):
        g = mock.Mock()
        g.players = g.turn.order = [mock.Mock(), mock.Mock(), mock.Mock()]
        tf = t.TextualFrontend(g.players[0])
        tf.game = g
        info = t.TextualInfoDisplay(tf)
        g.players[0].opponents = g.players[1:]

        self.assertEqual(
            info.player_overview,
            u"You: {}\nOpponents: {}, {}".format(*g.turn.order)
        )

    def test_turn_info(self):
        p = self.game.turn.phase = mock.MagicMock()
        s = self.game.turn.step = mock.MagicMock()

        p.__unicode__.return_value, s.__name__ = "Beginning", "untap"
        p.__len__.return_value = 2
        self.assertEqual(self.info.turn, u"Phase: Beginning\nStep: Untap")

        p.__unicode__.return_value = "First Main"
        p.__len__.return_value = 1
        self.assertEqual(self.info.turn, u"Phase: First Main")

    def test_zone_info(self):
        self.assertEqual(self.info.zone([1, 2, 3]), "1\n2\n3")


class TestSelector(unittest.TestCase):

    tf = t.TextualFrontend(mock.Mock())
    p1, p2 = tf.game.players = tf.game.turn.order = [mock.Mock(), mock.Mock()]
    tf.player = p1
    s = t.TextualSelector(tf)

    def setUp(self):
        super(TestSelector, self).setUp()
        self.f = self.tf.out_file = StringIO()

    def test_select(self):
        self.tf.in_file = StringIO(u"1\n1, 3\n")

        class Thing(object):
            def __init__(self, name):
                self.name = name

            def __str__(self):
                return self.name

        c = [Thing(u"bar"), Thing(u"foo"), Thing(u"baz")]

        sel = self.s(c)
        p = u"Select 1 choice.\n\n    1. bar\n    2. foo\n    3. baz\n\n▸▸▸ "
        self.assertEqual(self.f.getvalue(), p.encode("utf-8"))
        self.assertEqual(sel, [c[0]])

        self.assertEqual(self.s(c, how_many=2), [c[0], c[2]])

    def test_select_cards(self):
        self.s.choice = mock.Mock(return_value=[2, 4])
        self.s.cards(range(8), match=lambda i : i % 2 == 0, how_many=2)

        args, kwargs = self.s.choice.call_args
        kwargs["choices"] = list(kwargs["choices"])

        self.assertFalse(args)
        self.assertEqual(
            kwargs, dict(choices=[0, 2, 4, 6], how_many=2, duplicates=False)
        )

    def test_select_players(self):
        self.s.choice = mock.Mock(return_value=[self.p1, self.p1, self.p1])
        self.s.players(
            match=lambda p : p == self.p1, how_many=3, duplicates=True
        )

        args, kwargs = self.s.choice.call_args
        kwargs["choices"] = list(kwargs["choices"])

        self.assertFalse(args)
        self.assertEqual(
            kwargs, dict(choices=[self.p1], how_many=3, duplicates=True)
        )

    def test_select_range(self):
        self.tf.in_file = StringIO(u"13\n2, 6, 4\n1, 2, 3, 4, 5\n")

        sel = self.s.range(1, 21)

        p = u"Select a number between 1 and 20.\n▸▸▸ "
        self.assertEqual(self.f.getvalue(), p.encode("utf-8"))
        self.assertEqual(sel, [13])

        self.f = self.tf.out_file = StringIO()
        sel = self.s.range(1, 10, how_many=3)

        p = u"Select 3 numbers between 1 and 9.\n▸▸▸ "
        self.assertEqual(self.f.getvalue(), p.encode("utf-8"))
        self.assertEqual(sel, [2, 6, 4])

        self.f = self.tf.out_file = StringIO()
        sel = self.s.range(1, 6, how_many=None)

        p = u"Select some numbers between 1 and 5.\n▸▸▸ "
        self.assertEqual(self.f.getvalue(), p.encode("utf-8"))
        self.assertEqual(sel, [1, 2, 3, 4, 5])

        # invalid ranges
        with self.assertRaises(ValueError):
            self.s.range(5, 2)

        with self.assertRaisesRegexp(ValueError, "empty"):
            self.s.range(2, 2)
