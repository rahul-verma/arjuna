# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

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

from arjuna.tpi.enums import *
from arjuna.core.utils import sys_utils
from arjuna.core.utils import file_utils
from arjuna.core.reader.hocon import HoconFileReader, HoconConfigDictReader
from arjuna.configure.invoker.config import CliArgsConfig
from .validation import *

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
        parser = argparse.ArgumentParser(prog='python -m arjuna', conflict_handler='resolve',
                                description="This is the CLI of Arjuna. Use the appropriate command and sub-commands as needed.")
        parser.add_argument('-dl', '--display-level', dest='log.console.level', type=ustr, choices=[i for i in LoggingLevel.__members__],
                                 help="Minimum message level for display. (choose from 'DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL')", default=LoggingLevel.INFO.name)
        parser.add_argument('-ll', '--log-level', dest='log.file.level', type=ustr, choices=[i for i in LoggingLevel.__members__],
                                 help="Minimum message level for log file. (choose from 'DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL')", default=LoggingLevel.DEBUG.name)
        self._set_parser(parser)

    def create_subparsers(self):
        return self.parser.add_subparsers(title="Valid Commands", description="What do you want Arjuna to do?", dest='command')

    def convert_to_dict(self, args):
        def format_value(k, v):
            if k in {"ao", "uo"}:
                return v
            if type(v) is list:
                return ",".join([str(i) for i in v])
            else:
                return v
        try:
            args = self.parser.parse_args(args[1:])
            return {k:format_value(k,v) for k,v in vars(args).items()}
        except Exception as e:
            print("!!!Fatal Error!!!")
            print(e)
            import traceback
            traceback.print_exc()
            sys_utils.fexit()

    def execute(self, arg_dict):
        pass

#
# class LaunchSetu(Command):
#     def __init__(self, subparsers, parents):
#         super().__init__()
#         self.parents = parents
#         parser = subparsers.add_parser('launch-setu', parents=[parent.get_parser() for parent in parents], help="Launch Setu")
#         self._set_parser(parser)
#
#     def execute(self, arg_dict):
#         for parent in self.parents:
#             parent.process(arg_dict)
#         from arjuna.setu.service import launch_setu
#         launch_setu(int(arg_dict["setu.port"]))


class FileObjectType(Enum):
    DIR = auto()
    FILE = auto()


class CreateProject(Command):

    COMMON_DIRS_FILES = (
        (FileObjectType.DIR, "config"),
        (FileObjectType.DIR, "config/env"),
        (FileObjectType.FILE, "config/project.conf"),
        (FileObjectType.DIR, "data"),
        (FileObjectType.DIR, "data/source"),
        (FileObjectType.DIR, "data/reference"),
        (FileObjectType.DIR, "data/reference/excel_column"),
        (FileObjectType.DIR, "data/reference/excel_row"),
        (FileObjectType.DIR, "l10n"),
        (FileObjectType.DIR, "l10n/excel"),
        (FileObjectType.DIR, "l10n/json"),
        (FileObjectType.DIR, "guiauto"),
        (FileObjectType.DIR, "guiauto/driver"),
        (FileObjectType.DIR, "guiauto/driver/linux"),
        (FileObjectType.DIR, "guiauto/driver/mac"),
        (FileObjectType.DIR, "guiauto/driver/windows"),
        (FileObjectType.DIR, "guiauto/namespace"),
        (FileObjectType.DIR, "guiauto/withx"),
        (FileObjectType.FILE, "guiauto/withx/withx.yaml"),
        (FileObjectType.DIR, "report"),
        (FileObjectType.DIR, "script"),
        (FileObjectType.DIR, "test"),
        (FileObjectType.FILE, "test/__init__.py"),
        (FileObjectType.DIR, "test/module"),
        (FileObjectType.FILE, "test/module/__init__.py"),
        (FileObjectType.DIR, "lib"),
        (FileObjectType.FILE, "lib/__init__.py"),
        (FileObjectType.DIR, "lib/fixture"),
        (FileObjectType.FILE, "lib/fixture/__init__.py"),
        (FileObjectType.FILE, "lib/fixture/session.py"),
        (FileObjectType.FILE, "lib/fixture/module.py"),
        (FileObjectType.FILE, "lib/fixture/test.py"),
    )

    def __init__(self, subparsers, parents):
        super().__init__()
        self.parents = parents
        parser = subparsers.add_parser('create-project', parents=[parent.get_parser() for parent in parents], help="Create a new project")
        self._set_parser(parser)

    def __create_file_or_dir(self, project_temp_dir, ftype, frpath):
        if ftype == FileObjectType.DIR:
            os.makedirs(os.path.join(project_temp_dir, frpath))
        else:
            f = open(os.path.join(project_temp_dir, frpath), "w")
            f.close()

    def execute(self, arg_dict):
        def get_src_file_path(src):
            return os.path.join(os.path.dirname(os.path.realpath(__file__)), src)

        def get_proj_target_path(dest):
            return os.path.join(project_temp_dir, dest)

        def copy_file(src, dest):
            shutil.copyfile(get_src_file_path(src), get_proj_target_path(dest))

        for parent in self.parents:
            parent.process(arg_dict)
        # from arjuna import ArjunaCore
        pdir = arg_dict['project.root.dir']
        if os.path.exists(os.path.join(pdir, "config/project.conf")):
            print("Arjuna project already exists at the specified location.")
            sys.exit(1)
        parent_dir = os.path.abspath(os.path.join(pdir, ".."))
        project_name = os.path.basename(pdir)
        with tempfile.TemporaryDirectory() as tdir:
            project_temp_dir = os.path.join(tdir, project_name)
            os.makedirs(project_temp_dir)
            for ftype, frpath in CreateProject.COMMON_DIRS_FILES:
                self.__create_file_or_dir(project_temp_dir, ftype, frpath)
            copy_file("../../res/proj.conf", "config/project.conf")
            copy_file("../../res/check_dummy.py", "test/module/check_dummy.py")
            copy_file("../../res/arjuna_launcher.py", "script/arjuna_launcher.py")
            f = open(get_src_file_path("../../res/conftest.txt"), "r")
            contents = f.read().format(project=project_name)
            f.close()
            f = open(get_proj_target_path("test/conftest.py"), "w")
            f.write(contents)
            f.close()
            for d in [ "config/env", "data/source", "l10n/excel", "l10n/json", "data/reference/excel_row", "data/reference/excel_column", "guiauto/namespace"]:
                copy_file("../../res/placeholder.txt", d + "/placeholder.txt")
            for os_name in ["mac", "windows", "linux"]:
                copy_file("../../res/placeholder.txt", "guiauto/driver/{}/placeholder.txt".format(os_name))
            for f in os.listdir(project_temp_dir):
                try:
                    shutil.move(os.path.join(project_temp_dir, f), pdir)
                except Exception as e:
                    print(e)
                    pass

        print("Project {} successfully created at {}.".format(project_name, parent_dir))


