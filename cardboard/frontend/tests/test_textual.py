# coding: utf-8

from StringIO import StringIO
from textwrap import dedent

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

    def test_prompt(self):
        # no trailing newline for empty msg
        self.tf.prompt(u"")
        self.assertFalse(self.f.getvalue())

        msg = u"héllo world"
        self.tf.prompt(msg)
        self.assertEqual(self.f.getvalue(), msg.encode("utf-8") + "\n")

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

    def test_select(self):
        self.p1.frontend.in_file = StringIO(u"1\n1, 3\n")

        class Thing(object):
            def __init__(self, name):
                self.name = name

            def __str__(self):
                return self.name

        c = [Thing(u"bar"), Thing(u"foo"), Thing(u"baz")]

        sel = self.tf.select(c)
        p = u"Select 1 choice.\n\n    1. bar\n    2. baz\n    3. foo\n\n▸▸▸ "
        print p
        self.assertEqual(self.f.getvalue(), p.encode("utf-8"))

        self.assertEqual(sel, [c[0]])

        sel = self.tf.select(c, how_many=2)
        self.assertEqual(sel, [c[0], c[1]])

    def test_card_info(self):
        class Bar(mock.Mock):
            name = u"Bar"
            type = u"Land"
            subtypes = []
            mana_cost = None
            abilities = [u"T: Do bar."]
            power = toughness = None

        # NOTE: don't really care at the moment but maybe later trim spaces
        bar_info = (u"Bar                 \n"
                    u"Land\n\n"
                    u"T: Do bar.")

        self.assertEqual(self.tf.card_info(Bar), bar_info)

        class Foo(mock.Mock):
            name = "Foo"
            type = "Creature"
            subtypes = ["Thing"]
            mana_cost = "2BB"
            abilities = ["Do foo.", "Do bar."]
            power = 2
            toughness = 3

        foo_info = (u"Foo                 2BB\n"
                    u"Creature — Thing\n\n"
                    u"Do foo.\n"
                    u"Do bar.\n"
                    u"2/3")

        self.assertEqual(self.tf.card_info(Foo), foo_info)

    def test_player_info(self):
        self.game.start()
        self.assertEqual(self.tf.player_info(),
                         u"You: {0.p1}\nOpponent: {0.p2}".format(self))

    def test_player_info_multiple_opponents(self):
        self.game.add_existing_player(self.p3)
        self.game.start()

        self.game.turn.order = [self.p1, self.p2, self.p3]

        self.assertEqual(
            self.tf.player_info(),
            u"You: {}\nOpponents: {}, {}".format(*self.game.turn.order)
        )

    def test_turn_info(self):
        self.game.start()

        self.assertEqual(self.tf.turn_info(), u"Phase: Beginning\nStep: Untap")

        for _ in "untap", "upkeep", "draw":
            self.game.turn.next()

        self.assertEqual(self.tf.turn_info(), u"Phase: First Main")
