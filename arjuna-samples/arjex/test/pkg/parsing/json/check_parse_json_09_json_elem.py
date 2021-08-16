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

# The tests are based on tests for jsonpath-rw-ext in https://github.com/wolverdude/GenSON

from arjuna import *


@test
def check_json_assert_delitem(request):
    obj1 = {
        "id": 1,
        "arr": [1,2]
    }

    j1 = Json.from_object(obj1)
    del j1["id"]
    print(j1)
    assert ("id" in j1) == False

@test
def check_assert_match_01(request):
    obj1 = {
        "id": 1,
        "arr": [1,2]
    }

    obj2 = {
        "id": 1,
        "arr": [1,2]
    }

    d = {
        "id": 1,
        "arr": [1,2]
    }

    j1 = Json.from_object(obj1)
    j2 = Json.from_object(obj2)

    j1.assert_match(j2, msg="Jdict not matched")
    j1.assert_match(d,  msg="pydict not matched")

@test(xfail=True)
def check_assert_match_02_xfail(request):
    obj1 = {
        "id": 1,
        "arr": [1,2]
    }

    obj2 = {
        "id": 2,
        "arr": [1,2]
    }

    j1 = Json.from_object(obj1)
    j2 = Json.from_object(obj2)

    j1.assert_match(j2, msg="Jdict scalar matched.")

@test(xfail=True)
def check_assert_match_03_xfail(request):
    obj1 = {
        "id": 1,
        "arr": [1,2]
    }

    obj2 = {
        "id": 2,
        "arr": [1,3]
    }

    j1 = Json.from_object(obj1)
    j2 = Json.from_object(obj2)

    j1.assert_match(j2, msg="Jdict arr content matched.")

@test
def check_assert_match_04_ikeys(request):
    obj1 = {
        "id": 1,
        "arr": [1,2]
    }

    obj2 = {
        "id": 2,
        "arr": [1,2]
    }

    j1 = Json.from_object(obj1)
    j2 = Json.from_object(obj2)

    j1.assert_match(j2, ignore_keys="id", msg="Jdict scalar matched.")

@test
def check_assert_match_04_ikeys(request):
    obj1 = {
        "id": 1,
        "arr": [1,2],
        "child": {
            "id": 1,
            "val": 5
        },
        "child2": {
            "id": 1,
            "val": 5
        },
        "child3": {
            "id": 1,
            "val": 5
        },
        "child4": {
            "gchild": {
                "id": 10,
                "val": 20
            }
        }
    }

    obj2 = {
        "id": 2,
        "arr": [1,2],
        "child": {
            "id": 2,
            "val": 5
        },
        "child2": {
            "id": 1,
            "val": 5
        },
        "child3": {
            "id": 4,
            "val": 5
        },
        "child4": {
            "gchild": {
                "id": 20,
                "val": 20
            }
        }
    }

    j1 = Json.from_object(obj1)
    j2 = Json.from_object(obj2)

    j1.assert_match(j2, ignore={"id", "child.id", "child3.id", "child4.gchild.id"}, msg="Jdict scalar matched.")


@test
def check_assert_match_05_user_submitted_01(request):
    obj1 = {
                "name": 'Thorshammer',
                "debNum": '11111',
                "subdomain": 'sub',
                "sDebNum": '11111',
            }

    obj2 = {
        "id": "632b6b68-fe70-11eb-b27b-96000028c1ce",
        "name": "Thorshammer",
        "debNum": None,
        "domain": "sub.something.com",
        "list": [],
        "host": "somehost",
        "sDebNum": "11111",
        "fid": 540,
        "subdomain": "sub"
    }

    j1 = Json.from_object(obj1)
    j2 = Json.from_object(obj2)

    j1.assert_match(j2, ignore=['id', 'debNum', 'domain', 'list', 'host', 'fid'], msg="Jdict scalar matched.")
    j2.assert_match(j1, ignore=['id', 'debNum', 'domain', 'list', 'host', 'fid'], msg="Jdict scalar matched.")

@test(xfail=True)
def check_assert_match_05_diffkeys_01(request):
    '''
        obj2 has extra key. obj1 matching with obj2.
    '''

    obj1 = {
                "a": 'a1',
                "b": 'b1',
                "c": 'c1'
            }

    obj2 = {
                "a": 'a1',
                "b": 'b1',
                "c": 'c1',
                "d": 'd1',
            }

    j1 = Json.from_object(obj1)
    j2 = Json.from_object(obj2)

    j1.assert_match(j2, msg="Extraneous key found.")

@test(xfail=True)
def check_assert_match_05_diffkeys_02(request):
    '''
        obj2 has extra key. obj2 matching with obj1.
    '''

    obj1 = {
                "a": 'a1',
                "b": 'b1',
                "c": 'c1'
            }

    obj2 = {
                "a": 'a1',
                "b": 'b1',
                "c": 'c1',
                "d": 'd1',
            }

    j1 = Json.from_object(obj1)
    j2 = Json.from_object(obj2)

    j2.assert_match(j1, msg="Missing key.")

@test
def check_assert_match_05_diffkeys_03(request):
    '''
        obj2 has extra key. obj1 matching with obj2. Using ignore.
    '''

    obj1 = {
                "a": 'a1',
                "b": 'b1',
                "c": 'c1'
            }

    obj2 = {
                "a": 'a1',
                "b": 'b1',
                "c": 'c1',
                "d": 'd1',
            }

    j1 = Json.from_object(obj1)
    j2 = Json.from_object(obj2)

    j1.assert_match(j2, ignore=["d"], msg="Extraneous key found.")

@test
def check_assert_match_05_diffkeys_04(request):
    '''
        obj2 has extra key. obj2 matching with obj1. Using ignore.
    '''

    obj1 = {
                "a": 'a1',
                "b": 'b1',
                "c": 'c1'
            }

    obj2 = {
                "a": 'a1',
                "b": 'b1',
                "c": 'c1',
                "d": 'd1',
            }

    j1 = Json.from_object(obj1)
    j2 = Json.from_object(obj2)

    j2.assert_match(j1, ignore=["d"], msg="Missing key.")