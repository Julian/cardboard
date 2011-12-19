"""
Integration tests and tests that touch the db or filesystem and the like.

"""

import unittest

from cardboard.cards import match
from cardboard.db import models as m


class AbilityMatchingTest(unittest.TestCase):
    def test_match(self):
        breezekeeper = m.Card.query.get(u"Breezekeeper")
        self.assertTrue(match.phases(breezekeeper))
