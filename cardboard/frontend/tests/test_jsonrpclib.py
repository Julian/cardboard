import json
import unittest

from twisted.python import failure

from cardboard.frontend import jsonrpclib as j


class TestJSONRPCLib(unittest.TestCase):
    def test_error(self):
        self.assertEqual(
            json.loads(j.error(1, failure.Failure(j.ParseError()))),
            {"jsonrpc" : "2.0", "id" : 1,
             "error" : j.ParseError().to_response()}
        )

    def test_notify(self):
        self.assertEqual(
            json.loads(j.notify("foo")),
            {"jsonrpc" : "2.0", "method" : "foo", "params" : []}
        )

        self.assertEqual(
            json.loads(j.notify("bar", [1, 2, "foo"])),
            {"jsonrpc" : "2.0", "method" : "bar", "params" : [1, 2, "foo"]}
        )

    def test_request(self):
        self.assertEqual(
            json.loads(j.request("1", "foo")),
            {"jsonrpc" : "2.0", "id" : "1", "method" : "foo", "params" : []}
        )

        self.assertEqual(
            json.loads(j.request("2", "bar", [1, 2, "foo"])),
            {"jsonrpc" : "2.0", "id" : "2",
             "method" : "bar", "params" : [1, 2, "foo"]}
        )

    def test_loads(self):
        with self.assertRaises(j.ParseError):
            j.loads("bigboom")

        r = {"foo" : [1, 2, 3]}
        self.assertEqual(r, j.loads(json.dumps(r)))

    def test_received_request(self):
        r = {"jsonrpc" : "2.0", "id" : "1", "method": "foo"}
        self.assertEqual(
            j.received_request(r, {"foo" : next}),
            {"jsonrpc" : "2.0", "id" : "1", "method" : "foo",
             "args" : [], "kwargs" : {}},
        )

        r = {"jsonrpc" : "2.0", "id" : "2", "method": "bar", "params" : [1, 2]}
        self.assertEqual(
            j.received_request(r, {"bar" : next}),
            {"jsonrpc" : "2.0", "id" : "2", "method" : "bar",
             "params" : [1, 2], "args" : [1, 2], "kwargs" : {}},
        )

        r = {"jsonrpc" : "2.0", "id" : "3",
             "method": "quux", "params" : {"foo" : 2}}
        self.assertEqual(
            j.received_request(r, {"quux" : next}),
            {"jsonrpc" : "2.0", "id" : "3", "method" : "quux",
             "params" : {"foo" : 2}, "args" : [], "kwargs" : {"foo" : 2}},
        )

        with self.assertRaises(j.InvalidParams):
            r = {"jsonrpc" : "2.0", "id" : "4", "method": "qu", "params" : 2}
            j.received_request(r, {"qu" : next})

    def test_received_response(self):
        r = {"jsonrpc" : "2.0", "id" : "1", "result": [1, 2, 3]}
        self.assertEqual(j.received_result(r), r)

    def test_received_result_invalid_properties(self):
        for invalid in [
            # missing
            {"result" : [], "id" : "1"},
            {"jsonrpc" : "2.0", "id" : "1"},
            {"jsonrpc" : "2.0", "result" : []},
            {"jsonrpc" : "2.0"},
            {"result" : []},
            {"id" : "1"},

            # invalid
            {"jsonrpc" : "other", "result" : [], "error" : {}, "id" : "1"},
        ]:
            with self.assertRaises(j.InvalidRequest):
                j.received_result(json.dumps(invalid))

    def test_received_error(self):
        r = {"jsonrpc" : "2.0", "id" : "1"}

        for err in j.PROTOCOL_ERRORS.itervalues():
            r["error"] = err().to_response()

            with self.assertRaises(err):
                j.received_result(r)

        # ServerError
        r["error"] = j.ServerError(code=-32007).to_response()
        with self.assertRaises(j.ServerError) as err:
            j.received_result(r)

        o = {"bar" : 2, "quux" : 4}
        r["error"] = {"code" : "-32098", "message" : "Server err", "data" : o}
        with self.assertRaises(j.ServerError) as err:
            j.received_result(r)

        self.assertEqual(err.exception.data, o)

        o = {"quux" : 4}
        r["error"] = {"code" : "-29", "message" : "Foo blew up", "data" : o}
        with self.assertRaises(j.ApplicationError) as err:
            j.received_result(r)

        self.assertEqual(err.exception.data, o)
        self.assertEqual(err.exception.message, "Foo blew up")
        self.assertEqual(err.exception.code, -29)

    def test_received_error_invalid(self):
        r = {"jsonrpc" : "2.0", "id" : "1"}

        for invalid in [
            # missing
            {},
            {"code" : -32000},
            {"code" : -32000, "data" : {}},
            {"message" : "foo"},
            {"message" : "foo", "data" : {}},

            # invalid
            {"code" : "foo", "message" : "foo"},
            24,
        ]:

            with self.assertRaises(j.InvalidResponse):
                r["error"] = invalid
                j.received_result(r)
