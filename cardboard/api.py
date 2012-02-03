import functools
import json
import uuid

import jsonschema
import panglery
import txjsonrpc

from cardboard import core
from cardboard.util import ANY


class NotAuthorized(Exception):
    """
    The user was not authorized to call an API method.

    """

    def __str__(self):
        return "Authorization failed or was not provided."


class User(object):
    """
    A user is an enraged animal sitting across the network.

    If you truly wish to interact with one, be my guest.

    """


    def event_triggered(self, **event):
        pass

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
        self,
        zone=None,
        match_cards=ANY,
        how_many_cards=1,
        duplicate_cards=False,
        match_players=ANY,
        how_many_players=1,
        duplicate_players=False,
        bad=True,
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


def document_schema(schema, type, indent=0):
    """
    Document a schema for a JSON RPC object of the given type.

    :argument schema: a JSON Schema
    :argument type: the type of object that the schema validates
    :type type: "request", "response" or "notification"
    :argument indent: an indent level to move the schema string over
    :type indent: integer
    :rtype: a str in the Sphinx markup language

    """

    if type not in {"request", "response", "notification"}:
        raise ValueError(type)

    ind = (indent + 4) * " "
    schema = ind + json.dumps(schema, sort_keys=True, indent=4)
    schema = schema.replace("\n", "\n" + ind)
    return indent * " " + ".. {}::\n\n{}".format(type, schema)


def exposed(request_schema, response_schema, validate=jsonschema.validate):
    """
    Document and validate an exposed API method.

    :argument request_schema: a schema to use to validate the incoming request
    :argument response_schema: a schema used only to document the response
                               object that will be sent back

    """

    def _expose(fn):
        if not fn.__doc__:
            raise ValueError(
                "Get off your lazy ass and write some documentation!"
            )
        else:
            for indent, c in enumerate(fn.__doc__.lstrip("\n")):
                if c != " ":
                    break

            req_doc = document_schema(request_schema, "request", indent)
            res_doc = document_schema(response_schema, "response", indent)
            fn.__doc__  = "\n\n".join([fn.__doc__.rstrip(), req_doc, res_doc])

        # TODO: Document schema["properties"] too

        @functools.wraps(fn)
        def exposed_fn(self, **request):
            validate(request, request_schema)
            return fn(self, **request)

        exposed_fn.request_schema = request_schema
        exposed_fn.response_schema = response_schema
        return exposed_fn
    return _expose


