#! /usr/bin/env python

from twisted.internet import defer
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory, ServerFactory
from twisted.protocols.basic import NetstringReceiver
from twisted.internet.defer import Deferred, succeed, inlineCallbacks
from shorturl_client import transformShortUrlAsync
from download_client import downloadVideoFromUrlAsync

class DownloadVideoServerProtocol(NetstringReceiver):
    """ The protocol to download a video from
    a short URL and store it locally.
    """
    
    count = 0
    
    def __init__(self, *args, **argd):
        DownloadVideoServerProtocol.count += 1
        self.__count = DownloadVideoServerProtocol.count

    def stringReceived(self, shortUrl):
        self.transport.loseConnection()
        self.downloadVideoFromShortUrlAsync(shortUrl)

    def downloadVideoFromShortUrlAsync(self, shortUrl):
        d = transformShortUrlAsync(shortUrl)

        def downloadVideoFromUrl(url):
            d = downloadVideoFromUrlAsync(url)

            def errDownloadVideoFromUrl(err):
                print "[%d] exception:" % self.__count, err
            
            d.addCallbacks(lambda v: self.storeVideo(v), errDownloadVideoFromUrl)

        def errTransformShortUrl(err):
            print "[%d] exception:" % self.__count, err
            
        d.addCallbacks(downloadVideoFromUrl, errTransformShortUrl)
        
    def storeVideo(self, video):
        print "[%d] store" % self.__count, video

class DownloadVideoServerFactory(ServerFactory):
    
    protocol = DownloadVideoServerProtocol
        

def storeVideo(video):
    print "store", video


if __name__ == '__main__':
    port = reactor.listenTCP(62222, DownloadVideoServerFactory())
    print "Download Video Server running at port", 62222
    reactor.run()
