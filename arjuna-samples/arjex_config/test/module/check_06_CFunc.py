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
def check_config_retrieval_C(request):
    print(C(ArjunaOption.BROWSER_NAME))
    print(C("browser.name"))
    print(C("BROWSER_NAME"))

@test
def check_conf_name_wise_query(request):
    cb = request.config.builder
    cb.browser_name = BrowserName.FIREFOX
    mconf = cb.register("nconf")

    print(C("browser.name"))
    print(C("reference.browser.name"))
    print(C("reference.browser_name"))
    print(C("nconf.browser_name"))
    print(C("nconf.browser.name"))