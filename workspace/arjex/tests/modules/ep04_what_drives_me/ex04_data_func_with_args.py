from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *
from arjuna.tpi.helpers import *


def data_func_with_args(num):
    return range(num)

@test_function(
    drive_with=data_function(data_func_with_args, 8)
)
def drive_with_data_func_args(my):
    console.display(my.data.record)