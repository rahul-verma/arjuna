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
from arjuna.tpi.parser.yaml import Yaml

@test
def check_xml_nodelocator_01(request):
    l1 = Xml.node_locator(tags="form", id="login-form")
    print(l1)
    l2 = Xml.node_locator(tags="input", name="requestId")
    print(l2)
    l3 = Xml.node_locator(tags="input", name="csrf-token")
    print(l3)
