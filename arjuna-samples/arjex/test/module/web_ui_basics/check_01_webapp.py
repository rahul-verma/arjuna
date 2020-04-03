# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from arjuna import *

@test
def check_webpp_nobase_url(request):
    google = GuiApp()
    google.launch(blank_slate=True)
    google.go_to_url("https://google.com")
    request.asserter.assert_equal("Google", google.title, "GuiPage title does not match.")
    google.quit()

@test
def check_webpp_base_url_arg(request):
    google = GuiApp(base_url="https://google.com")
    google.launch()
    request.asserter.assert_equal("Google", google.title, "GuiPage title does not match.")
    google.quit()

@test
def check_webpp_base_url_in_custom_config(request):
    cb = request.config.builder
    cb[ArjunaOption.APP_URL] = "https://google.com"
    conf = cb.register()

    google = GuiApp(config=conf)
    google.launch()
    request.asserter.assert_equal("Google", google.title, "GuiPage title does not match.")
    google.quit()
