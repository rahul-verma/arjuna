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
import os
import argparse
from functools import partial

from arjuna.unitee.enums import *

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
        self.parser.add_argument('-p', '--port', dest="setu.port", default=9000, type=port, help='Setu network port')

    def process(self, arg_dict):
        pass


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
        self.parser.add_argument('--non-unitee', dest="project.is_not_unitee", action="store_true", help = 'Pass this switch for creating a non-UniTEE project.')

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
        self.parser.add_argument("-rid", "--runid", nargs=1, dest="runid", type=partial(lname_check, "Run ID"), help = 'Alnum 3-30 length. Only lower case letters.')
        self.parser.add_argument('-ar', '--active-reporters', dest="unitee.project.active.reporters",
                                 metavar=('R1','R2'), nargs='+',
                                 type=ustr,
                                 choices=[i for i in ActiveReporterNames.__members__],
                                 help='One or more valid active state names: ' + str([i for i in ActiveReporterNames.__members__]))
        self.parser.add_argument('-dr', '--deferred-reporters', dest="unitee.project.deferred.reporters",
                                 metavar=('R1','R2'), nargs='+',
                                 type=ustr,
                                 choices=[i for i in DeferredReporterNames.__members__],
                                 help='One or more valid deferred state names: ' + str([i for i in DeferredReporterNames.__members__]))

        self.parser.add_argument('-aco', '--arjuna-central-option', dest="aco",
                                 nargs=2,
                                 action='append',
                                 metavar=('option', 'value'),
                                 help='Arjuna Central Option. Can pass any number of these switches as -aco x y -aco z t')

        self.parser.add_argument('-ato', '--arjuna-test-option', dest="ato",
                                 nargs=2,
                                 action='append',
                                 metavar=('option', 'value'),
                                 help='Arjuna Test Option. Can pass any number of these switches as -aco x y -ato z t')

        self.parser.add_argument('-uco', '--user-central-option', dest="uco",
                                 nargs=2,
                                 action='append',
                                 metavar=('option', 'value'),
                                 help='User Central Option. Can pass any number of these switches as -aco x y -uco z t')

        self.parser.add_argument('-uto', '--user-text-option', dest="uto",
                                 nargs=2,
                                 action='append',
                                 metavar=('option', 'value'),
                                 help='User Test Option. Can pass any number of these switches as -aco x y -uto z t')

    def process(self, arg_dict):
        pass

class SessionParser(Parser):
    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(add_help=False)
        self.parser.add_argument('-s', '--session-name', dest="unitee.project.session.name", type=partial(lname_check, "Session"), help='Existing session template name.')

    def process(self, arg_dict):
        if arg_dict['unitee.project.session.name'] is None:
            print("Fatal Error in CLI processing. You must provide a valid session name using -s or --session-name switch", file=sys.stderr)
            sys.exit(1)


class GroupParser(Parser):
    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(add_help=False)
        self.parser.add_argument('-g', '--group-name', dest="group.name", type=partial(lname_check, "Group"), help='Existing group template name.')

    def process(self, arg_dict):
        pass


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