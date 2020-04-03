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

import os
import copy
import re
import datetime
import platform
from pprint import pprint

from arjuna.core.reader.hocon import HoconFileReader, HoconStringReader, HoconConfigDictReader

from arjuna.tpi.enums import ArjunaOption
from .validator import Validator
from .config import Config, ArjunaConfig, UserConfig

class ConfigCreator:
    SETU_CONF_DESC_MAP = None

    @classmethod
    def init(cls):
        if cls.SETU_CONF_DESC_MAP is not None:
            return
        my_dir = os.path.dirname(os.path.realpath(__file__))
        setu_conf_desc_file = os.path.abspath(os.path.join(my_dir, "..", "..", "res", "arjuna_conf_desc.conf"))
        cls.__process_setu_conf_desc(setu_conf_desc_file)  

    @classmethod
    def __process_setu_conf_desc(cls, type_path):
        cls.SETU_CONF_DESC_MAP = cls.get_flat_map_from_hocon_string_for_setu_types(
            HoconFileReader(type_path)
        )    

    @classmethod
    def __setu_conf_key(cls, key):
        try:
            key = re.sub(r"\"(.*?)\"", r"\1", key)
            return ArjunaOption[key]
        except Exception:
            raise Exception("Config option <{}> is not a valid ArjunaOption constant".format(key))

    @classmethod
    def __get_flat_map_from_hocon_string(cls, hreader):
        hreader.process()
        return {i.upper().strip().replace(".", "_"): j for i, j in hreader.get_flat_map().items()}

    @classmethod      
    def get_flat_map_from_hocon_string_for_setu_types(cls, hreader):
        return {cls.__setu_conf_key(k):v for k,v in cls.__get_flat_map_from_hocon_string(hreader).items()}

    @classmethod
    def create_config_for_raw_map(self, map, validator_func):
        out_map = {}
        for conf_name, raw_value in map.items():
            validator_name, validator = validator_func(conf_name)
            try:
                is_not_set = False
                try:
                    is_not_set = raw_value.lower() == "not_set"
                except:
                    pass
                finally:
                    if is_not_set:
                        out_map[conf_name] = "not_set"
                    else:
                        out_map[conf_name] = validator(raw_value)
            except Exception as e:
                print(e)
                raise Exception("Config option value <{}>(type:{}) for <{}> option did not pass the validation check: [{}]".format(
                    raw_value, type(raw_value), conf_name, validator_name)
                )
        return out_map

    @classmethod
    def create_conf(cls, processor, arjuna_conf, user_conf):
        config = Config()
        config.arjuna_config = ArjunaConfig(arjuna_conf)
        config.user_config = UserConfig(user_conf)
        config.processor = processor
        return config

    @classmethod
    def __create_new_conf(cls, processor, source, setu_dict=None, user_dict=None):
        out_setu = source and copy.deepcopy(source.arjuna_config.as_map()) or {}
        out_user = source and copy.deepcopy(source.user_config.as_map()) or {}
        if setu_dict:
            out_setu.update(setu_dict)
        if user_dict:
            out_user.update(user_dict)
        return cls.create_conf(processor, out_setu, out_user)

    @classmethod
    def create_new_conf(cls, processor, source, cdict):
        if not cdict:
            return cls.__create_new_conf(processor, source)

        custom_setu_conf = None
        if "arjunaOptions" in cdict:
            d = HoconConfigDictReader(cdict["arjunaOptions"])
            custom_raw_setu_config_map = cls.get_flat_map_from_hocon_string_for_setu_types(d)
            custom_setu_conf = cls.create_config_for_raw_map(custom_raw_setu_config_map, processor.get_setu_option_validator)

        custom_user_conf = None
        if "userOptions" in cdict:
            d = HoconConfigDictReader(cdict["userOptions"])
            project_raw_user_config_map = cls.__get_flat_map_from_hocon_string(d)
            custom_user_conf = cls.create_config_for_raw_map(
                project_raw_user_config_map, 
                processor.get_user_option_validator
            )
        return cls.__create_new_conf(processor, source, custom_setu_conf, custom_user_conf) 

