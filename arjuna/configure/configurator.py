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

import json
import os
from enum import Enum

from arjuna.configure.options import EditableConfig
from arjuna.core.value import Value
from arjuna.core.utils import file_utils
from arjuna.core.constant import ConfigStage


class TestConfigurator:
    _EMPTY_CONF = EditableConfig.empty_conf()

    def __init__(self, root_dir, cli_config, run_id, linked_projects=[]):
        self.__root_dir = root_dir
        self.__cli_config = cli_config
        self.__run_id = run_id
        self.__default_ref_config = None
        self.__data_confs = None
        self.__env_confs = None
        self.__dataconf_enconf_confs = dict()
        self.__project_config_loaded = False
        self.__linked_projects = linked_projects

        self.__load()

    def __load(self):
        self.__load_central_conf()
        self.__load_project_conf()
        self.__load_cli_dicts()
        self.__load_data_confs()
        self.__load_env_confs()

        self.__default_ref_config.update(self.__data_confs["data"])
        self.__default_ref_config.update(self.__env_confs["env"])
        self.__update_config(self.__default_ref_config)
        # self.__process_data_configs()

        self.__load_combinations()

    def __load_central_conf(self):
        self.__default_ref_config = EditableConfig.arjuna_conf(project_root_dir=self.__root_dir, run_id=self.__run_id)

    def __load_project_conf(self):
        self.__default_ref_config = EditableConfig.project_conf(arjuna_conf=self.__default_ref_config, linked_projects=self.__linked_projects)

    def __load_data_confs(self):
        self.__data_confs = EditableConfig.data_confs(arjuna_conf=self.__default_ref_config) 
        if "data" not in self.__data_confs:
            self.__data_confs["data"] = self._EMPTY_CONF

    def __load_env_confs(self):
        self.__env_confs = EditableConfig.env_confs(arjuna_conf=self.__default_ref_config)
        if "env" not in self.__env_confs:
            self.__env_confs["env"] = self._EMPTY_CONF

    def load_options_from_file(self, fpath, *, conf_stage):
        if file_utils.is_absolute_path(fpath):
            if not file_utils.is_file(fpath):
                if file_utils.is_dir(fpath):
                    raise Exception("Not a file: {}".format(fpath))
                else:
                    raise Exception("File does not exist: {}".format(fpath))
        else:
            from arjuna import Arjuna, ArjunaOption
            conf_dir = self.__default_ref_config.arjuna_options.value(ArjunaOption.CONF_DIR)
            fpath = os.path.abspath(os.path.join(conf_dir, fpath))
            if not file_utils.is_file(fpath):
                if file_utils.is_dir(fpath):
                    raise Exception("Not a file: {}".format(fpath))
                else:
                    raise Exception("File does not exist: {}".format(fpath))
        return EditableConfig.from_file(file_path=fpath, creation_context=f"Ad-hoc configuration file at {fpath}", conf_stage=conf_stage)

    def __load_cli_dicts(self):
        self.__cli_config = EditableConfig.from_maps(ref_config=None, arjuna_options=self.__cli_config.arjuna_options, user_options=self.__cli_config.user_options, conf_stage=ConfigStage.CLI)

    def __update_config_for_env(self, config):
        if self.__chosen_env_conf:
            config.update(self.__chosen_env_conf)

    def __update_config_for_data_conf(self, config):
        if self.__data_conf:
            config.update(self.__data_conf)

    def __update_config_for_cli(self, config):
        config.update(self.__cli_config)

    def __update_config(self, config):
        self.__update_config_for_cli(config)
        config.process_arjuna_options()

    def __update_ref_config(self):
        self.__update_config(self.__default_ref_config, update_from_chosen_env=True)

    def __load_one_combo(self, dconf, econf):
        conf = EditableConfig.empty_conf()
        conf.update(self.__default_ref_config)
        conf.update(dconf)
        conf.update(econf)
        self.__update_config(conf)
        return conf

    def __load_combinations(self):
        def __add(name, conf):
            if name not in self.__dataconf_enconf_confs:
                self.__dataconf_enconf_confs[name] = EditableConfig.empty_conf()
            self.__dataconf_enconf_confs[name].update(conf)

        # Load combinations from linked projects
        for linked_project in self.__linked_projects:
            confs = linked_project.data_env_conf_map
            for name, conf in confs.items():
                __add(name, conf)

        for dname, dconf in self.__data_confs.items():
            conf = self.__load_one_combo(dconf, self._EMPTY_CONF)
            __add(dname, conf)
            
        for ename, econf in self.__env_confs.items():
            conf = self.__load_one_combo(self._EMPTY_CONF, econf)
            __add(ename, conf)

        for dname, dconf in self.__data_confs.items():
            for ename, econf in self.__env_confs.items():
                cname = "{}_{}".format(dname, ename)
                conf = self.__load_one_combo(dconf, econf)
                __add(cname, conf)

    @property
    def ref_config(self):
        return self.__default_ref_config

    @property
    def file_confs(self):
        return self.__dataconf_enconf_confs

    def register_new_config(self, arjuna_options, user_options, *, conf_stage, parent_config=None):
        # Registering a config is post project conf registration. If no project conf, set it to true.
        self.__project_config_loaded = True
        reference = parent_config and parent_config._wrapped_config or self.__default_ref_config._wrapped_config
        conf = EditableConfig.from_maps(ref_config=reference, conf_stage=conf_stage, arjuna_options=arjuna_options, user_options=user_options)
        self.__update_config(conf)
        return conf