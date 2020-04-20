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
def check_default_run_env_update(request):

    conf = Arjuna.get_config()
    assert conf.roption is 1
    assert conf.eoption is 1

    assert C("roption") is 1
    assert C("eoption") is 1

@test
def check_run_env_confs_with_getconf(request):

    r1e1 = Arjuna.get_config("run1_tenv1")
    r1e2 = Arjuna.get_config("run1_tenv2")
    r2e1 = Arjuna.get_config("run2_tenv1")
    r2e2 = Arjuna.get_config("run2_tenv2")

    print(r1e1.check)
    print(r1e2.check)
    print(r2e1.check)
    print(r2e2.check)    

    print(r1e1.app_url)
    print(r1e2.app_url)
    print(r2e1.app_url)
    print(r2e2.app_url)

    # print(re.user) -> Not present
    print(r1e1.user)
    print(r1e2.user)
    print(r2e1.user)
    print(r2e2.user)

    assert  r1e1 is request.get_config("run1_tenv1")

@test
def check_run_env_confs_with_CFunc(request):
    print(C("run_env.browser_name"))
    print(C("run1_env.browser_name"))
    print(C("run1_tenv1.browser_name"))
    print(C("run_tenv1.browser_name"))

    print(C("run_env.browser.name"))
    print(C("run1_env.browser.name"))
    print(C("run1_tenv1.browser.name"))
    print(C("run_tenv1.browser.name"))


@test
def check_default_conf(request):
    '''
        With and without the -c switch the result should vary.
    '''
    print(C("app.url"))