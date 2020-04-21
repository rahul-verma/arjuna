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

import os
import pytest
import sys
import threading

from arjuna.core.enums import ReportFormat, DryRunType
from arjuna.tpi.enums import ArjunaOption
from arjuna.core.value import Value
from arjuna.core.yaml import YamlFile

class GroupsFinished(Exception):
    pass

class PyTestCommand:

    def __init__(self, config, *, group, im=None, em=None, it=None, et=None, dry_run=False):
        self.__config = config
        self.__group = group
        self.__thname = None
        self.__dry_run = dry_run
        self.__filters = {'im' : im, 'em': em, 'it': it, 'et': et}

    @property
    def config(self):
        return self.__config

    @property
    def thread_name(self):
        return self.__thname

    @thread_name.setter
    def thread_name(self, name):
        self.__thname = name

    @property
    def tests_dir(self):
        return self.__tests_dir

    def run(self):
        from arjuna import Arjuna
        from arjuna.tpi.enums import ArjunaOption
        Arjuna.register_group_params(name=self.__group, config=self.__config, thread_name=self.thread_name)
        self.__load_command_line()

        os.chdir(self.__project_dir)
        print("Executing pytest with args: {}".format(" ".join(self.__pytest_args)))


        pytest_retcode = pytest.main(self.__pytest_args)
        return pytest_retcode

    def __load_command_line(self):
        from arjuna import Arjuna
        from arjuna.tpi.enums import ArjunaOption
        self.__project_dir = self.config.value(ArjunaOption.PROJECT_ROOT_DIR)
        # import sys
        # sys.path.insert(0, self.__project_dir + "/..")
        self.__tests_dir = self.config.value(ArjunaOption.TESTS_DIR)
        suffix = ""
        if self.__group != "mgroup":
            suffix = "-" + self.thread_name + "-" + self.__group
        self.__xml_path = os.path.join(self.config.value(ArjunaOption.REPORT_XML_DIR), "report{}.xml".format(suffix))
        self.__html_path = os.path.join(self.config.value(ArjunaOption.REPORT_HTML_DIR), "report{}.html".format(suffix))
        self.__report_formats = self.config.value(ArjunaOption.REPORT_FORMATS)
        # self.__report_formats = Value.as_enum_list(rfmts, ReportFormat)
        res_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../res"))
        pytest_ini_path = res_path + "/pytest.ini"

        # -s is to print to console.
        self.__pytest_args = ["-c", pytest_ini_path, "--rootdir", self.__project_dir, "--no-print-logs", "--show-capture", "all", "--disable-warnings"] # 
        self.__test_args = []
        self.__load_tests(**self.__filters)
        self.__load_meta_args()


    def __load_tests(self, *, im=None, em=None, it=None, et=None):
        if im is None and em is None and it is None and et is None:
            self.__load_all_tests()
        else:
            self.__load_tests_from_pickers(im=im, em=em, it=it, et=et)

    def __load_all_tests(self):
        self.__pytest_args.insert(0, self.tests_dir)

    def __load_tests_from_pickers(self, *, im=None, em=None, it=None, et=None):  

        def process_modules(ms):
            ms = [m.replace(".py", "").replace("*","").replace("/", " and ").replace("\\", " and ") for m in ms]
            return ["and" in m and "({})".format(m) or m for m in ms]

        k_args = []

        k_flag = False

        if em:            
            em = process_modules(em)
            k_args.append(" and ".join(["not " + m for m in em]))
            k_flag = True

        # if ic:
        #     prefix = k_flag and " and " or ""
        #     k_args.append(prefix + " and ".join(["not " + c for c in ic]))
        #     k_flag = True

        if et:
            prefix = k_flag and " and " or ""
            k_args.append(prefix + " and ".join(["not " + c for c in et]))
            k_flag = True

        if im:
            prefix = k_flag and " and " or ""            
            cm = process_modules(im)
            k_args.append(prefix + " or ".join(im))
            k_flag = True

        # if cc:
        #     prefix = k_flag and " and " or "" 
        #     k_args.append(prefix + " or ".join(cc))
        #     k_flag = True

        if it:
            prefix = k_flag and " and " or "" 
            k_args.append(prefix + " or ".join(it))
            k_flag = True

        if k_flag:
            self.__test_args.append("-k " + "".join(k_args))

    def __load_meta_args(self):
        pytest_report_args = []

        if ReportFormat.XML in self.__report_formats:
            pytest_report_args.extend(["--junit-xml", self.__xml_path])

        if ReportFormat.HTML in self.__report_formats:
            pytest_report_args.extend(["--html", self.__html_path, "--self-contained-html"])

        self.__pytest_args.extend(pytest_report_args)
        self.__pytest_args.extend(self.__test_args)

        if self.__dry_run is not False:
            if self.__dry_run == DryRunType.SHOW_TESTS:
                self.__pytest_args.extend(["--collect-only"])
            elif self.__dry_run == DryRunType.SHOW_PLAN:
                self.__pytest_args.extend(["--setup-plan"])
            elif self.__dry_run == DryRunType.RUN_FIXTURES:
                self.__pytest_args.extend(["--setup-only"])

    def __str__(self):
        return "Command: config={}, group={}, pickers={}".format(self.config.name, self.__group, self.__filters)

class PytestCommands:

    def __init__(self):
        self.__commands = []
        self.__iter = None

    def add_command(self, cmd):
        self.__commands.append(cmd)

    def freeze(self):
        self.__iter = iter(self.__commands)

    def __iter__(self):
        return self

    def next(self):
        try:
            return next(self.__iter)
        except StopIteration:
            raise GroupsFinished()

    def __str__(self):
        return str([str(c) for c in self.__commands])

