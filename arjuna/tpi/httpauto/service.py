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

import os

from arjuna.tpi.httpauto.response import HttpResponse
from arjuna.interact.http.session import HttpSession
from .seamful.eploader import HttpEndPointLoader

class HttpService:
    '''
        HTTP Service representing SEAMful automation in Arjuna.

        Keyword Arguments:
            name: Name of service. Should have a corresponding named directory in Project root/httpauto/service directory. If not provided then the name is set to **anon** and root directory is set to Project root/httpauto.
            url: Base URL for this HTTP session. If relative path is used as a route in sender methods like `.get`, then this URL is prefixed to their provided routes.
            oauth_token: OAuth 2.0 Bearer token for this service.
            request_content_handler: Default content type handler for requests sent in this service. Overridable in individual sender methods. Default is Http.content.urlencoded.
            headers: HTTP headers to be added to request headers made by this service.
            max_redirects: Maximum number of redirects allowed for a request. Default is 30.
            auth: HTTP Authentication object: Basic/Digest.
            proxy: Proxies dict to be associated with this service.
    '''

    def __init__(self, *, name="anon", url=None, oauth_token=None, request_content_handler=None, headers=None, max_redirects=None, auth=None, proxy=None, _auto_session=True):
        self.__name = name
        self.__session = HttpSession(url=url, oauth_token=oauth_token, request_content_handler=request_content_handler, headers=headers, max_redirects=max_redirects, auth=auth, proxy=proxy, _auto_session=_auto_session)
        from arjuna import C
        if name == "anon":
            self.__root_dir = C("httpauto.dir")
        else:
            self.__root_dir = os.path.join(C("httpauto.dir"), "service/{}".format(name))
        self.__endpoints = HttpEndPointLoader(self)

    def _set_session(self, session):
        self.__session._set_session(session)

    @property
    def root_dir(self):
        return self.__root_dir

    @property
    def name(self):
        '''
            Name of service
        '''
        return self.__name

    @property
    def _session(self):
        '''
            HTTP Session object associated with this service.
        '''
        return self.__session

    @property
    def ep(self):
        '''
            Http End Point loader for this service.
        '''
        return self.__endpoints

    @property
    def message(self):
        '''
            Http Message Loader for this service using default end point.
        '''
        return self.ep._anon.message

    @property
    def action(self):
        '''
            Http Action Loader for this service using default end point.
        '''
        return self.ep._anon.action

    def send(self, msg_name=None, **fargs) -> HttpResponse:
        '''
            Send an HTTP Message using this service using default end point.
        '''
        return self.ep._anon.send(msg_name=msg_name, **fargs)
    
    def perform(self, msg_name=None, **fargs) -> HttpResponse:
        '''
            Perform an HTTP Action using this service using default end point.
        '''
        return self.ep._anon.perform(msg_name=msg_name, **fargs)

    @property
    def cookies(self) -> dict:
        '''
            All current cookie name/values in this service.
        '''
        return self._session.cookies

    @property
    def parsed_cookies(self) -> dict:
        '''
            All current cookie name and corresponding `HttpCookie` object in this service.
        '''
        return self._session.parsed_cookies

    def add_cookies(self, cookie_dict):
        '''
            Add cookies to the service.
        '''
        self._session.add_cookies(cookie_dict)

    @property
    def request_content_handler(self):
        '''
        Request content handler for content formatting.
        '''
        return self.__request_content_handler

    @property
    def headers(self):
        '''
        Request headers.
        '''
        return self._session.headers

    @property
    def auth(self):
        '''
        HTTP Authentication object.
        '''
        return self._session.auth

    @property
    def url(self):
        '''
            Base URL for this session.
        '''
        return self._session.url

    @property
    def _session(self):
        return self.__session

    @property
    def _request_headers(self):
        return self.__session._request_headers

    def get(self, route, label=None, xcodes=None, headers=None, cookies=None, allow_redirects=True, auth=None, timeout: float=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
        '''
        Sends an HTTP GET request.

        Arguments:
            route: Absolute or relative URL. If relative, then `url` of this session object is pre-fixed.

        Keyword Arguments:
            label: Label for this request. If available, it is used in reports and logs.
            xcodes: Expected HTTP response code(s).
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
        return self._session.get(route, label=label, xcodes=xcodes, headers=headers, cookies=cookies, allow_redirects=allow_redirects, auth=auth, timeout=timeout, pretty_url=pretty_url, query_params=query_params, **named_query_params)

    def head(self, route, label=None, xcodes=None, headers=None, cookies=None, allow_redirects=True, auth=None, timeout: float=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
        '''
        Sends an HTTP HEAD request.

        Arguments:
            route: Absolute or relative URL. If relative, then `url` of this session object is pre-fixed.

        Keyword Arguments:
            label: Label for this request. If available, it is used in reports and logs.
            xcodes: Expected HTTP response code(s).
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
        return self._session.head(route, label=label, xcodes=xcodes, headers=headers, cookies=cookies, allow_redirects=allow_redirects, auth=auth, timeout=timeout, pretty_url=pretty_url, query_params=query_params, **named_query_params)

    def delete(self, route, label=None, xcodes=None, headers=None, cookies=None, allow_redirects=True, auth=None, timeout: float=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
        '''
        Sends an HTTP DELETE request.

        Arguments:
            route: Absolute or relative URL. If relative, then `url` of this session object is pre-fixed.

        Keyword Arguments:
            label: Label for this request. If available, it is used in reports and logs.
            xcodes: Expected HTTP response code(s).
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
        return self._session.delete(route, label=label, xcodes=xcodes, headers=headers, cookies=cookies, allow_redirects=allow_redirects, auth=auth, timeout=timeout, pretty_url=pretty_url, query_params=query_params, **named_query_params)

    def post(self, route, *, content, label=None, xcodes=None, headers=None, cookies=None, allow_redirects=True, auth=None, timeout: float=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
        '''
        Sends an HTTP POST request.

        Arguments:
            route: Absolute or relative URL. If relative, then `url` of this session object is pre-fixed.

        Keyword Arguments:
            label: Label for this request. If available, it is used in reports and logs.
            content: Content to be sent in this HTTP request. If passed as string, then content-type set in session is used using the content request handler. It can also be a dictionary with keys - 'content' and 'type'.
            xcodes: Expected HTTP response code(s).
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
        return self._session.post(route, label=label, content=content, xcodes=xcodes, headers=headers, cookies=cookies, allow_redirects=allow_redirects, auth=auth, timeout=timeout, pretty_url=pretty_url, query_params=query_params, **named_query_params)

    def put(self, route, *, content, label=None, xcodes=None, headers=None, cookies=None, allow_redirects=True, auth=None, timeout: float=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
        '''
        Sends an HTTP PUT request.

        Arguments:
            route: Absolute or relative URL. If relative, then `url` of this session object is pre-fixed.

        Keyword Arguments:
            label: Label for this request. If available, it is used in reports and logs.
            content: Content to be sent in this HTTP request. If passed as string, then content-type set in session is used using the content request handler. It can also be a dictionary with keys - 'content' and 'type'.
            xcodes: Expected HTTP response code(s).
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
        return self._session.put(route, label=label, content=content, xcodes=xcodes, headers=headers, cookies=cookies, allow_redirects=allow_redirects, auth=auth, timeout=timeout, pretty_url=pretty_url, query_params=query_params, **named_query_params)

    def patch(self, route, *, content, label=None, xcodes=None, headers=None, cookies=None, allow_redirects=True, auth=None, timeout: float=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
        '''
        Sends an HTTP PATCH request.

        Arguments:
            route: Absolute or relative URL. If relative, then `url` of this session object is pre-fixed.

        Keyword Arguments:
            label: Label for this request. If available, it is used in reports and logs.
            content: Content to be sent in this HTTP request. If passed as string, then content-type set in session is used using the content request handler. It can also be a dictionary with keys - 'content' and 'type'.
            xcodes: Expected HTTP response code(s).
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
        return self._session.patch(route, label=label, content=content, xcodes=xcodes, headers=headers, cookies=cookies, allow_redirects=allow_redirects, auth=auth, timeout=timeout, pretty_url=pretty_url, query_params=query_params, **named_query_params)

    def options(self, route, *, content, label=None, xcodes=None, headers=None, cookies=None, allow_redirects=True, auth=None, timeout: float=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
        '''
        Sends an HTTP OPTIONS request.

        Arguments:
            route: Absolute or relative URL. If relative, then `url` of this session object is pre-fixed.

        Keyword Arguments:
            label: Label for this request. If available, it is used in reports and logs.
            content: Content to be sent in this HTTP request. If passed as string, then content-type set in session is used using the content request handler. It can also be a dictionary with keys - 'content' and 'type'.
            xcodes: Expected HTTP response code(s).
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
        return self._session.options(route, label=label, content=content, xcodes=xcodes, headers=headers, cookies=cookies, allow_redirects=allow_redirects, auth=auth, timeout=timeout, pretty_url=pretty_url, query_params=query_params, **named_query_params)
