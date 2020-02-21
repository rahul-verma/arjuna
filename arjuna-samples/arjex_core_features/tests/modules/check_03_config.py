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
def check_config_retrieval(request):
    config = Arjuna.get_ref_config()

    wait_value = config.get_arjuna_option_value(ArjunaOption.BROWSER_NAME)
    print(wait_value.as_str())

    wait_value = config.get_arjuna_option_value("BROWSER_NAME")
    print(wait_value.as_str())

    wait_value = config.get_arjuna_option_value("BrOwSeR_NaMe")
    print(wait_value.as_str())

    wait_value = config.get_arjuna_option_value("browser.name")
    print(wait_value.as_str())

    wait_value = config.get_arjuna_option_value("Browser.Name")
    print(wait_value.as_str())

    browser = config.browser_name
    print(browser)


@test
def check_project_conf(request):
    '''
        For this test:
        You must add browser.name = firefox to arjunaOptions in project.conf to see the impact.
        It changes the default browser from Chrome to Firefox across the project.
    '''
    google = WebApp(base_url="https://google.com")
    google.launch()
    my.asserter.assert_equal("Google", google.title, "Page title")
    google.quit()


@test
def check_update_config(request):
    context = Arjuna.get_run_context()
    cc = context.config_creator
    cc.arjuna_option(ArjunaOption.BROWSER_NAME, BrowserName.FIREFOX)
    cc.register()

    google = WebApp(base_url="https://google.com", config=context.get_config())
    google.launch()
    my.asserter.assert_equal("Google", google.title, "Page title")
    google.quit()

@test
def check_simpler_builder_method(request):
    context = Arjuna.get_run_context()
    cc = context.config_creator
    cc.firefox()
    cc.register()

    google = WebApp(base_url="https://google.com", config=context.get_config())
    google.launch()
    my.asserter.assert_equal("Google", google.title, "Page title")
    google.quit()


@test
def check_user_options(request):
    '''
        For this test:
        You must add target.url = "https://google.com" to userOptions in project.conf to see the impact.
    '''
    context = Arjuna.get_run_context()
    cc = context.config_creator
    cc.user_option("target.title", "Google")
    cc.register()

    config = context.get_config()

    url = config.get_user_option_value("target.url").as_str()
    title = config.get_user_option_value("target.title").as_str()

    google = WebApp(base_url=url, config=config)
    google.launch()
    my.asserter.assert_equal(title, google.title, "Page Title")
    google.quit()