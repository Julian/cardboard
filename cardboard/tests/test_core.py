import pprint
import unittest

import mock
import panglery

from cardboard import core as c, events as e
from cardboard.tests.util import ANY


class TestBehavior(unittest.TestCase):
    def test_advance(self):
        p1 = c.Player(deck=[], handler=mock.Mock(), life=1, hand_size=0)
        p2 = c.Player(deck=[], handler=mock.Mock(), life=1, hand_size=0)
        s = c.State(players=[p1, p2], handler=mock.Mock())

        self.assertIs(s.turn, p1)

        self.assertEqual(s.phase, "beginning")
        self.assertEqual(s.subphase, "untap")

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

            s.advance()
            self.assertEqual(s.phase, phase)
            self.assertEqual(s.subphase, subphase)

        s.advance()

        self.assertIs(s.turn, p2)

        self.assertEqual(s.phase, "beginning")
        self.assertEqual(s.subphase, "untap")

    def test_draw(self):
        p = mock.Mock()
        p1 = c.Player(deck=[0], handler=p, life=1, hand_size=0)
        p1.draw()
        self.assertEqual(p1.hand, {0})

        p2 = c.Player(deck=range(5), handler=p, life=1, hand_size=0)
        p2.draw(5)
        self.assertEqual(p2.hand, set(range(5)))

    def test_dont_die_when_drawing_zero_cards(self):
        p = mock.Mock()
        p1 = c.Player(deck=[0], handler=p, life=1, hand_size=0)
        self.assertFalse(p1.dead)
        p1.draw(0)
        self.assertFalse(p1.dead)


class TestPlayerStateEvents(unittest.TestCase):
    def setUp(self):
        self.events = mock.Mock()
        self.p1 = c.Player(self.events, deck=range(3), life=1, hand_size=0)
        self.p2 = c.Player(self.events, deck=range(3), life=2, hand_size=0)

    def assertHeard(self, event, with_request=False, handler=None):
        if handler is None:
            handler = self.events

        e = {"event" : event, "pool" : ANY}

        if not with_request:
            return handler.trigger.assert_called_with(**e)

        r = {"request" : event, "pool" : ANY}
        self.assertEqual(handler.trigger.call_args_list[-2:], [[r], [e]])

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
        s = c.State(events, players=[p1, p2])

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
        p1 = c.Player(deck=[1], handler=self.events, life=1, hand_size=0)
        p1.draw()

        self.assertHeard(e.events.player["draw"], with_request=True)

        def side_effect(*args, **kwargs):
            if e.events.player.draw in kwargs.viewvalues():
                self.fail("Unexpected card draw")
            return mock.DEFAULT

        self.events.trigger.side_effect = side_effect

        p1.draw()
        self.assertHeard(e.events.player["died"])

    def test_move_to_graveyard(self):
        self.p1.move_to_graveyard(object())
        self.assertHeard(e.events.card.graveyard["entered"], with_request=True)

    def test_remove_from_game(self):
        self.p1.remove_from_game(object())
        self.assertHeard(e.events.card["removed_from_game"],
                         with_request=True)

    def test_mana_changed(self):
        self.p1.mana_pool.red += 1
        self.assertHeard(e.events.player.mana.red["added"], with_request=True)

        self.p1.mana_pool.red -= 1
        self.assertHeard(e.events.player.mana.red["left"], with_request=True)
