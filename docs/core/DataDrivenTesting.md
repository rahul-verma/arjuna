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

