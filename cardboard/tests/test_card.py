import unittest

import mock

from cardboard import card as c
from cardboard import exceptions, types
from cardboard.db import models as m
from cardboard.events import events
from cardboard.tests.util import GameTestCase


def mock_card(type, abilities=(), mana_cost=""):
    name = "Test {}".format(type)
    card = mock.Mock()
    card.name, card.types, card.abilities = name, {type}, list(abilities)
    card.mana_cost, card.subtypes, card.supertypes = mana_cost, set(), set()
    return card


class TestCard(GameTestCase):

    creature_db_card = mock_card(types.creature)
    instant_db_card = mock_card(types.instant, abilities=["foo", "bar"])
    land_db_card = mock_card(types.land)

    creature = c.Card(creature_db_card)
    instant = c.Card(instant_db_card)
    land = c.Card(land_db_card)

    def setUp(self):
        super(TestCard, self).setUp()
        self.library[-3:] = [self.creature, self.instant, self.land]
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
        abilities = [mock.Mock(), mock.Mock()]
        cards = {self.creature_db_card.name : lambda card, abils : abilities}
        card = c.Card(self.creature_db_card, _cards=cards)

        self.assertEqual(card.name, self.creature_db_card.name)
        self.assertEqual(card.loyalty, self.creature_db_card.loyalty)
        self.assertEqual(card.mana_cost, self.creature_db_card.mana_cost)
        self.assertEqual(card.types, self.creature_db_card.types)
        self.assertEqual(card.subtypes, self.creature_db_card.subtypes)
        self.assertEqual(card.supertypes, self.creature_db_card.supertypes)
        self.assertEqual(card.abilities, abilities)

        self.assertIsNone(card.game)
        self.assertIsNone(card.controller)
        self.assertIsNone(card.owner)
        self.assertIsNone(card.zone)

    def test_not_implemented_card(self):
        card = c.Card(self.instant_db_card, _cards={})
        self.assertEqual(card.abilities, [c.Ability.NotImplemented] * 2)

    def test_sort(self):
        c1 = c.Card(self.creature_db_card)
        c1.name = "Foo"

        c2 = c.Card(self.creature_db_card)
        c2.name = "Bar"

        c3 = c.Card(self.creature_db_card)
        c3.name = "Baz"

        self.assertEqual(sorted([c1, c2, c3]), [c2, c3, c1])

        self.assertIs(NotImplemented, c1.__lt__(object()))

    def test_load(self):
        session = mock.Mock()
        card = self.creature_db_card
        session.query(m.Card).filter_by.return_value.one.return_value = card

        d = c.Card.load("Foo", session=session)
        session.query(m.Card).filter_by.assert_called_once_with(name="Foo")

        with mock.patch("cardboard.card.Session") as Session:
            Session.return_value = session
            d = c.Card.load("Bar")
            session.query(m.Card).filter_by.assert_called_with(name="Bar")

    def test_colors(self):
        costs = [
            ("UU", {"U"}), ("B", {"B"}), ("2R", {"R"}), ("WWW", {"W"}),
            ("G", {"G"}), ("GWR", {"G", "W", "R"}), ("GBB", {"G", "B"}),
            ("3", set()), ("10", set()), ("0", set()), (None, set()),
        ]

        for cost, colors in costs:
            self.creature.mana_cost = cost
            self.assertEqual(self.creature.colors, colors)

    def test_play_land(self):
        self.assertEqual(self.land.owner.lands_this_turn, 0)
        self.assertEqual(self.land.owner.lands_per_turn, 1)

        self.land.play()

        self.assertEqual(self.land.owner.lands_this_turn, 1)
        self.assertIn(self.land, self.game.battlefield)

        second_land = c.Card(self.land_db_card)
        second_land.game = self.land.game
        second_land.owner = self.land.owner

        with self.assertRaises(exceptions.InvalidAction):
            second_land.play()

    def test_play_spell(self):
        """
        Playing (=casting) a spell should follow a specific series of steps.

        The steps are outlined in :ref:`cast-steps`.

        """

        # TODO: Test all types

        self.creature.play()
        self.instant.play()

        # instant spell on top
        creature_spell, instant_spell = self.game.stack

        self.assertIs(creature_spell.card, self.creature)
        self.assertIs(instant_spell.card, self.instant)

        # controller is set to owner
        self.assertIs(creature_spell.card.controller, self.p4)
        self.assertIs(instant_spell.card.controller, self.p4)

        self.assertLastEventsWere([events["card"]["cast"]])


