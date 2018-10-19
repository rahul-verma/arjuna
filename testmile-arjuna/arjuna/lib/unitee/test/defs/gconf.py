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
from arjuna.lib.unitee.validation import checks
from arjuna.lib.unitee.exceptions import *

class Picker:

    def __init__(self, fpath, gname, pickers_node):
        self.gname = gname
        self.fpath = fpath
        self.root = pickers_node
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
            self.console.display_error((msg + " Fix groups template file: {}").format(self.fpath))
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

def none(value):
    if type(value) is str:
        return value.lower() == "none" and None or value
    else:
        return value is None and None or value

converter_map = {
    'int': int,
    'str': str,
    'float': float,
    'bool': bool,
    'none' : none
}

from enum import Enum, auto

class RuleType(Enum):
    INCLUSION = auto()
    EXCLUSION = auto()

class RuleTargetType(Enum):
    PROPS = auto()
    EVARS = auto()

class RuleConditionType(Enum):
    EQUAL = auto()
    NOT_EQUAL = auto()
    NONE = auto()
    NOT_NONE = auto()
    TRUE = auto()
    FALSE = auto()
    MATCH = auto()
    PARTIAL_MATCH = auto()

import re

single_value_checkers = {
    RuleConditionType.NONE : checks.is_none,
    RuleConditionType.NOT_NONE : checks.is_not_none,
    RuleConditionType.TRUE : checks.is_true,
    RuleConditionType.FALSE : checks.is_false
}

multi_value_checkers = {
    RuleConditionType.EQUAL : checks.are_equal,
    RuleConditionType.NOT_EQUAL : checks.are_not_equal,
    RuleConditionType.MATCH : checks.match,
    RuleConditionType.PARTIAL_MATCH : checks.partially_match,
}

class Rule:
    def __init__(self, rtype, target, robject, condition, expression, object_type):
        self.is_include_type = RuleType[rtype.upper().strip()] == RuleType.INCLUSION
        self.target = RuleTargetType[target.upper().strip()]
        self.robject = str(robject.strip())
        condition = re.sub(r"\s+", "_", condition.strip())
        self.condition = RuleConditionType[condition.upper()]
        self.expression = expression
        self.converter = converter_map[object_type.lower().strip()]

    def __not_met_exc(self):
        raise RuleNotMet() #"Run time rule checking did not succeed for the test object.")

    def __raise_exception_for_check_result(self, check_result):
        if check_result:
            if self.is_include_type:
                return
            else:
                self.__not_met_exc()
        else:
            if self.is_include_type:
                self.__not_met_exc()
            else:
                return

    def evaluate(self, test_object):
        include = False
        target_object = None
        if self.target == RuleTargetType.PROPS:
            o_container = None

            if test_object.type == TestObjectTypeEnum.Module:
                o_container = test_object.tvars.info.module
            elif test_object.type == TestObjectTypeEnum.Function:
                o_container = test_object.tvars.info.function
            else:
                return

            try:
                target_object = o_container.props[self.robject]
            except Exception as e:
                if self.is_include_type: self.__not_met_exc()
                return
            else:
                self.__raise_exception_for_check_result(self.__call_checker(target_object))

        else:
            raise Exception("Not supported yet.")

    def __call_checker(self, target_object):
        actual = self.converter(target_object)
        if self.condition in single_value_checkers:
            func = single_value_checkers[self.condition]
            return func(actual)
        elif self.condition in multi_value_checkers:
            expected = self.converter(self.expression)
            func = multi_value_checkers[self.condition]
            return func(actual, expected)

class Rules:

    def __init__(self, fpath, gname, rules_node):
        self.gname = gname
        self.fpath = fpath
        self.root = rules_node
        self.__rules = []

        from arjuna.lib.core import ArjunaCore
        self.console = ArjunaCore.console
        self.__process()

    def __process(self):
        def display_err_and_exit(msg):
            self.console.display_error((msg + " Fix groups template file: {}").format(self.fpath))
            sys_utils.fexit()

        node_dict = etree_utils.convert_to_cidict(self.root)

        # Validate only picker keys exist.
        if node_dict.keys() != {'rule'}:
            display_err_and_exit(">>rules<< element can contain only one or more >>rule<< element. Check group: {}.".format(self.gname))
        elif not node_dict:
            display_err_and_exit(">>rules<< element must contain atleast one >>rule<< element.Check group: {}.".format(self.gname))

        for rule in list(self.root):
            run_conf_utils.validate_rule_xml_child("groups", self.gname, self.fpath, rule)
            rule_dict = etree_utils.convert_attribs_to_cidict(rule)
            try:
                otype = 'object_type' in rule_dict and rule_dict['object_type'] or "str"
                exp = 'expression' in rule_dict and rule_dict['expression'] or None
                self.__rules.append(Rule(
                    rtype=rule_dict['type'],
                    target=rule_dict['target'],
                    robject=rule_dict['object'],
                    condition=rule_dict['condition'],
                    expression=exp,
                    object_type=otype
                ))
            except Exception as e:
                display_err_and_exit(
                    "Exception in processing >>rule<< element: {}. Check group: {}.".format(e, self.gname))

    def evaluate(self, test_object):
        for rule in self.__rules:
            rule.evaluate(test_object)

class GroupConf(Root):

    def __init__(self, name, gconf_xml, fpath):
        super().__init__()
        self.name = name
        self.evars = SingleObjectVars()
        self.picker = None
        self.__rules = None
        self.threads = 1
        self.fpath = fpath
        self.root = gconf_xml
        self.__fixtures = FixturesDef()
        self.__process()

    @property
    def fixture_defs(self):
        return self.__fixtures

    @property
    def rules(self):
        return self.__rules

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
            elif child_tag =='rules':
                self.__rules = Rules(self.fpath, self.name, child)
            else:
                display_err_and_exit("Unexpected element >>{}<< found in session definition.".format(child.tag))

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



