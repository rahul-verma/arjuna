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

import json
from enum import Enum

from arjuna.configure.impl.processor import ConfigCreator, CentralConfigLoader, ProjectConfigCreator
from arjuna.core.reader.hocon import HoconStringReader, HoconConfigDictReader
from arjuna.core.value import AnyRefValue

class TestConfigurator:

    def __init__(self, run_id):
        self.__run_id = run_id
        self.__default_ref_config = None
        self.__config_map = {}
        self.__cli_central_config = None
        self.__cli_test_config = None
        self.__project_config_loaded = False

    def __create_config_from_option_dicts(self, reference, arjuna_options, user_options):
        def format_value(val):
            if isinstance(val, AnyRefValue):
                return val.as_str()
            elif isinstance(val, Enum):
                return val.name
            else:
                return str(val)

        # ANCHOR
        crawdict = {
            "arjunaOptions": {k:format_value(v) for k,v in arjuna_options.items()},
            "userOptions": {k:format_value(v) for k,v in user_options.items()}
        }
        hreader = HoconStringReader(json.dumps(crawdict))
        hreader.process()

        config = ConfigCreator.create_new_conf(
            self.__default_ref_config.processor,
            reference,
            hreader.get_map()
        )
        return config

    def __init_cli_dicts(self, arjunaCentralOptions={}, arjunaTestOptions={}, userCentralOptions={}, userTestOptions={}):
        self.__cli_central_config = self.__create_config_from_option_dicts(None, arjunaCentralOptions, userCentralOptions)
        self.__cli_test_config = self.__create_config_from_option_dicts(None, arjunaTestOptions,
                                                                        userTestOptions)

    def init(self, root_dir, cli_config):
        self.__default_ref_config = CentralConfigLoader(root_dir, self.__run_id).config
        # self.__config_map[self.__default_ref_config.id] = self.__default_ref_config
        cli_config = cli_config and cli_config or {}
        self.__init_cli_dicts(**cli_config)
        return self.__default_ref_config

    def create_project_conf(self):
        project_conf_loader = ProjectConfigCreator(self.__default_ref_config)
        self.__default_ref_config = project_conf_loader.config
        self.__default_ref_config.process_arjuna_options()
        self.__default_ref_config.update(self.__cli_central_config)
        self.__default_ref_config.update(self.__cli_test_config)
        # self.__config_map[self.__default_ref_config.id] = self.__default_ref_config
        return self.__default_ref_config

    @property
    def ref_config(self):
        return self.__default_ref_config

    def get_config(self, id):
        return self.__config_map[id]

    # def get_arjuna_option_value(self, config_setu_id, option):
    #     sname = ArjunaOption[option.upper().strip().replace(".", "_")]
    #     rvalue = self.__config_map[config_setu_id].get_arjuna_option_value(sname)
    #     return rvalue

    # def get_user_option_value(self, config_setu_id, option):
    #     sname = option.upper().strip().replace(".", "_")
    #     rvalue = self.__config_map[config_setu_id].user_config.value(sname)
    #     return rvalue

    # def get_central_arjuna_option_value(self, option):
    #     sname = ArjunaOption[option.upper().strip().replace(".", "_")]
    #     rvalue = self.__default_ref_config.get_arjuna_option_value(sname)
    #     return rvalue

    # def get_central_user_option_value(self, option):
    #     sname = option.upper().strip().replace(".", "_")
    #     rvalue = self.__default_ref_config.user_config.value(sname)
    #     return rvalue

    def register_new_config(self, arjuna_options, user_options, parent_config=None):
        # Registering a config is post project conf registration. If no project conf, set it to true.
        self.__project_config_loaded = True
        reference = parent_config and parent_config._wrapped_config or self.__default_ref_config._wrapped_config
        config = self.__create_config_from_option_dicts(reference, arjuna_options, user_options)
        config.update(self.__cli_test_config)
        config.process_arjuna_options()
        return config