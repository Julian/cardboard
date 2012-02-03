from minerva import mutils
from twisted.application import service, strports
from twisted.python.filepath import FilePath
from webmagic.filecache import FileCache

from cardboard.web import site


def makeService(config):
    from twisted.internet import reactor

    multi = service.MultiService()

    domain = config['domain']
    mutils.maybeWarnAboutDomain(reactor, domain)

    closureLibrary = FilePath(config['closure-library'])
    mutils.maybeWarnAboutClosureLibrary(reactor, closureLibrary)

    socketPorts = []
    for minervaStrport in config['minerva']:
        _, _args, _ = strports.parse(minervaStrport, object())
        socketPorts.append(_args[0])

    fileCache = FileCache(lambda: reactor.seconds(), -1)
    stf, httpSite = site.setupMinerva(
        reactor, fileCache, socketPorts, domain, closureLibrary,
    )

    for httpStrport in config["minerva"]:
        httpService = strports.service(httpStrport, httpSite)
        httpService.setServiceParent(multi)

    for minervaStrport in config["minerva"]:
        minervaServer = strports.service(minervaStrport, stf)
        minervaServer.setServiceParent(multi)

    return multi
