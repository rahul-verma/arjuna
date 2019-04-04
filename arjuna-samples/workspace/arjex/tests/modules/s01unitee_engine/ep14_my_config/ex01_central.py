'''
This file is a part of Test Mile Arjuna
Copyright 2018 Test Mile Software Testing Pvt Ltd

Website: www.TestMile.com
Email: support [at] testmile.com
Creator: Rahul Verma

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

from arjuna.tpi.markup import *
from arjuna.tpi.helpers import *
from arjuna.tpi.enums import ArjunaOption

@init_module
def setup_module(my):
    console.display(my.context.get_config().get_browser_type())
    my.context.ConfigBuilder().chrome().build("chrome_config")
    console.display(my.context.get_config("chrome_config").get_browser_type())


@test_function
def test_config_from_central(my):
    console.display(my.context.get_config("chrome_config").get_browser_type())
    console.display(my.context.get_config().get_browser_type())

    my.context.ConfigBuilder().firefox().build("firefox_config")

    console.display(my.context.get_config().get_browser_type())
    console.display(my.context.get_config("firefox_config").get_browser_type())
