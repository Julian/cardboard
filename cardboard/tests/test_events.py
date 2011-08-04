import unittest

from mock import Mock

from cardboard.tests.util import ANY
import cardboard.events as e


class TestCollaborate(unittest.TestCase):
    def test_trigger(self):
        handler = Mock()

        r, v, q = (e.Event(i) for i in ["do request", "do event",
                                        "do requested event"])

        @e.collaborate(handler)
        def nothing():
            pool = (yield)
            yield
            self.assertFalse(handler.trigger.called)

        @e.collaborate(handler)
        def request():
            pool = (yield)
            yield r
            yield
            handler.trigger.assert_called_with(request=r, pool=ANY)

        @e.collaborate(handler)
        def event():
            pool = (yield)
            yield
            yield v
            handler.trigger.assert_called_with(event=v, pool=ANY)


        @e.collaborate(handler)
        def requested_event():
            pool = (yield)
            self.pool = pool
            yield q
            handler.trigger.assert_called_with(request=q, pool=ANY)
            yield
            yield q
            handler.trigger.assert_called_with(event=q, pool=ANY)

        nothing()
        request()
        event()
        requested_event()

    def test_default_handler(self):
        event = e.Event("do event")

        class Foo(object):
            events = Mock()

            @e.collaborate()
            def foo(self):
                pool = (yield)
                yield
                yield event

        Foo().foo()
        Foo.events.trigger.assert_called_once_with(event=event, pool=ANY)


class TestEventStore(unittest.TestCase):
    def test_iter(self):
        s = e.EventStore("foo", "bar")
        self.assertEqual(list(iter(s)), ["foo", "bar"])

    def test_substore(self):
        s = e.EventStore("foo")

        s.test = {"bar", "baz"}
        self.assertIsInstance(s.test, e.EventStore)
        self.assertEqual(s.substores.viewkeys(), {"test"})

        self.assertIsInstance(s.test["bar"], e.Event)
        self.assertEqual(s.test["bar"].name, "bar")

        self.assertIsInstance(s.test["baz"], e.Event)
        self.assertEqual(s.test["baz"].name, "baz")
