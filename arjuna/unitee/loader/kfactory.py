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

from arjuna.unitee.enums import *

class Kallable:

	def __init__(self, obj):
		self.obj = obj
		self.process()
		self.args = []

	def process(self):
		*pkg_parts, self.module = self.obj.__module__.split(".")
		self.pkg = ".".join(pkg_parts)
		self.name = self.obj.__name__
		self.qname = ".".join([self.pkg, self.module, self.name])

	def __call__(self):
		self.obj(*self.args)

class TestModule(Kallable):
	def process(self):
		*pkg_parts, self.module = self.obj.__name__.split(".")
		self.pkg = ".".join(pkg_parts)
		self.name = self.module
		self.qname = self.obj.__name__

class _TestFunction(Kallable):
	pass

class _DataSourceClass(Kallable):
	pass

class _DataSourceFunction(Kallable):
	pass

class _FixtureFunction(Kallable):
	def __init__(self, func, dec_name):
		super().__init__(func)
		self.type = FixtureTypeEnum[dec_name.upper()]
		self.func = func

class _DepModule(Kallable):
	pass

class _DepFunction(Kallable):
	pass

def __str(obj):
	try:
		return ".".join([obj.__module__, obj.__qualname__])
	except:
		return str(obj)

def create_test_module(obj):
	return TestModule(obj)

def create_dsource_class(obj):
	return _DataSourceClass(obj)

def create_dsource_func(obj):
	return _DataSourceFunction(obj)

def create_fixture(dec_name, obj):
	return _FixtureFunction(obj, dec_name)

def create_test_func(obj):
	return _TestFunction(obj)



