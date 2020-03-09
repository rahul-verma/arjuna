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

    tenv1 = Arjuna.get_config("tenv1")
    tenv2 = Arjuna.get_config("tenv2")

    print(tenv1.browser_name)
    print(tenv2.browser_name)

    print(tenv1.app_url)
    print(tenv2.app_url)

    print(tenv1.user)
    print(tenv2.user)

    tenv1 = request.get_config("tenv1")
    tenv2 = request.get_config("tenv2")

    print(tenv1.browser_name)
    print(tenv2.browser_name)

    print(tenv1.app_url)
    print(tenv2.app_url)

    print(tenv1.user)
    print(tenv2.user)


@test
def check_env_confs_with_CFunc(request):
    print(C("tenv1.browser_name"))
    print(C("tenv2.browser_name"))

    print(C("tenv1.app_url"))
    print(C("tenv2.app_url"))

    print(C("tenv1.user"))
    print(C("tenv2.user"))


@test
def check_runenv_cli(request):
    '''
        Pass --run-env tenv2 in CLI
    '''

    conf = Arjuna.get_config()
    print(conf.browser_name)
    print(conf.app_url)
    print(conf.user)

    print(C("browser.name"))
    print(C("app.url"))
    print(C("user"))


@test
def check_runconf_cli(request):
    '''
        Pass --run-conf <path of dynamic.conf> in CLI
    '''

    conf = Arjuna.get_config()
    print(conf.browser_name)
    print(conf.app_url)
    print(conf.user)

    print(C("browser.name"))
    print(C("app.url"))
    print(C("user"))


@test
def check_runenv_runconf_cli(request):
    '''
        Pass --run-env tenv2 --run-conf <path of dynamic.conf> in CLI
    '''

    conf = Arjuna.get_config()
    print(conf.browser_name)
    print(conf.app_url)
    print(conf.user)
    print(conf.pwd)

    print(C("browser.name"))
    print(C("app.url"))
    print(C("user"))
    print(C("pwd"))
    