class BaseConfigProcessor:

    def __init__(self):
        self.__setu_type_map = {}
        self.__config = None

    @property
    def config(self):
        return self.__config

    @config.setter
    def _config(self, config):
        self.__config = config

    def pass_through(self, input):
        return input

    def get_setu_option_validator(self, conf_name):
        validator_name = ConfigCreator.SETU_CONF_DESC_MAP[conf_name]
        return validator_name, getattr(Validator, validator_name.lower())

    def get_user_option_validator(self, conf_name):
        return "pass_through", self.pass_through


class CentralConfigLoader(BaseConfigProcessor):
    OS_MAP = {
        'Windows': 'windows',
        'Darwin': 'mac',
        'Linux': 'linux'
    }

    def __init__(self, project_root_dir, runid=None):
        self.__my_dir = os.path.dirname(os.path.realpath(__file__))
        self.__setu_central_confg_file = os.path.abspath(os.path.join(self.__my_dir, "..","..","res", "arjuna.conf"))
        self.__project_root_dir = project_root_dir
        self.__project_name = os.path.basename(self.__project_root_dir)
        self.__runid = runid and runid or "mrun"
        self.__process()

    def __process(self):
        # Processes central conf based on root directory
        f = open(self.__setu_central_confg_file, "r")
        contents = f.read()
        f.close()
        arjuna_root = os.path.abspath(os.path.join(self.__my_dir, "..", ".."))

        irunid = self.__runid
        test_module_import_prefix = "{}.tests.modules.".format(self.__project_name)
        conf_fixtures_import_prefix = "{}.fixtures.".format(self.__project_name)

        contents = contents.replace("<ARJUNA_ROOT_DIR>", arjuna_root)
        contents = contents.replace("<PROJECT_ROOT_DIR>", self.__project_root_dir)
        contents = contents.replace("<PROJECT_NAME>", self.__project_name)
        contents = contents.replace("<RUNID>", irunid)
        contents = contents.replace("<TEST_MODULE_IMPORT_PREFIX>", test_module_import_prefix)
        contents = contents.replace("<FIXTURES_IMPORT_PREFIX>", conf_fixtures_import_prefix)
        contents = contents.replace("<HOST_OS>", CentralConfigLoader.OS_MAP[platform.system()])
        raw_config_map = ConfigCreator.get_flat_map_from_hocon_string_for_setu_types(
            HoconStringReader(contents)
        )
        self._config = ConfigCreator.create_conf(
            self,
            ConfigCreator.create_config_for_raw_map(raw_config_map, self.get_setu_option_validator), 
            {}
        )


class ProjectConfigCreator(BaseConfigProcessor):

    def __init__(self, central_conf):
        self.__central_conf = central_conf
        self.__process()

    def __process(self):
        # Process project conf
        project_conf_file = self.__central_conf.arjuna_config.value(ArjunaOption.PROJECT_CONF_FILE)
        project_hreader = HoconFileReader(project_conf_file)
        project_hreader.process()
        cdict = project_hreader.get_map()

        self._config = ConfigCreator.create_new_conf(self, self.__central_conf, cdict)

class EmptyConfCreator(BaseConfigProcessor):

    def __init__(self):
        self.__process()

    def __process(self):
        self._config = ConfigCreator.create_new_conf(self, None, dict())

class PartialConfCreator(BaseConfigProcessor):

    def __init__(self, cfpath):
        self.__cfile_path = cfpath
        self.__process()

    def __process(self):
        # process conf file
        hreader = HoconFileReader(self.__cfile_path)
        hreader.process()
        cdict = hreader.get_map()

        self._config = ConfigCreator.create_new_conf(self, None, cdict)



