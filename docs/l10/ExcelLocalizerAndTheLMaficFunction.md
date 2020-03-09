### Localization of Strings

As a part of automating tests, a test author might need to deal with localization of strings that are used for various purposes.

Arjuna supports Excel based localization data out of the box. These files are automatically loaded when `Arjuna.init()` is called by Arjuna launcher.

#### Excel based Localization

**Sample Localization File**

The localization file follows the format of Excel Column Data Reference files.

You place such files in `<Project Root>/data/l10/excel` directory. Two reference files can be found in this example project.

<img src="img/l10_1.png">

First column is always the Reference column. The other columns represent the languages mentioned as `Locale` type in column heading.

In the example file, the columns mentions `en` and `hi` which are Locale value for English and Hindi respectively.

For demonstration purpose, 3 English words are provided with corresponding strings in Hindi.

<img src="img/l10_2.png">

The second file `sample2.xls` has the same data except the localized string for `Correct` in Hindi which is different from `sample1.xls`.

##### The `L` function for Localization

```python
# arjuna-samples/arjex_data/test/module/check_12_dd_localizer.py

from arjuna import *

@test
def check_excel_localizer(request):
    print(L("test")) # Default Locale in Config
    print(L("qual", locale=Locale.HI))
    print(L("qual", locale=Locale.EN))

    print(L("corr")) # From global l10 container

    print(L("corr", bucket="sample1")) # From sample1 excel file (bucket)
    print(L("corr", bucket="sample2")) # From sample2 excel file (bucket)

    print(L("sample1.corr")) # From sample1 excel file (bucket)
    print(L("sample2.corr")) # From sample2 excel file (bucket)
```

```
# project.conf

arjunaOptions {
    l10.locale = hi
}
```

#### Points to Note
1. Arjuna provides a special function `L` for localizing a string.
2. `L("Testing")` localizes the string as per the `ArjunaOption.L10_LOCALE` value in reference configuration. In `project.conf`, we have set it as `HI`.
3. You can also explcitily mention the locale as `Locale.HI`.
4. When a name is repeated across multiple localization files (buckets), the last one holds. `L("Correct")` will give the value from `sample2` file as it is loaded after `sample1`.
5. You can explcitily refer to a bucket by providing the `bucket` argument. Each Excel localization file represents a bucket and its name without the extension is the bucket name.
6. You can also provide the bucket name by prefixing it before the reference key, for example `sample1.corr`.