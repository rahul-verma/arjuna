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
def check_proxy_default(request):
    # any proxy related error (address resolution, no route to host, etc) should result in a ProxyError
    s = Http.service()
    r = s.get('https://www.google.com')
    print(r.text)

@test
def check_proxy_valid(request):
    # any proxy related error (address resolution, no route to host, etc) should result in a ProxyError
    s = Http.service(proxy=Http.proxy('localhost', 8080))
    r = s.get('https://www.google.com')
    print(r.text)

@test
def check_proxy_error(request):
    # any proxy related error (address resolution, no route to host, etc) should result in a ProxyError
    with pytest.raises(HttpConnectError):
        s = Http.service(proxy=Http.proxy('non-resolvable-address'))
        s.get('http://httpbin.org')

@test
def check_proxy_error_on_bad_url(request):
    with pytest.raises(HttpConnectError):
        s = Http.service(proxy=Http.proxy('badproxyurl',3128))
        s.get("https://httpbing.org")

    with pytest.raises(HttpConnectError):
        s = Http.service(proxy=Http.proxy('/example.com'))
        s.get("http://httpbing.org")