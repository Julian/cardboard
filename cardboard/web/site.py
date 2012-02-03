import textwrap

from minerva.mserver import ServerTransportFactory, StreamTracker, WebPort
from webmagic.untwist import (
    BetterFile, BetterResource, CookieInstaller, ResponseCacheOptions,
    ConnectionTrackingSite,
)

from cardboard import api


class CardboardStreamFactory(object):
    def __init__(self, engineFactory=api.factory):
        self.engineFactory = engineFactory

    def buildProtocol(self):
        protocol = CardboardStreamProtocol()
        protocol.engine = self.engineFactory.buildProtocol()
        protocol.factory = self
        return protocol


class CardboardStreamProtocol(object):
    def stringReceived(self, string):
        self.engine.stringReceived(string)


class CardboardRoot(BetterResource):
    def __init__(
        self, webPort, fileCache, mainSocketPort, domain, closureLibrary
    ):

        BetterResource.__init__(self)


def setupMinerva(reactor, fileCache, socketPorts, domain, closureLibrary):
    toPorts = ",".join(str(p) for p in socketPorts)

    policyString = textwrap.dedent("""
        <cross-domain-policy>
            <allow-access-from domain="{domain}" to-ports="{toPorts}"/>
            <allow-access-from domain="*.{domain}" to-ports="{toPorts}"/>
        </cross-domain-policy>
        """).strip().format(domain=domain, toPorts=toPorts)

    tracker = StreamTracker(reactor, CardboardStreamFactory())

    allowedDomains = []
    if domain:
        allowedDomains.append(domain)

    webPort = WebPort(reactor, tracker, fileCache, allowedDomains)
    stf = ServerTransportFactory(reactor, tracker, policyString=policyString)

    mainSocketPort = socketPorts[0] if socketPorts else None
    root = CardboardRoot(
        webPort, fileCache, mainSocketPort, domain, closureLibrary
    )

    site = ConnectionTrackingSite(root, timeout=75)
    return stf, site
