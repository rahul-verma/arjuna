from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *
from arjuna.tpi.helpers import *


def fixed_data_func():
    return range(5)

@test_function(
    drive_with=data_function(fixed_data_func)
)
def drive_with_fixed_data_func(my):
    console.display(my.data.record)