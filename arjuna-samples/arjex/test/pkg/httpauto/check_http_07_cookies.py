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

# The tests are based on tests for requests library in https://github.com/psf/requests

import io

from arjuna import *

@test
def check_set_cookie_on_301(request):
    s = Http.session(url="http://httpbin.org")
    s.get('cookies/set?foo=bar')
    assert s.cookies['foo'] == 'bar'

@test
def check_cookie_sent_on_redirect(request):
    s = Http.session(url="http://httpbin.org")
    s.get('cookies/set?foo=bar')
    r = s.get('/redirect/1')
    assert s.cookies['foo'] == 'bar'
    assert 'Cookie' in r.request.headers

@test
def check_cookie_removed_on_expire(request):
    s = Http.session(url="http://httpbin.org")
    s.get('cookies/set?foo=bar')
    assert s.cookies['foo'] == 'bar'
    s.get(
        'response-headers',
        query_params={
            'Set-Cookie':
                'foo=deleted; expires=Thu, 01-Jan-1970 00:00:01 GMT'
        }
    )
    assert 'foo' not in s.cookies

@test
def check_cookie_persists_via_api(request):
    s = Http.session(url="http://httpbin.org")
    r = s.get('/redirect/1', cookies={'foo': 'bar'})
    assert 'foo' in r.request.headers['Cookie']
    assert 'foo' in r.redir_history[0].request.headers['Cookie']

@test
def check_request_cookie_overrides_session_cookie(request):
    s = Http.session(url="http://httpbin.org")
    s.add_cookies({'foo': 'bar'})
    r = s.get('/cookies', cookies={'foo': 'baz'})
    # Session cookie should not be modified
    assert s.cookies['foo'] == 'bar'

@test
def check_request_cookies_not_persisted(request):
    s = Http.session(url="http://httpbin.org")
    r = s.get('/cookies', cookies={'foo': 'baz'})
    # Sending a request with cookies should not add cookies to the session
    assert not s.cookies