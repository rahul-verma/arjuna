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
import re
import os

from arjuna.tpi.constant import *
from arjuna.core.constant import *

def ustr(input):
    return (str(input)).upper()

VNREGEX = r'^[a-z][_a-z0-9]{2,49}$'
VNREGEX_TEXT = '''
{} name must be a string of length 3-50 containing lower case letters, digits or _ (underscore).
It must begin with a letter.
'''

import os


def new_project_dir(input):
    input = input.rstrip("/").rstrip("\\")
    proj_name = os.path.basename(input)
    lname_check("Project", proj_name)
    if os.path.exists(input):
        print('Project path already exists: {}'.format(input))
        return input
    else:
        os.makedirs(input)
        return input

def absolute_file_path(input):
    if not os.path.isabs(input) or not os.path.isfile(input):
        print('Config file path does not exist or is not a file: {}'.format(input))
        print('Exiting...', file=sys.stderr)
        sys.exit(1)
    return input

def project_dir(input):
    if not os.path.exists(input):
        print('Project path does not exist: {}'.format(input))
        print('Current Working Directory: {}'.format(os.getcwd()))
        print('Path should be a correct absolute path or a correct path relative to current working directory.')
        print('Exiting...', file=sys.stderr)
        sys.exit(1)
    elif not os.path.isdir(input):
        print('Project path is not a directory: {}'.format(input))
        print('Exiting...', file=sys.stderr)
        sys.exit(1)
    else:
        if input == ".":
            proj_name = os.path.basename(os.getcwd())
        else:
            proj_name = os.path.basename(input)
        lname_check("Project", proj_name)
        return input

def lname_check(context, input):
    if not re.match(VNREGEX, input):
        print('Invalid {} name {} provided.'.format(context, input), file=sys.stderr)
        print(VNREGEX_TEXT.format(context), file=sys.stderr)
        print('Exiting...', file=sys.stderr)
        sys.exit(1)
    return input

# Argprse sends one argument at a time
def report_format(input):
    try:
        return ReportFormat[input.upper()].name
    except Exception as e:
        print(e)
        print('Invalid Report Format provided: {}. Allowed values: {}'.format(input, ", ".join([e.name for e in ReportFormat])))
        print('Exiting...', file=sys.stderr)
        sys.exit(1)

def dry_run_type(input):
    try:
        return DryRunType[input.upper()].name
    except Exception as e:
        allowed = ", ".join([e.name for e in DryRunType])
        print('Invalid Dry Run Type provided: {}. Allowed values: {}'.format(input, allowed))
        print('Exiting...', file=sys.stderr)
        sys.exit(1)

def int_or_notset(input):
    try:
        return int(input)
    except:
        if input.lower() == "not_set":
            return "not_set"
        else:
            print(e)
            print('Invalid input argument: {}. Expected an int.'.format(input))
            print('Exiting...', file=sys.stderr)
            sys.exit(1)
