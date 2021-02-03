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
        self.parser.add_argument('--project', metavar="test_project_root_dir", dest="project.root.dir", type=project_dir, help = 'Valid absolute path of an existing Arjuna test project. Needed with python -m arjuna call only. With python arjuna_launcher.py you can skip this argument as the script determines its container Arjuna test project automatically.')

    def process(self, arg_dict):
        if arg_dict['project.root.dir'] is None:
            print("Fatal Error in CLI processing. You must provide a valid project root directory using -p or --project-dir switch", file=sys.stderr)
            sys.exit(1)


class NewProjectParser(Parser):
    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(add_help=False)
        self.parser.add_argument('--project', metavar="test_project_root_dir", dest="project.root.dir", type=new_project_dir, help = 'Absolute non-existing Project root directory. Last part of directory represents project name. Name of project should be an Alnum 3-30 length with only lower case letters.')

    def process(self, arg_dict):
        if arg_dict['project.root.dir'] is None:
            print("Fatal Error in CLI processing. You must provide a valid project root directory using -p or --project-dir switch", file=sys.stderr)
            sys.exit(1)