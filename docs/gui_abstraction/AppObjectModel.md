### Arjuna's App Model for Gui Abstraction

In this section, we discuss the App Model of Gui Abstraction.

We can implement a class as a `WebApp` by using inheritance. This is the suggested way of implenting a web application abstraction in Arjuna. 

This is the simplest way to get started with an equivalent of Page Object Model (POM), Page Factories, Loadable Component, all clubbed into one concept. We represent the complete appplication as a single class which is attached to a a single GNS file for externalization. It should work well for small apps or where you are automating only a small sub-set of the application. 

`WebApp` is a type of `Gui` in Arjuna. So, it follows the Gui-loading mechanism of Arjuna. 

You can find the example code and files used on this section in [arjuna_app project](https://github.com/rahul-verma/arjuna//tree/master/arjuna-samples/arjex_app).

#### The GNS File

We will use the same GNS file as the previous section.

#### The App Model Class Code

```python
# arjuna-samples/arjex_app/lib/wp_app_model.py


from arjuna import *

class WordPress(WebApp):

    def __init__(self):
        url = C("wp.login.url")
        super().__init__(base_url=url)
        self.launch()

    def login(self):
        user = C("wp.admin.name")
        pwd = C("wp.admin.pwd")

        # Login
        self.gns.user.text = user
        self.gns.pwd.text = pwd
        self.gns.submit.click()
        self.gns.view_site

    def logout(self):
        url = C("wp.logout.url")
        self.go_to_url(url)
        self.gns.logout_confirm.click()
        self.gns.logout_msg

        self.quit()

    def tweak_role_value_in_settings(self, value):
        self.app.gns.settings.click()
        role_select = self.gns.role
        role_select.select_value(value)
        self.asserter.assert_true(role_select.has_value_selected(value), "Selection of {} as Role".format(value))
        return self
```

#### Points to Note
1. Rather than a composition relationship with `WebApp` object in previous example, the `WordPress` class inherits from `WebApp` class.
2. This means all `WebApp` methods are directly callable by `WordPress` as now `WordPress` **IS** `WebApp`. `self.app`, becomes just `self`, thereby simplifying the code.
3. Rest of the code is exactly like earlier example code.


#### Using the App Class in Test Code

```python
# arjuna-samples/arjex_app/test/module/check_02_app_model.py

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
def check_with_wp_app_model(request, wordpress):
    wordpress.tweak_role_value_in_settings("editor")
```

##### Points to Note
1. The code is exactly the same code as the previous example, but makes use of the new WordPress class that we created.
