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

from arjuna.tpi.helper.arjtype import CIStringDict

from arjuna.tpi.constant import *
from arjuna.core.constant import *
from arjuna.core.utils.repr_utils import repr_dict

class InteractionConfig:

    def __init__(self, meta_dict):
        self.__settings = {
            GuiInteractionConfigType.CHECK_TYPE: True,
            GuiInteractionConfigType.CHECK_PRE_STATE : True,
            GuiInteractionConfigType.CHECK_POST_STATE : True,
            GuiInteractionConfigType.SCROLL_TO_VIEW : False,
        }   

        loaded = []
        for k,v in meta_dict.items():
            try:
                if isinstance(k, GuiInteractionConfigType):
                    self.__settings[k] = v
                else:
                    self._settings[GuiInteractionConfigType[k.upper()]] = v
                loaded.append(k)
            except:
                pass

        for l in loaded:
            del meta_dict[l]

    def should_check_type(self):
        return self.__settings[GuiInteractionConfigType.CHECK_TYPE]

    def should_check_pre_state(self):
        return self.__settings[GuiInteractionConfigType.CHECK_PRE_STATE]

    def should_check_post_state(self):
        return self.__settings[GuiInteractionConfigType.CHECK_POST_STATE]

    def should_scroll_to_view(self):
        return self.__settings[GuiInteractionConfigType.SCROLL_TO_VIEW]

    def __str__(self):
        return repr_dict(self.__settings)

class Meta:

    def __init__(self, mdict=None):
        self.__mdict = not mdict and CIStringDict() or CIStringDict(mdict)
        from arjuna.core.constant import GuiWidgetType
        if "type" in self.__mdict:
            try:
                widget_type = self.__mdict["type"]
                if not isinstance(widget_type, GuiWidgetType):
                    self.__mdict["type"] = GuiWidgetType[widget_type.upper()]
            except Exception as e:
                raise Exception("{} is not a valid Gui widget type.".format(widget_type))
        else:
            self.__mdict["type"] = GuiWidgetType.ELEMENT
        self.__mdict["settings"] = InteractionConfig(self.__mdict) # Interconfig keys are removed

    def update_settings(self, source_wmd):
        self.settings.update(source_wmd.meta.settings)

    def items(self):
        return self.__mdict.items()

    def has(self, name):
        return name.lower() in self.__mdict

    def __getattr__(self, name):
        return self[name]

    def __getitem__(self, name):
        if self.has(name):
            return self.__mdict[name]
        else:
            return None

    def __setitem__(self, name, value):
        self.__mdict[name] = value

    def __str__(self):
        return repr_dict(self.__mdict)

    