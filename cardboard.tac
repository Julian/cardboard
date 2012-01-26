from twisted.application import service, internet
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import protocol, reactor
from txjsonrpc import JSONRPCFactory


application = service.Application("Cardboard")

port = 6497
endpoint = TCP4ServerEndpoint(reactor, port)
cardboard = internet.StreamServerEndpointService(endpoint, JSONRPCFactory())
cardboard.setServiceParent(application)
