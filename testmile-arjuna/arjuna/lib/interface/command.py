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

from arjuna.lib.core import ARJUNA_ROOT
from arjuna.lib.core.enums import *
from arjuna.lib.unitee.enums import *
from arjuna.lib.core.utils import sys_utils
from arjuna.lib.core.reader.hocon import HoconFileReader, HoconConfigDictReader
from arjuna.lib.core.reader.textfile import TextResourceReader
from arjuna.lib.unitee import UniteeFacade

from .validation import *

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

    def __process_conf_file(self, path):
        from arjuna.lib.core import ArjunaCore

        armap = {}
        uomap = {}
        evars = {}

        try:
            r = HoconFileReader(path)
            r.process()
        except Exception as e:
            strace = traceback.format_exc()
            ArjunaCore.console.display_exception_block(e, strace)
            sys_utils.fexit()
        else:
            for k,v in r.get_map().items():
                lk = k.lower()
                if lk == "arjuna_options":
                    r = HoconConfigDictReader(v)
                    r.process()
                    armap = r.get_flat_map()
                elif lk == "evars":
                    uomap = v
                elif lk == "user_options":
                    evars = v

        return armap, uomap, evars

    def __process_confs(self, integrator, ppd, pname, cli_map):
        cfile = os.path.join(integrator.value(CorePropertyTypeEnum.CONFIG_DIR),
                             integrator.value(CorePropertyTypeEnum.CONFIG_CENTRAL_FILE_NAME))

        armap, uomap, evars = self.__process_conf_file(cfile)
        armap2, uomap2, evars2 = self.__process_conf_file(os.path.join(ppd, pname, "config", "{}.conf".format(pname)))

        armap.update(armap2); uomap.update(uomap2); evars.update(evars2)

        integrator.process_conf_file_options(armap)
        integrator.process_interface_options(cli_map)

        integrator.process_user_options(uomap)

        integrator.process_evars(evars)


    def _init_components(self, arg_dict):
        from arjuna.lib.core import ArjunaCore
        integrator = ArjunaCore.integrator
        pname = arg_dict['project.name']
        wsd = self.get_wsdir(integrator, arg_dict)
        runid = arg_dict['runid']

        from arjuna.lib.unitee import init
        init(pname, wsd, runid)
        self.__process_confs(integrator, wsd, pname, arg_dict)

        ArjunaCore.freeze(integrator)
        integrator.enumerate()

        # All options are processed, so if components want to do initial processing, it is done here.
        integrator.load()

    def get_wsdir(self, integrator, arg_dict):
        return arg_dict['workspace.dir'] and arg_dict['workspace.dir'] or integrator.value(CorePropertyTypeEnum.WORKSPACE_DIR)

class MainCommand(Command):

    def __init__(self):
        super().__init__()
        parser = argparse.ArgumentParser(prog='python arjuna_launcher.py', conflict_handler='resolve',
                                description="This is the CLI of Arjuna. Use the appropriate command and sub-commands as needed.")
        parser.add_argument('-dl', '--display-level', dest='logger.console.level', type=ustr, choices=[i for i in LoggingLevelEnum.__members__],
                                 help="Minimum message level for display. (choose from 'DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL')")
        parser.add_argument('-ll', '--log-level', dest='logger.file.level', type=ustr, choices=[i for i in LoggingLevelEnum.__members__],
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
        from arjuna.lib.core import init
        init(arg_dict)
        # This is the first stage at which integrator can enumerate properties
        # integrator.enumerate()

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
                f = open(os.path.join(ptdir, "config", "groups.conf"), "w")
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
        self._init_components(arg_dict)

        import sys
        from arjuna.lib.core import ArjunaCore
        sys.path.append(ArjunaCore.config.value(UniteePropertyEnum.PROJECT_DIR) + "/..")
        self.unitee = UniteeFacade()
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
        from arjuna.lib.core import ArjunaCore
        self.unitee.load_session(ArjunaCore.config.value(UniteePropertyEnum.SESSION_NAME))
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
        super().execute(arg_dict)
        self.unitee.load_session_for_name_pickers(arg_dict['cmodules'],arg_dict['imodules'],arg_dict['cfunctions'],arg_dict['ifunctions'])
        self.unitee.run()
        self.unitee.tear_down()

