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
    record(msg="m01_default1"),
    record(msg=None),
    record(msg="m01_default2"),
    record(msg="m01_default3_onlyres"),
))
def check_msg_defaults(request, data, httpbin):
    if data.msg is not None:
        r = httpbin.send(data.msg)
    else:
        r = httpbin.send()

@test
def check_msg_default_with_dot(request, httpbin):
    httpbin.message.m01_default1.send()

@test(drive_with=records(
    record(msg="m02_200_ex"),
    record(msg="m02_404_unex"),
    record(msg="m02_404_ex"),
    record(msg="m01_default3_onlyres"),
))
def check_msg_basic(request, data, httpbin):
    r = httpbin.send(data.msg)

@test
def check_msg_basic_with_dot(request, httpbin):
    httpbin.message.m02_200_ex.send()

@test(xfail=True, drive_with=records(
    record(msg="m03_ex_fail"),
    record(msg="m03_unex_fail"),
))
def check_msg_fail(request, data, httpbin):
    r = httpbin.send(data.msg)

@test
def check_msg_simple_get_with_label(request, httpbin):
    r = httpbin.send('m04_label')

@test
def check_msg_params_and_fmting(request, httpbin):
    url = "http://example.com/path?key=value"
    r = httpbin.send('m05_params_fmt', url=url, param_str="a=b")

@test
def check_msg_params_and_fmting_with_dot(request, httpbin):
    url = "http://example.com/path?key=value"
    r = httpbin.message.m05_params_fmt.send(url=url, param_str="a=b")

@test
def check_msg_pretty_url(request, httpbin):
    url = "http://httpbin.org"
    r = httpbin.send('m05_params_pretty_url', url=url, param="a", val=1)

@test
def check_msg_pretty_url_with_dot(request, httpbin):
    url = "http://httpbin.org"
    r = httpbin.message.m05_params_pretty_url.send(url=url, param="a", val=1)

@test
def check_msg_post_str(request, httpbin):
    r = httpbin.send('m06_content01_str')

@test
def check_msg_post_urlencoded(request, httpbin):
    r = httpbin.send('m06_content02_urlencoded')

@test(drive_with=records(
    record(msg="m06_content03_json_req1"),
    record(msg="m06_content03_json_req2"),
    record(msg="m06_content03_json_req3"),
    record(msg="m06_content03_json_req4"),
    record(msg="m06_content03_json_req5"),
    record(msg="m06_content03_json_req6"),
    record(msg="m06_content03_json_req7"),
    record(msg="m06_content03_json_res1"),
    record(msg="m06_content03_json_res2"),
    record(msg="m06_content03_json_res3"),
    record(msg="m06_content03_json_res4"),
    record(msg="m06_content03_json_res5"),
))
def check_msg_post_json(request, data, httpbin):
    httpbin.send(data.msg)

@test(drive_with=records(
    record(msg="m06_content03_json_res6"),
    record(msg="m06_content03_json_res7"),
))
def check_msg_multiline_payload(request, data, httpbin):
    payload = {
      "str" : "b",
      "int": 1,
      "float": 1.1,
      "dict": {
          "a": "b"
      },
      "list": [1,2,3],
      "bool": True,
      "int_as_str": "1",
      "float_as_str": "1.2",
      "bool1_as_str": "true",
      "bool2_as_str": "True",
      "space": "what is this 1"
    }

    httpbin.send(data.msg, payload=payload)

@test(drive_with=records(
    record(msg="m07_headers_req1"),
    record(msg="m07_headers_res1"),
))
def check_msg_headers(request, data, httpbin):
    httpbin.send(data.msg)

@test(drive_with=records(
    record(msg="m08_cookies_1"),
))
def check_msg_cookies(request, data, httpbin):
    httpbin.send(data.msg)

@test(drive_with=records(
    record(msg="m08_text01"),
))
def check_msg_text(request, data, httpbin):
    httpbin.send(data.msg)

@test(xfail=True, drive_with=records(
    record(msg="m08_text02")
))
def check_msg_text(request, data, httpbin):
    httpbin.send(data.msg)

# SEAMful

@test
def check_root_message(request, httpbinseam):
    httpbinseam.message.m_200_ex.send()

@test
def check_message_store_1(request, httpbin):
    response = httpbin.message.m09_store_1.send()
    print(response.store)