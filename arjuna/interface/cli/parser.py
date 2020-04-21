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

import sys
import os
import argparse
from functools import partial

from .validation import *
from arjuna.core.enums import ReportFormat


class Parser:

    def __init__(self):
        self.parser = None

    def get_parser(self):
        return self.parser

class ProjectParser(Parser):

    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(add_help=False)
        self.parser.add_argument('-p', '--project-root-dir', metavar="test_project_root_dir", dest="project.root.dir", type=project_dir, help = 'Valid absolute path of an existing Arjuna test project. Needed with python -m arjuna call only. With python arjuna_launcher.py you can skip this argument as the script determines its container Arjuna test project automatically.')

    def process(self, arg_dict):
        if arg_dict['project.root.dir'] is None:
            print("Fatal Error in CLI processing. You must provide a valid project root directory using -p or --project-dir switch", file=sys.stderr)
            sys.exit(1)


class NewProjectParser(Parser):
    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(add_help=False)
        self.parser.add_argument('-p', '--project-root-dir', metavar="test_project_root_dir", dest="project.root.dir", type=new_project_dir, help = 'Absolute non-existing Project root directory. Last part of directory represents project name. Name of project should be an Alnum 3-30 length with only lower case letters.')

    def process(self, arg_dict):
        if arg_dict['project.root.dir'] is None:
            print("Fatal Error in CLI processing. You must provide a valid project root directory using -p or --project-dir switch", file=sys.stderr)
            sys.exit(1)

class RunParser(Parser):
    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(add_help=False)
        self.parser.add_argument("-r", "--run-id", dest="run.id", metavar="run_id", type=partial(lname_check, "Run ID"), help = 'Alnum 3-30 length. Only lower case letters.', default="mrun")
        self.parser.add_argument('-o', '--output-formats', dest="report.formats", type=report_format, metavar=('F1','F2'), default=['XML', 'HTML'], nargs='+', help='One or more report format names.') # choices=['XML', 'HTML'], 
        self.parser.add_argument('--update', dest="static.rid", action='store_true', help = 'Will result in overwriting of report files. Useful during script development.')
        self.parser.add_argument('--dry-run', dest="dry_run", metavar="dry_run_type", type=dry_run_type, help='Does a dry run. Tests are not executed. Behavior depends on the type passed as argument. SHOW_TESTS - enumerate tests. SHOW_PLAN - enumerates tests and fixtures. RUN_FIXTURES - Executes setup/teardown fixtures and emuerates tests.')
        self.parser.add_argument('-ao', '--arjuna-option', dest="ao",
                                 nargs=2,
                                 action='append',
                                 metavar=('option', 'value'),
                                 help='Arjuna Option. Can pass any number of these switches.')
        self.parser.add_argument('-uo', '--user-option', dest="uo",
                                 nargs=2,
                                 action='append',
                                 metavar=('option', 'value'),
                                 help='User Option. Can pass any number of these switches.')
    def process(self, arg_dict):
        pass

class RunDefaultGroupParser(Parser):
    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(add_help=False)
        self.parser.add_argument('-c', '--conf', dest="group.conf.name", metavar="config_name", type=str, default="ref", help='Configuration object name for this run.')

    def process(self, arg_dict):
        pass

class SessionParser(Parser):
    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(add_help=False)
        self.parser.add_argument("-s", "--session-name", dest="run.session.name", metavar="session_def_name", type=partial(lname_check, "Run ID"), help = 'Name of session configuration file. Corresponding <sessionname>.yaml file must exist in <Project Root>/config/session directory')

    def process(self, arg_dict):
        if arg_dict['run.session.name'] is None:
            print("Fatal Error in CLI processing. You must provide a valid session name using -s or --session-name switch", file=sys.stderr)
            sys.exit(1)

class PickersParser(Parser):
    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(add_help=False)
        self.parser.add_argument('-im', '--include-modules', dest="imodules", metavar=('M1','M2'), default=None, nargs='+', help='One or more names/patterns for including test modules.')
        self.parser.add_argument('-em', '--exclude-modules-in-stage', dest="emodules", metavar=('M1','M2'), default=None, nargs='+', help='One or more names/patterns for excluding test modules.')
        # self.parser.add_argument('-cc', '--cclasses', dest="cclasses", metavar=('C1','C2'), default=None, nargs='+', help='One or more names/patterns for considering test classes.')
        # self.parser.add_argument('-ic', '--iclasses', dest="iclasses", metavar=('C1','C2'), default=None, nargs='+', help='One or more names/patterns for ignoring test classes.')
        self.parser.add_argument('-it', '--include-tests', dest="itests", metavar=('F1','F2'), default=None, nargs='+', help='One or more names/patterns for including test functions.')
        self.parser.add_argument('-et', '--exclude-tests', dest="etests", metavar=('F1','F2'), default=None, nargs='+', help='One or more names/patterns for excluding test functions.')

    def process(self, arg_dict):
        pass