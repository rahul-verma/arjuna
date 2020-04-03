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
from arjuna.tpi.enums import ReportFormat


class Parser:

    def __init__(self):
        self.parser = None

    def get_parser(self):
        return self.parser

class ProjectParser(Parser):

    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(add_help=False)
        #self.parser.add_argument('-w', '--workspace-dir', dest="workspace_dir", type=str, help='Workspace Directory')
        self.parser.add_argument('-p', '--project-root-dir', dest="project.root.dir", type=project_dir, help = 'Valid absolute Project root directory. Name of project (Alnum 3-30 length. Only lower case letters.).')

    def process(self, arg_dict):
        # arg_dict['workspace.dir'] = arg_dict['workspace_dir']
        # del arg_dict['workspace_dir']
        if arg_dict['project.root.dir'] is None:
            print("Fatal Error in CLI processing. You must provide a valid project root directory using -p or --project-dir switch", file=sys.stderr)
            sys.exit(1)


class NewProjectParser(Parser):
    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(add_help=False)
        #self.parser.add_argument('-w', '--workspace-dir', dest="workspace_dir", type=str, help='Workspace Directory')
        self.parser.add_argument('-p', '--project-root-dir', dest="project.root.dir", type=new_project_dir, help = 'Absolute non-existing Project root directory. Name of project (Alnum 3-30 length. Only lower case letters.).')

    def process(self, arg_dict):
        # arg_dict['workspace.dir'] = arg_dict['workspace_dir']
        # del arg_dict['workspace_dir']
        if arg_dict['project.root.dir'] is None:
            print("Fatal Error in CLI processing. You must provide a valid project root directory using -p or --project-dir switch", file=sys.stderr)
            sys.exit(1)


class RunParser(Parser):
    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(add_help=False)
        self.parser.add_argument("-rid", "--runid", dest="run.id", type=partial(lname_check, "Run ID"), help = 'Alnum 3-30 length. Only lower case letters.', default="mrun")
        self.parser.add_argument('--static-rid', dest="static.rid", action='store_true', help = 'Use static RunID. Will result in overwriting of report files. Useful during script development.')
        self.parser.add_argument('-rf', '--report-formats', dest="report.formats", type=report_format, metavar=('F1','F2'), default=['XML', 'HTML'], nargs='+', help='One or more report format names.') # choices=['XML', 'HTML'], 
        self.parser.add_argument('--dry-run', dest="dry_run", action='store_true', help = 'Launch Arjuna, enumerate tests, but do not execute tests.')
        self.parser.add_argument('--run-env', dest="run.env.name", type=str, default="not_set", help = 'Name of environment with its options defined in <env>.conf file in <Project Root>/config/env directory.')
        self.parser.add_argument('--run-conf', dest="run_conf", type=str, default=None, help = 'Absolute path of a conf file to be used for this run.')
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

class PickersParser(Parser):
    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(add_help=False)
        self.parser.add_argument('-im', '--include-modules', dest="imodules", metavar=('M1','M2'), default=None, nargs='+', help='One or more names/patterns for including test modules.')
        self.parser.add_argument('-em', '--exclude-modules', dest="emodules", metavar=('M1','M2'), default=None, nargs='+', help='One or more names/patterns for excluding test modules.')
        # self.parser.add_argument('-cc', '--cclasses', dest="cclasses", metavar=('C1','C2'), default=None, nargs='+', help='One or more names/patterns for considering test classes.')
        # self.parser.add_argument('-ic', '--iclasses', dest="iclasses", metavar=('C1','C2'), default=None, nargs='+', help='One or more names/patterns for ignoring test classes.')
        self.parser.add_argument('-it', '--include-tests', dest="itests", metavar=('F1','F2'), default=None, nargs='+', help='One or more names/patterns for including test functions.')
        self.parser.add_argument('-et', '--exclude-tests', dest="etests", metavar=('F1','F2'), default=None, nargs='+', help='One or more names/patterns for excluding test functions.')

    def process(self, arg_dict):
        pass