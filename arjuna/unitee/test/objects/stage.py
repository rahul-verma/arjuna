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

from .base import *
from .group import TestGroup
from arjuna.unitee.engine.pool import TestObjectThreadPool
from arjuna.unitee.enums import *
from arjuna.unitee.reporter.result.types import *
from arjuna.unitee.state.states import *

class TestStage(TestObject):
	def __init__(self, num, session, defn):
		super().__init__(TestObjectTypeEnum.Stage)
		self.num = num
		self.session = session
		self.defn = defn
		self.name = self.defn.name
		self.thcount = self.defn.threads
		self.groups = []
		self.state = StageState()
		self.fixture_defs = self.defn.fixture_defs
		self.append_before_fixture(self.session.fixture_defs.build(FixtureTypeEnum.INIT_EACH_STAGE))
		self.append_before_fixture(self.fixture_defs.build(FixtureTypeEnum.INIT_STAGE))
		self.append_after_fixture(self.fixture_defs.build(FixtureTypeEnum.END_STAGE))
		self.append_after_fixture(self.session.fixture_defs.build(FixtureTypeEnum.END_EACH_STAGE))

	def load(self, base_tvars):
		self._populate_tvars(base_tvars)
		for index, gdef in enumerate(self.defn.gdefs):
			group = TestGroup(index + 1, self, gdef)
			group.load(self.tvars.clone())
			self.groups.append(group)
		self.children = self.groups

	def _populate_tvars(self, base_tvars):
		self.tvars = base_tvars
		self.tvars.info.stage.meta['name'] = self.defn.name
		if not self.defn.config.is_empty():
			self.tvars.context.update_with_file_config_container(self.defn.config)

	def _execute(self):
		tp = TestObjectThreadPool(self.thcount, self, "{}::{}".format(self.thname, "g"))
		tp.run()

	def report(self, result):
		super().report(result)
		self.session.state.update(result)
		self.session.state.update_test_summary_from_state(self.state)