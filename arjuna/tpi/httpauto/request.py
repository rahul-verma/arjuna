# This file is a part of Arjuna
# Copyright 2015-2021 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import abc
from urllib.parse import urlparse, urlencode, parse_qs, quote
from requests import Request
from arjuna.tpi.error import HttpRequestCreationError
from arjuna.tpi.parser.json import Json, JsonDict, JsonList
from arjuna.tpi.parser.html import Html
from arjuna.tpi.data.entity import _DataEntity
from arjuna.tpi.engine.asserter import AsserterMixIn
import time

from .packet import HttpPacket
from .response import HttpResponse

class HttpRequest(HttpPacket):
    '''
        Encapsulates HTTP request packet.

        Arguments:
            session: `HttpSession` object which created this `HttpRequest`.
            request: `requests` library's Request object wrapped by this class.

        Keyword Arguments:
            label: Label for this request. If available, it is used in Reports and logs.
            xcodes: Expected Status Code(s)
            allow_redirects: If True, redirections are allowed for the HTTP message. Default is True.
            timeout: How long to wait for the server to send data before giving up.
            cookies: Cookie dictionary
    '''

    def __init__(self, session, request, label=None, xcodes=None, allow_redirects=True, timeout=None, cookies=None):
        super().__init__(request)
        self.__session = session
        self.__request = request
        req_repr = "{} {}".format(self.method, self.url)
        self.__label = label and label or req_repr
        printable_label = label and self.__label + "::" + req_repr or req_repr
        printable_label = len(printable_label) > 119 and printable_label[:125] + "<SNIP>" or printable_label
        self.__label = printable_label
        self.__allow_redirects = allow_redirects
        self.__timeout = timeout
        self.__cookies = cookies

    @property
    def _request(self):
        return self.__request

    @property
    def allow_redirects(self):
        '''
        True if redirects are allowed for this request.
        '''
        return self.__allow_redirects

    @property
    def timeout(self):
        '''
        Timeout for this request.
        '''
        return self.__timeout

    @property
    def label(self) -> str:
        '''
            Label for this request object.
        '''
        return self.__label

    @property
    def query_params(self) -> dict:
        '''
            URL Query Parameters for this request object.
        '''
        return parse_qs(self.url)

    @property
    def url(self) -> str:
        '''
            URL correspnding to this request message.
        '''
        return self.__request.url

    @property
    def method(self) -> str:
        '''
            HTTP Method/Verb used by this request.
        '''
        return self.__request.method

    @property
    def xcodes(self) -> set:
        '''
        Expected status codes for this request.
        '''
        return self.__xcodes

    @property
    def text(self):
        '''
            Content of this request message as Text object.
        '''
        from arjuna.tpi.parser.text import Text
        return Text(self.content)

    @property
    def content(self):
        '''
            Content of this request message as plain unformatted text.
        '''
        return self.__request.body

    __OUT ='''{}
{}{}'''

    @classmethod
    def repr_as_str(cls, *, method, url, headers, content=None):
        if content:
            content = '\n\n{}\n'.format(content)
        else:
            content = ""
        return cls.__OUT.format(
            method + ' ' + url,
            '\n'.join('{}: {}'.format(k, v) for k, v in headers.items()),
            content
        ).strip()

    def __str__(self):
        content = self.content
        if isinstance(content, bytes):
            content = content.decode()
        return self.repr_as_str(
            method = self.__request.method,
            url = self.url,
            headers = self.__request.headers,
            content = content
        )


class _HttpRequest(HttpRequest):

    def __init__(self, session, url, method, label=None, content=None, xcodes=None, headers=None, cookies=None, allow_redirects=True, auth=None, timeout=None, pretty_url=False, query_params=None, **named_query_params):
        self.__session = session
        self.__method = method.upper()
        self.__url = url
        self.__content = None
        if content is not None:
            if type(content) in {str, dict, list, tuple} or isinstance(content, JsonDict) or isinstance(content, JsonList) or isinstance(content, _DataEntity):
                self.__content = self.__session.request_content_handler(content)
            else:
                self.__content = content
        self.__xcodes = None
        if xcodes is not None:
            self.__xcodes = self._process_codes(xcodes)
        self.__query_params = query_params
        if self.__query_params is None:
            self.__query_params = dict()
        self.__query_params.update(named_query_params)
        self.__pretty_url = pretty_url
        self.__headers = {}
        self.__headers.update(session.headers)
        if headers:
            self.__headers.update(headers)
        self.__cookies = dict()
        self.__cookies.update(self.__session.cookies)
        if cookies is not None:
            self.__cookies.update(cookies)
        self.__auth = auth is not None and auth or self.__session.auth
        self.__prepare_headers()
        self.__req = self.__build_request()
        super().__init__(self.__session, self.__req, label=label, xcodes=self.__xcodes, allow_redirects=allow_redirects, timeout=timeout, cookies=self.__cookies)

    @classmethod
    def _process_codes(cls, codes):
        return type(codes) in {set, list, tuple} and codes or {int(codes)}

    def __prepare_headers(self):
        if self.__method in {'POST', 'PUT', 'PATCH', 'OPTIONS'}:
            self.__headers['Content-Type'] = self.__content.type
        if self.__method in {'GET', 'HEAD', 'DELETE'}:
            if 'Content-Type' in self.__headers:
                del self.__headers['Content-Type']

    def __build_request(self):
        parsed_uri = urlparse(self.__url)
        #self.__headers['Host'] = parsed_uri.netloc
        if self.__pretty_url:
            query = "/".join([quote(f"{k}/{v}") for k,v in self.__query_params.items()])
            url = self.__url + query
            query_params = None
        else:
            url = self.__url
            query_params = self.__query_params

        try:
            if self.__content:
                data = self.__content.content
            else:
                data = None
            req = Request(self.__method, url, data=data, headers=self.__headers, params=query_params, cookies=self.__cookies, auth=self.__auth)
            return req.prepare()
        except Exception as e:
            raise HttpRequestCreationError("{} : {}".format(e.__class__.__name__, str(e)))

