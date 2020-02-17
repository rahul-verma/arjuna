### Arjuna's App Model for Gui Abstraction

In this section, we discuss the App Model of Gui Abstraction.

We can implement a class as a `WebApp` by using inheritance. This is the suggested way of implenting a web application abstraction in Arjuna. 

This is the simplest way to get started with an equivalent of Page Object Model (POM), Page Factories, Loadable Component, all clubbed into one concept. We represent the complete appplication as a single class which is attached to a a single GNS file for externalization. It should work well for small apps or where you are automating only a small sub-set of the application. 

#### The GNS File

We will use the same GNS file as the previous section.

#### The App Model Class Code

```python
# arjuna-samples/arjex_app/lib/wp_app_model.py

from arjuna import *

class WordPress(WebApp):

    def __init__(self):
        url = Arjuna.get_ref_config().get_user_option_value("wp.login.url").as_str()
        super().__init__(base_url=url)
        self.launch()
        self.externalize()

    def login(self):
        user = self.config.get_user_option_value("wp.admin.name").as_str()
        pwd = self.config.get_user_option_value("wp.admin.pwd").as_str()

        # Login
        self.element("login").text = user
        self.element("pwd").text = pwd
        self.element("submit").click()
        self.element("view_site")

    def logout(self):
        url = self.config.get_user_option_value("wp.logout.url").as_str()
        self.go_to_url(url)
        self.element("logout_confirm").click()
        self.element("logout_msg")

        self.quit()
```

#### Points to Note
1. Rather than a composition relationship with `WebApp` object in previous example, the `WordPress` class inherits from `WebApp` class.
2. This means all `WebApp` methods are directly callable by `WordPress` as now `WordPress` **IS** `WebApp`.
3. `self.app.element`, for example, now becomes `self.element`, thereby simplifying the code.
4. Rest of the code is exactly like earlier example code.


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
