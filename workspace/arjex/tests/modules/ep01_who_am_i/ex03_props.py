from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *
from arjuna.tpi.helpers import *

@test_function(4)
def id_test(my):
    console.display(my.info.function.props)

@test_function(id=5)
def id_test2(my):
    console.display(my.info.function.props)

@test_function(id=91, priority=1,
    name='This test demonstrates using of built-in keywords for describing a test function.',
    author='Rahul',
    idea='Explore the test function properties dictionary',
    unstable=True,
    component='Arjuna Sample Project',
    app_version='3.23'
)
def id_test3(my):
    console.display(my.info.function.props)

@test_function(id=91, priority=1,
    name='This test demonstrates using of custom keywords for describing a test function.',
    author='Rahul',
    idea='Explore the test function properties dictionary',
    policy='Product Policy 33',
    os='Mac'
)
def id_test4(my):
    console.display(my.info.function.props)
