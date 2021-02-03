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
import io
import os

from urllib.parse import urlencode
from requests.auth import *
from requests_toolbelt.multipart.encoder import MultipartEncoder
from .session import HttpSession
from .response import HttpResponse
from .oauth import OAuthImplicitGrantSession, OAuthClientGrantSession

from collections import namedtuple
from arjuna.tpi.data.entity import data_entity

_HttpContent = namedtuple("_HttpContent", "content type")
_HttpField = namedtuple("_HttpField", "name value is_file content_type headers")

class Http:
    '''
    The Facade class for HTTP Automation.
    '''

    @classmethod
    def session(cls, *, url=None, oauth_token=None, request_content_handler=None, headers=None, max_redirects=None, auth=None, proxy=None):
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
        return HttpSession(url=url, oauth_token=oauth_token, request_content_handler=request_content_handler, headers=headers, max_redirects=max_redirects, auth=auth, proxy=proxy, _auto_session=True)

    @classmethod
    def get(cls, route, label=None, xcodes=None, strict=False, headers=None, cookies=None, allow_redirects=True, auth=None, timeout: float=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
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
        return HttpSession().get(route, label=label, xcodes=xcodes, strict=strict, headers=headers, cookies=cookies, allow_redirects=allow_redirects, auth=auth, timeout=timeout, pretty_url=pretty_url, query_params=query_params, **named_query_params)

    @classmethod
    def head(cls, route, label=None, xcodes=None, strict=False, headers=None, cookies=None, allow_redirects=True, auth=None, timeout: float=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
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
        return HttpSession().head(route, label=label, xcodes=xcodes, strict=strict, headers=headers, cookies=cookies, allow_redirects=allow_redirects, auth=auth, timeout=timeout, pretty_url=pretty_url, query_params=query_params, **named_query_params)

    @classmethod
    def delete(cls, route, label=None, xcodes=None, strict=False, headers=None, cookies=None, allow_redirects=True, auth=None, timeout: float=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
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
        return HttpSession().delete(route, label=label, xcodes=xcodes, strict=strict, headers=headers, cookies=cookies, allow_redirects=allow_redirects, auth=auth, timeout=timeout, pretty_url=pretty_url, query_params=query_params, **named_query_params)

    @classmethod
    def post(cls, route, *, content, label=None, xcodes=None, strict=False, headers=None, cookies=None, allow_redirects=True, auth=None, timeout: float=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
        '''
        Sends an HTTP POST request.

        Arguments:
            route: Absolute or relative URL. If relative, then `url` of this session object is pre-fixed.

        Keyword Arguments:
            label: Label for this request. If available, it is used in reports and logs.
            content: Content to be sent in this HTTP request. If passed as string, then content-type set in session is used using the content request handler. It can also be a dictionary with keys - 'content' and 'type'.
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
        return HttpSession().post(route, label=label, content=content, xcodes=xcodes, strict=strict, headers=headers, cookies=cookies, allow_redirects=allow_redirects, auth=auth, timeout=timeout, pretty_url=pretty_url, query_params=query_params, **named_query_params)

    @classmethod
    def put(cls, route, *, content, label=None, xcodes=None, strict=False, headers=None, cookies=None, allow_redirects=True, auth=None, timeout: float=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
        '''
        Sends an HTTP PUT request.

        Arguments:
            route: Absolute or relative URL. If relative, then `url` of this session object is pre-fixed.

        Keyword Arguments:
            label: Label for this request. If available, it is used in reports and logs.
            content: Content to be sent in this HTTP request. If passed as string, then content-type set in session is used using the content request handler. It can also be a dictionary with keys - 'content' and 'type'.
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
        return HttpSession().put(route, label=label, content=content, xcodes=xcodes, strict=strict, headers=headers, cookies=cookies, allow_redirects=allow_redirects, auth=auth, timeout=timeout, pretty_url=pretty_url, query_params=query_params, **named_query_params)

    @classmethod
    def patch(cls, route, *, content, label=None, xcodes=None, strict=False, headers=None, cookies=None, allow_redirects=True, auth=None, timeout: float=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
        '''
        Sends an HTTP PUT request.

        Arguments:
            route: Absolute or relative URL. If relative, then `url` of this session object is pre-fixed.

        Keyword Arguments:
            label: Label for this request. If available, it is used in reports and logs.
            content: Content to be sent in this HTTP request. If passed as string, then content-type set in session is used using the content request handler. It can also be a dictionary with keys - 'content' and 'type'.
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
        return HttpSession().patch(route, label=label, content=content, xcodes=xcodes, strict=strict, headers=headers, cookies=cookies, allow_redirects=allow_redirects, auth=auth, timeout=timeout, pretty_url=pretty_url, query_params=query_params, **named_query_params)

    @classmethod
    def options(cls, route, *, content, label=None, xcodes=None, strict=False, headers=None, cookies=None, allow_redirects=True, auth=None, timeout: float=None, pretty_url=False, query_params=None, **named_query_params) -> HttpResponse:
        '''
        Sends an HTTP PUT request.

        Arguments:
            route: Absolute or relative URL. If relative, then `url` of this session object is pre-fixed.

        Keyword Arguments:
            label: Label for this request. If available, it is used in reports and logs.
            content: Content to be sent in this HTTP request. If passed as string, then content-type set in session is used using the content request handler. It can also be a dictionary with keys - 'content' and 'type'.
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
        return HttpSession().options(route, label=label, content=content, xcodes=xcodes, strict=strict, headers=headers, cookies=cookies, allow_redirects=allow_redirects, auth=auth, timeout=timeout, pretty_url=pretty_url, query_params=query_params, **named_query_params)

    @classmethod
    def proxy(cls, url):
        '''
        Create a proxy dict.
        '''
        return {'http': url, 'https': url}

    class auth:
        '''
        HTTP Authentication Builder
        '''

        @classmethod
        def basic(cls, *, user, pwd):
            '''
            Create an HTTP Basic Authentication object.
            '''
            return HTTPBasicAuth(user, pwd)

        @classmethod
        def digest(cls, *, user, pwd):
            '''
            Create an HTTP Basic Authentication object.
            '''
            return HTTPDigestAuth(user, pwd)

    class content:

        @classmethod
        def get_content_type(cls, handler_method):
            mapping = {
                cls.blank: "text/html",
                cls.html: "text/html",
                cls.text: "text/html",
                cls.utf8: "text/html",
                cls.bytes: "text/html",
                cls.urlencoded: "application/x-www-form-urlencoded",
                cls.json: "application/json",
                cls.xml: "application/xml"
            }
            return mapping[handler_method]

        @classmethod
        def blank(cls, content=""):
            '''
            Send empty content. Content-Type is sent as “text/html”
            '''
            return _HttpContent(content="", type=cls.get_content_type(cls.blank))

        @classmethod
        def html(cls, content=""):
            '''
            Send HTML content. Content-Type is sent as “text/html”
            '''
            return _HttpContent(content=content, type=cls.get_content_type(cls.html))

        text = html

        @classmethod
        def bytes(cls, content=""):
            '''
            Send bytes string. Content-Type is sent as “text/html”
            '''
            if content:
                content = io.BytesIO(content)
            return _HttpContent(content=content, type=cls.get_content_type(cls.bytes))

        @classmethod
        def utf8(cls, content=""):
            '''
            Send UTF-8 string. Content-Type is sent as “text/html”
            '''
            if content:
                content = content.encode("utf-8")
            return _HttpContent(content=content, type=cls.get_content_type(cls.utf8))

        @classmethod
        def urlencoded(cls, content=""):
            '''
            Send a dictionary of key-values in URL encoded format. Content-Type is sent as “application/x-www-form-urlencoded”
            '''
            if content:
                content = urlencode(content)
            return _HttpContent(content=content, type=cls.get_content_type(cls.urlencoded))

        @classmethod
        def json(cls, content=""):
            '''
            Send a dictionary of key-values as JSON. Content-Type is sent as “application/json”
            '''
            from json import JSONEncoder
            from arjuna.tpi.parser.yaml import YamlDict, YamlList
            from arjuna.tpi.parser.json import JsonDict, JsonList
            class _CustomEncoder(JSONEncoder):
                def default(self, o):
                    if isinstance(o, YamlDict) or isinstance(o, YamlList) or isinstance(o, JsonList) or isinstance(o, JsonDict):
                        return o.raw_object
                    return JSONEncoder.default(self, o)

            if type(content) is tuple:
                content = list(content)

            if content:
                if isinstance(content, JsonList) or isinstance(content, JsonDict):
                    content = content.raw_object
                content = json.dumps(content, cls=_CustomEncoder, indent=2)
            else:
                content = str(content)
            return _HttpContent(content=content, type=cls.get_content_type(cls.json))

        @classmethod
        def xml(cls, content=""):
            '''
            Send an XML string as XML. Content-Type is sent as “application/xml
            '''
            return _HttpContent(content=content, type=cls.get_content_type(cls.xml))

        @classmethod
        def file(cls, field_name, file_name, *, content_type='text/plain', headers=None):
            '''
            Upload a file and send as multipart data. Content-Type is sent as the content type got from multipart encoding.
            '''
            from arjuna import C, ArjunaOption
            file_path = os.path.join(C(ArjunaOption.DATA_FILE_DIR), file_name)
            encoder = MultipartEncoder(
                {field_name: (file_name, open(file_path, 'rb'), content_type, headers)}
            )
            return _HttpContent(content=encoder.to_string(), type=encoder.content_type)

        @classmethod
        def multipart(cls, *fields):
            '''
            Send the provided HTTP fields as multipart data. Content-Type is sent as the content type got from multipart encoding.
            '''
            from arjuna import C, ArjunaOption
            elist = list()
            for field in fields:
                if type(field) is dict:
                    for k,v in field.items():
                        elist.append((k, str(v)))
                elif isinstance(field, _HttpField):
                    if field.is_file:
                        file_path = os.path.join(C(ArjunaOption.DATA_FILE_DIR), field.value)
                        elist.append((field.name, (field.value, open(file_path, 'rb'), field.content_type, field.headers)))
                    else:
                        elist.append((field.name, str(field.value)))
            encoder = MultipartEncoder(elist)
            return _HttpContent(content=encoder.to_string(), type=encoder.content_type)

        @classmethod
        def custom(self, content, *, type):
            '''
            Send content with a custom content type.
            '''
            return _HttpContent(content=content, type=type)

    @classmethod
    def field(cls, name, value, is_file=False, content_type="text/plain", headers=None):
        return _HttpField(name=name, value=value, is_file=is_file, content_type=content_type, headers=headers)

    @classmethod
    def oauth_client_grant_session(cls, *, url, client_id, client_secret, token_url):
        '''
            Create OAuthClientGrantSession object.

            Creates token using OAuth's Resource Owner Client Credentials Grant Type.
            Uses BackendApplicationClient from requests_oauthlib.

            Keyword Arguments:
                url: Base URL for this HTTP session. If relative path is used as a route in sender methods like `.get`, then this URL is prefixed to their provided routes.
                client_id: Client ID
                client_secret: Client Secret
                token_url: Token URL
        '''
        return OAuthClientGrantSession(url=url, client_id=client_id, client_secret=client_secret, token_url=token_url)


    @classmethod
    def oauth_implicit_grant_session(cls, *, url, client_id, scope, redirect_uri=None, auth_url, auth_handler=None, **auth_args):
        '''
            Create OAuthImplicitGrantSession object.

            Creates token using OAuth's Implicit Code Grant Type.
            Uses MobileApplicationClient from requests_oauthlib.

            Keyword Arguments:
                url: Base URL for this HTTP session. If relative path is used as a route in sender methods like `.get`, then this URL is prefixed to their provided routes.
                client_id: Client ID
                scope: Scope
                redirect_uri: Redirect URI
                auth_url: Authorization URL
                auth_handler: A callback function to handle custom authroization logic. It will be called by providing session object, authorization URL and auth_args.
                **auth_args: Arbitray key-value pairs to be passed as arguments to the auth_handler callback.

            Note:
                Some sample auth_handler signatures:

                    .. code-block:: python

                        auth_handler_1(oauth_session, auth_url, **kwargs)
                        auth_handler_2(oauth_session, auth_url, some_arg=None, another_arg="some_def_value")

        '''
        return OAuthImplicitGrantSession(url=url, client_id=client_id, scope=scope, redirect_uri=redirect_uri, auth_url=auth_url, auth_handler=auth_handler, **auth_args)
