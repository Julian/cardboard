from twisted.application import service, internet
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import protocol, reactor
from txjsonrpc import JSONRPCFactory

from cardboard.api import APIController


application = service.Application("Cardboard")

port = 6497
api = APIController()
factory = JSONRPCFactory(api.lookup_method)

endpoint = TCP4ServerEndpoint(reactor, port)
cardboard = internet.StreamServerEndpointService(endpoint, factory)
cardboard.setServiceParent(application)
