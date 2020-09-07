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
from arjuna.tpi.parser.yaml import Yaml
from arjuna.core.error import *
from arjuna.tpi.error import *
from .stage import TestStage, MagicTestStage, YamlTestStage, MagicTestStageForGroup
from arjuna.tpi.parser.yaml import YamlList

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
            print("Executing stage: {} ...".format(stage.name))
            stage.run()
            print("Finished Executing stage: {} ...".format(stage.name))
            import time
            time.sleep(2)


class MagicTestSession(BaseTestSession):

    def __init__(self, config, *, rules=None, dry_run=False):
        super().__init__("msession", config, dry_run=dry_run)

        stage = MagicTestStage(session=self, rules=rules)
        self.add_stage(stage)

class MagicTestSessionForStage(BaseTestSession):

    def __init__(self, stage_name, config, dry_run=False):
        super().__init__("msession", config, dry_run=dry_run)

        YamlTestSession.load_session_defs()
        self.add_stage(YamlTestStage(name=stage_name, stage_yaml=YamlTestSession.get_stage_yaml(stage_name), session=self))

class MagicTestSessionForGroup(BaseTestSession):

    def __init__(self, group_name, config, dry_run=False):
        super().__init__("msession", config, dry_run=dry_run)

        YamlTestSession.load_session_defs()
        self.add_stage(MagicTestStageForGroup(session=self, group_name=group_name))

class YamlTestSession(BaseTestSession):

    __SESSIONS_YAML = None
    SESSIONS_YAML_FILE = None
    __STAGES_YAML = None
    STAGES_YAML_FILE = None
    __GROUPS_YAML = None
    GROUPS_YAML_FILE = None

    @classmethod
    def __load_sessions_file(cls):
        from arjuna import C
        if cls.__SESSIONS_YAML is None:
            cls.SESSIONS_YAML_FILE = C(ArjunaOption.CONF_SESSIONS_FILE)
            try:
                cls.__SESSIONS_YAML = Yaml.from_file(cls.SESSIONS_YAML_FILE, allow_any=True)
            except FileNotFoundError as e:
                raise TestSessionsFileNotFoundError(file_path=cls.SESSIONS_YAML_FILE)

    @classmethod
    def get_session_yaml(cls, name):
        try:
            return cls.__SESSIONS_YAML.get_section(name)
        except YamlUndefinedSectionError as e:
            raise UndefinedTestSessionError(name=name, file_path=cls.SESSIONS_YAML_FILE)

    @classmethod
    def __load_stages_file(cls):
        from arjuna import C
        if cls.__STAGES_YAML is None:
            cls.STAGES_YAML_FILE = C(ArjunaOption.CONF_STAGES_FILE)
            try:
                cls.__STAGES_YAML = Yaml.from_file(cls.STAGES_YAML_FILE, allow_any=True)
            except FileNotFoundError:
                raise TestStagesFileNotFoundError(file_path=cls.STAGES_YAML_FILE)

    @classmethod
    def get_stage_yaml(cls, name):
        try:
            return cls.__STAGES_YAML.get_section(name)
        except YamlUndefinedSectionError as e:
            raise UndefinedTestStageError(name=name, file_path=cls.STAGES_YAML_FILE)

    @classmethod
    def __load_groups_file(cls):
        from arjuna import C
        if cls.__GROUPS_YAML is None:
            cls.GROUPS_YAML_FILE = C(ArjunaOption.CONF_GROUPS_FILE)
            try:
                cls.__GROUPS_YAML = Yaml.from_file(cls.GROUPS_YAML_FILE, allow_any=True)
            except FileNotFoundError:
                raise TestGroupsFileNotFoundError(file_path=cls.GROUPS_YAML_FILE)

    @classmethod
    def get_group_yaml(cls, name):
        try:
            return cls.__GROUPS_YAML.get_section(name)
        except YamlUndefinedSectionError as e:
            raise UndefinedTestGroupError(name=name, file_path=cls.GROUPS_YAML_FILE)

    @classmethod
    def load_session_defs(cls):
        cls.__load_sessions_file()
        cls.__load_stages_file()
        cls.__load_groups_file()

    def __init__(self, name, ref_config_name, dry_run=False):
        self.__yaml = None
        self.load_session_defs()
        self.__yaml = self.get_session_yaml(name)

        from arjuna import Arjuna
        self.__config = None
        if ref_config_name is None:
            self.__config = Arjuna.get_config()
        else:
            self.__config = Arjuna.get_config(ref_config_name)
        self.__load_metadata()
        super().__init__(name, self.__config, dry_run=dry_run)
        self.__load_stages()

    def __load_metadata(self):
        for section_name in self.__yaml.section_names:
            section_name = section_name.lower()
            if section_name.lower() not in {"groups", "include"}:
                if section_name.lower() == "conf":
                    from arjuna import Arjuna
                    self.__config = Arjuna.get_config(self.__yaml["conf"])

    def __load_stages(self):
        from arjuna import Arjuna

        if "include" not in self.__yaml.section_names:
            raise InvalidTestSessionDefError(
                            session_name=self.name, 
                            sessions_file_path=self.SESSIONS_YAML_FILE, 
                            msg="It must contain 'include' section. Section names found: {}".format(tuple(self.__yaml.section_names))
            )

        for section_name in  self.__yaml.section_names:
            if section_name.lower() == "include":
                stage_names = self.__yaml[section_name]
                if type(stage_names) not in {list, YamlList} or set([type(s) is str for s in stage_names]) != {True}:
                    raise InvalidTestSessionDefError(
                                    session_name=self.name, 
                                    sessions_file_path=self.SESSIONS_YAML_FILE, 
                                    msg="'include' section can only contain a YAML list of stage names. Found:\n{}:\n {}".format(section_name, str(self.__yaml[section_name]))
                    )
                for stage_name in stage_names:
                    self.add_stage(YamlTestStage(name=stage_name, stage_yaml=self.get_stage_yaml(stage_name), session=self))
            # elif section_name.lower() == "stages":
            #     stages_yaml = self.__yaml.get_section(section_name)
            #     stages = stages_yaml.section_names
            #     if not stages:
            #         raise InvalidTestSessionDefError(
            #                         session_name=self.name, 
            #                         sessions_file_path=self.__SESSIONS_YAML.file_path, 
            #                         msg="'stages' section must define atleast one stage."
            #         )
                
            #     for stage in stages:
            #         self.add_stage(YamlTestStage(stage_yaml=stages_yaml.get_section(stage), session=self))
