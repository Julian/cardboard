from twisted.internet import defer, protocol
from twisted.trial import unittest
import mock

from cardboard import card, zone
from cardboard.frontend import network


class TestLookupProxy(unittest.TestCase):

    card, token, uzone, ozone = [mock.Mock(spec=cls) for cls in (
        card.Card, card.Token, zone.UnorderedZone, zone.OrderedZone
    )]

    def setUp(self):
        self.frontend = mock.Mock()
        self.frontend.protocol.request.side_effect = (
            lambda method, parameters : defer.Deferred()
        )
        self.lookup = network.LookupProxy()

    def test_proxy(self):
        self.assertEqual(self.lookup.proxy(self.card), 1)
        self.assertEqual(self.lookup.proxy(self.token), 2)
        self.assertEqual(self.lookup.proxy(self.uzone), 3)
        self.assertEqual(self.lookup.proxy(self.ozone), 4)

        # duplicates get the same ID
        self.assertEqual(self.lookup.proxy(self.card), 1)
        self.assertEqual(self.lookup.proxy(self.token), 2)
        self.assertEqual(self.lookup.proxy(self.uzone), 3)
        self.assertEqual(self.lookup.proxy(self.ozone), 4)

        other = object()
        self.assertEqual(self.lookup.proxy(other), other)

        self.assertEqual(self.lookup.unproxy(1), self.card)
        self.assertEqual(self.lookup.unproxy(2), self.token)
        self.assertEqual(self.lookup.unproxy(3), self.uzone)
        self.assertEqual(self.lookup.unproxy(4), self.ozone)

        self.assertEqual(self.lookup.unproxy(other), other)

    def test_notify(self):
        n = self.lookup.notify(
            self.frontend, "foo", {"bar" : self.card, "baz" : self.token}
        )

        c, t = self.lookup.proxy(self.card), self.lookup.proxy(self.token)
        self.frontend.protocol.notify.assert_called_once_with(
            method="foo", parameters={"bar" : c, "baz" : t}
        )
        self.assertIsNone(n)

        other = object()

        r = self.lookup.request(
            self.frontend, "bar", {"foo" : self.card, "bar" : self.uzone}
        )

        r.addCallback(
            lambda r : self.assertEqual(
                r, {"foo" : self.card, "bar" : self.uzone, "baz" : other}
            )
        )

        r.callback(
            {"foo" : c, "bar" : self.lookup.proxy(self.uzone), "baz" : other}
        )


class TestNetworkFrontend(unittest.TestCase):

    p1 = mock.Mock()
    frontend = network.NetworkFrontend(p1)
    lookup_proxy = frontend.lookup_proxy

    def test_persists_lookup_proxy(self):
        frontend = network.NetworkFrontend(self.p1)
        self.assertIs(frontend.lookup_proxy, self.frontend.lookup_proxy)

        self.p1.game.lookup_proxy = None
        frontend = network.NetworkFrontend(self.p1)
        self.assertIs(self.p1.game.lookup_proxy, frontend.lookup_proxy)
        self.assertIsNot(frontend.lookup_proxy, self.frontend.lookup_proxy)

    def test_select(self):
        self.frontend.select([u"foo", u"bar", u"baz"])

        self.lookup_proxy.request.assert_called_with(
            frontend=self.frontend, method="select", parameters={
            "choices" : [u"foo", u"bar", u"baz"],
            "how_many" : 1,
            "duplicates" : False,
        })

        self.frontend.select([u"foo"], how_many=2, duplicates=True)

        self.lookup_proxy.request.assert_called_with(
            frontend=self.frontend, method="select", parameters={
            "choices" : [u"foo"],
            "how_many" : 2,
            "duplicates" : True,
        })

    def test_select_cards(self):
        # Instead of a real zone, let's just match a list
        self.frontend.select_cards([1, 2, 3, 4])

        self.lookup_proxy.request.assert_called_with(
            frontend=self.frontend, method="select_cards", parameters={
            "zone" : [1, 2, 3, 4],
            "cards" : [1, 2, 3, 4],
            "how_many" : 1,
            "duplicates" : False,
            "bad" : True,
        })

        # match should be evaluated immediately,
        # since we can't serialize the match function
        self.frontend.select_cards(
            [1, 2, 3, 4], match=lambda x : x % 2,
            how_many=3, duplicates=True, bad=False
        )

        self.lookup_proxy.request.assert_called_with(
            frontend=self.frontend, method="select_cards", parameters={
            "zone" : [1, 2, 3, 4],
            "cards" : [1, 3],
            "how_many" : 3,
            "duplicates" : True,
            "bad" : False,
        })

    def test_select_players(self):
        self.frontend.game.players = [1, 2, 3, 4]

        self.frontend.select_players()

        self.lookup_proxy.request.assert_called_with(
            frontend=self.frontend, method="select_players", parameters={
            "players" : [1, 2, 3, 4],
            "how_many" : 1,
            "duplicates" : False,
            "bad" : True,
        })

        self.frontend.select_players(
            match=lambda x : x % 2, how_many=4, duplicates=True, bad=False,
        )

        self.lookup_proxy.request.assert_called_with(
            frontend=self.frontend, method="select_players", parameters={
            "players" : [1, 3],
            "how_many" : 4,
            "duplicates" : True,
            "bad" : False,
        })

    def test_select_combined(self):
        self.frontend.game.players = [1, 2, 3, 4]

        self.frontend.select_combined(zone=[2, 4, 6, 8])

        self.lookup_proxy.request.assert_called_with(
            frontend=self.frontend, method="select_combined", parameters={
            "zone" : [2, 4, 6, 8],
            "cards" : [2, 4, 6, 8],
            "players" : [1, 2, 3, 4],
            "how_many_cards" : 1,
            "how_many_players" : 1,
            "duplicate_cards" : False,
            "duplicate_players" : False,
            "bad" : True,
        })

        self.frontend.select_combined(
            zone=[2, 4, 6, 8], bad=False, how_many_cards=2, how_many_players=4,
            match_cards=lambda x : x > 4, match_players=lambda x : x % 2,
            duplicate_cards=True, duplicate_players=True,
        )

        self.lookup_proxy.request.assert_called_with(
            frontend=self.frontend, method="select_combined", parameters={
            "zone" : [2, 4, 6, 8],
            "cards" : [6, 8],
            "players" : [1, 3],
            "how_many_cards" : 2,
            "how_many_players" : 4,
            "duplicate_cards" : True,
            "duplicate_players" : True,
            "bad" : False,
        })

    def test_select_range(self):
        self.frontend.select_range(2, 24)

        self.lookup_proxy.request.assert_called_with(
            frontend=self.frontend, method="select_range", parameters={
            "start" : 2,
            "stop" : 24,
            "how_many" : 1,
            "duplicates" : False,
        })

        self.frontend.select_range(2, 4, how_many=3, duplicates=True)

        self.lookup_proxy.request.assert_called_with(
            frontend=self.frontend, method="select_range", parameters={
            "start" : 2,
            "stop" : 4,
            "how_many" : 3,
            "duplicates" : True,
        })
