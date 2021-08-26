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
import pytest

from requests.exceptions import *
from arjuna import *

@test
def check_whitespaces_are_removed_from_url(request):
    service = Http.service(url="  http://httpbin.org  ")
    resp = service.get('/ ')
    assert resp.request.url == 'http://httpbin.org/'

@test
def check_slash_added(request):
    service = Http.service(url="  http://httpbin.org  ")
    resp = service.get('abc')
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
    service = Http.service(url=f"{data.scheme}httpbin.org")
    resp = service.get('/', xcodes=200, strict=True)

@test(drive_with=records(
    # Connecting to an unknown domain should raise a ConnectionError
    record(url='http://doesnotexist.google.com', exception=HttpConnectError),
    # Connecting to an invalid port should raise a ConnectionError
    record(url='http://localhost:1', exception=HttpConnectError),
    # Inputing a URL that cannot be parsed should raise an InvalidURL error
    record(url='http://fe80::5054:ff:fe5a:fc0', exception=HttpRequestCreationError)
))
def check_errors(request, data):
    with pytest.raises(data.exception):
        Http.service().get(data.url, timeout=1)