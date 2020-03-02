### Contextual Data References

There are various situations in which you need contextual data. Such a need is catered by the concept of Contextual Data References (or simply Data References) in Arjuna.

Consider the following example:
1. You have 3 types of user accounts - `Bronze`, `Silver` and `Gold`.
2. The user account information includes a `User` and `Pwd` to repesented user name and password representing a given account type.
3. In different situations, you want to use the user accounts and retrieve them by the context name from a single source of information.

Arjuna supports Excel based data references out of the box. These reference files are automatically loaded when `Arjuna.init()` is called by Arjuna launcher.

#### Content Format for Data References

There are two types of Excel based Data References that you can create in Arjuna:

** Column Data References **

You place such files in `<Project Root>/data/reference/column` directory. A reference file can be found in this example project.

<img src="img/colref.png">

In a column data reference file, the context of data is represented by columns. Here Account Type's values -  `Bronze`, `Silver` and `Gold` represent the contexts, for which the `User` and `Pwd` values are different.

** Row Data References **

You place such files in `<Project Root>/data/reference/row` directory. A reference file can be found in this example project.

<img src="img/rowref.png">

In a row data reference file, the context of data is represented by cells of the first column. Here Account Type's values - `Bronze`, `Silver` and `Gold` represent the contexts, for which the `User` and `Pwd` values are different.

#### Using Data References in Test

```python
# arjuna-samples/arjex_core_features/test/module/check_13_dataref_excel.py

from arjuna import *

@test
def check_excel_column_data_ref(request):
    ref = request.data_refs.cusers
    record = ref.record_for("bronze")
    print(record.user, record.pwd)


@test
def check_excel_row_data_ref(request):
    ref = request.data_refs.rusers
    record = ref.record_for("gold")
    print(record.user, record.pwd)
```

#### Points to Note
1. You can access data references in your test code as `request.data_refs`.
2. The name of the file is used to refer to a given data reference: `request.data_refs.cusers` or `request.data_refs["cusers"]`.
3. Now, we can retrieve the values for a context using the `record_for` method of the reference. For example, here we are retrieiving the values for `gold` context.
4. The values are returned as a `DataRecord` object, which should be familiar to you by this time as it is the same object returned for `drive_with` markup.