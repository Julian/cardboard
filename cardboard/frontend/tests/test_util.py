# -*- coding: utf-8 -*-
import unittest

from cardboard.frontend import util as u


class TestUtil(unittest.TestCase):
    def test_type_line(self):
        class Foo(object):
            types = {u"foo"}
            subtypes = None

        class Bar(object):
            types = {u"bar"}
            subtypes = {u"fly"}

        class Baz(object):
            types = {u"baz"}
            subtypes = [u"shoe", u"fly"]

        class Quux(object):
            types = {u"Artifact", u"Creature"}
            subtypes = {u"thing"}

        self.assertEqual(u.type_line(Foo), u"foo")
        self.assertEqual(u.type_line(Bar), u"bar — fly")
        self.assertEqual(u.type_line(Baz), u"baz — shoe, fly")
        self.assertEqual(u.type_line(Quux), u"Artifact Creature — thing")
