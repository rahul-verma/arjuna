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
from .service import HttpService
from .oauth import OAuthImplicitGrantService, OAuthClientGrantService

from collections import namedtuple
from arjuna.tpi.data.entity import data_entity

_HttpContent = namedtuple("_HttpContent", "content type")
_HttpField = namedtuple("_HttpField", "name value is_file content_type headers")

class Http:
    '''
    The Facade class for HTTP Automation.
    '''

    @classmethod
    def service(cls, *, name="anon", url=None, oauth_token=None, request_content_handler=None, headers=None, max_redirects=None, auth=None, proxy=None):
        '''
            Create an HTTP Service representing SEAMful automation in Arjuna.

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
        return HttpService(name=name, url=url, oauth_token=oauth_token, request_content_handler=request_content_handler, headers=headers, max_redirects=max_redirects, auth=auth, proxy=proxy, _auto_session=True)

    @classmethod
    def proxy(cls, host="localhost", port=8080):
        '''
        Create a proxy dict.

        Arguments:

            host: Proxy host name/IP. Default is localhost
            port: Proxy network port. Default is 8080
        '''
        proxy = f"http://{host}:{port}"
        return {'http': proxy, 'https': proxy}

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
            from arjuna.core.fmt import arj_convert
            content = json.dumps(arj_convert(content), indent=2)
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
    def oauth_client_grant_service(cls, *, name="anon", url, client_id, client_secret, token_url):
        '''
            Create OAuthClientGrantService object.

            Creates token using OAuth's Resource Owner Client Credentials Grant Type.
            Uses BackendApplicationClient from requests_oauthlib.

            Keyword Arguments:
                url: Base URL for this HTTP session. If relative path is used as a route in sender methods like `.get`, then this URL is prefixed to their provided routes.
                client_id: Client ID
                client_secret: Client Secret
                token_url: Token URL
        '''
        return OAuthClientGrantService(name=name, url=url, client_id=client_id, client_secret=client_secret, token_url=token_url)


    @classmethod
    def oauth_implicit_grant_service(cls, *, name="anon", url, client_id, scope, redirect_uri=None, auth_url, auth_handler=None, **auth_args):
        '''
            Create OAuthImplicitGrantService object.

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

            Note:s
                Some sample auth_handler signatures:

                    .. code-block:: python

                        auth_handler_1(oauth_session, auth_url, **kwargs)
                        auth_handler_2(oauth_session, auth_url, some_arg=None, another_arg="some_def_value")

        '''
        return OAuthImplicitGrantService(name=name, url=url, client_id=client_id, scope=scope, redirect_uri=redirect_uri, auth_url=auth_url, auth_handler=auth_handler, **auth_args)
