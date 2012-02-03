from twisted.trial import unittest
import jsonschema
import mock

from cardboard import api


class TestUser(unittest.TestCase):

    skip = True

    def test_select(self):
        self.user.select([u"foo", u"bar", u"baz"])

        self.protocol.callRemote.assert_called_with(
            communicate.Select,
            choices=[u"foo", u"bar", u"baz"],
            how_many=1,
            duplicates=False,
        )

        self.user.select([u"foo"], how_many=2, duplicates=True)

        self.protocol.callRemote.assert_called_with(
            communicate.Select,
            choices=[u"foo"],
            how_many=2,
            duplicates=True,
        )

    def test_select_cards(self):
        # Instead of a real zone, let's just match a list
        self.user.select_cards([1, 2, 3, 4])

        self.protocol.callRemote.assert_called_with(
            communicate.SelectCards,
            cards=[1, 2, 3, 4],
            how_many=1,
            duplicates=False,
            bad=True,
        )

        # match should be evaluated immediately,
        # since we can't serialize the match function
        self.user.select_cards(
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
        self.user.game.players = [1, 2, 3, 4]

        self.user.select_players()

        self.protocol.callRemote.assert_called_with(
            communicate.SelectPlayers,
            players=[1, 2, 3, 4],
            how_many=1,
            duplicates=False,
            bad=True,
        )

        self.user.select_players(
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
        self.user.game.players = [1, 2, 3, 4]

        self.user.select_combined(zone=[2, 4, 6, 8])

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

        self.user.select_combined(
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
        self.user.select_range(2, 24)

        self.protocol.callRemote.assert_called_with(
            communicate.SelectRange,
            start=2,
            stop=24,
            how_many=1,
            duplicates=False,
        )

        self.user.select_range(2, 4, how_many=3, duplicates=True)

        self.protocol.callRemote.assert_called_with(
            communicate.SelectRange,
            start=2,
            stop=4,
            how_many=3,
            duplicates=True,
        )


class TestAPIController(unittest.TestCase):
    def setUp(self):
        self.api = api.APIController()

    def call(self, fn, *args, **kwargs):
        response = fn(*args, **kwargs)
        jsonschema.validate(response, fn.response_schema)
        return response

    def test_Game(self):
        create = self.api.lookupMethod("Game.create")
        info = self.api.lookupMethod("Game.info")
        join = self.api.lookupMethod("Game.join")
        lst = self.api.lookupMethod("Game.list")
        start = self.api.lookupMethod("Game.start")
        end = self.api.lookupMethod("Game.end")

        response = self.call(create)
        self.assertEqual(response, {"gameID" : 0})
        self.assertEqual(len(self.api.games), 1)

        response = self.call(create)
        self.assertEqual(response, {"gameID" : 1})
        self.assertEqual(len(self.api.games), 2)

        game = self.api.games[0]

        response = self.call(info, gameID=0)
        expected = {"gameID" : 0, "teams" : game.teams, "started" : False}
        self.assertEqual(response, expected)

        response = self.call(lst)
        expected = [info(gameID=0), info(gameID=1)]
        self.assertEqual(response, expected)

        response = self.call(join, gameID=0, name="Foo")
        auth = response.pop("auth")
        self.assertEqual(response, {"playerID" : 0})

        response = self.call(start, gameID=0)
        self.assertEqual(response, {})
        self.assertTrue(self.api.games[0].started)

        response = self.call(end, gameID=0)
        self.assertEqual(response, {})
        self.assertTrue(self.api.games[0].ended)

    def test_Player(self):
        gameID = self.api.lookupMethod("Game.create")()["gameID"]

        p = self.api.lookupMethod("Game.join")(gameID=gameID, name="Foo")
        playerID = p["playerID"]

        info = self.api.lookupMethod("Player.info")

        response = self.call(info, gameID=gameID, playerID=playerID)
        expected = {
            "name" : "Foo", "handSize" : 7, "life" : 20,
            "poison" : 0, "dead" : False,
        }
        self.assertEqual(response, expected)

    def test_concede(self):
        gameID = self.api.lookupMethod("Game.create")()["gameID"]
        p = self.api.lookupMethod("Game.join")(gameID=gameID, name="Foo")
        auth, playerID = p["auth"], p["playerID"]

        concede = self.api.lookupMethod("concede")

        self.assertRaises(
            api.NotAuthorized,
            concede, auth="wrong", gameID=gameID, playerID=playerID
        )
        self.assertFalse(self.api.players[0][0][1].dead)

        response = self.call(
            concede, auth=auth, gameID=gameID, playerID=playerID,
        )
        self.assertTrue(self.api.players[0][0][1].dead)
        self.assertEqual(response, {})
