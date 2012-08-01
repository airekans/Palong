#! /usr/bin/env python

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory, ServerFactory
from twisted.protocols.basic import NetstringReceiver
import time
import socket
import struct


def getNetString(netstring):
    first_nets , sep, rest = netstring.partition(",")
    if sep == "":
        raise BaseException("invalid short url: %s" % netstring)

    num, sep, s = first_nets.partition(":")
    num = int(num)
    if sep == "":
        raise BaseException("invalid short url: %s" % netstring)

    if num != len(s):
        raise BaseException("invalid short url: %s" % netstring)

    return s
        

def transformShortUrl(shortUrl):
    if len(shortUrl) % 2 == 1:
        time.sleep(2)
        raise BaseException("invalid short url: %s" % shortUrl)

    sock = socket.socket()
    sock.connect(('localhost', 63333))
    
    data = "%d:%s," % (len(shortUrl), shortUrl)
    sock.sendall(data)

    netstring = sock.recv(1024)
    url = getNetString(netstring)
    print "recv url:", url
    return url

def downloadVideoFromUrl(url):
    time.sleep(2)
    return "video.mp4"


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
        self.downloadVideoFromShortUrl(shortUrl)

    def downloadVideoFromShortUrl(self, shortUrl):
        try:
            url = transformShortUrl(shortUrl)
            video = downloadVideoFromUrl(url)
            self.storeVideo(video)
        except BaseException, e:
            print "[%d] exception:" % self.__count, e

    def storeVideo(self, video):
        print "[%d] store" % self.__count, video


class DownloadVideoServerFactory(ServerFactory):
    
    protocol = DownloadVideoServerProtocol


if __name__ == '__main__':
    port = reactor.listenTCP(62222, DownloadVideoServerFactory())
    print "Download Video Server running at port", 62222
    reactor.run()
