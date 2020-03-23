### Arjuna's RadioGroup Abstraction - Handling Default HTML Radio Group

RadioGroup object in Arjuna represents the Radio Buttons in the UI that belong to a single selection group (have the same name). Here, we cover handling of a default-HTML RadioGroup control which represents multiple `<input type='radio'>` elements which have the same `name` attribute value.


#### Test Fixture for Examples in This Page

We are going to use `logged_in_wordpress` test fixture from the GuiMultiElement example.

#### Important point for GNS

The following entry in `WordPress.yaml` is of interest:

```YAML
  date_format:
    template: radio_group
    name: date_format
```

##### Points to Note
1. To instruct Arjuna to treat an element as a `RadioGroup`, under the label entry in GNS file, you can mention `template: radio_group`.

#### Usage

```python
# arjuna-samples/arjex/test/module/check_11_radio_group.py

from arjuna import *
from arjex.lib.app_procedural.wp import *

@test
def check_radiogroup(request, logged_in_wordpress):
    wordpress = logged_in_wordpress
    wordpress.gns.settings.click()

    date_format = wordpress.gns.date_format

    fmsg = "Failed to select m/d/Y date format"
    request.asserter.assert_true(date_format.has_value_selected("m/d/Y"), fmsg)
    request.asserter.assert_true(date_format.has_index_selected(2), fmsg)
    request.asserter.assert_equal(date_format.value, "m/d/Y", "Unpexpected Value attribute of Date Format")

    date_format.select_value(r"\c\u\s\t\o\m")
    date_format.select_index(2)
```

#### Points to Note
1. Creation is same as a Gui Element.
2. We can select a a by its visible text by calling `select_text` method of DropDown.
3. DropDown provides various enquiry methods - `has_value_selected`, `has_index_selected`.
4. DropDown also has `value` enquirable property.
5. We assert using `request.asserter`'s appropriate assertion methods.
6. You can use two ways of selecting a radio button - `select_value` to select by value attribute of an option, `select_index` to select a radio button present at provided index.

