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

from arjuna.core.yaml import Yaml
from .stage import TestStage, MagicTestStage

class BaseTestSession:

    def __init__(self, name, config, dry_run=False):
        self.__name = name
        self.__config = config
        self.__dry_run = dry_run
        self.__stages = []

    def add_stage(self, stage):
        self.__stages.append(stage)

    @property
    def name(self):
        return self.__name

    @property
    def config(self):
        return self.__config

    @property
    def dry_run(self):
        return self.__dry_run
  
    def run(self):
        from arjuna import log_info
        for stage in self.__stages:
            log_info("Executing stage: {} ...".format(stage.name))
            stage.run()
            log_info("Finished Executing stage: {} ...".format(stage.name))


class MagicTestSession(BaseTestSession):

    def __init__(self, config, *, dry_run=False, im=None, em=None, it=None, et=None):
        super().__init__("msession", config, dry_run=dry_run)

        stage = MagicTestStage(config=config, session=self, dry_run=dry_run, im=im, em=em, it=it, et=et)
        self.add_stage(stage)


class YamlTestSession(BaseTestSession):

    def __init__(self, name, config, dry_run=False):
        super().__init__(name, config, dry_run=dry_run)
        self.__yaml = None
        fpath = config.value(ArjunaOption.CONF_SESSIONS_FILE)
        session_yaml = Yaml.from_file(file_path=fpath)
        try:
            self.__yaml = session_yaml.get_section(name)
        except YamlUndefinedSectionError as e:
            raise UndefinedTestSessionError(session_name=name, sessions_file_path=fpath)

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
            stage = TestStage(stage_yaml.name, commands, name_prefix=self.__yaml.name + "-", num_threads=num_threads, dry_run=self.__dry_run)
            self.__runnable_session.add_stage(stage)

        if "stages" not in self.__yaml.section_names:
            raise Exception("Invalid session file {}. It must contain 'stages' section. Section names found: {}".format(self.__yaml_file_path, tuple(self.__yaml.section_names)))

        stages_yaml = self.__yaml.get_section("stages")
        stages = stages_yaml.section_names
        if not stages:
            raise Exception("Invalid session file {}. 'stages' section must define atleast one stage.'".format(self.__yaml_file_path))
        
        self.__runnable_session = RunnableSession()
        for stage in stages:
            __add_stage(stages_yaml.get_section(stage))
