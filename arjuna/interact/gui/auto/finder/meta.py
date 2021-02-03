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

from arjuna.tpi.helper.arjtype import CIStringDict

from arjuna.tpi.constant import *
from arjuna.core.constant import *
from arjuna.core.utils.repr_utils import repr_dict
from arjuna.tpi.tracker import track

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

    def __setitem__(self, name, value):
        if isinstance(name, GuiInteractionConfigType):
            self.__settings[k] = value
        else:
            self._settings[GuiInteractionConfigType[name.upper()]] = value

    @classmethod
    def is_a_setting(cls, name):
        if isinstance(name, GuiInteractionConfigType):
            return True
        else:
            try:
                GuiInteractionConfigType[name.upper()]
                return True
            except:
                return False


    def __str__(self):
        return repr_dict(self.__settings)

class Meta:
    _ALLOWED_FILTERS = {
        GuiWidgetType.ELEMENT: {'pos'},
        GuiWidgetType.MULTI_ELEMENT: {'pos'},
        GuiWidgetType.DROPDOWN: {'pos'},
        GuiWidgetType.RADIO_GROUP: set(),
    }

    _POS = {"first", "last", "random", "odd", "even"}

    @track("trace")
    def __init__(self, mdict=None):
        from arjuna import log_debug
        temp_dict = not mdict and CIStringDict() or CIStringDict(mdict)
        self.__mdict = CIStringDict()
        self.__process_type(temp_dict)
        self.__process_relations(temp_dict)
        self.__process_filters(temp_dict)
        self.__process_settings(temp_dict)
        log_debug("Meta dictionary is: {}".format(repr_dict(self.__mdict)))

    def __process_type(self, temp_dict):
        from arjuna import log_debug
        from arjuna.core.constant import GuiWidgetType
        if "type" in temp_dict:
            log_debug("Copying provided type from meta dict: {}".format(temp_dict["type"]))
            try:
                widget_type = temp_dict["type"]
                if not isinstance(widget_type, GuiWidgetType):
                    self.__mdict["type"] = GuiWidgetType[widget_type.upper()]
                else:
                    self.__mdict["type"] = temp_dict["type"]
            except Exception as e:
                raise Exception("{} is not a valid Gui widget type.".format(widget_type))
        else:
            self.__mdict["type"] = GuiWidgetType.ELEMENT

    def __process_relations(self, temp_dict):
        from arjuna import log_debug
        self.__mdict["relations"] = CIStringDict()
        to_remove = list()
        for k,v in temp_dict.items():
            if k.lower() in {'above', 'below', 'left_of', 'right_of', 'near'}:
                 
                to_remove.append(k)
        for k in to_remove:
            del temp_dict[k]

        if "relations" in temp_dict:
            self.__mdict["relations"].update(temp_dict["relations"])
            del temp_dict["relations"]

        from arjuna.tpi.guiauto.base.single_widget import SingleGuiWidget
        from arjuna.tpi.error import GuiWidgetDefinitionError

        for k,v in self.__mdict["relations"].items():
            self.__set_relation(k, v)

    def __process_filters(self, temp_dict):
        from arjuna import log_debug
        self.__mdict["filters"] = CIStringDict()
        to_remove = list()
        for k,v in temp_dict.items():
            if k.lower() in {'pos'}:
                self.__set_filter(k,v)
                to_remove.append(k)
        for k in to_remove:
            del temp_dict[k]
        if "filters" in temp_dict:
            self.__mdict["filters"].update(temp_dict["filters"])
            del temp_dict["filters"]

    def __process_settings(self, temp_dict):
        self.__mdict["settings"] = InteractionConfig(temp_dict) # Interconfig keys are removed

    def update_settings(self, source_wmd):
        self.settings.update(source_wmd.meta.settings)

    def items(self):
        return self.__mdict.items()

    def has(self, name):
        return name.lower() in self.__mdict

    @track("trace")
    def __getattr__(self, name):
        return self[name]

    def __getitem__(self, name):
        if self.has(name):
            return self.__mdict[name]
        else:
            return None

    def __set_relation(self, name, value):
        from arjuna.tpi.guiauto.base.single_widget import SingleGuiWidget
        if isinstance(value, SingleGuiWidget):
            value = value.dispatcher.driver_element
        self.__mdict["relations"][name] = value

    def __format_pos(self, pos):
        from arjuna.tpi.helper.extract import pos as pos_factory
        from arjuna.tpi.helper.extract import Extractor
        if self.__mdict["type"] == GuiWidgetType.RADIO_GROUP:
            raise Exception(">>pos<< filter is not supported for Gui Widget Type RADIO_GROUP.")
        if type(pos) is str:
            fpos = pos.lower().strip()
            if fpos in self._POS:
                return pos_factory._create_extractor(fpos)
            else:
                raise Exception("The only string liternals support for defining position are first/last/random")
        elif type(pos) in {list, tuple}:
            return pos_factory.at(*[int(str(i).strip()) for i in pos])
        elif type(pos) is dict:
            if len(pos) > 1:
                raise Exception("Extractor specification dictionary can take only one root key. Found entry: {}".format(pos))
            extractor_name = list(pos.keys())[0].lower().strip()
            extractor_args = list(pos.values())[0]
            if type(extractor_args) in {list, tuple}:
                return pos_factory._create_extractor(extractor_name, *extractor_args)
            elif type(extractor_args) is dict:
                return pos_factory._create_extractor(extractor_name, **extractor_args)
            else:
                return pos_factory._create_extractor(extractor_name, extractor_args)
        elif isinstance(pos, Extractor):
            return pos
        else:
            try:
                return pos_factory.at(int(str(pos).lower().strip()))
            except:
                raise Exception("Value of pos is not of any allowed type. It can be an int, a list of ints, an extractor specification dictionary or an Extractor object.")          

    def __set_filter(self, name, value):
        allowed_filters = self._ALLOWED_FILTERS[self.__mdict['type']]
        if name not in allowed_filters:
            raise Exception("{} is not allowed filter meta data for GuiWidget of type: {}. Allowed: {}".format(k, self.__mdict['type'], allowed_filters))
        if name == "pos":
            self.__mdict["filters"][name] = self.__format_pos(value)
        else:
            self.__mdict["filters"][name] = value

    def __setitem__(self, name, value):
        if InteractionConfig.is_a_setting(name):
            self["settings"][name] = value
        elif name.lower() in {"above", "below", "near", "right_of", "left_of"}:
            self.__set_relation(name, value)
        elif name.lower() in {"pos", "slice"}:
            self.__set_filter(name, value)
        else:
            self.__mdict[name] = value

    def __str__(self):
        return repr_dict(self.__mdict)


    