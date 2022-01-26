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
def check_temp_http(request, httpbin):
    s = Http.service(url="https://google.com")
    s.send()
    for c,v in s.parsed_cookies.items():
        print(c, v.secure, v.httponly)

@test
def check_HTTP_200_OK_HEAD(request, httpbin):
    r = httpbin.head('/get')
    assert r.status_code == 200

@test
def check_HTTP_200_OK_PUT(request, httpbin):
    r = httpbin.put('/put', content="")
    assert r.status_code == 200

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
        record(method='PATCH')
    )
)
def check_no_body_content_length(request, data, httpbin):
    resp = getattr(httpbin, data.method.lower())("/")

@test(
    drive_with = records(
        record(method='POST'),
        record(method='PUT'),
        record(method='PATCH')
    )
)
def check_no_body_content_length_json_content_type(request, data, httpbin):
    resp = getattr(httpbin, data.method.lower())("/", content=Http.content.json())

@test(
    drive_with = records(
        record(method='POST'),
        record(method='PUT'),
        record(method='PATCH')
    )
)
def check_no_body_content_length_with_svc_json_content_handler(request, data):
    svc = Http.service(url="http://httpbin.org", request_content_handler=Http.content.json)
    resp = getattr(svc, data.method.lower())("/")