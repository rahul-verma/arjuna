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

class _ConfigCreator:

    def __init__(self, test_session, config_map, conf_trace, code_mode=True):
        self.__code_mode = code_mode
        self.__test_session = test_session
        self.__config_container = ConfigContainer()

        self.__config_map = config_map
        if "default_config" in config_map:
            self.__parent_config = config_map["default_config"]
        else:
            self.__parent_config = None

        # For Unitee
        self.__conf_trace = conf_trace

    def parent_config(self, config):
        self.__parent_config = config

    def arjuna_option(self, option, obj):
        if isinstance(obj, Enum):
            obj = obj.name
        self.__config_container.set_arjuna_option(option, obj)
        return self

    def user_option(self, option, obj):
        self.__config_container.set_user_option(option, obj)
        return self

    def options(self, option_map):
        self.__config_container.set_options(option_map)
        return self

    def selenium(self):
        self.__config_container.set_arjuna_option(ArjunaOption.GUIAUTO_AUTOMATOR_NAME, GuiAutomatorName.SELENIUM.name)
        return self

    def appium(self, context):
        self.arjuna_option(ArjunaOption.GUIAUTO_AUTOMATOR_NAME, GuiAutomatorName.APPIUM.name)
        self.arjuna_option(ArjunaOption.GUIAUTO_CONTEXT, context)
        return self

    def chrome(self):
        self.arjuna_option(ArjunaOption.BROWSER_NAME, BrowserName.CHROME.name)
        return self

    def firefox(self):
        self.arjuna_option(ArjunaOption.BROWSER_NAME, BrowserName.FIREFOX.name)
        return self

    def headless_mode(self):
        self.arjuna_option(ArjunaOption.BROWSER_HEADLESS_MODE, True)
        return self

    def guiauto_max_wait_time(self, seconds):
        self.arjuna_option(ArjunaOption.GUIAUTO_MAX_WAIT, seconds)
        return self

    def app(self, path):
        self.arjuna_option(ArjunaOption.MOBILE_APP_FILE_PATH, path)
        return self

    def mobile_device_name(self, name):
        self.arjuna_option(ArjunaOption.MOBILE_DEVICE_NAME, name)
        return self

    def mobile_device_udid(self, udid):
        self.arjuna_option(ArjunaOption.MOBILE_DEVICE_UDID, udid)
        return self

    def register(self, config_name="default_config"):
        if not self.__config_container.arjuna_options.str_items() and not self.__config_container.user_options.items():
            if not self.__parent_config:
                if config_name != "default_config":
                    self.__config_map[config_name] = self.__config_map["default_config"]
            else:
                self.__config_map[config_name] = self.__parent_config
            return

        config = self.__test_session.register_config(config_name, 
                                        self.__config_container.arjuna_options.str_items(),
                                        self.__config_container.user_options.items(),
                                        self.__parent_config
                                    )

        self.__config_map[config_name] = config
        if self.__code_mode:
            if config_name not in self.__conf_trace:
                self.__conf_trace[config_name] = {"arjuna_options": set(), "user_options" : set()}
            self.__conf_trace[config_name]["arjuna_options"].update(self.__config_container.arjuna_options.items().keys())
            self.__conf_trace[config_name]["user_options"].update(self.__config_container.user_options.items().keys())


class DefaultTestContext:

    def __init__(self, test_session, name, parent_config=None):
        self.__test_session = test_session
        self.__name = name
        self.__parent_config = parent_config and parent_config or None
        from arjuna import Arjuna
        self.__configs = {"default_config" : Arjuna.get_ref_config()}
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

    def get_config(self, config_name="default_config"):
        return self.__configs[config_name]

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

# class DefaultTestContext:

#     def __init__(self, test_session, name, parent_context=None):
#         self.__test_session = test_session
#         self.__name = name

#         # dict of name and TestConfig
#         if parent_context is not None:
#             self.__config_map = parent_context.clone_config_map()
#         else:
#             self.__config_map = dict()
#             self.__config_builder = self.ConfigBuilder()
#             builder.ref_config(Arjuna.get_ref_config());
#             builder.build(ConfigBuilder.DEFAULT_CONF_NAME)

#     def ConfigBuilder(self):
#         return ConfigBuilder(self.__test_session, self.__config_map)

#     @property
#     def config(self):
#         return self.__config_map[ConfigBuilder.DEFAULT_CONF_NAME]

#     def get_named_config(self, name):
#         if name is None:
#             raise Exception("Config name was passed as None.")
#         else:
#             try:
#                 return self.get_named_config[name.lower()]
#             except:
#                 raise Exception("No context config found with name: " + name)

#     @property
#     def name(self):
#         return self.__name

#     def _update_options(self, option_map):
#         for conf_name, config in option_map.items():
#             builder = self.ConfigBuilder()
#             builder.ref_config(self.__config_map.get(conf_name))
#             builder.options(option_map)
#             builder.build(conf_name)

#     def clone_config_map(self):
#         out_map = dict()
#         out_map.update(self.__config_map)
