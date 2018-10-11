from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *
from arjuna.tpi.helpers import *

@test_function(
    evars = evars(sample_var="your_value")
)
def passing_test(my):
    console.display(my.evars)
    my.evars['runtime_evar'] = "dynamic"
    console.display(my.evars)