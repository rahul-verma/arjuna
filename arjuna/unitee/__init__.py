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

from arjuna.tpi.enums import ArjunaOption
from arjuna.lib.adv.decorators import singleton
from arjuna.lib.reader.hocon import *
from arjuna.lib.utils import sys_utils
from arjuna.unitee.enums import *
from arjuna.unitee.types.root import Root
from arjuna.unitee.test.defs.gconf import GroupConfsLoader, GroupConf
from arjuna.unitee.state.defdb import *
from arjuna.lib.utils import file_utils, thread_utils
from arjuna.lib.config import InternalTestContext

@singleton
class Unitee:

    def __init__(self, setu_test_session, config):
        super().__init__()
        self.__state_mgr = None
        self.__reporter = None
        self.__test_loader = None
        self.__tdb = None
        self.__session = None
        self.__cli_picker_options = None
        self.__frozen = False
        self.__groups = None
        self.__setu_test_session = setu_test_session
        self.__config = config

        if self.__frozen:
            raise Exception("Unitee has already been loaded.")

        from arjuna.unitee.state.states import ThreadManager
        from arjuna.unitee.state.reporter import ActiveReporter
        self.__state_mgr = ThreadManager()
        self.__reporter = ActiveReporter()
        self.__reporter.set_up()

        from arjuna.unitee.state.loader import TestLoader
        self.__test_loader = TestLoader()

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

    def load_testdb(self):
        self.__tdb = DefDB()
        self.test_loader.load()
        self.__groups = GroupConfsLoader.load()

    def load_session_for_all(self):
        from arjuna.unitee.test.defs.session import MSessionAllTests
        sdef = MSessionAllTests()
        sdef.process()
        self.__session = sdef.pick()
        self.__session.context = self.__create_test_context()
        self.__session.load()

    def __create_test_context(self):
        context = InternalTestContext(self.__setu_test_session, "default", parent_config=self.__config)
        # Populate default config (central config post project conf processing)
        context.ConfigBuilder(code_mode=False).build()
        return context

    def load_session(self, session_name):
        from arjuna.tpi import Arjuna
        from arjuna.unitee.test.defs.session import UserDefinedSessionDef
        sdir = Arjuna.get_central_config().get_arjuna_option_value(ArjunaOption.UNITEE_PROJECT_SESSIONS_DIR).as_string()
        session_file_path = os.path.join(sdir, session_name + ".xml")
        if not file_utils.is_file(session_file_path):
            Arjuna.get_console().display_error("Not able to find session file {}.xml at {}".format(session_name, sdir))
            sys_utils.fexit()
        sdef = UserDefinedSessionDef(session_name, session_file_path)
        sdef.process()
        self.__session = sdef.pick()
        self.__session.context = self.__create_test_context()
        self.__session.load()

    def load_session_for_group(self, group_name):
        from arjuna.unitee.test.defs.session import MSessionSingleGroup
        sdef = MSessionSingleGroup(group_name)
        sdef.process()
        self.__session = sdef.pick()
        self.__session.context = self.__create_test_context()
        self.__session.load()

    def load_session_for_name_pickers(self, **picker_args):
        from xml.etree.ElementTree import Element, SubElement, Comment, tostring
        gname = '_mngroup'
        group_xml = Element('group')
        group_xml.attrib['name'] = gname

        pickers = Element('pickers')

        pattern_list = ['cm', 'im', 'cf', 'if']

        for picker in pattern_list:
            patterns = picker_args[picker]
            if patterns is not None:
                for pattern in patterns:
                    child = Element('picker')
                    child.attrib['type'] = picker
                    child.attrib['pattern'] = pattern
                    pickers.append(child)

        group_xml.append(pickers)

        gconf = GroupConf(gname, group_xml, "(Arjuna generated object)")
        self.__groups[gname] = gconf
        self.load_session_for_group(gname)

    def run(self):
        self.state_mgr.register_thread(thread_utils.get_current_thread_name())
        self.__session.run()

    def tear_down(self):
        self.__reporter.tear_down()