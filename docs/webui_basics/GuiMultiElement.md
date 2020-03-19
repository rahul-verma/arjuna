### Matching Multiple Elements as GuiMultiElement

Arjuna provides a special abstraction for representing mutliple ```GuiElement```s together rather than a raw Python list. This provides an opportunity to include higher level methods for test code authors.

#### Test Fixture for Examples in This Page

We are going to use a test-level fixture for the examples.

Below is the `@for_test` fixture code to get logged-in WordPress for a test using the reusable module that we created in the last section. We place it in the `project.lib.fixture.test` module so that it can be used for a any test. 

```python
# arjuna-samples/arjex/lib/fixture/test.py

from arjuna import *
from arjex.lib.wp import WordPress

@for_test
def logged_in_wordpress(request):
    # Setup
    wordpress = create_wordpress_app()
    login(wordpress)
    yield wordpress

    # Teadown
    logout(wordpress)
```

#### Important point for GNS

The following entry in `WordPress.yaml` is of interest:

```YAML
  cat_checkboxes:
    template: multi_element
    name: "delete_tags[]"
```

##### Points to Note
1. To instruct Arjuna to treat an element as a multiple element, under the label entry in GNS file, you can mention `template: multi_element`.

#### Test Code

```python
# arjuna-samples/arjex/test/module/check_09_gui_multielement.py

from arjuna import *

@test
def check_multielement(request, logged_in_wordpress):
    wordpress = logged_in_wordpress
    wordpress.gns.posts.click()
    wordpress.gns.categories.click()

    check_boxes = wordpress.gns.cat_checkboxes
    check_boxes[1].check()
    check_boxes[1].uncheck()
    check_boxes.first_element.uncheck()
    check_boxes.last_element.uncheck()
    check_boxes.random_element.uncheck()
```

##### Points to Note
1. The creation code is same as that for a single element.
3. `GuiMultiElement` supports index based retrieval just like a regular list. Indexes start from computer counting (0).
4. In addition to this, it provides methods like `first_element`, `last_element` and `random_element`.
5. It provides more features that we will cover in advanced section of this tutorial. It also forms the basis of Arjuna's DropDown and RadioGroup abstractions which we cover in next sections.
