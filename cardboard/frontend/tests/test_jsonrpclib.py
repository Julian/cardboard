import json
import unittest

from cardboard.frontend import jsonrpclib as j


class TestJSONRPCLib(unittest.TestCase):
    def test_error(self):
        self.assertEqual(
            json.loads(j.error(1, j.ParseError())),
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

    def assertInvalid(self, req):
        with self.assertRaises(j.InvalidRequest):
            j.received(req)

    def test_received(self):
        r = {"jsonrpc" : "2.0", "id" : "1", "result": [1, 2, 3]}
        self.assertEqual(r, j.received(json.dumps(r)))

        with self.assertRaises(j.ParseError):
            j.received("bigboom")

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
                j.received(json.dumps(invalid))
