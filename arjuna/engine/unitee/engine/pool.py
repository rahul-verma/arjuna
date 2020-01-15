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

from arjuna.tpi import Arjuna
from threading import Thread
from arjuna.unitee import Unitee
from arjuna.unitee.exceptions import *

class TestObjectRunner(Thread):

	def __init__(self, nprefix, wnum, test_obj):
		Thread.__init__(self, name="{}-{}".format(nprefix, wnum))
		Arjuna.get_unitee_instance().state_mgr.register_thread(self.name)
		self.test_obj =  test_obj

	def run(self):
		while True:
			try:
				child = self.test_obj.next()
			except SubTestsFinished as e:
				return
			except Exception as e:
				print  ("An exception occured in thread pooling. Would continue executing.")
				print (e)
				import traceback
				traceback.print_exc()
				return

			child.thname = self.name
			child.run()

class TestObjectThreadPool:

	def __init__(self, num_threads, test_obj, ct_name_prefix):
		self.workers = []
		for i in range(num_threads):
			self.workers.append(TestObjectRunner(
				ct_name_prefix,
				i + 1,
				test_obj
			))

	def run(self):
		for w in self.workers:
			w.start()

		for w in self.workers:
			w.join()