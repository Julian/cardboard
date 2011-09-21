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
        with self.assertTriggers(event=self.zone_events["entered"]):
            self.u.add(30)

        with self.assertTriggers(event=self.zone_events["entered"]):
            self.o.add(30)

        self.assertEqual(set(self.u), set(self.noise) | {30})
        self.assertEqual(list(self.o), self.noise + [30])

    def test_add_already_contains(self):
        self.resetEvents()

        with self.assertRaises(ValueError):
            self.u.add(self.noise[0])

        with self.assertRaises(ValueError):
            self.o.add(self.noise[0])

        # wasn't added twice nor removed
        self.assertIn(self.noise[0], self.u)
        self.assertEqual(self.o.count(self.noise[0]), 1)

        self.assertFalse(self.events.trigger.called)

    def test_events_default(self):
        u = z.UnorderedZone("Emerald Hill", self.noise)
        o = z.OrderedZone("Casino Night", self.noise)

        self.assertIs(u._events, events)
        self.assertIs(o._events, events)

    def test_move(self):
        self.o.add(self.card)
        self.card.zone = self.o  # on actual cards this is a property

        with self.assertTriggers(event=self.zone_events["entered"]):
            self.u.move(self.card)
            self.card.zone = self.u

        self.assertIn(self.card, self.u)

        with self.assertTriggers(event=self.zone_events["entered"]):
            self.o.move(self.card)

        self.assertIn(self.card, self.o)

    def test_move_to_self(self):
        self.resetEvents()

        # shouldn't even be checking noise[0].zone
        with self.assertRaises(ValueError):
            self.u.move(self.noise[0])

        with self.assertRaises(ValueError):
            self.o.move(self.noise[0])

        # wasn't added twice nor removed
        self.assertIn(self.noise[0], self.u)
        self.assertEqual(self.o.count(self.noise[0]), 1)

        self.assertFalse(self.events.trigger.called)

    def test_pop(self):
        with self.assertTriggers(event=self.zone_events["left"]):
            e = self.u.pop()

        with self.assertTriggers(event=self.zone_events["left"]):
            self.o.pop()

        self.assertEqual(set(self.u), set(self.noise) - {e})
        self.assertEqual(list(self.o), self.noise[:-1])

    def test_remove(self):
        e = self.noise[-7]
        self.noise.remove(e)

        with self.assertTriggers(event=self.zone_events["left"]):
            self.u.remove(e)

        with self.assertTriggers(event=self.zone_events["left"]):
            self.o.remove(e)

        self.assertEqual(set(self.u), set(self.noise))
        self.assertEqual(list(self.o), self.noise)

        self.assertRaises(ValueError, self.u.remove, object())
        self.assertRaises(ValueError, self.o.remove, object())

    def test_silent(self):
        self.resetEvents()

        self.u.add(20, silent=True)
        self.o.add(20, silent=True)

        self.u.remove(self.noise[0], silent=True)
        self.o.remove(self.noise[0], silent=True)

        self.u.pop(silent=True)
        self.o.pop(silent=True)

        self.assertFalse(self.events.trigger.called)

    def test_iterable(self):
        i = range(10)

        # TODO: This is incomplete, all the methods don't take iterables
        o = z.OrderedZone(game=None, name="Emerald Hill", contents=i)
        u = z.UnorderedZone(game=None, name="Emerald Hill", contents=i)

        i.pop()

        self.assertEqual(list(o), range(10))
        self.assertEqual(list(u), range(10))


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

        event = {"event" : self.zone_events["entered"]}
        self.assertLastEventsWere([event] * 4)

    def test_index(self):
        e = self.noise[13]
        self.assertEqual(self.o.index(e), 13)

    def test_pop_index(self):
        self.o.pop(0)
        self.o.pop(13)

        self.noise.pop(0)
        self.noise.pop(13)

        self.assertEqual(list(self.o), self.noise)
        self.assertLastEventsWere([{"event" : self.zone_events["left"]}] * 2)

    def test_reverse(self):
        self.o.reverse()
        self.assertEqual(list(self.o), list(reversed(self.noise)))

    def test_shuffle(self):
        with mock.patch("cardboard.zone.random.shuffle") as shuffle:
            self.o.shuffle()

        shuffle.assert_called_once_with(self.o._order)

class TestZone(unittest.TestCase):
    def test_zone(self):
        c = mock.Mock()

        for zone in ["battlefield", "exile", "hand"]:
            n = z.zone[zone](game=None, contents=[c])
            self.assertIsInstance(n, z.UnorderedZone)
            self.assertEquals(n.name, zone.title())
            self.assertIn(c, n)

        for zone in ["graveyard", "library", "stack"]:
            n = z.zone[zone](game=None, contents=[c])
            self.assertIsInstance(n, z.OrderedZone)
            self.assertEquals(n.name, zone.title())
            self.assertIn(c, n)
