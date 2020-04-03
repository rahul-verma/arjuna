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

from arjuna.tpi.enums import ArjunaOption
from enum import Enum, auto


class ViewContextHandler:

    def __init__(self, automator):
        self.__automator = automator

    @property
    def automator(self):
        return self.__automator

    def switch_to_view_context(self, view_name):
        self._act(TestAutomatorActionBodyCreator.switch_to_view_context(view_name))

    def get_current_view_context(self):
        response = self._act(TestAutomatorActionBodyCreator.get_current_view_context())
        return response["data"]["viewContext"]

    def get_all_view_contexts(self):
        response = self._act(TestAutomatorActionBodyCreator.get_all_view_contexts())
        return response["data"]["viewContexts"]

    def switch_to_native_view(self):
        self.switch_to_view_context(MobileView.NATIVE_APP.name)

    def switch_to_web_view(self, pkg):
        self.switch_to_view_context(
            "{}_{}".format(MobileView.WEBVIEW.name, pkg)
        )

    def switch_to_first_web_view(self):
        for context_name in self.get_all_view_contexts():
            if context_name.find(MobileView.WEBVIEW.name) != -1:
                self.switch_to_view_context(context_name)
                break

    def _does_name_represent_web_view(self, view_name):
        return view_name.lower().find(MobileView.WEBVIEW.name.lower()) != -1 

    def is_web_view(self):
        return self._does_name_represent_web_view(self.get_current_view_context())

    def is_native_view(self):
        return self.get_current_view_context().lower() == MobileView.WEBVIEW.name.lower()