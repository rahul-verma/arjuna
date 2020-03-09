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

@test
def check_config_retrieval_C(request):
    print(C(ArjunaOption.BROWSER_NAME))
    print(C("browser.name"))
    print(C("BROWSER_NAME"))

@test
def check_project_conf(request):
    '''
        For this test:
        You must add browser.name = firefox to arjunaOptions in project.conf to see the impact.
        It changes the default browser from Chrome to Firefox across the project.
    '''
    google = WebApp(base_url="https://google.com")
    google.launch()
    request.asserter.assert_equal("Google", google.title, "Page title does not match.")
    google.quit()


@test
def check_create_config(request):
    cb = request.config.builder
    cb.option(ArjunaOption.BROWSER_NAME, BrowserName.FIREFOX)
    # or
    cb.option("browser.name", BrowserName.FIREFOX)
    # or
    cb["browser_name"] = BrowserName.FIREFOX
    # or
    cb.browser_name = BrowserName.FIREFOX
    config = cb.register()

    google = WebApp(base_url="https://google.com", config=config)
    google.launch()
    request.asserter.assert_equal("Google", google.title, "Page title does not match.")
    google.quit()

@test
def check_named_config(request):
    cb = request.config.builder
    cb.browser_name = BrowserName.FIREFOX
    cb.register("my_config")

    config = Arjuna.get_config("my_config")
    print(config.name)

    config = request.get_config("my_config")
    print(config.name) 

    google = WebApp(base_url="https://google.com", config=config)
    google.launch()
    request.asserter.assert_equal("Google", google.title, "Page title does not match.")
    google.quit()

@test
def check_simpler_builder_method(request):
    cb = request.config.builder
    cb.firefox()
    config = cb.register()

    google = WebApp(base_url="https://google.com", config=config)
    google.launch()
    request.asserter.assert_equal("Google", google.title, "Page title does not match.")
    google.quit()


@test
def check_user_options(request):
    '''
        For this test:
        You must add target.url = "https://google.com" to userOptions in project.conf to see the impact.
    '''
    # Just like Arjuna options, C works for user options in reference config
    url = C("target.url")

    cb = request.config.builder
    cb.option("target.title", "Google")
    # or
    cb["target.title"] = "Google"
    # or
    cb.target_title = "Google"
    config = cb.register()

    title = config.target_title
    #or
    title = config["target.title"] # or config.value("target.title") or other variants seen earlier
    url = config.value("target.url") # Ref user options are available in new config as well.

    google = WebApp(base_url=url, config=config)
    google.launch()
    request.asserter.assert_equal(title, google.title, "Page title does not match.")
    google.quit()
