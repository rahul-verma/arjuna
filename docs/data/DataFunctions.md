### Driving with Data Functions

Rather than including static data in Python code, one might want to generate data or pull data from an external service to create data records.

A simple way to achieve this is to write a data function.

```python
# arjuna-samples/arjex_data/test/module/check_03_dd_fixed_func.py

from arjuna import *

def fixed_data_func():
    return range(5)

@test(drive_with=data_function(fixed_data_func))
def check_fixed_data_func(request, data):
    Arjuna.get_logger().info(data[0])
```

#### Points to Note
1. In this example, we create a data function. It always returns the same data when called.
2. We use `data_function` builder function to associate the data function with the test function.
3. Retrieval of values is same as earlier.

You can also use a Python generator instead of a normal function:

```python
# arjuna-samples/arjex_data/test/module/check_04_dd_generator.py

from arjuna import *

def data_generator():
    l = [1,2,3,4,5]
    counter = 0
    while counter < len(l):
        yield l[counter]
        counter += 1

@test(drive_with=data_function(data_generator))
def check_generator_func(request, data):
    Arjuna.get_logger().info(data[0])
```

Another advanced measure that you can take is creating a data function which acts on the arguments supplied by you to govern the data it generates.

```python
# arjuna-samples/arjex_data/test/module/check_05_dd_dynamic_func.py

from arjuna import *

def dynamic_data_func(num):
    return range(num)

@test(drive_with=data_function(dynamic_data_func, 8))
def check_dynamic_data_func(request, data):
    Arjuna.get_logger().info(data[0])
```

##### Points to Note
1. Data functions can take any number of arguments - positional as well as named.
2. You supply the arguments in the `data_function` builder function to control the data function.
