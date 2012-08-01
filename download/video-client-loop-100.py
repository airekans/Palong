#! /usr/bin/env python

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory, ServerFactory
from twisted.protocols.basic import NetstringReceiver


class DownloadVideoClientProtocol(NetstringReceiver):
    """ The protocol used to download video.
    On client side, it just send an short URL to the server.
    The server is responsible for downloading the video.
    """
    
    def connectionMade(self):
        self.sendShortUrl()
        
    def sendShortUrl(self):
        self.sendString(self.factory.shortUrl)
        self.transport.loseConnection()

class DownloadVideoClientFactory(ClientFactory):
    
    protocol = DownloadVideoClientProtocol

    def __init__(self, shortUrl):
        self.shortUrl = shortUrl

if __name__ == '__main__':
    for i in range(100):
        reactor.connectTCP("localhost", 62222,
                           DownloadVideoClientFactory("%d%d%d" % (i, i, i)))

    reactor.run()
        
