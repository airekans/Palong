#! /usr/bin/env python

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory, ServerFactory
from twisted.protocols.basic import NetstringReceiver
import time
import socket
import struct


def transformShortUrl(shortUrl):
    sock = socket.socket()
    sock.connect(('localhost', 63333))
    
    # data = struct.pack('!i', len(shortUrl))
    # data += ":" + shortUrl + ","
    data = "%d:%s," % (len(shortUrl), shortUrl)
    print "send data:", data
    sock.sendall(data)

    url = sock.recv(1024)
    print "recv url:", url
    return url

def downloadVideoFromUrl(url):
    time.sleep(2)
    return "video.mp4"


class DownloadVideoServerProtocol(NetstringReceiver):
    """ The protocol to download a video from
    a short URL and store it locally.
    """

    def stringReceived(self, shortUrl):
        self.transport.loseConnection()
        self.downloadVideoFromShortUrl(shortUrl)

    def downloadVideoFromShortUrl(self, shortUrl):
        try:
            url = transformShortUrl(shortUrl)
            video = downloadVideoFromUrl(url)
            storeVideo(video)
        except BaseException, e:
            print "exception:", e


class DownloadVideoServerFactory(ServerFactory):
    
    protocol = DownloadVideoServerProtocol

    
def storeVideo(video):
    print "store", video


if __name__ == '__main__':
    port = reactor.listenTCP(62222, DownloadVideoServerFactory())
    print "Download Video Server running at port", 62222
    reactor.run()
