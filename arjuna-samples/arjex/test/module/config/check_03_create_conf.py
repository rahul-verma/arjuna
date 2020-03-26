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

    google = GuiApp(base_url="https://google.com", config=config)
    google.launch()
    request.asserter.assert_equal("Google", google.title, "GuiPage title does not match.")
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

    google = GuiApp(base_url="https://google.com", config=config)
    google.launch()
    request.asserter.assert_equal("Google", google.title, "GuiPage title does not match.")
    google.quit()


@test
def check_simpler_builder_method(request):
    cb = request.config.builder
    cb.firefox()
    config = cb.register()

    google = GuiApp(base_url="https://google.com", config=config)
    google.launch()
    request.asserter.assert_equal("Google", google.title, "GuiPage title does not match.")
    google.quit()
