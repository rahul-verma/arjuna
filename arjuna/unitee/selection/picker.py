import re
import xml.etree.ElementTree as ETree

from arjuna.tpi.enums import ArjunaOption
from arjuna.unitee.types.containers import *
from arjuna.unitee.enums import *
from arjuna.lib.utils import etree_utils
from arjuna.lib.utils import sys_utils
from arjuna.unitee.utils import run_conf_utils

class NameMatcher:

    def __init__(self, consider_names, ignore_names):
        self.__consider_names = consider_names
        self.__ignore_names = ignore_names

        # Ignore overrides consider
        for name in self.__ignore_names:
            if name in self.__consider_names:
                self.__consider_names.remove(name)

    def matches(self, name):
        if self.__consider_names:
            consider = False
            for reg in self.__consider_names:
                if reg.match(name):
                    consider = True
            return consider

        if self.__ignore_names:
            consider = True
            for reg in self.__ignore_names:
                if reg.match(name):
                    consider = False
            return consider

        return True


class Picker:

    def __init__(self, fpath, gname, pickers_node):
        self.gname = gname
        self.fpath = fpath
        self.root = pickers_node

        # Although using a set would give better performance, using a list so that pickers are evaluated
        # in the order they are specified.
        self._rule_dict = CIStringDict(
            {
                'cm': [],
                'im': [],
                'cf': [],
                'if': []
            }
        )

        self.__module_matcher = None
        self.__function_matcher = None

        from arjuna.tpi import Arjuna
        self.console = Arjuna.get_console()
        self.tm_prefix = Arjuna.get_central_config().get_arjuna_option_value(ArjunaOption.UNITEE_PROJECT_TEST_MODULE_IMPORT_PREFIX).as_string()
        self.__process()

    def __process(self):
        def display_err_and_exit(msg):
            self.console.display_error((msg + " Fix groups template file: {}").format(self.fpath))
            sys_utils.fexit()

        node_dict = etree_utils.convert_to_cidict(self.root)
        pattern_set = {i.lower() for i in self._rule_dict.keys()}

        # Validate only pickers keys exist.
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
                    ">>pickers<< element type attribute can only contain one of {}.Check group: {}".format(
                        pattern_set,
                        self.gname))
            pattern_value = pattern_dict['pattern'].strip()
            if not pattern_value:
                display_err_and_exit(
                    ">>pickers<< element's >>pattern<< attribute can not be empty.Check group: {}".format(
                        pattern_set,
                        self.gname))

            if pattern_name in {'cm', 'im'}:
                self._rule_dict[pattern_name].append(re.compile(self.tm_prefix + pattern_value))
            else:
                self._rule_dict[pattern_name].append(re.compile(pattern_value))

        self.__module_matcher = NameMatcher(self._rule_dict['cm'], self._rule_dict['im'])
        self.__function_matcher = NameMatcher(self._rule_dict['cf'], self._rule_dict['if'])


    def include_module(self, mname):
        return self.__module_matcher.matches(mname)


    def include_func(self, fname):
        return self.__function_matcher.matches(fname)