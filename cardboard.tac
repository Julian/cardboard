from twisted.application import service, internet
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import protocol, reactor
from twisted.protocols import amp


application = service.Application("Cardboard")

port = 6497
endpoint = TCP4ServerEndpoint(reactor, port)
factory = protocol.Factory()
factory.protocol = amp.AMP

cardboard = internet.StreamServerEndpointService(endpoint, factory)
cardboard.setServiceParent(application)
