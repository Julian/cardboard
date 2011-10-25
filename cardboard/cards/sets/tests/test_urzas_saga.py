import mock

from cardboard.card import Card
from cardboard.tests.util import GameTestCase
from cardboard.cards.sets import urzas_saga as u
from cardboard.frontend.testing import TestingFrontend


def card(**kwargs):
    m = mock.Mock(spec=Card, name=kwargs.get("name"))

    for k, v in kwargs.iteritems():
        setattr(m, k, v)

    return m


class TestUrzasSaga(GameTestCase):
    def setUp(self):
        super(TestUrzasSaga, self).setUp()
        self.f = self.p1.frontend = TestingFrontend(self.p1)
        self.game.start()

    def test_brand(self):
        controllers = [self.p1, self.p1, self.p2]
        f = [card(controller=c, owner=self.p1) for c in controllers]
        g = [card(controller=c, owner=self.p2) for c in controllers]
        self.game.battlefield.update(f + g)

        brand = card(game=self.game, controller=self.p1, owner=self.p1)
        self.game.battlefield.add(brand)

        u.brand(brand, [""])[0]()

        for c in f:
            self.assertIs(c.controller, self.p1)
            self.assertIs(c.owner, self.p1)

        for controller, c in zip(controllers, g):
            self.assertIs(c.controller, controller)
            self.assertIs(c.owner, self.p2)
