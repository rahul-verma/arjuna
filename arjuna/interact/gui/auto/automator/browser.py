# This file is a part of Arjuna
# Copyright 2015-2021 Rahul Verma

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

from arjuna.tpi.constant import ArjunaOption

from arjuna.core.poller.conditions import *
from arjuna.core.poller.caller import *
from arjuna.tpi.tracker import track

class BrowserConditions:

    def __init__(self, browser):
        self.__browser = browser

    @property
    def gui(self):
        return self.__gui

    def DocumentReadyState(self):
        caller = DynamicCaller(self.__browser.is_document_ready)
        return BooleanCondition(caller)

@track("info")
class Browser:

    def __init__(self, automator):
        self.__automator = automator
        self.__conditions = BrowserConditions(self)

    def is_document_ready(self):
        return self.execute_javascript("return document.readyState") == "complete"

    def go_to_url(self, url):
        self.__automator.dispatcher.go_to_url(url=url)
        self.__conditions.DocumentReadyState().wait()

    def go_back(self):
        self.__automator.dispatcher.go_back_in_browser()
        self.__conditions.DocumentReadyState().wait()

    def go_forward(self):
        self.__automator.dispatcher.go_forward_in_browser()
        self.__conditions.DocumentReadyState().wait()

    def refresh(self, hard=False):
        if hard:
            self.__automator.execute_javascript("window.location.reload(true);")
        else:
            self.__automator.execute_javascript("window.location.reload(false);")
        self.__conditions.DocumentReadyState().wait()

    def execute_javascript(self, js, *args):
        return self.__automator.dispatcher.execute_javascript(js, *args)