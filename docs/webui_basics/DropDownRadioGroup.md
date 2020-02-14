### DropDown and RadioButton Abstractions

We will use the logged in WordPress app fixture that we used in previous example(s).

```python
# arjuna-samples/arjex_webui_basics/tests/modules/test_05_dropdown_radiogroup.py

@for_test
def wordpress(request):
    # Setup
    wordpress = WordPress()
    wordpress.login()
    yield wordpress

    # Teadown
    wordpress.logout()
```

### DropDown

DropDown object in Arjuna represents the Select-style control in the UI. Here, we cover handling of a default-HTML select control which has `<select>` as the root tag and `option` as the tag for an option.


```python
# arjuna-samples/arjex_webui_basics/tests/modules/test_05_dropdown_radiogroup.py

@test
def test_dropdown(my, request, wordpress):
    wordpress.element(With.link("Settings")).click()

    role_select = wordpress.dropdown(With.id("default_role"))

    role_select.select_text("Subscriber")
    context = "Selection of Subscriber Role"
    my.asserter.assert_true(role_select.has_visible_text_selected("Subscriber"), context)
    my.asserter.assert_true(role_select.has_value_selected("subscriber"), context)
    my.asserter.assert_true(role_select.has_index_selected(0), context)
    my.asserter.assert_equal(role_select.value, "subscriber", "Value attribute of Role")
    my.asserter.assert_equal(role_select.text, "Subscriber",  "Selected Role Text")

    role_select.select_value("editor")
    role_select.select_index(4)
    role_select.text = "Subscriber"
```

#### Points to Note
1. To create an object of a DropDown, we use the `dropdown` factory method of the `WebApp`.
2. We can select an option by its visible text by calling `select_text` method of DropDown.
3. DropDown provides various enquiry methods - `has_visible_text_selected`, ``has_value_selected`, has_index_selected`.
4. DropDown also has enquirable properties - `value` and `text`.
5. We assert using `my.asserter`'s appropriate assertion methods.
6. There are other ways of selection as well - `select_value` to select by value attribute of an option, `select_index` to select an option present at provided index.
7. DropDown also has a way of selecting an option by setting its `text` property. This is similar to `.text` property setting of a text-box. It is different from `select_text` method in terms of implementation. `select_text` uses DOM inquiry to match the text of an option and then clicks it to select it. Setting the `.text` property similuates the user action where the user types a string in a focused/highlighted select control to select an option (in technical terms it is equivalent of sendkeys).
