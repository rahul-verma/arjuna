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

class HttpMessage(AsserterMixIn, metaclass=abc.ABCMeta):

    def __init__(self, http_msg):
        super().__init__()
        self.__http_msg = http_msg

    @property
    def headers(self) -> dict:
        ''' 
            HTTP Headers for this message.
        '''
        return self.__http_msg.headers

    def assert_empty_content(self, *, msg):
        '''
            Validates if content is empty.

            Keyword Arguments:
                msg: A context string explaining why this assertion was done.
        '''
        if self.headers['Content-Length'] != '0':
            raise AssertionError("Content is not empty.")

    def assert_non_empty_content(self, *, msg):
        '''
            Validates if content is empty.

            Keyword Arguments:
                msg: A context string explaining why this assertion was done.
        '''
        if self.headers['Content-Length'] == '0':
            raise AssertionError("Content is empty.")

    def assert_header_match(self, header, value=None, *, msg):
        '''
            Validates the presence and optionally the value of an HTTP Header.

            Arguments:
                header: Name of header
                value: Text contained in header. If not provided, then only presence of header is checked.

            Keyword Arguments:
                msg: A context string explaining why this assertion was done.
        '''
        if header not in self.headers:
            raise AssertionError(f">>{header}<< not present in HTTP Request. {msg}")

        if value is not None:
            actual = self.headers[header]
            if actual != value:
                raise AssertionError(f"Value >>header<< is {actual} but was expected to be {value}. {msg}.")

    def assert_header_mismatch(self, header, value=None, *, msg):
        '''
            Validates the absence of header or mismatch of its content with provided value.

            Arguments:
                header: Name of header
                value: Text contained in header. If not provided, then only absence of header is checked.

            Keyword Arguments:
                msg: A context string explaining why this assertion was done.
        '''

        if value is None:
            if header in self.headers:
                raise AssertionError(f">>{header}<< is present in HTTP Request. {msg}")
        else:
            actual = self.headers[header]
            if actual == value:
                raise AssertionError(f"Value >>header<< is {actual}. It was expected to be different. {msg}.")


