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

import abc
import os
import re
import argparse
import tempfile
import shutil
import logging
import traceback
import json
import sys

from arjuna.lib.core.enums import *
from arjuna.lib.unitee.enums import *
from arjuna.lib.core.utils import sys_utils
from arjuna.lib.core.utils import file_utils
from arjuna.lib.core.reader.hocon import HoconFileReader, HoconConfigDictReader
from arjuna.lib.interface.cli.config import CliArgsConfig
from .validation import *

from arjuna.tpi.enums import ArjunaOption

blank_groups_xml = '''<groups>
    <group name="everything">
        <pickers>
            <picker type="cm" pattern=".*"/>
        </pickers>
    </group>
</groups>'''

class Command(metaclass=abc.ABCMeta):
    PENTRY = '''
    project.name = {}
    workspace.dir = "{}"
    '''

    def __init__(self):
        self.parser = None

    def print_help(self):
        self.parser.print_help()

    def _set_parser(self, parser):
        self.parser = parser

    def get_parser(self):
        return self.parser

    @abc.abstractmethod
    def execute(self, integrator, arg_dict):
        pass

class MainCommand(Command):

    def __init__(self):
        super().__init__()
        parser = argparse.ArgumentParser(prog='python arjuna_launcher.py', conflict_handler='resolve',
                                description="This is the CLI of Arjuna. Use the appropriate command and sub-commands as needed.")
        parser.add_argument('-dl', '--display-level', dest='arjuna.log.console.level', type=ustr, choices=[i for i in LoggingLevelEnum.__members__],
                                 help="Minimum message level for display. (choose from 'DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL')")
        parser.add_argument('-ll', '--log-level', dest='arjuna.log.file.level', type=ustr, choices=[i for i in LoggingLevelEnum.__members__],
                                 help="Minimum message level for log file. (choose from 'DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL')")
        self._set_parser(parser)

    def create_subparsers(self):
        return self.parser.add_subparsers(title="Valid Commands", description="What do you want Arjuna to do?", dest='command')

    def convert_to_dict(self, args):
        try:
            args = self.parser.parse_args(args[1:])
            return vars(args)
        except Exception as e:
            print("!!!Fatal Error!!!")
            print(e)
            import traceback
            traceback.print_exc()
            sys_utils.fexit()

    def execute(self, arg_dict):
        pass

class LaunchSetu(Command):
    def __init__(self, subparsers, parents):
        super().__init__()
        self.parents = parents
        parser = subparsers.add_parser('launch-setu', parents=[parent.get_parser() for parent in parents], help="Launch Setu")
        self._set_parser(parser)

    def execute(self, arg_dict):
        for parent in self.parents:
            parent.process(arg_dict)
        from arjuna.lib.setu.service import launch_setu
        launch_setu((arg_dict["setu.port"]))


class CreateProject(Command):

    def __init__(self, subparsers, parents):
        super().__init__()
        self.parents = parents
        parser = subparsers.add_parser('create-project', parents=[parent.get_parser() for parent in parents], help="Create a new project")
        self._set_parser(parser)

    def execute(self, arg_dict):
        for parent in self.parents:
            parent.process(arg_dict)
        from arjuna.lib.core import ArjunaCore
        integrator = ArjunaCore.integrator
        pname = arg_dict['project.name']
        wsd = self.get_wsdir(integrator, arg_dict)
        existing_project_names = os.listdir(wsd)
        pdir = os.path.join(wsd, pname)
        fatal = False
        reason = None
        if pname in existing_project_names:
            reason = "A directory with name '{}' already exists in workspace:{}.".format(pname, wsd)
            fatal = True
        elif os.path.isfile(pdir):
            reason = "A file with name '{}' already exists in workspace:{}.".format(pname, wsd)
            fatal = True

        if fatal:
            print(reason, "Choose another project name.", file=sys.stderr)
            sys_utils.fexit()
        else:
            if not os.path.isdir(wsd):
                os.makedirs(wsd)
            d_names = integrator.value(CorePropertyTypeEnum.PROJECT_DIRS_FILES)
            with tempfile.TemporaryDirectory() as tdir:
                ptdir = os.path.join(tdir, pname)
                os.mkdir(ptdir)
                for d_name in d_names:
                    os.mkdir(os.path.join(ptdir, d_name))
                f = open(os.path.join(ptdir, "__init__.py"), "w")
                f.close()
                f = open(os.path.join(ptdir, "config", "{}.conf".format(pname)), "w")
                f.close()
                f = open(os.path.join(ptdir, "config", "groups.xml"), "w")
                f.write(blank_groups_xml)
                f.close()
                f = open(os.path.join(ptdir, "fixtures", "__init__.py"), "w")
                f.close()
                f = open(os.path.join(ptdir, "tests", "modules", "__init__.py"), "w")
                f.close()
                shutil.move(ptdir, wsd)

            print("Project {} successfully created.".format(pname))


class __RunCommand(Command):
    def __init__(self, subparsers, sub_parser_name, parents):
        super().__init__()
        self.parents = parents
        parser = subparsers.add_parser(sub_parser_name, parents=[parent.get_parser() for parent in parents])
        self._set_parser(parser)
        self.unitee = None

    def execute(self, arg_dict):
        for parent in self.parents:
            parent.process(arg_dict)

        from arjuna.tpi import Arjuna
        project_root_dir = arg_dict["project.root.dir"]
        del arg_dict["project.root.dir"]
        Arjuna.init(project_root_dir, CliArgsConfig(arg_dict))

        import sys
        proj_dir = Arjuna.get_central_config().get_arjuna_option_value(ArjunaOption.PROJECT_ROOT_DIR).as_string()
        sys.path.append(proj_dir + "/..")

        py_3rdparty_dir = Arjuna.get_central_config().get_arjuna_option_value(ArjunaOption.ARJUNA_EXTERNAL_IMPORTS_DIR).as_string()
        sys.path.append(py_3rdparty_dir)
        self.unitee = Arjuna.get_unitee_instance()
        self.unitee.load_testdb()


class RunProject(__RunCommand):
    def __init__(self, subparsers, parents):
        super().__init__(subparsers, 'run-project', parents)

    def execute(self, arg_dict):
        super().execute(arg_dict)
        self.unitee.load_session_for_all()
        self.unitee.run()
        self.unitee.tear_down()


class RunSession(__RunCommand):
    def __init__(self, subparsers, parents):
        super().__init__(subparsers, 'run-session', parents)

    def execute(self, arg_dict):
        super().execute(arg_dict)
        self.unitee.load_session(arg_dict['unitee.project.session.name'])
        self.unitee.run()
        self.unitee.tear_down()


class RunGroup(__RunCommand):
    def __init__(self, subparsers, parents):
        super().__init__(subparsers, 'run-group', parents)

    def execute(self, arg_dict):
        super().execute(arg_dict)
        self.unitee.load_session_for_group(arg_dict['group.name'])
        self.unitee.run()
        self.unitee.tear_down()


class RunNames(__RunCommand):
    def __init__(self, subparsers, parents):
        super().__init__(subparsers, 'run-names', parents)

    def execute(self, arg_dict):
        picker_args = {
            'cm': arg_dict.pop('cmodules'),
            'im': arg_dict.pop('imodules'),
            'cf': arg_dict.pop('cfunctions'),
            'if': arg_dict.pop('ifunctions')
        }
        super().execute(arg_dict)
        self.unitee.load_session_for_name_pickers(**picker_args)
        self.unitee.run()
        self.unitee.tear_down()

