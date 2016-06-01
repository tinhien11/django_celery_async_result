# -*- coding: utf-8 -*-
import urllib
import urllib2
import glob
import sqlite3
import os
import cookielib
import json
import time
import lxml.html

LOGIN_EMAIL = 'thanhtinpk092007@gmail.com'
LOGIN_PASSWORD = '721992'
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
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    html = opener.open(LOGIN_URL).read()
    data = parse_form(html)
    data['LoginForm[email]'] = LOGIN_EMAIL
    data['LoginForm[password]'] = LOGIN_PASSWORD
    encoded_data = urllib.urlencode(data)
    request = urllib2.Request(LOGIN_URL, encoded_data)
    response = opener.open(request)
    print response.geturl()
    return opener


def parse_form(html):
    """extract all input properties from the form
    """
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    del data['yt0']
    return data


def main():
    login_cookies()


if __name__ == '__main__':
    main()
