### Driving with Data Classes

Instead of a function, you can also represent your data generation logic as a data class.

```python
# arjuna-samples/arjex_data/test/module/check_06_dd_class.py

from arjuna import *

class MyDataClass:

    def __iter__(self):
        return iter(range(5))

@test(drive_with=data_class(MyDataClass))
def check_data_class(request, data):
    Arjuna.get_logger().info(data[0])
```

##### Points to Note
1. In this example, we create a data class. It always returns the same data when called.
2. The data class implements the Python Iteration protocol. It has `__iter__` method which returns an iterator.
2. We use `data_class` builder function to associate the data class with the test function.
3. Retrieval of values is same as earlier.

Another advanced measure that you can take is creating a data class which acts on the arguments supplied by you to govern the data it generates.

```python
# arjuna-samples/arjex_data/test/module/check_07_dd_dynamic_class.py

from arjuna import *

class MyDataClass:

    def __init__(self, num):
        self.num = num

    def __iter__(self):
        return iter(range(self.num))

@test(drive_with=data_class(MyDataClass, 8))
def check_dynamic_data_class(request, data):
    Arjuna.get_logger().info(data[0])
```

##### Points to Note
1. Data classes can take any number of arguments - positional as well as named.
2. You supply the arguments in the `data_class` builder function to control the data class.

