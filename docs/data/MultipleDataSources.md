#### Driving with Mltiple Data Sources

You can also associate multiple data sources with a single test in Arjuna.

```python
# arjuna-samples/arjex_data/test/module/check_10_dd_many_data_sources.py

from arjuna import *

class MyDataClass:

    def __iter__(self):
        records = (
            {'left':10, 'right':12, 'sum':22},
            {'left':20, 'right':32, 'sum':13},
        )
        return iter(records)


def myrange():
    return (
            {'left':30, 'right':42, 'sum':72},
            {'left':40, 'right':52, 'sum':17},
        )

@test(drive_with=many_data_sources(
    record(left=1, right=2, sum=3),
    records(
        record(left=3, right=4, sum=7),
        record(left=7, right=8, sum=10)
    ),
    data_function(myrange),
    data_class(MyDataClass),
    data_file("input.xls")
))
def check_drive_with_many_sources(request, data):
    request.asserter.assert_equal(int(data.left) + int(data.right), int(data.sum), "Calculation failed.")
```

##### Points to Note
1. We can provide multiple data sources using the `many_data_sources` builder function.
2. Rest of the code remains same. This test will run for a total of `9 times` based on data records from all the sources.

