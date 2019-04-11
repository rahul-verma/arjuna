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
from arjuna.lib.core.config import CliArgsConfig
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


class FileObjectType(Enum):
    DIR = auto()
    FILE = auto()


class CreateProject(Command):

    UNITEE_DIRS_FILES = (
        (FileObjectType.DIR, "archives"),
        (FileObjectType.DIR, "config"),
        (FileObjectType.DIR, "config/sessions"),
        (FileObjectType.DIR, "core"),
        (FileObjectType.DIR, "core/db"),
        (FileObjectType.DIR, "core/db/central"),
        (FileObjectType.DIR, "core/db/run"),
        (FileObjectType.DIR, "data"),
        (FileObjectType.DIR, "data/sources"),
        (FileObjectType.DIR, "data/references"),
        (FileObjectType.DIR, "fixtures"),
        (FileObjectType.DIR, "guiauto"),
        (FileObjectType.DIR, "guiauto/drivers"),
        (FileObjectType.DIR, "guiauto/drivers/linux"),
        (FileObjectType.DIR, "guiauto/drivers/mac"),
        (FileObjectType.DIR, "guiauto/drivers/windows"),
        (FileObjectType.DIR, "guiauto/images"),
        (FileObjectType.DIR, "guiauto/namespace"),
        (FileObjectType.DIR, "report"),
        (FileObjectType.DIR, "screenshots"),
        (FileObjectType.DIR, "tests"),
        (FileObjectType.DIR, "tests/modules"),
        (FileObjectType.FILE, "__init__.py"),
        (FileObjectType.FILE, "config/project.conf"),
        (FileObjectType.FILE, "config/groups.xml"),
        (FileObjectType.FILE, "fixtures/__init__.py"),
        (FileObjectType.FILE, "fixtures/all.py"),
        (FileObjectType.FILE, "tests/__init__.py"),
        (FileObjectType.FILE, "tests/modules/__init__.py"),
    )

    def __init__(self, subparsers, parents):
        super().__init__()
        self.parents = parents
        parser = subparsers.add_parser('create-project', parents=[parent.get_parser() for parent in parents], help="Create a new project")
        self._set_parser(parser)

    def execute(self, arg_dict):
        for parent in self.parents:
            parent.process(arg_dict)
        # from arjuna.lib.core import ArjunaCore
        pdir = arg_dict['project.root.dir']
        parent_dir = os.path.abspath(os.path.join(pdir, ".."))
        project_name = os.path.basename(pdir)
        with tempfile.TemporaryDirectory() as tdir:
            project_temp_dir = os.path.join(tdir, project_name)
            os.makedirs(project_temp_dir)
            for ftype, frpath in CreateProject.UNITEE_DIRS_FILES:
                if ftype == FileObjectType.DIR:
                    os.makedirs(os.path.join(project_temp_dir, frpath))
                else:
                    f = open(os.path.join(project_temp_dir, frpath), "w")
                    f.close()
            shutil.move(project_temp_dir, parent_dir)

        print("Project {} successfully created at {}.".format(project_name, parent_dir))


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
        proj_dir = Arjuna.get_central_arjuna_option(ArjunaOption.PROJECT_ROOT_DIR).as_string()
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
        group_name = arg_dict.pop('group.name')
        super().execute(arg_dict)
        self.unitee.load_session_for_group(group_name)
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

