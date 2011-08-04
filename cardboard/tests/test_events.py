import unittest

from mock import Mock

from cardboard.tests.util import ANY
import cardboard.events as e


class TestAnnounce(unittest.TestCase):
    def test_add_events(self):
        store = {}

        @e.announce(bar="foo bar", baz="foo baz", store=store)
        def foo():
            pass

        self.assertEqual(store["bar"].description, "foo bar")
        self.assertEqual(store["baz"].description, "foo baz")

    def test_trigger(self):
        handler = Mock()

        r, v, q = (e.Event(i) for i in ["do request", "do event",
                                        "do requested event"])
        store = {"request" : r, "event" : v, "requested_event" : q}

        @e.announce(handler, store=store)
        def nothing():
            pool = (yield)
            yield
            self.assertFalse(handler.trigger.called)

        @e.announce(handler, store=store)
        def request():
            pool = (yield)
            yield "request"
            yield
            handler.trigger.assert_called_with(request=r, pool=ANY)

        @e.announce(handler, store=store)
        def event():
            pool = (yield)
            yield
            yield "event"
            handler.trigger.assert_called_with(event=v, pool=ANY)


        @e.announce(handler, store=store)
        def requested_event():
            pool = (yield)
            self.pool = pool
            yield "requested_event"
            handler.trigger.assert_called_with(request=q, pool=ANY)
            yield
            yield "requested_event"
            handler.trigger.assert_called_with(event=q, pool=ANY)

        nothing()
        request()
        event()
        requested_event()

    def test_default_handler(self):
        event = e.Event("do event")

        class Foo(object):
            events = Mock()
            store = {"event" : event}

            @e.announce(store=store)
            def foo(self):
                pool = (yield)
                yield
                yield "event"

        Foo().foo()
        Foo.events.trigger.assert_called_once_with(event=event, pool=ANY)


class TestEventStore(unittest.TestCase):
    def test_substore(self):
        s = e.EventStore()
        self.assertIsInstance(s.test_store, e.EventStore)
        self.assertIn("test_store", s.substores)

    def test_event(self):
        s = e.EventStore()
        s["foo"] = "called foo"
        self.assertIn("foo", s)
        self.assertEqual(s["foo"], "called foo")
        self.assertEqual(len(s), 1)
