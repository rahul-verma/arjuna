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

