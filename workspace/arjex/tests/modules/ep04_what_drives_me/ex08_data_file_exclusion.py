from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *
from arjuna.tpi.helpers import *


@test_function(
    drive_with=data_file("input_exclude_ex.xls")
)
def drive_with_excel(my):
    console.display(my.data.record)


@test_function(
    drive_with=data_file("input_exclude_ex.txt")
)
def drive_with_tsv(my):
    console.display(my.data.record)


@test_function(
    drive_with=data_file("input_exclude_ex.csv")
)
def drive_with_csv(my):
    console.display(my.data.record)


@test_function(
    drive_with=data_file("input_exclude_ex.ini")
)
def drive_with_ini(my):
    console.display(my.data.record)