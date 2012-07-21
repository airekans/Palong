#! /usr/bin/env python

from twisted.internet import defer
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.protocols.basic import NetstringReceiver
from twisted.internet.defer import Deferred, succeed, inlineCallbacks


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


def getShortUrl():
    try:
        return raw_input('url: ')
    except EOFError:
        return None

SHORTURL_HOST = "localhost"
SHORTURL_PORT = 63333
    
def transformShortUrlAsync(shortUrl):
    d = defer.Deferred()
    reactor.connectTCP(SHORTURL_HOST, SHORTURL_PORT,
                       ShortUrlClientFactory(shortUrl, d))
    return d

def downloadVideoFromUrlAsync(url):
    # similate the latency to download the whole video files
    d = defer.Deferred()
    reactor.callLater(2, lambda: d.callback("video file"))
    return d

def storeVideo(video):
    pass

@inlineCallbacks
def downloadVideoFromShortUrl(shortUrl):
    url = yield transformShortUrlAsync(shortUrl)
    print "long url:", url
    video = yield downloadVideoFromUrlAsync(url)
    print "video file:", video
    storeVideo(video)

def startDownloadService():
    while True:
        shortUrl = getShortUrl()
        if shortUrl is None:
            break

        downloadVideoFromShortUrl(shortUrl)

if __name__ == '__main__':
    startDownloadService()
    reactor.run()
