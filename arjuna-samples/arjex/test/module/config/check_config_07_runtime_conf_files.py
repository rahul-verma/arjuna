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
def check_data_conf(request):

    assert Arjuna.get_config("data1").check == "data1"
    assert Arjuna.get_config("data2").check == "data2"

    assert C("data1.check") == "data1"
    assert C("data2.check") == "data2"

@test
def check_env_conf(request):

    assert Arjuna.get_config("env1").app_url == "https://env1"
    assert Arjuna.get_config("env2").app_url == "https://env2"

    assert C("env1.app.url") == "https://env1"
    assert C("env2.app.url") == "https://env2"

@test
def check_default_data_env_update(request):

    conf = Arjuna.get_config()
    assert conf.roption == 1
    assert conf.eoption == 1

    assert C("roption") == 1
    assert C("eoption") == 1

@test
def check_data_env_confs_with_getconf(request):

    d1e1 = Arjuna.get_config("data1_env1")
    d1e2 = Arjuna.get_config("data1_env2")
    d2e1 = Arjuna.get_config("data2_env1")
    d2e2 = Arjuna.get_config("data2_env2")

    print(d1e1.check)
    print(d1e2.check)
    print(d2e1.check)
    print(d2e2.check)    

    print(d1e1.app_url)
    print(d1e2.app_url)
    print(d2e1.app_url)
    print(d2e2.app_url)

    # print(re.user) -> Not present
    print(d1e1.user)
    print(d1e2.user)
    print(d2e1.user)
    print(d2e2.user)

    assert  d1e1 is request.get_config("data1_env1")

@test
def check_data_env_confs_with_CFunc(request):
    print(C("data_env.browser_name"))
    print(C("data.browser_name"))
    print(C("env.browser_name"))

    print(C("data1.browser_name"))
    print(C("env1.browser_name"))

    print(C("data1_env1.browser_name"))


@test
def check_default_conf(request):
    '''
        With and without the -c switch the result should vary.
    '''
    print(C("app.url"))