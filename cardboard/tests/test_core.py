import pprint
import unittest

import mock
import panglery

from cardboard import core as c, events as e, exceptions as exc
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

    def test_initialize_turn_and_phase(self):
        self.assertIs(self.game.turn, self.p1)
        self.assertEqual(self.game.phase, "beginning")
        self.assertEqual(self.game.subphase, "untap")

    def test_next_phase(self):
        self.game.next_turn = mock.Mock()

        for phase, subphase in [("beginning", "draw"),
                                ("beginning", "upkeep"),
                                ("first_main", None),
                                ("combat", "beginning"),
                                ("combat", "declare_attackers"),
                                ("combat", "declare_blockers"),
                                ("combat", "combat_damage"),
                                ("combat", "end"),
                                ("second_main", None),
                                ("ending", "end"),
                                ("ending", "cleanup")]:

            self.game.next_phase()
            self.assertEqual(self.game.phase, phase)
            self.assertEqual(self.game.subphase, subphase)

        # check calls next_turn at end of last subphase
        self.assertFalse(self.game.next_turn.called)
        self.game.next_phase()
        self.assertTrue(self.game.next_turn.called)

    def test_phase_set(self):
        # just move to the middle of a turn somewhere
        for i in range(6):
            self.game.next_phase()

        self.assertIs(self.game.turn, self.p1)
        self.assertNotEquals(self.game.phase, "beginning")
        self.assertNotEquals(self.game.subphase, "untap")

        self.game.phase = "beginning"

        self.assertIs(self.game.turn, self.p1)
        self.assertEquals(self.game.phase, "beginning")
        self.assertEquals(self.game.subphase, "untap")

        # check that next_phase still works
        self.test_next_phase()

    def test_phase_set_nonexisting(self):
        self.assertRaises(ValueError, setattr, self.game, "phase", object())

    def test_next_turn(self):
        self.assertIs(self.game.turn, self.p1)
        self.game.next_turn()
        self.assertIs(self.game.turn, self.p2)
        self.assertEqual(self.game.phase, "beginning")
        self.assertEqual(self.game.subphase, "untap")

    def test_turn_set(self):
        events = mock.Mock()
        game = c.Game(events)
        p1 = game.add_player(library=[], life=1, hand_size=0)
        p2 = game.add_player(library=[], life=2, hand_size=0)
        p3 = game.add_player(library=[], life=3, hand_size=0)
        game.start()

        game.turn = p3

        self.assertIs(game.turn, p3)
        self.assertEqual(game.phase, "beginning")
        self.assertEqual(game.subphase, "untap")

    def test_turn_set_nonexisting(self):
        self.assertRaises(ValueError, setattr, self.game, "turn", object())

    def test_next_turn_from_middle(self):
        # just move to the middle of a turn somewhere
        for i in range(4):
            self.game.next_phase()

        self.game.next_turn()
        self.assertIs(self.game.turn, self.p2)
        self.assertEqual(self.game.phase, "beginning")
        self.assertEqual(self.game.subphase, "untap")

    def test_unstarted_game(self):
        game = c.Game(mock.Mock())

        self.assertIs(game.game_over, None)

        self.assertIs(game.turn, None)
        self.assertIs(game.phase, None)
        self.assertIs(game.subphase, None)

        self.assertFalse(game.started)

        self.assertRaises(exc.RuntimeError, setattr, game, "phase", "ending")
        self.assertRaises(exc.RuntimeError, setattr, game, "turn", object())
        self.assertRaises(exc.RuntimeError, game.next_phase)
        self.assertRaises(exc.RuntimeError, game.next_turn)

    def test_no_player_game(self):
        game = c.Game(mock.Mock())
        self.assertRaises(exc.RuntimeError, game.start)

    def test_draw(self):
        self.p1.library = [0]
        self.p1.draw()
        self.assertEqual(self.p1.hand, {0})

        self.p2.library = range(5)
        self.p2.draw(5)
        self.assertEqual(self.p2.hand, set(range(5)))

    def test_cast(self):
        permanent = mock.Mock()
        permanent.is_permanent = True

        nonpermanent = mock.Mock()
        nonpermanent.is_permanent = False

        self.p1.put_into_play = mock.Mock()
        self.p1.move_to_graveyard = mock.Mock()

        self.p1.cast(permanent)

        self.p1.put_into_play.assert_called_once_with(permanent)
        self.assertFalse(self.p1.move_to_graveyard.called)

        self.p1.put_into_play = mock.Mock()
        self.p1.move_to_graveyard = mock.Mock()

        self.p1.cast(nonpermanent)

        self.p1.move_to_graveyard.assert_called_once_with(nonpermanent)
        self.assertFalse(self.p1.put_into_play.called)

    def test_put_into_play(self):
        card = mock.Mock()
        self.p1.put_into_play(card)

        self.assertIn(card, self.game.field)
        self.assertEqual(card.owner, self.p1)

    def test_dont_die_when_drawing_zero_cards(self):
        self.assertFalse(self.p1.dead)
        self.p1.draw(0)
        self.assertFalse(self.p1.dead)

    def test_negatives(self):
        self.assertRaises(ValueError, self.p1.draw, -1)
        self.assertRaises(ValueError, setattr, self.p1.mana_pool, "black", -1)


