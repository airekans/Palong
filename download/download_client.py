from twisted.internet import reactor
from twisted.internet.defer import Deferred


def downloadVideoFromUrlAsync(url):
    # similate the latency to download the whole video files
    d = Deferred()
    if len(url) % 2 == 1:
        reactor.callLater(2, lambda: d.errback(BaseException("invalid url: %s" % url)))
    else:
        reactor.callLater(2, lambda: d.callback("video.mp4"))
    return d
    