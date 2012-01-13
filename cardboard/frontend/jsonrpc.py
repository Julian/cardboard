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
        id, args, kwargs = nr.get("id"), nr["args"], nr["kwargs"]
        method = self.exposed.get(nr["method"])
        is_notification = id is None

        if method is None:
            err = jsonrpclib.MethodNotFound(nr["method"])
            log.err(err)

            if is_notification:
                return
            else:
                return self._send(jsonrpclib.error(id, err))

        if is_notification:
            try:
                method(*args, **kwargs)
            except:
                log.err()
            return

        def errback(failure):
            log.err(failure)
            return jsonrpclib.error(id, jsonrpclib.InternalError({
                "exception" : failure.type.__name__,
                "traceback" : failure.getTraceback()
            }))

        defer.maybeDeferred(method, *args, **kwargs).addCallbacks(
            lambda result : jsonrpclib.response(id, result), errback
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
