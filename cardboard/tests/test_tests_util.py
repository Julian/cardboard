import unittest

import mock

from cardboard.util import requirements
import cardboard.tests.util as u

class TestEventHandlerTestCase(u.EventHandlerTestCase):
    def test_assertSubscribed(self):
        self.events.subscribe(next, event="foo")
        self.assertSubscribed(next, event="foo")

        with self.assertRaises(self.failureException):
            self.assertSubscribed(next, event="bar")

        with self.assertRaises(self.failureException):
            self.assertSubscribed(next, event="foo", other="bar")

    def test_assertTriggered(self):
        i = [[(), {"e" : i}] for i in range(10)]

        self.assertTriggered([{"e" : 1}, {"e" : 3}, {"e" : 7}], i)
        self.assertTriggered([{"e" : 3}, {"e" : 8}, {"e" : 9}], i)

        with self.assertRaises(self.failureException):
            self.assertTriggered([{"e" : 9}, {"e" : 7}, {"e" : 9}], i)

        with self.assertRaises(self.failureException):
            self.assertTriggered([{"e" : 7}, {"e" : 7}, {"e" : 7}], i)

    def test_checkRequirements(self):

        test = self

        i, j, k = object(), object(), object()

        class Foo(object):
            foo = i
            bar = j
            baz = k

            require = requirements()

            @property
            def quux(self):
                return i

            def requires_foo(self, arg, kwarg):
                self.require(foo=True)
                test.assertEqual(arg, 0)
                test.assertEqual(kwarg, 2)

            def requires_foo_not_bar(self, arg, kwarg):
                self.require(foo=True, bar=False)
                test.assertEqual(arg, 1)
                test.assertEqual(kwarg, 1)

            def requires_not_quux(self, arg, kwarg):
                self.require(quux=False)
                test.assertEqual(arg, 2)
                test.assertEqual(kwarg, 0)

        f = Foo()

        for req, fn, arg, kwarg in [
            ({"foo" : True}, f.requires_foo, 0, 2),
            ({"foo" : True, "bar" : False}, f.requires_foo_not_bar, 1, 1),
            ({"quux" : False}, f.requires_not_quux, 2, 0),
        ]:

            with self.checkRequirements(fn, arg, kwarg=kwarg) as require:
                require.assertMet(**req)
                require.assertNotMet(**{k : not v for k, v in req.iteritems()})

        for wrong, fn, arg, kwarg in [
            ({"foo" : False}, f.requires_foo, 0, 2),
            ({"foo" : False, "bar" : True}, f.requires_foo_not_bar, 1, 1),
            ({"foo" : True, "quux" : True}, f.requires_not_quux, 2, 0),
        ]:

            with self.assertRaises(self.failureException):
                with self.checkRequirements(fn, arg, kwarg=kwarg) as require:
                    require.assertMet(**wrong)

            with self.assertRaises(self.failureException):
                with self.checkRequirements(fn, arg, kwarg=kwarg) as require:
                    good = {k : not v for k, v in wrong.iteritems()}
                    require.assertNotMet(**good)

        self.assertIs(f.foo, i)
        self.assertIs(f.bar, j)
        self.assertIs(f.baz, k)

        self.assertIs(f.quux, i)

    def test_resetEvents(self):
        self.events.trigger("foo")
        self.events.trigger("bar", baz=2)

        self.assertTrue(self.events.trigger.call_args_list)
        self.assertTrue(self.events.trigger.called)

        self.resetEvents()

        self.assertFalse(self.events.trigger.call_args_list)
        self.assertFalse(self.events.trigger.called)

        self.events.trigger("foobar")

        self.assertTrue(self.events.trigger.call_args_list)
        self.assertTrue(self.events.trigger.called)
