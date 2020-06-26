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

from arjuna.tpi.error import *

from .group import TestGroups, YamlTestGroup, MagicTestGroup
from .runner import TestGroupRunner
from arjuna.tpi.parser.yaml import YamlList

class TestStage:

    def __init__(self, *, name, config, session, num_threads):
        self.__name = name
        self.__config = config
        self.__session = session
        self.__num_threads = num_threads
        self.__groups = TestGroups()
        self.__workers = []

    def add_group(self, group):
        self.__groups.add_group(group)

    @property
    def name(self):
        return self.__name

    @property
    def config(self):
        return self.__config

    @property
    def session(self):
        return self.__session

    @property
    def num_threads(self):
        return self.__num_threads

    def run(self):
        from arjuna import log_info

        pref = ""
        if self.session.name != "msession":
            pref += self.session.name + "-"
        if self.name != "mstage":
            pref += self.name + "-"
        if self.session.dry_run:
            self.__num_threads = 1

        self.__groups.freeze()
        for i in range(self.num_threads):
            self.__workers.append(TestGroupRunner(
                pref,
                i + 1,
                self.__groups
            ))
        
        for w in self.__workers:
            w.start()

        for w in self.__workers:
            w.join()

        print("All group runners in stage finished.")


class YamlTestStage(TestStage):

    def __init__(self, *, name, stage_yaml, session):
        self.__config = session.config
        self.__num_threads = 1
        self.__load_yaml_meta_data(stage_yaml)
        super().__init__(name=name, config=self.__config, session=session, num_threads=self.__num_threads)
        self.__load_groups(stage_yaml)

    def __load_yaml_meta_data(self, stage_yaml):
        for section_name in stage_yaml.section_names:
            section_name = section_name.lower()
            if section_name.lower() not in {"groups", "include"}:
                if section_name == "threads":
                    self.__num_threads = int(stage_yaml[section_name])
                elif section_name.lower() == "conf":
                    from arjuna import Arjuna
                    self.__config = Arjuna.get_config(stage_yaml["conf"])
  
    def __load_groups(self, stage_yaml):
        from arjuna.engine.session import YamlTestSession
        if "include" not in stage_yaml.section_names:
            raise InvalidTestStageDefError(
                            session_name=self.session.name, 
                            stage_name=self.name, 
                            stages_file_path=YamlTestSession.STAGES_YAML_FILE, 
                            msg="It must contain 'include' section. Section names found: {}".format(tuple(stage_yaml.section_names))
            )

        for section_name in stage_yaml.section_names:
            if section_name.lower() == "include":
                group_names = stage_yaml[section_name]
                if type(group_names) not in {list, YamlList} or set([type(s) is str for s in group_names]) != {True}:
                    raise InvalidTestStageDefError(
                            session_name=self.session.name, 
                            stage_name=self.name, 
                            stages_file_path=YamlTestSession.STAGES_YAML_FILE, 
                            msg="'include' section can only contain a YAML list of group names. Found:\n{}:\n {}".format(section_name, str(stage_yaml[section_name]))
                    )
                for group_name in group_names:
                    self.add_group(YamlTestGroup(name=group_name, group_yaml=YamlTestSession.get_group_yaml(group_name), session=self.session, stage=self))
            # elif section_name.lower() == "groups":
            #     section_name = section_name.lower()
            #     if section_name.lower() == section_name:
            #         groups = stage_yaml.get_section(section_name)
            #         if not groups.section_names:
            #             raise Exception("Invalid session file {}. 'groups' must contain atlease one group section.".format(stage_yaml.file_path))
            #         for group_name in groups.section_names:
            #             group_yaml = groups.get_section(group_name)
            #             self.add_group(YamlTestGroup(group_yaml=group_yaml, session=self.session, stage=self))

class MagicTestStage(TestStage):

    def __init__(self, *, session, rules=None):
        super().__init__(name="mstage", config=session.config, session=session, num_threads=1)
        self.add_group(MagicTestGroup(session=session, stage=self, rules=rules))

class MagicTestStageForGroup(TestStage):

    def __init__(self, *, session, group_name):
        super().__init__(name="mstage", config=session.config, session=session, num_threads=1)
        from arjuna.engine.session import YamlTestSession
        self.add_group(YamlTestGroup(name=group_name, group_yaml=YamlTestSession.get_group_yaml(group_name), session=self.session, stage=self))
        