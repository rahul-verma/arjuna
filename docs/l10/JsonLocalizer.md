### JSON Based Localization

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