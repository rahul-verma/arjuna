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
import threading
import platform
# import multiprocessing
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="UTF-8")
# sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="UTF-8")

import logging
from arjuna.core.utils import thread_utils
from arjuna.core.thread.decorators import *
from arjuna.core.utils import sys_utils
from arjuna.core.adv.proxy import ROProxy
from arjuna.tpi.helper.arjtype import CIStringDict
from arjuna.tpi.error import UndefinedConfigError
from arjuna.core.adv.decorators import singleton
from arjuna.tpi.error import TestSelectorNotFoundError
import codecs
import sys


@singleton
class ArjunaSingleton:

    def __init__(self):
        self.__project_root_dir = None
        self.__test_session = None
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
        self.__contextual_data_references = None
        self.__indexed_data_references = None
        self.__logger = None
        from arjuna.engine.data.store import DataStore
        self.__data_store = DataStore()
        self.__thread_wise_group_params_map = dict()
        self.__thread_wise_ref_conf_map = dict()
        self.__thread_wise_test_selector_map = dict()
        self.__test_meta_data = dict()

        from arjuna.tpi.engine.testwise import CurrentTestWiseContainer
        self.__current_test_wise_objects = CurrentTestWiseContainer()
        self.__allowed_log_contexts = {"default"}
        self.__bmproxy_server = None

    def __start_bmproxy(self, config):
        # BrowserMob
        from browsermobproxy import Server
        from arjuna.tpi.constant import ArjunaOption
        capture_traffic = config.value(ArjunaOption.BROWSER_NETWORK_RECORDER_ENABLED)
        if capture_traffic:
            bmproxy_dir = config.value(ArjunaOption.TOOLS_BMPROXY_DIR)
            sub_dirs = os.listdir(bmproxy_dir)
            bmproxy_bin_dir = None
            if "bin" in sub_dirs:
                bmproxy_bin_dir = os.path.join(bmproxy_dir, "bin")
            else:
                sub_dirs.sort(reverse=True) # Last version will be picked.
                for d in sub_dir:
                    if d.startswith("browsermob"):
                        bmproxy_bin_dir = os.path.join(bmproxy_dir, d, "bin")
                        break

            if bmproxy_bin_dir is None:
                raise Exception("Network recording is enabled in configuration. There was an error in creating proxy server/server using BrowserMob Proxy. Could not find proxy package at {}".format(bmproxy_dir))
            
            if platform.system().lower() == "windows":
                exe = "browsermob-proxy.bat"
            else:
                exe = "browsermob-proxy"
            bmproxy_exe_path = os.path.join(bmproxy_bin_dir, exe)

            try:
                self.__bmproxy_server = Server(bmproxy_exe_path)
                self.__bmproxy_server.start()
            except ProxyServerError as e:
                raise Exception("Network recording is enabled in configuration. There was an error in creating proxy server/server using BrowserMob Proxy. Fix and retry. Error message: {}".format(str(e)))

    @property
    def bmproxy_server(self):
        return self.__bmproxy_server

    @property
    def allowed_log_contexts(self):
        return self.__allowed_log_contexts

    @property
    def gui_mgr(self):
        return self.__test_session.gui_manager

    def __create_dir_if_doesnot_exist(self, d):
        if not os.path.exists(d):
            os.makedirs(d)

    def init(self, project_root_dir, cli_config, run_id, *, static_rid):
        from arjuna.configure.options import ArjunaOptions
        ArjunaOptions.load_desc()
        
        self.__project_root_dir = project_root_dir

        from arjuna.engine.controller import TestSessionController
        self.__test_session = TestSessionController()
        run_id = run_id and run_id or "mrun"
        prefix = ""
        if not static_rid:
            prefix = "{}-".format(datetime.datetime.now().strftime("%Y.%m.%d-%H.%M.%S.%f")[:-3])
        run_id = "{}{}".format(prefix, run_id)
        self.__thread_wise_ref_conf_map[threading.currentThread().name] = self.__test_session.init(project_root_dir, cli_config, run_id)

        from arjuna.tpi.constant import ArjunaOption
        self.__create_dir_if_doesnot_exist(self.ref_config.value(ArjunaOption.REPORT_DIR))
        self.__create_dir_if_doesnot_exist(self.ref_config.value(ArjunaOption.REPORT_XML_DIR))
        self.__create_dir_if_doesnot_exist(self.ref_config.value(ArjunaOption.REPORT_HTML_DIR))
        self.__create_dir_if_doesnot_exist(self.ref_config.value(ArjunaOption.LOG_DIR))
        self.__create_dir_if_doesnot_exist(self.ref_config.value(ArjunaOption.SCREENSHOTS_DIR))

        from arjuna.engine.logger import Logger
        self.__logger = Logger(self.ref_config)
        from arjuna import ArjunaOption
        self.__allowed_log_contexts = self.ref_config.value(ArjunaOption.LOG_ALLOWED_CONTEXTS)

        from arjuna.tpi.hook.config import Configurator
        configurator = Configurator()
        # Load configs from config hooks
        hooks_dir = self.ref_config.value(ArjunaOption.HOOKS_DIR)
        if os.path.isdir(hooks_dir):
            sys.path.append(hooks_dir)
        try:
            from arjuna_config import register_configs
        except ModuleNotFoundError as e: # Module not defined.
            pass
        except ImportError as f: # Hook not defined
            pass
        else:
            register_configs(configurator)

        # Load data references
        from arjuna.engine.data.factory import DataReference
        self.__contextual_data_references, self.__indexed_data_references  = DataReference.load_all(self.ref_config)

        # Load localization data
        from arjuna.engine.data.localizer import Localizer
        self.__localizer = Localizer.load_all(self.ref_config)

        from arjuna.tpi.parser.yaml import Yaml
        from arjuna.interact.gui.auto.finder.withx import WithX
        fpath = self.ref_config.value(ArjunaOption.CONF_WITHX_FILE)
        creation_context= f"WithX.yaml file at {fpath}"
        if os.path.isfile(fpath):        
            wyaml = Yaml.from_file(fpath, allow_any=True)
            if wyaml is not None:
                self.__common_withx_ref = WithX(wyaml.as_map())

        self.__start_bmproxy(self.ref_config)

        return self.ref_config

    @property
    def test_wise_container(self):
        return self.__current_test_wise_objects

    @property
    def withx_ref(self):
        return self.__common_withx_ref

    @property
    def contextual_data_references(self):
        return self.__contextual_data_references

    @property
    def indexed_data_references(self):
        return self.__indexed_data_references

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

    def get_config_value(self, query, *, cname=None):
        if cname is None:
            if type(query) is str:
                if query.find('.') != -1:
                    conf, _query = query.split(".", 1)
                    if self.has_config(conf):
                        cname = conf
                        query = _query
                    else:
                        cname = "ref"
                else:
                    cname = "ref"
            else:
                cname = "ref"

        return self.get_config(cname).value(query)

    @property
    def ref_config(self):
        return self.__thread_wise_ref_conf_map[threading.currentThread().name]


    def __get_thread_name(self):
        #multiprocessing.current_process().name
        return threading.current_thread().name

    def get_config(self, name):
        if name == "ref":
            current_proc_name = self.__get_thread_name()
            if current_proc_name == "MainThread":
                return self.ref_config
            else:
                return self.get_group_params()["config"]
        else:
            if not self.has_config(name):
                raise UndefinedConfigError(name, tuple(self.__config_map.keys()))
            return self.__config_map[name.lower()]

    def register_config(self, config):
        self.__config_map[config.name.lower()] = config

    def has_config(self, name):
        return name.lower() in self.__config_map

    def get_group_params(self):
        return self.__thread_wise_group_params_map[self.__get_thread_name()]

    def register_group_params(self, **params):
        self.__thread_wise_group_params_map[self.__get_thread_name()] = params
        self.__thread_wise_ref_conf_map[self.__get_thread_name()] = params['config']

    def register_test_selector_for_group(self, selector):
        self.__thread_wise_test_selector_map[self.__get_thread_name()] = selector

    def get_test_selector(self):
        try:
            return self.__thread_wise_test_selector_map[self.__get_thread_name()]
        except KeyError:
            raise TestSelectorNotFoundError()

    def register_test_meta_data(self, qual_name, test_meta_data):
        if qual_name not in self.__test_meta_data:
            self.__test_meta_data[qual_name] = test_meta_data

    def get_test_meta_data(self, qual_name):
        try:
            return self.__test_meta_data[qual_name]
        except KeyError as e:
            try:
                from arjuna import ArjunaOption
                return self.__test_meta_data[self.get_config("ref").value(ArjunaOption.PROJECT_NAME) + "." + qual_name]
            except KeyError:
                raise Exception("Test Meta data not found for test: {}. If you have a function with prefix 'check_', verify if it is decorated with @test. Existing entries: {}".format(qual_name, self.__test_meta_data.keys()))

