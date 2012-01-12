"""
This module, along with :module:`jsonrpclib`, naively implement JSON RPC.

All of the implementations I found were either resource-based or really ugly.

"""

import itertools

from twisted.internet import defer, error, protocol
from twisted.python import log
from zope.interface import implements
import jsonschema

from cardboard.frontend import jsonrpclib, network


class JSONRPC(protocol.Protocol):

    implements(network.IRPC)

    transport = None

    def __init__(self):
        self._counter = itertools.count(1)
        self._requests = {}

    def dataReceived(self, data):
        received = jsonrpclib.received(data)

        if "result" in data:
            return self._received_result(received)
        elif "error" in data:
            return self._received_error(received)
        else:
            return self._received_notify_request(received)

    def _received_result(self, response):
        d = self._requests.get(response["id"])

        if d is None:
            log.msg("Received unsolicited response: {!r}".format(response))
            return

        d.callback(response["result"])

    def _received_notify_request(self, nr):
        try:
            method = self.exposed[nr["method"]]
        except KeyError:
            log.err()
            return

        params = nr.get("params", [])
        if isinstance(params, list):
            args, kwargs = params, {}
        elif isinstance(params, dict):
            args, kwargs = (), params
        else:
            log.err(TypeError("{!r} is not a list or dict".format(params)))
            return

        id = nr.get("id")
        if id is None:
            try:
                method(*args, **kwargs)
            except:
                log.err()
            return

        defer.maybeDeferred(method, *args, **kwargs).addCallback(
            lambda result : jsonrpclib.response(id, result)
        ).addCallback(self._send)

    def _send(self, obj):
        self.transport.write(obj)

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
