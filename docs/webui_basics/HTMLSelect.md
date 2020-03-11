### Arjuna's DropDown Abstraction - Handling Default HTML Select

DropDown object in Arjuna represents the Select-style control in the UI. Here, we cover handling of a default-HTML select control which has `<select>` as the root tag and `option` as the tag for an option.

#### Test Fixture for Examples in This Page

We are going to use `logged_in_wordpress` test fixture from the GuiMultiElement example.

#### Important point for GNS

The following entry in `WordPress.yaml` is of interest:

```YAML
  role:
    template: dropdown
    id: default_role
```

##### Points to Note
1. To instruct Arjuna to treat an element as a `Dropdown`, under the label entry in GNS file, you can mention `template: dropdown`.

#### Usage

```python
# arjuna-samples/arjex_webui_basics/test/module/check_10_dropdown.py

from arjuna import *

@test
def check_dropdown(request, logged_in_wordpress):
    wordpress = logged_in_wordpress
    wordpress.settings.click()

    role_select = wordpress.role

    role_select.select_text("Subscriber")
    fmsg = "Failed to select Subscriber Role"
    request.asserter.assert_true(role_select.has_visible_text_selected("Subscriber"), fmsg)
    request.asserter.assert_true(role_select.has_value_selected("subscriber"), fmsg)
    request.asserter.assert_true(role_select.has_index_selected(0), fmsg)
    request.asserter.assert_equal(role_select.value, "subscriber", "Unexpected Value attribute of Role.")
    request.asserter.assert_equal(role_select.text,"Subscriber",  "Unexpected Selected Role Text ")

    role_select.select_value("editor")
    role_select.select_index(4)
    role_select.text = "Subscriber"
```

#### Points to Note
1. Creation is same as a Gui Element.
2. We can select an option by its visible text by calling `select_text` method of DropDown.
3. DropDown provides various enquiry methods - `has_visible_text_selected`, `has_value_selected`, has_index_selected`.
4. DropDown also has enquirable properties - `value` and `text`.
5. We assert using `request.asserter`'s appropriate assertion methods.
6. There are other ways of selection as well - `select_value` to select by value attribute of an option, `select_index` to select an option present at provided index.
7. DropDown also has a way of selecting an option by setting its `text` property. This is similar to `.text` property setting of a text-box. It is different from `select_text` method in terms of implementation. `select_text` uses DOM inquiry to match the text of an option and then clicks it to select it. Setting the `.text` property similuates the user action where the user types a string in a focused/highlighted select control to select an option (in technical terms it is equivalent of sendkeys).
