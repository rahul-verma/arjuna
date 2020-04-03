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

import re
from enum import Enum, auto

class ConfigPropertyType(Enum):
	ARO = auto()
	ACO = auto()
	URO = auto()
	UCO = auto()

class CliArgsConfig:
    ARJ_PATTERN = re.compile("(?i)(aro|aco)\\s*:\\s*(\\S+)\\s*")
    USER_PATTERN = re.compile("(?i)(uro|uco)\\s*:\\s*(\\S+)\\s*")

    def __init__(self, options):
        self.__arj_options_map = {
            ConfigPropertyType.ARO : dict(),
            ConfigPropertyType.ACO : dict()
        }
        self.__user_options_map = {
            ConfigPropertyType.URO : dict(),
            ConfigPropertyType.UCO : dict()
        }

        for option in options:
            m = CliArgsConfig.ARJ_PATTERN.match(option.name)
            if m is not None:
                c_type = ConfigPropertyType[m.group(1).upper()]
                try:
                    arj_prop = m.group(2)
                except:
                    raise Exception("Empty Arjuna Option Key provided in CLI: {}".format(option.name))
                else:
                    try:
                        arj_option = Arjuna.normalise_arjuna_option(arj_prop)
                    except:
                        raise Exception("You have provided an invalid Arjuna Option in CLI: {}".format(option.name))
                    else:
                        self.__arj_options_map[c_type][arj_option] = option.value
                        continue

            m = CliArgsConfig.USER_PATTERN.match(option.name)
            if m is not None:
                c_type = ConfigPropertyType[m.group(1).upper()]
                try:
                    user_option = Arjuna.normalise_user_option(m.group(2))
                except:
                    raise Exception("Empty User Option key provided in CLI: {}".format(option.name))
                else:
                    self.__arj_options_map[c_type][user_option] = option.value
                    continue

    def as_map(self):
        map = dict()
        map["arjuna_reference_options"] = self.__get_arjuna_reference_options()
        map["arjuna_custom_options"] = self.__get_arjuna_custom_options()
        map["user_reference_options"] = self.__get_user_reference_options()
        map["user_reference_options"] = self.__get_user_custom_options()

    def __get_arjuna_reference_options(self):
        return self.__arj_options_map[ConfigPropertyType.ARO]

    def __get_arjuna_custom_options(self):
        return self.__arj_options_map[ConfigPropertyType.ACO]

    def __get_user_reference_options(self):
        return self.__arj_options_map[ConfigPropertyType.URO]

    def __get_user_custom_options(self):
        return self.__arj_options_map[ConfigPropertyType.UCO]


#### From old Setu code
from arjuna.tpi.enums import *
from arjuna.core.value import Value

class CliArgsConfig:

    def __init__(self, arg_dict):
        self.__option_map = {
            "ao" : dict(),
            "uo" : dict()
        }

        def update_map(otype, arg_dict):
            if otype in arg_dict:
                opt_list = arg_dict[otype]
                if opt_list is not None:
                    self.__option_map[otype].update(dict(arg_dict[otype]))
                del arg_dict[otype]
            else:
                self.__option_map[otype] = dict()
        
        update_map("ao", arg_dict)
        update_map("uo", arg_dict)
        self.__option_map["ao"].update(arg_dict)
        arg_dict.clear()

    def as_map(self):
        return {
            "arjunaOptions": self.__option_map["ao"],
            "userOptions": self.__option_map["uo"],
        }
