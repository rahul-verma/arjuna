'''
This file is a part of Test Mile Arjuna
Copyright 2018 Test Mile Software Testing Pvt Ltd

Website: www.TestMile.com
Email: support [at] testmile.com
Creator: Rahul Verma

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

import os
import shutil
import threading

ARJUNA_REF_NAME = "arjuna"
ARJUNA_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../../..'))
ARJUNA_RES_DIR = os.path.join(ARJUNA_ROOT, "arjuna", "res")
ARJUNA_LOG_DIR = ARJUNA_ROOT + "/log"
ARJUNA_LOG_NAME = ARJUNA_REF_NAME + ".log"
ARJUNA_CONF = ARJUNA_ROOT + "/config/" + ARJUNA_REF_NAME + ".conf"

import logging
import sys
import traceback

from arjuna.lib.core.thread.decorators import *
from arjuna.lib.core.utils import sys_utils
from arjuna.lib.core.integration.configurator import *
from arjuna.lib.core.adv.proxy import ROProxy
from arjuna.lib.core.adv.decorators import singleton


class InfoMessages:
    EXIT_ON_ERROR = "message.exit.on.error"

import os
import copy

from arjuna.lib.core.types.named_strings import *

from arjuna.lib.core import *
from arjuna.lib.core import ARJUNA_ROOT
from arjuna.lib.core.types.descriptors import *
from arjuna.lib.core.utils import thread_utils

class __Configuration:

    def __init__(self):
        self.prop_enum_to_prop_path_map = {}
        # It is base config object
        self.arjuna_options = {}
        # NAme of thread: Base configuration
        self.thread_map = {}
        # Strings manager object
        self.strings_manager = StringsManager()
        # DefaultStringKeyValueContainer
        self.exec_var_map = {}
        # DefaultStringKeyValueContainer
        self.user_options = {}

    def __get_prop_path_for_enum(self, prop_enum):
        key = "{}.{}".format((prop_enum.__class__.__name__).upper(), prop_enum.name)
        return self.prop_enum_to_prop_path_map[key]

    def get_central_property(self, prop):
        if type(prop) is str:
            return self.arjuna_options[prop]
        else:
            # enum
            return self.arjuna_options[self.__get_prop_path_for_enum(prop)]

    def has_configuration(self, config_name):
        return config_name.upper() in self.thread_map

    def has_property(self, config_name, path):
        return self.has_configuration(config_name) and path.upper() in self.thread_map[config_name]

    def merge_configuration(self, source_config_name, target_config_name):
        if self.has_configuration(source_config_name):
            if self.has_configuration(target_config_name):
                self.thread_map[target_config_name.upper()] = self.thread_map[source_config_name].clone()
            else:
                self.register_new_configuration(target_config_name.upper())
                self.thread_map[target_config_name.upper()] = self.thread_map[source_config_name.upper()].clone()
        else:
            raise Exception("No source configuration found for name: %s".format(source_config_name))


    def register_new_configuration(self, config_name):
        self.thread_map[config_name.upper()] = {}

    def update_thread_config(self, config_name, config):
        self.thread_map[config_name].clone_add(config)

    def value(self, prop_name):
        uc_prop_name = None
        if type(prop_name) is not str:
            prop_name = self.__get_prop_path_for_enum(prop_name).upper()
        uc_prop_name = prop_name.upper()
        tname = thread_utils.get_current_thread_name()
        if tname in self.thread_map and uc_prop_name in self.thread_map[tname]:
            return self.thread_map[tname][uc_prop_name].value
        elif uc_prop_name in self.arjuna_options:
            return self.arjuna_options[uc_prop_name].value
        else:
            raise Exception("No property configred for name: {}".format(prop_name))

    def get_configured_name(self, section_name, internal_name):
        return self.strings_manager.get_configured_name(section_name, internal_name)

    def get_problem_text(self, problem_code):
        return self.strings_manager.get_problem_text(problem_code)

    def get_info_message_text(self, code):
        return self.strings_manager.get_info_message_text(code)

    def clone_evars(self):
        return copy.deepcopy(self.exec_var_map)

    def clone_user_options(self):
        return copy.deepcopy(self.user_options)

class __ComponentIntegrator:
    def __init__(self, config):
        self.ref_dir = ARJUNA_ROOT
        self.proj_dir = None
        self.configurators = []
        self.configurator_map = {}
        self.central_config = config
        self.overrideable_properties = set()
        self.visiable_properties = set()
        self.readable_names = {}

        self.prop_name_to_component_map = {}
        self.prop_name_expected_type_map = {}

        self._frozen = False

    def add_configurator(self, configurator):
        self.configurators.append(configurator)
        self.configurator_map[configurator.get_component_name().upper()] = configurator

    def get_key_name_for_enum_constant(self, enum_const):
        return "%s.%s".format(enum_const.__class__.__name__, enum_const)

    def __validate_not_frozen(self):
        if self._frozen:
            raise Exception("Component integrator is in frozen state. You can not add any more properties.")

    def register_property(self, component_name, property):
        self.__validate_not_frozen()
        uc_component_name = component_name.upper()
        if uc_component_name not in self.configurator_map:
            raise Exception("No configurator found for component: {}".format(component_name))
        if property.value is None:
            raise Exception("{} supplied None types for {}".format(component_name, property.path))

        prop_name = property.path.upper()
        self.prop_name_to_component_map[prop_name] = component_name
        self.central_config.prop_enum_to_prop_path_map["{}".format(property.code.upper())] = prop_name
        self.central_config.arjuna_options[prop_name] = property
        self.prop_name_expected_type_map[prop_name] = property.value_type
        self.readable_names[prop_name] = property.text

        if property.overridable:
            self.overrideable_properties.add(prop_name)

        if property.visible:
            self.visiable_properties.add(prop_name)

    def enumerate(self):
        from arjuna.lib.core import ArjunaCore
        keys = list(self.central_config.arjuna_options.keys())
        keys.sort()
        ArjunaCore.console.marker(100)
        header = " Central Properties Table "
        mark_length = (50 - len(header)// 2)
        ArjunaCore.console.marker_on_same_line(mark_length)
        ArjunaCore.console.display_on_same_line(header)
        ArjunaCore.console.marker(mark_length)
        ArjunaCore.console.marker(100)
        for key in keys:
            if self.central_config.arjuna_options[key].visible:
                sval = self.central_config.arjuna_options[key].value
                if EnumConstant.check(sval):
                    sval = sval.name
                elif EnumConstantList.check(sval):
                    sval = str([i.name for i in sval])
                else:
                    if key != "arjuna.root.dir" and String.check(sval):
                        sval = sval.replace(ARJUNA_ROOT, "<arjuna_root_dir>")
                    else:
                        sval = str(sval)

                ArjunaCore.console.display(
                    "| {:60s}| {}".format(self.central_config.arjuna_options[key].text,
                                          sval))
                ArjunaCore.console.display("| {:60s}| {}".format("(" + key + ")", ""))
                ArjunaCore.console.marker(100)
        ArjunaCore.console.marker(100)

    def process_defaults(self):
        self.__validate_not_frozen()
        for configurator in self.configurators[1:]:
            configurator.process_defaults()

    def process_conf_file_options(self, properties):
        self.__validate_not_frozen()
        for configurator in self.configurators[1:]:
            configurator.process_conf_file_options(properties)

    def process_interface_options(self, properties):
        self.__validate_not_frozen()
        for configurator in self.configurators[1:]:
            configurator.process_interface_options(properties)

    def load(self):
        for configurator in self.configurators[1:]:
            configurator.load()

    def process_user_options(self, properties):
        self.__validate_not_frozen()
        self.central_config.user_options.update(properties)

    def process_evars(self, properties):
        self.__validate_not_frozen()
        self.central_config.exec_var_map.update(properties)

    def freeze(self):
        self._frozen = True
        return self.central_config

    def populate_messages(self, messages):
        self.central_config.strings_manager.populate_messages(messages)

    def populate_names(self, names):
        self.central_config.strings_manager.populate_names(names)

    def __get_prop_path_for_enum(self, prop_enum):
        key = "{}.{}".format(prop_enum.__class__.__name__.upper(),
                             prop_enum.name.upper())
        return self.central_config.prop_enum_to_prop_path_map[key]

    def value(self, enum_object):
        return self.central_config.value(enum_object)

    def value_type(self, enum_object):
        return self.central_config.value(enum_object).value_type

    def expected_value_type(self, obj):
        if type(obj) is str:
            return self.prop_name_expected_type_map[obj]
        else:
            # enum
            return self.prop_name_expected_type_map[self.__get_prop_path_for_enum(obj)]

class __CoreConfigurator(AbstractComponentConfigurator):
    def __init__(self, integrator):
        super().__init__(integrator, "ArjunaCore", CorePropertyTypeEnum)

    def _handle_log_level_config(self, prop_path, config_value, purpose, visible):
        try:
            prop = property_factory.create_enum_property(self._code_for_path(prop_path), prop_path, LoggingLevelEnum,
                                                         config_value,
                                                         purpose, visible)
        except Exception as e:
            raise Exception("Error in processing Logging Level configuration: " + str(e))
        else:
            self.register_property(prop)

    def _handle_logging_name(self, prop_path, config_value, purpose, visible):
        self.builder.overridable(False).visible(False)
        self._handle_string_config(prop_path, config_value, "Log file name", visible)

    def process_config_properties(self, properties):
        cases = {
            CorePropertyTypeEnum.ARJUNA_ROOT_DIR: (
                self._handle_core_dir_path, "Arjuna Root Directory", False),
            CorePropertyTypeEnum.CONFIG_PROJECTS_DIR: (
                self._handle_core_dir_path, "Configuration Directory for Project Information", False),
            CorePropertyTypeEnum.WORKSPACE_DIR: (
                self._handle_core_dir_path, "Default Projects Directory", False),
            CorePropertyTypeEnum.PROJECT_DIRS_FILES: (
                self._handle_string_list_config, "Arjuna Project Directory Names", False),
            CorePropertyTypeEnum.PROG: (
                self._handle_string_config, "Arjuna Reference Name", False),
            CorePropertyTypeEnum.CONFIG_CENTRAL_FILE_NAME: (
            self._handle_string_config, "Central Configuration File", False),
            CorePropertyTypeEnum.CONFIG_DIR: (self._handle_core_dir_path, "Configuration Directory", False),
            CorePropertyTypeEnum.EXTERNAL_TOOLS_DIR: (self._handle_core_dir_path, "Tools Directory", False),
            CorePropertyTypeEnum.EXTERNAL_IMP_DIR: (self._handle_core_dir_path, "Tools Directory", False),
            CorePropertyTypeEnum.LOGGER_CONSOLE_LEVEL: (self._handle_log_level_config, "Minimum Logging Message Level for Console Display", True),
            CorePropertyTypeEnum.LOGGER_DIR: (self._handle_core_dir_path, "Central Log Directory", False),
            CorePropertyTypeEnum.LOGGER_FILE_LEVEL: (
            self._handle_log_level_config, "Minimum Logging Message Level for File Log", True),
            CorePropertyTypeEnum.LOGGER_NAME: (self._handle_string_config, "Log file name", False),
        }

        handled_props = []

        for prop_path, c_value in properties.items():
            if not self.does_path_map_contain(prop_path): continue
            if c_value is None:
                handled_props.append(prop_path)
                continue
            switch = EnumSwitch(cases, (prop_path, c_value))
            switch(self._code_for_path(prop_path))
            handled_props.append(prop_path)

        for prop in handled_props:
            del properties[prop]

    def process_defaults(self):
        reader = HoconResourceReader("core.conf")
        reader.process()
        self.process_config_properties(reader.get_flat_map())
        self.configure_names(self.__get_all_names())
        self.configure_messages(self.__get_all_messages())

    def process_conf_file_options(self, properties):
        pass

    def process_interface_options(self, properties):
        pass

    def load(self):
        pass

    def __get_all_messages(self):
        from arjuna.lib.core import InfoMessages
        containers = []
        info_messages = MessagesContainer("INFO_MESSAGES")
        info_messages.add(Message(InfoMessages.EXIT_ON_ERROR, "Critical Error. Exiting."))
        containers.append(info_messages)
        return containers

    def __get_all_names(self):
        containers = []

        object_names = NamesContainer("COMPONENT_NAMES")
        object_names.add(Name("dsource", "Data Source"))
        containers.append(object_names)

        return containers

@singleton
class ArjunaCoreFacade:

    def init(self, integrator, configurator, arg_dict):
        self.integrator = integrator
        self.configurator = configurator
        self.config = None
        self.integrator.add_configurator(self.configurator)
        self.configurator.process_defaults()
        self.configurator.process_config_properties(arg_dict)
        self.prog = self.integrator.value(CorePropertyTypeEnum.PROG)
        dl = logging.getLevelName(self.integrator.value(CorePropertyTypeEnum.LOGGER_CONSOLE_LEVEL).name)
        log_dir = self.integrator.value(CorePropertyTypeEnum.LOGGER_DIR)
        fl = logging.getLevelName(self.integrator.value(CorePropertyTypeEnum.LOGGER_FILE_LEVEL).name)
        fname = self.integrator.value(CorePropertyTypeEnum.LOGGER_NAME)
        self.__init_logger(self.prog, dl, log_dir, fl, fname)
        self.console = self.create_console(self.prog, dl)
        self.log_file_discovery_info = False
        self._data_references = {}
        self.central_conf = None

    def __init_logger(self, prog, dl, log_dir, fl, fname):
        logger = logging.getLogger(prog)
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(dl)
        if not os.path.isdir(ARJUNA_LOG_DIR):
            os.makedirs(ARJUNA_LOG_DIR)
        fh = logging.FileHandler(os.path.join(ARJUNA_LOG_DIR, ARJUNA_LOG_NAME), "w")
        fh.setLevel(fl)
        f_fmt = logging.Formatter('[%(levelname)5s]\t%(asctime)s\t%(pathname)s::%(module)s.%(funcName)s:%(lineno)d\t%(message)s')
        c_fmt = logging.Formatter('%(message)s')
        ch.setFormatter(c_fmt)
        fh.setFormatter(f_fmt)
        logger.addHandler(ch)
        logger.addHandler(fh)

    def get_logger(self):
        return logging.getLogger(self.prog)

    def create_console(self, prog, dl):

        class __console:
            lock = threading.RLock()

            def __init__(self):
                # self.lock = threading.RLock()
                self.separator = os.linesep
                self.log_display_level = dl
                self.logger = logging.getLogger(prog)

            @sync_method('lock')
            def __log(self, message, err=False):
                if err:
                    mparts = message.replace("\r\n", "--|--").replace("\n", "--|--").split('--|--')
                    for mpart in mparts:
                        self.logger.error(mpart)
                else:
                    mparts = message.replace("\r\n", "--|--").replace("\n", "--|--").split('--|--')
                    for mpart in mparts:
                        self.logger.info(mpart)

            @sync_method('lock')
            def __print(self, message):
                print (message, end='', file=sys.stdout, flush=True)

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
        return __console()

    def freeze(self, integrator):
        self.config = integrator.freeze()

    logger = get_logger

ArjunaCore = ArjunaCoreFacade()

def init(arg_dict=None):
    integrator = __ComponentIntegrator(__Configuration())
    configurator = __CoreConfigurator(integrator)
    acore = ArjunaCoreFacade()
    acore.init(integrator, configurator, arg_dict)