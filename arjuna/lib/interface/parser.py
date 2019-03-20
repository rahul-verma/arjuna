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

import sys
import argparse
from functools import partial

from arjuna.lib.unitee.enums import *

from .validation import *

class Parser:

    def __init__(self):
        self.parser = None

    def get_parser(self):
        return self.parser


class SetuParser(Parser):
    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(add_help=False)
        self.parser.add_argument('-p', '--port', dest="setu_port", default=9000, type=port, help='Setu network port')

    def process(self, arg_dict):
        arg_dict['setu.port'] = arg_dict['setu_port']
        del arg_dict['setu_port']


class ProjectParser(Parser):
    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(add_help=False)
        self.parser.add_argument('-w', '--workspace-dir', dest="workspace_dir", type=str, help='Workspace Directory')
        self.parser.add_argument('-p', '--project-name', dest="project_name", type=partial(lname_check, "Project"), help = 'Name of project (Alnum 3-30 length. Only lower case letters.).')

    def process(self, arg_dict):
        arg_dict['workspace.dir'] = arg_dict['workspace_dir']
        del arg_dict['workspace_dir']
        if arg_dict['project_name'] is None:
            print("Fatal Error in CLI processing. You must provide a valid project name using -p or --project-name switch", file=sys.stderr)
            sys.exit(1)
        arg_dict['project.name'] = arg_dict['project_name']

        del arg_dict['project_name']

class RunParser(Parser):
    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(add_help=False)
        self.parser.add_argument("-rid", "--runid", nargs=1, dest="runid", type=partial(lname_check, "Run ID"), help = 'Alnum 3-30 length. Only lower case letters.')
        self.parser.add_argument('-ar', '--active-reporters', dest="active.reporters",
                                 metavar=('R1','R2'), nargs='+',
                                 type=ustr,
                                 choices=[i for i in ActiveReporterNames.__members__],
                                 help='One or more valid active state names: ' + str([i for i in ActiveReporterNames.__members__]))
        self.parser.add_argument('-dr', '--deferred-reporters', dest="deferred.reporters",
                                 metavar=('R1','R2'), nargs='+',
                                 type=ustr,
                                 choices=[i for i in DeferredReporterNames.__members__],
                                 help='One or more valid deferred state names: ' + str([i for i in DeferredReporterNames.__members__]))

    def process(self, arg_dict):
        pass

class SessionParser(Parser):
    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(add_help=False)
        self.parser.add_argument('-s', '--session-name', dest="session_name", type=partial(lname_check, "Session"), help='Existing session template name.')

    def process(self, arg_dict):
        if arg_dict['session_name'] is None:
            print("Fatal Error in CLI processing. You must provide a valid session name using -s or --session-name switch", file=sys.stderr)
            sys.exit(1)
        arg_dict['session.name'] = arg_dict['session_name']
        del arg_dict['session_name']

class GroupParser(Parser):
    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(add_help=False)
        self.parser.add_argument('-g', '--group-name', dest="group_name", type=partial(lname_check, "Group"), help='Existing group template name.')

    def process(self, arg_dict):
        arg_dict['group.name'] = arg_dict['group_name']
        del arg_dict['group_name']

class NamesParser(Parser):
    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(add_help=False)
        self.parser.add_argument('-cm', '--cmodules', dest="cmodules", metavar=('M1','M2'), default=None, nargs='+', help='One or more names/patterns for considering test modules.')
        self.parser.add_argument('-im', '--imodules', dest="imodules", metavar=('M1','M2'), default=None, nargs='+',
                         help='One or more names/patterns for ignoring test modules.')
        self.parser.add_argument('-cf', '--cfunctions', dest="cfunctions", metavar=('F1','F2'), default=None, nargs='+', help='One or more names/patterns for considering test functions.')
        self.parser.add_argument('-if', '--ifunctions', dest="ifunctions", metavar=('F1','F2'), default=None, nargs='+',
                         help='One or more names/patterns for ignoring test functions.')

    def process(self, arg_dict):
        pass