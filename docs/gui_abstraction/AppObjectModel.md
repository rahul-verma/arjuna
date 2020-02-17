### Creating a Self-Contained App

Python is an OOP language. OOP simplifies API signatures and some of the best of the features of Python can be explored only with OOP.

Please note that this is not the suggested implementation. Consider this as an interim implementation, a step towards the right one. We'll explore the suggested way in the next section.

#### The GNS File

We will use the same GNS file as the previous section.

#### The App Class Code

```python
# arjuna-samples/arjex_app/lib/wp_app_model.py


```

#### Points to Note
1. The code is a basic restructuring of the procedural style of code, written in the previous section into the WordPress class.
2. The functionality `create_wordpress_app` function is now dealt in the `__init__` method and will be triggered when you create an object of `WordPress` class.
3. This is an example of a `Wrapper` object, which wraps another object (in other words, it is a `HAS-A` or `Composition` relationship). The `WordPress` class wraps the `WebApp` class which is available in the code as `self.app` because we set it as a property with the `@property` decorator of Python.
4. `login` and `logout` are bound methods and hence you dont need to supply the wordpress app as the argument, thereby simplying the call signatures.
5. In the methods, `WordPress` code makes calls to the `WebApp` object to achieve its functionality.

#### Using the App Class in Test Code

```python
# arjuna-samples/arjex_app/tests/modules/test_03_app_model.py


from arjuna import *
from arjex_app.lib.wp_app_model import WordPress

@for_test
def wordpress(request):
    # Setup
    wordpress = WordPress()
    wordpress.login()
    yield wordpress

    # Teadown
    wordpress.logout()

@test
def test_with_wp_app_model(my, request, wordpress):
    wordpress.element("Settings").click()
    role_select = wordpress.dropdown("role")
    role_select.select_value("editor")
    my.asserter.assert_true(role_select.has_value_selected("editor"), "Selection of editor as Role")
```

##### Points to Note
1. The code is exactly the same code as the previous example, but makes use of the new WordPress class that we created.