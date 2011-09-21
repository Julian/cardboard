# -*- coding: utf-8 -*-
import unittest

from cardboard.frontend import util as u


class TestUtil(unittest.TestCase):
    def test_type_line(self):
        class Foo(object):
            type = u"foo"
            subtypes = None

        class Bar(object):
            type = u"bar"
            subtypes = [u"fly"]

        class Baz(object):
            type = u"baz"
            subtypes = [u"shoe", u"fly"]

        self.assertEqual(u.type_line(Foo), u"foo")
        self.assertEqual(u.type_line(Bar), u"bar — fly")
        self.assertEqual(u.type_line(Baz), u"baz — shoe, fly")
