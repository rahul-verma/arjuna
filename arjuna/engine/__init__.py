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
from arjuna.core.adv.decorators import singleton
import codecs
import sys


@singleton
class ArjunaSingleton:

    def __init__(self):
        self.__project_root_dir = None
        self.__test_session = None
        self.__ref_config = None
        self.__context_map = dict()
        self.__default_context_name = "default_context"
        self.__run_id = None

        # From central config
        self.prop_enum_to_prop_path_map = {}
        # It is base config object
        self.arjuna_options = {}

        # Check relevance of above and following
        self.prog = "Arjuna"

        self.dl = None
        self.log_file_discovery_info = False
        self._data_references = {}
        self.central_conf = None
        self.__console = None
        self.__logger = None
        from arjuna.engine.data.store import DataStore
        self.__data_store = DataStore()

    @property
    def gui_mgr(self):
        return self.__test_session.gui_manager

    def __create_dir_if_doesnot_exist(self, d):
        if not os.path.exists(d):
            os.makedirs(d)

    def init(self, project_root_dir, cli_config, run_id):
        from arjuna.configure.impl.processor import ConfigCreator
        ConfigCreator.init()
        self.__project_root_dir = project_root_dir

        from arjuna.session.invoker.test_session import DefaultTestSession
        self.__test_session = DefaultTestSession()
        run_id = run_id and run_id or "mrun"
        run_id = "{}-{}".format(datetime.datetime.now().strftime("%Y.%m.%d-%H.%M.%S.%f")[:-3], run_id)
        self.__ref_config = self.__test_session.init(project_root_dir, cli_config, run_id)

        from arjuna.core.enums import ArjunaOption
        self.__create_dir_if_doesnot_exist(self.__ref_config.get_arjuna_option_value(ArjunaOption.PROJECT_RUN_REPORT_DIR).as_str())
        self.__create_dir_if_doesnot_exist(self.__ref_config.get_arjuna_option_value(ArjunaOption.PROJECT_RUN_REPORT_XML_DIR).as_str())
        self.__create_dir_if_doesnot_exist(self.__ref_config.get_arjuna_option_value(ArjunaOption.PROJECT_RUN_REPORT_HTML_DIR).as_str())
        self.__create_dir_if_doesnot_exist(self.__ref_config.get_arjuna_option_value(ArjunaOption.PROJECT_RUN_LOG_DIR).as_str())
        self.__create_dir_if_doesnot_exist(self.__ref_config.get_arjuna_option_value(ArjunaOption.PROJECT_RUN_SCREENSHOTS_DIR).as_str())

        dl = logging.getLevelName(self.__ref_config.get_arjuna_option_value(ArjunaOption.LOG_CONSOLE_LEVEL).as_str().upper())

        self.__init_logger(dl)
        self.__load_console(dl, self.logger)

        return self.create_test_context(self.__default_context_name)

    @property
    def logger(self):
        return self.__logger

    @property
    def console(self):
        return self.__console

    @property
    def data_store(self):
        return self.__data_store

    @classmethod
    def get_test_session(cls):
        return cls.__SESSION

    @classmethod
    def has_configuration(cls, config_name):
        return config_name.upper() in cls.thread_map

    @classmethod
    def has_property(cls, config_name, path):
        return cls.has_configuration(config_name) and path.upper() in cls.thread_map[config_name]

    @classmethod
    def merge_configuration(cls, source_config_name, target_config_name):
        if cls.has_configuration(source_config_name):
            if cls.has_configuration(target_config_name):
                cls.thread_map[target_config_name.upper()] = cls.thread_map[source_config_name].clone()
            else:
                cls.register_new_configuration(target_config_name.upper())
                cls.thread_map[target_config_name.upper()] = cls.thread_map[source_config_name.upper()].clone()
        else:
            raise Exception("No source configuration found for name: %s".format(source_config_name))

    @classmethod
    def register_new_configuration(cls, config_name):
        cls.thread_map[config_name.upper()] = {}

    @classmethod
    def update_thread_config(cls, config_name, config):
        cls.thread_map[config_name].clone_add(config)

    @classmethod
    def value(cls, prop_name):
        # uc_prop_name = None
        # if type(prop_name) is not str:
        #     prop_name = self.__get_prop_path_for_enum(prop_name).upper()
        uc_prop_name = prop_name.upper()
        tname = thread_utils.get_current_thread_name()
        if tname in cls.thread_map and uc_prop_name in cls.thread_map[tname]:
            return cls.thread_map[tname][uc_prop_name].value
        elif uc_prop_name in cls.arjuna_options:
            return cls.arjuna_options[uc_prop_name].value
        else:
            raise Exception("No property configred for name: {}".format(prop_name))

    @classmethod
    def get_configured_name(self, section_name, internal_name):
        return self.strings_manager.get_configured_name(section_name, internal_name)

    @classmethod
    def get_problem_text(self, problem_code):
        return self.strings_manager.get_problem_text(problem_code)

    @classmethod
    def get_info_message_text(self, code):
        return self.strings_manager.get_info_message_text(code)

    @classmethod
    def clone_evars(self):
        return copy.deepcopy(self.exec_var_map)

    @classmethod
    def clone_user_options(self):
        return copy.deepcopy(self.user_options)

    def __init_logger(self, dl):
        from arjuna.core.enums import ArjunaOption
        log_dir = self.__ref_config.get_arjuna_option_value(ArjunaOption.PROJECT_RUN_LOG_DIR).as_str()
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)
        fl = logging.getLevelName(self.__ref_config.get_arjuna_option_value(ArjunaOption.LOG_FILE_LEVEL).as_str().upper())
        fname = "arjuna-run.log"
        lpath = os.path.join(log_dir, fname)

        logger = logging.getLogger("arjuna")
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler(sys.stdout)
        ch.flush = sys.stdout.flush
        ch.setLevel(dl)
        fh = logging.FileHandler(lpath, "w", 'utf-8')
        fh.setLevel(fl)
        f_fmt = logging.Formatter(u'[%(levelname)5s]\t%(asctime)s\t%(pathname)s::%(module)s.%(funcName)s:%(lineno)d\t%(message)s')
        c_fmt = logging.Formatter(u'[%(levelname)5s]\t%(message)s')
        ch.setFormatter(c_fmt)
        fh.setFormatter(f_fmt)
        logger.addHandler(ch)
        logger.addHandler(fh)

        self.__logger = logger

    def __load_console(self, dl, logger):
        class __console:
            lock = threading.RLock()

            def __init__(self):
                # self.lock = threading.RLock()
                self.separator = os.linesep
                self.log_display_level = dl
                self.logger = logger

            @sync_method('lock')
            def __log(self, message, err=False):
                if err:
                    mparts = message.replace(u"\r\n", u"--|--").replace(u"\n", u"--|--").split(u'--|--')
                    for mpart in mparts:
                        self.logger.error(mpart)
                else:
                    mparts = message.replace(u"\r\n", u"--|--").replace(u"\n", u"--|--").split(u'--|--')
                    for mpart in mparts:
                        self.logger.info(mpart)

            @sync_method('lock')
            def __print(self, message):
                print(message, end='', file=sys.stdout, flush=True)

            @sync_method('lock')
            def __eprint(self, message):
                print(message, end='', file=sys.stderr, flush=True)

            @sync_method('lock')
            def __println(self, message):
                print(message, file=sys.stdout, flush=True)

            @sync_method('lock')
            def __eprintln(self, message):
                print(message, file=sys.stderr, flush=True)

            @sync_method('lock')
            def __msg(self, *messages):
                return " ".join([str(m) for m in messages])

            @sync_method('lock')
            def display(self, *messages):
                message = self.__msg(*messages)
                should_print = self.__log(message)
                if should_print:
                    self.__println(message)

            @sync_method('lock')
            def display_error(self, *messages):
                message = self.__msg(*messages)
                should_print = self.__log(message, err=True)
                if should_print:
                    self.__eprintln(message)

            @sync_method('lock')
            def error_for_console(self, *messages):
                message = self.__msg(*messages)
                self.__eprintln(message)

            @sync_method('lock')
            def display_on_same_line(self, *messages):
                message = self.__msg(*messages)
                should_print = self.__log(message)
                if should_print:
                    self.__print(message)

            @sync_method('lock')
            def marker(self, length, symbol='-'):
                self.display(symbol * length)

            @sync_method('lock')
            def marker_error(self, length, symbol='-'):
                self.display_error(symbol * length)

            @sync_method('lock')
            def marker_on_same_line(self, length=40):
                self.display_on_same_line("-" * length)

            @sync_method('lock')
            def display_key_value(self, key, value):
                message = "%s %s".format(key, value)
                self.display(message)

            @sync_method('lock')
            def __get_formatted_key_value(self, key, value, left_padding):
                if not left_padding:
                    message = "| {:20s}| {}".format(key, value)
                else:
                    message = "| {}| {}".format(key.ljust(left_padding), value)
                return message

            @sync_method('lock')
            def __display_paddedKV(self, key, value, print_func, left_padding):
                print_func(self.__get_formatted_key_value(key, value, left_padding))

            @sync_method('lock')
            def display_padded_key_value(self, key, value, left_padding=None):
                self.__display_paddedKV(key, value, self.display, left_padding)

            @sync_method('lock')
            def display_padded_key_value_error(self, key, value, left_padding=None):
                self.__display_paddedKV(key, value, self.display_error, left_padding)

            @sync_method('lock')
            def display_exception_block(self, e, strace):
                self.marker_error(80)
                self.display_padded_key_value_error("Exception Type", e.__class__.__name__, 30)
                self.display_padded_key_value_error("Exception Message", str(e), 30)
                self.display_padded_key_value_exception_trace("Exception Trace", strace, 30)
                self.marker_error(80)

            def set_central_log_level(self, level):
                self.central_log_level = level

            @sync_method('lock')
            def display_multiline_key_value(self, key, value, left_padding=30):
                value = str(value)
                ctrace_parts = value.replace("\t", " ").replace("\r\n\r\n","\r\n").replace("\n\n","\n").split(sys_utils.get_line_separator())

                header = self.__get_formatted_key_value(key, ctrace_parts[0], left_padding)
                self.__log(header)
                # if should_print:
                #     self.error_for_console(header)

                for s in ctrace_parts[1:]:
                    message = self.__get_formatted_key_value("", s, left_padding)
                    self.__log(message)
                    # if should_print:
                    #     self.(message)

            display_padded_key_value_exception_trace = display_multiline_key_value
        self.__console = __console()

    @property
    def ref_config(self):
        return self.__ref_config

    def create_test_context(self, name):
        '''
            Creates test context object.
            ?? Does it take central config??
        '''

        from arjuna.configure.invoker.context import DefaultTestContext
        context = DefaultTestContext(self.__test_session, name)
        self.__context_map[name] = context
        return context