class APIController(object):
    def __init__(self):
        self.drafts = []
        self.games = []
        self.players = []

    def lookupMethod(self, name):
        """
        Lookup the appropriate API method with the given name.

        """

        return getattr(self, "api_" + name.replace(".", "_"))

    @exposed(
        {
         "type" : "object",
         "properties" : {
             "auth" : {"type" : "string", "required" : True},
             "gameID" : {"type" : "integer", "required" : True},
             "playerID" : {"type" : "integer", "required" : True},
         },
         "additionalProperties" : False,
        },
        {
         "type" : "object",
         "properties" : {
         },
         "additionalProperties" : False,
        },
    )
    def api_concede(self, auth, gameID, playerID):
        """
        Concede from the current game.

        """

        expected_auth, player = self.players[gameID][playerID]
        if auth != expected_auth:
            raise NotAuthorized()
        player.concede()
        return {}

    @exposed(
        {
         "type" : "object",
         "properties" : {
             "gameID" : {"type" : "integer", "required" : True},
             "verbose" : {"type" : "boolean", "default" : False},
         },
         "additionalProperties" : False,
        },
        {
         "type" : "object",
         "properties" : {
             "gameID" : {"type" : "integer", "required" : True},
             "started" : {"type" : "boolean", "required" : True},
             "teams" : {"required" : True},
         },
         "additionalProperties" : False,
        },
    )
    def api_Game_info(self, gameID, verbose=False):
        """
        Retrieve game info about a specific game.

        """

        # XXX: verbose
        game = self.games[gameID]
        return {
            "gameID" : gameID, "started" : game.started, "teams" : game.teams,
        }

    @exposed(
        {
         "type" : "object",
         "properties" : {
         },
         "additionalProperties" : False,
        },
        {
         "type" : "array",
        },
    )
    def api_Game_list(self, verbose=False):
        """
        List the currently open games.

        """

        info = self.lookupMethod("Game.info")
        return [
            info(gameID=i, verbose=verbose) for i in xrange(len(self.games))
        ]


    @exposed(
        {
         "type" : "object",
         "additionalProperties" : False,
        },
        {
         "type" : "object",
         "properties" : {"gameID" : {"type" : "integer", "required" : True}}
        },
    )
    def api_Game_create(self):
        """
        Create a new game.

        """

        self.games.append(core.Game(panglery.Pangler()))
        self.players.append([])
        return {"gameID" : len(self.games) - 1}


    @exposed(
        {
         "type" : "object",
         "properties" : {
             "gameID" : {"type" : "integer", "required" : True},
         },
         "additionalProperties" : False,
        },
        {
         "type" : "object",
         "properties" : {
         },
         "additionalProperties" : False,
        },
    )
    def api_Game_start(self, gameID):
        """
        Start a game.

        """

        # XXX: Unknown game, not authorized
        self.games[gameID].start()
        return {}

    @exposed(
        {
         "type" : "object",
         "properties" : {
             "gameID" : {"type" : "integer", "required" : True},
             "name" : {"type" : "string", "required" : True},
         },
         "additionalProperties" : False,
        },
        {
         "type" : "object",
         "properties" : {
             "auth" : {"type" : "string", "required" : True},
             "playerID" : {"type" : "integer", "required" : True},
         },
         "additionalProperties" : False,
        },
    )
    def api_Game_join(self, gameID, name):
        """
        Join a currently open game.

        """

        # XXX: Can't join a started game, can't join twice, library
        game, players = self.games[gameID], self.players[gameID]
        player = game.add_player(library=[], user=User(), name=name)
        auth = uuid.uuid4().bytes
        players.append((auth, player))
        return {"playerID" : len(players) - 1, "auth" : auth}

    @exposed(
        {
         "type" : "object",
         "properties" : {
             "gameID" : {"type" : "integer", "required" : True},
         },
         "additionalProperties" : False,
        },
        {
         "type" : "object",
         "properties" : {
         },
         "additionalProperties" : False,
        },
    )
    def api_Game_end(self, gameID):
        """
        End the current game.

        """

        self.games[gameID].end()
        return {}


    @exposed({}, {})
    def api_Draft_info(self):
        """
        Retrieve game info about a specific draft.

        """

        pass


    @exposed({}, {})
    def api_Draft_list(self):
        """
        List the currently open drafts.

        """

        pass


    @exposed({}, {})
    def api_Draft_create(self):
        """
        Create a new draft.

        """

        pass


    @exposed({}, {})
    def api_Draft_start(self):
        """
        Start a draft.

        """

        pass


    @exposed({}, {})
    def api_Draft_join(self):
        """
        Join a currently open draft.

        """

        pass


    @exposed({}, {})
    def api_Draft_end(self):
        """
        End the current draft.

        """

        pass

    @exposed(
        {
         "type" : "object",
         "properties" : {
             "gameID" : {"type" : "integer", "required" : True},
             "playerID" : {"type" : "integer", "required" : True},
         },
         "additionalProperties" : False,
        },
        {
         "type" : "object",
         "properties" : {
             "name" : {"type" : "string", "required" : True},
             "dead" : {"type" : "boolean", "required" : True},
             "handSize" : {"type" : "integer", "required" : True},
             "life" : {"type" : "integer", "required" : True},
             "poison" : {
                 "type" : "integer", "required" : True,
                 "minimum" : 0, "maximum" : 10,
             },
         },
         "additionalProperties" : False,
        },
    )
    def api_Player_info(self, gameID, playerID):
        """
        Retrieve info about a given player.

        """

        # XXX: No such player
        player = self.players[gameID][playerID][1]
        return {
            "name" : player.name, "handSize" : player.hand_size,
            "life" : player.life, "poison" : player.poison,
            "dead" : player.dead,
        }


controller = APIController()
factory = txjsonrpc.JSONRPCFactory(controller.lookupMethod)
