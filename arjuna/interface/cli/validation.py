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
import re

from arjuna.tpi.enums import ArjunaOption

def ustr(input):
    return (str(input)).upper()

VNREGEX = r'^[a-z][_a-z0-9]{2,29}$'
VNREGEX_TEXT = '''
{} name must be a string of length 3-30 containing lower case letters, digits or _ (underscore).
It must begin with a letter.
'''

import os


def new_project_dir(input):
    input = input.rstrip("/").rstrip("\\")
    proj_name = os.path.basename(input)
    lname_check("Project", proj_name)
    if os.path.exists(input):
        print('Project path already exist: {}'.format(input))
        return input
    else:
        os.makedirs(input)
        return input

def project_dir(input):
    if not os.path.exists(input):
        print('Project path does not exist: {}'.format(input))
        print('Exiting...', file=sys.stderr)
        sys.exit(1)
    elif not os.path.isdir(input):
        print('Project path is not a directory: {}'.format(input))
        print('Exiting...', file=sys.stderr)
        sys.exit(1)
    else:
        proj_name = os.path.basename(input)
        lname_check("Project", proj_name)
        return input

def lname_check(context, input):
    if not re.match(VNREGEX, input):
        print('Invalid {} name provided.'.format(context), file=sys.stderr)
        print(VNREGEX_TEXT.format(context), file=sys.stderr)
        print('Exiting...', file=sys.stderr)
        sys.exit(1)
    return input


def port(input):
    if type(input) is not str or int(input) < 1024:
        print('Invalid Setu port {} provided. It should be an int such that 1024 < port < 65535'.format(input))
        sys.exit(1)
    return input