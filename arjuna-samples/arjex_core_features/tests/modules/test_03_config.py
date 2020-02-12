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
def test_config_retrieval(my, request):
    config = Arjuna.get_ref_config()

    wait_value = config.get_arjuna_option_value(ArjunaOption.GUIAUTO_MAX_WAIT)
    print(wait_value.as_int())

    wait_value = config.get_arjuna_option_value("GUIAUTO_MAX_WAIT")
    print(wait_value.as_int())

    wait_value = config.get_arjuna_option_value("GuIAuTo_MaX_WaIt")
    print(wait_value.as_int())

    wait_value = config.get_arjuna_option_value("guiauto.max.wait")
    print(wait_value.as_int())

    wait_value = config.get_arjuna_option_value("guiauto.max.wait")
    print(wait_value.as_int())

    wait_time = config.guiauto_max_wait
    print(wait_time)

    should_maximize_browser = config.get_arjuna_option_value(ArjunaOption.BROWSER_MAXIMIZE)
    print(should_maximize_browser.as_bool())

@test
def test_update_config(my, request):
    context = Arjuna.get_run_context()
    cc = context.config_creator
    cc.arjuna_option(ArjunaOption.BROWSER_NAME, BrowserName.FIREFOX)
    cc.register()

    google = WebApp(base_url="https://google.com", config=context.get_config())
    google.launch()
    my.asserter.assertEqual("Google", google.ui.main_window.title)
    google.quit()

@test
def test_simpler_builder_method(my, request):
    context = Arjuna.get_run_context()
    cc = context.config_creator
    cc.firefox()
    cc.register()

    google = WebApp(base_url="https://google.com", config=context.get_config())
    google.launch()
    my.asserter.assertEqual("Google", google.ui.main_window.title)
    google.quit()


@test
def test_project_conf(my, request):
    '''
        For this test:
        You must add browser.name = firefox to arjunaOptions in project.conf to see the impact.
        It changes the default browser from Chrome to Firefox across the project.
    '''
    google = WebApp(base_url="https://google.com")
    google.launch()
    my.asserter.assertEqual("Google", google.ui.main_window.title)
    google.quit()