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

from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *
from arjuna.tpi.helpers import *

@init_module(author='Mouli', true_prop=True, false_prop=False, none_prop=None, not_none_prop=2, match_prop="matched", partial_match_prop="partial match")
def module_setup(my):
    console.display("ex03 module")
    console.display(my.info.module.props['author'])

@test_function(author='Mouli', my_prop=123)
def test1_picking(my):
    console.display("ex03.test1")

@test_function(author='Mouli', my_prop=456)
def test2_picking(my):
    console.display("ex03.test2")

@test_function(author='Mouli', true_prop=False)
def test3_picking(my):
    console.display("ex03.test3")

@test_function(author='Mouli', true_prop=True, false_prop=True)
def test4_picking(my):
    console.display("ex03.test4")

@test_function(author='Mouli', true_prop=True, false_prop=False, none_prop=2)
def test5_picking(my):
    console.display("ex03.test5")

@test_function(author='Mouli', true_prop=True, false_prop=False, none_prop=None, not_none_prop=None)
def test6_picking(my):
    console.display("ex03.test6")

@test_function(author='Mouli', true_prop=True, false_prop=False, none_prop=None, not_none_prop=2, match_prop="not_matched")
def test7_picking(my):
    console.display("ex03.test7")

@test_function(author='Mouli', true_prop=True, false_prop=False, none_prop=None, not_none_prop=2, match_prop="matched", partial_match_prop="partial")
def test8_picking(my):
    console.display("ex03.test8")

@test_function(author='Mouli', true_prop=True, false_prop=False, none_prop=None, not_none_prop=2, match_prop="matched", partial_match_prop="partial match")
def test9_picking(my):
    console.display("ex03.test9")