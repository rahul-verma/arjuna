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
from requests import Request, Session
from arjuna.tpi.error import HttpUnexpectedStatusCodeError, HttpSendError
from arjuna.tpi.parser.json import Json
from arjuna.tpi.parser.html import Html
from arjuna.tpi.engine.asserter import AsserterMixIn
from requests.exceptions import ConnectionError, TooManyRedirects
import time

from .message import HttpMessage


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

    content = text

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
        from .request import HttpRequest
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
        from .request import HttpRequest
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

