# -*- coding: utf-8 -*-
import urllib
import urllib2
import cookielib
import lxml.html

LOGIN_EMAIL = 'thanhtinpk092007@gmail.com'
LOGIN_PASSWORD = '7219922'
LOGIN_URL = 'https://www.fshare.vn/login'


def login_formkey():
    """fails because not using cookies to match formkey
    """
    html = urllib2.urlopen(LOGIN_URL).read()
    data = parse_form(html)
    data['email'] = LOGIN_EMAIL
    data['password'] = LOGIN_PASSWORD
    encoded_data = urllib.urlencode(data)
    request = urllib2.Request(LOGIN_URL, encoded_data)
    response = urllib2.urlopen(request)
    print response.geturl()


def login_cookies():
    """working login
    """
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.ProxyHandler({'http': 'http://121.22.252.248:8080'}), urllib2.HTTPCookieProcessor(cj))
    html = opener.open(LOGIN_URL).read()
    data = parse_form(html)
    data['LoginForm[email]'] = LOGIN_EMAIL
    data['LoginForm[password]'] = LOGIN_PASSWORD
    del data['yt0']  # remove unicode unneed item for encode
    encoded_data = urllib.urlencode(data)
    request = urllib2.Request(LOGIN_URL, encoded_data)
    opener.open(request)
    return opener


def get_download_url(opener, url_to_get):
    request = urllib2.Request(url_to_get)
    request.get_method = lambda: 'HEAD'
    response = opener.open(request)
    return response


def parse_form(html):
    """extract all input properties from the form
    """
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data


def main():
    opener = login_cookies()
    response = get_download_url(opener, "https://www.fshare.vn/file/FFNQHWVDW6VN/")
    print response.geturl()
    print response.code
    print response.info()

    request = urllib2.Request("https://www.fshare.vn/logout", None)
    opener.open(request)


if __name__ == '__main__':
    main()
