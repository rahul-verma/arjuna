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

from arjuna import *

@test
def check_default_containers(request):
    assert hasattr(request, 'info') is True
    info = request.info

    assert hasattr(info, 'qual_name') is True
    assert info.qual_name == 'arjex.test.pkg.rules.check_rules_08_request_object_population.check_default_containers'

    assert hasattr(info, 'package') is True
    assert info.package == 'arjex.test.pkg.rules'

    assert hasattr(info, 'module') is True
    assert info.module == 'check_rules_08_request_object_population'

    assert hasattr(info, 'name') is True
    assert info.name == 'check_default_containers'

    assert hasattr(info, 'id') is True
    assert info.id == info.qual_name

    assert hasattr(info, 'priority') is True
    assert info.priority == 5

    assert hasattr(info, 'author') is True   
    assert info.author is None

    assert hasattr(info, 'idea') is True   
    assert info.idea is None

    assert hasattr(info, 'unstable') is True   
    assert info.unstable is False

    assert hasattr(info, 'component') is True   
    assert info.component is None

    assert hasattr(info, 'app_version') is True   
    assert info.app_version == "0.0.0"

    assert hasattr(info, 'level') is True   
    assert info.level == None

    assert hasattr(info, 'reviewed') is True   
    assert info.reviewed is False

    assert hasattr(request, 'tags') is True
    assert request.tags == set()

    assert hasattr(request, 'bugs') is True
    assert request.bugs == set()

    assert hasattr(request, 'envs') is True
    assert request.envs == set()


@test(
    id="abc",
    priority=3,
    author="Rahul",
    idea='Sample idea',
    unstable=True,
    component="TestComp",
    app_version="1.2",
    level="TestLevel",
    reviewed=True,
    tags={'t1', 'T2'},
    bugs={'B1', 'b2'},
    envs={'EnV1', '     enV2     '},
    rating=2
)
def check_updated_containers(request):
    assert hasattr(request, 'info') is True
    info = request.info

    assert hasattr(info, 'qual_name') is True
    assert info.qual_name == 'arjex.test.pkg.rules.check_rules_08_request_object_population.check_updated_containers'

    assert hasattr(info, 'package') is True
    assert info.package == 'arjex.test.pkg.rules'

    assert hasattr(info, 'module') is True
    assert info.module == 'check_rules_08_request_object_population'

    assert hasattr(info, 'name') is True
    assert info.name == 'check_updated_containers'

    assert hasattr(info, 'id') is True
    assert info.id == 'abc'

    assert hasattr(info, 'priority') is True
    assert info.priority == 3

    assert hasattr(info, 'author') is True   
    assert info.author == 'Rahul'

    assert hasattr(info, 'idea') is True   
    assert info.idea == 'Sample idea'

    assert hasattr(info, 'unstable') is True   
    assert info.unstable is True

    assert hasattr(info, 'component') is True   
    assert info.component == "TestComp"

    assert hasattr(info, 'app_version') is True   
    assert info.app_version == "1.2"

    assert hasattr(info, 'level') is True   
    assert info.level == "TestLevel"

    assert hasattr(info, 'reviewed') is True   
    assert info.reviewed is True

    assert hasattr(request, 'tags') is True
    assert request.tags == {'t1', 't2'}

    assert hasattr(request, 'bugs') is True
    assert request.bugs == {'b1', 'b2'}

    assert hasattr(request, 'envs') is True
    assert request.envs == {'env1', 'env2'}

    # User Defined
    assert hasattr(request.info, 'rating') is True
    assert request.info.rating == 2


@test
def check_case_insensitivity_for_tags_and_attrs(request):
    raise Exception("Test to be implemented.")