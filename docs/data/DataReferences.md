### Contextual Data References

There are various situations in which you need contextual data. Such a need is catered by the concept of Contextual Data References (or simply Data References) in Arjuna.

Consider the following example:
1. You have 3 types of user accounts - `Bronze`, `Silver` and `Gold`.
2. The user account information includes a `User` and `Pwd` to repesented user name and password representing a given account type.
3. In different situations, you want to use the user accounts and retrieve them by the context name from a single source of information.

Arjuna supports Excel based data references out of the box. These reference files are automatically loaded when `Arjuna.init()` is called by Arjuna launcher.

#### Content Format for Data References

There are two types of Excel based Data References that you can create in Arjuna:

**Column Data References**

You place such files in `<Project Root>/data/reference/column` directory. A reference file can be found in this example project.

<img src="img/colref.png">

In a column data reference file, the context of data is represented by columns. Here Account Type's values -  `Bronze`, `Silver` and `Gold` represent the contexts, for which the `User` and `Pwd` values are different.

**Row Data References**

You place such files in `<Project Root>/data/reference/row` directory. A reference file can be found in this example project.

<img src="img/rowref.png">

In a row data reference file, the context of data is represented by cells of the first column. Here Account Type's values - `Bronze`, `Silver` and `Gold` represent the contexts, for which the `User` and `Pwd` values are different.

#### Using Data References in Test

```python
# arjuna-samples/arjex_data/test/module/check_11_dataref_excel.py

from arjuna import *

@test
def check_excel_column_data_ref(request):
    print(R("user", bucket="cusers", context="bronze"))
    print(R("bronze.user", bucket="cusers"))
    print(R("cusers.bronze.user"))


@test
def check_excel_row_data_ref(request):
    print(R("user", bucket="rusers", context="gold"))
    print(R("gold.user", bucket="rusers"))
    print(R("rusers.gold.user"))
```

#### Points to Note
1. You can access data references in your test code with Arjuna's special `R` function (similar to `L` and `C` functions seen in other features).
2. The name of the file is the `bucket` name. For example, here `cusers` and `rusers` are buckets represenating `cusers.xls` and `rusers.xls` data reference files.
3. You can retrieve values from the data reference with a combination of `query`, `bucket` and `context` combinations.
    - Query can contain just the ref name and bucket and context arguments can be provided.
    - Query can be of format `context.refname` and bucket can be supplied as argument.
    - Query can be of format `bucket.context.refname` without passing bucket and context arguments separately.
4. The only difference between the two styles of references is the format and the way Arjuna loads them. Usage for a test author is exactly the same.
