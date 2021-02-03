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
def check_pretty_url(request, httpbin):
    r = httpbin.get('/', abc=1, pretty_url=True)
    assert r.request.url == 'http://httpbin.org/abc/1'