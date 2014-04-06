# -*- coding: utf-8 -*-
"""
.. module: helpers
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""
import urllib2
import json


class Info(object):
    def __init__(self, data):
        self.data = data

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        return getattr(self.data, item, None)


class Client(object):
    def __init__(self):
        self._response = None
        self._info = None

    def request(self, url, data=None):
        self._response = None
        self._info = None
        opener = urllib2.Request(url, data)
        self._response = urllib2.urlopen(opener)
        self._response_data = self._response.read()

    @property
    def info(self):
        if self._info is None:
            if self._response is None:
                self._info = Info({})
            else:
                self._info = Info(self._response.info())
        return self._info

    @property
    def mimetype(self):
        return self.info.type

    @property
    def response(self):
        resp = self._response_data
        if self.info.subtype == 'json':
            return json.loads(resp)

        return resp

    def status(self):
        return self._response.getcode()
