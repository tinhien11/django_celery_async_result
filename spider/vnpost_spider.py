from __future__ import unicode_literals
import urllib, urllib2
import lxml
from base_spider import BaseSpider

TRACKING_URL = 'http://www.vnpost.vn/vi-vn/dinh-vi/buu-pham?'


class VnpostSpider(BaseSpider):
    tracking_url = TRACKING_URL

    def parse_main(self):
        opener = self.get_opener_cookie()
        html = opener.open(self.tracking_url).read()
        data = self.parse_form(html)
        data['key'] = str(self.parcel_id).upper().strip()
        encoded_data = urllib.urlencode(data)
        request = urllib2.Request(self.tracking_url + encoded_data)
        response = opener.open(request)
        return response.read()

    def normalize(self):

        tree = lxml.html.fromstring(self.parse_main())
        # overview = {}
        try:
            parcel_id_elm = tree.find_class('col-sm-3 package-code')[0].getchildren()
            parcel_id = parcel_id_elm[2].text_content().strip()
            # overview['parcel_id'] = parcel_id
            self.base_raw_data['info_parcel']['id'] = parcel_id

            parcel_weight_elm = tree.find_class('col-sm-4 package-weight')[0].getchildren()
            parcel_weight = parcel_weight_elm[2].text_content().strip()
            self.base_raw_data['info_parcel']['weight'] = parcel_weight

            package_status_elm = tree.find_class('col-sm-4 package-location')[0].getchildren()
            parcel_status = package_status_elm[2].text_content().strip()
            self.base_raw_data['info_parcel']['status'] = parcel_status

            tracking_info_elm = tree.find_class('table-tracking-info')[0].getchildren()
            country_elm = tracking_info_elm[0]
            from_country = country_elm[1].text_content().strip()
            to_country = country_elm[3].text_content().strip()
            self.base_raw_data['info_from']['address'] = from_country
            self.base_raw_data['info_to']['address'] = to_country
        except Exception as error:
            pass

        try:
            list_detail_event = tree.find_class('timeline-list-item')[0].getchildren()[0].getchildren()
            for e in list_detail_event:
                event_dict = {}
                list_event_elm = e.getchildren()
                event_time = list_event_elm[0].text_content().strip()
                event_dict['event_time'] = event_time
                event_name = list_event_elm[1].text.strip()
                event_dict['event_name'] = event_name
                event_localtion = list_event_elm[1].getchildren()[0].text_content().strip()
                event_dict['event_localtion'] = event_localtion
                self.base_raw_data['detail_events'].append(event_dict)
        except Exception as error:
            pass

        return self.base_raw_data


if __name__ == '__main__':
    vnpost = VnpostSpider('EL745355158vn')
    print vnpost.normalize()