class Arjuna:
    '''
        Facade of Arjuna framework.
        Contains static methods which wrapper an internal singleton class for easy access to top level Arjuna functions.
    '''

    ARJUNA_SINGLETON = None
    LOGGER = None

    @classmethod
    def init(cls, project_root_dir, cli_config=None, run_id=None):
        '''
            Returns reference test context which contains reference configuration.
            This reference test context merges central conf, project conf and central CLI options.
            Root directory is assumed as per the project structure.
            You can also provide an alternative root directory for test project.
        '''
        cls.ARJUNA_SINGLETON = ArjunaSingleton()
        return cls.ARJUNA_SINGLETON.init(project_root_dir, cli_config, run_id)

    @classmethod
    def get_logger(cls):
        '''
            Returns framework logger.
        '''
        return cls.ARJUNA_SINGLETON.logger

    @classmethod
    def get_console(cls):
        '''
            Returns framework console.
        '''
        return cls.ARJUNA_SINGLETON.console

    @classmethod
    def get_ref_config(cls):
        '''
            Returns the reference configuration.
        '''
        return cls.ARJUNA_SINGLETON.ref_config

    @classmethod
    def get_gui_mgr(cls):
        '''
            Returns the central GUI Manager object that mangages namespaces.
        '''
        return cls.ARJUNA_SINGLETON.gui_mgr

    @classmethod
    def get_ref_arjuna_option_value(cls, option):
        return cls.get_central_config().get_ref_arjuna_option_value(option)

    @classmethod
    def get_ref_user_option_value(cls, option):
        return cls.get_central_config().get_ref_user_option_value(option) 

    @classmethod
    def get_data_store(cls):
        return cls.ARJUNA_SINGLETON.data_store

    @staticmethod
    def get_test_context(name):
        '''
            Returns test context for a given name (case-insensitive).
        '''
        pass

    @staticmethod
    def register_test_context(context):
        '''
            Registers a test context object.
        '''
        pass    

    @classmethod
    def create_test_context(cls, name):
        '''
            Creates test context object.
            ?? Does it take central config??
        '''
        return cls.ARJUNA_SINGLETON.create_test_context(name)

    @staticmethod
    def get_root_dir(context):
        '''
            Returns root directory of test project.
        '''
        pass

    @staticmethod
    def create_datasource_builder():
        '''
            Creates and returns DataSourceBuilder object.
        '''
        pass

    @staticmethod
    def exit():
        '''
            Clean-up and finalise resources currently opened by Arjuna.
        '''
        pass