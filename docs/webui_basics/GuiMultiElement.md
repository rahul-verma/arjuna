### GuiMultiElement

Arjuna provides a special abstraction for representing mutliple ```GuiElement```s together rather than a raw Python list. This provides an opportunity to include higher level methods for test code authors.

#### Test Fixture for Examples in This Page

We are going to use a test-level fixture for the examples.

Below is the `@for_test` fixture code to get logged-in WordPress for a test using the reusable module that we created in the last section:

```python
# arjuna-samples/arjex_webui_basics/tests/modules/check_04_gui_multielement.py

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

#### Test Code

```python
# arjuna-samples/arjex_webui_basics/tests/modules/check_04_gui_multielement.py

@test
def check_multielement(request, wordpress):
    wordpress.element(With.link("Posts")).click()
    wordpress.element(With.link("Categories")).click()

    check_boxes = wordpress.multi_element(With.name("delete_tags[]"))
    check_boxes[1].check()
    check_boxes[1].uncheck()
    check_boxes.first_element.uncheck()
    check_boxes.last_element.uncheck()
    check_boxes.random_element.uncheck()
```

##### Points to Note
1. The factory method to create a `GuiMultiElement` is `multi_element`.
2. All identification strategies that work for `GuiElement` also work for `GuiMultiElement`.
3. It supports index based retrieval just like a regular list. Indexes start from computer counting (0).
4. In addition to this, it provides methods like `first_element`, `last_element` and `random_element`.
5. It provides more features that we will cover in advanced section of this tutorial. It also forms the basis of Arjuna's DropDown and RadioGroup abstractions which we cover in next chapter.
