### DropDown and RadioButton Abstractions

Below is the `@for_test` fixture code to get logged-in WordPress for a test using the reusable module that we created earlier:

```python
# arjuna-samples/arjex_webui_basics/test/module/check_04_gui_multielement.py
from arjuna import *
from arjex_webui_basics.lib.wp import WordPress

@for_test
def wordpress(request):
    # Setup
    wordpress = create_wordpress_app()
    login(wordpress)
    yield wordpress

    # Teadown
    logout(wordpress)
```

### DropDown

DropDown object in Arjuna represents the Select-style control in the UI. Here, we cover handling of a default-HTML select control which has `<select>` as the root tag and `option` as the tag for an option.


```python
# arjuna-samples/arjex_webui_basics/test/module/check_05_dropdown_radiogroup.py

@test
def check_dropdown(request, wordpress):
    wordpress.element(With.link("Settings")).click()

    role_select = wordpress.dropdown(With.id("default_role"))

    role_select.select_text("Subscriber")
    context = "Selection of Subscriber Role"
    request.asserter.assert_true(role_select.has_visible_text_selected("Subscriber"), context)
    request.asserter.assert_true(role_select.has_value_selected("subscriber"), context)
    request.asserter.assert_true(role_select.has_index_selected(0), context)
    request.asserter.assert_equal(role_select.value, "subscriber", "Value attribute of Role")
    request.asserter.assert_equal(role_select.text, "Subscriber",  "Selected Role Text")

    role_select.select_value("editor")
    role_select.select_index(4)
    role_select.text = "Subscriber"
```

#### Points to Note
1. To create an object of a DropDown, we use the `dropdown` factory method of the `WebApp`.
2. We can select an option by its visible text by calling `select_text` method of DropDown.
3. DropDown provides various enquiry methods - `has_visible_text_selected`, `has_value_selected`, has_index_selected`.
4. DropDown also has enquirable properties - `value` and `text`.
5. We assert using `request.asserter`'s appropriate assertion methods.
6. There are other ways of selection as well - `select_value` to select by value attribute of an option, `select_index` to select an option present at provided index.
7. DropDown also has a way of selecting an option by setting its `text` property. This is similar to `.text` property setting of a text-box. It is different from `select_text` method in terms of implementation. `select_text` uses DOM inquiry to match the text of an option and then clicks it to select it. Setting the `.text` property similuates the user action where the user types a string in a focused/highlighted select control to select an option (in technical terms it is equivalent of sendkeys).


### RadioGroup

RadioGroup object in Arjuna represents the Radio Buttons in the UI that belong to a single selection group (have the same name). Here, we cover handling of a default-HTML RadioGroup control which represents multiple `<input type='radio'>` elements which have the same `name` attribute value.


```python
# arjuna-samples/arjex_webui_basics/test/module/check_05_dropdown_radiogroup.py
@test
def check_radiogroup(request, wordpress):
    wordpress.element(With.link("Settings")).click()

    date_format = wordpress.radio_group(With.name("date_format"))

    context = "Selection of m/d/Y date format"
    request.asserter.assert_true(date_format.has_value_selected("m/d/Y"), context)
    request.asserter.assert_true(date_format.has_index_selected(2), context)
    request.asserter.assert_equal(date_format.value, "m/d/Y", "Value attribute of Date Format")

    date_format.select_value(r"\c\u\s\t\o\m")
    date_format.select_index(2)
```

#### Points to Note
1. To create an object of a RadioGroup, we use the `radio_group` factory method of the `WebApp`.
2. We can select a a by its visible text by calling `select_text` method of DropDown.
3. DropDown provides various enquiry methods - `has_value_selected`, `has_index_selected`.
4. DropDown also has `value` enquirable property.
5. We assert using `request.asserter`'s appropriate assertion methods.
6. You can use two ways of selecting a radio button - `select_value` to select by value attribute of an option, `select_index` to select a radio button present at provided index.

