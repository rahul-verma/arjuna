### Strict vs Non-strict mode

By default, Arjuna handles localization in a non-strict mode. This means if localized string is absent for a given reference, it ignores the error and returns the reference as return value.

```python
# arjuna-samples/arjex_data/test/module/check_12_dd_localizer.py

from arjuna import *

@test
def check_strict_l10n_mode(request):
    print(L("non_existing"))
    print(L("non_existing", strict=True, locale=Locale.DE_DE))
```

#### Points to Note
1. As by default the strict mode if off, `L("non_existing")` returns `non_existing`.
2. You can enforce strict behavior by providing the `strict=True` argument to the `L` function. The second print statement in above code will raise an exception.
3. You can switch on strict mode at the project level by including `l10n.strict = True` in the `project.conf` file.