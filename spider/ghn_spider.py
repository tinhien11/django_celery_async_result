from __future__ import unicode_literals
import urllib, urllib2
import lxml
from base_spider import BaseSpider

TRACKING_URL = 'https://5sao.ghn.vn/Tracking/ViewTracking/'


class GHNSpider(BaseSpider):
    tracking_url = TRACKING_URL

    def parse_main(self):
        opener = self.get_opener_cookie()
        request = urllib2.Request(self.tracking_url + self.parcel_id)
        response = opener.open(request)
        return response.read()


if __name__ == '__main__':
    ghn = GHNSpider('MPDS-321351882-8472')
    print ghn.parse_main()
    print ghn.normalize()
