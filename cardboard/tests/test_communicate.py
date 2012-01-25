from twisted.trial import unittest
import mock

from cardboard import communicate


class TestNetworkFrontend(unittest.TestCase):

    game, protocol = mock.Mock(), mock.Mock()
    frontend = communicate.NetworkFrontend(game, protocol)

    def test_select(self):
        self.frontend.select([u"foo", u"bar", u"baz"])

        self.protocol.callRemote.assert_called_with(
            communicate.Select,
            choices=[u"foo", u"bar", u"baz"],
            how_many=1,
            duplicates=False,
        )

        self.frontend.select([u"foo"], how_many=2, duplicates=True)

        self.protocol.callRemote.assert_called_with(
            communicate.Select,
            choices=[u"foo"],
            how_many=2,
            duplicates=True,
        )

    def test_select_cards(self):
        # Instead of a real zone, let's just match a list
        self.frontend.select_cards([1, 2, 3, 4])

        self.protocol.callRemote.assert_called_with(
            communicate.SelectCards,
            cards=[1, 2, 3, 4],
            how_many=1,
            duplicates=False,
            bad=True,
        )

        # match should be evaluated immediately,
        # since we can't serialize the match function
        self.frontend.select_cards(
            [1, 2, 3, 4], match=lambda x : x % 2,
            how_many=3, duplicates=True, bad=False
        )

        self.protocol.callRemote.assert_called_with(
            communicate.SelectCards,
            cards=[1, 3],
            how_many=3,
            duplicates=True,
            bad=False,
        )

    def test_select_players(self):
        self.frontend.game.players = [1, 2, 3, 4]

        self.frontend.select_players()

        self.protocol.callRemote.assert_called_with(
            communicate.SelectPlayers,
            players=[1, 2, 3, 4],
            how_many=1,
            duplicates=False,
            bad=True,
        )

        self.frontend.select_players(
            match=lambda x : x % 2, how_many=4, duplicates=True, bad=False,
        )

        self.protocol.callRemote.assert_called_with(
            communicate.SelectPlayers,
            players=[1, 3],
            how_many=4,
            duplicates=True,
            bad=False,
        )

    def test_select_combined(self):
        self.frontend.game.players = [1, 2, 3, 4]

        self.frontend.select_combined(zone=[2, 4, 6, 8])

        self.protocol.callRemote.assert_called_with(
            communicate.SelectCombined,
            cards=[2, 4, 6, 8],
            players=[1, 2, 3, 4],
            how_many_cards=1,
            how_many_players=1,
            duplicate_cards=False,
            duplicate_players=False,
            bad=True,
        )

        self.frontend.select_combined(
            zone=[2, 4, 6, 8], bad=False, how_many_cards=2, how_many_players=4,
            match_cards=lambda x : x > 4, match_players=lambda x : x % 2,
            duplicate_cards=True, duplicate_players=True,
        )

        self.protocol.callRemote.assert_called_with(
            communicate.SelectCombined,
            cards=[6, 8],
            players=[1, 3],
            how_many_cards=2,
            how_many_players=4,
            duplicate_cards=True,
            duplicate_players=True,
            bad=False,
        )

    def test_select_range(self):
        self.frontend.select_range(2, 24)

        self.protocol.callRemote.assert_called_with(
            communicate.SelectRange,
            start=2,
            stop=24,
            how_many=1,
            duplicates=False,
        )

        self.frontend.select_range(2, 4, how_many=3, duplicates=True)

        self.protocol.callRemote.assert_called_with(
            communicate.SelectRange,
            start=2,
            stop=4,
            how_many=3,
            duplicates=True,
        )
