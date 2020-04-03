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

import copy
import os
import codecs
import sys
import io
import time
import datetime
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="UTF-8")
# sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="UTF-8")

import logging
from arjuna.core.utils import thread_utils
from arjuna.core.thread.decorators import *
from arjuna.core.utils import sys_utils
from arjuna.core.adv.proxy import ROProxy
from arjuna.tpi.helpers.types import CIStringDict
from arjuna.core.adv.decorators import singleton
import codecs
import sys


@singleton
class ArjunaSingleton:

    def __init__(self):
        self.__project_root_dir = None
        self.__test_session = None
        self.__ref_config = None
        self.__config_map = dict()
        self.__run_id = None

        # From central config
        self.prop_enum_to_prop_path_map = {}
        # It is base config object
        self.arjuna_options = {}

        # Check relevance of above and following
        self.prog = "Arjuna"

        self.dl = None
        self.log_file_discovery_info = False
        self.__data_references = None
        self.__logger = None
        from arjuna.engine.data.store import DataStore
        self.__data_store = DataStore()

    @property
    def gui_mgr(self):
        return self.__test_session.gui_manager

    def __create_dir_if_doesnot_exist(self, d):
        if not os.path.exists(d):
            os.makedirs(d)

    def init(self, project_root_dir, cli_config, run_id, *, static_rid, run_conf):
        from arjuna.configure.impl.processor import ConfigCreator
        ConfigCreator.init()
        self.__project_root_dir = project_root_dir

        from arjuna.session.invoker.test_session import DefaultTestSession
        self.__test_session = DefaultTestSession()
        run_id = run_id and run_id or "mrun"
        prefix = ""
        if not static_rid:
            prefix = "{}-".format(datetime.datetime.now().strftime("%Y.%m.%d-%H.%M.%S.%f")[:-3])
        run_id = "{}{}".format(prefix, run_id)
        self.__ref_config = self.__test_session.init(project_root_dir, cli_config, run_id, run_conf)

        from arjuna.tpi.enums import ArjunaOption
        self.__create_dir_if_doesnot_exist(self.__ref_config.value(ArjunaOption.REPORT_DIR))
        self.__create_dir_if_doesnot_exist(self.__ref_config.value(ArjunaOption.REPORT_XML_DIR))
        self.__create_dir_if_doesnot_exist(self.__ref_config.value(ArjunaOption.REPORT_HTML_DIR))
        self.__create_dir_if_doesnot_exist(self.__ref_config.value(ArjunaOption.LOG_DIR))
        self.__create_dir_if_doesnot_exist(self.__ref_config.value(ArjunaOption.SCREENSHOTS_DIR))

        from .logger import Logger
        self.__logger = Logger(self.__ref_config)

        # Load data references
        from arjuna.engine.data.factory import DataReference
        self.__data_references = DataReference.load_all(self.__ref_config)

        # Load localization data
        from arjuna.engine.data.localizer import Localizer
        self.__localizer = Localizer.load_all(self.__ref_config)

        from arjuna.core.yaml import YamlFile
        from arjuna.interact.gui.auto.finder.withx import WithX
        fpath = self.ref_config.value(ArjunaOption.GUIAUTO_WITHX_YAML)
        self.__common_withx_ref = WithX(YamlFile(fpath).as_map())

        return self.ref_config

    @property
    def withx_ref(self):
        return self.__common_withx_ref

    @property
    def data_references(self):
        return self.__data_references

    @property
    def localizer(self):
        return self.__localizer

    @property
    def logger(self):
        return self.__logger.arjuna_logger

    @property
    def data_store(self):
        return self.__data_store

    @property
    def test_session(self):
        return self.__test_session

    def get_config_value(self, name, config=None):
        config = config
        query = name
        if config is None:
            if type(name) is str:
                if name.find('.') != -1:
                    conf, query = name.split(".", 1)
                    if self.has_config(conf):
                        config = self.get_config(conf)
                    else:
                        config = self.ref_config
                        query = name
                else:
                    config = self.ref_config
                    query = name
            else:
                config = self.ref_config
                query = name
        else:
            if type(config) is str:
                config = self.get_config(config)

        return config.value(query)

    @property
    def ref_config(self):
        return self.__ref_config

    def get_config(self, name):
        if not self.has_config(name):
            raise Exception("There is no registered configuration for name: {}".format(name))
        return self.__config_map[name.lower()]

    def register_config(self, config):
        self.__config_map[config.name.lower()] = config

    def has_config(self, name):
        return name.lower() in self.__config_map

class Arjuna:
    '''
        Facade of Arjuna framework.
        Contains static methods which wrapper an internal singleton class for easy access to top level Arjuna functions.
    '''

    ARJUNA_SINGLETON = None
    LOGGER = None

    @classmethod
    def init(cls, project_root_dir, cli_config=None, run_id=None, *, static_rid=False, run_conf=None):
        '''
            Returns reference test context which contains reference configuration.
            This reference test context merges central conf, project conf and central CLI options.
            Root directory is assumed as per the project structure.
            You can also provide an alternative root directory for test project.
        '''
        cls.ARJUNA_SINGLETON = ArjunaSingleton()
        return cls.ARJUNA_SINGLETON.init(project_root_dir, cli_config, run_id, static_rid=static_rid, run_conf=run_conf)

    @classmethod
    def get_logger(cls):
        '''
            Returns framework logger.
        '''
        return cls.ARJUNA_SINGLETON.logger

    @classmethod
    def register_config(cls, config):
        cls.ARJUNA_SINGLETON.register_config(config)

    @classmethod
    def has_config(cls, name):
        return cls.ARJUNA_SINGLETON.has_config(name)

    @classmethod
    def get_config(cls, name=None):
        '''
            Returns the reference configuration.
        '''
        if name is None:
            return cls.ARJUNA_SINGLETON.ref_config
        else:
            return cls.ARJUNA_SINGLETON.get_config(name)

    @classmethod
    def get_config_value(cls, name, config=None):
        '''
            Returns the reference configuration.
        '''
        return cls.ARJUNA_SINGLETON.get_config_value(name, config)

    @classmethod
    def get_dataref_value(cls, name, *, bucket=None, context=None):
        '''
            Returns the data reference value for a given context.
        '''
        from arjuna.engine.data.reference import R
        return R(name, bucket=bucket, context=context)


    @classmethod
    def get_gui_mgr(cls):
        '''
            Returns the central GUI Manager object that mangages namespaces.
        '''
        return cls.ARJUNA_SINGLETON.gui_mgr

    @classmethod
    def get_localizer(cls):
        return cls.ARJUNA_SINGLETON.localizer

    @classmethod
    def get_data_ref(cls, name):
        return cls.ARJUNA_SINGLETON.data_references[name]

    @classmethod
    def get_localized_str(cls, in_str, *, locale=None, bucket=None, strict=None):
        from arjuna.engine.data.localizer import L
        return L(in_str, locale=locale, bucket=bucket, strict=strict)

    @classmethod
    def get_data_store(cls):
        return cls.ARJUNA_SINGLETON.data_store

    @classmethod
    def get_withx_ref(cls):
        return cls.ARJUNA_SINGLETON.withx_ref

    @staticmethod
    def exit():
        '''
            Clean-up and finalise resources currently opened by Arjuna.
        '''
        pass