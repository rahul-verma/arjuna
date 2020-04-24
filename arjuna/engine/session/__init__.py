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

from arjuna.tpi.constant import ArjunaOption
from arjuna.core.yaml import Yaml
from arjuna.core.error import *
from arjuna.tpi.error import *
from .stage import TestStage, MagicTestStage, YamlTestStage

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

        stage = MagicTestStage(session=self, im=im, em=em, it=it, et=et)
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
        self.__load()

    def __load(self):
        from arjuna import Arjuna

        if "stages" not in self.__yaml.section_names:
            raise InvalidTestSessionDefError(
                            session_name=self.name, 
                            sessions_file_path=self.__yaml_file_path, 
                            msg="It must contain 'stages' section. Section names found: {}".format(tuple(self.__yaml.section_names))
            )

        stages_yaml = self.__yaml.get_section("stages")
        stages = stages_yaml.section_names
        if not stages:
            raise InvalidTestSessionDefError(
                            session_name=self.name, 
                            sessions_file_path=self.__yaml_file_path, 
                            msg="'stages' section must define atleast one stage."
            )
        
        for stage in stages:
            self.add_stage(YamlTestStage(stage_yaml=stages_yaml.get_section(stage), session=self))
