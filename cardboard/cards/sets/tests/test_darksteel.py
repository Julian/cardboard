import mock

from cardboard.card import Card
from cardboard.tests.util import GameTestCase
from cardboard.cards.sets import darksteel as d
from cardboard.frontend.testing import TestingFrontend


def card(**kwargs):
    m = mock.Mock(spec=Card, name=kwargs.get("name"))

    for k, v in kwargs.iteritems():
        setattr(m, k, v)

    return m


class TestDarkSteel(GameTestCase):
    def setUp(self):
        super(TestDarkSteel, self).setUp()
        self.f = self.p1.frontend = TestingFrontend(self.p1)
        self.game.start()

    def test_echoing_truth(self):
        f = [card(name="Foo", owner=o) for o in [self.p1, self.p1, self.p2]]
        g = [card(name=name, owner=self.p2) for name in "Bar", "Baz"]
        self.game.battlefield.update(f + g)

        echoing_truth = card(
            name="Echoing Truth", game=self.game,
            controller=self.p1, owner=self.p1
        )
        self.game.battlefield.add(echoing_truth)

        with self.f.select.cards.will_return(f[0]):
            d.echoing_truth(echoing_truth, [""])[0]()

        for c in f:
            self.assertIn(c, c.owner.hand)

        for c in g:
            self.assertIn(c, self.game.battlefield)
