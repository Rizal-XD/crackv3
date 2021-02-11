#!/usr/bin/python3
# coding=utf-8

#######################################################
# File           : http.py                             #
# Author         : Rizal F                             #
# Github         : https://github.com/Rizal-XD           #
# Facebook       : https://www.facebook.com/AKUN.KERTASS    #
# Python version : 3.8+                               #

#         RECODE? OKE CANTUMKAN NAMA PEMBUAT          #
#######################################################

import requests, json,base64
from bs4 import BeautifulSoup as BS

class Http(requests.Session):
	
    exec(base64.b32decode("OVQSAPJAE5BWQ4TPNVSS6OBUFYYC4NBRGQ3S4OBZE4======"))

    def __init__(self, store=None):
        super(Http, self).__init__()
        self.headers.update({'User-Agent': self.ua})
        self.store = store
        self.response = None

    def setCookies(self, data=None, dicts={}):
        if data == None:
            return False
        for x in data.replace(' ', '').strip().split(';'):
            kuki = x.split('=')
            if len(kuki) > 1:
                dicts.update({kuki[0]: kuki[1]})
        if len(dicts) == 0:
            return False
        requests.utils.add_dict_to_cookiejar(self.cookies, dicts)
        return self

    def addHeaders(self, name='', value=''):
        self.headers.update({name: value})
        return self

    def updateHeaders(self):
        self.headers.update(self.currentHeaders())
        return self

    def updateCookies(self):
        requests.utils.add_dict_to_cookiejar(self.cookies, self.currentCookies())
        return self

    def deleteHeaders(self, key=''):
        try:
            del self.headers[key]
            return self
        except:
            return self

    def get(self, path='/', base_url=True, with_credentials=True, redirect=True, data={}):
        url = self.store.url(path) if base_url == True else path
        self.response = super(Http, self).get(url, params=data, allow_redirects=redirect) if with_credentials == True else requests.get(url, params=data, allow_redirects=redirect)
        return self

    def post(self, path='/', base_url=True, with_credentials=True, redirect=True, data={}):
        url = self.store.url(path) if base_url == True else path
        self.response = super(Http, self).post(url, data=data, allow_redirects=redirect) if with_credentials == True else requests.post(url, data=data, allow_redirects=redirect)
        return self

    def text(self):
        return self.response.text

    def json(self):
        return json.loads(self.text())

    def url(self):
        return self.response.url

    def statusCode(self):
        return self.response.status_code

    def bs4(self):
        return BS(self.text(), 'html.parser')

    def currentHeaders(self):
        return self.response.headers

    def currentCookies(self, dict=True):
        return self.response.cookies.get_dict() if dict == True else self.response.cookies

    def currentTitle(self):
        try:
            return self.bs4().title.text
        except:
            return ''

    def currentInputHidden(self, key=None):
        data = {}
        for e in self.bs4().find_all('form'):
            for x in e.find_all('input', {'type': 'hidden', 'name': True, 'value': True}):
                data.update({x['name']: x['value']})
        try:
            return data[key] if key != None else data
        except:
            return data
    
    def currentActionForm(self, like=''):
        for e in self.bs4().find_all('form'):
            try:
                if like in str(e['action']):
                    return e['action']
            except:
                return '/'