class TestGroupRunner(threading.Thread):

    def __init__(self, nprefix, wnum, commands):
        super().__init__(name="{}t{}".format(nprefix, wnum))
        #Arjuna.get_unitee_instance().state_mgr.register_thread(self.name)
        self.__commands =  commands

    @property
    def commands(self):
        return self.__commands

    def run(self):
        from arjuna import log_info
        log_info("Group runner started")
        while True:
            try:
                child = self.__commands.next()
            except GroupsFinished as e:
                log_info("Groups finished")
                return
            except Exception as e:
                log_info("An exception occured in thread pooling. Would continue executing.")
                log_info(e)
                import traceback
                traceback.print_exc()
                return
            
            try:
                log_info("Running child")
                child.thread_name = self.name
                child.run()
            except Exception as e:
                log_info(e)
                continue
        log_info("Group runner started")

class RunnableStage:

    def __init__(self, name, commands, name_prefix, num_threads=1, dry_run=False):
        self.__name = name
        self.__workers = []
        pref = ""
        if name != "mstage":
            pref = name + "-"
        for i in range(num_threads):
            self.__workers.append(TestGroupRunner(
                name_prefix + pref,
                i + 1,
                commands
            ))

        self.__dry_run = dry_run

    @property
    def dry_run(self):
        return self.__dry_run

    @property
    def name(self):
        return self.__name

    def run(self):
        from arjuna import log_info
        for w in self.__workers:
            w.start()

        for w in self.__workers:
            w.join()

        log_info("All group runners in stage finished.")

class RunnableSession:

    def __init__(self):
        self.__stages = []

    def add_stage(self, stage):
        self.__stages.append(stage)

    def run(self):
        from arjuna import log_info
        for stage in self.__stages:
            log_info("Executing stage: {} ...".format(stage.name))
            stage.run()
            log_info("Finished Executing stage: {} ...".format(stage.name))

class BaseTestRunner:

    def __init__(self, name, config, runnable_session):
        self.__name = name
        self.__config = config
        self.__runnable_session = runnable_session

    @property
    def name(self):
        return self.__name

    @property
    def config(self):
        return self.__config
  
    def run(self):
        self.__runnable_session.run()


class MSessionRunner(BaseTestRunner):

    def __init__(self, config, *, dry_run=False, im=None, em=None, it=None, et=None):
        commands = PytestCommands()
        command = PyTestCommand(config, group="mgroup", dry_run=dry_run, im=im, em=em, it=it, et=et)
        commands.add_command(command)
        commands.freeze()
        stage = RunnableStage("mstage", commands, name_prefix="", num_threads=1, dry_run=dry_run)
        runnable_session = RunnableSession()
        runnable_session.add_stage(stage)
        super().__init__(config, config, runnable_session)

class SessionRunner(BaseTestRunner):

    def __init__(self, name, config, dry_run=False):
        self.__runnable_session = None
        self.__yaml_file_path = os.path.join(config.value(ArjunaOption.RUN_SESSION_CONF_DIR), name + ".yaml")
        self.__yaml = YamlFile(self.__yaml_file_path)
        self.__dry_run = dry_run
        self.__load(config)
        super().__init__(name, config, self.__runnable_session)

    def __load(self, config):
        from arjuna import Arjuna

        def __add_group_command(commands, group_yaml):
            command_kwargs_dict = {
                'group': group_yaml.name,
                'dry_run': self.__dry_run,
                'im': None,
                'em': None,
                'it': None,
                'et': None,
            }
            cmd_config = config
            for gmd_name in group_yaml.section_names:
                if gmd_name.lower() == "conf":
                    cmd_config = Arjuna.get_config(group_yaml.get_value("conf"))
                elif gmd_name.lower() in {'im', 'em', 'it', 'et'}:
                    command_kwargs_dict[gmd_name.lower()] = group_yaml.get_value(gmd_name)

            command = PyTestCommand(cmd_config, **command_kwargs_dict)
            commands.add_command(command)

        def __add_stage(stage_yaml):
            if "groups" not in stage_yaml.section_names:
                raise Exception("Invalid session file {}. It must contain 'stages' section.".format(self.__yaml_file_path))

            num_threads = 1
            for section_name in stage_yaml.section_names:
                commands = PytestCommands()
                section_name = section_name.lower()
                if section_name.lower() != "groups":
                    if section_name == "threads":
                        if not self.__dry_run:
                            num_threads = int(stage_yaml.get_value(section_name))
                else:
                    groups = stage_yaml.get_section(section_name)
                    if not groups.section_names:
                        raise Exception("Invalid session file {}. 'groups' must contain atlease one group section.".format(self.__yaml_file_path))
                    for group_name in groups.section_names:
                        group = groups.get_section(group_name)
                        __add_group_command(commands, group)

            commands.freeze()
            stage = RunnableStage(stage_yaml.name, commands, name_prefix=self.__yaml.name + "-", num_threads=num_threads, dry_run=self.__dry_run)
            self.__runnable_session.add_stage(stage)

        if "stages" not in self.__yaml.section_names:
            raise Exception("Invalid session file {}. It must contain 'stages' section.".format(self.__yaml_file_path))

        stages_yaml = self.__yaml.get_section("stages")
        stages = stages_yaml.section_names
        if not stages:
            raise Exception("Invalid session file {}. 'stages' section must define atleast one stage.'".format(self.__yaml_file_path))
        
        self.__runnable_session = RunnableSession()
        for stage in stages:
            __add_stage(stages_yaml.get_section(stage))



    



