import json

from twisted.internet import defer
from twisted.python import failure
from twisted.test import proto_helpers
from twisted.trial import unittest
import mock

from cardboard.frontend import jsonrpc, jsonrpclib


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
        """
        notify() sends a valid JSON RPC notification.

        """

        self.proto.notify("foo")
        self.assertSent({"method" : "foo", "params" : []})

        self.tr.clear()

        self.proto.notify("bar", [1, 2, "baz"])
        self.assertSent({"method" : "bar", u"params" : [1, 2, "baz"]})

    def test_request(self):
        """
        request() sends a valid JSON RPC request and returns a deferred.

        """

        d = self.proto.request("foo")
        self.assertSent({"id" : "1", "method" : "foo", "params" : []})

        d.addCallback(lambda r : self.assertEqual(r, [2, 3, "bar"]))

        receive = {"jsonrpc" : "2.0", "id" :  "1", "result" : [2, 3, "bar"]}
        self.proto.dataReceived(json.dumps(receive))
        return d

    def test_unhandled_error(self):
        """
        An unhandled error gets logged and disconnects the transport.

        """

        v = failure.Failure(ValueError("Hey a value error"))
        self.proto.unhandled_error(v)
        self.assertTrue(self.tr.disconnecting)

        errors = self.flushLoggedErrors(ValueError)
        self.assertEqual(errors, [v])

    def test_invalid_json(self):
        """
        Invalid JSON causes a JSON RPC ParseError and disconnects.

        """

        self.proto.dataReceived("[1,2,")
        self.assertTrue(self.tr.disconnecting)

        err = {"id" : None, "error" : jsonrpclib.ParseError().to_response()}
        self.assertSent(err)

        errors = self.flushLoggedErrors(jsonrpclib.ParseError)
        self.assertEqual(len(errors), 1)

    def test_invalid_request(self):
        """
        An invalid request causes a JSON RPC InvalidRequest and disconnects.

        """

        self.proto.dataReceived(json.dumps({"id" : 12}))
        self.assertTrue(self.tr.disconnecting)

        err = jsonrpclib.InvalidRequest({"reason" : "jsonrpc"})
        self.assertSent({"id" : None, "error" : err.to_response()})

        errors = self.flushLoggedErrors(jsonrpclib.InvalidRequest)
        self.assertEqual(len(errors), 1)

    def test_unsolicited_result(self):
        """
        An incoming result for an id that does not exist raises an error.

        """

        receive = {"jsonrpc" : "2.0", "id" :  "1", "result" : [2, 3, "bar"]}
        self.proto.dataReceived(json.dumps(receive))

        self.assertTrue(self.tr.disconnecting)

        err = jsonrpclib.InternalError({
            "exception" : "KeyError", "message" : "u'1'",
        })
        expect = {"jsonrpc" : "2.0", "id" : "1", "error" : err.to_response()}
        sent = json.loads(self.tr.value())
        tb = sent["error"]["data"].pop("traceback")

        self.assertEqual(sent, expect)
        self.assertTrue(tb)

        # TODO: Raises original exception. Do we want InternalError instead?
        errors = self.flushLoggedErrors(KeyError)
        self.assertEqual(len(errors), 1)

    def test_error_result(self):
        for id, error in enumerate(jsonrpclib.PROTOCOL_ERRORS.itervalues(), 1):
            d = self.proto.request("foo")
            d.addErrback(lambda fail : self.assertEqual(fail.type, error))

            receive = {"jsonrpc" : "2.0", "id" : str(id), "error" : {}}
            receive["error"] = {"code" : error.code, "message" : error.message}
            self.proto.dataReceived(json.dumps(receive))

            errors = self.flushLoggedErrors(error)
            self.assertEqual(len(errors), 1)

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
        errors = self.flushLoggedErrors(jsonrpclib.MethodNotFound)
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

    def test_received_request_no_method(self):
        receive = {"jsonrpc" : "2.0", "id" : "3", "method" : "quux"}
        self.proto.dataReceived(json.dumps(receive))
        errors = self.flushLoggedErrors(jsonrpclib.MethodNotFound)
        self.assertEqual(len(errors), 1)

        sent = json.loads(self.tr.value())
        self.assertIn("error", sent)
        self.assertEqual(sent["error"]["code"], jsonrpclib.MethodNotFound.code)

    def test_received_request_error(self):
        receive = {
            "jsonrpc" : "2.0", "id" : "1", "method" : "foo", "params" : [1, 2]
        }
        self.proto.dataReceived(json.dumps(receive))

        response = json.loads(self.tr.value())

        self.assertNotIn("result", response)
        self.assertEqual(response["id"], "1")
        self.assertEqual(response["error"]["data"]["exception"], "TypeError")
        self.assertTrue(response["error"]["data"]["traceback"])

        errors = self.flushLoggedErrors(TypeError)
        self.assertEqual(len(errors), 1)
