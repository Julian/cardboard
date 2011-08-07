import collections
import unittest

import cardboard.events as e


class TestEvent(unittest.TestCase):
    def test_iter(self):
        s = e.Event(None, {"foo" : {}, "bar" : {}})
        self.assertEqual({v.name for v in s}, {"foo", "bar"})

    def test_contains(self):
        s = e.Event(None, {"foo" : {}})
        f = s.foo
        self.assertIn(f, s)

    def test_repr_str(self):
        s = e.Event("s")
        self.assertEqual(repr(s), "Event('s')")
        self.assertEqual(str(s), "s")

    def test_name(self):
        s = e.Event("s")
        self.assertEqual(s.name, "s")

    def test_kwargs(self):
        s = e.Event("s", foo={})
        self.assertIsInstance(s.foo, e.Event)
        self.assertEqual(s.foo.name, "foo")

        s = e.Event("s", {"foo" : {}}, bar={})
        self.assertEqual(s.foo.name, "foo")
        self.assertEqual(s.bar.name, "bar")

    def test_subevent_names(self):
        s = e.Event("s", {"foo" : {}, "bar" : {}})
        self.assertEqual(s.subevent_names, {"foo", "bar"})

    def test_set_subevents(self):
        s = e.Event(None, {"a" : {"b" : {}, "c" : {}}, "b" : {"a" : {}}})

        self.assertIsInstance(s.a, e.Event)
        self.assertIsInstance(s.a.b, e.Event)
        self.assertIsInstance(s.a.c, e.Event)
        self.assertEqual(s.a.name, "a")
        self.assertEqual(s.a.b.name, "b")
        self.assertEqual(s.a.c.name, "c")

        self.assertIsInstance(s.b, e.Event)
        self.assertIsInstance(s.b.a, e.Event)
        self.assertEqual(s.b.name, "b")
        self.assertEqual(s.b.a.name, "a")

        self.assertRaises(AttributeError, getattr, s, "d")

    def test_ordered(self):
        keys = ["foo", "bar", "a", "z", "baz", "hello", "world", "oof", "rab"]
        o = collections.OrderedDict([(a, {}) for a in keys])
        s = e.Event("s", o)
        self.assertEqual([v.name for v in s], keys)
        self.assertIsInstance(s._subevents, collections.OrderedDict)
