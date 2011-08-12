import unittest

import mock

from cardboard import (core as k, card as c, exceptions as exc,
                       models as m, zones as z)
from cardboard.events import events
from cardboard.tests.util import EventHandlerTestCase
from cardboard import core as o, zones as z


def mock_zone(name, contents):
    zone = mock.Mock(spec=z.Zone)
    zone.name = name
    zone.__contains__ = mock.Mock()
    zone.__contains__.side_effect = lambda i : i in contents
    zone.add.side_effect = lambda i : contents.append(i)
    return zone


def mock_player(exile=(), hand=(), graveyard=(), library=()):
    player = mock.Mock(spec=k.Player(()))
    player.library = mock_zone("library", list(library))
    player.hand = mock_zone("hand" , list(hand))
    player.graveyard = mock_zone("graveyard", list(graveyard))
    player.exile = mock_zone("exile", list(exile))
    return player


class TestCardBehavior(unittest.TestCase):
    def setUp(self):
        self.player = mock_player()
        self.player.game = self.game = mock.Mock(spec=k.Game)
        self.game.battlefield = mock_zone("battlefield", [])
        self.game.events = self.events = mock.Mock()

        self.db_card = mock.Mock()
        self.db_card.name = "Test Card"
        self.card = c.Card(self.db_card, controller=self.player)
        self.player.library.add(self.card)

    def test_repr_str(self):
        self.db_card.name = "Testing 123"
        card = c.Card(self.db_card, controller=mock.Mock())
        self.assertEqual(repr(card), "<Card: Testing 123>")
        self.assertEqual(str(card), "Testing 123")

    def test_init(self):
        self.assertIs(self.card.owner, self.player)
        self.assertIs(self.card.controller, self.player)

    def test_load(self):
        session = mock.Mock()
        d = c.Card.load("Foo", self.player, session=session)
        session.query(m.Card).filter_by.assert_called_once_with(name="Foo")
        self.assertIs(d.controller, self.player)

        with mock.patch("cardboard.card.Session") as session:
            session.return_value = session
            d = c.Card.load("Foo", self.player)
            session.query(m.Card).filter_by.assert_called_once_with(name="Foo")

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
        self.db_card.type = "Creature"

        creature = c.Card(self.db_card, controller=self.player)

        creature.zone = self.game.battlefield
        self.assertIn(creature, self.player.game.battlefield)
        self.assertEqual(creature.zone, self.player.game.battlefield)
        self.assertNotIn(creature, self.player.library)

    def test_zone_nonvalid(self):
        with self.assertRaises(ValueError):
            self.card.zone = "something"

    def test_taps_when_goes_to_battlefield(self):
        self.assertIsNone(self.card.tapped)
        self.card.zone = self.game.battlefield
        self.assertIsNotNone(self.card.tapped)
        self.assertFalse(self.card.tapped)

    def test_tap_not_in_play(self):
        with self.assertRaises(exc.RuntimeError):
            self.card.tapped = True


class TestCardEvents(EventHandlerTestCase):
    def setUp(self):
        super(TestCardEvents, self).setUp()

        self.player = mock_player()
        self.player.game = self.game = mock.Mock(spec=k.Game)
        self.game.events = self.events

        self.game.battlefield = mock_zone("battlefield", [])

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

            zone.__set__.assert_called_with(creature, self.game.battlefield)

        self.assertLastEventsWere(events["card"]["cast"])

    def test_cast_nonpermanent(self):
        # TODO: Test all types
        with mock.patch.object(c.Card, "zone") as zone:
            zone.__set__ = mock.Mock()

            instant = c.Card(self.instant_db_card, controller=self.player)
            instant.cast()

            zone.__set__.assert_called_with(instant, self.player.graveyard)

        self.assertLastEventsWere(events["card"]["cast"])

    """
    def test_cast_countered(self):
        self.creature.cast()
        self.assertLastEventsWere(events["card"]["countered"],
                                  events["card"]["zones"]["library"]["left"],
                                  events["card"]["zones"]["graveyard"]["entered"])
    """

    def test_zone(self):
        self.creature.zone = self.game.battlefield
        self.assertLastEventsWere(events["card"]["zones"]["library"]["left"],
                                  events["card"]["zones"]["battlefield"]["entered"],
                                  events["card"]["untapped"])

        self.creature.zone = self.player.graveyard
        self.assertLastEventsWere(events["card"]["zones"]["battlefield"]["left"],
                                  events["card"]["zones"]["graveyard"]["entered"])

        self.creature.zone = self.player.exile
        self.assertLastEventsWere(events["card"]["zones"]["graveyard"]["left"],
                                  events["card"]["zones"]["exile"]["entered"])

        self.creature.zone = self.player.hand
        self.assertLastEventsWere(events["card"]["zones"]["exile"]["left"],
                                  events["card"]["zones"]["hand"]["entered"])

        self.creature.zone = self.player.library
        self.assertLastEventsWere(events["card"]["zones"]["hand"]["left"],
                                  events["card"]["zones"]["library"]["entered"])

    def test_zone_same(self):
        self.creature.zone = self.player.library
        self.assertLastEventsWereNot(events["card"]["zones"]["library"]["entered"])

    def test_tap(self):
        self.creature.zone = self.game.battlefield

        self.creature.tapped = True
        self.assertTrue(self.creature.tapped)

        self.assertLastEventsWere(events["card"]["tapped"])
