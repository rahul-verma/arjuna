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


from arjuna.tpi.constant import *
from arjuna.core.constant import *
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

    @property
    def arjuna_options(self):
        return self.__option_map["ao"]

    @property
    def user_options(self):
        return self.__option_map["uo"]

    def as_map(self):
        return {
            "arjuna_options": self.arjuna_options,
            "user_options": self.user_options,
        }
