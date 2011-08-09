import unittest

import mock

from cardboard import exceptions as exc
from cardboard.events import events
from cardboard.tests.util import EventHandlerTestCase, pool
import cardboard.models as m


def spawn_card(type, game, player):
    card = m.Card(name="Test {}".format(type), type=type)

    player.library.append(card)

    card.controller = player
    card.game = game
    card.library = player.library
    card._location = "library"

    return card


class TestCardBehavior(unittest.TestCase):
    def setUp(self):
        self.game = mock.Mock()
        self.player = mock.Mock()
        self.player.library = []
        self.player.game = self.game

        self.creature = spawn_card("Creature", self.game, self.player)
        self.instant = spawn_card("Instant", self.game, self.player)

    def test_repr_str(self):
        self.assertEqual(repr(self.creature),
                         "<Card: Test Creature (Creature)>")
        self.assertEqual(str(self.creature), "Test Creature")

        self.assertEqual(repr(self.instant), "<Card: Test Instant (Instant)>")
        self.assertEqual(str(self.instant), "Test Instant")

    def test_is_permanent(self):
        for type in ["Artifact", "Creature", "Enchantment", "Enchant Creature",
                     "Land", "Planeswalker"]:
            card = m.Card(name="Test", type=type)
            self.assertTrue(card.is_permanent)

        for type in ["Instant", "Sorcery"]:
            card = m.Card(name="Test", type=type)
            self.assertFalse(card.is_permanent)

    def test_cast(self):
        self.creature.move_to = mock.Mock()
        self.instant.move_to = mock.Mock()

        self.creature.cast()
        self.creature.move_to.assert_called_once_with("field")

        self.assertIsNotNone(self.creature.tapped)
        self.assertFalse(self.creature.tapped)

        self.instant.cast()
        self.instant.move_to.assert_called_once_with("graveyard")

    def test_controller(self):
        # create a library, check that instantiating a player with that library
        # makes all the cards have that controller
        pass

    def test_move_to(self):
        self.game.field = set()
        self.assertIn(self.creature, self.player.library)

        self.creature.move_to("field")
        self.assertIn(self.creature, self.game.field)
        self.assertIs(self.creature.location, self.game.field)
        self.assertNotIn(self.creature, self.player.library)

    def test_move_to_nonvalid(self):
        self.assertRaises(ValueError, self.creature.move_to, "something")


class TestCardEvents(EventHandlerTestCase):
    def setUp(self):
        super(TestCardEvents, self).setUp()

        self.game = mock.Mock()
        self.game.events = self.events
        self.player = mock.Mock()

        self.creature = spawn_card("Creature", self.game, self.player)
        self.instant = spawn_card("Instant", self.game, self.player)

    def test_cast_permanent(self):
        with mock.patch.object(self.creature, "move_to"):
            self.creature.cast()
        self.assertLastRequestedEventWas(events.card.cast)

    def test_cast_nonpermanent(self):
        with mock.patch.object(self.instant, "move_to"):
            self.instant.cast()
        self.assertLastRequestedEventWas(events.card.cast)

    def test_move_to(self):
        self.creature.move_to("field")
        self.assertLastEventsWere(pool(request=events.card.library.left),
                                  pool(request=events.card.field.entered),
                                  pool(event=events.card.library.left),
                                  pool(event=events.card.field.entered))

        self.creature.move_to("graveyard")
        self.assertLastEventsWere(pool(request=events.card.field.left),
                                  pool(request=events.card.graveyard.entered),
                                  pool(event=events.card.field.left),
                                  pool(event=events.card.graveyard.entered))

        self.creature.move_to("exile")
        self.assertLastEventsWere(pool(request=events.card.graveyard.left),
                                  pool(request=events.card.exile.entered),
                                  pool(event=events.card.graveyard.left),
                                  pool(event=events.card.exile.entered))

        self.creature.move_to("hand")
        self.assertLastEventsWere(pool(request=events.card.exile.left),
                                  pool(request=events.card.hand.entered),
                                  pool(event=events.card.exile.left),
                                  pool(event=events.card.hand.entered))

        self.creature.move_to("library")
        self.assertLastEventsWere(pool(request=events.card.hand.left),
                                  pool(request=events.card.library.entered),
                                  pool(event=events.card.hand.left),
                                  pool(event=events.card.library.entered))

    def test_move_to_nowhere(self):
        self.creature.move_to("library")
        self.assertLastEventsWereNot(pool(event=events.card.library.entered))
