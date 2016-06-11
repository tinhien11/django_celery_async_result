# -*- coding: utf-8 -*-
import urllib
import urllib2
import cookielib
import lxml.html

TRACKING_URL = 'http://www.vnpost.vn/vi-vn/dinh-vi/buu-pham?'


def normalize(html):
    tree = lxml.html.fromstring(html)
    overview = {}

    packed_code = tree.find_class('col-sm-3 package-code')[0].getchildren()
    overview[packed_code[0].text_content()] = packed_code[2].text_content().strip()

    package_weight = tree.find_class('col-sm-4 package-weight')[0].getchildren()
    overview[package_weight[0].text_content()] = package_weight[2].text_content().strip()

    package_location = tree.find_class('col-sm-4 package-location')[0].getchildren()
    overview[package_location[0].text_content()] = package_location[2].text_content().strip()

    tracking_info = tree.find_class('table-tracking-info')[0].getchildren()
    overview[tracking_info[0].text_content()] = tracking_info[1].text_content()
    overview[tracking_info[1].text_content()] = tracking_info[2].text_content()


    # detail = []
    # list_detail_event = tree.find_class('timeline-list-item')[0].getchildren()[0].getchildren()
    # for e in list_detail_event:
    #     print e.text_content()

    return overview


def parse_main(parcel_id):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    html = opener.open(TRACKING_URL).read()
    data = parse_form(html)
    data['key'] = str(parcel_id).upper().strip()
    encoded_data = urllib.urlencode(data)
    request = urllib2.Request(TRACKING_URL + encoded_data)
    response = opener.open(request)
    return response.read()


def parse_form(html):
    """extract all input properties from the form
    """
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('search-input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data


if __name__ == '__main__':
    html = parse_main('EL745355158vn')
    print normalize(html)
