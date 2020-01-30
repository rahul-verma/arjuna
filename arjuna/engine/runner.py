'''
This file is a part of Arjuna
Copyright 2015-2020 Rahul Verma

Website: www.RahulVerma.net

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

import os
import pytest

from arjuna.core.enums import ReportFormat

class TestRunner:
    import sys
    import os
    import unittest
    
    def __init__(self):
        from arjuna import Arjuna
        from arjuna.core.enums import ArjunaOption
        self.__project_dir = Arjuna.get_ref_config().get_arjuna_option_value(ArjunaOption.PROJECT_ROOT_DIR).as_str()
        self.__tests_dir = Arjuna.get_ref_config().get_arjuna_option_value(ArjunaOption.PROJECT_TESTS_DIR).as_str()
        self.__xml_path = os.path.join(Arjuna.get_ref_config().get_arjuna_option_value(ArjunaOption.PROJECT_RUN_REPORT_XML_DIR).as_str(), "report.xml")
        self.__html_path = os.path.join(Arjuna.get_ref_config().get_arjuna_option_value(ArjunaOption.PROJECT_RUN_REPORT_HTML_DIR).as_str(), "report.html")
        self.__report_formats = Arjuna.get_ref_config().get_arjuna_option_value(ArjunaOption.PROJECT_REPORT_FORMATS).as_enum_list(ReportFormat)
        self.__pytest_args = ["--rootdir", self.__project_dir, "--no-print-logs"]

    @property
    def tests_dir(self):
        return self.__tests_dir

    @property
    def test_suite(self):
        return self.__suite
    
    def load_all_tests(self):
        self.__pytest_args.insert(0, self.tests_dir)
    
    def run(self):
        from arjuna import Arjuna
        from arjuna.core.enums import ArjunaOption

        pytest_report_args = []

        if ReportFormat.XML in self.__report_formats:
            pytest_report_args.extend(["--junit-xml", self.__xml_path])

        if ReportFormat.HTML in self.__report_formats:
            pytest_report_args.extend(["--html", self.__html_path, "--self-contained-html"])

        self.__pytest_args.extend(pytest_report_args)

        print("Executing pytest with args: {}".format(self.__pytest_args))
        pytest.main(self.__pytest_args)
