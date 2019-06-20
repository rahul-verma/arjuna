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

import importlib

import xml.etree.ElementTree as ETree

from arjuna.tpi import Arjuna
from arjuna.lib.utils import sys_utils
from arjuna.lib.utils import etree_utils
from arjuna.unitee.utils import run_conf_utils
from arjuna.unitee.types.root import Root
from arjuna.unitee.types.containers import *
from arjuna.lib.enums import *

from arjuna.lib.reader.textfile import *
from arjuna.lib.reader.hocon import *
from arjuna.unitee.test.defs.stage import *
from arjuna.unitee.test.objects.session import *
from arjuna.unitee.test.defs.fixture import *
from arjuna.lib.config import ConfigContainer


class __SessionDef(Root, metaclass=abc.ABCMeta):
    def __init__(self, sname):
        super().__init__()
        self.name = sname
        self.config = ConfigContainer()
        self.fpath = None
        self.raw_contents = None
        self.root = None
        self.stage_defs = []
        self.tmcount = 0
        # self.evars.update(self.central_config.clone_evars())
        self.__iter = None
        self.__fixtures = FixturesDef()
        self.logger = Arjuna.get_logger()
        self.unitee = Arjuna.get_unitee_instance()

    @property
    def fixture_defs(self):
        return self.__fixtures

    def process(self):
        def display_err_and_exit(msg):
            self.console.display_error((msg + " Fix session template file: {}").format(self.fpath))
            sys_utils.fexit()

        try:
            self.root = ETree.fromstring(self.raw_contents)
        except Exception as e:
            print(e)
            display_err_and_exit("Session definition could not be loaded because of errors in XML.")

        if self.root.tag != 'session':
            display_err_and_exit("Invalid session template file. Root element tag should be session.")

        node_dict = etree_utils.convert_to_cidict(self.root)

        if 'stages' not in node_dict:
            display_err_and_exit(">>stages<< must be specified in a session template.")

        for child_tag, child in node_dict.items():
            child_tag = child_tag.lower()
            if child_tag == 'config':
                config = child
                for option in config:
                    run_conf_utils.validate_config_xml_child("session", self.fpath, option)
                    run_conf_utils.add_config_node_to_configuration("session", self.config, option)
            elif child_tag == 'fixtures':
                fixtures = child
                for child in fixtures:
                    run_conf_utils.validate_fixture_xml_child("session", "session", self.fpath, child)
                    run_conf_utils.add_fixture_node_to_fixdefs(self.fixture_defs, child)
            elif child_tag =='stages':
                if "stage" not in etree_utils.convert_to_cidict(child):
                    display_err_and_exit(">>stages<< element in session definition must contain atleast one >>stage<< element.")

                stages = list(child)
                for index, stage in enumerate(stages):
                    run_conf_utils.validate_stage_xml_child("session", self.fpath, stage)
                    node = StageDef(self, index + 1, stage)
                    self.stage_defs.append(node)
            else:
                display_err_and_exit("Unexpected element >>{}<< found in session definition.".format(child.tag))

    def schedule(self):
        self.logger.debug("%s: Scheduling nodes".format(self.name))
        for stage in self.stage_defs:
            self.logger.debug("Session node: " + stage.get_name())
            stage.schedule()
            self.tmcount += stage.get_tmcount()
        self.__iter = iter(self.stage_defs)

    def pick(self):
        for stage_def in self.stage_defs:
            stage_def.pick()
        self.unitee.testdb.process_unpicked_and_skipped()
        self.unitee.testdb.process_dependencies()

        return TestSession(self)


class __MSessionDef(__SessionDef):
    def __init__(self, gname):
        super().__init__("msession")
        sr = TextResourceReader("st/msession.xml")
        contents = sr.read()
        sr.close()
        contents = contents.format(gname=gname)
        self.fpath = os.path.join(self.central_config.get_arjuna_option_value(ArjunaOption.ARJUNA_ROOT_DIR).as_string(),
                                  "arjuna/lib/res/st/msession.xml")
        self.raw_contents = contents


class MSessionAllTests(__MSessionDef):
    def __init__(self):
        super().__init__("_magroup")

class MSessionSingleGroup(__MSessionDef):
    def __init__(self, group_name):
        super().__init__(group_name)

class UserDefinedSessionDef(__SessionDef):
    def __init__(self, name, fpath):
        super().__init__(name)
        self.fpath = fpath
        f = open(self.fpath, "r")
        self.raw_contents = f.read()
        f.close()
