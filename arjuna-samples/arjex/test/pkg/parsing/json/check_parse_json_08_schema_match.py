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
def check_assert_schema_1(request):
    obj1 = {
        "id": 1,
        "arr": [1,2]
    }

    obj2 = {
        "id": 3,
        "arr": ["str"]
    }

    Json.from_object(obj2).assert_match_schema(obj1, msg="dummy")