class __RunCommand(Command):
    def __init__(self, subparsers, sub_parser_name, parents, help):
        super().__init__()
        self.parents = parents
        parser = subparsers.add_parser(sub_parser_name, parents=[parent.get_parser() for parent in parents], help=help)
        self._set_parser(parser)
        self.enumerate_only = False

    def execute(self, arg_dict):
        for parent in self.parents:
            parent.process(arg_dict)

        from arjuna import Arjuna
        project_root_dir = arg_dict.pop("project.root.dir")
        runid = arg_dict.pop("run.id")
        static_rid = arg_dict.pop("static.rid")
        self.dry_run = arg_dict.pop("dry_run")
        self.run_conf = arg_dict.pop("run_conf")

        Arjuna.init(project_root_dir, CliArgsConfig(arg_dict).as_map(), runid, static_rid=static_rid, run_conf=self.run_conf)

        import sys
        proj_dir = Arjuna.get_config().value(ArjunaOption.PROJECT_ROOT_DIR)
        sys.path.append(proj_dir + "/..")

        py_3rdparty_dir = Arjuna.get_config().value(ArjunaOption.ARJUNA_EXTERNAL_IMPORTS_DIR)
        sys.path.append(py_3rdparty_dir)


class RunProject(__RunCommand):
    def __init__(self, subparsers, parents):
        super().__init__(subparsers, 'run-project', parents, "Run all tests in an Arjuna Test Project.")

    def execute(self, arg_dict):
        super().execute(arg_dict)
        from arjuna.engine.runner import TestRunner
        test_runner = TestRunner()
        test_runner.load_all_tests()
        test_runner.run(dry_run=self.dry_run)

class RunSelected(__RunCommand):

    def __init__(self, subparsers, parents):
        super().__init__(subparsers, 'run-selected', parents, "Run tests selected based on selectors specified.")

    def execute(self, arg_dict):
        pickers_dict = dict()
        pickers = (
            ('imodules', 'im'),
            ('emodules', 'em'),
            # ('cclasses', 'cc'),
            # ('iclasses', 'ic'),
            ('itests', 'it'),
            ('etests', 'et'),
            )

        def process_picker(sname, tname):
            if sname in arg_dict:
                val = arg_dict.pop(sname)
                if not val: 
                    pickers_dict[tname] = list()
                    return
                pickers_dict[tname] = val.split(",")
            else:
                pickers_dict[tname] = list()

        def remove_py_ext(name):
            if not name.lower().endswith(".py"):
                return name
            else:
                return name.replace(".py","")

        for picker in pickers:
            process_picker(picker[0], picker[1])

        pickers_dict['im'] = [remove_py_ext(m) for m in pickers_dict['im']]
        pickers_dict['em'] = [remove_py_ext(m) for m in pickers_dict['em']]

        super().execute(arg_dict)

        from arjuna.engine.runner import TestRunner
        test_runner = TestRunner()
        test_runner.load_tests_from_pickers(**pickers_dict)
        test_runner.run(dry_run=self.dry_run)

