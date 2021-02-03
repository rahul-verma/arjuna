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

from arjuna.core.constant import ConfigStage

class Configurator:

    def __init__(self):
        self.__arjuna = None

    @property
    def _arjuna(self):
        return self.__arjuna

    @_arjuna.setter
    def _arjuna(self, singleton):
        self.__arjuna = singleton

    def builder(self, *, base_config: str="ref") -> 'ConfigBuilder':
        '''
            Creates a configuration builder object which takes the provided configuration as its basis.

            Keyword Arguments:
                base_config: The base `Configuration` object. All its options become a part of the new configuration. Its options can be overriden and new options can be added using the builder to create a new **Configuration** object. Default is reference configuration in CLI.

            Returns:
                **new** `ConfigBuilder` object
        '''
        from arjuna import Arjuna
        from arjuna.tpi.config import ConfigBuilder
        return ConfigBuilder(base_config=Arjuna.get_config(name=base_config), auto_name_gen=False, _conf_stage=ConfigStage.REFERENCE)
