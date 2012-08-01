#! /usr/bin/env python

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory, ServerFactory
from twisted.protocols.basic import NetstringReceiver

class ShortUrlServerProtocol(NetstringReceiver):
    """ The protocol to transform a short URL
    to its original form.
    """

    def stringReceived(self, url):
        # simulate the processing time delay
        reactor.callLater(2, lambda: self.transformShortUrl(url))

    def transformShortUrl(self, shortUrl):
        print "recv url: ", shortUrl
        self.sendString("http://www.youku.com/index.mp4")
        self.transport.loseConnection()


class ShortUrlServerFactory(ServerFactory):

    protocol = ShortUrlServerProtocol


if __name__ == '__main__':
    reactor.listenTCP(63333, ShortUrlServerFactory())
    reactor.run()
