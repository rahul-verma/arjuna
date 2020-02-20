### Arjuna's App-Page Model for Gui Abstraction

For professional test automation, where you automate multiple use cases across different pages/screens, a simple App Model will not suffice. In the simple App Model, the GNS file will be cluttered with labels from multiple pages and the `WebApp` class will have so many methods that it will impact code mainteance and understandability.

One step forward from Arjuna's App Model is the App-Page Model:
1. We implement the web application as a child of `WebApp`class.
2. We implemented each web page of interest as a child of `Page` class.
3. The `Page` classes have methods to move from one page to another. 

`Page` just like `WebApp` is a type of `Gui` in Arjuna. So, it follows the Gui-loading mechanis of Arjuna. 

We are going to create the following 3 pages:
1. Home
2. Dashboard
3. Settings

You can find the example code and files used on this section in [arjuna_app_page project](https://github.com/rahul-verma/arjuna//tree/master/arjuna-samples/arjex_app_page).

You will see that this approach is more involved than the previous approaches discussed so far. Professional test automation code is more than exercise/raw code seen on the web. This is a step in the right direction, in case you are dealing with test automation professionally.

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

[logout_confirm]
link = log out

[logout_msg]
text = logged out
```

**Settings.gns**

```INI
[role]
id = default_role
```

Please note that the above is not an accurate representation of screens. The logout related confirmation link and success messages are common across multiple pages (but not Home page). We'll discuss this problem in the next section with the next model in Arjuna.

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
 
#### Points to Note
1. The `WordPress` class itself is now a very simple class. It does not use externalization. That will be done at page level.
2. The `launch` method is separated from the `__init__` as it is supposed to act as a transition method to return the `Home` page. As an alternative, `home` property can be created to store the home page, however it may not be an accurate representation when the pages change beyond home page.
3. To create the instance, it passes itself as argument. Pages in Arjuna are need a `Source GUI`, which can be a `WebApp` or a `Page`.
 
 **Base Page**

 ```python
 # arjuna-samples/arjex_app_page/lib/gom/pages/base.py
 
import abc
from arjuna import Page

class WPBasePage(Page, metaclass=abc.ABCMeta):

    def __init__(self, source_gui):
        super().__init__(source_gui=source_gui)

    def prepare(self):
        self.externalize()

    def logout(self):
        url = self.config.get_user_option_value("wp.logout.url").as_str()
        self.go_to_url(url)

        self.element("logout_confirm").click()
        self.element("logout_msg").wait_until_visible()

        from .home import Home
        return Home(self)

```

#### Points to Note
1. A Base Page class will help us in placing resuable functionality across all classes inheriting from it. 
2. It inherits from Arjuna's `Page` class.
3. As it is not supposed to instantiated directly, we make it an abstract class by using Python's `abc` module.
4. `prepare` method is called by Arjuna as a part of loading the page. We place the `externalize` call here. It will automatically associate the object of a Page class with name `Xyz` with `Xyz.gns` file in the `namespace` directory.
5. The `logout` method has the usual logic used earlier. One kye difference is that now it is a page transition method. It returns the `Home` page. Notice how, a `Page` can pass itself as an argument while instantiating another `Page` class.
6. As the page transitions might refer to each other and can cause import conflicts, it is suggested that you add the import for the same, for example, `from .home import Home` only where it is needed within a method.


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

#### Points to Note
1. `validate_readiness` method is called by Arjuna as a part of its page-loading mechanism. It is an optional method, but we implement it for a proper Page class.
2. `login` returns `Dashboard` page.
3. `login_with_default_creds` logins with the admin credentials configured in `project.conf`.

 **Dashboard Page**

 ```python
 # arjuna-samples/arjex_app_page/lib/gom/pages/dashboard.py
 
from .base import WPBasePage

class Dashboard(WPBasePage):

    def validate_readiness(self):
        self.element("view_site").wait_until_visible()

    @property
    def settings(self):
        self.element("settings").click()

        from .settings import Settings
        return Settings(self)
```

#### Points to Note
1. `validate_readiness` method is implemented just like Home page.
2. Instead of a method like `go_to_settings`, we can also implement simple page transitions as Python properties. Here `settings` property implementation is an example of this style.

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
1. As tweaking of user role happens in `Settings` page, its name is simplified from `tweak_role_value_in_settings` to `tweak_role_value`.

#### Using the App-Page Model in Test Code

```python
# arjuna-samples/arjex_app_page/tests/modules/check_01_app_page_model.py

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
def check_with_wp_app_page(my, request, dashboard):
    dashboard.settings.tweak_role_value("editor")
```

##### Points to Note
1. The fixture now yields `Dashboard` object instead of app. We change the name to reflect this.
2. In the setup part, we create the WordPress instance as earlier, it now refers to the new class that we created.
3. `wordpress.launch` launches the web application (opens browser and goes to the `base_url`). It returns the `Home` object.
4. We login with default credentials using `home.login_with_default_creds()` call. It returns `Dashboard` which is then yielded.
5. In the teardown part of fixture, we logout using `dashboard.logout()` call.
6. In the test, the argument is changed from `wordpress` to `dashbaord`.
7. `dashboard.settings.tweak_role_value("editor")` gets the `settings` property of `Dashboard` object, which returns the `Settings` object and calls its `tweak_role_value` method.

