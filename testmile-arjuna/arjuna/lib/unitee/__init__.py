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

import datetime
import re
import types

from arjuna.lib.core.adv.py import EnumSwitch
from arjuna.lib.core.adv.decorators import singleton
from arjuna.lib.core.config import property_factory
from arjuna.lib.core.enums import *
from arjuna.lib.core.integration.configurator import AbstractComponentConfigurator
from arjuna.lib.core.reader.hocon import *
from arjuna.lib.core.reader.textfile import TextResourceReader
from arjuna.lib.core.types.named_strings import *
from arjuna.lib.core.utils import sys_utils
from arjuna.lib.unitee.enums import *
from arjuna.lib.unitee.enums import *
from arjuna.lib.core.adv.proxy import ROProxy
from arjuna.lib.unitee.types.root import Root
from arjuna.lib.unitee.test.defs.gconf import GroupConfsLoader, GroupConf
from arjuna.lib.unitee.state.defdb import *
from arjuna.lib.core import ArjunaCore
from arjuna.lib.core.utils import file_utils, thread_utils

class UniteeNames:
    @staticmethod
    def get_all_names():
        return []


class __UniteeConfigurator(AbstractComponentConfigurator):
    def __init__(self, integrator, project_name, proj_parent_dir, runid):
        super().__init__(integrator, "Unitee", UniteePropertyEnum)
        from arjuna.lib.core import ArjunaCore
        self.component = None
        self.logger = ArjunaCore.get_logger()
        self._integrator = integrator
        self.project_name = project_name
        self.proj_parent_dir = proj_parent_dir
        self.proj_full_path = file_utils.normalize_path(os.path.join(self.proj_parent_dir, self.project_name))
        self.runid = runid and runid or "mrunid"
        self.irunid = "{}-{}".format(datetime.datetime.now().strftime("%Y.%m.%d-%H.%M.%S.%f")[:-3], self.runid)
        self.__overridable = set()

        self.__load_project_console()

    def __load_project_console(self):
        from arjuna.lib.core import ArjunaCore
        lpath = os.path.join(self.proj_full_path, "log")
        if not os.path.isdir(lpath):
            os.makedirs(lpath)
        ArjunaCore.load_console(lpath)


    def _handle_project_dir_path(self, prop_path, config_value, purpose, visible):
        prop = property_factory.create_project_dir_path(self.proj_full_path, self._code_for_path(prop_path), prop_path,
                                                        config_value,
                                                        purpose, visible)
        self.register_property(prop)

    def _handle_active_reporter_names(self, prop_path, config_value, purpose, visible):
        prop = None
        try:
            prop = property_factory.create_enum_list_property(self._code_for_path(prop_path), prop_path,
                                                              ActiveReporterNames, config_value, purpose, visible)
        except IncompatibleInputForValueException as e:
            ArjunaCore.console.display_error("Error: Invalid Report Generator Format supplied.")
            ArjunaCore.console.display_error(
                "Solution: Check configuration files and CLI options that you have provided. Allowed formats: EXCEL.")
            # comments.SLC_629
            sys_utils.fexit()

        self.register_property(prop)

    def _handle_deferred_reporter_names(self, prop_path, config_value, purpose, visible):
        prop = None
        try:
            prop = property_factory.create_enum_list_property(self._code_for_path(prop_path), prop_path,
                                                              DeferredReporterNames, config_value, purpose, visible)
        except IncompatibleInputForValueException as e:
            ArjunaCore.console.display_error("Error: Invalid Report Listener Format supplied.")
            ArjunaCore.console.display_error(
                "Solution: Check configuration files and CLI options that you have provided. Allowed formats: CONSOLE.")
            # comments.SLC_629
            sys_utils.fexit()

        self.register_property(prop)

    def _handle_runid(self, prop_path, config_value, purpose, visible):
        m = re.match(r"^[a-zA-Z0-9\-_]{3,30}$", config_value)
        if m is None:
            raise Exception(
                "Invalid run id. It can only contain alphanumeric, - and _ chars. Length should be between 3 and 30 chars.")
        self._handle_string_config(purpose, visible, prop_path, config_value)
        prop = property_factory.create_enum_list_property(self._code_for_path(prop_path), prop_path,
                                                          IgnoredTestStatusEnum, config_value, purpose, visible)
        self.register_property(prop)

    def __cases(self):
        return {
            UniteePropertyEnum.PROJECT_NAME: (self._handle_string_config, "Project Name", False),
            UniteePropertyEnum.PROJECT_DIR: (self._handle_core_dir_path, "Project Root Directory", False),
            UniteePropertyEnum.PROJECT_CONFIG_DIR: (self._handle_core_dir_path, "Project Config Directory", False),
            UniteePropertyEnum.DATA_REFERENCES_DIR: (
                self._handle_project_dir_path, "Data References Directory", False),
            UniteePropertyEnum.DATA_DIR: (self._handle_project_dir_path, "Data Directory", False),
            UniteePropertyEnum.DATA_SOURCES_DIR: (
                self._handle_project_dir_path, "Data Sources Directory", False),
            UniteePropertyEnum.SCREENSHOTS_DIR: (
                self._handle_project_dir_path, "Screenshots Directory", False),
            UniteePropertyEnum.SESSION_NAME: (self._handle_string_config, "Test Session Name", False),
            UniteePropertyEnum.IRUNID: (self._handle_string_config, "Internal Run ID", False),
            UniteePropertyEnum.RUNID: (self._handle_string_config, "Test Run ID", True),
            UniteePropertyEnum.FAILFAST: (self._handle_boolean_config, "Stop on first failure/error?", False),
            UniteePropertyEnum.TESTS_DIR: (self._handle_project_dir_path, "Test Directory", True),
            UniteePropertyEnum.REPORT_DIR: (self._handle_project_dir_path, "Report Directory", False),
            UniteePropertyEnum.ARCHIVES_DIR: (self._handle_project_dir_path, "Report Archives directory", False),
            UniteePropertyEnum.SESSIONS_DIR: (self._handle_project_dir_path, "Session Templates directory", False),
            UniteePropertyEnum.GROUPS_DIR: (self._handle_project_dir_path, "Group Templates directory", False),
            UniteePropertyEnum.RUN_REPORT_DIR: (self._handle_string_config, "Report Directory for the Run ID", False),
            UniteePropertyEnum.RUN_REPORT_JDB_DIR: (
                self._handle_string_config, "Report Directory for the Run ID for JDB", False),
            UniteePropertyEnum.RUN_REPORT_JSON_DIR: (
                self._handle_string_config, "Root Raw Report Directory for JSON.", False),
            UniteePropertyEnum.RUN_REPORT_JSON_TESTS_DIR: (
                self._handle_string_config, "Raw Report Directory for JSON Test Execution results.", False),
            UniteePropertyEnum.RUN_REPORT_JSON_ISSUES_DIR: (
                self._handle_string_config, "Report Directory for JSON Fixture results.", False),
            UniteePropertyEnum.RUN_REPORT_JSON_IGNOREDTESTS_DIR: (
                self._handle_string_config, "Report Directory for JSON Ignored Test results.", False),
            UniteePropertyEnum.RUN_REPORT_JSON_EVENTS_DIR: (
                self._handle_string_config, "Report Directory for JSON Event results.", False),
            UniteePropertyEnum.RUN_REPORT_JSON_FIXTURES_DIR: (
                self._handle_string_config, "Report Directory for JSON Fixture results.", False),
            UniteePropertyEnum.REPORT_NAME_FORMAT: (self._handle_string_config, "Report Name Format", False),
            UniteePropertyEnum.ACTIVE_REPORTERS: (
                self._handle_active_reporter_names, "Chosen Built-in Report Generators", True),
            UniteePropertyEnum.DEFERRED_REPORTERS: (
                self._handle_deferred_reporter_names, "Chosen Built-in Report Listeners", True),
            UniteePropertyEnum.CORE_DIR: (self._handle_string_config, "Core Root Directory.", False),
            UniteePropertyEnum.CORE_DB_CENTRAL_DIR: (self._handle_string_config, "Core Central DB Directory.", False),
            UniteePropertyEnum.CORE_DB_CENTRAL_DBFILE: (self._handle_string_config, "Core Central DB File.", False),
            UniteePropertyEnum.CORE_DB_RUN_DIR: (self._handle_string_config, "Core Run DB Directory.", False),
            UniteePropertyEnum.CORE_DB_RUN_DBFILE: (self._handle_string_config, "Core Current Run DB File.", False),
            UniteePropertyEnum.CORE_DB_TEMPLATE_DIR: (self._handle_string_config, "Core Template DB Directory.", False),
            UniteePropertyEnum.CORE_DB_TEMPLATE_CENTRAL_DBFILE: (
                self._handle_string_config, "Core DB Template for Central DB.", False),
            UniteePropertyEnum.CORE_DB_TEMPLATE_RUN_DBFILE: (
                self._handle_string_config, "Core DB Template for Run DB.", False),
        }

    def __process_arjuna_option(self, prop_path, c_value, handled_list=None):
        if not self.does_path_map_contain(prop_path): return
        if c_value is not None:
            switch = EnumSwitch(self.__cases(), (prop_path, c_value))
            switch(self._code_for_path(prop_path))

        # Processed ones as well as those with None value.
        if handled_list is not None:
            handled_list.append(prop_path)

    def __process_arjuna_options(self, properties, filter=False):
        handled_list = []
        for prop_path, c_value in properties.items():
            if not filter or prop_path.upper() in self.__overridable:
                self.__process_arjuna_option(prop_path, c_value, handled_list)

        for prop in handled_list:
            del properties[prop]

    def process_defaults(self):
        trr = TextResourceReader("unitee.conf")
        contents = trr.read()
        trr.close()
        contents = contents.format(proj_name=self.project_name, proj_dir=self.proj_full_path,
                                   runid=self.runid,
                                   irunid=self.irunid)
        hrr = HoconStringReader(contents)
        hrr.process()
        self.__process_arjuna_options(hrr.get_flat_map())
        self.configure_names(self.__get_all_names())
        self.configure_messages(self.__get_all_messages())

    def process_conf_file_options(self, properties):
        self.__process_arjuna_options(properties, filter=True)

    def process_interface_options(self, properties):
        self.__process_arjuna_options(properties)

    def set_component(self, comp):
        self.component = comp

    def load(self):
        self.component._load()

    def __get_all_messages(self):
        from arjuna.lib.unitee import InfoMessages, ProblemMessages
        containers = []

        problem_messages = MessagesContainer("PROBLEM_MESSAGES")
        problem_messages.add(Message(
            ProblemMessages.REPORT_WRONG_FORMAT,
            "!!!Wrong Report Format(s) Supplied!!!"
        ))
        containers.append(problem_messages)
        info_messages = MessagesContainer("INFO_MESSAGES")

        info_messages.add(Message(
            InfoMessages.RUN_BEGIN,
            "------------ RUN: START -----------------"
        ))

        info_messages.add(Message(
            InfoMessages.RUN_FINISH,
            "------------ RUN: FINISH -----------------"
        ))

        info_messages.add(Message(
            InfoMessages.PRINT_CONFIGURATION,
            "Proceeding with the following Configuration Settings:"
        ))

        info_messages.add(Message(
            InfoMessages.TESTRUNNER_CREATE_START,
            "Create Test Runner - Start"
        ))

        info_messages.add(Message(
            InfoMessages.TESTRUNNER_CREATE_FINISH,
            "Create Test Runner - Finish"
        ))

        info_messages.add(Message(
            InfoMessages.TESTREPORTER_CREATE_START,
            "Create Test Reporter - Start"
        ))

        info_messages.add(Message(
            InfoMessages.TESTREPORTER_CREATE_FINISH,
            "Create Test Reporter - Finish"
        ))

        info_messages.add(Message(
            InfoMessages.TEST_DISCOVERY_START,
            "Discovering tests..."
        ))

        info_messages.add(Message(
            InfoMessages.TEST_DISCOVERY_FINISH,
            "Discovery completed."
        ))

        info_messages.add(Message(
            InfoMessages.ALLOWED_REPORT_FORMATS,
            "Allowed Formats: XML/XLS/DELIMITED/INI/CONSOLE"
        ))
        containers.append(info_messages)

        return containers


    def __get_all_names(self):
        return UniteeNames.get_all_names()  # Types of reporting would be Active, Deferred and Offline

