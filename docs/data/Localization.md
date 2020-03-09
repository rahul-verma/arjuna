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
2. `L("Testing")` localizes the string as per the `ArjunaOption.LOCALE` value in reference configuration. In `project.conf`, we have set it as `HI`.
3. You can also explcitily mention the locale as `Locale.HI`.
4. When a name is repeated across multiple localization files (buckets), the last one holds. `L("Correct")` will give the value from `sample2` file as it is loaded after `sample1`.
5. You can explcitily refer to a bucket by providing the `bucket` argument. Each Excel localization file represents a bucket and its name without the extension is the bucket name.
6. You can also provide the bucket name by prefixing it before the reference key, for example `sample1.corr`.

#### JSON Based Localization

**Sample Localization Files**

With JSON format, there is a specific structure expected. The files are placed in `<Project Root>/data/l10/json` directory.

Following is the sample JSON localization structure created in the examples project:

```
json
├── bucket1
│   ├── de-DE.json
│   └── en-GB.json
├── bucket2
│   ├── de-DE.json
│   └── en-GB.json
├── de-DE.json
└── en-GB.json
```

##### Points to Note
1. Each directory represents a bucket with the name as that of directory. The concept is similar to an Excel file representing a bucket as discussed above.
2. The root directory represents the `root` bucket.
3. For a given bucket, the localization data for a `Locale` is kept in a file named `<locale>.json`.

**Sample JSON Content**

Following is the content of one such file in root directory for German localization:

```JSON
{
  "address": {
    "address": "Adresse",
    "city": "Stadt",
    "coordinates": "Koordinaten",
    "country": "Land",
    "houseNumber": "Hausnummer",
    "latitude": "Breitengrad",
    "location": "Ort",
    "longitude": "Längengrad",
    "postalCode": "Postleitzahl",
    "streetName": "Straße"
  },

  "shared": {
    "back": "zurück",
    "cancel": "Abbrechen"
  }
}
```

##### Points to Note
1. Each JSON path of keys repesents a string to be localized. 
2. The key names should be kept same across language files.
3. `Key1.Key2...KeyN` is the flattened syntax to refer a localized string e.g. `address.coordinates`

#### Using the `L` Function

```python
# arjuna-samples/arjex_data/test/module/check_12_dd_localizer.py

from arjuna import *

@test
def check_json_localizer(request):
    print(L("error.data.lastTransfer", locale=Locale.EN_GB)) # From global l10 container
    print(L("error.data.lastTransfer", locale=Locale.DE_DE)) # From global l10 container

    print(L("error.data.lastTransfer", locale=Locale.EN_GB, bucket="bucket2")) # From bucket2    
    print(L("bucket2.error.data.lastTransfer", locale=Locale.EN_GB)) # From bucket2

    print(L("address.coordinates", locale=Locale.EN_GB, bucket="bucket2"))
    print(L("address.coordinates", locale=Locale.EN_GB, bucket="root"))
    print(L("root.address.coordinates", locale=Locale.EN_GB))
```

##### Points to Note
1. Use the flattened key syntax as discussed earlier. 
2. The key names should be kept same across language files.
3. `Key1.Key2...KeyN` is the flattened syntax to refer a localized string e.g. `address.coordinates`
4. Files in root localization directory are available in `root` bucket.

#### Strict vs Non-strict mode

By default, Arjuna handles localization in a non-strict mode. This means if localized string is absent for a given reference, it ignores the error and returns the reference as return value.

```python
# arjuna-samples/arjex_data/test/module/check_12_dd_localizer.py

from arjuna import *

@test
def check_strict_l10_mode(request):
    print(L("non_existing"))
    print(L("non_existing", strict=True, locale=Locale.DE_DE))
```

##### Points to Note
1. As by default the strict mode if off, `L("non_existing")` returns `non_existing`.
2. You can enforce strict behavior by providing the `strict=True` argument to the `L` function. The second print statement in above code will raise an exception.
3. You can switch on strict mode at the project level by including `l10.strict = True` in the `project.conf` file.