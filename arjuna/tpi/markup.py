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

from functools import partial
from arjuna.unitee.markup.tsmarkup import *

test_function = test_function
tfunc = test_function

init_module = init_module
end_module = partial(fixture, "end_module")
init_each_function = partial(fixture, "init_each_function")
init_tfunc = init_each_function
end_each_function = partial(fixture, "end_each_function")
end_tfunc = end_each_function
init_each_test = partial(fixture, "init_each_test")
init_test = init_each_test
end_each_test = partial(fixture, "end_each_test")
end_test = end_each_test

skip_me = skip_me

