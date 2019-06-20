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
from .func import TestFunc
from arjuna.unitee.engine.pool import TestObjectThreadPool
from arjuna.unitee.enums import *

class TestModuleSlot(TestObject):
	def __init__(self, num, group, module, fnames):
		super().__init__(TestObjectTypeEnum.MSlot)
		self.num = num
		self.group = group
		self.module = module
		self.fnames = fnames
		self.thcount = self.module.fthread_count
		self.funcs = []

	def load(self, base_tvars):
		self._populate_tvars(base_tvars)

		for fname in self.fnames:
			func = TestFunc(self.group, self.module, self, self.module.defn.get_fdef(fname))
			func.load(self.tvars.clone())
			self.funcs.append(func)

		self.children = self.funcs

	def _populate_tvars(self, base_tvars):
		self.tvars = base_tvars
		self.tvars.info.module.meta['slot'] = self.num

	def _execute(self):
		self.tvars.context = self.module.tvars.context.clone()
		self.tvars.runtime.update(self.module.tvars.runtime)
		tp = TestObjectThreadPool(self.thcount, self, "{}::{}".format(self.thname, "f"))
		tp.run()

	def report(self, result):
		pass

	def next(self):
		test_func = super().next()
		return test_func