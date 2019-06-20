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

from arjuna.tpi import Arjuna
from arjuna.unitee.types.root import *
from arjuna.unitee.types.containers import *
from arjuna.lib.reader.hocon import *
from arjuna.lib.utils import sys_utils
from arjuna.unitee.test.defs.fixture import *

from .group import *

from xml.etree.ElementTree import Element

from arjuna.lib.utils import etree_utils
from arjuna.unitee.utils import run_conf_utils
from arjuna.lib.config import ConfigContainer

class StageDef(Root):
    def __init__(self, sdef, id, stage_xml):
        super().__init__()
        self.gdefs = []
        self.config = ConfigContainer()
        self.tmcount = 0
        self.threads = 1
        self.sdef = sdef
        self.__iter = None
        self.__fixtures = FixturesDef()
        self.root = stage_xml

        self.unitee = Arjuna.get_unitee_instance()

        self.id = id
        self.name = "stage{:d}".format(id)

        if not isinstance(stage_xml, Element):
            self.console.display_error("Fatal: [Arjuna Error] Unsuppored input argument supplied for stage creation: {}".format(stage_xml))
            sys_utils.fexit()
        else:
            self.__process(stage_xml)
            # self.nodes.append(SessionSubNode(self, len(self.nodes) + 1, input))

    @property
    def fixture_defs(self):
        return self.__fixtures

    def __process(self, group_hocon):
        def display_err_and_exit(msg):
            self.console.display_error((msg + " Fix session template file: {}").format(self.sdef.fpath))
            sys_utils.fexit()

        stage_attrs = etree_utils.convert_attribs_to_cidict(self.root)

        if "name" in stage_attrs:
            self.name = stage_attrs['name'].strip()
            if not self.name:
                display_err_and_exit(">>name<< attribute in stage definition should be a non-empty string.")

        threads_err_msg = ">>threads<< attribute in stage definition can be integer >=1."
        if "threads" in stage_attrs:
            self.threads = stage_attrs['threads'].strip()
            try:
                self.threads = int(self.threads)
            except:
                display_err_and_exit(threads_err_msg)
            else:
                if self.threads <=0:
                    display_err_and_exit(threads_err_msg)


        node_dict = etree_utils.convert_to_cidict(self.root)

        if "groups" not in node_dict:
            display_err_and_exit(">>stage<< element in session definition must contain >>groups<< element.")

        for child_tag, child in node_dict.items():
            child_tag = child_tag.lower()
            if child_tag == 'config':
                config = child
                for option in config:
                    run_conf_utils.validate_config_xml_child("session", self.sdef.fpath, option)
                    run_conf_utils.add_config_node_to_configuration("session", self.config, option)
            elif child_tag == 'fixtures':
                fixtures = child
                for child in fixtures:
                    run_conf_utils.validate_fixture_xml_child("session", "stage", self.sdef.fpath, child)
                    run_conf_utils.add_fixture_node_to_fixdefs(self.fixture_defs, child)
            elif child_tag =='groups':
                if "group" not in etree_utils.convert_to_cidict(child):
                    display_err_and_exit(">>groups<< element in stage definition must contain atleast one >>group<< element.")

                groups = list(child)

                for index, group in enumerate(groups):
                    run_conf_utils.validate_group_xml_child("session", self.sdef.fpath, group)
                    node = GroupDef(self.sdef, self, len(self.gdefs) + 1, group)
                    self.gdefs.append(node)
            else:
                display_err_and_exit("Unexpected element >>{}<< found in >>stage<< definition in session file.".format(child.tag))

    def pick(self):
        for gdef in self.gdefs:
            self.tmcount += gdef.pick()

        self.__iter = iter(self.gdefs)