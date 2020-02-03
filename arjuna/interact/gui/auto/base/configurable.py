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

from arjuna.core.enums import GuiInteractionConfigType

class Configurable:

    def __init__(self, gui, iconfig=None):
        self.__settings = {
            GuiInteractionConfigType.CHECK_TYPE: True,
            GuiInteractionConfigType.CHECK_PRE_STATE : True,
            GuiInteractionConfigType.CHECK_POST_STATE : True,
            GuiInteractionConfigType.SCROLL_TO_VIEW : False,
        }

        if iconfig:
            iconfig = type(iconfig) is dict and iconfig or iconfig.settings
            self.__settings.update(iconfig)

    @property
    def settings(self):
        return self.__settings

    def _should_check_type(self):
        return self.settings[GuiInteractionConfigType.CHECK_TYPE]

    def _should_check_pre_state(self):
        return self.settings[GuiInteractionConfigType.CHECK_PRE_STATE]

    def _should_check_post_state(self):
        return self.settings[GuiInteractionConfigType.CHECK_POST_STATE]

    def _should_scroll_to_view(self):
        return self.settings[GuiInteractionConfigType.SCROLL_TO_VIEW]