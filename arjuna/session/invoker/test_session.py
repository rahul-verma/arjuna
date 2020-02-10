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

import uuid
import time
import logging
from arjuna import ArjunaOption


from arjuna.configure.invoker.config import DefaultTestConfig

from arjuna.configure.invoker.configurator import TestConfigurator
from arjuna.drive.invoker.databroker import TestSessionDataBrokerHandler
from arjuna.interact.gui.gom.guimgr import GuiManager

class DefaultTestSession:
    
    def __init__(self):
        self.__id = uuid.uuid4()
        self.__DEF_CONF_NAME = "central"
        self.__default_ref_config = None
        self.__config_map = {}
        self.__cli_central_config = None
        self.__cli_test_config = None
        self.__configurator = None
        self.__project_config_loaded = False
        self.__guimgr = None

    @property
    def id(self):
        return self.__id

    @property
    def configurator(self):
        return self.__configurator

    @property
    def data_broker(self):
        return self.__data_broker   

    @property
    def gui_manager(self):
        return self.__guimgr

    def init(self, root_dir, cli_config=None, run_id=None):
        self.__configurator = TestConfigurator(run_id)
        self.__configurator.init(root_dir, cli_config)
        config = self.__configurator.create_project_conf()
        self.__guimgr = GuiManager(config)
        return self.__create_config(config)

    def __create_config(self, config, name=None):
        config = DefaultTestConfig(
            self,
            name and name or self.__DEF_CONF_NAME,
            config
        )
        return config

    def finish(self):
        pass

    def register_config(self, name, arjuna_options, user_options, parent_config=None):
        config = self.configurator.register_new_config(arjuna_options, user_options, parent_config)
        return self.__create_config(config)

    def create_file_data_source(self, record_type, file_name, *arg_pairs):
        response = self._send_request(
            ArjunaComponent.DATA_SOURCE,
            DataSourceActionType.CREATE_FILE_DATA_SOURCE,
            *arg_pairs
        )
        return response.get_data_source_id()

    def define_gui(self, automator, label=None, name=None, qual_name=None, def_file_path=None):
        return self.gui_manager.define_gui(automator, label=label, name=name, qual_name=qual_name, def_file_path=def_file_path)