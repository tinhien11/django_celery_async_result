from __future__ import unicode_literals
import urllib
import urllib2
import cookielib
import lxml.html

TRACKING_URL = 'http://www.vnpost.vn/vi-vn/dinh-vi/buu-pham?'


def normalize(html):
    tree = lxml.html.fromstring(html)

    overview = {}

    try:
        parcel_id_elm = tree.find_class('col-sm-3 package-code')[0].getchildren()
        parcel_id = parcel_id_elm[2].text_content().strip()
        overview['parcel_id'] = parcel_id

        parcel_weight_elm = tree.find_class('col-sm-4 package-weight')[0].getchildren()
        parcel_weight = parcel_weight_elm[2].text_content().strip()
        overview['parcel_weight'] = parcel_weight

        package_status_elm = tree.find_class('col-sm-4 package-location')[0].getchildren()
        parcel_status = package_status_elm[2].text_content().strip()
        overview['parcel_status'] = parcel_status

        tracking_info_elm = tree.find_class('table-tracking-info')[0].getchildren()
        country_elm = tracking_info_elm[0]
        from_country = country_elm[1].text_content()
        to_country = country_elm[3].text_content()
        overview['from_country'] = from_country
        overview['from to_country'] = to_country
    except Exception as error:
        pass

    details = []
    try:
        list_detail_event = tree.find_class('timeline-list-item')[0].getchildren()[0].getchildren()
        for e in list_detail_event:
            event_dict = {}
            list_event_elm = e.getchildren()
            event_time = list_event_elm[0].text_content()
            event_dict['event_time'] = event_time
            event_name = list_event_elm[1].text_content()
            event_dict['event_name'] = event_name
            event_localtion = list_event_elm[1].getchildren()[0].text_content()
            event_dict['event_localtion'] = event_localtion
            details.append(event_dict)
    except Exception as error:
        pass

    res = {}
    res['overview'] = overview
    res['details'] = details
    return res


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
