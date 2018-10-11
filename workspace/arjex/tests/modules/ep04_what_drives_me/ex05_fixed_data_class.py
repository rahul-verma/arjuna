from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *
from arjuna.tpi.helpers import *


class MyDataClass:

    def __iter__(self):
        return iter(range(5))

@test_function(
    drive_with=data_class(MyDataClass)
)
def drive_with_fixed_data_class(my):
    console.display(my.data.record)