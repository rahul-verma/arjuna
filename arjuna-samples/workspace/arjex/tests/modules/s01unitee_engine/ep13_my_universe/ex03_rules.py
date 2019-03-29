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

@test_function(author='Rahul Verma')
def test1_picking(my):
    console.display("ex03.test1")

@test_function(author='Don')
def test2_picking(my):
    console.display("ex03.test2")

@test_function(unstable=True, author=None,bugs=bugs('B1'))
def test3_picking(my):
    console.display("ex03.test3")

@test_function(author='Rahul Verma', priority=2)
def test4_picking(my):
    console.display("ex03.test4")

@test_function(author='Rahul Verma', priority=2, rating=5, something='cooking', give_up=False)
def test5_picking(my):
    console.display("ex03.test5")


@test_function(evars=evars(myvar="testing"))
def test6_picking(my):
    console.display("ex03.test6")


@test_function(abc=2, evars=evars(myvar="testing", myvar2=20, myvar3=True))
def test7_picking(my):
    console.display("ex03.test7")

@test_function(tags=tags('Chrome'))
def test8_picking(my):
    console.display("ex03.test8")

@test_function(tags=tags('Chrome','Firefox'))
def test9_picking(my):
    console.display("ex03.test9")

@test_function(bugs=bugs('B1'))
def test10_picking(my):
    console.display("ex03.test10")

@test_function(bugs=bugs('B1','B2'))
def test11_picking(my):
    console.display("ex03.test11")