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