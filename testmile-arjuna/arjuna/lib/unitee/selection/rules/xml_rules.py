import xml.etree.ElementTree as ETree
import re

from arjuna.lib.unitee.enums import *
from arjuna.lib.core.utils import sys_utils
from arjuna.lib.core.utils import etree_utils
from arjuna.lib.unitee.utils import run_conf_utils

from .builder import RuleBuilder

class XmlRules:

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

        # Validate only pickers keys exist.
        if not set(node_dict.keys()).issubset({'modules', 'functions'}):
            display_err_and_exit(">>rules<< element can contain only >>modules<< and/or >>functions<< elements. Check group: {}.".format(self.gname))
        elif not node_dict:
            display_err_and_exit(">>rules<< element is empty.Check group: {}.".format(self.gname))

        # xyz condition def
        pattern_1 = re.compile(r"^\s*(?P<object>\w+)\s+(?P<condition>(is|=|==|matches|~=|contains|\*=){1,1})\s+(?P<expression>.*?)\s*$", re.IGNORECASE)
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
                    rule_builder = RuleBuilder()
                    match_1 = pattern_1.match(rule_dict['if'])
                    if match_1:
                        print(match_1.groups())
                        rule_builder.test_object_type(tobject)
                        rule_builder.rule_type(rule.tag)

                        robject = match_1.group('object')
                        condition = match_1.group('condition')
                        expression = match_1.group('expression')

                        if not robject:
                            raise Exception("Target Rule Object not defined.")
                        if not condition:
                            raise Exception("Target condition not defined.")
                        if not expression:
                            raise Exception("Target expression not defined.")

                        rule_builder.rule_object(robject.upper())
                        rule_builder.condition(condition.upper())
                        rule_builder.expression(expression)
                    else:
                        raise Exception("The >>if<< condition content in the rule is invalid: " + rule_dict['if'])
                    self.__rules.append(rule_builder.build())
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    display_err_and_exit(
                        "Exception in processing rule: {}. {}. Check group: {}.".format(ETree.tostring(rule),e, self.gname))

    def evaluate(self, test_object):
        for rule in self.__rules:
            rule.evaluate(test_object)