# This file is a part of Arjuna
# Copyright 2015-2021 Rahul Verma

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

import argparse
import copy
import abc
import sys
import time

from arjuna.core.utils import sys_utils
from arjuna.tpi.constant import *
from arjuna.core.constant import *
from arjuna.tpi.parser.text import _TextResource
from arjuna.core.types import constants
from arjuna.core.adv.py import *
from arjuna.interface.enums import CommandEnum, TargetEnum

from .parser import *
from .command import *

class ArjunaCLI:

    def __init__(self, args):
        super().__init__()
        self._args = args
        from arjuna import Arjuna
        Arjuna._set_command(" ".join(self._args))
        self.arg_dict = None
        self.main_command = MainCommand()

        # Create parser for primary commands
        subparsers = self.main_command.create_subparsers()

        # Create re-usable parses for command arguments
        new_project_parser = NewProjectParser()

        # Create primary command handlers
        self.create_project = CreateProject(subparsers, [new_project_parser])

    def init(self):
        time.sleep(0.1)
        self.arg_dict = self.main_command.convert_to_dict(self._args)
        #self.main_command.execute(self.arg_dict)

    def execute(self):
        command = self.arg_dict['command']
        del self.arg_dict['command']

        if not command:
            print("!!!Fatal Error!!! You did not provide any command.")
            print()
            self.main_command.print_help()
            sys.exit(1)

        # Delegation dictionary for primary command description
        desc_cases = {
            # CommandEnum.LAUNCH_SETU: "Launching Setu",
            CommandEnum.CREATE_PROJECT: "Creating new project",
            # CommandEnum.RUN_PROJECT: "Running the project",
            # CommandEnum.RUN_SESSION: "Running the selected test session",
            # CommandEnum.RUN_STAGE: "Running the selected test stage",
            # CommandEnum.RUN_GROUP: "Running the selected test group",
            # CommandEnum.RUN_SELECTED: "Running tests based on selectors"
        }

        # Hyphens in commands are replaced with underscores for enum conversion
        # So, create-project is internally referred as CREATE_PROJECT
        command_enum = CommandEnum[command.upper().replace("-", "_")]

        print(desc_cases[command_enum] + "...")

        # Delegation dictionary for primary command choices
        # Respective command object's 'execute' method is the handler.
        execute_cases = {
            # CommandEnum.LAUNCH_SETU: (self.launch_setu.execute,),
            CommandEnum.CREATE_PROJECT: (self.create_project.execute, ),
            # CommandEnum.RUN_PROJECT: (self.run_project.execute, ),
            # CommandEnum.RUN_SESSION: (self.run_session.execute, ),
            # CommandEnum.RUN_STAGE: (self.run_stage.execute, ),
            # CommandEnum.RUN_GROUP: (self.run_group.execute, ),
            # CommandEnum.RUN_GROUP: (self.run_group.execute, ),
            # CommandEnum.RUN_SELECTED: (self.run_selected.execute, )
        }

        # Delegation using Arjuna's Enum based switch-case equivalent
        switch = EnumSwitch(execute_cases, (self.arg_dict,))
        switch(command_enum)

    def load(self):
        command = self.arg_dict['command']
        del self.arg_dict['command']

        if not command:
            command = "run-project"

        # Delegation dictionary for primary command description
        desc_cases = {
            # CommandEnum.LAUNCH_SETU: "Launching Setu",
            CommandEnum.CREATE_PROJECT: "Creating new project",
            CommandEnum.RUN_PROJECT: "Loading Project",
            CommandEnum.RUN_GROUP: "Loading group",
            CommandEnum.RUN_SELECTED: "Loading selected tests"
        }

        # Hyphens in commands are replaced with underscores for enum conversion
        # So, create-project is internally referred as CREATE_PROJECT
        command_enum = CommandEnum[command.upper().replace("-", "_")]

        print(desc_cases[command_enum] + "...")

        # Delegation dictionary for primary command choices
        # Respective command object's 'execute' method is the handler.
        execute_cases = {
            CommandEnum.RUN_PROJECT: (self.run_project.load, ),
            CommandEnum.RUN_GROUP: (self.run_group.load, ),
            CommandEnum.RUN_SELECTED: (self.run_selected.load, )
        }

        # Delegation using Arjuna's Enum based switch-case equivalent
        switch = EnumSwitch(execute_cases, (self.arg_dict,))
        switch(command_enum)

