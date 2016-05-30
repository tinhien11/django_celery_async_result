from fshare_spider import FshareSpider
from scrapy.crawler import Crawler
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from twisted.internet import reactor


def stop_reactor():
    reactor.stop()


dispatcher.connect(stop_reactor, signal=signals.spider_closed)
crawler = Crawler(FshareSpider)
crawler.crawl()

links = reactor.run()
