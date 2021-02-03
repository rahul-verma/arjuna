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

'''
Provides configuration related public classes.

Provides the Configuration and ConfigBuilder classes.

Configuration class represents the immutable, read-only configuration object.

ConfigBuilder can be used to create new configuration from an existing one.
'''

from enum import Enum
from arjuna.tpi.constant import *
from arjuna.core.constant import *
import uuid
from arjuna.tpi.arjuna_types import *
from typing import *


class _ROWrapper:

    def __init__(self, config):
        self.__config = config

    def value(self, option):
        return self.__config.value(option)

    def items(self):
        return self.__config.items()

from arjuna.tpi.tracker import track

class Configuration:
    '''
        Read-only, immutable object that contains a fixed mapping of ArjunaOptions and User defined options.

        Args:
            test_session: Current test session object.
            name: Name of this configuration.
            config: WrappedConfiguration object. Configuration provides a read-only interface on top of it.

        Note:
            - You never directly create a Configuration object.
            - It is an outcome of configuration processing that Arjuna does.

        Note:
            - The option name string is considered by Arjuna as **case-insensitive**. Also, **. (dot)** and **_ (underscore)** are interchangeable. So, following are equivalent arguments
                - ArjunaOption.BROWSER_NAME
                - BROWSER_NAME
                - BrOwSeR_NaMe
                - browser.name
                - Browser.Name
                - and so on

        Note:
            You can also use **. notation** or **[] dict notation** to retrieve an option value.

            .. code-block:: python

                config.option
                config[option]
    '''

    def __init__(self, test_session: 'TestSession', name: str, config: 'WrappedConfiguration'):
        super().__init__()
        self.__session = test_session
        self.__name = name
        self.__wrapped_config = config
        self.__arjuna_options = _ROWrapper(self.__wrapped_config.arjuna_options)
        self.__user_options = _ROWrapper(self.__wrapped_config.user_options)

    @property
    def builder(self) -> 'ConfigBuilder':
        '''
            Creates a configuration builder object which takes this configuration as its reference.

            Returns:
                **new** `ConfigBuilder` object
        '''
        return ConfigBuilder(base_config=self)

    def value(self, option: ArjunaOptionOrStr) -> Any:
        '''
            Get the value of a configuration option.

            Args:
                option: An ArjunaOption or a string representing ArjunaOption or a user defined option.

            Returns:
                Object of any type, depending on the option.
        '''
        try:
            return self.__arjuna_options.value(option)
        except:
            try:
                return self.__user_options.value(option)
            except:
                raise Exception("No config option with name '{}' found in {} configuration.".format(option, self.name))

    @property
    def _wrapped_config(self):
        return self.__wrapped_config

    @property
    def test_session(self) -> 'TestSession':
        '''
            Test Session object for this Configuration.
        '''
        return self.__session

    def get_arjuna_options_as_map(self) -> Dict[ArjunaOptionOrStr, Any]:
        '''
            Get all Arjuna options.

            Returns:
                A dictionary of all Arjuna Options.
        '''
        return self.__wrapped_config.arjuna_options.as_dict()

    def is_arjuna_option_not_set(self, option) -> bool:
        '''
            Check if the value for an Arjuna option was set. (Checks for 'not_set' string.)

            Args:
                option: An ArjunaOption or a string representing ArjunaOption or a user defined option.

            Returns:
                True/False
        '''
        return self.__wrapped_config.arjuna_options.is_not_set(option)

    @property
    def name(self) -> str:
        '''
            Name of this configuration object.

            Returns:
                Name of this configuration
        '''
        return self.__name

    def __getattr__(self, name):
        return self.value(name)

    def __getitem__(self, name):
        return self.value(name)

    def __call__(self, name):
        return self.value(name)

    def as_dict(self) -> Dict[str, Any]:
        '''
            Get all options.

            Returns:
                A dictionary of all Arjuna Options and User Defined Options
        '''
        return self.__wrapped_config.as_dict()

    def __str__(self):
        return self.name

