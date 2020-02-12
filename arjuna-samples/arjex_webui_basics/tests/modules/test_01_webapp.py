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
def test_webpp_nobase_url(my, request):
    google = WebApp()
    google.launch(blank_slate=True)
    google.ui.browser.go_to_url("https://google.com")
    my.asserter.assertEqual("Google", google.ui.main_window.title)
    google.quit()


@test
def test_webpp_base_url_arg(my, request):
    google = WebApp(base_url="https://google.com")
    google.launch()
    my.asserter.assertEqual("Google", google.ui.main_window.title)
    google.quit()

@test
def test_webpp_base_url_in_custom_config(my, request):
    context = Arjuna.get_run_context()
    cc = context.config_creator
    cc.arjuna_option(ArjunaOption.AUT_BASE_URL, "https://google.com")
    cc.register()

    google = WebApp(config=context.get_config())
    google.launch()
    my.asserter.assertEqual("Google", google.ui.main_window.title)
    google.quit()
