### Localization of Strings

As a part of automating tests, a test author might need to deal with localization of strings that are used for various purposes.

Arjuna supports Excel based localization data out of the box. These files are automatically loaded when `Arjuna.init()` is called by Arjuna launcher.

**Sample Localization File**

The localization file follows the format of Excel Column Data Reference files.

You place such files in `<Project Root>/data/l10/excel` directory. A reference file can be found in this example project.

<img src="img/l10.png">

First column is always the English language column. The other columns represent the other languages mentioned as `Locale` type in column heading.

In the example file, the column mentions `hi` which is Locale value for Hindi.

For demonstration purpose, 2 English words are provided with corresponding strings in Hindi.

#### Using Data References in Test

```python
# arjuna-samples/arjex_core_features/test/module/check_14_dd_localizer.py

from arjuna import *

@test
def check_excel_localizer(request):
    print(L("Testing"))
    print(L("Quality", Locale.HI))
```

#### Points to Note
1. Arjuna provides a special function `L` for localizing a string.
2. `L("Testing")` localizes the string as the `ArjunaOption.LOCALE` value in reference configuration.
3. You can also explcitily mention the locale as `Locale.HI`.
