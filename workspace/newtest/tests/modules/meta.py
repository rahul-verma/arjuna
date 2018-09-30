from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *
from arjuna.tpi.helpers import *

@test_function
def passing_test(my):
    # Session Info
    console.display(my.info.session.meta['name'])

    # Stage Info
    console.display(my.info.stage.meta['name'])

    # Group Info
    console.display(my.info.group.meta['name'])
    console.display(my.info.group.meta['slot'])

    # Module Info
    console.display(my.info.module.meta['pkg'])
    console.display(my.info.module.meta['name'])
    console.display(my.info.module.meta['qname'])
    console.display(my.info.module.meta['slot'])

    # Function Info
    console.display(my.info.function.meta['name'])
    console.display(my.info.function.meta['qname'])

    # Object Type (Here it is always Test. However Test is one of the many test object types in Arjuna)
    console.display(my.info.object_type)

    # Test Number. Usually 1. For data driven tests, it is the incremental counter
    console.display(my.info.test_num)

