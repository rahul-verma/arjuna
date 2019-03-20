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

from arjuna.lib.core import *
from arjuna.lib.core.adv.py import EnumSwitch
from arjuna.lib.core.config import config_utils
from arjuna.lib.core.config import property_factory
from arjuna.lib.core.config.builder import *
from arjuna.lib.core.reader.hocon import *
from arjuna.lib.core.types.named_strings import *

class AbstractComponentConfigurator(metaclass=abc.ABCMeta):
    def __init__(self, integrator, comp_name, prop_enum):
        self.base_dir = None
        self._integrator = integrator
        self.component_name = comp_name
        self.builder = ConfigPropertyBuilder()
        self.path_to_enum_map = {}
        self.enum_to_path_map = {}

        for e in list(prop_enum):
            path = config_utils.enum_to_prop_path(e)
            self.path_to_enum_map[path.upper()] = e
            self.enum_to_path_map[e] = path.upper()

    def _code_for_path(self, prop_path):
        return self.path_to_enum_map[prop_path.upper()]

    def does_path_map_contain(self, path):
        return path.upper() in self.path_to_enum_map

    def _handle_string_config(self, prop_path, config_value, purpose, visible):
        prop = property_factory.create_string_property(self._code_for_path(prop_path), prop_path, config_value, purpose,
                                                       visible)
        self.register_property(prop)

    def _handle_core_dir_path(self, prop_path, config_value, purpose, visible):
        prop = property_factory.create_core_dir_path(self._code_for_path(prop_path), prop_path, config_value, purpose,
                                                     visible)
        self.register_property(prop)

    def _handle_boolean_config(self, prop_path, config_value, purpose, visible):
        prop = property_factory.create_boolean_property(self._code_for_path(prop_path), prop_path, config_value,
                                                        purpose, visible)
        self.register_property(prop)

    def _handle_string_list_config(self, prop_path, config_value, purpose, visible):
        prop = property_factory.create_string_list_property(self._code_for_path(prop_path), prop_path, config_value, purpose, visible)
        self.register_property(prop)

    def register_property(self, prop):
        self._integrator.register_property(self.get_component_name(), prop)

    def get_component_name(self):
        return self.component_name

    def set_component_name(self, component_name):
        self.component_name = component_name

    def configure_messages(self, messages):
        self._integrator.populate_messages(messages)

    def configure_names(self, names):
        self._integrator.populate_names(names)

    @abc.abstractmethod
    def process_defaults(self):
        pass

    @abc.abstractmethod
    def process_conf_file_options(self, options):
        pass

    @abc.abstractmethod
    def process_interface_options(self, options):
        pass

    @abc.abstractmethod
    def load(self):
        pass
