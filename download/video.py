#! /usr/bin/env python

from twisted.internet import defer
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.protocols.basic import NetstringReceiver

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
        self.factory.handleUrl(url)


class ShortUrlClientFactory(ClientFactory):

    protocol = ShortUrlClientProtocol

    def __init__(self, shortUrl):
        self.shortUrl = shortUrl
        self.deferred = defer.Deferred()

    def handleUrl(self, url):
        d, self.deferred = self.deferred, None
        d.callback(url)

    def clientConnectionLost(self, _, reason):
        if self.deferred is not None:
            d, self.deferred = self.deferred, None
            d.errback(reason)

    clientConnectionFailed = clientConnectionLost


def transformShortUrl(shortUrl):
    pass
    
if __name__ == '__main__':
    pass
