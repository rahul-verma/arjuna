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
from urllib.parse import urlparse, urlencode
from requests import Request, Session

class HttpResponse:

    def __init__(self, session, response):
        self.__session = session
        self.__resp = response

    @property
    def url(self):
        return self.__resp.url

    @property
    def status_code(self):
        return self.__resp.status_code

    @property
    def headers(self):
        return self.__resp.headers

    @property
    def text(self):
        return self.__resp.text

    @property
    def json(self):
        return json.loads(self.text)

    @property
    def redir_history(self):
        if self.__resp.history is not None:
            return [HttpResponse(self.__session, h) for h in self.__resp.history]
        else:
            return None

    @property
    def last_redir_response(self):
        if self.redir_history is None:
            return None
        else:
            return self.redir_history[-1]

    @property
    def next_request(self):
        return HttpRequest(self.__session, self.__resp.next)

    __OUT = '''
-----------Response-----------
{}
{}{}
---------End Response----------
'''

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
            str(self.status_code) + ' ' + self.url,
            '\n'.join('{}: {}'.format(k, v) for k, v in self.headers.items()),
            content
        )


class HttpRequest:

    def __init__(self, session, request):
        self.__session = session
        self.__request = request

    def send(self):
        from arjuna import log_info
        log_info(str(self))
        result = HttpResponse(self.__session, self.__session.send(self.__req))
        log_info(str(result))
        if self.__xcodes is not None and result.status_code not in self.__xcodes:
            raise Exception(f"Unexpected status code {result.status_code} for {result.url} in {self.__method} request.")
        return result

    @property
    def url(self):
        return self.__request.url

    @property
    def text(self):
        return self.__request.body

    __OUT ='''
-----------Request-----------
{}
{}{}
---------End Request----------
'''

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
        )


class _HttpRequest(HttpRequest):

    def __init__(self, session, url, method, content=None, content_type=None, xcodes=None, headers=None, **query_params):
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
        from arjuna import log_info
        log_info(self.__headers)

        self.__prepare_content()
        self.__req = self.__build_request()
        super().__init__(self.__session, self.__req)

    def __prepare_content(self):
        if self.__method in {'GET', 'DELETE'}: return
        if self.__headers['Content-Type'].lower() == 'application/json':
            self.__prep_content = json.dumps(self.__content, indent=2)
        else:
            self.__prep_content = urlencode(self.__content)

    def __build_request(self):
        from arjuna import log_info
        parsed_uri = urlparse(self.__url)
        #self.__headers['Host'] = parsed_uri.netloc
        if self.__method in {'POST', 'PUT'}:
            if self.__content_type is not None:
                self.__headers['Content-Type'] = self.__content_type
        if self.__method in {'GET', 'DELETE'}:
            if 'Content-Type' in self.__headers:
                del self.__headers['Content-Type']
        log_info(self.__content_type)
        log_info(type(self.__prep_content))
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

    def get(self, route, xcodes=None, **query_params):
        request = _HttpRequest(self._session, self.__route(route), method="get", xcodes=xcodes, **query_params)
        return request.send()

    def delete(self, route, xcodes=None, **query_params):
        request = _HttpRequest(self._session, self.__route(route), method="delete", xcodes=xcodes, **query_params)
        return request.send()

    def post(self, route, *, content, content_type=None, xcodes=None, headers=None, **query_params):
        request = _HttpRequest(self._session, self.__route(route), method="post", content=content, content_type=content_type, xcodes=xcodes, headers=headers, **query_params)
        return request.send()

    def put(self, route, *, content, content_type=None, xcodes=None, **query_params):
        request = _HttpRequest(self._session, self.__route(route), method="put", content=content, content_type=content_type, xcodes=xcodes, **query_params)
        return request.send()



