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

import argparse
import copy
import abc
import sys
import time

from arjuna.lib.core.utils import sys_utils
from arjuna.lib.core.enums import *
from arjuna.lib.enums import *
from arjuna.lib.core.reader.textfile import TextResourceReader
from arjuna.lib.core.types import constants
from arjuna.lib.core.adv.py import *

from .commands import *

class ArjunaCLI:

    def __init__(self, args):
        super().__init__()
        self._args = args
        self.arg_dict = None
        self.main_command = MainCommand()
        subparsers = self.main_command.create_subparsers()

        run_parser =  RunParser(subparsers)
        session_parser = SessionParser(subparsers)
        group_parser = GroupParser(subparsers)
        names_parser = NamesParser(subparsers)

        self.create_project = CreateProject(subparsers)
        self.run_project = RunProject(subparsers, [run_parser])
        self.run_session = RunSession(subparsers, [run_parser, session_parser])
        self.run_group = RunGroup(subparsers, [run_parser, group_parser])
        self.run_names = RunNames(subparsers, [run_parser, names_parser])

    def init(self):
        time.sleep(0.1)
        self.arg_dict = self.main_command.convert_to_dict(self._args)
        self.main_command.execute(self.arg_dict)

    def execute(self):

        command = self.arg_dict['command']
        del self.arg_dict['command']

        cases = {
            CommandEnum.CREATE_PROJECT : (self.create_project.execute, ),
            CommandEnum.RUN_PROJECT : (self.run_project.execute, ),
            CommandEnum.RUN_SESSION : (self.run_session.execute, ),
            CommandEnum.RUN_GROUP : (self.run_group.execute, ),
            CommandEnum.RUN_NAMES : (self.run_names.execute, )
        }

        switch = EnumSwitch(cases, (self.arg_dict,))
        switch(CommandEnum[command.upper().replace("-","_")])
