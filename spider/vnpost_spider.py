from __future__ import unicode_literals
from base_spider import BaseSpider

TRACKING_URL = 'http://www.vnpost.vn/vi-vn/dinh-vi/buu-pham?'


class VnpostSpider(BaseSpider):
    tracking_url = TRACKING_URL


if __name__ == '__main__':
    vnpost = VnpostSpider('EL745355158vn')
    print vnpost.normalize()
