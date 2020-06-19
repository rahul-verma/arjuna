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
from arjuna.tpi.error import HttpUnexpectedStatusCodeError, HttpSendError, HttpConnectError, HttpRequestCreationError
from arjuna.tpi.parser.json import Json
from arjuna.tpi.parser.html import Html
from arjuna.tpi.engine.asserter import AsserterMixIn
from requests.exceptions import ConnectionError, TooManyRedirects, ProxyError, InvalidProxyURL
import time

from .message import HttpMessage
from .response import HttpResponse

class HttpRequest(HttpMessage):
    '''
        Encapsulates HTTP response message.

        Arguments:
            session: `HttpSession` object which created this `HttpRequest`.
            request: `requests` library's Request object wrapped by this class.

        Keyword Arguments:
            label: Label for this request. If available, it is used in Reports and logs.
            xcodes: Expected Status Code(s)
            strict: If True in case of unexpected status code, an AssertionError is raised, else HttpUnexpectedStatusCodeError is raised.
            allow_redirects: If True, redirections are allowed for the HTTP message. Default is True.
    '''

    def __init__(self, session, request, label=None, xcodes=None, strict=False, allow_redirects=True, timeout=None):
        super().__init__(request)
        self.__session = session
        self.__request = request
        req_repr = "{} {}".format(self.method, self.url)
        self.__label = label and label or req_repr
        self.__printable_label = label and self.__label + "::" + req_repr or req_repr
        self.__printable_label = len(self.__printable_label) > 119 and self.__printable_label[:125] + "<SNIP>" or self.__printable_label
        self.__strict = strict
        self.__allow_redirects = allow_redirects
        self.__timeout = timeout

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

    def __register_network_info(self, response):
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
            NetworkPacketInfo(label=self.label, request=str(self), response=str(response), sub_network_packets=tuple(sub_network_packets))
        )

    def send(self) -> HttpResponse:
        '''
            Send this request to server.

            In case of ConnectionError, retries the connection 5 times at a gap of 1 second. Currently, not configurable.

            Returns
                `HttpResponse` object. In case of redirections, this is the last HttpResponse object, which encapsulates all redirections which can be retrieved from it.
        '''
        from arjuna import Arjuna, log_info
        from arjuna.tpi.helper.arjtype import NetworkPacketInfo
        log_info(self.__printable_label)
        max_connection_retries = 5
        try:
            counter = 0
            exc_flag = False
            while counter < max_connection_retries:
                counter += 1
                try:
                    response = HttpResponse(self.__session, self.__session.send(self.__req, allow_redirects=self.__allow_redirects, timeout=self.__timeout, proxies=self.__session.proxies))
                except (ProxyError, InvalidProxyURL) as e:
                    raise HttpConnectError(self.__req, "There is an error in connecting to the configured proxy. Proxy settings: {}. Error: {}".format(self.__session.proxies, str(e)))
                except ConnectionError:
                    exc_flag = True
                    time.sleep(1)
                    continue
                else:
                    break
            if exc_flag:
                raise HttpConnectError(self.__req, "Connection error despite trying 5 times.")
        except TooManyRedirects as e:
            response = HttpResponse(self.__session, e.response)
            self.__register_network_info(response)
            raise HttpSendError(self, response, str(e) + ". Error redir URL: " + e.response.url)
        except Exception as e:
            import traceback
            response = "Error in sending the request\n"
            response += e.__class__.__name__ + ":" + str(e) + "\n"
            response += traceback.format_exc()
            Arjuna.get_report_metadata().add_network_packet_info(
                NetworkPacketInfo(label=self.label, request=str(self), response=str(response), sub_network_packets=tuple())
            )
            raise e
        else:
            self.__register_network_info(response)
            if self.__xcodes is not None and response.status_code not in self.__xcodes:
                if self.__strict:
                    raise AssertionError(f"HTTP status code {self.status_code} is not expected. Expected: {self.__xcodes}")
                else:
                    raise HttpUnexpectedStatusCodeError(self.__req, response)
            return response

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
    def text(self):
        '''
            Content of this request message as plain text.
        '''
        return self.__request.body

    content = text

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
        return self.repr_as_str(
            method = self.__request.method,
            url = self.url,
            headers = self.__request.headers,
            content = self.text
        )


class _HttpRequest(HttpRequest):

    def __init__(self, session, url, method, label=None, content=None, content_type=None, xcodes=None, strict=False, headers=None, cookies=None, allow_redirects=True, auth=None, timeout=None, pretty_url=False, query_params=None, **named_query_params):
        self.__session = session
        self.__method = method.upper()
        self.__url = url
        self.__content = content
        self.__prep_content = content
        self.__content_type = content_type
        self.__xcodes = None
        if xcodes is not None:
            self.__xcodes = type(xcodes) in {set, list, tuple} and xcodes or {xcodes}
        self.__query_params = query_params
        if self.__query_params is None:
            self.__query_params = dict()
        self.__query_params.update(named_query_params)
        self.__pretty_url = pretty_url
        self.__headers = {}
        self.__headers.update(session.headers)
        if headers:
            self.__headers.update(headers)
        self.__cookies = cookies
        self.__auth = auth is not None and auth or self.__session.auth
        self.__prepare_headers()
        self.__prepare_content()
        self.__req = self.__build_request()
        super().__init__(self.__session, self.__req, label=label, xcodes=self.__xcodes, strict=strict, allow_redirects=allow_redirects, timeout=timeout)

    def __prepare_headers(self):
        if self.__method in {'POST', 'PUT', 'PATCH', 'OPTIONS'}:
            if self.__content_type is not None:
                self.__headers['Content-Type'] = self.__content_type
        if self.__method in {'GET', 'HEAD', 'DELETE'}:
            if 'Content-Type' in self.__headers:
                del self.__headers['Content-Type']

    def __prepare_content(self):
        if self.__method in {'GET', 'DELETE', 'HEAD'}: return
        if self.__headers['Content-Type'].lower() == 'application/json':
            self.__prep_content = json.dumps(self.__content, indent=2)
        elif self.__headers['Content-Type'].lower() == 'text/html':
            self.__prep_content = self.__content
        else:
            self.__prep_content = urlencode(self.__content)

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
        cookie_dict = dict()
        cookie_dict.update(self.__session.cookies)
        if self.__cookies is not None:
            cookie_dict.update(self.__cookies)
        try:
            req = Request(self.__method, url, data=self.__prep_content, headers=self.__headers, params=query_params, cookies=cookie_dict, auth=self.__auth)
            return req.prepare()
        except Exception as e:
            raise HttpRequestCreationError("{} : {}".format(e.__class__.__name__, str(e)))

