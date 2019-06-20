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

from .base import TestObject
from .module import TestModule
from arjuna.unitee.engine.pool import TestObjectThreadPool
from arjuna.unitee.enums import *

class TestGroupSlot(TestObject):
	def __init__(self, num, group, mnames):
		super().__init__(TestObjectTypeEnum.GSlot)
		self.num = num
		self.group = group
		self.mnames = mnames
		self.thcount = self.group.mthread_count
		self.modules = []

	def load(self, base_tvars):
		self._populate_tvars(base_tvars)
		for index, mname in enumerate(self.mnames):
			module = TestModule(self.group, self.unitee.testdb.get_mdef(mname))
			module.load(self.tvars.clone())
			self.modules.append(module)
		self.children = self.modules

	def _populate_tvars(self, base_tvars):
		self.tvars = base_tvars
		self.tvars.info.group.meta['slot'] = self.num

	def _execute(self):
		tp = TestObjectThreadPool(self.thcount, self, "{}::{}".format(self.thname, "m"))
		tp.run()

	def report(self, result):
		pass