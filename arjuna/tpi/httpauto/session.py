# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

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
from requests import Request, Session
from arjuna.tpi.error import HttpUnexpectedStatusCodeError, HttpSendError
from arjuna.tpi.parser.json import Json
from arjuna.tpi.parser.html import Html
from arjuna.tpi.engine.asserter import AsserterMixIn
from requests.exceptions import ConnectionError, TooManyRedirects
import time

from .request import _HttpRequest
from .response import HttpResponse


class HttpSession:
    '''
        Create an HTTP Session. Does automatic cookie management.

        Keyword Arguments:
            url: Base URL for this HTTP session. If relative path is used as a route in sender methods like `.get`, then this URL is prefixed to their provided routes.
            oauth_token: OAuth 2.0 Bearer token for this session.
            content_type: Default content type for requests sent in this session. Overridable in individual sender methods. Default is `application/x-www-form-urlencoded`
            headers: HTTP headers to be added to request headers made by this session.
            max_redirects: Maximum number of redirects allowed for a request. Default is 30.
            auth: HTTP Authentication object: Basic/Digest.
            proxy: Proxies dict to be associated with this session.
    '''

    def __init__(self, *, url=None, oauth_token=None, content_type='application/x-www-form-urlencoded', headers=None, max_redirects=None, auth=None, proxy=None, _auto_session=True):
        self.__url = url is not None and url.strip() or None
        self.__content_type = content_type
        self.__session = None
        self.__provided_headers = headers
        if _auto_session:
            self._set_session(Session())
            if max_redirects is not None:
                self.__session.max_redirects = max_redirects
            if auth is not None:
                self.__session.auth = auth
            if proxy is not None:
                self.__session.proxies = proxy
        if oauth_token:
            self.__session.headers['Authorization'] = f'Bearer {oauth_token}'

    @property
    def cookies(self) -> dict:
        '''
            All current cookies in this session object.
        '''
        return self.__session.cookies.get_dict()

    def add_cookies(self, cookie_dict):
        '''
            Add cookies to the session.
        '''
        self.__session.cookies.update(cookie_dict)

    def _set_session(self, session):
        self.__session = session
        if self.__provided_headers is not None:
            self.__session.headers.update(self.__session.headers)
        self.__session.headers['Content-Type'] = self.__content_type

    @property
    def url(self):
        '''
            Base URL for this session.
        '''
        return self.__url

    @property
    def _session(self):
        return self.__session

    @property
    def _request_headers(self):
        return self.__session.headers

    def __route(self, route):
        route = route.strip()
        if route.lower().startswith("http"):
            return route
        else:
            if route.startswith("/"):
                return self.url + route
            else:
                return self.url + "/" + route

    def get(self, route, label=None, xcodes=None, strict=False, headers=None, cookies=None, allow_redirects=True, auth=None, timeout: float=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
        '''
        Sends an HTTP GET request.

        Arguments:
            route: Absolute or relative URL. If relative, then `url` of this session object is pre-fixed.

        Keyword Arguments:
            label: Label for this request. If available, it is used in reports and logs.
            xcodes: Expected HTTP response code(s).
            strict: If True in case of unexpected status code, an AssertionError is raised, else HttpUnexpectedStatusCodeError is raised.
            headers: Mapping of additional HTTP headers to be sent with this request.
            cookies: Python dict of cookies to send with request.
            allow_redirects: If True, redirections are allowed for the HTTP message. Default is True.
            auth: HTTP Authentication object: Basic/Digest.
            timeout: How long to wait for the server to send data before giving up.
            pretty_url: If True, the query params are formatted using pretty URL format instead of usual query string which is the default.
            query_params: A mapping of key-values to be included in query string.
            **named_query_params: Arbitrary key/value pairs. These are appended to the query string of URL for this request.

        Note:
            **query_params** and **named_query_params** have the same goal.
            In case of duplicates, named_query_params override query_params.
        '''
        request = _HttpRequest(self._session, self.__route(route), method="get", label=label, xcodes=xcodes, strict=strict, headers=headers, cookies=cookies, allow_redirects=allow_redirects, auth=auth, timeout=timeout, pretty_url=pretty_url, query_params=query_params, **named_query_params)
        return request.send()


    def head(self, route, label=None, xcodes=None, strict=False, headers=None, cookies=None, allow_redirects=True, auth=None, timeout: float=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
        '''
        Sends an HTTP HEAD request.

        Arguments:
            route: Absolute or relative URL. If relative, then `url` of this session object is pre-fixed.

        Keyword Arguments:
            label: Label for this request. If available, it is used in reports and logs.
            xcodes: Expected HTTP response code(s).
            strict: If True in case of unexpected status code, an AssertionError is raised, else HttpUnexpectedStatusCodeError is raised.
            headers: Mapping of additional HTTP headers to be sent with this request.
            cookies: Python dict of cookies to send with request.
            allow_redirects: If True, redirections are allowed for the HTTP message. Default is True.
            auth: HTTP Authentication object: Basic/Digest.
            timeout: How long to wait for the server to send data before giving up.
            pretty_url: If True, the query params are formatted using pretty URL format instead of usual query string which is the default.
            query_params: A mapping of key-values to be included in query string.
            **named_query_params: Arbitrary key/value pairs. These are appended to the query string of URL for this request.

        Note:
            **query_params** and **named_query_params** have the same goal.
            In case of duplicates, named_query_params override query_params.
        '''
        request = _HttpRequest(self._session, self.__route(route), method="head", label=label, xcodes=xcodes, strict=strict, headers=headers, cookies=cookies, allow_redirects=allow_redirects, auth=auth, timeout=timeout, pretty_url=pretty_url, query_params=query_params, **named_query_params)
        return request.send()


    def delete(self, route, label=None, xcodes=None, strict=False, headers=None, cookies=None, allow_redirects=True, auth=None, timeout: float=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
        '''
        Sends an HTTP DELETE request.

        Arguments:
            route: Absolute or relative URL. If relative, then `url` of this session object is pre-fixed.

        Keyword Arguments:
            label: Label for this request. If available, it is used in reports and logs.
            xcodes: Expected HTTP response code(s).
            strict: If True in case of unexpected status code, an AssertionError is raised, else HttpUnexpectedStatusCodeError is raised.
            headers: Mapping of additional HTTP headers to be sent with this request.
            cookies: Python dict of cookies to send with request.
            allow_redirects: If True, redirections are allowed for the HTTP message. Default is True.
            auth: HTTP Authentication object: Basic/Digest.
            timeout: How long to wait for the server to send data before giving up.
            pretty_url: If True, the query params are formatted using pretty URL format instead of usual query string which is the default.
            query_params: A mapping of key-values to be included in query string.
            **named_query_params: Arbitrary key/value pairs. These are appended to the query string of URL for this request.

        Note:
            **query_params** and **named_query_params** have the same goal.
            In case of duplicates, named_query_params override query_params.
        '''
        request = _HttpRequest(self._session, self.__route(route), method="delete", label=label, xcodes=xcodes, strict=strict, headers=headers, cookies=cookies, allow_redirects=allow_redirects, auth=auth, timeout=timeout, pretty_url=pretty_url, query_params=query_params, **named_query_params)
        return request.send()

    def post(self, route, *, content, label=None, content_type=None, xcodes=None, strict=False, headers=None, cookies=None, allow_redirects=True, auth=None, timeout: float=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
        '''
        Sends an HTTP POST request.

        Arguments:
            route: Absolute or relative URL. If relative, then `url` of this session object is pre-fixed.

        Keyword Arguments:
            label: Label for this request. If available, it is used in reports and logs.
            content: Content to be sent in this HTTP request.
            content-type: Content type. If not provided, default content type set for this session is used. Default is `application/x-www-form-urlencoded`
            xcodes: Expected HTTP response code(s).
            strict: If True in case of unexpected status code, an AssertionError is raised, else HttpUnexpectedStatusCodeError is raised.
            headers: Mapping of additional HTTP headers to be sent with this request.
            cookies: Python dict of cookies to send with request.
            allow_redirects: If True, redirections are allowed for the HTTP message. Default is True.
            auth: HTTP Authentication object: Basic/Digest.
            timeout: How long to wait for the server to send data before giving up.
            pretty_url: If True, the query params are formatted using pretty URL format instead of usual query string which is the default.
            query_params: A mapping of key-values to be included in query string.
            **named_query_params: Arbitrary key/value pairs. These are appended to the query string of URL for this request.

        Note:
            **query_params** and **named_query_params** have the same goal.
            In case of duplicates, named_query_params override query_params.
        '''
        request = _HttpRequest(self._session, self.__route(route), method="post", label=label, content=content, content_type=content_type, xcodes=xcodes, strict=strict, headers=headers, cookies=cookies, allow_redirects=allow_redirects, auth=auth, timeout=timeout, pretty_url=pretty_url, query_params=query_params, **named_query_params)
        return request.send()

    def put(self, route, *, content, label=None, content_type=None, xcodes=None, strict=False, headers=None, cookies=None, allow_redirects=True, auth=None, timeout: float=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
        '''
        Sends an HTTP PUT request.

        Arguments:
            route: Absolute or relative URL. If relative, then `url` of this session object is pre-fixed.

        Keyword Arguments:
            label: Label for this request. If available, it is used in reports and logs.
            content: Content to be sent in this HTTP request.
            content-type: Content type. If not provided, default content type set for this session is used. Default is `application/x-www-form-urlencoded`
            xcodes: Expected HTTP response code(s).
            strict: If True in case of unexpected status code, an AssertionError is raised, else HttpUnexpectedStatusCodeError is raised.
            headers: Mapping of additional HTTP headers to be sent with this request.
            cookies: Python dict of cookies to send with request.
            allow_redirects: If True, redirections are allowed for the HTTP message. Default is True.
            auth: HTTP Authentication object: Basic/Digest.
            timeout: How long to wait for the server to send data before giving up.
            pretty_url: If True, the query params are formatted using pretty URL format instead of usual query string which is the default.
            query_params: A mapping of key-values to be included in query string.
            **named_query_params: Arbitrary key/value pairs. These are appended to the query string of URL for this request.

        Note:
            **query_params** and **named_query_params** have the same goal.
            In case of duplicates, named_query_params override query_params.
        '''
        request = _HttpRequest(self._session, self.__route(route), method="put", label=label, content=content, content_type=content_type, xcodes=xcodes, strict=strict, headers=headers, cookies=cookies, allow_redirects=allow_redirects, auth=auth, timeout=timeout, pretty_url=pretty_url, query_params=query_params, **named_query_params)
        return request.send()

    def patch(self, route, *, content, label=None, content_type=None, xcodes=None, strict=False, headers=None, cookies=None, allow_redirects=True, auth=None, timeout: float=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
        '''
        Sends an HTTP PUT request.

        Arguments:
            route: Absolute or relative URL. If relative, then `url` of this session object is pre-fixed.

        Keyword Arguments:
            label: Label for this request. If available, it is used in reports and logs.
            content: Content to be sent in this HTTP request.
            content-type: Content type. If not provided, default content type set for this session is used. Default is `application/x-www-form-urlencoded`
            xcodes: Expected HTTP response code(s).
            strict: If True in case of unexpected status code, an AssertionError is raised, else HttpUnexpectedStatusCodeError is raised.
            headers: Mapping of additional HTTP headers to be sent with this request.
            cookies: Python dict of cookies to send with request.
            allow_redirects: If True, redirections are allowed for the HTTP message. Default is True.
            auth: HTTP Authentication object: Basic/Digest.
            timeout: How long to wait for the server to send data before giving up.
            pretty_url: If True, the query params are formatted using pretty URL format instead of usual query string which is the default.
            query_params: A mapping of key-values to be included in query string.
            **named_query_params: Arbitrary key/value pairs. These are appended to the query string of URL for this request.

        Note:
            **query_params** and **named_query_params** have the same goal.
            In case of duplicates, named_query_params override query_params.
        '''
        request = _HttpRequest(self._session, self.__route(route), method="patch", label=label, content=content, content_type=content_type, xcodes=xcodes, strict=strict, headers=headers, cookies=cookies, allow_redirects=allow_redirects, auth=auth, timeout=timeout, pretty_url=pretty_url, query_params=query_params, **named_query_params)
        return request.send()

    def options(self, route, *, content, label=None, content_type=None, xcodes=None, strict=False, headers=None, cookies=None, allow_redirects=True, auth=None, timeout: float=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
        '''
        Sends an HTTP PUT request.

        Arguments:
            route: Absolute or relative URL. If relative, then `url` of this session object is pre-fixed.

        Keyword Arguments:
            label: Label for this request. If available, it is used in reports and logs.
            content: Content to be sent in this HTTP request.
            content-type: Content type. If not provided, default content type set for this session is used. Default is `application/x-www-form-urlencoded`
            xcodes: Expected HTTP response code(s).
            strict: If True in case of unexpected status code, an AssertionError is raised, else HttpUnexpectedStatusCodeError is raised.
            headers: Mapping of additional HTTP headers to be sent with this request.
            cookies: Python dict of cookies to send with request.
            allow_redirects: If True, redirections are allowed for the HTTP message. Default is True.
            auth: HTTP Authentication object: Basic/Digest.
            timeout: How long to wait for the server to send data before giving up.
            pretty_url: If True, the query params are formatted using pretty URL format instead of usual query string which is the default.
            query_params: A mapping of key-values to be included in query string.
            **named_query_params: Arbitrary key/value pairs. These are appended to the query string of URL for this request.

        Note:
            **query_params** and **named_query_params** have the same goal.
            In case of duplicates, named_query_params override query_params.
        '''
        request = _HttpRequest(self._session, self.__route(route), method="options", label=label, content=content, content_type=content_type, xcodes=xcodes, strict=strict, headers=headers, cookies=cookies, allow_redirects=allow_redirects, auth=auth, timeout=timeout, pretty_url=pretty_url, query_params=query_params, **named_query_params)
        return request.send()



