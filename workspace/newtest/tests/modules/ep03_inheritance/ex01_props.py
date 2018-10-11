from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *
from arjuna.tpi.helpers import *

@init_module(id=91, priority=1,
    name='This test demonstrates using of custom keywords for describing a test module.',
    author='Rahul',
    idea='Explore the test module properties dictionary',
    policy='Product Policy 33',
    os='Mac'
)
def setup_module(my):
    pass

@test_function
def demo_inherited_module_props(my):
    console.display(my.info.module.props)