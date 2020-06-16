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

@for_module
def httpbin(request):
    yield HttpSession(url="http://httpbin.org")

@for_module
def httpsbin(request):
    yield HttpSession(url="https://httpbin.org")

@test(
    drive_with = records(
        record(method='GET'),
        record(method='HEAD'),
    )
)
def check_get_head(request, data, httpbin):
    resp = getattr(httpbin, data.method.lower())("/")
    resp.request.assert_header_mismatch('Content-Length', msg="GET/HEAD should not have content length header.")


@test(
    drive_with = records(
        record(method='POST'),
        record(method='PUT'),
        record(method='PATCH'),
        record(method='OPTIONS'),
    )
)
def check_no_body_content_length(request, data, httpbin):
    resp = getattr(httpbin, data.method.lower())("/", content="")
    resp.request.assert_empty_content(msg="Empty content request should have content length as 0.")


@test(
    drive_with=records(
        record(url='http://example.com/path#fragment', expected='http://example.com/path?a=b#fragment'),
        record(url='http://example.com/path?key=value#fragment', expected='http://example.com/path?key=value&a=b#fragment')
    )
)
def check_params_are_added_before_fragment(request, data, httpbin):
    resp = httpbin.get(data.url, a="b")
    assert resp.request.url == data.expected

@test
def check_params_original_order_is_preserved_by_default(request, httpbin):
    resp = httpbin.get('http://example.com/', z=1, a=1, k=1)
    assert resp.request.url == 'http://example.com/?z=1&a=1&k=1'

@test
def check_query_params(request, httpbin):
    resp = httpbin.get('http://example.com/', query_params={'z':1, 'a':1, 'k':1})
    assert resp.request.url == 'http://example.com/?z=1&a=1&k=1'

@test
def check_query_params_override_with_named(request, httpbin):
    resp = httpbin.get('http://example.com/', query_params={'z':1, 'a':1, 'k':1}, z=5, y=2)
    assert resp.request.url == 'http://example.com/?z=5&a=1&k=1&y=2'

@test
def check_binary_put(request, httpbin):
    resp = httpbin.put('http://example.com/',  content=u"ööö".encode("utf-8"), content_type="text/html")
    assert isinstance(resp.request.content, bytes)

@test
def check_whitespaces_are_removed_from_url(request):
    session = HttpSession(url="  http://httpbin.org  ")
    resp = session.get('/ ')
    assert resp.request.url == 'http://httpbin.org/'

@test
def check_slash_added(request):
    session = HttpSession(url="  http://httpbin.org  ")
    resp = session.get('abc')
    assert resp.request.url == 'http://httpbin.org/abc'

@test(
    drive_with=records(
        record(scheme='http://'),
        record(scheme='HTTP://'),
        record(scheme='hTTp://'),
        record(scheme='HttP://')
    )
)
def check_mixed_case_scheme_acceptable(request, data):
    session = HttpSession(url=f"{data.scheme}httpbin.org")
    resp = session.get('/', xcodes=200, strict=True)

@test
def check_pretty_url(request, httpbin):
    r = httpbin.get('/', abc=1, pretty_url=True)
    assert r.request.url == 'http://httpbin.org/abc/1'

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
        requests allows up to 20 redirects
    '''
    try:
        httpbin.get('/', query_params={'relative-redirect' : 50}, pretty_url=True)
    except HttpSendError as e:
        assert e.request.url == 'http://httpbin.org/relative-redirect/50'
        assert e.response.url == 'http://httpbin.org/relative-redirect/20'
        assert len(e.response.redir_history) == 30
    else:
        raise AssertionError('Expected redirect to raise HttpSendError but it did not')