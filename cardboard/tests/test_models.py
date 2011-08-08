import unittest

import mock

from cardboard.events import events
from cardboard.tests.util import pool
import cardboard.models as m

class TestCardBehavior(unittest.TestCase):
    def setUp(self):
        self.game = mock.Mock()

        self.creature = m.Card(name="Test Creature", type="Creature")
        self.instant = m.Card(name="Test Instant", type="Instant")

        self.creature.game = self.game
        self.instant.game = self.game

    def test_is_permanent(self):
        for type in ["Artifact", "Creature", "Enchantment", "Enchant Creature",
                     "Land", "Planeswalker"]:
            card = m.Card(name="Test", type=type)
            self.assertTrue(card.is_permanent)

        for type in ["Instant", "Sorcery"]:
            card = m.Card(name="Test", type=type)
            self.assertFalse(card.is_permanent)

    def test_cast(self):
        self.creature.put_into_play = mock.Mock()
        self.creature.move_to_graveyard = mock.Mock()

        self.creature.cast()

        self.creature.put_into_play.assert_called_once_with()
        self.assertFalse(self.creature.move_to_graveyard.called)

        self.instant.put_into_play = mock.Mock()
        self.instant.move_to_graveyard = mock.Mock()

        self.instant.cast()

        self.instant.move_to_graveyard.assert_called_once_with()
        self.assertFalse(self.instant.put_into_play.called)

    def test_owner(self):
        # create a library, check that instantiating a player with that library
        # makes all the cards have that owner
        pass

    def test_put_into_play(self):
        self.game.field = set()
        self.creature.put_into_play()
        self.assertIn(self.creature, self.game.field)

class TestCardEvents(unittest.TestCase):
    def setUp(self):
        self.game = mock.Mock()
        self.events = self.game.events
        self.player = mock.Mock()

        self.creature = m.Card(name="Test Creature", type="Creature")
        self.instant = m.Card(name="Test Instant", type="Instant")

        self.creature.game = self.game
        self.instant.game = self.game
        self.creature.owner = self.player
        self.instant.owner = self.player

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
            self.fail("{} was triggered by {}.".format(event, handler))

    def test_cast_permanent(self):
        self.creature.cast()

        calls = [[pool(request=events.card.cast)],
                 [pool(request=events.card.field.entered)],
                 [pool(event=events.card.field.entered)],
                 [pool(event=events.card.cast)]]

        self.assertEqual(self.events.trigger.call_args_list[-4:], calls)

    def test_cast_nonpermanent(self):
        self.instant.cast()

        calls = [[pool(request=events.card.cast)],
                 [pool(request=events.card.graveyard.entered)],
                 [pool(event=events.card.graveyard.entered)],
                 [pool(event=events.card.cast)]]

        self.assertEqual(self.events.trigger.call_args_list[-4:], calls)

    def test_put_into_play(self):
        self.creature.put_into_play()
        self.assertHeard(events.card.field.entered, request=True)

    def test_move_to_graveyard(self):
        self.creature.move_to_graveyard()
        self.assertHeard(events.card.graveyard.entered, request=True)

    def test_remove_from_game(self):
        self.creature.remove_from_game()
        self.assertHeard(events.card.removed_from_game, request=True)
