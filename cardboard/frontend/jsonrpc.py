"""
This module, along with :module:`jsonrpclib`, naively implement JSON RPC.

All of the implementations I found were either resource-based or really ugly.

"""

import itertools

from jsonschema import validate
from twisted.internet import defer, protocol
from twisted.python import failure, log
from zope.interface import implements

from cardboard.frontend import jsonrpclib, network


class JSONRPC(protocol.Protocol):

    implements(network.IRPC)

    transport = None

    def __init__(self):
        self._counter = itertools.count(1)
        self._requests = {}

    def dataReceived(self, data):
        try:
            received = jsonrpclib.loads(data)
        except jsonrpclib.ParseError:
            return self.unhandled_error(failure.Failure())

        if "result" in received or "error" in received:
            return self._received_result(received)
        else:
            return self._received_request(received)

    def _received_result(self, result):
        defer.execute(jsonrpclib.received_result, result).addCallback(
            lambda res : self._requests[res["id"]].callback(res["result"])
        ).addErrback(self.unhandled_error, id=result.get("id"))

    def _received_request(self, request):
        try:
            req = jsonrpclib.received_request(request, self.exposed)
        except:
            return self.unhandled_error(failure.Failure())

        id = request.get("id")
        d = defer.maybeDeferred(
            self.exposed[req["method"]], *req["args"], **req["kwargs"]
        )

        if id is not None:
            d.addCallback(lambda res : jsonrpclib.response(id, res))

        d.addErrback(self.unhandled_error, id=id)

        if id is not None:
            d.addCallback(self._send)

    def _send(self, obj):
        self.transport.write(obj)

    def unhandled_error(self, failure, id=None):
        log.err(
            failure,
            "An error went unhandled by the client application. "
            "Dropping connection. To avoid this, add errbacks to all remote "
            "requests and verify that valid JSON is being sent."
        )

        if self.transport is not None:
            self._send(jsonrpclib.error(id, failure))
            self.transport.loseConnection()

    def notify(self, method, parameters=()):
        self._send(jsonrpclib.notify(method, parameters))

    def request(self, method, parameters=()):
        id = str(next(self._counter))
        self._send(jsonrpclib.request(id, method, parameters))
        deferred = self._requests[id] = defer.Deferred()
        return deferred


class JSONRPCFactory(protocol.Factory):
    protocol = JSONRPC

    def __init__(self, frontend, exposed=()):
        self.exposed = dict(exposed)
        self.frontend = frontend

    def buildProtocol(self, addr):
        proto = protocol.Factory.buildProtocol(self, addr)
        proto.exposed = self.exposed
        proto.frontend = self.frontend
        proto.frontend.protocol = protocol
        return proto
