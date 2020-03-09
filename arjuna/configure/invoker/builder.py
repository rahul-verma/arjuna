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

from enum import Enum
from arjuna.configure.impl.container import ConfigContainer
from arjuna.core.enums import *
import uuid

class ConfigBuilder:

    def __init__(self, test_session, parent_config):
        # vars(self)[__code_mode = code_mode
        vars(self)['_test_session'] = test_session
        vars(self)['_config_container'] = ConfigContainer()
        vars(self)['_parent_config'] = parent_config

    def option(self, option, obj):
        self._config_container.set_option(option, obj)
        return self

    def __setattr__(self, option, obj):
        self.option(option, obj)
        return self

    def __setitem__(self, option, obj):
        self.option(option, obj)
        return self

    def options(self, option_map):
        self._config_container.set_options(option_map)
        return self

    def selenium(self):
        self.set_option(ArjunaOption.GUIAUTO_NAME, GuiAutomatorName.SELENIUM)
        return self

    def appium(self, context):
        self.option(ArjunaOption.GUIAUTO_NAME, GuiAutomatorName.APPIUM)
        self.option(ArjunaOption.GUIAUTO_CONTEXT, context)
        return self

    def chrome(self):
        self.option(ArjunaOption.BROWSER_NAME, BrowserName.CHROME)
        return self

    def firefox(self):
        self.option(ArjunaOption.BROWSER_NAME, BrowserName.FIREFOX)
        return self

    def app(self, path):
        self.option(ArjunaOption.MOBILE_APP_FILE_PATH, path)
        return self

    def from_file(self, fpath):
        conf = self._test_session.load_options_from_file(fpath)
        for k,v in conf.arjuna_config._config_dict.items():
            self._config_container.set_arjuna_option(k,v)
        for k,v in conf.user_config._config_dict.items():
            self._config_container.set_user_option(k,v)

    def register(self, config_name=None):
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

'''


class _ConfigCreator:

    def __init__(self, test_session, config_map, conf_trace, code_mode=True):
        # vars(self)[__code_mode = code_mode
        vars(self)['_test_session'] = test_session
        vars(self)['_config_container'] = ConfigContainer()

        vars(self)['_config_map'] = config_map
        if "reference" in config_map:
            vars(self)['_parent_config'] = config_map["reference"]
        else:
            vars(self)['_parent_config'] = None

    def parent_config(self, config):
        self.__parent_config = config

    def option(self, option, obj):
        self._config_container.set_option(option, obj)
        return self

    def __setattr__(self, option, obj):
        self.option(option, obj)
        return self

    def __setitem__(self, option, obj):
        self.option(option, obj)
        return self

    def options(self, option_map):
        self._config_container.set_options(option_map)
        return self

    def selenium(self):
        self.set_option(ArjunaOption.GUIAUTO_AUTOMATOR_NAME, GuiAutomatorName.SELENIUM)
        return self

    def appium(self, context):
        self.option(ArjunaOption.GUIAUTO_AUTOMATOR_NAME, GuiAutomatorName.APPIUM)
        self.option(ArjunaOption.GUIAUTO_CONTEXT, context)
        return self

    def chrome(self):
        self.option(ArjunaOption.BROWSER_NAME, BrowserName.CHROME)
        return self

    def firefox(self):
        self.option(ArjunaOption.BROWSER_NAME, BrowserName.FIREFOX)
        return self

    def app(self, path):
        self.option(ArjunaOption.MOBILE_APP_FILE_PATH, path)
        return self

    def register(self, config_name=None):
        config_name = config_name and config_name or 'c{}'.format(str(uuid.uuid4()).replace("-","_"))
        if config_name.lower() in self._config_map:
            raise Exception("You can not re-register a configuration for a name. Config with name {} already exists.".format(config_name))

        if not self._config_container.arjuna_options.items() and not self._config_container.user_options.items():
            if not self.__parent_config:
                if config_name != "reference":
                    cfg = self._config_map["reference"]
                    self._config_map[config_name.lower()] = cfg
                    return cfg
            else:
                cfg = self._parent_config
                self._config_map[config_name.lower()] = cfg
                return cfg

        config = self._test_session.register_config(config_name.lower(), 
                                        self._config_container.arjuna_options, #.items(),
                                        self._config_container.user_options, #.items(),
                                        self._parent_config
                                    )

        self._config_map[config_name.lower()] = config
        return config

class RunContext:

    def __init__(self, test_session, name, parent_config=None):
        self.__test_session = test_session
        self.__name = name
        self.__parent_config = parent_config and parent_config or None
        from arjuna import Arjuna
        self.__configs = {"reference" : Arjuna.get_config()}
        self.__conf_trace = dict()

    @property
    def config_creator(self):
        return _ConfigCreator(self.__test_session, self.__configs, self.__conf_trace) # Sent code_mode=True earlier. Check.

    def update_with_file_config_container(self, container):
        for config_name, conf in self.__configs.items():
            builder = self.ConfigBuilder(code_mode=False)
            builder.parent_config(conf)
            amap = container.arjuna_options
            umap = container.user_options
            if config_name in self.__conf_trace:
                if "arjuna_options" in self.__conf_trace[config_name]:
                    for k,v in container.arjuna_options.items():
                        if k not in self.__conf_trace[config_name]["arjuna_options"]:
                            builder.arjuna_option(k, v)
                else:
                    for k, v in container.arjuna_options.items():
                        builder.arjuna_option(k, v)
                if "user_options" in self.__conf_trace[config_name]:
                    for k,v in container.user_options.items():
                        if k not in self.__conf_trace[config_name]["user_options"]:
                            builder.user_option(k, v)
                else:
                    for k, v in container.user_options.items():
                        builder.user_option(k, v)
            else:
                for k in amap.keys():
                    builder.arjuna_option(k, amap.object(k))
                for k in umap.keys():
                        builder.user_option(k, umap.object(k))
            builder.build(config_name=config_name)

    @property
    def config(self):
        return self.get_config()

    def get_config(self, config_name="reference"):
        return self.__configs[config_name.lower()]

    def add_config(self, config):
        self.__configs[config.name.lower()] = config 

    def _add_configs(self, configs):
        self.__configs.update(configs)

    def _add_conf_trace(self, conf_trace):
        self.__conf_trace.update(conf_trace)

    def _get_conf_trace(self):
        return self.__conf_trace

    def _get_configs(self):
        return self.__configs

    def _get_test_session(self):
        return self.__test_session

    def get_name(self):
        return self.__name
'''