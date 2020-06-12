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

'''
    Run these tests with -ao report.network.always true to see network capture for passed tests
'''

@for_test
def browser_1(request):
    cb = request.config.builder
    cb["browser.network.recorder.enabled"] = True
    config = cb.register()

    browser = GuiApp(url="https://google.com", config=config)
    browser.launch()

    request.space.network_recorder = browser.network_recorder

    browser.network_recorder.record("Test Mile")
    browser.go_to_url("http://testmile.com")
    yield
    browser.quit()

@for_test
def browser_2(request):
    cb = request.config.builder
    cb["browser.network.recorder.enabled"] = True
    cb["browser.network.recorder.automatic"] = True
    config = cb.register()

    browser = GuiApp(url="https://google.com", config=config)
    browser.launch()

    request.space.network_recorder = browser.network_recorder

    browser.network_recorder.record("Test Mile")
    browser.go_to_url("http://testmile.com")
    yield
    browser.quit()

@test
def check_recording_auto_off_pass(request, browser_1):
    # No network traffic
    pass

@test
def check_recording_auto_on_pass(request, browser_2):
    # No network traffic
    pass

@test
def check_recording_auto_off_fail(request, browser_1):
    1/0

@test
def check_recording_auto_on_fail(request, browser_2):
    1/0