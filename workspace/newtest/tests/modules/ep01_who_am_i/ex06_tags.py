from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *
from arjuna.tpi.helpers import *

@test_function(
    tags = tags('sample', 'ver2')
)
def configure_tags(my):
    console.display(my.tags)

@test_function(
    tags=tags('sample', 'ver2')
)
def demo_immutable_tags(my):
    console.display(my.tags)
    # This would throw an exception as tags are not mutable within the body of methods just like props.
    # Tags are stored as a Frozen Set
    my.tags['runtime_tag'] = "tag"