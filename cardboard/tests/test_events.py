import unittest

import cardboard.events as e


class TestEvent(unittest.TestCase):
    def test_iter(self):
        s = e.Event(foo={}, bar={})
        self.assertEqual({v.name for v in s}, {"foo", "bar"})

    def test_contains(self):
        s = e.Event(foo={})
        f = s["foo"]
        self.assertIn(f, s)

    def test_len(self):
        s = e.Event(subevents={"a" : {"b" : {}, "c" : {}}, "b" : {"a" : {}}})
        self.assertEqual(len(s), 2)

    def test_repr_str(self):
        s = e.Event("s", t={})
        self.assertEqual(repr(s), "<Event: s>")
        self.assertEqual(str(s), "s")

        self.assertEqual(repr(s["t"]), "<Event: s['t']>")
        self.assertEqual(str(s["t"]), "t")

    def test_setattr(self):
        s = e.Event("s")
        s["t"] = {}
        self.assertIsInstance(s["t"], e.Event)
        self.assertEquals(s["t"].name, "t")

    def test_eq(self):
        s = e.Event(subevents={"a" : {"b" : {}, "c" : {}}, "b" : {"a" : {}}})
        t = e.Event(subevents={"a" : {"b" : {}, "c" : {}}, "b" : {"a" : {}}})
        self.assertEqual(s, t)

        s = e.Event("s")
        self.assertNotEqual(s, t)

        self.assertIs(s.__eq__(object()), NotImplemented)

    def test_name(self):
        s = e.Event("s")
        self.assertEqual(s.name, "s")

    def test_kwargs(self):
        s = e.Event("s", foo={})
        self.assertIsInstance(s["foo"], e.Event)
        self.assertEqual(s["foo"].name, "foo")

        s = e.Event("s", {"foo" : {}}, bar={})
        self.assertEqual(s["foo"].name, "foo")
        self.assertEqual(s["bar"].name, "bar")

    def test_get(self):
        s = e.Event("s", foo={})
        self.assertIs(s.get("foo"), s["foo"])
        self.assertIsNone(s.get("bar"))

    def test_subevents(self):
        s = e.Event("s", {"foo" : {}, "bar" : {}})
        self.assertEqual(s.subevent_names, {"foo", "bar"})
        self.assertEqual(s.subevents, {s["foo"], s["bar"]})

    def test_set_subevents(self):
        s = e.Event(subevents={"a" : {"b" : {}, "c" : {}}, "b" : {"a" : {}}})

        self.assertIsInstance(s["a"], e.Event)
        self.assertIsInstance(s["a"]["b"], e.Event)
        self.assertIsInstance(s["a"]["c"], e.Event)
        self.assertEqual(s["a"].name, "a")
        self.assertEqual(s["a"]["b"].name, "b")
        self.assertEqual(s["a"]["c"].name, "c")

        self.assertIsInstance(s["b"], e.Event)
        self.assertIsInstance(s["b"]["a"], e.Event)
        self.assertEqual(s["b"].name, "b")
        self.assertEqual(s["b"]["a"].name, "a")

        self.assertRaises(AttributeError, getattr, s, "d")

    def test_update(self):
        s = e.Event("s")
        s.update({"a" : {"b" : {}, "c" : {}}, "b" : {}}, d={})
        self.assertEqual(s.subevent_names, {"a", "b", "d"})

        self.assertFalse(s["a"]["b"].subevents)
        self.assertFalse(s["a"]["c"].subevents)
        self.assertFalse(s["b"].subevents)
