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


from enum import Enum
from arjuna.configure.impl.container import ConfigContainer
from arjuna.tpi.enums import *
import uuid

class ConfigBuilder:
    '''
        Helps in constructing a new `Configuration` object from an existing one.
    '''

    def __init__(self, test_session, parent_config):
        # vars(self)[__code_mode = code_mode
        vars(self)['_test_session'] = test_session
        vars(self)['_config_container'] = ConfigContainer()
        vars(self)['_parent_config'] = parent_config

    def option(self, option, obj):
        '''
            Add/Change option value.
        '''
        self._config_container.set_option(option, obj)
        return self

    def __setattr__(self, option, obj):
        self.option(option, obj)
        return self

    def __setitem__(self, option, obj):
        self.option(option, obj)
        return self

    def options(self, option_map):
        '''
            Add/Change multiple option values.
        '''
        self._config_container.set_options(option_map)
        return self

    def selenium(self):
        '''
            Configure Selenium as the automation engine.
        '''
        self.set_option(ArjunaOption.GUIAUTO_NAME, GuiAutomatorName.SELENIUM)
        return self

    def appium(self, context):
        '''
            (Not supported yet) Configure Appium as the automation engine.
        '''
        self.option(ArjunaOption.GUIAUTO_NAME, GuiAutomatorName.APPIUM)
        self.option(ArjunaOption.GUIAUTO_CONTEXT, context)
        return self

    def chrome(self):
        '''
            Configure Chrome as the browser.
        '''
        self.option(ArjunaOption.BROWSER_NAME, BrowserName.CHROME)
        return self

    def firefox(self):
        '''
            Configure Firefox as the browser.
        '''
        self.option(ArjunaOption.BROWSER_NAME, BrowserName.FIREFOX)
        return self

    def app(self, path):
        '''
            (Not supported yet) Configure path for mobile app installer.
        '''
        self.option(ArjunaOption.MOBILE_APP_FILE_PATH, path)
        return self

    def from_file(self, fpath):
        '''
            Add all options from a .conf file.
        '''
        conf = self._test_session.load_options_from_file(fpath)
        for k,v in conf.arjuna_config._config_dict.items():
            self._config_container.set_arjuna_option(k,v)
        for k,v in conf.user_config._config_dict.items():
            self._config_container.set_user_option(k,v)

    def register(self, config_name=None):
        '''
            Register the new configuration.
        '''
        from arjuna import Arjuna
        config_name = config_name and config_name or 'c{}'.format(str(uuid.uuid4()).replace("-","_"))
        if Arjuna.has_config(config_name):
            raise Exception("You can not re-register a configuration for a name. Config with name {} already exists.".format(config_name))

        config = self._test_session.register_config(config_name.lower(), 
                                        self._config_container.arjuna_options, #.items(),
                                        self._config_container.user_options, #.items(),
                                        self._parent_config
                                    )

        return config


class _ROWrapper:

    def __init__(self, config):
        self.__config = config

    def value(self, option):
        return self.__config.value(option)

class Configuration:

    def __init__(self, test_session, name, config):
        super().__init__()
        self.__session = test_session
        self.__name = name
        self.__wrapped_config = config
        self.__arjuna_options = _ROWrapper(self.__wrapped_config.arjuna_config)
        self.__user_options = _ROWrapper(self.__wrapped_config.user_config)

    @property
    def builder(self):
        return ConfigBuilder(self.__session, self)

    def value(self, name):
        try:
            return self.__arjuna_options.value(name)
        except:
            try:
                return self.__user_options.value(name)
            except:
                raise Exception("No config option with name {} found in {} configuration.".format(name, self.name))

    @property
    def _wrapped_config(self):
        return self.__wrapped_config

    @property
    def test_session(self):
        return self.__session

    def get_arjuna_options_as_map(self):
        return self.__wrapped_config.arjuna_config.as_json_dict()

    def is_arjuna_option_not_set(self, option):
        return self.__wrapped_config.arjuna_config.is_not_set(option)

    @property
    def name(self):
        return self.__name

    def __getattr__(self, name):
        return self.value(name)

    def __getitem__(self, name):
        return self.value(name)

    def __call__(self, name):
        return self.value(name)

    def as_map(self):
        return self.__wrapped_config.as_json_dict()