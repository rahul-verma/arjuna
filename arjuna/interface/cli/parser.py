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
        self.parser.add_argument('-rf', '--report-formats', dest="project.report.formats", type=report_format, metavar=('F1','F2'), default=['XML', 'HTML'], nargs='+', help='One or more report format names.') # choices=['XML', 'HTML'], 
        self.parser.add_argument('-e', '--enumerate-only', dest="enumerate", action='store_true', help = 'Show picked tests without running them.')

        # self.parser.add_argument('-aco', '--arjuna-ref-option', dest="aro",
        #                          nargs=2,
        #                          action='append',
        #                          metavar=('option', 'value'),
        #                          help='Arjuna Reference Option. Can pass any number of these switches as -aco x y -aco z t')
        #
        # self.parser.add_argument('-ato', '--arjuna-ext-option', dest="aeo",
        #                          nargs=2,
        #                          action='append',
        #                          metavar=('option', 'value'),
        #                          help='Arjuna Extended Option. Can pass any number of these switches as -aco x y -ato z t')
        #
        # self.parser.add_argument('-uco', '--user-ref-option', dest="uro",
        #                          nargs=2,
        #                          action='append',
        #                          metavar=('option', 'value'),
        #                          help='User Reference Option. Can pass any number of these switches as -aco x y -uco z t')
        #
        # self.parser.add_argument('-uto', '--user-ext-option', dest="ueo",
        #                          nargs=2,
        #                          action='append',
        #                          metavar=('option', 'value'),
        #                          help='User Extended Option. Can pass any number of these switches as -aco x y -uto z t')

    def process(self, arg_dict):
        pass

class PickersParser(Parser):
    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(add_help=False)
        self.parser.add_argument('-cm', '--cmodules', dest="cmodules", metavar=('M1','M2'), default=None, nargs='+', help='One or more names/patterns for considering test modules.')
        self.parser.add_argument('-im', '--imodules', dest="imodules", metavar=('M1','M2'), default=None, nargs='+', help='One or more names/patterns for ignoring test modules.')
        self.parser.add_argument('-cc', '--cclasses', dest="cclasses", metavar=('C1','C2'), default=None, nargs='+', help='One or more names/patterns for considering test classes.')
        self.parser.add_argument('-ic', '--iclasses', dest="iclasses", metavar=('C1','C2'), default=None, nargs='+', help='One or more names/patterns for ignoring test classes.')
        self.parser.add_argument('-cf', '--cfunctions', dest="cfunctions", metavar=('F1','F2'), default=None, nargs='+', help='One or more names/patterns for considering test functions/methods.')
        self.parser.add_argument('-if', '--ifunctions', dest="ifunctions", metavar=('F1','F2'), default=None, nargs='+', help='One or more names/patterns for ignoring test function/methods.')

    def process(self, arg_dict):
        pass

# class NamesParser(Parser):
#     def __init__(self):
#         super().__init__()
#         self.parser = argparse.ArgumentParser(add_help=False)
#         self.parser.add_argument('-cf', '--cfunctions', dest="cfunctions", metavar=('F1','F2'), default=None, nargs='+', help='One or more names/patterns for considering test functions.')
#         # self.parser.add_argument('-cm', '--cmodules', dest="cmodules", metavar=('M1','M2'), default=None, nargs='+', help='One or more names/patterns for considering test modules.')
#         # self.parser.add_argument('-im', '--imodules', dest="imodules", metavar=('M1','M2'), default=None, nargs='+',
#         #                  help='One or more names/patterns for ignoring test modules.')
#         # self.parser.add_argument('-cf', '--cfunctions', dest="cfunctions", metavar=('F1','F2'), default=None, nargs='+', help='One or more names/patterns for considering test functions.')
#         # self.parser.add_argument('-if', '--ifunctions', dest="ifunctions", metavar=('F1','F2'), default=None, nargs='+',
#         #                  help='One or more names/patterns for ignoring test functions.')

#     def process(self, arg_dict):
#         pass