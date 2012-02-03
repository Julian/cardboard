import os.path

from twisted.application import internet, service
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint

from cardboard import api
from cardboard.web import config as web_config


options = {
    "closure-library" : os.path.dirname(web_config.__file__),
    "domain" : "Cardboard",
    "enginePort" : 6497,
    "minerva" : ["tcp:6479:interface=localhost"],
    "http" : [],
    "no-tracebacks" : False,
}

application = service.Application("Cardboard")

cardboardService = service.MultiService()
cardboardService.setServiceParent(application)

engineEndpoint = TCP4ServerEndpoint(reactor, options["enginePort"])
engine = internet.StreamServerEndpointService(engineEndpoint, api.factory)
engine.setServiceParent(cardboardService)

httpService = web_config.makeService(options)
httpService.setServiceParent(cardboardService)
