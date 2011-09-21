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
        self.creature_db_card.name = u"Test Creature"
        self.creature_db_card.type = types.CREATURE

        self.instant_db_card = mock.Mock()
        self.instant_db_card.name = u"Test Instant"
        self.instant_db_card.type = types.INSTANT

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

        self.assertEqual(unicode(self.creature), u"Test Creature")
        self.assertEqual(unicode(self.instant), u"Test Instant")

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
        self.assertEqual(self.creature.colors, {"U"})

        self.creature.mana_cost = "B"
        self.assertEqual(self.creature.colors, {"B"})

        self.creature.mana_cost = "2R"
        self.assertEqual(self.creature.colors, {"R"})

        self.creature.mana_cost = "WWW"
        self.assertEqual(self.creature.colors, {"W"})

        self.creature.mana_cost = "G"
        self.assertEqual(self.creature.colors, {"G"})

        self.creature.mana_cost = "GWR"
        self.assertEqual(self.creature.colors, {"G", "W", "R"})

        self.creature.mana_cost = "GBB"
        self.assertEqual(self.creature.colors, {"G", "B"})

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

    def test_cast(self):
        """
        Casting a spell should follow a specific series of steps.

        The steps are outlined in :ref:`cast-steps`.

        """

        # TODO: Test all types

        self.creature.cast()
        self.instant.cast()

        # instant spell on top
        creature_spell, instant_spell = self.game.stack

        self.assertIs(creature_spell.card, self.creature)
        self.assertIs(instant_spell.card, self.instant)

        # controller is set to owner
        self.assertIs(creature_spell.card.controller, self.p4)
        self.assertIs(instant_spell.card.controller, self.p4)

        self.assertLastEventsWere([events["card"]["cast"]])


class TestStatus(GameTestCase):
    def setUp(self):
        super(TestStatus, self).setUp()

        self.creature_db_card = mock.Mock()
        self.creature_db_card.name = "Test Creature"
        self.creature_db_card.type = types.CREATURE

        self.creature = c.Card(self.creature_db_card)

        self.library[-1] = self.creature
        self.p3 = self.game.add_player(library=self.library)

        self.evs = [("tapped", "untapped"),
                    ("flipped", "unflipped"),
                    ("turned_face_down", "turned_face_up"),
                    ("phased_out", "phased_in")]

        self.fns = [(self.creature.tap, self.creature.untap),
                    (self.creature.flip, self.creature.unflip),
                    (self.creature.turn_face_down, self.creature.turn_face_up),
                    (self.creature.phase_out, self.creature.phase_in)]

        self.game.start()
        self.resetEvents()

    def test_not_on_battlefield(self):
        for default, nondefault in self.fns:
            with self.assertRaises(exceptions.RequirementNotMet):
                default()

            with self.assertRaises(exceptions.RequirementNotMet):
                nondefault()

            # didn't fire any events
            self.assertFalse(self.events.trigger.called)

    def test_defaults(self):
        self.game.battlefield.move(self.creature)

        self.assertFalse(self.creature.is_tapped)
        self.assertFalse(self.creature.is_flipped)
        self.assertTrue(self.creature.is_face_up)
        self.assertTrue(self.creature.is_phased_in)

    def test_toggle(self):
        self.game.battlefield.move(self.creature)

        for (nondefault, _), (event, _) in zip(self.fns, self.evs):
            nondefault()
            self.assertLastEventsWere([events["card"]["status"][event]])

        self.assertTrue(self.creature.is_tapped)
        self.assertTrue(self.creature.is_flipped)
        self.assertFalse(self.creature.is_face_up)
        self.assertFalse(self.creature.is_phased_in)

        self.resetEvents()

        # card already has status raises RNM
        for nondefault, _ in self.fns:
            with self.assertRaises(exceptions.RequirementNotMet):
                nondefault()

        # didn't fire any events
        self.assertFalse(self.events.trigger.called)

        for (_, default), (_, event) in zip(self.fns, self.evs):
            default()
            self.assertLastEventsWere([events["card"]["status"][event]])

        self.assertFalse(self.creature.is_tapped)
        self.assertFalse(self.creature.is_flipped)
        self.assertTrue(self.creature.is_face_up)
        self.assertTrue(self.creature.is_phased_in)

        self.resetEvents()

        # card already has status raises RNM
        for _, default in self.fns:
            with self.assertRaises(exceptions.RequirementNotMet):
                default()

        # didn't fire any events
        self.assertFalse(self.events.trigger.called)


class TestSpell(GameTestCase):
    def setUp(self):
        super(TestSpell, self).setUp()

        self.db_card = mock.Mock()
        self.db_card.name = u"Test Creature"
        self.db_card.type = types.CREATURE

        self.card = c.Card(self.db_card)
        self.spell = c.Spell(self.card)

    def test_repr_str(self):
        self.assertEqual(repr(self.spell), "<Spell: Test Creature>")
        self.assertEqual(str(self.spell), "Test Creature")
        self.assertEqual(unicode(self.spell), u"Test Creature")

    def test_init(self):
        self.assertIs(self.spell.card, self.card)
