### Arjuna's App-Page Model for Gui Abstraction

For professional test automation, where you automate multiple use cases across different pages/screens, a simple App Model will not suffice. In the simple App Model, the GNS file will be cluttered with labels from multiple pages and the `WebApp` class will have so many methods that it will impact code mainteance and understandability.

One step forward from Arjuna's App Model is the App-Page Model:
1. We implement the web application as a child of `WebApp`class.
2. We implemented each web page of interest as a child of `Page` class.
3. The `Page` classes have methods to move from one page to another. 

We are going to create the following 3 pages:
1. Home
2. Dashboard
3. Settings

You can find the example code and files used on this section in [arjuna_app_page project](https://github.com/rahul-verma/arjuna//tree/master/arjuna-samples/arjex_app_page).

#### The GNS Files

So far we represented the complete application as a single `WebApp` and hence all identifiers were put in a single `GNS` file. Now, we put them in page-wise GNS files:

**Home.gns**
```INI
[login]
id = user_login

[pwd]
id = user_pass

[submit]
id = wp-submit
```

**Dashbaord.gns**

```INI
[view_site]
classes = welcome-view-site

[settings]
link = Settings
```

**Settings.gns**

```INI
[role]
id = default_role

[logout_confirm]
link = log out

[logout_msg]
text = logged out
```

Please note that the above is not an accurate representation of screens. The logout related confirmation link and success messages are not on settings screen. For simplicity of example, it has been done like this for now.

#### The Model Classes for App and Pages

**WebApp**

```python
# arjuna-samples/arjex_app_page/lib/gom/app.py

from arjuna import *

class WordPress(WebApp):

    def __init__(self, gns_format="sgns"):
        url = Arjuna.get_ref_config().get_user_option_value("wp.login.url").as_str()
        super().__init__(base_url=url)

    def launch(self):
        super().launch()

        from .pages.home import Home
        return Home(self)
 ```
 
 **Base Page**

 ```python
 # arjuna-samples/arjex_app_page/lib/gom/pages/base.py
 
from arjuna import *

class WordPress(WebApp):

    def __init__(self, gns_format="sgns"):
        url = Arjuna.get_ref_config().get_user_option_value("wp.login.url").as_str()
        super().__init__(base_url=url)

    def launch(self):
        super().launch()

        from .pages.home import Home
        return Home(self)
```


 **Home Page**

 ```python
 # arjuna-samples/arjex_app_page/lib/gom/pages/home.py
 
from .base import WPBasePage

class Home(WPBasePage):

    def validate_readiness(self):
        self.element("submit").wait_until_visible()

    def login(self, user, pwd):
        self.element("login").text = user
        self.element("pwd").text = pwd
        self.element("submit").click()

        from .dashboard import Dashboard
        return Dashboard(self)

    def login_with_default_creds(self):
        user = self.config.get_user_option_value("wp.admin.name").as_str()
        pwd = self.config.get_user_option_value("wp.admin.pwd").as_str()

        return self.login(user, pwd)
```

 **Dashboard Page**

 ```python
 # arjuna-samples/arjex_app_page/lib/gom/pages/dashboard.py
 
from .base import WPBasePage

class Dashboard(WPBasePage):

    def validate_readiness(self):
        print("dfkghdkjghdfghk")
        self.element("view_site").wait_until_visible()

    @property
    def settings(self):
        self.element("settings").click()

        from .settings import Settings
        return Settings(self)
```

 **Settings Page**

 ```python
 # arjuna-samples/arjex_app_page/lib/gom/pages/settings.py
 
from .base import WPBasePage

class Settings(WPBasePage):

    def validate_readiness(self):
        self.element("role").wait_until_visible()

    def tweak_role_value(self, value):
        role_select = self.dropdown("role")
        role_select.select_value(value)
        self.asserter.assert_true(role_select.has_value_selected(value), "Selection of {} as Role".format(value))

```

#### Points to Note
1. Rather than a composition relationship with `WebApp` object in previous example, the `WordPress` class inherits from `WebApp` class.
2. This means all `WebApp` methods are directly callable by `WordPress` as now `WordPress` **IS** `WebApp`.
3. `self.app.element`, for example, now becomes `self.element`, thereby simplifying the code.
4. Rest of the code is exactly like earlier example code.


#### Using the App-Page Model in Test Code

```python
# arjuna-samples/arjex_app_page/tests/modules/test_01_app_page_model.py

from arjuna import *
from arjex_app_page.lib.gom.app import WordPress

@for_test
def dashboard(request):
    # Setup
    wordpress = WordPress()
    home = wordpress.launch()
    dashboard = home.login_with_default_creds()
    yield dashboard

    # Teadown
    dashboard.logout()

@test
def test_with_wp_app_page(my, request, dashboard):
    dashboard.settings.tweak_role_value("editor")
```

##### Points to Note
1. The code is exactly the same code as the previous example, but makes use of the new WordPress class that we created.