def pool(**kwargs):
    kwargs["pool"] = ANY
    return kwargs


class TestEvents(unittest.TestCase):
    def setUp(self):
        self.events = mock.Mock()
        self.game = c.Game(self.events)
        self.p1 = self.game.add_player(library=[], life=1, hand_size=0)
        self.p2 = self.game.add_player(library=[], life=2, hand_size=0)

    def assertHeard(self, event, request=False, handler=None):
        if handler is None:
            handler = self.events

        e = pool(event=event)
        r = pool(request=event)

        if not request:
            return handler.trigger.assert_called_with(**e)

        arg_list = handler.trigger.call_args_list
        self.assertEqual(handler.trigger.call_args_list[-2:], [[r], [e]])

    def assertNotHeard(self, event, request=False, handler=None):
        try:
            self.assertHeard(event, request, handler)
        except (AssertionError, IndexError):
            return
        else:
            self.fail("{} was triggered by the handler.".format(event))

    def test_game_started(self):
        self.game.start()
        self.events.trigger.assert_called_with(e.events.game.started)

    @unittest.skip
    def test_next_phase(self):
        self.assertIs(self.game.turn, self.p1)

        self.assertEqual(self.game.phase, "beginning")
        self.assertEqual(self.game.subphase, "untap")

        for phase, subphase in [("beginning", "draw"),
                                ("beginning", "upkeep"),
                                ("first_main", None),
                                ("combat", "beginning"),
                                ("combat", "declare attackers"),
                                ("combat", "declare blockers"),
                                ("combat", "combat damage"),
                                ("combat", "end"),
                                ("second_main", None),
                                ("ending", "end"),
                                ("ending", "cleanup")]:

            self.game.advance()
            self.assertEqual(self.game.phase, phase)
            self.assertEqual(self.game.subphase, subphase)

        self.game.advance()

        self.assertIs(self.game.turn, self.p2)

        self.assertEqual(self.game.phase, "beginning")
        self.assertEqual(self.game.subphase, "untap")

    def test_die(self):
        self.p1.die()
        self.assertHeard(e.events.player.died, request=True)

    def test_life_changed(self):
        self.p1.life += 2
        self.assertHeard(e.events.player.life.gained, request=True)

        self.p1.life -= 2
        self.assertHeard(e.events.player.life.lost, request=True)

    def test_card_drawn(self):
        self.p1.library = [1]
        self.p1.draw()
        self.assertHeard(e.events.player.draw, request=True)

        def side_effect(*args, **kwargs):
            if e.events.player.draw in kwargs.viewvalues():
                self.fail("Unexpected card draw")
            return mock.DEFAULT

        self.events.trigger.side_effect = side_effect

        self.p1.draw()
        self.assertHeard(e.events.player.died)

    def test_cast_permanent(self):
        card = mock.Mock()
        card.is_permanent = True

        self.p1.cast(card)

        calls = [[pool(request=e.events.card.cast)],
                 [pool(request=e.events.card.field.entered)],
                 [pool(event=e.events.card.field.entered)],
                 [pool(event=e.events.card.cast)]]
        self.assertEqual(self.events.trigger.call_args_list[-4:], calls)

    def test_cast_nonpermanent(self):
        card = mock.Mock()
        card.is_permanent = False

        self.p1.cast(card)

        calls = [[pool(request=e.events.card.cast)],
                 [pool(request=e.events.card.graveyard.entered)],
                 [pool(event=e.events.card.graveyard.entered)],
                 [pool(event=e.events.card.cast)]]
        self.assertEqual(self.events.trigger.call_args_list[-4:], calls)

    def test_put_into_play(self):
        card = mock.Mock()
        self.p1.put_into_play(card)
        self.assertHeard(e.events.card.field.entered, request=True)

    def test_move_to_graveyard(self):
        card = mock.Mock()
        self.p1.move_to_graveyard(card)
        self.assertHeard(e.events.card.graveyard.entered, request=True)

    def test_remove_from_game(self):
        self.p1.remove_from_game(object())
        self.assertHeard(e.events.card.removed_from_game, request=True)

    def test_mana_changed(self):
        self.p1.mana_pool.red += 0
        self.assertNotHeard(e.events.player.mana.red.added, request=True)

        self.p1.mana_pool.red += 1
        self.assertHeard(e.events.player.mana.red.added, request=True)

        self.p1.mana_pool.red -= 1
        self.assertHeard(e.events.player.mana.red.removed, request=True)
