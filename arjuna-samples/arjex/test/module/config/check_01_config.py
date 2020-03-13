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

'''
Code is kept redundant across methods for the purpose of easier learning.
'''

@test
def check_ref_config_retrieval(request):
    config = Arjuna.get_config()
    print(config.name)

    config = request.config
    print(config.name)

@test
def check_config_value_retrieval(request):
    config = request.config

    print(config.value(ArjunaOption.BROWSER_NAME))

    print(config.value("BROWSER_NAME"))
    print(config.value("BrOwSeR_NaMe"))
    print(config.value("browser.name"))
    print(config.value("Browser.Name"))

    print(config["browser.name"])

    print(config.browser_name)