import collections
import random
import unittest

import mock

from cardboard import card as c, events, zone as z
from cardboard.tests.util import GameTestCase
from cardboard.util import ANY


ENTER, LEAVE = events.ENTERED_ZONE, events.LEFT_ZONE


class ZoneTest(GameTestCase):

    card = mock.Mock(spec=c.Card)

    def setUp(self):
        super(ZoneTest, self).setUp()
        self.u = z.UnorderedZone(
            name="Emerald Hill", game=self.game, contents=self.library,
        )

        self.o = z.OrderedZone(
            name="Casino Night", game=self.game, contents=self.library,
        )


class TestZones(ZoneTest):
    def test_name(self):
        self.assertEqual(self.u.name, "Emerald Hill")
        self.assertEqual(self.o.name, "Casino Night")

    def test_ordered(self):
        self.assertFalse(self.u.ordered)
        self.assertTrue(self.o.ordered)

    def test_str_repr(self):
        self.assertEqual(str(self.u), "Emerald Hill")
        self.assertEqual(str(self.o), "Casino Night")

        self.assertEqual(repr(self.u), "<Zone: Emerald Hill>")
        self.assertEqual(repr(self.o), "<Zone: Casino Night>")

    def test_contains(self):
        for i in self.library:
            self.assertIn(i, self.u)
            self.assertIn(i, self.o)

        self.assertNotIn(object(), self.u)
        self.assertNotIn(object(), self.o)

    def test_iter(self):
        self.assertEqual(set(self.u), set(self.library))
        self.assertEqual(list(self.o), self.library)

    def test_len(self):
        self.assertEqual(len(self.u), len(self.library))
        self.assertEqual(len(self.o), len(self.library))

    def test_add(self):
        with self.assertTriggers(event=ENTER, card=30, zone=self.u):
            self.u.add(30)

        with self.assertTriggers(event=ENTER, card=30, zone=self.o):
            self.o.add(30)

        self.assertEqual(set(self.u), set(self.library) | {30})
        self.assertEqual(list(self.o), self.library + [30])

    def test_add_already_contains(self):
        NO_OWNER, OWNER = "on the {}", "in {}'s {}"
        u, o = self.u.name, self.o.name

        n = mock.Mock()
        self.u.add(n)
        self.o.add(n)

        self.resetEvents()

        with self.assertRaisesRegexp(ValueError, NO_OWNER.format(u)):
            self.u.add(n)

        with self.assertRaisesRegexp(ValueError, NO_OWNER.format(o)):
            self.o.add(n)

        with self.assertRaisesRegexp(ValueError, OWNER.format(n.owner, u)):
            self.u.owner = n.owner
            self.u.add(n)

        with self.assertRaisesRegexp(ValueError, OWNER.format(n.owner, o)):
            self.o.owner = n.owner
            self.o.add(n)

        # wasn't added twice nor removed
        self.assertIn(self.library[0], self.u)
        self.assertEqual(self.o.count(self.library[0]), 1)

        self.assertFalse(self.events.trigger.called)

    def test_add_owner_redirection(self):
        """
        Adding a card with a different owner than the zone's redirects.

        """

        card = mock.Mock()

        self.u.name, self.o.name = "foo", "bar"
        self.u.owner, self.o.owner = mock.Mock(), mock.Mock()

        self.u.add(card)
        self.o.add(card)

        card.owner.foo.add.assert_called_once_with(card)
        card.owner.bar.add.assert_called_once_with(card)

    def test_move(self):
        self.o.add(self.card)
        self.card.zone = self.o  # on actual cards this is a property

        with self.assertTriggers(event=ENTER, card=self.card, zone=self.u):
            self.u.move(self.card)
            self.card.zone = self.u

        self.assertIn(self.card, self.u)

        with self.assertTriggers(event=ENTER, card=self.card, zone=self.o):
            self.o.move(self.card)

        self.assertIn(self.card, self.o)

    def test_move_to_self(self):
        self.resetEvents()

        # shouldn't even be checking library[0].zone
        with self.assertRaises(ValueError):
            self.u.move(self.library[0])

        with self.assertRaises(ValueError):
            self.o.move(self.library[0])

        # wasn't added twice nor removed
        self.assertIn(self.library[0], self.u)
        self.assertEqual(self.o.count(self.library[0]), 1)

        self.assertFalse(self.events.trigger.called)

    def test_pop(self):
        self.resetEvents()
        e = self.u.pop()
        self.assertLastEventsWere([dict(event=LEAVE, card=e, zone=self.u)])

        self.resetEvents()
        f = self.o.pop()
        self.assertLastEventsWere([dict(event=LEAVE, card=f, zone=self.o)])

        self.assertEqual(set(self.u), set(self.library) - {e})
        self.assertEqual(list(self.o), self.library[:-1])

    def test_remove(self):
        e = self.library[-7]
        self.library.remove(e)

        with self.assertTriggers(event=LEAVE, card=e, zone=self.u):
            self.u.remove(e)

        with self.assertTriggers(event=LEAVE, card=e, zone=self.o):
            self.o.remove(e)

        self.assertEqual(set(self.u), set(self.library))
        self.assertEqual(list(self.o), self.library)

        self.assertRaises(ValueError, self.u.remove, object())
        self.assertRaises(ValueError, self.o.remove, object())

    def test_update(self):
        self.u.update(range(4))

        for i in range(4):
            self.assertIn(i, self.u)

        self.assertEqual(len(self.u), len(self.library) + 4)

        evs = [dict(event=ENTER, card=i, zone=self.u) for i in range(4)]
        self.assertLastEventsWere(evs)

        self.resetEvents()

        self.o.update(range(4))
        self.assertEqual(self.o[-4:], range(4))

        self.assertEqual(len(self.o), len(self.library) + 4)

        evs = [dict(event=ENTER, card=i, zone=self.o) for i in range(4)]
        self.assertLastEventsWere(evs)

    def test_silent(self):
        self.o.add(self.card)
        self.card.zone = self.o
        self.resetEvents()

        self.u.add(20, silent=True)
        self.o.add(20, silent=True)

        self.u.remove(self.library[0], silent=True)
        self.o.remove(self.library[0], silent=True)

        self.u.pop(silent=True)
        self.o.pop(silent=True)

        self.u.move(self.card, silent=True)
        self.card.zone = self.u
        self.o.move(self.card, silent=True)

        self.u.update(range(10), silent=True)
        self.o.update(range(10), silent=True)

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
        self.assertEqual(list(reversed(self.o)), list(reversed(self.library)))

    def test_getitem(self):
        for i, e in enumerate(self.library):
            self.assertEqual(self.o[i], e)

        self.assertEqual(self.o[2:7:2], self.library[2:7:2])

    def test_set_del_item(self):
        self.assertRaises(AttributeError, getattr, self.o, "__setitem__")
        self.assertRaises(AttributeError, getattr, self.o, "__delitem__")

    def test_count(self):
        o = z.OrderedZone(game=None, name="Emerald Hill",
                          contents=[1, 1, 1, 2, 2, 3])

        for i, e in enumerate(range(3, 0, -1), 1):
            self.assertEqual(o.count(e), i)

    def test_index(self):
        e = self.library[4]
        self.assertEqual(self.o.index(e), 4)

    def test_pop_index(self):
        e1 = self.o.pop(0)
        e2 = self.o.pop(4)

        self.library.pop(0)
        self.library.pop(4)

        self.assertEqual(list(self.o), self.library)
        self.assertLastEventsWere([
            {"event" : LEAVE, "card" : e1, "zone" : self.o},
            {"event" : LEAVE, "card" : e2, "zone" : self.o},
        ])

    def test_reverse(self):
        self.o.reverse()
        self.assertEqual(list(self.o), list(reversed(self.library)))

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
            self.assertEquals(n.name, zone)
            self.assertIn(c, n)

        for zone in ["graveyard", "library", "stack"]:
            n = z.zone[zone](game=None, contents=[c])
            self.assertIsInstance(n, z.OrderedZone)
            self.assertEquals(n.name, zone)
            self.assertIn(c, n)
