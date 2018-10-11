from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *
from arjuna.tpi.helpers import *


class MyDataClass:

    def __init__(self, num):
        self.num = num

    def __iter__(self):
        return iter(range(self.num))

@test_function(
    drive_with=data_class(MyDataClass, 8)
)
def drive_with_data_class_with_args(my):
    console.display(my.data.record)