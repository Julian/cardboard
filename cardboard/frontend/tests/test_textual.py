# coding: utf-8
from __future__ import print_function

import mock

from cardboard.card import Card
from cardboard.frontend import textual as t
from cardboard.tests.util import GameTestCase


class TestTextualFrontend(GameTestCase):
    def setUp(self):
        super(TestTextualFrontend, self).setUp()
        self.p1.frontend = self.tf = t.TextualFrontend(self.p1)

    def test_repr(self):
        rpr = "<TextualFrontend to {}>".format(self.p1)
        self.assertEqual(repr(self.tf), rpr)

    def test_init(self):
        self.assertFalse(self.tf._debug)
        self.assertIs(self.tf.player, self.p1)

    def test_prompt(self):
        with mock.patch.object(t, "print", spec=print, create=True) as prnt:
            self.tf.prompt(u"hello", u"world", sep="", end="\n\n")

        h, w = u"hello".encode("utf-8"), u"world".encode("utf-8")
        prnt.assert_called_once_with(h, w, sep="", end="\n\n")

    def test_card_info(self):
        class Bar(mock.Mock):
            name = "Bar"
            type = "Land"
            subtypes = []
            mana_cost = None
            abilities = ["T: Do bar."]
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


braids_info = """\
┌───────────────────────────────┐
│  Braids, Cabal Minion    2BB  │
│ ┌───────────────────────────┐ │
│ │                           │ │
│ │                           │ │
│ │                           │ │
│ │                           │ │
│ └───────────────────────────┘ │
│  Creature — Minion Legend     │
│  ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈  │
│                               │
│   At the beginning of each    │
│   player's upkeep, that       │
│   player sacrifices an        │
│   artifact, creature, or      │
│   land.                       │
│                               │
│                               │
│                               │
│                               │
│                               │
│                               │
│                          2/2  │
└───────────────────────────────┘\
""".decode("utf-8")


zig_info = """\
┌───────────────────────────────┐
│  Ancient Ziggurat             │
│ ┌───────────────────────────┐ │
│ │                           │ │
│ │                           │ │
│ │                           │ │
│ │                           │ │
│ └───────────────────────────┘ │
│  Land                         │
│  ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈  │
│                               │
│  T: Add one mana of any       │
│  color to our mana pool.      │
│  Spend this mana only to      │
│  play creature spells.        │
│                               │
│                               │
│                               │
│                               │
│                               │
│                               │
│                               │
│                               │
└───────────────────────────────┘\
""".decode("utf-8")


prog_info = """\
┌───────────────────────────────┐
│  Progenitus       WWUUBBRRGG  │
│ ┌───────────────────────────┐ │
│ │                           │ │
│ │                           │ │
│ │                           │ │
│ │                           │ │
│ └───────────────────────────┘ │
│  Legendary Creature - Hydra Avatar  │
│  ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈  │
│                               │
│  Protection from everything   │
│                               │
│  If Progenitus would be put   │
│  into a graveyard from        │
│  anywhere, reveal Progenitus  │
│  and shuffle it into its      │
│  owner's library instead.     │
│                               │
│                               │
│                               │
│                               │
│                        10/10  │
└───────────────────────────────┘\
""".decode("utf-8")
