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
    card.location = "library"

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

    def test_controller(self):
        # create a library, check that instantiating a player with that library
        # makes all the cards have that controller
        pass

    def test_location(self):
        self.game.field = set()
        self.assertIn(self.creature, self.player.library)

        self.creature.location = "field"
        self.assertIn(self.creature, self.game.field)
        self.assertEqual(self.creature.location, "field")
        self.assertNotIn(self.creature, self.player.library)

    def test_location_nonvalid(self):
        with self.assertRaises(ValueError):
            self.creature.location = "something"

    def test_move_to_field(self):
        self.game.field = set()
        self.creature.location = "field"

        self.assertIsNotNone(self.creature.tapped)
        self.assertFalse(self.creature.tapped)


class TestCardEvents(EventHandlerTestCase):
    def setUp(self):
        super(TestCardEvents, self).setUp()

        self.game = mock.Mock()
        self.game.events = self.events
        self.player = mock.Mock()

        self.creature = spawn_card("Creature", self.game, self.player)
        self.instant = spawn_card("Instant", self.game, self.player)

    def test_cast_permanent(self):
        with mock.patch.object(m.Card, "location") as location:
            location.__set__ = mock.Mock()

            creature = spawn_card("Creature", self.game, self.player)
            creature.cast()

            location.__set__.assert_called_with(creature, "field")

        self.assertLastRequestedEventWas(events.card.cast)

    def test_cast_nonpermanent(self):
        with mock.patch.object(m.Card, "location") as location:
            location.__set__ = mock.Mock()

            instant = spawn_card("Instant", self.game, self.player)
            instant.cast()

            location.__set__.assert_called_with(instant, "graveyard")

        self.assertLastRequestedEventWas(events.card.cast)

    def test_location(self):
        self.creature.location = "field"
        self.assertLastEventsWere(pool(request=events.card.library.left),
                                  pool(request=events.card.field.entered),
                                  pool(event=events.card.library.left),
                                  pool(event=events.card.field.entered),
                                  pool(request=events.card.untapped),
                                  pool(event=events.card.untapped))

        self.creature.location = "graveyard"
        self.assertLastEventsWere(pool(request=events.card.field.left),
                                  pool(request=events.card.graveyard.entered),
                                  pool(event=events.card.field.left),
                                  pool(event=events.card.graveyard.entered))

        self.creature.location = "exile"
        self.assertLastEventsWere(pool(request=events.card.graveyard.left),
                                  pool(request=events.card.exile.entered),
                                  pool(event=events.card.graveyard.left),
                                  pool(event=events.card.exile.entered))

        self.creature.location = "hand"
        self.assertLastEventsWere(pool(request=events.card.exile.left),
                                  pool(request=events.card.hand.entered),
                                  pool(event=events.card.exile.left),
                                  pool(event=events.card.hand.entered))

        self.creature.location = "library"
        self.assertLastEventsWere(pool(request=events.card.hand.left),
                                  pool(request=events.card.library.entered),
                                  pool(event=events.card.hand.left),
                                  pool(event=events.card.library.entered))

    def test_location_same(self):
        self.creature.location = "library"
        self.assertLastEventsWereNot(pool(event=events.card.library.entered))
