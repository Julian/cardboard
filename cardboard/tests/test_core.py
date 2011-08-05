import pprint
import unittest

import mock
import panglery

from cardboard import core as c, events as e
from cardboard.tests.util import ANY


class TestManaPool(unittest.TestCase):
    def test_repr(self):
        o = mock.Mock()
        m = c.ManaPool(o)
        self.assertEqual(repr(m), "[0B, 0G, 0R, 0U, 0W, 0]")

        m.black, m.green, m.red, m.blue, m.white, m.colorless = range(1, 7)
        self.assertEqual(repr(m), "[1B, 2G, 3R, 4U, 5W, 6]")


class TestBehavior(unittest.TestCase):
    def setUp(self):
        self.events = mock.Mock()
        self.game = c.Game(self.events)
        self.p1 = self.game.add_player(library=[], life=1, hand_size=0)
        self.p2 = self.game.add_player(library=[], life=1, hand_size=0)
        self.game.start()

    def test_advance(self):
        self.assertIs(self.game.turn, self.p1)

        self.assertEqual(self.game.phase, "beginning")
        self.assertEqual(self.game.subphase, "untap")

        for phase, subphase in [("beginning", "draw"),
                                ("beginning", "upkeep"),
                                ("first main", None),
                                ("combat", "beginning"),
                                ("combat", "declare attackers"),
                                ("combat", "declare blockers"),
                                ("combat", "combat damage"),
                                ("combat", "end"),
                                ("second main", None),
                                ("ending", "end"),
                                ("ending", "cleanup")]:

            self.game.advance()
            self.assertEqual(self.game.phase, phase)
            self.assertEqual(self.game.subphase, subphase)

        self.game.advance()

        self.assertIs(self.game.turn, self.p2)

        self.assertEqual(self.game.phase, "beginning")
        self.assertEqual(self.game.subphase, "untap")

    def test_draw(self):
        self.p1.library = [0]
        self.p1.draw()
        self.assertEqual(self.p1.hand, {0})

        self.p2.library = range(5)
        self.p2.draw(5)
        self.assertEqual(self.p2.hand, set(range(5)))

    def test_dont_die_when_drawing_zero_cards(self):
        self.assertFalse(self.p1.dead)
        self.p1.draw(0)
        self.assertFalse(self.p1.dead)

    def test_negatives(self):
        self.assertRaises(ValueError, self.p1.draw, -1)
        self.assertRaises(ValueError, setattr, self.p1.mana_pool, "black", -1)


class TestEvents(unittest.TestCase):
    def setUp(self):
        self.events = mock.Mock()
        self.game = c.Game(self.events)
        self.p1 = self.game.add_player(library=[], life=1, hand_size=0)
        self.p2 = self.game.add_player(library=[], life=1, hand_size=0)

    def assertHeard(self, event, with_request=False, handler=None):
        if handler is None:
            handler = self.events

        e = {"event" : event, "pool" : ANY}

        if not with_request:
            return handler.trigger.assert_called_with(**e)

        r = {"request" : event, "pool" : ANY}
        self.assertEqual(handler.trigger.call_args_list[-2:], [[r], [e]])

    def assertNotHeard(self, event, with_request=False, handler=None):
        try:
            self.assertHeard(event, with_request, handler)
        except AssertionError:
            return
        else:
            self.fail("{} was triggered by the handler.".format(event))

    def test_die(self):
        self.p1.die()
        self.assertHeard(e.events.player["died"], with_request=True)

    """
    # FIXME: This should pass, need to patch a real pangler correctly or think
    # of the right way to test these
    def test_game_over(self):
        events = panglery.Pangler()
        trigger = mock.Mock()
        trigger.side_effect = events.trigger
        events.trigger = trigger

        p1 = c.Player(events, deck=[], life=1, hand_size=0)
        p2 = c.Player(events, deck=[], life=2, hand_size=0)
        s = c.Game(events, players=[p1, p2])

        # TODO: patch this to check that p2 didn't die here yet
        p2.life -= 1

        p2.life -= 1
        self.assertHeard(e.events.player["died"], handler=events)

        p1.life -= 1
        self.assertHeard(e.events.game["ended"], with_request=True,
                         handler=events)
    """

    def test_life_changed(self):
        self.p1.life += 2
        self.assertHeard(e.events.player.life["gained"], with_request=True)

        self.p1.life -= 2
        self.assertHeard(e.events.player.life["lost"], with_request=True)

    def test_card_drawn(self):
        self.p1.library = [1]
        self.p1.draw()
        self.assertHeard(e.events.player["draw"], with_request=True)

        def side_effect(*args, **kwargs):
            if e.events.player["draw"] in kwargs.viewvalues():
                self.fail("Unexpected card draw")
            return mock.DEFAULT

        self.events.trigger.side_effect = side_effect

        self.p1.draw()
        self.assertHeard(e.events.player["died"])

    def test_move_to_graveyard(self):
        self.p1.move_to_graveyard(object())
        self.assertHeard(e.events.card.graveyard["entered"], with_request=True)

    def test_remove_from_game(self):
        self.p1.remove_from_game(object())
        self.assertHeard(e.events.card["removed from game"],
                         with_request=True)

    def test_mana_changed(self):
        self.p1.mana_pool.red += 0
        self.assertNotHeard(e.events.player.mana.red["added"],
                            with_request=True)

        self.p1.mana_pool.red += 1
        self.assertHeard(e.events.player.mana.red["added"], with_request=True)

        self.p1.mana_pool.red -= 1
        self.assertHeard(e.events.player.mana.red["left"], with_request=True)
