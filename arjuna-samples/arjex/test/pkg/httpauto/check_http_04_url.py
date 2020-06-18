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
