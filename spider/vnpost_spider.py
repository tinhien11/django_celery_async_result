from __future__ import unicode_literals
import urllib
import urllib2
import cookielib
import lxml.html

TRACKING_URL = 'http://www.vnpost.vn/vi-vn/dinh-vi/buu-pham?'


def normalize(html):
    tree = lxml.html.fromstring(html)
    overview = {}

    parcel_id_elm = tree.find_class('col-sm-3 package-code')[0].getchildren()
    parcel_id = parcel_id_elm[2].text_content().strip()
    overview['parcel_id'] = parcel_id

    parcel_weight_elm = tree.find_class('col-sm-4 package-weight')[0].getchildren()
    parcel_weight = parcel_weight_elm[2].text_content().strip()
    overview['parcel_weight'] = parcel_weight

    package_status_elm = tree.find_class('col-sm-4 package-location')[0].getchildren()
    parcel_status = package_status_elm[2].text_content().strip()
    overview['parcel_status'] = parcel_status


    #
    # tracking_info = tree.find_class('table-tracking-info')[0].getchildren()
    # overview[tracking_info[0].text_content()] = tracking_info[1].text_content()
    # overview[tracking_info[1].text_content()] = tracking_info[2].text_content()



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