class HttpResponse(HttpMessage):
    '''
        Encapsulates HTTP response message. Contains redirected responses as redirection history, if applicable.

        Arguments:
            session: `HttpSession` object which created corresponding `HttpRequest` for this response.
            response: `requests` library's Response object wrapped by this class.
    '''

    def __init__(self, session, response):
        super().__init__(response)
        self.__session = session
        self.__resp = response

    @property
    def is_redirect(self):
        '''
        Is True if this is a response is a redirection response.
        '''
        return self.__resp.is_redirect

    @property
    def url(self) -> str:
        ''' 
            URL for which this response was generated.

            In case of redirections, this is the last URL requested.
        '''
        return self.__resp.url

    @property
    def query_params(self) -> dict:
        ''' 
            Query parameters in URL for this response.

            In case of redirections, these are the query parameters in last request.
        '''
        return parse_qs(self.__resp.url)

    @property
    def status_code(self) -> int:
        ''' 
            HTTP Status code for this response. For example, 200
        '''
        return self.__resp.status_code

    def assert_status_codes(self, codes, *, msg):
        '''
            Assert that the status code is as expected.

            Arguments:
                codes: str or iterator

            Keyword Arguments:
                msg: Purpose of this assertion
        '''
        if type(codes) is int:
            codes = {codes}
        self.asserter.assert_true(self.status_code in codes, f"HTTP status code {self.status_code} is not expected. Expected: {codes}. {msg}")

    @property
    def status(self) -> str:
        ''' 
            HTTP Status Message for this response. For example, Not Found
        '''
        return self.__resp.reason

    @property
    def text(self) -> str:
        ''' 
            HTTP Response content as plain text.
        '''
        return self.__resp.text

    @property
    def json(self) -> 'JsonDictOrJsonList':
        ''' 
            HTTP Response content as Arjuna's `JsonDict` or `JsonList` object.
        '''
        return Json.from_str(self.text)

    @property
    def html(self) -> 'HtmlNode':
        ''' 
            HTTP Response content as Arjuna's `HtmlNode` object.
        '''
        return Html.from_str(self.text)

    @property
    def redir_history(self) -> tuple:
        '''
            Ordered `HttpResponse` objects for all redirections that led to this response.
        '''
        if self.__resp.history:
            return tuple([HttpResponse(self.__session, h) for h in self.__resp.history])
        else:
            return tuple()

    @property
    def last_redir_response(self) -> 'HttpResponse or None':
        '''
            Last `HttpResponse` object in case of redirections. None in case of no reidrections.
        '''
        if not self.redir_history:
            return None
        return self.redir_history[-1]

    @property
    def next_request(self):
        '''
            Next `HttpRequest` object if this response redirects to another request. None in case this is the last response in chain.
        '''
        next_req = self.__resp.next
        if next_req:
            return HttpRequest(self.__session, self.__resp.next)
        else:
            return None

    @property
    def request(self):
        '''
            `HttpRequest` object corresponding to this response object.
        '''
        return HttpRequest(self.__session, self.__resp.request)   

    __OUT = '''{}
{}{}'''

    @classmethod
    def __try_as_json(self, text):
        if text is None: return ""
        try:
            return json.dumps(json.loads(text), indent=2)
        except:
            return text

    @classmethod
    def repr_as_str(cls, *, status_code, status_msg, headers, content=None):
        content = cls.__try_as_json(content)
        if content:
            content = '\n\n{}\n'.format(content)
        return cls.__OUT.format(
            str(status_code) + ' ' + status_msg,
            '\n'.join('{}: {}'.format(k, v) for k, v in headers.items()),
            content
        ).strip()

    def __str__(self):
        return self.repr_as_str(
            status_code = self.status_code,
            status_msg = self.status,
            headers = self.headers,
            content = self.text
        )


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
    '''

    def __init__(self, session, request, label=None, xcodes=None, strict=False):
        super().__init__(request)
        self.__session = session
        self.__request = request
        req_repr = "{} {}".format(self.method, self.url)
        self.__label = label and label or req_repr
        self.__printable_label = label and self.__label + "::" + req_repr or req_repr
        self.__printable_label = len(self.__printable_label) > 119 and self.__printable_label[:125] + "<SNIP>" or self.__printable_label
        self.__strict = strict

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
                    response = HttpResponse(self.__session, self.__session.send(self.__req))
                except ConnectionError:
                    exc_flag = True
                    time.sleep(1)
                    continue
                else:
                    break
            if exc_flag:
                raise Exception("Connection error despite trying 5 times.")
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

    def __init__(self, session, url, method, label=None, content=None, content_type=None, xcodes=None, strict=False, headers=None, pretty_url=False, query_params=None, **named_query_params):
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

        self.__prepare_headers()
        self.__prepare_content()
        self.__req = self.__build_request()
        super().__init__(self.__session, self.__req, label=label, xcodes=self.__xcodes, strict=strict)

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
        req = Request(self.__method, url, data=self.__prep_content, headers=self.__headers, params=query_params, cookies=self.__session.cookies)
        return req.prepare()


class HttpSession:
    '''
        Encapsulates `requests` lib's Session object. Does automatic cookie management.

        Keyword Arguments:
            url: (Mandatory) Base URL for this HTTP session. If relative path is used as a route in sender methods like `.get`, then this URL is prefixed to their provided routes.
            oauth_token: OAuth 2.0 Bearer token for this session.
            content_type: Default content type for requests sent in this session. Overridable in individual sender methods. Default is `application/x-www-form-urlencoded`
            headers: HTTP headers to be added to request headers made by this session.
    '''

    def __init__(self, *, url, oauth_token=None, content_type='application/x-www-form-urlencoded', headers=None, _auto_session=True):
        self.__url = url.strip()
        self.__content_type = content_type
        self.__session = None
        self.__provided_headers = headers
        if _auto_session:
            self._set_session(Session())
        if oauth_token:
            self.__session.headers['Authorization'] = f'Bearer {oauth_token}'

    @property
    def cookies(self) -> dict:
        '''
            All current cookies in this session object.
        '''
        return self.__session.cookies.get_dict()

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

    def get(self, route, label=None, xcodes=None, strict=False, headers=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
        '''
            Sends an HTTP GET request.

            Arguments:
                route: Absolute or relative URL. If relative, then `url` of this session object is pre-fixed.

            Keyword Arguments:
                label: Label for this request. If available, it is used in reports and logs.
                xcodes: Expected HTTP response code(s).
                strict: If True in case of unexpected status code, an AssertionError is raised, else HttpUnexpectedStatusCodeError is raised.
                headers: Mapping of additional HTTP headers to be sent with this request.
                pretty_url: If True, the query params are formatted using pretty URL format instead of usual query string which is the default.
                query_params: A mapping of key-values to be included in query string.
                **named_query_params: Arbitrary key/value pairs. These are appended to the query string of URL for this request.

            Note:
                **query_params** and **named_query_params** have the same goal.
                In case of duplicates, named_query_params override query_params.
        '''
        request = _HttpRequest(self._session, self.__route(route), method="get", label=label, xcodes=xcodes, strict=strict, headers=headers, pretty_url=pretty_url, query_params=query_params, **named_query_params)
        return request.send()


    def head(self, route, label=None, xcodes=None, strict=False, headers=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
        '''
            Sends an HTTP HEAD request.

            Arguments:
                route: Absolute or relative URL. If relative, then `url` of this session object is pre-fixed.

            Keyword Arguments:
                label: Label for this request. If available, it is used in reports and logs.
                xcodes: Expected HTTP response code(s).
                strict: If True in case of unexpected status code, an AssertionError is raised, else HttpUnexpectedStatusCodeError is raised.
                headers: Mapping of additional HTTP headers to be sent with this request.
                pretty_url: If True, the query params are formatted using pretty URL format instead of usual query string which is the default.
                query_params: A mapping of key-values to be included in query string.
                **named_query_params: Arbitrary key/value pairs. These are appended to the query string of URL for this request.

            Note:
                **query_params** and **named_query_params** have the same goal.
                In case of duplicates, named_query_params override query_params.
        '''
        request = _HttpRequest(self._session, self.__route(route), method="head", label=label, xcodes=xcodes, strict=strict, headers=headers, pretty_url=pretty_url, query_params=query_params, **named_query_params)
        return request.send()


    def delete(self, route, label=None, xcodes=None, strict=False, headers=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
        '''
            Sends an HTTP DELETE request.

            Arguments:
                route: Absolute or relative URL. If relative, then `url` of this session object is pre-fixed.

            Keyword Arguments:
                label: Label for this request. If available, it is used in reports and logs.
                xcodes: Expected HTTP response code(s).
                strict: If True in case of unexpected status code, an AssertionError is raised, else HttpUnexpectedStatusCodeError is raised.
                headers: Mapping of additional HTTP headers to be sent with this request.
                pretty_url: If True, the query params are formatted using pretty URL format instead of usual query string which is the default.
                query_params: A mapping of key-values to be included in query string.
                **named_query_params: Arbitrary key/value pairs. These are appended to the query string of URL for this request.

            Note:
                **query_params** and **named_query_params** have the same goal.
                In case of duplicates, named_query_params override query_params.
        '''
        request = _HttpRequest(self._session, self.__route(route), method="delete", label=label, xcodes=xcodes, strict=strict, headers=headers, pretty_url=pretty_url, query_params=query_params, **named_query_params)
        return request.send()

    def post(self, route, *, content, label=None, content_type=None, xcodes=None, strict=False, headers=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
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
            pretty_url: If True, the query params are formatted using pretty URL format instead of usual query string which is the default.
            query_params: A mapping of key-values to be included in query string.
            **named_query_params: Arbitrary key/value pairs. These are appended to the query string of URL for this request.

        Note:
            **query_params** and **named_query_params** have the same goal.
            In case of duplicates, named_query_params override query_params.
        '''
        request = _HttpRequest(self._session, self.__route(route), method="post", label=label, content=content, content_type=content_type, xcodes=xcodes, strict=strict, headers=headers, pretty_url=pretty_url, query_params=query_params, **named_query_params)
        return request.send()

    def put(self, route, *, content, label=None, content_type=None, xcodes=None, strict=False, headers=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
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
            pretty_url: If True, the query params are formatted using pretty URL format instead of usual query string which is the default.
            query_params: A mapping of key-values to be included in query string.
            **named_query_params: Arbitrary key/value pairs. These are appended to the query string of URL for this request.

        Note:
            **query_params** and **named_query_params** have the same goal.
            In case of duplicates, named_query_params override query_params.
        '''
        request = _HttpRequest(self._session, self.__route(route), method="put", label=label, content=content, content_type=content_type, xcodes=xcodes, strict=strict, headers=headers, pretty_url=pretty_url, query_params=query_params, **named_query_params)
        return request.send()

    def patch(self, route, *, content, label=None, content_type=None, xcodes=None, strict=False, headers=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
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
            pretty_url: If True, the query params are formatted using pretty URL format instead of usual query string which is the default.
            query_params: A mapping of key-values to be included in query string.
            **named_query_params: Arbitrary key/value pairs. These are appended to the query string of URL for this request.

        Note:
            **query_params** and **named_query_params** have the same goal.
            In case of duplicates, named_query_params override query_params.
        '''
        request = _HttpRequest(self._session, self.__route(route), method="patch", label=label, content=content, content_type=content_type, xcodes=xcodes, strict=strict, headers=headers, pretty_url=pretty_url, query_params=query_params, **named_query_params)
        return request.send()

    def options(self, route, *, content, label=None, content_type=None, xcodes=None, strict=False, headers=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
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
            pretty_url: If True, the query params are formatted using pretty URL format instead of usual query string which is the default.
            query_params: A mapping of key-values to be included in query string.
            **named_query_params: Arbitrary key/value pairs. These are appended to the query string of URL for this request.

        Note:
            **query_params** and **named_query_params** have the same goal.
            In case of duplicates, named_query_params override query_params.
        '''
        request = _HttpRequest(self._session, self.__route(route), method="options", label=label, content=content, content_type=content_type, xcodes=xcodes, strict=strict, headers=headers, pretty_url=pretty_url, query_params=query_params, **named_query_params)
        return request.send()



