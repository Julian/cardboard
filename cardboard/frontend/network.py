import itertools

from twisted.internet import endpoints, reactor
from zope.interface import Interface, implements

from cardboard import card, zone
from cardboard.frontend.mixin import FrontendMixin
from cardboard.util import ANY


class ILookupProxy(Interface):
    def proxy(e):
        pass

    def unproxy(e):
        pass

    def notify(frontend, method, parameters=()):
        pass

    def request(frontend, method, parameters=()):
        pass


class IRPC(Interface):
    def notify(method, parameters=()):
        pass

    def request(method, parameters=()):
        pass


class LookupProxy(object):

    implements(ILookupProxy)

    PROXIED = (card.Card, card.Token, zone.OrderedZone, zone.UnorderedZone)

    def __init__(self):
        self._counter = itertools.count(1)
        self._forward_lookups = {}
        self._reverse_lookups = {}

    def proxy(self, e):
        if isinstance(e, self.PROXIED):
            seen = self._reverse_lookups.get(e)

            if seen is not None:
                return seen
            else:
                id = next(self._counter)
                self._forward_lookups[id], self._reverse_lookups[e] = (e, id)
                return id
        return e

    def unproxy(self, e):
        return self._forward_lookups.get(e, e)

    def notify(self, frontend, method, parameters=()):
        proxied = {k : self.proxy(v) for k, v in parameters.iteritems()}
        frontend.protocol.notify(method=method, parameters=proxied)

    def request(self, frontend, method, parameters=()):
        proxied = {k : self.proxy(v) for k, v in parameters.iteritems()}
        deferred = frontend.protocol.request(method=method, parameters=proxied)
        return deferred.addCallback(
            lambda d : {k : self.unproxy(v) for k, v in d.iteritems()}
        )


class NetworkFrontend(FrontendMixin):
    """
    A frontend that sits across the network, communicated with via a protocol.

    The actual protocol used is arbitrary as far as this object is concerned.

    """

    LookupProxy = LookupProxy

    def __init__(self, player, debug=False):
        super(NetworkFrontend, self).__init__(player=player, debug=debug)
        self.lookup_proxy = getattr(self.game, "lookup_proxy", None)

        if self.lookup_proxy is None:
            self.lookup_proxy = self.game.lookup_proxy = self.LookupProxy()

    @property
    def protocol(self):
        return self.lookup_proxy.protocol

    @protocol.setter
    def protocol(self, proto):
        self.lookup_proxy.protocol = proto

    def select(self, choices, how_many=1, duplicates=False):
        return self.lookup_proxy.request(
            frontend=self, method="select", parameters={
                "choices" : choices,
                "how_many" : how_many,
                "duplicates" : duplicates,
        })

    def select_cards(
        self, zone=None, match=ANY, how_many=1, duplicates=False, bad=True
    ):
        return self.lookup_proxy.request(
            frontend=self, method="select_cards", parameters={
            "zone" : zone,
            "cards" : [card for card in zone if match(card)],
            "how_many" : how_many,
            "duplicates" : duplicates,
            "bad" : bad,
        })

    def select_players(
        self, match=ANY, how_many=1, duplicates=False, bad=True
    ):
        return self.lookup_proxy.request(
            frontend=self, method="select_players", parameters={
            "players" : [play for play in self.game.players if match(play)],
            "how_many" : how_many,
            "duplicates" : duplicates,
            "bad" : bad,
        })

    def select_combined(
        self, zone=None, match_cards=ANY, how_many_cards=1,
        duplicate_cards=False, match_players=ANY, how_many_players=1,
        duplicate_players=False, bad=True
    ):
        return self.lookup_proxy.request(
            frontend=self, method="select_combined", parameters={
            "zone" : zone,
            "cards" : [card for card in zone if match_cards(card)],
            "players" : [p for p in self.game.players if match_players(p)],
            "how_many_cards" : how_many_cards,
            "duplicate_cards" : duplicate_cards,
            "how_many_players" : how_many_players,
            "duplicate_players" : duplicate_players,
            "bad" : bad,
        })

    def select_range(self, start, stop, how_many=1, duplicates=False):
        return self.lookup_proxy.request(
            frontend=self, method="select_range", parameters={
            "start" : start,
            "stop" : stop,
            "how_many" : how_many,
            "duplicates" : duplicates,
        })
