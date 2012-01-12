import json

from twisted.internet import defer
from twisted.test import proto_helpers
from twisted.trial import unittest
import mock

from cardboard.frontend import jsonrpc


class TestJSONRPC(unittest.TestCase):
    def setUp(self):
        self.deferred = defer.Deferred()

        exposed = {
            "foo" : lambda : setattr(self, "foo_fired", True),
            "bar" : lambda p : setattr(self, "bar_result", p ** 2),
            "baz" : lambda p, q : (q, p),
            "late" : lambda p : self.deferred,
        }

        self.frontend = mock.Mock()
        self.factory = jsonrpc.JSONRPCFactory(self.frontend, exposed)
        self.proto = self.factory.buildProtocol(("127.0.0.1", 0))
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)

    def assertSent(self, expected):
        expected["jsonrpc"] = "2.0"
        self.assertEqual(json.loads(self.tr.value()), expected)

    def test_notify(self):
        self.proto.notify("foo")
        self.assertSent({"method" : "foo", "params" : []})

        self.tr.clear()

        self.proto.notify("bar", [1, 2, "baz"])
        self.assertSent({"method" : "bar", u"params" : [1, 2, "baz"]})

    def test_request(self):
        d = self.proto.request("foo")
        self.assertSent({"id" : "1", "method" : "foo", "params" : []})

        d.addCallback(lambda r : self.assertEqual(r, [2, 3, "bar"]))

        receive = {"jsonrpc" : "2.0", "id" :  "1", "result" : [2, 3, "bar"]}
        self.proto.dataReceived(json.dumps(receive))
        return d

    def test_unsolicited_result(self):
        receive = {"jsonrpc" : "2.0", "id" :  "1", "result" : [2, 3, "bar"]}
        self.proto.dataReceived(json.dumps(receive))

    def test_received_notify(self):
        receive = {"jsonrpc" : "2.0", "method" : "foo"}
        self.proto.dataReceived(json.dumps(receive))
        self.assertTrue(self.foo_fired)

        receive = {"jsonrpc" : "2.0", "method" : "bar", "params" : [2]}
        self.proto.dataReceived(json.dumps(receive))
        self.assertEqual(self.bar_result, 4)

    def test_received_notify_no_method(self):
        receive = {"jsonrpc" : "2.0", "method" : "quux"}
        self.proto.dataReceived(json.dumps(receive))
        errors = self.flushLoggedErrors(KeyError)
        self.assertEqual(len(errors), 1)

    def test_received_notify_wrong_param_type(self):
        receive = {"jsonrpc" : "2.0", "method" : "foo", "params" : [1, 2]}
        self.proto.dataReceived(json.dumps(receive))

        receive = {"jsonrpc" : "2.0", "method" : "bar", "params" : "foo"}
        self.proto.dataReceived(json.dumps(receive))

        errors = self.flushLoggedErrors(TypeError)
        self.assertEqual(len(errors), 2)

    def test_received_request(self):
        receive = {
            "jsonrpc" : "2.0", "id" : "1", "method" : "baz", "params" : [1, 2]
        }

        self.proto.dataReceived(json.dumps(receive))
        self.assertSent({"jsonrpc" : "2.0", "id" : "1", "result" : [2, 1]})

    def test_received_request_deferred(self):
        receive = {
            "jsonrpc" : "2.0", "id" : "3",
            "method" : "late", "params" : {"p" : 3}
        }

        self.proto.dataReceived(json.dumps(receive))
        self.deferred.callback(27)
        self.assertSent({"jsonrpc" : "2.0", "id" : "3", "result" : 27})
