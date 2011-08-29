import unittest

import mock

from cardboard import core as k, card as c, zone as z
from cardboard import exceptions, types
from cardboard.db import models as m
from cardboard.events import events
from cardboard.tests.util import GameTestCase


class TestCard(GameTestCase):
    def setUp(self):
        super(TestCard, self).setUp()

        self.creature_db_card = mock.Mock()
        self.creature_db_card.name = "Test Creature"
        self.creature_db_card.type = types.creature

        self.instant_db_card = mock.Mock()
        self.instant_db_card.name = "Test Instant"
        self.instant_db_card.type = types.instant

        self.creature = c.Card(self.creature_db_card)
        self.instant = c.Card(self.instant_db_card)

        self.game.add_existing_player(self.p3)

        self.library[-2:] = [self.creature, self.instant]
        self.p4 = self.game.add_player(library=self.library)

        self.game.start()

    def test_repr_str(self):
        self.assertEqual(repr(self.creature), "<Card: Test Creature>")
        self.assertEqual(repr(self.instant), "<Card: Test Instant>")

        self.assertEqual(str(self.creature), "Test Creature")
        self.assertEqual(str(self.instant), "Test Instant")

    def test_init(self):
        card = c.Card(self.creature_db_card)
        self.assertIsNone(card.game)
        self.assertIsNone(card.controller)
        self.assertIsNone(card.owner)
        self.assertIsNone(card.zone)

    def test_sort(self):
        self.creature_db_card.name = "Foo"
        c1 = c.Card(self.creature_db_card)

        self.creature_db_card.name = "Bar"
        c2 = c.Card(self.creature_db_card)

        self.creature_db_card.name = "Baz"
        c3 = c.Card(self.creature_db_card)

        self.assertEqual(sorted([c1, c2, c3]), [c2, c3, c1])

        self.assertIs(NotImplemented, c1.__lt__(object()))

    def test_load(self):
        session = mock.Mock()
        d = c.Card.load("Foo", session=session)
        session.query(m.Card).filter_by.assert_called_once_with(name="Foo")

        with mock.patch("cardboard.card.Session") as session:
            session.return_value = session
            d = c.Card.load("Foo")
            session.query(m.Card).filter_by.assert_called_once_with(name="Foo")

    def test_colors(self):
        self.creature.mana_cost = "UU"
        self.assertEqual(self.creature.colors, {"blue"})

        self.creature.mana_cost = "B"
        self.assertEqual(self.creature.colors, {"black"})

        self.creature.mana_cost = "2R"
        self.assertEqual(self.creature.colors, {"red"})

        self.creature.mana_cost = "WWW"
        self.assertEqual(self.creature.colors, {"white"})

        self.creature.mana_cost = "G"
        self.assertEqual(self.creature.colors, {"green"})

        self.creature.mana_cost = "GWR"
        self.assertEqual(self.creature.colors, {"green", "white", "red"})

        self.creature.mana_cost = "GBB"
        self.assertEqual(self.creature.colors, {"green", "black"})

        self.creature.mana_cost = "3"
        self.assertEqual(self.creature.colors, set())

        self.creature.mana_cost = "10"
        self.assertEqual(self.creature.colors, set())

    def test_is_permanent(self):
        """
        `is_permanent` delegates to Card.type.

        """

        mt = mock.Mock()
        class MockType(mock.Mock):
            @property
            def is_permanent(self):
                return mt()

        self.creature_db_card.type = MockType()
        card = c.Card(self.creature_db_card)
        card.is_permanent
        mt.assert_called_once_with()

    def test_cast_permanent(self):
        self.game.battlefield.move = mock.Mock()

        # TODO: Test all types
        self.creature.cast()
        self.game.battlefield.move.assert_called_with(self.creature)
        self.assertLastEventsWere([events["card"]["cast"]])

    def test_cast_nonpermanent(self):
        self.p4.graveyard.move = mock.Mock()

        # TODO: Test all types
        self.instant.cast()
        self.p4.graveyard.move.assert_called_with(self.instant)
        self.assertLastEventsWere([events["card"]["cast"]])

    def test_tap(self):
        self.creature.zone = self.game.battlefield

        self.creature.tap()
        self.assertTrue(self.creature.tapped)

        self.assertLastEventsWere([events["card"]["tapped"]])

    def test_untap(self):
        self.creature.zone = self.game.battlefield

        self.creature.untap()
        self.assertFalse(self.creature.tapped)

        self.assertLastEventsWere([events["card"]["untapped"]])

    def test_tap_untap_already(self):
        self.creature.zone = self.game.battlefield

        self.creature.tap()
        self.assertRaises(exceptions.RuntimeError, self.creature.tap)

        # check that it didn't trigger twice
        self.assertLastEventsWereNot([events["card"]["tapped"],
                                      events["card"]["tapped"]])

        self.creature.untap()
        self.assertRaises(exceptions.RuntimeError, self.creature.untap)

        # check that it didn't trigger twice
        self.assertLastEventsWereNot([events["card"]["untapped"],
                                      events["card"]["untapped"]])
    def test_tap_not_in_play(self):
        self.assertRaises(exceptions.RuntimeError, self.creature.tap)
        self.assertRaises(exceptions.RuntimeError, self.creature.untap)
