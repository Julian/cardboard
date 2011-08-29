from collections import deque
from cStringIO import StringIO
from textwrap import dedent
import unittest

import cardboard.db.util as u

class TestParser(unittest.TestCase):
    def test_parse(self):
        b = deque(["Title", "UU", "Instant", "Do something cool.", "UG-R"])

        self.assertEqual(u.parse(b), {"name" : "Title",
                                      "type" : "Instant",
                                      "mana_cost" : "UU",
                                      "appearances" : [("UG", "R")],
                                      "abilities" : ["Do something cool."]})

    def test_load(self):
        s = dedent("""
                   Title
                   UU
                   Instant
                   Do something cool.
                   UG-R

                   WTFIsASchemeWizards
                   Scheme
                   Not at all cool.
                   ARC-C

                   Another
                   GG
                   Creature -- Cool Doer
                   4/2
                   Does cool things.
                   Like this.
                   UG-U

                   Last One
                   G/U
                   Enchantment
                   Still cooler than Schemes.
                   UG-C, GU-U
                   """)

        r = u.load(StringIO(s))

        self.assertEqual(next(r), {"name" : "Title",
                                   "type" : "Instant",
                                   "mana_cost" : "UU",
                                   "appearances" : [("UG", "R")],
                                   "abilities" : ["Do something cool."]})

        self.assertEqual(next(r), {"name" : "Another",
                                   "type" : "Creature",
                                   "subtypes" : ["Cool Doer"],
                                   "power" : "4",
                                   "toughness" : "2",
                                   "mana_cost" : "GG",
                                   "appearances" : [("UG", "U")],
                                   "abilities" : ["Does cool things.",
                                                  "Like this."]})

        self.assertEqual(next(r), {"name" : "Last One",
                                   "type" : "Enchantment",
                                   "mana_cost" : "G/U",
                                   "appearances" : [("UG", "C"), ("GU", "U")],
                                   "abilities" : ["Still cooler than Schemes."]})
