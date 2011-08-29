import unittest

import mock

import cardboard.tests.util as u

class TestEventHandlerTestCase(u.EventHandlerTestCase):
    def test_assertTriggered(self):
        i = [[(), {"e" : i}] for i in range(10)]

        self.assertTriggered([{"e" : 1}, {"e" : 3}, {"e" : 7}], i)
        self.assertTriggered([{"e" : 3}, {"e" : 8}, {"e" : 9}], i)

        with self.assertRaises(AssertionError):
            self.assertTriggered([{"e" : 9}, {"e" : 7}, {"e" : 9}], i)

        with self.assertRaises(AssertionError):
            self.assertTriggered([{"e" : 7}, {"e" : 7}, {"e" : 7}], i)
