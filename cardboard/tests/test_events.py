import unittest

from mock import Mock

from cardboard.tests.util import ANY
import cardboard.events as e


class TestCollaborate(unittest.TestCase):
    def test_trigger(self):

        game = Mock()
        r, v, q = (e.Event(i) for i in ["req", "ev", "req ev"])

        @e.collaborate(game)
        def nothing():
            pool = (yield)
            yield
            self.assertFalse(game.events.trigger.called)

        @e.collaborate(game)
        def request():
            pool = (yield)
            yield r
            yield
            game.events.trigger.assert_called_with(request=r, pool=ANY)

        @e.collaborate(game)
        def event():
            pool = (yield)
            yield
            yield v
            game.events.trigger.assert_called_with(event=v, pool=ANY)


        @e.collaborate(game)
        def requested_event():
            pool = (yield)
            self.pool = pool
            yield q
            game.events.trigger.assert_called_with(request=q, pool=ANY)
            yield
            yield q
            game.events.trigger.assert_called_with(event=q, pool=ANY)

        nothing()
        request()
        event()
        requested_event()

    def test_default_handler(self):
        event = e.Event("do event")

        class Foo(object):
            game = Mock()

            @e.collaborate()
            def foo(self):
                pool = (yield)
                yield
                yield event

        Foo().foo()
        Foo.game.events.trigger.assert_called_once_with(event=event, pool=ANY)


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
