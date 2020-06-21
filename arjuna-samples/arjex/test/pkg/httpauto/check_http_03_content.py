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
def check_binary_put(request):
    resp = Http.put('http://example.com/',  content=Http.content.utf8(u"ööö"))
    assert isinstance(resp.request.content, bytes)

@test
def check_multipart_file(request):
    url = "http://httpbin.org/post"
    Http.post(url, content="")

    post1 = Http.post(url, content={'some': 'data'})
    assert post1.status_code == 200

    post2 = Http.post(url, content=Http.content.file('fname', "sample.txt", headers={'X-A': 'b'}))
    assert post2.status_code == 200

@test
def check_multipart_files_and_fields(request):
    url = "http://httpbin.org/post"

    r = Http.post(url, content=Http.content.multipart(
        {'a': 1, 'b': 3},
        Http.field('fname', "sample.txt", is_file=True),
        {'a': 1, 'b': 3},
        Http.field('c', 'something')
    ))
    assert r.status_code == 200