### Data Driven Testing

Driving an automated test with data is a critical feature in test automation frameworks.

Here, we will explore various flexible options available in Arjuna for data driven testing.

You can supply `drive_with` argument to the `@test` decorator to instruct Arjuna to associate a `Data Source` with a test. Depending on the needs, as described below, you use Arjuna's markup for different types of data sources.

#### Single data record

Sometimes, the need is simple. You have a single data record, but want to separate it from the test code for the sake of clarity.

This need is solved with the `record` markup of Arjuna.

```python
# arjuna-samples/arjex_core_features/test/module/check_03_dd_record.py


from arjuna import *

msg="Unexpected data record."

@test(drive_with=record(1,2))
def check_pos_data(request, data):
    request.asserter.assert_equal(data[0] + data[1], 3, msg=msg)

@test(drive_with=record(a=1,b=2))
def check_named_data(request, data):
    request.asserter.assert_equal(data['a'] + data['b'], 3, msg=msg)

@test(drive_with=record(1,2, a=3,b=4))
def check_pos_named_data(request, data):
    request.asserter.assert_equal(data[0] + data[1] + data['a'] + data['b'], 10, msg=msg)

@test(drive_with=record(a=1,b=2))
def check_names_args_with_dot(request, data):
    request.asserter.assert_equal(data.a + data.b, 3, msg=msg)

@test(drive_with=record(a=1,b=2))
def check_names_args_ci(request, data):
    request.asserter.assert_equal(data.A + data['B'], 3, msg=msg)

```

##### Points to Note
1. We provide `drive_with` argument to the `@test` decorator.
2. To specify a single data record, we call the `record` builder function.
3. `record` can take any number of positional or keyword arguments.
4. The signature of the test now contains a `data` argument.
5. Within the body of the tests, you access the positional values using indices (e.g. `data[0]`)
6. You can retrieve named values using a dictionary syntax (e.g. `data['a']`) or dot syntax (e.g. `data.a`).
7. Names are case-insensitive. `data['a']`, `data['A']`, `data.a` and `data.A` mean the same thing.

#### Multiple Data Records

```python
# arjuna-samples/arjex_core_features/test/module/check_04_dd_records.py

from arjuna import *

msg="Unexpected data record."

@test(drive_with=
    records(
        record(1,2,sum=3),    # Pass
        record(4,5,sum=9),    # Pass
        record(7,8,sum=10),   # Fail
    )
)
def check_records(request, data):
    request.asserter.assert_equal(data[0] + data[1], data['sum'], msg=msg)
```

##### Points to Note
1. You use the `records` builder function to provide multiple records.
2. It can contain any number of `record` entries.
3. This test will be repeated as many times as the number of records (3 in this example.)
4. The report will contain separate entries for each test. The name will indicate the data used. (e.g. `test/module/check_04_dd_records.py::check_records[Data-> Indexed:[7, 8] Named:{sum=10}]`)
5. Retrieval of data values is done exactly the same way as in case of a single data record.

#### Data Function

Rather than including static data in Python code, one might want to generate data or pull data from an external service to create data records.

A simple way to achieve this is to write a data function.

```python
# arjuna-samples/arjex_core_features/test/module/check_05_dd_fixed_func.py

from arjuna import *

def fixed_data_func():
    return range(5)

@test(drive_with=data_function(fixed_data_func))
def check_fixed_data_func(request, data):
    Arjuna.get_logger().info(data[0])
```

##### Points to Note
1. In this example, we create a data function. It always returns the same data when called.
2. We use `data_function` builder function to associate the data function with the test function.
3. Retrieval of values is same as earlier.

You can also use a Python generator instead of a normal function:

```python
# arjuna-samples/arjex_core_features/test/module/check_06_dd_generator.py

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
# arjuna-samples/arjex_core_features/test/module/check_07_dd_dynamic_func.py

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



#### Data Class

Instead of a function, you can also represent your data generation logic as a data class.

```python
# arjuna-samples/arjex_core_features/test/module/check_08_dd_class.py

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
# arjuna-samples/arjex_core_features/test/module/check_09_dd_dynamic_class.py

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


#### Data Files

For large, static data it might be useful to externalize the data completely outside of Python code.

Arjuna supports data externalization in XLS, TSV/CSV and INI files out of the box.

```python
# arjuna-samples/arjex_core_features/test/module/check_10_dd_data_files.py

from arjuna import *

@test(drive_with=data_file("input.xls"))
def check_drive_with_excel(request, data):
    request.asserter.assert_equal(int(data.left) + int(data.right), int(data.sum), "Calculation failed.")

@test(drive_with=data_file("input.xls"))
def check_drive_with_excel(request, data):
    request.asserter.assert_equal(int(data.left) + int(data.right), int(data.sum), "Calculation failed.")

@test(drive_with=data_file("input.txt"))
def check_drive_with_tsv(request, data):
    request.asserter.assert_equal(int(data.left) + int(data.right), int(data.sum), "Calculation failed.")

@test(drive_with=data_file("input.csv", delimiter=","))
def check_drive_with_csv(request, data):
    request.asserter.assert_equal(int(data.left) + int(data.right), int(data.sum), "Calculation failed.")

@test(drive_with=data_file("input.ini"))
def check_drive_with_ini(request, data):
    request.asserter.assert_equal(int(data.left) + int(data.right), int(data.sum), "Calculation failed.")
```

For the above code to work, there are sample files provided in the directory `<Project Root>/data/source`.

**input.xls**

<img src="img/inputxls.png">

**input.txt**

```text
Left	Right	Sum
1	2	3
4	5	8
```

**input.csv**

```text
Left,Right,Sum
1,2,3
4,5,8
```

**input.ini**

```ini

[Record 1]
Left = 1
Right = 2
Sum = 3

[Record 2]
Left = 4
Right = 5
Sum = 8
```

##### Points to Note
1. The files are automatically picked up from `Data Sources directory` which is `<Project Root>/data/source`.
2. We use `data_file` builder function to specify a data file. Arjuna determines the loader based on the file extension.
3. `.txt` extension indicates a file with `tab-separated` values.
4. You can specify a custom delimiter by using the `delimiter` argument.

