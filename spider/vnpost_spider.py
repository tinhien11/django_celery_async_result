# -*- coding: utf-8 -*-
import urllib
import urllib2
import cookielib
import lxml.html

TRACKING_URL = 'http://www.vnpost.vn/vi-vn/dinh-vi/buu-pham?'


def parse_main(parcel_id):
    """working login
    """
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
    result_html = parse_main('EL745355158vn')
    print result_html