class Arjuna:
    '''
        Facade of Arjuna framework.
        Contains static methods which wrapper an internal singleton class for easy access to top level Arjuna functions.
    '''

    ARJUNA_SINGLETON = None
    LOGGER = None

    @classmethod
    def init(cls, project_root_dir, cli_config=None, run_id=None, *, static_rid=False):
        '''
            Returns reference test context which contains reference configuration.
            This reference test context merges central conf, project conf and central CLI options.
            Root directory is assumed as per the project structure.
            You can also provide an alternative root directory for test project.
        '''
        cls.ARJUNA_SINGLETON = ArjunaSingleton()
        return cls.ARJUNA_SINGLETON.init(project_root_dir, cli_config, run_id, static_rid=static_rid)

    @classmethod
    def get_logger(cls):
        '''
            Returns framework logger.
        '''
        return cls.ARJUNA_SINGLETON.logger

    @classmethod
    def _get_allowed_log_contexts(cls):
        return cls.ARJUNA_SINGLETON.allowed_log_contexts

    @classmethod
    def _get_bmproxy_server(cls):
        return cls.ARJUNA_SINGLETON.bmproxy_server

    @classmethod
    def get_test_session(cls):
        '''
            Returns the current Test Session object.
        '''
        return cls.ARJUNA_SINGLETON.test_session

    @classmethod
    def register_config(cls, config):
        cls.ARJUNA_SINGLETON.register_config(config)

    @classmethod
    def has_config(cls, name):
        return cls.ARJUNA_SINGLETON.has_config(name)

    @classmethod
    def get_config(cls, name="ref"):
        '''
            Returns the configuration.
        '''
        return cls.ARJUNA_SINGLETON.get_config(name)

    @classmethod
    def get_configs(cls, *names):
        '''
            Returns the reference configuration.
        '''
        return [cls.get_config(name) for name in names]

    @classmethod
    def get_config_value(cls, query, *, cname=None):
        '''
            Returns the configuration value.
        '''
        return cls.ARJUNA_SINGLETON.get_config_value(query, cname=cname)

    @classmethod
    def get_data_ref(cls, name):
        try:
            return cls.ARJUNA_SINGLETON.contextual_data_references[name]
        except:
            try:
                return cls.ARJUNA_SINGLETON.indexed_data_references[name]
            except:
                raise Exception(f"No data reference found with name: {name}")

    @classmethod
    def get_dataref_value(cls, query="", *, bucket=None, context=None, index=None):
        '''
            Returns the data reference value for a given context.
        '''
        from arjuna.engine.data.reference import R
        return R(query, bucket=bucket, context=context, index=index)

    @classmethod
    def get_report_metadata(cls):
        return cls.ARJUNA_SINGLETON.test_wise_container

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
    def get_localized_str(cls, in_str, *, locale=None, bucket=None, strict=None):
        from arjuna.engine.data.localizer import L
        return L(in_str, locale=locale, bucket=bucket, strict=strict)

    @classmethod
    def get_data_store(cls):
        return cls.ARJUNA_SINGLETON.data_store

    @classmethod
    def get_withx_ref(cls):
        return cls.ARJUNA_SINGLETON.withx_ref

    @classmethod
    def get_group_params(cls):
        return cls.ARJUNA_SINGLETON.get_group_params()

    @classmethod
    def register_group_params(cls, **params):
        return cls.ARJUNA_SINGLETON.register_group_params(**params)

    @classmethod
    def register_test_selector_for_group(cls, selector):
        cls.ARJUNA_SINGLETON.register_test_selector_for_group(selector)

    @classmethod
    def get_test_selector(cls):
        return cls.ARJUNA_SINGLETON.get_test_selector()

    @classmethod
    def register_test_meta_data(cls, qual_name, test_meta_data):
        cls.ARJUNA_SINGLETON.register_test_meta_data(qual_name, test_meta_data)

    @classmethod
    def get_test_meta_data(cls, qual_name):
        return cls.ARJUNA_SINGLETON.get_test_meta_data(qual_name)

    @classmethod
    def exit(cls):
        '''
            Clean-up and finalise resources currently opened by Arjuna.
        '''
        proxy_server = cls._get_bmproxy_server()
        if proxy_server is not None:
            proxy_server.stop()