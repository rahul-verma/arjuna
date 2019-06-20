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

import xml.etree.ElementTree as ETree
import re

from arjuna.lib.utils import sys_utils
from arjuna.lib.utils import etree_utils
from arjuna.unitee.utils import run_conf_utils
from arjuna.unitee.markup import mrules

from .builder import RuleBuilder
from .common.ref import *

class XmlRules:

    def __init__(self, fpath, gname, rules_node):
        self.gname = gname
        self.fpath = fpath
        self.root = rules_node
        self.__rules = []
        from arjuna.tpi import Arjuna
        self.console = Arjuna.get_console()
        self.__process()


    def __create_rule(self, rule, tobject, rule_type, rcontainer, robject, condition, expression):
        if not robject:
            raise Exception("Target Rule Object not defined.")
        if not condition:
            raise Exception("Target condition not defined.")
        if not expression:
            raise Exception("Target expression not defined.")

        rule_builder = RuleBuilder()
        rule_builder.xml(rule)
        rule_builder.test_object_type(tobject)
        rule_builder.rule_type(rule_type)
        rule_builder.target(rcontainer)
        if (type(robject) is str):
            rule_builder.rule_object(robject.lower())
            rule_builder.condition(condition.upper())
        else:
            rule_builder.rule_object(robject)
            rule_builder.condition(condition)

        rule_builder.expression(expression)
        self.__rules.append(rule_builder.build())

    def __create_4_word_rule_for_container(self, rule, tobject, rule_type, match):
        container = match.group('container').lower()
        if container not in PROPERTY_CONTAINER_MAP:
            raise Exception("Property type in a rule definition can only be one of : {}".format(
                list(PROPERTY_CONTAINER_MAP.keys())
            ))
        self.__create_rule(rule, tobject, rule_type, PROPERTY_CONTAINER_MAP[container], match.group('object'), match.group('condition'),match.group('expression'))

    def __create_3_word_value_rule_for_prop(self, rule, tobject, rule_type, match):
        self.__create_rule(rule, tobject, rule_type, RuleTargetType.PROPS, match.group('object'), match.group('condition'), match.group('expression'))

    def __create_2_word_value_rule_for_tags(self, rule, tobject, rule_type, match):
        tags = [i.strip().lower() for i in match.group('object').split(',')]
        self.__create_rule(rule, tobject, rule_type, RuleTargetType.TAGS, tags, 'is', 'defined')

    def __create_4_word_value_rule_for_multi_defined(self, rule, tobject, rule_type, match):
        container = match.group('container').lower()
        if container not in CONTAINER_MAP:
            raise Exception("Property type in a rule definition for an >>are defined/present<< condition can only be one of : {}".format(
                list(CONTAINER_MAP.keys())
            ))
        tags = [i.strip().lower() for i in match.group('object').split(',')]
        self.__create_rule(rule, tobject, rule_type, CONTAINER_MAP[container], tags,
                           RuleConditionType.CONTAINS, match.group('expression'))

    def __create_1_word_boolean_rule(self, rule, tobject, rule_type, match):
        robject = match.group('object').lower()
        if (mrules.is_builtin_prop(robject) and mrules.get_value_type(robject) is not bool) \
                or \
                (not mrules.is_builtin_prop(robject)):
            raise Exception("One word rules are available only for built-in properties of boolean nature.")
        self.__create_rule(rule, tobject, rule_type, RuleTargetType.PROPS, robject, 'is', 'True')

    def __process(self):
        def display_err_and_exit(msg):
            self.console.display_error((msg + " Fix groups template file: {}").format(self.fpath))
            sys_utils.fexit()

        node_dict = etree_utils.convert_to_cidict(self.root)

        # Validate only pickers keys exist.
        if not set(node_dict.keys()).issubset({'modules', 'functions'}):
            display_err_and_exit(">>rules<< element can contain only >>modules<< and/or >>functions<< elements. Check group: {}.".format(self.gname))
        elif not node_dict:
            display_err_and_exit(">>rules<< element is empty.Check group: {}.".format(self.gname))

        # xyz -- boolean built-in property or flags
        pattern_1 = re.compile(r"^\s*(?P<object>\w+)\s*$",re.IGNORECASE)
        # tagged abc[,.....]
        pattern_2 = re.compile(r"^\s*tagged\s*(?P<object>(.+?))\s*$",re.IGNORECASE)
        # tags/bugs a[,....] are defined
        pattern_3 = re.compile(r"^\s*(?P<container>\w+)\s*(?P<object>.*?)\s+(?P<condition>are)\s+(?P<expression>defined|present)\s*$", re.IGNORECASE)
        # prop is DEFINED
        pattern_4 = re.compile(r"^\s*(?P<object>\w+)\s+(?P<condition>is)\s+(?P<expression>defined|present)\s*$", re.IGNORECASE)
        # xyz condition def
        condition_str = "is|eq|=|==|lt|le|gt|ge|matches|~=|contains|\*="
        p5_raw = r"^\s*(?P<object>\w+)\s+(?P<condition>({}){{1,1}})\s+(?P<expression>.*?)\s*$".format(condition_str)
        pattern_5 = re.compile(p5_raw, re.IGNORECASE)
        # property_type xyz condition def
        condition_str = "is|eq|=|==|lt|le|gt|ge|matches|~=|contains|\*="
        p6_raw = r"^\s*(?P<container>prop|evar|tag|bug)\s*(?P<object>\w+)\s+(?P<condition>({}){{1,1}})\s+(?P<expression>.*?)\s*$".format(condition_str)
        pattern_6 = re.compile(p6_raw, re.IGNORECASE)

        for target_object in list(self.root):
            tobject = target_object.tag.lower() == 'modules' and 'Module' or 'Function'
            for rule in list(target_object):
                if rule.tag not in {'include', 'exclude'}:
                    display_err_and_exit(
                        ">>{}<< element in >>rules<< element can contain only rules with >>include<< and/or >>exclude<< tags. Check group: {}.".format(
                            target_object.tag,
                            self.gname)
                    )
                run_conf_utils.validate_rule_xml_child("groups", self.gname, self.fpath, rule)
                rule_dict = etree_utils.convert_attribs_to_cidict(rule)
                try:
                    match = pattern_1.match(rule_dict['if'])
                    if match:
                        self.__create_1_word_boolean_rule(rule, tobject, rule.tag, match)
                        continue

                    match = pattern_2.match(rule_dict['if'])
                    if match:
                        self.__create_2_word_value_rule_for_tags(rule, tobject, rule.tag, match)
                        continue

                    match = pattern_3.match(rule_dict['if'])
                    if match:
                        self.__create_4_word_value_rule_for_multi_defined(rule, tobject, rule.tag, match)
                        continue

                    match = pattern_4.match(rule_dict['if'])
                    if match:
                        self.__create_3_word_value_rule_for_prop(rule, tobject, rule.tag, match)
                        continue

                    match = pattern_5.match(rule_dict['if'])
                    if match:
                        self.__create_3_word_value_rule_for_prop(rule, tobject, rule.tag, match)
                        continue

                    match = pattern_6.match(rule_dict['if'])
                    if match:
                        self.__create_4_word_rule_for_container(rule, tobject, rule.tag, match)
                        continue

                    # Invalid rule
                    raise Exception("The >>if<< condition content in the rule is invalid: " + rule_dict['if'])

                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    display_err_and_exit(
                        "Exception in processing rule: {}. {}. Check group: {}.".format(ETree.tostring(rule).strip(),e, self.gname))

    def evaluate(self, test_object):
        for rule in self.__rules:
            rule.evaluate(test_object)