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

def __activity(config=None):
    browser = GuiApp(url="https://google.com", config=config)
    browser.launch()
    browser.network_recorder.start()
    browser.network_recorder.current_title = "Test Mile"
    browser.go_to_url("http://testmile.com")
    browser.network_recorder.stop()
    browser.quit()

@test
def check_explicit_capture_rec_off_auto_off_pass(request):
    # Recording Disabled. Auto recording is off. Filter is on. Inclusion for passed is off.
    # Test passes, no network packets in report.
    __activity()

@test
def check_explicit_capture_rec_off_auto_off_fail(request):
    # Recording Disabled. Auto recording is off. Filter is on. Inclusion for passed is off.
    # Test fails, no network packets in report.
    __activity()
    1/0

@test
def check_explicit_capture_rec_on_auto_off_pass(request):
    # Recording Enabled. Auto recording is off. Filter is on. Inclusion for passed is off.
    # Test passes, no network packets in report.
    cb = request.config.builder
    cb["browser.network.recorder.enabled"] = True
    config = cb.register()

    __activity(config)

@test
def check_explicit_capture_rec_on_auto_off_fail(request):
    # Recording Enabled. Auto recording is off. Filter is on. Inclusion for passed is off.
    # Test passes, network packets SHOULD be seen in report.
    cb = request.config.builder
    cb["browser.network.recorder.enabled"] = True
    config = cb.register()

    __activity(config)
    1/0

@test
def check_explicit_capture_rec_off_auto_on_pass(request):
    # Recording Disabled. Auto recording is on. Filter is on. Inclusion for passed is off.
    # Test passes, no network packets in report.
    cb = request.config.builder
    cb["browser.network.recorder.automatic"] = True
    config = cb.register()

    __activity(config)

@test
def check_explicit_capture_rec_off_auto_on_fail(request):
    # Recording Disabled. Auto recording is on. Filter is on. Inclusion for passed is off.
    # Test fails, no network packets in report.
    cb = request.config.builder
    cb["browser.network.recorder.automatic"] = True
    config = cb.register()

    __activity(config)
    1/0

@test
def check_explicit_capture_rec_on_auto_on_pass(request):
    # Recording Disabled. Auto recording is on. Filter is on. Inclusion for passed is off.
    # Test passes, no network packets in report.
    cb = request.config.builder
    cb["browser.network.recorder.enabled"] = True
    cb["browser.network.recorder.automatic"] = True
    config = cb.register()

    __activity(config)

@test
def check_explicit_capture_rec_on_auto_on_fail(request):
    # Recording Disabled. Auto recording is on. Filter is on. Inclusion for passed is off.
    # Test fails, no network packets in report.
    cb = request.config.builder
    cb["browser.network.recorder.enabled"] = True
    cb["browser.network.recorder.automatic"] = True
    config = cb.register()

    __activity(config)
    1/0


@test
def check_explicit_capture_rec_on_auto_on_pass(request):
    # Recording Disabled. Auto recording is on. Filter is on. Inclusion for passed is off.
    # Test passes, no network packets in report.
    cb = request.config.builder
    cb["browser.network.recorder.enabled"] = True
    cb["browser.network.recorder.automatic"] = True
    config = cb.register()

    __activity(config)