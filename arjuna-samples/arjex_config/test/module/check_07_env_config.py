'''
This file is a part of Arjuna
Copyright 2015-2020 Rahul Verma

Website: www.RahulVerma.net

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from arjuna import *

@test
def check_env_confs_with_conf(request):

    print(Arjuna.get_config("tenv1").browser_name)
    print(Arjuna.get_config("tenv2").browser_name)

    print(Arjuna.get_config("tenv1").aut_base_url)
    print(Arjuna.get_config("tenv2").aut_base_url)

    print(Arjuna.get_config("tenv1").user)
    print(Arjuna.get_config("tenv2").user)


@test
def check_env_confs_with_CFunc(request):
    print(C("tenv1.browser_name"))
    print(C("tenv2.browser_name"))

    print(C("tenv1.aut_base_url"))
    print(C("tenv2.aut_base_url"))

    print(C("tenv1.user"))
    print(C("tenv2.user"))


@test
def check_runenv_cli(request):
    '''
        Pass --run-env tenv2 in CLI
    '''

    print(Arjuna.get_config().browser_name)
    print(C("browser.name"))

    print(Arjuna.get_config().aut_base_url)
    print(Arjuna.get_config().user)

    print(C("aut.base.url"))
    print(C("user"))


@test
def check_runconf_cli(request):
    '''
        Pass --run-conf <path of dynamic.conf> in CLI
    '''

    print(Arjuna.get_config().browser_name)
    print(C("browser.name"))

    print(Arjuna.get_config().aut_base_url)
    print(Arjuna.get_config().user)

    print(C("aut.base.url"))
    print(C("user"))


@test
def check_runenv_runconf_cli(request):
    '''
        Pass --run-env tenv2 --run-conf <path of dynamic.conf> in CLI
    '''

    print(Arjuna.get_config().browser_name)
    print(C("browser.name"))

    print(Arjuna.get_config().aut_base_url)
    print(Arjuna.get_config().user)

    print(C("aut.base.url"))
    print(C("user"))

    print(Arjuna.get_config().pwd)
    print(C("pwd"))
    
