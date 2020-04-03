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

import json
import os
from enum import Enum

from arjuna.configure.impl.processor import ConfigCreator, CentralConfigLoader, ProjectConfigCreator, PartialConfCreator, EmptyConfCreator
from arjuna.core.reader.hocon import HoconStringReader, HoconConfigDictReader
from arjuna.core.value import Value
from arjuna.core.utils import file_utils

class TestConfigurator:

    def __init__(self, root_dir, cli_config, run_id, run_conf):
        self.__root_dir = root_dir
        self.__cli_config = cli_config
        self.__run_id = run_id
        self.__run_conf_path = run_conf
        self.__default_ref_config = None
        self.__run_conf = None
        self.__chosen_env_conf = None
        self.__env_confs = dict()
        self.__project_config_loaded = False

        self.__load()

    def __load(self):
        self.__load_central_conf()
        self.__load_project_conf()
        self.__load_cli_dicts()
        self.__update_ref_config()
        self.__load_env_configurations()
        self.__load_chosen_env()
        self.__load_run_conf()
        self.__update_ref_config()
        self.__update_env_dicts()

    def __load_central_conf(self):
        self.__default_ref_config = CentralConfigLoader(self.__root_dir, self.__run_id).config

    def __load_project_conf(self):
        project_conf_loader = ProjectConfigCreator(self.__default_ref_config)
        self.__default_ref_config = project_conf_loader.config

    def __load_env_configurations(self):
        from arjuna import ArjunaOption
        env_dir = self.__default_ref_config.arjuna_config.value(ArjunaOption.RUN_ENV_CONF_DIR)
        for fname in os.listdir(env_dir):
            if fname.lower().endswith(".conf"):
                env_conf_loader = PartialConfCreator(os.path.join(env_dir, fname))
                self.__env_confs[os.path.splitext(fname)[0].lower()] = env_conf_loader.config

    def load_options_from_file(self, fpath):
        if file_utils.is_absolute_path(fpath):
            if not file_utils.is_file(fpath):
                if file_utils.is_dir(fpath):
                    raise Exception("Not a file: {}".format(fpath))
                else:
                    raise Exception("File does not exist: {}".format(fpath))
        else:
            from arjuna import Arjuna, ArjunaOption
            conf_dir = self.__default_ref_config.arjuna_config.value(ArjunaOption.CONF_DIR)
            fpath = os.path.abspath(os.path.join(conf_dir, fpath))
            if not file_utils.is_file(fpath):
                if file_utils.is_dir(fpath):
                    raise Exception("Not a file: {}".format(fpath))
                else:
                    raise Exception("File does not exist: {}".format(fpath))
        return PartialConfCreator(fpath).config

    def __load_run_conf(self):
        if self.__run_conf_path:
            if not self.__run_conf_path.lower().endswith(".conf"):
                self.__run_conf_path += ".conf"
            self.__run_conf = self.load_options_from_file(self.__run_conf_path)

    def __create_config_from_option_dicts(self, reference, arjuna_options, user_options):
        def format_value(val):
            if isinstance(val, Enum):
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

    def __load_cli_dicts(self):

        def load(arjunaOptions={}, userOptions={}):
            self.__cli_config = self.__create_config_from_option_dicts(None, arjunaOptions, userOptions)

        cli_config = self.__cli_config and self.__cli_config or {}
        load(**cli_config)

    def __load_chosen_env(self):
        from arjuna.tpi.enums import ArjunaOption
        env_name = self.__default_ref_config.arjuna_config.value(ArjunaOption.RUN_ENV_NAME).lower()
        if env_name != "not_set":
            if env_name not in self.__env_confs:
                raise Exception("No environment configured for name: {}. Check the name and matching conf file in {}".format(
                                        env_name,
                                        self.__default_ref_config.arjuna_config.value(ArjunaOption.RUN_ENV_CONF_DIR)
                                ))
            self.__chosen_env_conf = self.__env_confs[env_name]

    def __update_config_for_env(self, config):
        if self.__chosen_env_conf:
            config.update(self.__chosen_env_conf)

    def __update_config_for_run_conf(self, config):
        if self.__run_conf:
            config.update(self.__run_conf)

    def __update_config_for_cli(self, config):
        config.update(self.__cli_config)

    def __update_config(self, config, update_from_chosen_env=False):
        if update_from_chosen_env:
            self.__update_config_for_env(config)
        self.__update_config_for_run_conf(config)
        self.__update_config_for_cli(config)
        config.process_arjuna_options()

    def __update_ref_config(self):
        self.__update_config(self.__default_ref_config, update_from_chosen_env=True)

    def __update_env_dicts(self):
        out_dict = dict()
        for name, econf in self.__env_confs.items():
            conf = EmptyConfCreator().config
            conf.update(self.__default_ref_config)
            conf.update(econf)
            self.__update_config(conf)
            out_dict[name] = conf
        self.__env_confs = out_dict

    @property
    def ref_config(self):
        return self.__default_ref_config

    @property
    def env_confs(self):
        return self.__env_confs

    def register_new_config(self, arjuna_options, user_options, parent_config=None):
        # Registering a config is post project conf registration. If no project conf, set it to true.
        self.__project_config_loaded = True
        reference = parent_config and parent_config._wrapped_config or self.__default_ref_config._wrapped_config
        conf = self.__create_config_from_option_dicts(reference, arjuna_options, user_options)
        self.__update_config(conf)
        return conf