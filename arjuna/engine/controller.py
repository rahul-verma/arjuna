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

import os
import uuid
import time
import logging
import shutil
from arjuna import ArjunaOption


from arjuna.tpi.config import Configuration

from arjuna.configure.configurator import TestConfigurator
from arjuna.drive.invoker.databroker import TestSessionDataBrokerHandler
from arjuna.interact.gui.gom.guimgr import GuiManager

class TestSessionController:
    
    def __init__(self):
        self.__id = uuid.uuid4()
        self.__DEF_CONF_NAME = "ref"
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

    def init(self, root_dir, cli_config=None, run_id=None, linked_projects=[]):
        self.__configurator = TestConfigurator(root_dir, cli_config, run_id, linked_projects)
        ref_config = self.__configurator.ref_config
        data_env_confs = self.__configurator.file_confs
        self.__guimgr = GuiManager(ref_config)
        ref_conf = self._create_config(ref_config)
        self.__add_to_map(ref_conf)
        for run_env_conf in [self._create_config(econf, name=name) for name, econf in data_env_confs.items()]:
            self.__add_to_map(run_env_conf)

        return ref_conf

    def __msession_config(self, ref_conf_name):
        from arjuna import Arjuna
        if ref_conf_name is None:
            ref_conf_name = "ref"
        return Arjuna.get_config(ref_conf_name)

    def _create_config(self, config, name=None):
        config = Configuration(
            self,
            name and name or self.__DEF_CONF_NAME,
            config
        )
        return config

    def finish(self):
        pass

    def __add_to_map(self, config):
        from arjuna import Arjuna
        Arjuna.register_config(config)

    def load_options_from_file(self, fpath, *, conf_stage):
        return self.configurator.load_options_from_file(fpath, conf_stage=conf_stage)

    def register_config(self, name, arjuna_options, user_options, *, conf_stage, parent_config=None):
        config = self.configurator.register_new_config(arjuna_options, user_options, parent_config=parent_config, conf_stage=conf_stage)
        conf = self._create_config(config, name=name)
        self.__add_to_map(conf)
        return conf

    def create_file_data_source(self, record_type, file_name, *arg_pairs):
        raise NotImplementedError()
        # response = self._send_request(
        #     ArjunaComponent.DATA_SOURCE,
        #     DataSourceActionType.CREATE_FILE_DATA_SOURCE,
        #     *arg_pairs
        # )
        # return response.get_data_source_id()

    def define_gui(self, automator, label=None, name=None, qual_name=None, def_file_path=None):
        return self.gui_manager.define_gui(automator, label=label, name=name, qual_name=qual_name, def_file_path=def_file_path)
