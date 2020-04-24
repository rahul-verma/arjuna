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

from .group import TestGroups, TestGroup, MagicTestGroup
from .runner import TestGroupRunner

class TestStage:

    def __init__(self, *, name, config, groups, session, num_threads, dry_run):
        self.__name = name
        self.__workers = []
        pref = ""
        if session.name != "msession":
            pref += session.name + "-"
        if name != "mstage":
            pref += name + "-"
        for i in range(num_threads):
            self.__workers.append(TestGroupRunner(
                pref,
                i + 1,
                groups
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


class YamlTestStage(TestStage):

    def __init__(self, *, config, stage_yaml, session, dry_run=False):

        super().__init__(name=stage_yaml.name, config=config, groups=groups, session=session, stage=self, num_threads=num_threads, dry_run=dry_run)

class MagicTestStage(TestStage):

    def __init__(self, *, config, session, dry_run=False, im=None, em=None, it=None, et=None):
        groups = TestGroups()
        group = MagicTestGroup(config=config, session=session, stage=self, dry_run=dry_run, im=im, em=em, it=it, et=et)
        groups.add_group(group)
        groups.freeze()
        super().__init__(name="mstage", config=config, groups=groups, session=session, num_threads=1, dry_run=dry_run)