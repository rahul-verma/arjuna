from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *
from arjuna.tpi.helpers import *

@test_function(
    drive_with=records(
        record(1,2,3, ver='v1'),
        record(4,5,6, ver='v2'),
    )
)

def drive_with_multiple_records(my):
    console.display(my.data.record)
    console.display(my.data.record.indexed_values())
    console.display(my.data.record.value_at(1))
    console.display(my.data.record.named_values())
    console.display(my.data.record.value_named('ver'))