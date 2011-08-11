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

    def test_zone(self):
        # TODO: Test all other zones
        self.player.game.battlefield = set()
        self.db_card.type = "Creature"

        creature = c.Card(self.db_card, controller=self.player)
        self.player.library = [creature]

        creature.zone = "battlefield"
        self.assertIn(creature, self.player.game.battlefield)
        self.assertEqual(creature.zone, "battlefield")
        self.assertNotIn(creature, self.player.library)

    def test_zone_nonvalid(self):
        with self.assertRaises(ValueError):
            self.card.zone = "something"

        # FIXME

        # def invalid_zone(pool, *args, **kwargs):
        #     if kwargs.get("request") is events.card.battlefield.entered:
        #         pool["to"] = object()
        #     return mock.DEFAULT

        # self.player.events.trigger.side_effect = invalid_zone

        # with self.assertRaises(TypeError):
        #     self.card.zone = "battlefield"

    def test_taps_when_goes_to_battlefield(self):
        self.assertIsNone(self.card.tapped)
        self.card.zone = "battlefield"
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
        with mock.patch.object(c.Card, "zone") as zone:
            zone.__set__ = mock.Mock()

            creature = c.Card(self.creature_db_card, controller=self.player)
            creature.cast()

            zone.__set__.assert_called_with(creature, "battlefield")

        self.assertLastRequestedEventWas(events.card.cast)

    def test_cast_nonpermanent(self):
        # TODO: Test all types
        with mock.patch.object(c.Card, "zone") as zone:
            zone.__set__ = mock.Mock()

            instant = c.Card(self.instant_db_card, controller=self.player)
            instant.cast()

            zone.__set__.assert_called_with(instant, "graveyard")

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
                                  request(events.card.zones.library.left),
                                  request(events.card.zones.graveyard.entered),
                                  event(events.card.zones.library.left),
                                  event(events.card.zones.graveyard.entered))

    def test_zone(self):
        self.creature.zone = "battlefield"
        self.assertLastEventsWere(request(events.card.zones.library.left),
                                  request(events.card.zones.battlefield.entered),
                                  event(events.card.zones.library.left),
                                  event(events.card.zones.battlefield.entered),
                                  request(events.card.untapped),
                                  event(events.card.untapped))

        self.creature.zone = "graveyard"
        self.assertLastEventsWere(request(events.card.zones.battlefield.left),
                                  request(events.card.zones.graveyard.entered),
                                  event(events.card.zones.battlefield.left),
                                  event(events.card.zones.graveyard.entered))

        self.creature.zone = "exile"
        self.assertLastEventsWere(request(events.card.zones.graveyard.left),
                                  request(events.card.zones.exile.entered),
                                  event(events.card.zones.graveyard.left),
                                  event(events.card.zones.exile.entered))

        self.creature.zone = "hand"
        self.assertLastEventsWere(request(events.card.zones.exile.left),
                                  request(events.card.zones.hand.entered),
                                  event(events.card.zones.exile.left),
                                  event(events.card.zones.hand.entered))

        self.creature.zone = "library"
        self.assertLastEventsWere(request(events.card.zones.hand.left),
                                  request(events.card.zones.library.entered),
                                  event(events.card.zones.hand.left),
                                  event(events.card.zones.library.entered))

    def test_zone_same(self):
        self.creature.zone = "library"
        self.assertLastEventsWereNot(event(events.card.zones.library.entered))

    def test_tap(self):
        self.game.start()
        self.creature.zone = "battlefield"

        self.creature.tapped = True
        self.assertTrue(self.creature.tapped)
        self.assertLastRequestedEventWas(events.card.tapped)