@track("trace")
class ConfigBuilder:
    '''
        Helps in constructing a new **Configuration** object from an existing one.

        Keyword Arguments:
            base_config: Parent configuration to be used be used as reference for creation of the new Configuration object.
            auto_gen_name: Generate a unique configuration name in **build** call if name is not provided. Default is True.

        Note:
            It is not meant to be directly constructed. Use **builder** method of a Configuration object to create the associated ConfigBuilder object.

        Note:
            You can also use **. notation** or **[] dict notation** to add/update an option value.

            .. code-block:: python

                builder.option = value
                builder[option] = value
    '''

    def __init__(self, *, base_config: Configuration, auto_name_gen=True, _conf_stage=ConfigStage.CODED):
        from arjuna.configure.options import EditableConfig
        vars(self)['_test_session'] = base_config.test_session
        vars(self)['_config_container'] = EditableConfig.empty_conf()
        vars(self)['_base_config'] = base_config
        vars(self)['_auto_gen_name'] = auto_name_gen
        vars(self)['_conf_stage'] = _conf_stage

    def option(self, option: ArjunaOptionOrStr, obj: Any) -> 'self':
        '''
            Add/Change option value.

            Args:
                option: An ArjunaOption or a string representing ArjunaOption or a user defined option.
                obj: An object of any type as per the option key.

            Returns:
                Current `ConfigBuilder` object
        '''
        self._config_container.set_option(option, obj)
        return self

    def __setattr__(self, option, obj) -> 'self':
        '''
            Enables **. notation** for setting option value. Same as **option** method.
        '''
        self.option(option, obj)
        return self

    def __setitem__(self, option, obj) -> 'self':
        '''
            Enables **[] dict notation** for setting option value. Same as **option** method.
        '''
        self.option(option, obj)
        return self

    def options(self, option_map: Dict[ArjunaOptionOrStr, Any]) -> 'self':
        '''
            Add/Change multiple option values.

            Args:
                option_map: A dictionary of options. Keys are ArjunaOptions or strings and values can be of any type as per the option key.

            Returns:
                Current `ConfigBuilder` object
        '''
        self._config_container.set_options(option_map)
        return self

    def selenium(self) -> 'self':
        '''
            Configure Selenium as the automation engine.

            Returns:
                Current `ConfigBuilder` object
        '''
        self.set_option(ArjunaOption.GUIAUTO_NAME, GuiAutomatorName.SELENIUM)
        return self

    def appium(self, context) -> 'self':
        '''
            (Not supported yet) Configure Appium as the automation engine.

            Returns:
                Current `ConfigBuilder` object
        '''
        self.option(ArjunaOption.GUIAUTO_NAME, GuiAutomatorName.APPIUM)
        self.option(ArjunaOption.GUIAUTO_CONTEXT, context)
        return self

    def chrome(self) -> 'self':
        '''
            Configure Chrome as the browser.

            Returns:
                Current `ConfigBuilder` object
        '''
        self.option(ArjunaOption.BROWSER_NAME, BrowserName.CHROME)
        return self

    def firefox(self) -> 'self':
        '''
            Configure Firefox as the browser.

            Returns:
                Current `ConfigBuilder` object
        '''
        self.option(ArjunaOption.BROWSER_NAME, BrowserName.FIREFOX)
        return self

    def app(self, path) -> 'self':
        '''
            (Not supported yet) Configure path for mobile app installer.

            Args:
                path: Absolute path of mobile app on test machine.

            Returns:
                Current `ConfigBuilder` object
        '''
        self.option(ArjunaOption.MOBILE_APP_FILE_PATH, path)
        return self

    def from_file(self, fpath) -> 'self':
        '''
            Add all options from a .conf file.

            Args:
                fpath: Path of .conf file. 

            Returns:
                Current `ConfigBuilder` object

            Note:
                If instead of full absolute path, a name or relative file path is provided, Arjuna creates the path in relation to the default configuration directory - **<Project Root>/config**.
        '''
        conf = self._test_session.load_options_from_file(fpath, conf_stage=self._conf_stage)
        for k,v in conf.arjuna_options.as_dict().items():
            self._config_container.set_arjuna_option(k,v)
        for k,v in conf.user_options.as_dict().items():
            self._config_container.set_user_option(k,v)

    def register(self, *, config_name=None):
        '''
            Register the new configuration.

            Keyword Arguments:
                config_name: (Optional) Name that you want to assign to the configuration.

            Note:
                - Name needs to be unique in a test run. No configuration should exist with the same name.
                - A dynamic, unique name is generated if name is not provided.

        '''
        from arjuna import Arjuna, ConfigCreationError
        if config_name is None and not self._auto_gen_name:
            raise ConfigCreationError("This ConfigBuilder has been created with auto_gen_name setting as False. You must provide a config_name to the build call.")
        config_name = config_name and config_name or 'c{}'.format(str(uuid.uuid4()).replace("-","_"))

        try:
            from arjuna.configure.validator import Validator
            Validator.name(config_name)
        except:
            raise ConfigCreationError("Unsupported name >>{}<< provided for a Configuration object. {}".format(config_name, Validator.VNREGEX_TEXT))

        if Arjuna.has_config(config_name):
            raise ConfigCreationError("You can not re-register a configuration for a name. Config with name {} already exists.".format(config_name))

        config = self._test_session.register_config(config_name.lower(), 
                                        self._config_container.arjuna_options, #.items(),
                                        self._config_container.user_options, #.items(),
                                        conf_stage=self._conf_stage,
                                        parent_config=self._base_config
                                    )
        return config