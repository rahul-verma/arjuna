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
def check_302_redirect_get(request, httpbin):
    r = httpbin.get('/', redirect=1, pretty_url=True)
    assert r.status_code == 200
    assert r.redir_history[0].status_code == 302
    assert r.redir_history[0].is_redirect

@test
def check_307_redirect_POST(request, httpbin):
    r = httpbin.post('/redirect-to?url=post', content='test', content_type="text/html", status_code=307)
    assert r.status_code == 200
    assert r.redir_history[0].status_code == 307
    assert r.redir_history[0].is_redirect
    assert r.json['data'] == 'test'

@test
def check_http_307_redirect_post_with_seekable(request, httpbin):
    byte_str = b'test'
    r = httpbin.post('/redirect-to?url=post', content=io.BytesIO(byte_str), content_type="text/html", status_code=307)
    assert r.status_code == 200
    assert r.redir_history[0].status_code == 307
    assert r.redir_history[0].is_redirect
    assert r.json['data'] == byte_str.decode('utf-8')

@test
def check_too_many_redirects(request, httpbin):
    '''
        requests allows up to 30 redirects
    '''
    try:
        httpbin.get('/', query_params={'relative-redirect' : 50}, pretty_url=True)
    except HttpSendError as e:
        assert e.request.url == 'http://httpbin.org/relative-redirect/50'
        assert e.response.url == 'http://httpbin.org/relative-redirect/20'
        assert len(e.response.redir_history) == 30
    else:
        raise AssertionError('Expected redirect to raise HttpSendError but it did not')

@test
def check_too_many_redirects_custom_limit(request, httpbin):
    '''
        requests allows up to 20 redirects
    '''
    try:
        session = HttpSession(url="http://httpbin.org", max_redirects=5)
        session.get('/', query_params={'relative-redirect' : 50}, pretty_url=True)
    except HttpSendError as e:
        assert e.request.url == 'http://httpbin.org/relative-redirect/50'
        assert e.response.url == 'http://httpbin.org/relative-redirect/45'
        assert len(e.response.redir_history) == 5
    else:
        raise AssertionError('Expected redirect to raise HttpSendError but it did not')

@test
def check_http_301_changes_post_to_get(request, httpbin):
    r = httpbin.post("/", status=301, content="", pretty_url=True)
    assert r.status_code == 200
    assert r.request.method == 'GET'
    assert r.redir_history[0].status_code == 301
    assert r.redir_history[0].is_redirect

@test
def check_http_301_doesnt_change_head_to_get(request, httpbin):
    r = httpbin.head("/", status=301, content="", pretty_url=True)
    print(r.content)
    assert r.status_code == 200
    assert r.request.method == 'HEAD'
    assert r.redir_history[0].status_code == 301
    assert r.redir_history[0].is_redirect

@test
def check_http_302_changes_post_to_get(request, httpbin):
    r = httpbin.post("/", status=302, content="", pretty_url=True)
    assert r.status_code == 200
    assert r.request.method == 'GET'
    assert r.redir_history[0].status_code == 302
    assert r.redir_history[0].is_redirect

@test
def check_http_302_doesnt_change_head_to_get(request, httpbin):
    r = httpbin.head("/", status=302, content="", pretty_url=True)
    assert r.status_code == 200
    assert r.request.method == 'HEAD'
    assert r.redir_history[0].status_code == 302
    assert r.redir_history[0].is_redirect

@test
def check_http_303_changes_post_to_get(request, httpbin):
    r = httpbin.post("/", status=303, content="", pretty_url=True)
    assert r.status_code == 200
    assert r.request.method == 'GET'
    assert r.redir_history[0].status_code == 303
    assert r.redir_history[0].is_redirect

@test
def check_http_303_doesnt_change_head_to_get(request, httpbin):
    r = httpbin.head("/", status=303, content="", pretty_url=True)
    assert r.status_code == 200
    assert r.request.method == 'HEAD'
    assert r.redir_history[0].status_code == 303
    assert r.redir_history[0].is_redirect

@test
def check_fragment_maintained_on_redirect(request, httpbin):
    fragment = "#view=edit&token=hunter2"
    route = "/redirect-to?url=get" + fragment
    url = "http://httpbin.org" + route
    r = httpbin.get(route)

    assert len(r.redir_history) > 0
    assert r.redir_history[0].request.url == url
    assert r.url == "http://httpbin.org/get" + fragment
