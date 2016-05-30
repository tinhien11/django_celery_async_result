from fshare_spider import FshareSpider
from scrapy.crawler import Crawler
from scrapy import signals
from twisted.internet import reactor


def stop_reactor():
    reactor.stop()

def add_item(item):
    print item
    return item

crawler = Crawler(FshareSpider)
crawler.crawl()
crawler.signals.connect(stop_reactor, signal=signals.spider_closed)
crawler.signals.connect(add_item, signals.item_passed)
links = reactor.run()

