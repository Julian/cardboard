from twisted.protocols import amp

from cardboard.util import ANY


class Select(amp.Command):
    pass


class SelectCards(amp.Command):
    pass


class SelectPlayers(amp.Command):
    pass


class SelectCombined(amp.Command):
    pass


class SelectRange(amp.Command):
    pass


class NetworkFrontend(object):
    """
    A frontend that sits across the network, communicated with via a protocol.

    """

    player = None

    def __init__(self, game, protocol):
        self.game = game
        self.protocol = protocol

    def select(self, choices, how_many=1, duplicates=False):
        return self.protocol.callRemote(
            Select, choices=choices, how_many=how_many, duplicates=duplicates
        )

    def select_cards(
        self, zone=None, match=ANY, how_many=1, duplicates=False, bad=True
    ):
        cards = [card for card in zone if match(card)]
        return self.protocol.callRemote(
            SelectCards, cards=cards, how_many=how_many,
            duplicates=duplicates, bad=bad,
        )

    def select_players(
        self, match=ANY, how_many=1, duplicates=False, bad=True
    ):
        players = [player for player in self.game.players if match(player)]
        return self.protocol.callRemote(
            SelectPlayers, players=players, how_many=how_many,
            duplicates=duplicates, bad=bad,
        )

    def select_combined(
        self, zone=None, match_cards=ANY, how_many_cards=1,
        duplicate_cards=False, match_players=ANY, how_many_players=1,
        duplicate_players=False, bad=True,
    ):
        cards = [card for card in zone if match_cards(card)]
        players = [play for play in self.game.players if match_players(play)]
        return self.protocol.callRemote(
            SelectCombined, cards=cards, players=players,
            how_many_cards=how_many_cards, duplicate_cards=duplicate_cards,
            how_many_players=how_many_players,
            duplicate_players=duplicate_players, bad=bad,
        )

    def select_range(self, start, stop, how_many=1, duplicates=False):
        return self.protocol.callRemote(
            SelectRange, start=start, stop=stop,
            how_many=how_many, duplicates=duplicates,
        )
