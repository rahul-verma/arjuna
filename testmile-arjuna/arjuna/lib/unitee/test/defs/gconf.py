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

import re
import xml.etree.ElementTree as ETree

from arjuna.lib.core.enums import *
from arjuna.lib.unitee.enums import *
from arjuna.lib.unitee.types.containers import *
from arjuna.lib.core.reader.hocon import *
from arjuna.lib.core.reader.textfile import *
from arjuna.lib.unitee.types.root import *
from arjuna.lib.unitee.test.defs.fixture import *

from arjuna.lib.core.utils import sys_utils
from arjuna.lib.core.utils import etree_utils
from arjuna.lib.unitee.utils import run_conf_utils

class Picker:

    def __init__(self, fpath, gname, picker_node):
        self.gname = gname
        self.fpath = fpath
        self.root = picker_node
        self._rule_dict = CIStringDict(
            {
                'cm': [],
                'im': [],
                'cf': [],
                'if': []
            }
        )

        from arjuna.lib.core import ArjunaCore
        self.console = ArjunaCore.console
        self.tm_prefix = ArjunaCore.config.value(UniteePropertyEnum.TEST_MODULE_IMPORT_PREFIX)
        self.__process()

    def __process(self):
        def display_err_and_exit(msg):
            self.console.display_error((msg + " Fix session template file: {}").format(self.fpath))
            sys_utils.fexit()

        node_dict = etree_utils.convert_to_cidict(self.root)
        pattern_set = {i.lower() for i in self._rule_dict.keys()}

        # Validate only picker keys exist.
        if node_dict.keys() != {'picker'}:
            display_err_and_exit(">>pickers<< element can contain only one or more >>picker<< element. Check group: {}".format(self.gname))
        elif not node_dict:
            display_err_and_exit(">>pickers<< element must contain atleast one >>picker<< element.Check group: {}".format(self.gname))

        for pattern in list(self.root):
            run_conf_utils.validate_pattern_xml_child("groups", self.gname, self.fpath, pattern)
            pattern_dict = etree_utils.convert_attribs_to_cidict(pattern)
            pattern_name = pattern_dict['type'].lower()
            if pattern_name not in pattern_set:
                display_err_and_exit(
                    ">>picker<< element type attribute can only contain one of {}.Check group: {}".format(
                        pattern_set,
                        self.gname))
            pattern_value = pattern_dict['pattern'].strip()
            if not pattern_value:
                display_err_and_exit(
                    ">>picker<< element's >>pattern<< attribute can not be empty.Check group: {}".format(
                        pattern_set,
                        self.gname))

            if pattern_name in {'cm', 'im'}:
                self._rule_dict[pattern_name].append(re.compile(self.tm_prefix + pattern_value))
            else:
                self._rule_dict[pattern_name].append(re.compile(pattern_value))


    def include_module(self, mname):
        if self._rule_dict['cm']:
            consider = False
            for reg in self._rule_dict['cm']:
                if reg.match(mname):
                    consider = True
            return consider

        if self._rule_dict['im']:
            consider = True
            for reg in self._rule_dict['im']:
                if reg.match(mname):
                    consider = False
            return consider

        return True

    def include_func(self, fname):

        if self._rule_dict['cf']:
            consider = False
            for reg in self._rule_dict['cf']:
                if reg.match(fname):
                    consider = True
            return consider

        if self._rule_dict['if']:
            consider = True
            for reg in self._rule_dict['if']:
                if reg.match(fname):
                    consider = False
            return consider

        return True

class GroupConf(Root):

    def __init__(self, name, gconf_xml, fpath):
        super().__init__()
        self.name = name
        self.evars = SingleObjectVars()
        self.picker = None
        self.threads = 1
        self.fpath = fpath
        self.root = gconf_xml
        self.__fixtures = FixturesDef()
        self.__process()

    @property
    def fixture_defs(self):
        return self.__fixtures

    def __process(self):
        def display_err_and_exit(msg):
            self.console.display_error((msg + " Fix group template file: {}").format(self.fpath))
            sys_utils.fexit()

        node_dict = etree_utils.convert_to_cidict(self.root)

        # Validate only group keys exist.
        if 'pickers' not in node_dict:
            display_err_and_exit(">>group<< element must contain >>pickers<< element.")

        for child_tag, child in node_dict.items():
            child_tag = child_tag.lower()
            if child_tag == 'evars':
                evars = child
                for child in evars:
                    run_conf_utils.validate_evar_xml_child("groups", self.fpath, child)
                    run_conf_utils.add_evar_node_to_evars("groups", self.evars, child)
            elif child_tag == 'fixtures':
                fixtures = child
                for child in fixtures:
                    run_conf_utils.validate_fixture_xml_child("groups", "group", self.fpath, child)
                    run_conf_utils.add_fixture_node_to_fixdefs(self.fixture_defs, child)
            elif child_tag =='pickers':
                self.picker = Picker(self.fpath, self.name, child)

class GroupConfsLoader:

    def __load_pick_all(gconfs):
        from arjuna.lib.core import ArjunaCore
        central_config = ArjunaCore.config
        fpath = os.path.join(central_config.value(CorePropertyTypeEnum.ARJUNA_ROOT_DIR),
                                  "arjuna/lib/res/st/magroup.xml")
        group_xml = ETree.parse(fpath).getroot()
        group_name = group_xml.attrib['name']
        gconfs[group_name] = GroupConf(group_name, group_xml, fpath)

    def __load_user_gconfs(gconfs):
        from arjuna.lib.core import ArjunaCore
        console = ArjunaCore.console
        ugcdir = ArjunaCore.config.value(UniteePropertyEnum.PROJECT_CONFIG_DIR)
        ugfpath = os.path.join(ugcdir, "groups.xml")

        def display_err_and_exit(msg):
            console.display_error((msg + " Fix groups template file: {}").format(ugfpath))
            sys_utils.fexit()

        try:
            tree = ETree.parse(ugfpath)
        except Exception as e:
            print(e)
            display_err_and_exit("Groups definition file could not be loaded because of errors in XML.")
        else:
            root = tree.getroot()
            if root.tag != 'groups':
                display_err_and_exit("Invalid groups template file. Root element tag should be >>groups<<.")
            node_dict = etree_utils.convert_to_cidict(root)

            # Validate only group keys exist.
            if node_dict.keys() != {'group'}:
                display_err_and_exit(">>groups<< element can contain only one or more >>group<< elements.")
            elif not node_dict:
                display_err_and_exit(">>groups<< element must contain atleast one >>group<< element.")
            else:
                for group in list(root):
                    run_conf_utils.validate_group_xml_child("session", ugfpath, group)
                    group_attrs = etree_utils.convert_attribs_to_cidict(group)
                    name = group_attrs['name'].strip()
                    if not name:
                        display_err_and_exit(">>name<< attribute in group definition can not be empty.")
                    gconfs[name] = GroupConf(name, group, ugfpath)


    def load():
        gconfs = CIStringDict()
        GroupConfsLoader.__load_pick_all(gconfs)
        GroupConfsLoader.__load_user_gconfs(gconfs)
        return gconfs