@singleton
class UniteeFacade:

    def __init__(self):
        super().__init__()
        self.__state_mgr = None
        self.__reporter = None
        self.__test_loader = None
        self.__tdb = None
        self.__session = None
        self.__cli_picker_options = None
        self.__frozen = False
        self.__groups = None

    @property
    def state_mgr(self):
        return self.__state_mgr

    @property
    def reporter(self):
        return self.__reporter

    @property
    def session(self):
        return self.__session

    @property
    def test_loader(self):
        return self.__test_loader

    @property
    def groups(self):
        return self.__groups

    @property
    def testdb(self):
        return self.__tdb

    def _load(self):
        if self.__frozen:
            raise Exception("Unitee has already been loaded.")
        from arjuna.lib.unitee.state.states import ThreadManager
        from arjuna.lib.unitee.state.reporter import ActiveReporter
        self.__state_mgr = ThreadManager()
        self.__reporter = ActiveReporter()
        self.__reporter.set_up()

        from arjuna.lib.unitee.state.loader import TestLoader
        self.__test_loader = TestLoader()

    def load_testdb(self):
        self.__tdb = DefDB()
        self.test_loader.load()
        self.__groups = GroupConfsLoader.load()

    def load_session_for_all(self):
        from arjuna.lib.unitee.test.defs.session import MSessionAllTests
        sdef = MSessionAllTests()
        sdef.process()
        self.__session = sdef.pick()
        self.__session.load()

    def load_session(self, session_name):
        from arjuna.lib.unitee.test.defs.session import UserDefinedSessionDef
        sdir = ArjunaCore.config.value(UniteePropertyEnum.SESSIONS_DIR)
        session_file_path = os.path.join(sdir, session_name + ".conf")
        if not file_utils.is_file(session_file_path):
            ArjunaCore.console.display_error("Not able to find session file {}.conf at {}".format(session_name, sdir))
            sys_utils.fexit()
        sdef = UserDefinedSessionDef(session_name, session_file_path)
        sdef.process()
        self.__session = sdef.pick()
        self.__session.load()

    def load_session_for_group(self, group_name):
        from arjuna.lib.unitee.test.defs.session import MSessionSingleGroup
        sdef = MSessionSingleGroup(group_name)
        sdef.process()
        self.__session = sdef.pick()
        self.__session.load()

    def load_session_for_name_pickers(self, cms, ims, cfs, ifs):
        picker = {}
        if cms is not None:
            picker['cm'] = cms
        if ims is not None:
            picker['im'] = ims
        if cfs is not None:
            picker['cf'] = cfs
        if ifs is not None:
            picker['if'] = ifs
        d = {'picker': picker}
        gconf = GroupConf('_mngroup', d, "--builtin--")
        self.__groups['_mngroup'] = gconf
        self.load_session_for_group('_mngroup')

    def run(self):
        Unitee.state_mgr.register_thread(thread_utils.get_current_thread_name())
        self.__session.run()

    def tear_down(self):
        self.__reporter.tear_down()

class ProblemMessages:
    REPORT_WRONG_FORMAT = "problem.report.wrong.format"


class InfoMessages:
    EXIT_ON_ERROR = "message.exit.on.error"
    RUN_BEGIN = "message.run.begin"
    RUN_FINISH = "message.run.finish"
    PRINT_CONFIGURATION = "message.print.configuration"
    TEST_DISCOVERY_START = "message.test.discovery.start"
    TEST_DISCOVERY_FINISH = "message.test.discovery.finish"
    TESTRUNNER_CREATE_START = "message.testrunner.create.start"
    TESTRUNNER_CREATE_FINISH = "message.testrunner.create.finish"
    TESTREPORTER_CREATE_START = "message.testreporter.create.start"
    TESTREPORTER_CREATE_FINISH = "message.testreporter.create.finish"
    ALLOWED_REPORT_FORMATS = "message.state.allowed.formats"

Unitee = UniteeFacade()

def init(pname, ppd, runid="mrunid"):
    integrator = ArjunaCore.integrator
    configurator = __UniteeConfigurator(integrator, pname, ppd, runid)
    integrator.add_configurator(configurator)
    configurator.process_defaults()
    unitee = UniteeFacade()
    configurator.set_component(unitee)
