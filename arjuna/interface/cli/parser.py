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
from arjuna.core.constant import ReportFormat


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
        self.parser.add_argument('-o', '--output-format', dest="report.formats", type=report_format, action="append", choices=[i for i in ReportFormat.__members__], help='Output/Report format. Can pass any number of these switches.') # choices=['XML', 'HTML'], 
        self.parser.add_argument('--update', dest="static.rid", action='store_true', help = 'Will result in overwriting of report files. Useful during script development.')
        self.parser.add_argument('--dry-run', dest="dry_run", choices=[i for i in DryRunType.__members__], type=dry_run_type, help='Does a dry run. Tests are not executed. Behavior depends on the type passed as argument. SHOW_TESTS - enumerate tests. SHOW_PLAN - enumerates tests and fixtures. RUN_FIXTURES - Executes setup/teardown fixtures and emuerates tests.')
        self.parser.add_argument('-c', '--ref-conf', dest="ref_conf", metavar="config_name", type=str, help="Reference Configuration object name for this run. Default is 'ref'")
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
        self.parser.add_argument('-dl', '--display-level', dest='log.console.level', type=ustr, choices=[i for i in LoggingLevel.__members__],
                                 help="Minimum message level for display. (choose from 'DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL')", default=LoggingLevel.INFO.name)
        self.parser.add_argument('-ll', '--log-level', dest='log.file.level', type=ustr, choices=[i for i in LoggingLevel.__members__],
                                 help="Minimum message level for log file. (choose from 'DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL')", default=LoggingLevel.DEBUG.name)

    def process(self, arg_dict):
        pass

class RunDefaultGroupParser(Parser):
    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(add_help=False)

    def process(self, arg_dict):
        pass

class SessionParser(Parser):
    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(add_help=False)
        self.parser.add_argument("-s", "--session-name", dest="run.session.name", metavar="session_def_name", type=partial(lname_check, "Session Name"), help = 'Name of a defined session in test sessions configuration file in <Project Root>/config/sessions.yaml file.')

    def process(self, arg_dict):
        if arg_dict['run.session.name'] is None:
            print("Fatal Error in CLI processing. You must provide a valid session name using -s or --session-name switch", file=sys.stderr)
            sys.exit(1)

class StageParser(Parser):
    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(add_help=False)
        self.parser.add_argument("-s", "--stage-name", dest="stage_name", metavar="stage_name", type=partial(lname_check, "Stage Name"), help = 'Name of a defined stage in test stages configuration file in <Project Root>/config/stages.yaml file.')

    def process(self, arg_dict):
        if arg_dict['stage_name'] is None:
            print("Fatal Error in CLI processing. You must provide a valid test stage name using -s or --stage-name switch", file=sys.stderr)
            sys.exit(1)

class GroupParser(Parser):
    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(add_help=False)
        self.parser.add_argument("-g", "--group-name", dest="group_name", metavar="group_name", type=partial(lname_check, "Group Name"), help = 'Name of a defined group in test groups configuration file in <Project Root>/config/groups.yaml file.')

    def process(self, arg_dict):
        if arg_dict['group_name'] is None:
            print("Fatal Error in CLI processing. You must provide a valid test group name using -g or --group-name switch", file=sys.stderr)
            sys.exit(1)

class PickersParser(Parser):
    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(add_help=False)
        self.parser.add_argument('-ip', '--include-package', dest="ip", action="append", metavar="package_name_or_regex", default=None, help='Name/regex pattern for including test packages. Can pass any number of these switches.')
        self.parser.add_argument('-ep', '--exclude-package', dest="ep", action="append", metavar="package_name_or_regex", default=None, help='Name/regex pattern for excluding test packages. Can pass any number of these switches.')
        self.parser.add_argument('-im', '--include-module', dest="im", action="append", metavar="module_name_or_regex", default=None, help='Name/regex pattern for including test modules. Can pass any number of these switches.')
        self.parser.add_argument('-em', '--exclude-module', dest="em", action="append", metavar="module_name_or_regex", default=None, help='Name/regex pattern for excluding test modules. Can pass any number of these switches.')
        self.parser.add_argument('-it', '--include-test', dest="it", action="append", metavar="test_name_or_regex", default=None, help='Name/regex pattern for including test functions. Can pass any number of these switches.')
        self.parser.add_argument('-et', '--exclude-test', dest="et", action="append", metavar="test_name_or_regex", default=None, help='Name/regex pattern for excluding test functions. Can pass any number of these switches.')

        self.parser.add_argument('-ir', '--include-rule', dest="ir", action="append", metavar="rule", default=None, help='Include test functions that match the rule. Can pass any number of these switches. Test Function is included if any of the inclusion rules matches.')
        self.parser.add_argument('-er', '--exclude-rule', dest="er", action="append", metavar="rule", default=None, help='Exclude test functions that match the rule. Can pass any number of these switches. Test Function is excluded if any of the exclusion rules matches. Evaluated before any inclusion rules.')

    def process(self, arg_dict):
        pass