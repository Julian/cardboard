import unittest

import mock

from cardboard.tests.util import ANY
import cardboard.events as e


class TestCollaborate(unittest.TestCase):
    def test_trigger(self):

        game = mock.Mock()
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
            game = mock.Mock()

            @e.collaborate()
            def foo(self):
                pool = (yield)
                yield
                yield event

        Foo().foo()
        Foo.game.events.trigger.assert_called_once_with(event=event, pool=ANY)

    def test_game_added_to_pool(self):
        game = mock.Mock()

        @e.collaborate(game)
        def foo():
            pool = (yield)
            self.assertEqual(pool["game"], game)
            yield

        foo()

class TestEvent(unittest.TestCase):
    def test_iter(self):
        s = e.Event(None, {"foo" : {}, "bar" : {}})
        self.assertEqual({v.name for v in s}, {"foo", "bar"})

    def test_contains(self):
        s = e.Event(None, {"foo" : {}})
        f = s.foo
        self.assertIn(f, s)

    def test_name(self):
        s = e.Event("s")
        self.assertEqual(s.name, "s")

    def test_subevents(self):
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
