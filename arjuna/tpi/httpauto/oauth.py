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

from oauthlib.oauth2 import BackendApplicationClient, MobileApplicationClient
from requests_oauthlib import OAuth2Session

from .session import HttpSession

from bs4 import BeautifulSoup
import urllib.parse

class OAuthSession(HttpSession):

    def __init__(self, *, session, url):
        super().__init__(url=url, _auto_session=False)
        self._set_session(session)
        self.__token = None

    @property
    def token(self):
        return self.__token

    def _set_outh_token(self, token):
        self.__token = token

    def create_new_session(self, url, *, content_type=None):
        return HttpSession(url=url, oauth_token=self.token, content_type=content_type)


class OAuthClientGrantSession(OAuthSession):
    '''
        Creates token using OAuth's Resource Owner Client Credentials Grant Type.
        Uses BackendApplicationClient from requests_oauthlib.
    '''

    def __init__(self, *, url, client_id, token_url, client_secret):
        client = BackendApplicationClient(client_id=client_id)
        oauth = OAuth2Session(client=client)
        super().__init__(session=oauth, url=url)
        token = oauth.fetch_token(token_url=token_url, 
                                  client_id=client_id,
                                  client_secret=client_secret)
        self._set_outh_token(token)


class OAuthImplicitGrantSession(OAuthSession):
    '''
        Creates token using OAuth's Implicit Code Grant Type.
        Uses MobileApplicationClient from requests_oauthlib.
    '''
    def __init__(self, *, url, client_id, scope, authorization_url, redirect_uri=None, authorization_handler=None, **auth_args):
        oauth = OAuth2Session(
            client=MobileApplicationClient(client_id=client_id),
            scope=scope,
            redirect_uri=redirect_uri,
        )
        super().__init__(session=oauth, url=url)

        authorization_url, state = oauth.authorization_url(authorization_url)
        from arjuna import log_info
        log_info(oauth.cookies.get_dict())

        token = None
        if authorization_handler is None:
            token = outh.token_from_fragment(callback_url)
        else:
            token = authorization_handler(self, authorization_url, **auth_args)
        self._set_outh_token(token)


class ImplicitGrand:
    def __init__(self):
        '''
        config can be None, but the use Set_env... and set_creds...
        or a yaml file to be loaded by loadConfigFile()
        or a dict resulting loadConfigFile()
        '''

        from arjuna import C

        self.set_environment(
            C('authorization_URL'),
            C('callback_URL'),
            C('scope'),
            C('client_Id')
        )
        self.set_credentials(
            C('username'),
            C('password')
        )

    def set_environment(self, authorization_URL,
                        callback_URL,
                        scope,
                        client_Id):
        self.authorization_URL = authorization_URL
        self.callback_URL = callback_URL
        self.client_Id = client_Id
        self.scope = scope

    def set_credentials(self, username, password):
        self.username = username
        self.password = password

    def get_token(self):
        oauth = OAuth2Session(
            client=MobileApplicationClient(client_id=self.client_Id),
            scope=self.scope,
            redirect_uri=self.callback_URL,
        )
        authorization_url, state = oauth.authorization_url(
            self.authorization_URL)

        authorize_req_response = oauth.get(authorization_url)
        if authorize_req_response.status_code != 200:
            raise Exception('Authorization request was not 200')

        soup = BeautifulSoup(authorize_req_response.content, "html.parser")

        action_element = soup.find("form", attrs={"id": "login-form"})
        if action_element is not None:
            action = action_element["action"]
        else:
            raise Exception(
                'Authorization response does not contain the login form.')

        payload = {"requestId": soup.find(
            "input",
            attrs={"name": "requestId"})["value"]}
        payload["csrf-token"] = soup.find("input",
                                          attrs={"name": "csrf-token"}
                                          )["value"]
        payload["mail"] = self.username
        payload["password"] = self.password

        authentication_response = oauth.post(
            self.authorization_URL.replace('authorization', action), data=payload)

        print(authentication_response.url)
        for k, v in authentication_response.request.headers.items():
            print(f"{k}: {v}")

        if authentication_response.status_code != 200:
            raise Exception('Authentication request was not 200')

        if authentication_response.history:
            self.dURLParsed = urllib.parse.parse_qs(
                authentication_response.history[-1]._next.url)
            if 'error_description' in self.dURLParsed.keys():
                raise Exception('Authentication did not work, error: {} {}'
                                .format(
                                    self.dURLParsed['error_description'],
                                    self.dURLParsed[self.callback_URL + '?error']))

            return self.dURLParsed["access_token"][0]
        else:
            raise Exception('Authentication did not work, error: {}'.format(
                authentication_response.text))


