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

# The tests are based on tests for requests library in https://github.com/psf/requests

import io

from arjuna import *


@test(drive_with=records(
    record(username='user', password='pass'),
    record(username=u'имя'.encode('utf-8'), password=u'пароль'.encode('utf-8')),
    record(username=42, password=42),
    record(username=None, password=None),
))
def check_set_basicauth(request, data):
    auth = Http.auth.basic(user=data.username, pwd=data.password)
    r = Http.get('http://httpbin.org/get', auth=auth)
    from requests.auth import _basic_auth_str
    assert r.request.headers['Authorization'] == _basic_auth_str(data.username, data.password)


@test
def check_basicauth_get(request):
    auth = Http.auth.basic(user='user', pwd='pass')
    url = 'http://httpbin.org/basic-auth/user/pass'

    r = Http.get(url, auth=auth)
    assert r.status_code == 200

    r = Http.get(url)
    assert r.status_code == 401

    s = Http.session(auth=auth)
    r = s.get(url)
    assert r.status_code == 200

@test
def check_basicauth_encodes_byte_strings(request):
    """Ensure b'test' formats as the byte string "test" rather
    than the unicode string "b'test'" in Python 3.
    """
    auth = Http.auth.basic(user=b'\xc5\xafsername', pwd=b'test\xc6\xb6')
    r = Http.get('http://httpbin.org', auth=auth)
    assert r.request.headers['Authorization'] == 'Basic xa9zZXJuYW1lOnRlc3TGtg=='

digest_auth_algo = ('MD5', 'SHA-256', 'SHA-512')

@test
def check_DIGEST_HTTP_200_OK_GET(request):

    for authtype in digest_auth_algo:
        auth = Http.auth.digest(user='user', pwd='pass')
        url = 'http://httpbin.org/digest-auth/auth/user/pass/' + authtype + '/never'

        r = Http.get(url, auth=auth)
        assert r.status_code == 200

        r = Http.get(url)
        assert r.status_code == 401
        print(r.headers['WWW-Authenticate'])

        s = Http.session(auth=auth)
        r = s.get(url)
        assert r.status_code == 200

@test
def check_DIGEST_AUTH_RETURNS_COOKIE(request):

    for authtype in digest_auth_algo:
        auth = Http.auth.digest(user='user', pwd='pass')
        url = 'http://httpbin.org/digest-auth/auth/user/pass/' + authtype

        r = Http.get(url)
        #assert r.cookies['fake'] == 'fake_value'

        r = Http.get(url, auth=auth)
        assert r.status_code == 200

@test
def check_DIGEST_AUTH_SETS_SESSION_COOKIES(request):
    for authtype in digest_auth_algo:
        auth = Http.auth.digest(user='user', pwd='pass')
        url = 'http://httpbin.org/digest-auth/auth/user/pass/' + authtype + '/never'

        s = Http.session()
        s.get(url, auth=auth)
        assert s.cookies['fake'] == 'fake_value'
        
        
@test
def check_DIGESTAUTH_WRONG_HTTP_401_GET(request):

    for authtype in digest_auth_algo:
        auth = Http.auth.digest(user='user', pwd='wrongpass')
        url = 'http://httpbin.org/digest-auth/auth/user/pass/' + authtype

        r = Http.get(url, auth=auth)
        assert r.status_code == 401

        r = Http.get(url)
        assert r.status_code == 401
        print(r.headers['WWW-Authenticate'])

        s = Http.session(auth=auth)
        r = s.get(url)
        assert r.status_code == 401

@test
def check_DIGESTAUTH_QUOTES_QOP_VALUE(request):

    for authtype in digest_auth_algo:
        auth = Http.auth.digest(user='user', pwd='wrongpass')
        url = 'http://httpbin.org/digest-auth/auth/user/pass/' + authtype

        r = Http.get(url, auth=auth)
        assert '"auth"' in r.request.headers['Authorization']
