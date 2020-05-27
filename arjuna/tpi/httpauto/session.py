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
from urllib.parse import urlparse, urlencode, parse_qs
from requests import Request, Session
from arjuna.tpi.error import HttpUnexpectedStatusCode
from arjuna.tpi.helper.json import Json
from arjuna.tpi.helper.html import Html
from requests.exceptions import ConnectionError
import time

class HttpResponse:
    '''
        Encapsulates HTTP response message.

        Arguments:
            session: `HttpSession` object which created corresponding `HttpRequest` for this response.
            response: `requests` library's Response object wrapped by this class.
    '''

    def __init__(self, session, response):
        self.__session = session
        self.__resp = response

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

    @property
    def status(self) -> str:
        ''' 
            HTTP Status Message for this response. For example, Not Found
        '''
        return self.__resp.reason

    @property
    def headers(self) -> dict:
        ''' 
            HTTP Response Headers for this response.
        '''
        return self.__resp.headers

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
            `HttpResponse` objects for all redirections that led to this response.
        '''
        if self.__resp.history:
            return (HttpResponse(self.__session, h) for h in self.__resp.history)
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
        next_req = self.__resp.next
        if next_req:
            return HttpRequest(self.__session, self.__resp.next)
        else:
            return None

    @property
    def request(self):
        return HttpRequest(self.__session, self.__resp.request)   

    __OUT = '''{}
{}{}'''

    def __try_as_json(self):
        if self.text is None: return ""
        try:
            return json.dumps(json.loads(self.text), indent=2)
        except:
            return self.text

    def __str__(self):
        content = self.__try_as_json()
        if content:
            content = '\n\n{}\n'.format(content)
        return self.__OUT.format(
            str(self.status_code) + ' ' + self.status,
            '\n'.join('{}: {}'.format(k, v) for k, v in self.headers.items()),
            content
        ).strip()


class HttpRequest:

    def __init__(self, session, request, label=None):
        self.__session = session
        self.__request = request
        req_repr = "{} {}".format(self.method, self.url)
        self.__label = label and label or req_repr
        self.__printable_label = label and self.__label + "::" + req_repr or req_repr
        self.__printable_label = len(self.__printable_label) > 119 and self.__printable_label[:125] + "<SNIP>" or self.__printable_label

    @property
    def label(self):
        return self.__label

    @property
    def query_params(self):
        return parse_qs(self.url)

    def send(self):
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
        except Exception as e:
            import traceback
            response = "Error in sending the request\n"
            response += e.__class__.__name__ + ":" + str(e) + "\n"
            response += traceback.format_exc()
            Arjuna.get_report_metadata().add_network_packet_info(
                NetworkPacketInfo(label=self.label, request=str(self), response=str(response))
            )
            raise e
        else:
            # Should be configurable
            redir_network_packets = []
            for redir_resp in response.redir_history:
                redir_req = redir_resp.request
                redir_network_packets.append(
                    NetworkPacketInfo(
                        label="Sub-Request: {} {}".format(redir_req.method, redir_req.url), 
                        request=str(redir_req), 
                        response=str(redir_resp),
                        redir_network_packets=tuple()
                    )
                )

            # The request for last response object was the last request and hence the last redirection.
            if response.redir_history:
                # last_req = response.last_request
                # if not last_req:
                last_req = response.request
                redir_network_packets.append(
                                    NetworkPacketInfo(
                                        label="Sub-Request: {} {}".format(last_req.method, last_req.url), 
                                        request=str(last_req), 
                                        response=str(response),
                                        redir_network_packets=tuple()
                                    )
                                )                

            Arjuna.get_report_metadata().add_network_packet_info(
                NetworkPacketInfo(label=self.label, request=str(self), response=str(response), redir_network_packets=tuple(redir_network_packets))
            )
            if self.__xcodes is not None and response.status_code not in self.__xcodes:
                raise HttpUnexpectedStatusCode(self.__req, response)
            return response

    @property
    def url(self):
        return self.__request.url

    @property
    def method(self):
        return self.__request.method

    @property
    def text(self):
        return self.__request.body

    __OUT ='''{}
{}{}'''

    def __str__(self):
        content = self.text
        if content:
            content = '\n\n{}\n'.format(content)
        else:
            content = ""
        return self.__OUT.format(
            self.__request.method + ' ' + self.url,
            '\n'.join('{}: {}'.format(k, v) for k, v in self.__request.headers.items()),
            content
        ).strip()


class _HttpRequest(HttpRequest):

    def __init__(self, session, url, method, label=None, content=None, content_type=None, xcodes=None, headers=None, **query_params):
        self.__session = session
        self.__method = method.upper()
        self.__url = url
        self.__content = content
        self.__prep_content = content
        self.__content_type = content_type
        self.__xcodes = None
        if xcodes is not None:
            self.__xcodes = type(xcodes) in {set, list, tuple} and xcodes or {xcodes}
        self.__query_parms = query_params
        self.__headers = {}
        self.__headers.update(session.headers)
        if headers:
            self.__headers.update(headers)

        self.__prepare_content()
        self.__req = self.__build_request()
        super().__init__(self.__session, self.__req, label=label)

    def __prepare_content(self):
        if self.__method in {'GET', 'DELETE'}: return
        if self.__headers['Content-Type'].lower() == 'application/json':
            self.__prep_content = json.dumps(self.__content, indent=2)
        else:
            self.__prep_content = urlencode(self.__content)

    def __build_request(self):
        parsed_uri = urlparse(self.__url)
        #self.__headers['Host'] = parsed_uri.netloc
        if self.__method in {'POST', 'PUT'}:
            if self.__content_type is not None:
                self.__headers['Content-Type'] = self.__content_type
        if self.__method in {'GET', 'DELETE'}:
            if 'Content-Type' in self.__headers:
                del self.__headers['Content-Type']
        req = Request(self.__method, self.__url, data=self.__prep_content, headers=self.__headers, params=self.__query_parms, cookies=self.__session.cookies)
        return req.prepare()


class HttpSession:

    def __init__(self, *, url, oauth_token=None, content_type='application/x-www-form-urlencoded', _auto_session=True):
        self.__url = url
        self.__content_type = content_type
        self.__session = None
        if _auto_session:
            self._set_session(Session())
        if oauth_token:
            self.__session.headers['Authorization'] = f'Bearer {oauth_token}'

    @property
    def cookies(self):
        return self.__session.cookies.get_dict()

    def _set_session(self, session):
        self.__session = session
        self.__session.headers['Content-Type'] = self.__content_type

    @property
    def url(self):
        return self.__url

    @property
    def _session(self):
        return self.__session

    @property
    def _request_headers(self):
        return self.__session.headers

    def __route(self, route):
        if route.lower().startswith("http"):
            return route
        else:
            return self.url + route

    def get(self, route, label=None, xcodes=None, **query_params):
        request = _HttpRequest(self._session, self.__route(route), method="get", label=label, xcodes=xcodes, **query_params)
        return request.send()

    def delete(self, route, label=None, xcodes=None, **query_params):
        request = _HttpRequest(self._session, self.__route(route), method="delete", label=label, xcodes=xcodes, **query_params)
        return request.send()

    def post(self, route, *, label=None, content, content_type=None, xcodes=None, headers=None, **query_params):
        request = _HttpRequest(self._session, self.__route(route), method="post", label=label, content=content, content_type=content_type, xcodes=xcodes, headers=headers, **query_params)
        return request.send()

    def put(self, route, *, label=None, content, content_type=None, xcodes=None, **query_params):
        request = _HttpRequest(self._session, self.__route(route), method="put", label=label, content=content, content_type=content_type, xcodes=xcodes, **query_params)
        return request.send()



