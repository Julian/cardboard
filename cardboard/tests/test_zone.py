import collections
import random
import unittest

import mock

from cardboard import card as c, zone as z
from cardboard.events import events
from cardboard.tests.util import GameTestCase


class ZoneTest(GameTestCase):
    def setUp(self):
        super(ZoneTest, self).setUp()
        self.card = mock.Mock(spec=c.Card)
        self.noise = [mock.Mock(spec=c.Card) for _ in range(30)]
        self.zone_events = {"entered" : object(), "left" : object()}

        self.u = z.UnorderedZone(name="Emerald Hill",
                                 game=self.game,
                                 contents=self.noise,
                                 _events=self.zone_events)

        self.o = z.OrderedZone(name="Casino Night",
                               game=self.game,
                               contents=self.noise,
                               _events=self.zone_events)


class TestZones(ZoneTest):
    def test_name(self):
        self.assertEqual(self.u.name, "Emerald Hill")
        self.assertEqual(self.o.name, "Casino Night")

    def test_ordered(self):
        self.assertFalse(self.u.ordered)
        self.assertTrue(self.o.ordered)

    def test_repr(self):
        self.assertEqual(repr(self.u), "<Zone: Emerald Hill>")
        self.assertEqual(repr(self.o), "<Zone: Casino Night>")

    def test_contains(self):
        for i in self.noise:
            self.assertIn(i, self.u)
            self.assertIn(i, self.o)

        self.assertNotIn(object(), self.u)
        self.assertNotIn(object(), self.o)

    def test_iter(self):
        self.assertEqual(set(self.u), set(self.noise))
        self.assertEqual(list(self.o), self.noise)

    def test_len(self):
        self.assertEqual(len(self.u), len(self.noise))
        self.assertEqual(len(self.o), len(self.noise))

    def test_add(self):
        self.u.add(30)
        self.o.add(30)

        self.assertEqual(set(self.u), set(self.noise) | {30})
        self.assertEqual(list(self.o), self.noise + [30])

        self.assertLastEventsWere([self.zone_events["entered"]])

    def test_clear(self):
        self.u.clear()
        self.o.clear()
        self.assertFalse(self.u)
        self.assertFalse(self.o)

    def test_discard(self):
        e = self.noise[17]
        self.noise.remove(e)

        self.u.discard(e)
        self.u.discard(object())

        self.o.discard(e)
        self.o.discard(object())

        self.assertEqual(len(self.u), len(self.noise))
        self.assertEqual(len(self.o), len(self.noise))

        self.assertEqual(set(self.u), set(self.noise))
        self.assertEqual(list(self.o), self.noise)

    def test_events_default(self):
        u = z.UnorderedZone("Emerald Hill", self.noise)
        o = z.OrderedZone("Casino Night", self.noise)

        self.assertIs(u._events, events)
        self.assertIs(o._events, events)

    def test_move(self):
        self.o.add(self.card)
        self.card.zone = self.o

        self.u.move(self.card)
        self.assertIn(self.card, self.u)
        self.assertEqual(self.card.zone, self.u)

        self.o.move(self.card)
        self.assertIn(self.card, self.o)
        self.assertEqual(self.card.zone, self.o)

    def test_pop(self):
        e = self.u.pop()
        self.o.pop()

        self.assertEqual(set(self.u), set(self.noise) - {e})
        self.assertEqual(list(self.o), self.noise[:-1])

    def test_remove(self):
        e = self.noise[-7]
        self.noise.remove(e)

        self.u.remove(e)
        self.o.remove(e)

        self.assertEqual(set(self.u), set(self.noise))
        self.assertEqual(list(self.o), self.noise)

        self.assertRaises(ValueError, self.u.remove, object())
        self.assertRaises(ValueError, self.o.remove, object())


class TestOrderedZone(ZoneTest):
    def test_reversed(self):
        self.assertEqual(list(reversed(self.o)), list(reversed(self.noise)))

    def test_getitem(self):
        for i, e in enumerate(self.noise):
            self.assertEqual(self.o[i], e)

        self.assertEqual(self.o[2:7:2], self.noise[2:7:2])

    def test_set_del_item(self):
        self.assertRaises(AttributeError, getattr, self.o, "__setitem__")
        self.assertRaises(AttributeError, getattr, self.o, "__delitem__")

    def test_count(self):
        o = z.OrderedZone(game=None, name="Emerald Hill",
                          contents=[1, 1, 1, 2, 2, 3])

        for i, e in enumerate(range(3, 0, -1), 1):
            self.assertEqual(o.count(e), i)

    def test_extend(self):
        self.o.extend(range(4))
        self.assertEqual(self.o[-4:], range(4))
        self.assertEqual(len(self.o), len(self.noise) + 4)

    def test_index(self):
        e = self.noise[13]
        self.assertEqual(self.o.index(e), 13)

    def test_pop_index(self):
        self.o.pop(0)
        self.o.pop(13)

        self.noise.pop(0)
        self.noise.pop(13)

        self.assertEqual(list(self.o), self.noise)

    def test_reverse(self):
        self.o.reverse()
        self.assertEqual(list(self.o), list(reversed(self.noise)))

    def test_shuffle(self):
        with mock.patch("cardboard.zone.random.shuffle") as shuffle:
            self.o.shuffle()

        shuffle.assert_called_once_with(self.o._order)

    def test_iterable(self):
        # TODO: This is incomplete, all the methods don't take iterables
        o = z.OrderedZone(game=None, name="Emerald Hill",
                          contents=iter(range(40)))
        self.assertIn(2, o)
        self.assertTrue(list(o))


class TestZone(unittest.TestCase):
    def test_Zone(self):
        c = mock.Mock()

        for zone in ["battlefield", "exile", "hand"]:
            n = z.zone[zone](game=None, contents=[c])
            self.assertIsInstance(n, z.UnorderedZone)
            self.assertEquals(n.name, zone)
            self.assertIn(c, n)

        for zone in ["graveyard", "library", "stack"]:
            n = z.zone[zone](game=None, contents=[c])
            self.assertIsInstance(n, z.OrderedZone)
            self.assertEquals(n.name, zone)
            self.assertIn(c, n)

    """
    def test_zone(self):
        # TODO: Test all other zones
        self.db_card.type = "Creature"

        creature = c.Card(self.db_card, controller=self.player)

        creature.zone = self.game.battlefield
        self.assertIn(creature, self.player.game.battlefield)
        self.assertEqual(creature.zone, self.player.game.battlefield)
        self.assertNotIn(creature, self.player.library)

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
    """
