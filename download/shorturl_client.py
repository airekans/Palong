from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import NetstringReceiver
from twisted.internet.defer import Deferred


class ShortUrlClientProtocol(NetstringReceiver):
    """ The protocol to transform a short URL
    to its original form.
    """

    def connectionMade(self):
        self.sendRequest(self.factory.shortUrl)

    def sendRequest(self, shortUrl):
        self.sendString(shortUrl)

    def stringReceived(self, url):
        self.transport.loseConnection()
        self.urlReceived(url)

    def urlReceived(self, url):
        print "recv url:", url
        self.factory.handleUrl(url)


class ShortUrlClientFactory(ClientFactory):

    protocol = ShortUrlClientProtocol

    def __init__(self, shortUrl, deferred):
        self.shortUrl = shortUrl
        self.deferred = deferred

    def handleUrl(self, url):
        d, self.deferred = self.deferred, None
        d.callback(url)

    def clientConnectionLost(self, _, reason):
        if self.deferred is not None:
            d, self.deferred = self.deferred, None
            d.errback(reason)
        #reactor.stop()

    clientConnectionFailed = clientConnectionLost


SHORTURL_HOST = "localhost"
SHORTURL_PORT = 63333
    
def transformShortUrlAsync(shortUrl):
    d = Deferred()

    if len(shortUrl) % 2 == 1:
        reactor.callLater(2, lambda: d.errback(BaseException("invalid short url: %s" % shortUrl)))
    else:
        reactor.connectTCP(SHORTURL_HOST, SHORTURL_PORT,
                           ShortUrlClientFactory(shortUrl, d))
    return d



