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
import sys

from arjuna.tpi.enums import ReportFormat
from arjuna.core.value import Value

class TestRunner:
    import sys
    import os
    import unittest
    
    def __init__(self):
        from arjuna import Arjuna
        from arjuna.tpi.enums import ArjunaOption
        self.__project_dir = Arjuna.get_config().value(ArjunaOption.PROJECT_ROOT_DIR)
        # import sys
        # sys.path.insert(0, self.__project_dir + "/..")
        self.__tests_dir = Arjuna.get_config().value(ArjunaOption.TESTS_DIR)
        self.__xml_path = os.path.join(Arjuna.get_config().value(ArjunaOption.REPORT_XML_DIR), "report.xml")
        self.__html_path = os.path.join(Arjuna.get_config().value(ArjunaOption.REPORT_HTML_DIR), "report.html")
        self.__report_formats = Arjuna.get_config().value(ArjunaOption.REPORT_FORMATS)
        # self.__report_formats = Value.as_enum_list(rfmts, ReportFormat)
        res_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../res"))
        pytest_ini_path = res_path + "/pytest.ini"

        # -s is to print to console.
        self.__pytest_args = ["-c", pytest_ini_path, "--rootdir", self.__project_dir, "--no-print-logs", "-s"]
        self.__test_args = []

    @property
    def tests_dir(self):
        return self.__tests_dir

    @property
    def test_suite(self):
        return self.__suite
    
    def load_all_tests(self):
        self.__pytest_args.insert(0, self.tests_dir)

    def load_tests_from_pickers(self, *, im=None, em=None, it=None, et=None):  

        def process_modules(ms):
            ms = [m.replace(".py", "").replace("*","").replace("/", " and ").replace("\\", " and ") for m in ms]
            return ["and" in m and "({})".format(m) or m for m in ms]

        k_args = []

        k_flag = False

        if em:            
            em = process_modules(em)
            k_args.append(" and ".join(["not " + m for m in em]))
            k_flag = True

        # if ic:
        #     prefix = k_flag and " and " or ""
        #     k_args.append(prefix + " and ".join(["not " + c for c in ic]))
        #     k_flag = True

        if et:
            prefix = k_flag and " and " or ""
            k_args.append(prefix + " and ".join(["not " + c for c in et]))
            k_flag = True

        if im:
            prefix = k_flag and " and " or ""            
            cm = process_modules(im)
            k_args.append(prefix + " or ".join(im))
            k_flag = True

        # if cc:
        #     prefix = k_flag and " and " or "" 
        #     k_args.append(prefix + " or ".join(cc))
        #     k_flag = True

        if it:
            prefix = k_flag and " and " or "" 
            k_args.append(prefix + " or ".join(it))
            k_flag = True

        if k_flag:
            self.__test_args.append("-k " + "".join(k_args))
        
  
    def run(self, *, dry_run):
        from arjuna import Arjuna
        from arjuna.tpi.enums import ArjunaOption

        pytest_report_args = []

        if ReportFormat.XML in self.__report_formats:
            pytest_report_args.extend(["--junit-xml", self.__xml_path])

        if ReportFormat.HTML in self.__report_formats:
            pytest_report_args.extend(["--html", self.__html_path, "--self-contained-html"])

        self.__pytest_args.extend(pytest_report_args)
        self.__pytest_args.extend(self.__test_args)

        if dry_run:
            self.__pytest_args.append("--collect-only")

        os.chdir(self.__project_dir)
        print("Executing pytest with args: {}".format(" ".join(self.__pytest_args)))


        pytest_retcode = pytest.main(self.__pytest_args)
        import sys
        sys.exit(pytest_retcode)
