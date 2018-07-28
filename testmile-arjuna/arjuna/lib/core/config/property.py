'''
This file is a part of Test Mile Arjuna
Copyright 2018 Test Mile Software Testing Pvt Ltd

Website: www.TestMile.com
Email: support [at] testmile.com
Creator: Rahul Verma

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

import copy

from arjuna.lib.core.enums import *
from arjuna.lib.core.enums import *

class ConfigPropertyMetaData:
    def __init__(self, definer, code_name, path, expected_value_type, level, text, override, visible):
        self.definer = definer  # "User_defined";
        self.code = code_name;
        self.path = path;
        self.value_type = expected_value_type  # ValueTypeEnum.STRING;
        self.level = level  # ConfigPropertyLevelEnum.CENTRAL;
        self.text = text;
        self.overridable = override  # true;
        self.visible = visible  # true;


class ConfigProperty:
    def __init__(self, code_name, path, value, text,
                 visible=True, expected_value_type=ValueTypeEnum.STRING,
                 level=ConfigPropertyLevelEnum.CENTRAL, definer="User_defined", override=True):
        self._cpm = ConfigPropertyMetaData(definer, code_name, path, expected_value_type, level, text, override,
                                           visible)
        self._prop_value = value

    def __getattr__(self, name):
        if name == "value":
            return vars(self)['_prop_value']
        else:
            return vars(self._cpm)[name]

    def __setattr__(self, name, value):
        if name in ['_cpm', '_prop_value', 'types', 'value']:
            if name == 'value':
                vars(self)['_prop_value'] = value
            else:
                vars(self)[name] = value
        else:
            setattr(self._cpm, name, value)

    def clone(self):
        return copy.deepcopy(self)

    def get_meta_data(self):
        return self._cpm
