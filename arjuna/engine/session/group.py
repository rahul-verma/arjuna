# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import pytest

from arjuna.core.error import TestGroupsFinished
from arjuna.core.constant import *
from arjuna.tpi.constant import *


class TestGroup:

    def __init__(self, *, name, config, session, stage, rules=None):
        self.__name = name
        self.__session = session
        self.__stage = stage
        self.__config = config
        self.__thname = None
        self.__dry_run = session.dry_run
        self.__rules = rules
        self.__css_path = config.value(ArjunaOption.ARJUNA_ROOT_DIR) + "/arjuna/res/arjuna.css" 

    @classmethod
    def create_rule_strs(cls, include_exclude_dict):
        pickers_rulestr = {
            'ip': "package *= {}",
            'ep': "package *= {}",
            'im': "module *= {}",
            'em': "module *= {}",
            'it': "name *= {}",
            'et': "name *= {}",
        }

        rules = {'ir': [], 'er': []}

        for picker in pickers_rulestr:
            names = include_exclude_dict.pop(picker)
            if names:
                for name in names:
                    if picker.startswith('i'):
                        rules['ir'].append(pickers_rulestr[picker].format(name))
                    else:
                        rules['er'].append(pickers_rulestr[picker].format(name))
        return rules

    @property
    def config(self):
        return self.__config

    @property
    def thread_name(self):
        return self.__thname

    @thread_name.setter
    def thread_name(self, name):
        self.__thname = name

    @property
    def tests_dir(self):
        return self.__tests_dir

    def run(self):
        from arjuna import Arjuna
        from arjuna.tpi.constant import ArjunaOption
        Arjuna.register_group_params(name=self.__name, config=self.__config, thread_name=self.thread_name)
        self.__load_command_line()

        os.chdir(self.__project_dir)
        print("Executing pytest with args: {}".format(" ".join(self.__pytest_args)))


        pytest_retcode = pytest.main(self.__pytest_args)
        return pytest_retcode

    def __load_command_line(self):
        from arjuna import Arjuna
        from arjuna.tpi.constant import ArjunaOption
        self.__project_dir = self.config.value(ArjunaOption.PROJECT_ROOT_DIR)
        # import sys
        # sys.path.insert(0, self.__project_dir + "/..")
        self.__tests_dir = self.config.value(ArjunaOption.TESTS_DIR)
        suffix = ""
        if self.__name != "mgroup":
            suffix = "-" + self.__session.name + "-" + self.__stage.name + "-" + self.__name
        self.__xml_path = os.path.join(self.config.value(ArjunaOption.REPORT_XML_DIR), "report{}.xml".format(suffix))
        self.__html_path = os.path.join(self.config.value(ArjunaOption.REPORT_HTML_DIR), "report{}.html".format(suffix))
        self.__report_formats = self.config.value(ArjunaOption.REPORT_FORMATS)
        # self.__report_formats = Value.as_enum_list(rfmts, ReportFormat)
        res_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../res"))
        pytest_ini_path = res_path + "/pytest.ini"

        # -s is to print to console.
        self.__pytest_args = ["-c", pytest_ini_path, "--rootdir", self.__project_dir, "--no-print-logs", "--show-capture", "all", "--disable-warnings", "-rxX", "--css", self.__css_path] # 
        self.__test_args = []
        self.__load_tests(rules=self.__rules)
        self.__load_meta_args()

    def __load_tests(self, *, rules):
        from arjuna import Arjuna
        from arjuna.engine.selection.selector import Selector
        selector = Selector()
        if rules:
            for rule in rules['ir']:
                selector.include(rule)
            for rule in rules['er']:
                selector.exclude(rule)
            

        Arjuna.register_test_selector_for_group(selector)

    def __load_meta_args(self):
        pytest_report_args = []

        if ReportFormat.XML in self.__report_formats:
            pytest_report_args.extend(["--junit-xml", self.__xml_path])

        if ReportFormat.HTML in self.__report_formats:
            pytest_report_args.extend(["--html", self.__html_path, "--self-contained-html"])

        self.__pytest_args.extend(pytest_report_args)
        self.__pytest_args.extend(self.__test_args)

        if self.__dry_run not in {False, None}:
            print("!!!!!! This is a DRY RUN !!!!!!!")
            if self.__dry_run == DryRunType.SHOW_TESTS:
                print("Dry Run Type: SHOW TESTS")
                print("You can see the test functions which will be executed as per settings of your command.")
                self.__pytest_args.extend(["--collect-only"])
            elif self.__dry_run == DryRunType.SHOW_PLAN:
                print("Dry Run Type: SHOW PLAN")
                print("You can see the test functions as well as the fixtures which will be executed as per settings of your command.")
                self.__pytest_args.extend(["--setup-plan"])
            elif self.__dry_run == DryRunType.CREATE_RES:
                print("Dry Run Type: CREATE RESOURCES")
                print("All resources will be created as per your current command. You can see the test functions which will be executed as per settings of your command.")
                self.__pytest_args.extend(["--setup-only"])

    def __str__(self):
        return "TestGroup: name:{}, config={}, rules={}".format(self.__name, self.config.name, self.__rules)


class YamlTestGroup(TestGroup):

    def __init__(self, *, name, group_yaml, session, stage):
        self.__config = stage.config
        self.__rules = {'ir': [], 'er': []}
        self.__process_yaml(group_yaml)
        super().__init__(name=name, config=self.__config, session=session, stage=stage, rules=self.__rules)

    def __process_yaml(self, group_yaml):
        from arjuna import Arjuna
        for gmd_name in group_yaml.section_names:
            pickers = {
                'ip': None,
                'ep': None,
                'im': None,
                'em': None,
                'it': None,
                'et': None,
            }
            gmd_name = gmd_name.lower()
            if gmd_name == "conf":
                self.__config = Arjuna.get_config(group_yaml["conf"])
            elif gmd_name in pickers:
                pickers[gmd_name] = group_yaml[gmd_name]
                if gmd_name.startswith('i'):
                    self.__rules['ir'].extend(TestGroup.create_rule_strs(pickers)['ir'])
                else:
                    self.__rules['er'].extend(TestGroup.create_rule_strs(pickers)['er'])
            elif gmd_name in {'ir', 'er'}:
                self.__rules[gmd_name].extend(group_yaml[gmd_name])


class MagicTestGroup(TestGroup):

    def __init__(self, *, session, stage, rules=None):
        super().__init__(name="mgroup", config=stage.config, session=session, stage=stage, rules=rules)


class TestGroups:

    def __init__(self):
        self.__names = []
        self.__iter = None

    def add_group(self, group):
        self.__names.append(group)

    def freeze(self):
        self.__iter = iter(self.__names)

    def __iter__(self):
        return self

    def next(self):
        try:
            return next(self.__iter)
        except StopIteration:
            raise TestGroupsFinished()

    def __str__(self):
        return str([str(c) for c in self.__names])