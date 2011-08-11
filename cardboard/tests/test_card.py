import unittest

import mock

from cardboard import card as c, exceptions as exc
from cardboard.events import events
from cardboard.tests.util import EventHandlerTestCase, request, event


class TestCardBehavior(unittest.TestCase):
    def setUp(self):
        self.player = mock.Mock()
        self.db_card = mock.Mock()
        self.db_card.name = "Test Card"
        self.card = c.Card(self.db_card, controller=self.player)

    def test_repr_str(self):
        self.db_card.name = "Testing 123"
        card = c.Card(self.db_card, controller=mock.Mock())
        self.assertEqual(repr(card), "<Card: Testing 123>")
        self.assertEqual(str(card), "Testing 123")

    def test_init(self):
        self.assertIs(self.card.owner, self.player)
        self.assertIs(self.card.controller, self.player)

    def test_is_permanent(self):
        controller = mock.Mock()

        for type in ["Artifact", "Creature", "Enchantment", "Enchant Creature",
                     "Land", "Planeswalker"]:
            self.db_card.type = type
            card = c.Card(self.db_card, controller=controller)
            self.assertTrue(card.is_permanent)

        for type in ["Instant", "Sorcery"]:
            self.db_card.type = type
            card = c.Card(self.db_card, controller=controller)
            self.assertFalse(card.is_permanent)

    def test_controller(self):
        # create a library, check that instantiating a player with that library
        # makes all the cards have that controller
        pass

    def test_location(self):
        # TODO: Test all other locations
        self.player.game.battlefield = set()
        self.db_card.type = "Creature"

        creature = c.Card(self.db_card, controller=self.player)
        self.player.library = [creature]

        creature.location = "battlefield"
        self.assertIn(creature, self.player.game.battlefield)
        self.assertEqual(creature.location, "battlefield")
        self.assertNotIn(creature, self.player.library)

    def test_location_nonvalid(self):
        with self.assertRaises(ValueError):
            self.card.location = "something"

        # FIXME

        # def invalid_location(pool, *args, **kwargs):
        #     if kwargs.get("request") is events.card.battlefield.entered:
        #         pool["to"] = object()
        #     return mock.DEFAULT

        # self.player.events.trigger.side_effect = invalid_location

        # with self.assertRaises(TypeError):
        #     self.card.location = "battlefield"

    def test_taps_when_goes_to_battlefield(self):
        self.assertIsNone(self.card.tapped)
        self.card.location = "battlefield"
        self.assertIsNotNone(self.card.tapped)
        self.assertFalse(self.card.tapped)

    def test_tap_not_in_play(self):
        with self.assertRaises(exc.RuntimeError):
            self.card.tapped = True


class TestCardEvents(EventHandlerTestCase):
    def setUp(self):
        super(TestCardEvents, self).setUp()

        self.player = mock.Mock()
        self.game = self.player.game
        self.game.events = self.events

        self.creature_db_card = mock.Mock()
        self.creature_db_card.name = "Test Creature"
        self.creature_db_card.type = "Creature"

        self.instant_db_card = mock.Mock()
        self.instant_db_card.name = "Test Instant"
        self.instant_db_card.type = "Instant"

        self.creature = c.Card(self.creature_db_card, controller=self.player)
        self.instant = c.Card(self.instant_db_card, controller=self.player)

    def test_cast_permanent(self):
        # TODO: Test all types
        with mock.patch.object(c.Card, "location") as location:
            location.__set__ = mock.Mock()

            creature = c.Card(self.creature_db_card, controller=self.player)
            creature.cast()

            location.__set__.assert_called_with(creature, "battlefield")

        self.assertLastRequestedEventWas(events.card.cast)

    def test_cast_nonpermanent(self):
        # TODO: Test all types
        with mock.patch.object(c.Card, "location") as location:
            location.__set__ = mock.Mock()

            instant = c.Card(self.instant_db_card, controller=self.player)
            instant.cast()

            location.__set__.assert_called_with(instant, "graveyard")

        self.assertLastRequestedEventWas(events.card.cast)

    def test_cast_countered(self):
        def counter(pool, *args, **kwargs):
            if kwargs.get("request") is events.card.cast:
                pool["countered"] = True
            return mock.DEFAULT

        self.events.trigger.side_effect = counter

        self.creature.cast()

        self.assertLastEventsWere(request(events.card.cast),
                                  event(events.card.countered),
                                  request(events.card.library.left),
                                  request(events.card.graveyard.entered),
                                  event(events.card.library.left),
                                  event(events.card.graveyard.entered))

    def test_location(self):
        self.creature.location = "battlefield"
        self.assertLastEventsWere(request(events.card.library.left),
                                  request(events.card.battlefield.entered),
                                  event(events.card.library.left),
                                  event(events.card.battlefield.entered),
                                  request(events.card.untapped),
                                  event(events.card.untapped))

        self.creature.location = "graveyard"
        self.assertLastEventsWere(request(events.card.battlefield.left),
                                  request(events.card.graveyard.entered),
                                  event(events.card.battlefield.left),
                                  event(events.card.graveyard.entered))

        self.creature.location = "exile"
        self.assertLastEventsWere(request(events.card.graveyard.left),
                                  request(events.card.exile.entered),
                                  event(events.card.graveyard.left),
                                  event(events.card.exile.entered))

        self.creature.location = "hand"
        self.assertLastEventsWere(request(events.card.exile.left),
                                  request(events.card.hand.entered),
                                  event(events.card.exile.left),
                                  event(events.card.hand.entered))

        self.creature.location = "library"
        self.assertLastEventsWere(request(events.card.hand.left),
                                  request(events.card.library.entered),
                                  event(events.card.hand.left),
                                  event(events.card.library.entered))

    def test_location_same(self):
        self.creature.location = "library"
        self.assertLastEventsWereNot(event(events.card.library.entered))

    def test_tap(self):
        self.game.start()
        self.creature.location = "battlefield"

        self.creature.tapped = True
        self.assertTrue(self.creature.tapped)
        self.assertLastRequestedEventWas(events.card.tapped)
