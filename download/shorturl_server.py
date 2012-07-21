#! /usr/bin/env python

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory, ServerFactory
from twisted.protocols.basic import NetstringReceiver
import time

class ShortUrlServerProtocol(NetstringReceiver):
    """ The protocol to transform a short URL
    to its original form.
    """

    def stringReceived(self, url):
        self.sendString(self.transformShortUrl(url))
        self.transport.loseConnection()

    def transformShortUrl(self, shortUrl):
        print "recv url: ", shortUrl
        # simulate the processing time delay
        time.sleep(2)
        return "http://www.youku.com/index.mp4"


class ShortUrlServerFactory(ServerFactory):

    protocol = ShortUrlServerProtocol


if __name__ == '__main__':
    reactor.listenTCP(63333, ShortUrlServerFactory())
    reactor.run()
