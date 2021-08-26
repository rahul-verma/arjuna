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

@test
def check_http_custom_headers(request, httpbin):
    heads = {'User-agent': 'Mozilla/5.0'}

    r = httpbin.get('/user-agent', headers=heads)

    assert heads['User-agent'] in r.text
    assert r.status_code == 200

@test
def check_http_headers_mixed_params(request, httpbin):
    heads = {'User-agent': 'Mozilla/5.0'}

    r = httpbin.get('/get?test=true', query_params={'q': 'test'}, something=3, headers=heads)
    assert r.status_code == 200
    assert r.request.url == "http://httpbin.org/get?test=true&q=test&something=3"

@test
def check_headers_on_session_with_None_are_not_sent(request, httpbin):
    """Do not send headers in Session.headers with None values."""
    s = Http.service(url="http://httpbin.org", headers={'Accept-Encoding': None})
    req = s.get('/get')
    assert 'Accept-Encoding' not in req.headers


@test(drive_with=records(
    record(agent_key='User-agent'),
    record(agent_key='user-agent'),
))
def check_user_agent_transfers(request, httpbin, data):
    headers = {data.agent_key: 'Mozilla/5.0 (github.com/psf/requests)'}
    r = httpbin.get('/user-agent', headers=headers)
    assert data.agent_key in r.request.headers
    assert headers[data.agent_key] == r.request.headers[data.agent_key]