class TestMTGObjectFunctions(unittest.TestCase):
    def test_characteristics(self):
        o = mock.Mock()
        self.assertEqual(c.characteristics(o), {
            "name" : o.name,
            "mana_cost" : o.mana_cost,
            "colors" : o.colors,
            "types" : o.types,
            "subtypes" : o.subtypes,
            "supertypes" : o.supertypes,
            "abilities" : o.abilities,
            "power" : o.power,
            "toughness" : o.toughness,
            "loyalty" : o.loyalty,
            "expansion" : o.expansion,
            "rules_text" : o.rules_text
        })

    def test_converted_mana_cost(self):
        o = mock.Mock()
        o.game.stack = set()

        costs = [
            ("UU", 2), ("B", 1), ("2R", 3), ("WWW", 3), ("G", 1), ("GWR", 3),
            ("GBB", 3), ("3", 3), ("10", 10), ("0", 0), (None, 0), ("2XBR", 4),
        ]

        for cost, cmc in costs:
            o.mana_cost = cost
            self.assertEqual(c.converted_mana_cost(o), cmc)

    def test_converted_mana_cost_stack(self):
        """
        On the stack, converted mana cost uses whatever was chosen for X.

        """

        o = mock.Mock()
        o.game.stack = {o}
        o.X = 4

        costs = [("2XBR", 8)]

        for cost, cmc in costs:
            o.mana_cost = cost
            self.assertEqual(c.converted_mana_cost(o), cmc)


class TestStatus(GameTestCase):
    def setUp(self):
        super(TestStatus, self).setUp()

        self.creature_db_card = mock_card(types.creature)
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


class TestAbility(GameTestCase):
    def test_repr_str(self):
        a = c.Ability(description="Does foo.", action=None, type="static")
        self.assertEqual(repr(a), "<Static Ability: Does foo.>")
        self.assertEqual(str(a), "Does foo.")

        a = c.Ability(description="f" * 100, action=None, type="spell")
        self.assertEqual(repr(a), "<Spell Ability: {} ... >".format("f" * 40))
        self.assertEqual(str(a), "f" * 100)

    def test_init(self):
        types = "spell", "activated", "triggered", "static"
        noop = lambda card : None

        a = [c.Ability(description="foo", action=noop, type=t) for t in types]

        self.assertEqual(a[0].action, noop)
        self.assertEqual(a[0].description, "foo")

        self.assertEqual(a[0].type, "spell")
        self.assertEqual(a[1].type, "activated")
        self.assertEqual(a[2].type, "triggered")
        self.assertEqual(a[3].type, "static")

    def test_call(self):
        m = mock.Mock()
        a = c.Ability(description="", action=m, type="spell")
        a()
        m.assert_called_once_with()

    def test_abilities(self):
        m = mock.Mock()

        a = c.Ability.spell(description="Foo")(m)
        self.assertEqual(a.action, m)
        self.assertEqual(a.description, "Foo")
        self.assertEqual(a.type, "spell")

        a = c.Ability.activated(cost="2BB", description="Foo")(m)
        self.assertEqual(a.action, m)
        self.assertEqual(a.description, "Foo")
        self.assertEqual(a.type, "activated")
        self.assertEqual(a.cost, "2BB")

        a = c.Ability.triggered(event="Bar", condition=3, description="Foo")(m)
        self.assertEqual(a.action, m)
        self.assertEqual(a.description, "Foo")
        self.assertEqual(a.type, "triggered")
        self.assertEqual(a.trigger, {"event" : "Bar", "condition" : 3})

        a = c.Ability.static(description="Foo")(m)
        self.assertEqual(a.action, m)
        self.assertEqual(a.description, "Foo")
        self.assertEqual(a.type, "static")

    def test_not_implemented(self):
        n = c.Ability.NotImplemented
        self.assertEqual(repr(n), "<Ability Not Implemented>")
        with self.assertRaises(exceptions.NotImplemented):
            n()


class TestSpell(GameTestCase):
    def setUp(self):
        super(TestSpell, self).setUp()

        self.db_card = mock_card(types.creature)
        self.card = c.Card(self.db_card)
        self.spell = c.Spell(self.card)

    def test_repr_str(self):
        self.assertEqual(repr(self.spell), "<Spell: Test Creature>")
        self.assertEqual(str(self.spell), "Test Creature")
        self.assertEqual(unicode(self.spell), u"Test Creature")

    def test_init(self):
        self.assertIs(self.spell.card, self.card)


class TestToken(GameTestCase):
    def setUp(self):
        super(TestToken, self).setUp()

        self.db_card = mock_card(types.creature)
        self.card = c.Card(self.db_card)

    def test_from_card(self):
        t = c.Token.from_card(self.card)
        self.assertEqual(c.characteristics(t), c.characteristics(self.card))

    def test_missing_characteristics(self):
        """
        A token doesn't have any characteristics not defined by its creator.

        .. seealso::
            :ref:`token-characteristics`

        """

        t = c.Token(power=1, toughness=1, colors="G",
                    types={types.creature}, subtypes={"Saproling"})

        self.assertEqual(t.mana_cost, "")
        self.assertEqual(t.supertypes, set())
        self.assertEqual(t.abilities, [])
