### Creating a Self-Contained App

Python is an OOP language. OOP simplifies API signatures and some of the best of the features of Python can be explored only with OOP.

Please note that this is not the suggested implementation. Consider this as an interim implementation, a step towards the right one. We'll explore the suggested way in the next section.

#### The GNS File

We will use the same GNS file as the previous section.

#### The App Class Code

```python
# arjuna-samples/arjex_app/lib/wp_app.py

from arjuna import *

class WordPress:

    def __init__(self):
        url = Arjuna.get_ref_config().get_user_option_value("wp.login.url").as_str()
        self.__app = WebApp(base_url=url)
        self.app.launch()
        self.app.externalize(gns_file_name="WordPress.gns")

    @property
    def app(self):
        return self.__app

    def login(self):
        user = self.app.config.get_user_option_value("wp.admin.name").as_str()
        pwd = self.app.config.get_user_option_value("wp.admin.pwd").as_str()

        # Login
        self.app.element("login").text = user
        self.app.element("pwd").text = pwd
        self.app.element("submit").click()
        self.app.element("view_site")

    def logout(self):
        url = self.app.config.get_user_option_value("wp.logout.url").as_str()
        self.app.go_to_url(url)
        self.app.element("logout_confirm").click()
        self.app.element("logout_msg")

        self.app.quit()

```

#### Points to Note
1. The code is a basic restructuring of the procedural style of code, written in the previous section into the WordPress class.
2. The functionality `create_wordpress_app` function is now dealt in the `__init__` method and will be triggered when you create an object of `WordPress` class.
3. This is an example of a `Wrapper` object, which wraps another object (in other words, it is a `HAS-A` or `Composition` relationship). The `WordPress` class wraps the `WebApp` class which is available in the code as `self.app` because we set it as a property with the `@property` decorator of Python.
4. `login` and `logout` are bound methods and hence you dont need to supply the wordpress app as the argument, thereby simplying the call signatures.
5. In the methods, `WordPress` code makes calls to the `WebApp` object to achieve its functionality.

#### Using the App Class in Test Code

```python
# arjuna-samples/arjex_app/tests/modules/test_02_app.py

from arjuna import *
from arjex_app.lib.wp_app import WordPress

@for_test
def wordpress(request):
    # Setup
    wordpress = WordPress()
    wordpress.login()
    yield wordpress

    # Teadown
    wordpress.logout()

@test
def test_with_wp_app_interim(my, request, wordpress):
    wordpress.app.element("Settings").click()
    role_select = wordpress.app.dropdown("role")
    role_select.select_value("editor")
    my.asserter.assert_true(role_select.has_value_selected("editor"), "Selection of editor as Role")
```

##### Points to Note
1. In the test fixture, we instantiate the `WordPress` class, call its `login` method and yield the object so that test can receive it. In its teardown section (after the `yield`), we call the `logout` method of `wordpress` object.
2. The fixture is mentioned as an argument of the test function.
3. In the test function we can call any of its methods as seen above. The `app` property is public, so it can be used in the test code as `wordpresss.app`

