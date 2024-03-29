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
import os
from requests import Session
from arjuna.tpi.error import HttpUnexpectedStatusCodeError, HttpSendError, HttpConnectError
from requests.exceptions import ConnectionError, TooManyRedirects, ProxyError, InvalidProxyURL
import time

from arjuna.tpi.httpauto.request import _HttpRequest
from arjuna.tpi.httpauto.response import HttpResponse
from arjuna.tpi.httpauto.cookie import HttpCookie
from arjuna.tpi.helper.arjtype import NotSet


class HttpSession:
    '''
        Create an HTTP Session. Does automatic cookie management.

        Keyword Arguments:
            url: Base URL for this HTTP session. If relative path is used as a route in sender methods like `.get`, then this URL is prefixed to their provided routes.
            oauth_token: OAuth 2.0 Bearer token for this session.
            request_content_handler: Default content type handler for requests sent in this session. Overridable in individual sender methods. Default is Http.content.urlencoded.
            headers: HTTP headers to be added to request headers made by this session.
            max_redirects: Maximum number of redirects allowed for a request. Default is 30.
            auth: HTTP Authentication object: Basic/Digest.
            proxy: Proxies dict to be associated with this session.
    '''

    def __init__(self, *, url=None, oauth_token=None, request_content_handler=None, headers=None, max_redirects=None, auth=None, proxy=None, _auto_session=True):
        self.__url = url is not None and url.strip() or None
        self.__request_content_handler = request_content_handler
        from arjuna.tpi.httpauto.http import Http
        if self.__request_content_handler is None:
            self.__request_content_handler = Http.content.urlencoded
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
            else:
                from arjuna import C, Http
                if C("http.proxy.enabled"):
                    self.__session.proxies = Http.proxy(C('http.proxy.host'), C('http.proxy.port'))

        if oauth_token:
            self.__session.headers['Authorization'] = f'Bearer {oauth_token}'

    @property
    def cookies(self) -> dict:
        '''
            All current cookie name/values in this session object.
        '''
        return self.__session.cookies.get_dict()

    @property
    def parsed_cookies(self) -> dict:
        '''
            All current cookie name and corresponding `HttpCookie` object in this session object.
        '''
        return {cookie.name:HttpCookie(self, cookie) for cookie in self._session.cookies}

    def add_cookies(self, cookie_dict):
        '''
            Add cookies to the session.
        '''
        self.__session.cookies.update(cookie_dict)

    @property
    def request_content_handler(self):
        '''
        Request content handler for content formatting.
        '''
        return self.__request_content_handler

    def _set_session(self, session):
        self.__session = session
        if self.__provided_headers is not None:
            self.__session.headers.update(self.__provided_headers)
        from arjuna.tpi.httpauto.http import Http
        if self.request_content_handler != Http.content.custom:
            self.__session.headers['Content-Type'] = Http.content.get_content_type(self.request_content_handler)

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
            if self.url is None:
                raise Exception("As Base URL is not set for this Service/Session, you must provide absolute URLs for all request methods.")
            if route.startswith("/"):
                return self.url + route
            else:
                return self.url + "/" + route

    def __register_network_info(self, request, response):
        from arjuna import Arjuna
        from arjuna.tpi.helper.arjtype import NetworkPacketInfo
        # Should be configurable
        sub_network_packets = []
        for redir_resp in response.redir_history:
            redir_req = redir_resp.request
            sub_network_packets.append(
                NetworkPacketInfo(
                    label="Sub-Request: {} {}".format(redir_req.method, redir_req.url), 
                    request=str(redir_req), 
                    response=str(redir_resp),
                    sub_network_packets=tuple()
                )
            )

        # The request for last response object was the last request and hence the last redirection.
        if response.redir_history:
            # last_req = response.last_request
            # if not last_req:
            last_req = response.request
            sub_network_packets.append(
                                NetworkPacketInfo(
                                    label="Sub-Request: {} {}".format(last_req.method, last_req.url), 
                                    request=str(last_req), 
                                    response=str(response),
                                    sub_network_packets=tuple()
                                )
                            )                

        Arjuna.get_report_metadata().add_network_packet_info(
            NetworkPacketInfo(label=request.label, request=str(request), response=str(response), sub_network_packets=tuple(sub_network_packets))
        )

    def _validate_status_code(cls, response, codes, *, expected=True):
        if expected:
            if response.status_code not in codes:
                raise HttpUnexpectedStatusCodeError(response.request, response, msg=f"Expected code(s): {codes}")
        else:
            if response.status_code in codes:
                raise HttpUnexpectedStatusCodeError(response.request, response, msg=f"Unexpected code(s): {codes}")


    def _send(self, request) -> HttpResponse:
        '''
            Send the provided HttpRequest to server.

            In case of ConnectionError, retries the connection 5 times at a gap of 1 second. Currently, not configurable.

            Returns
                `HttpResponse` object. In case of redirections, this is the last HttpResponse object, which encapsulates all redirections which can be retrieved from it.
        '''
        from arjuna import Arjuna, log_info, C
        from arjuna.tpi.helper.arjtype import NetworkPacketInfo
        log_info(request.label)
        max_connection_retries = 5
        try:
            counter = 0
            exc_flag = False
            exc_desc = None
            while counter < max_connection_retries:
                counter += 1
                try:
                    timeout = C("socket.timeout")
                    if request.timeout is not None:
                        timeout = request.timeout
                    if self._session.proxies:
                        response = HttpResponse(self, self._session.send(request._request, allow_redirects=request.allow_redirects, timeout=timeout, proxies=self._session.proxies, verify=False))
                    else:
                        response = HttpResponse(self, self._session.send(request._request, allow_redirects=request.allow_redirects, timeout=timeout))
                except (ProxyError, InvalidProxyURL) as e:
                    raise HttpConnectError(request, "There is an error in connecting to the configured proxy. Proxy settings: {}. Error: {}".format(self.__session.proxies, str(e)))
                except ConnectionError as f:
                    exc_flag = True
                    exc_desc = str(f)
                    time.sleep(1)
                    continue
                else:
                    break
            if exc_flag:
                raise HttpConnectError(request, "Connection error despite trying 5 times. Error: {}".format(exc_desc))
        except TooManyRedirects as e:
            response = HttpResponse(self._session, e.response)
            self.__register_network_info(request, response)
            raise HttpSendError(self, response, str(e) + ". Error redir URL: " + e.response.url)
        except Exception as e:
            import traceback
            response = "Error in sending the request\n"
            response += e.__class__.__name__ + ":" + str(e) + "\n"
            response += traceback.format_exc()
            Arjuna.get_report_metadata().add_network_packet_info(
                NetworkPacketInfo(label=request.label, request=str(request), response=str(response), sub_network_packets=tuple())
            )
            raise e
        else:
            self.__register_network_info(request, response)
            if request.xcodes is not None:
                self._validate_status_code(response, request.xcodes)
            return response


    def get(self, route, label=None, xcodes=None, headers=None, cookies=None, allow_redirects=True, auth=None, timeout: float=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
        request = _HttpRequest(self, self.__route(route), method="get", label=label, xcodes=xcodes, headers=headers, cookies=cookies, allow_redirects=allow_redirects, auth=auth, timeout=timeout, pretty_url=pretty_url, query_params=query_params, **named_query_params)
        return self._send(request)


    def head(self, route, label=None, xcodes=None, headers=None, cookies=None, allow_redirects=True, auth=None, timeout: float=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
        request = _HttpRequest(self, self.__route(route), method="head", label=label, xcodes=xcodes, headers=headers, cookies=cookies, allow_redirects=allow_redirects, auth=auth, timeout=timeout, pretty_url=pretty_url, query_params=query_params, **named_query_params)
        return self._send(request)


    def delete(self, route, label=None, xcodes=None, headers=None, cookies=None, allow_redirects=True, auth=None, timeout: float=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
        request = _HttpRequest(self, self.__route(route), method="delete", label=label, xcodes=xcodes, headers=headers, cookies=cookies, allow_redirects=allow_redirects, auth=auth, timeout=timeout, pretty_url=pretty_url, query_params=query_params, **named_query_params)
        return self._send(request)

    def post(self, route, *, content=NotSet(), label=None, xcodes=None, headers=None, cookies=None, allow_redirects=True, auth=None, timeout: float=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
        request = _HttpRequest(self, self.__route(route), method="post", label=label, content=content, xcodes=xcodes, headers=headers, cookies=cookies, allow_redirects=allow_redirects, auth=auth, timeout=timeout, pretty_url=pretty_url, query_params=query_params, **named_query_params)
        return self._send(request)

    def put(self, route, *, content=NotSet(), label=None, xcodes=None, headers=None, cookies=None, allow_redirects=True, auth=None, timeout: float=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
        request = _HttpRequest(self, self.__route(route), method="put", label=label, content=content, xcodes=xcodes, headers=headers, cookies=cookies, allow_redirects=allow_redirects, auth=auth, timeout=timeout, pretty_url=pretty_url, query_params=query_params, **named_query_params)
        return self._send(request)

    def patch(self, route, *, content=NotSet(), label=None, xcodes=None, headers=None, cookies=None, allow_redirects=True, auth=None, timeout: float=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
        request = _HttpRequest(self, self.__route(route), method="patch", label=label, content=content, xcodes=xcodes, headers=headers, cookies=cookies, allow_redirects=allow_redirects, auth=auth, timeout=timeout, pretty_url=pretty_url, query_params=query_params, **named_query_params)
        return self._send(request)

    def options(self, route, *, label=None, xcodes=None, headers=None, cookies=None, allow_redirects=True, auth=None, timeout: float=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
        request = _HttpRequest(self, self.__route(route), method="options", label=label, content=content, xcodes=xcodes, headers=headers, cookies=cookies, allow_redirects=allow_redirects, auth=auth, timeout=timeout, pretty_url=pretty_url, query_params=query_params, **named_query_params)
        return self._send(request)



