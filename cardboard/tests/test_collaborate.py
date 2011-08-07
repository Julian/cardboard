import unittest

import mock

from cardboard.tests.util import ANY
import cardboard.collaborate as c


class TestCollaborate(unittest.TestCase):
    def test_trigger(self):

        game = mock.Mock()
        r, v, q = (object() for _ in range(3))

        @c.collaborate(game)
        def nothing():
            pool = (yield)
            yield
            self.assertFalse(game.events.trigger.called)

        @c.collaborate(game)
        def request():
            pool = (yield)
            yield r
            yield
            game.events.trigger.assert_called_with(request=r, pool=ANY)

        @c.collaborate(game)
        def event():
            pool = (yield)
            yield
            yield v
            game.events.trigger.assert_called_with(event=v, pool=ANY)


        @c.collaborate(game)
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
        event = object()

        class Foo(object):
            game = mock.Mock()

            @c.collaborate()
            def foo(self):
                pool = (yield)
                yield
                yield event

        Foo().foo()
        Foo.game.events.trigger.assert_called_once_with(event=event, pool=ANY)

    def test_game_added_to_pool(self):
        game = mock.Mock()

        @c.collaborate(game)
        def foo():
            pool = (yield)
            self.assertEqual(pool["game"], game)
            yield

        foo()
