### Arjuna's App-Page-Section Model for Gui Abstraction

Consider the following before going into the technicalities of the model:
1. Typcally, the web applications follow a set of a templates for different pages. Such templates have some repetitive sections across multiple pages. Examples: Left navigation bars, Top Menus, Sidebars etc.
2. Some application pages might be two complex to be represented as a single page.
3. Some similar HTML components like tables etc. are resued across multiple pages as a part of their contents.

Unless we address the above in the way we implement the Gui abstraction, the code will not clearly represent the Gui. Also, even if externalized, this could result in repeated identifiers across different GNS files.

One step forward from Arjuna's App-Page Model is the App-Page-Section Model:
1. We implement the web application as a child of `WebApp`class.
2. We implemented each web page of interest as a child of `Page` class.
3. Pages inherit from different template base pages to represent common structures.
4. Reusables page portions are implemented as `Sections` and a correct composition relationship is established between a `Page` and its `Sections` using OOP.
5. In short, Apps have pages and a page can have sections.

There is another change which is optional but suggested which we are going to do - rather than using strings for element labels, we are going to implement an `Enum` in each `Page/Section` class. This goes a long way in eliminating typing errors in the code.

We will create 2 types of base pages:
1. WPBasePage - A base page **without** top and left navigation sections.
2. WPFullPage - A base page **with** top and left navigation sections.

We will create 2 types of sections:
1. LeftNav - A section representing left navigation sidebar in WordPress.
2. TopNav - A section representing top navigation bar.

We are going to create the retain 3 pages, but implement inheritance as follows to represent the strucutre:
1. Home (a child of WPBasePage)
2. Dashboard (a child of WPFullPage)
3. Settings (a child of WPFullPage)

You can find the example code and files used on this section in [arjuna_app_page_widget project](https://github.com/rahul-verma/arjuna//tree/master/arjuna-samples/arjex_app_page_widget).

You will see that this approach is the most involved than the previous approaches discussed so far. Professional test automation code is more than exercise/raw code seen on the web. This is a step in the right direction, in case you are dealing with test automation of medium to high complexity apps.

#### The GNS Files

In `App-Page Model` we had put identifiers in page-wise GNS files. The challenge was where to put the identifiers corresponding to page areas common across pages. Now, we have the solution. We put them in corresponding section GNS files. Specifically, compare the flawed GNS file for Dashaboard with this new approach.

Page: **Home.yaml**

```YAML
labels:

  login:
    id: user_login

  pwd:
    id: user_pass

  submit:
    id: wp-submit
```

Page: **Dashbaord.yaml**

```YAML
labels:

  view_site:
    classes: welcome-view-site
```

Page: **Settings.yaml**

```YAML
labels:

  role:
    id: default_role
```

Section: **LeftNav.yaml**

```YAML
labels:

  settings:
    link: Settings
```

Section: **TopNav.yaml**

```YAML
labels:

  logout_confirm:
    link: log out

  logout_msg:
    text: logged out
```

#### The Model Classes for App, Pages and Sections

**WebApp**

```python
# arjuna-samples/arjex_app_page_widget/lib/gom/app.py

from arjuna import *

class WordPress(WebApp):

    def __init__(self, gns_format="sgns"):
        url = C("wp.login.url")
        super().__init__(base_url=url)

    def launch(self):
        super().launch()

        from .pages.home import Home
        return Home(self)
 ```
 
#### Points to Note
1. Same code as App-Page Model.
 
 **Base Pages**

 ```python
 # arjuna-samples/arjex_app_page_widget/lib/gom/pages/base.py
 
import abc
from arjuna import Page

from .sections.topnav import TopNav
from .sections.leftnav import LeftNav


class WPBasePage(Page, metaclass=abc.ABCMeta):

    def __init__(self, source_gui):
        super().__init__(source_gui=source_gui)

    def prepare(self):
        self.externalize()


class WPFullPage(WPBasePage, metaclass=abc.ABCMeta):

    def __init__(self, source_gui):
        super().__init__(source_gui=source_gui)
        self.__top_nav = TopNav(self)
        self.__left_nav = LeftNav(self)

    @property
    def top_nav(self):
        return self.__top_nav

    @property
    def left_nav(self):
        return self.__left_nav
```

#### Points to Note
1. `WPBase` is the base class without sections.
2. `WPFullPage` has `top_nav` and `left_nav` sections available as properties.


 **Home Page**

 ```python
 # arjuna-samples/arjex_app_page_widget/lib/gom/pages/home.py
 
from enum import Enum, auto
from .base import WPBasePage

class Home(WPBasePage):

    class labels(Enum):
        login = auto()
        pwd = auto()
        submit = auto()

    def validate_readiness(self):
        self.element(self.labels.submit).wait_until_visible()

    def login(self, user, pwd):
        self.element(self.labels.login).text = user
        self.element(self.labels.pwd).text = pwd
        self.element(self.labels.submit).click()

        from .dashboard import Dashboard
        return Dashboard(self)

    def login_with_default_creds(self):
        user = self.config.user_options.value("wp.admin.name")
        pwd = self.config.user_options.value("wp.admin.pwd")

        return self.login(user, pwd)
```

#### Points to Note
1. Inherits from `WPBasePage` (No widgets).
2. Implements inner class `labels` to represent externalized identifier labels as enum constants.
3. Rest is same code.

 **Dashboard Page**

 ```python
 # arjuna-samples/arjex_app_page_widget/lib/gom/pages/dashboard.py
 
from enum import Enum, auto
from .base import WPFullPage

class Dashboard(WPFullPage):

    class labels(Enum):
        view_site = auto()

    def validate_readiness(self):
        self.element(self.labels.view_site).wait_until_visible()
```

#### Points to Note
1. Inherits from `WPFullPage` and hence has the `top_nav` and `left_nav` widget properties.
2. Does not have `settings` property anymore.
3. Implements `labels` as discussed for Home page.

 **Settings Page**

 ```python
 # arjuna-samples/arjex_app_page_widget/lib/gom/pages/settings.py
 
from enum import Enum, auto
from .base import WPBasePage

class Settings(WPFullPage):

    class labels(Enum):
        role = auto()

    def validate_readiness(self):
        self.element(self.labels.role).wait_until_visible()

    def tweak_role_value(self, value):
        role_select = self.dropdown(self.labels.role)
        role_select.select_value(value)
        self.asserter.assert_true(role_select.has_value_selected(value), "Selection of {} as Role".format(value))
        return self
```

#### Points to Note
1. Inherits from `WPFullPage` and hence has the `top_nav` and `left_nav` section properties.
3. Implements `labels` as discussed for Home page.

**Base Section**

 ```python
 # arjuna-samples/arjex_app_page_widget/lib/gom/pages/sections/base.py
 
import abc
from arjuna import Widget

class WPBaseSection(Widget, metaclass=abc.ABCMeta):

    def __init__(self, page):
        super().__init__(page)

    def prepare(self):
        self.externalize(gns_dir="widgets")
```

#### Points to Note
1. Inherits from Arjuna's `Widget` class and is implemented as abstract class.
2. Needs to be passed an instance of the parent `Page`.
3. We have placed the widget related GNS files in `sections` subdirectory of `namespace` directory. So, it passes the name of the sub-directory in the call to `externalize`.


**LeftNav Section**

 ```python
 # arjuna-samples/arjex_app_page_widget/lib/gom/pages/sections/leftnav.py
 
from enum import Enum, auto
from .base import WPBaseWidget

class LeftNav(WPBaseWidget):

    class labels(Enum):
        settings = auto()

    def validate_readiness(self):
        self.element(self.labels.settings)

    @property
    def settings(self):
        from arjex_app_page_widget.lib.gom.pages.settings import Settings
        self.element(self.labels.settings).click()
        return Settings(self)
```

#### Points to Note
1. Inherits from `WPBaseWidget`.
2. Implements `labels` as discussed for Home page.
3. The `settings` proerty is moved from `Dashboard` page to here for accurate representation of Gui.

**TopNav Section**

 ```python
 # arjuna-samples/arjex_app_page_widget/lib/gom/pages/sections/topnav.py
 
from enum import Enum, auto
from .base import WPBaseWidget

class TopNav(WPBaseWidget):

    class labels(Enum):
        logout_confirm = auto()
        logout_msg = auto()

    def logout(self):
        url = self.config.user_options.value("wp.logout.url")
        self.go_to_url(url)

        self.element(self.labels.logout_confirm).click()
        self.element(self.labels.logout_msg).wait_until_visible()

        from arjex_app_page_widget.lib.gom.pages.home import Home
        return Home(self)
```

#### Points to Note
1. Inherits from `WPBaseWidget`.
2. Implements `labels` as discussed for Home page.
3. The `logout` method is moved from `WPBasePage` page to here for accurate representation of Gui.

#### Using the App-Page-Widget Model in Test Code

```python
# arjuna-samples/arjex_app_page_widget/test/module/check_01_app_page_widget_model.py

from arjuna import *
from arjex_app_page_widget.lib.gom.app import WordPress

@for_test
def settings(request):
    # Setup
    wordpress = WordPress()
    home = wordpress.launch()
    dashboard = home.login_with_default_creds()
    settings = dashboard.left_nav.settings
    yield settings

    # Teadown
    settings.top_nav.logout()

@test
def check_with_wp_app_page_widget(request, settings):
    settings.tweak_role_value("editor")
```

##### Points to Note
1. With this modularity, we are no more dependent on Dashboard page for logging out. As per the template structure, just like the Gui of WordPress, this method is available in `TopNav` section which in turn is available to a page which is `WPFullPage` (inherits from it).
2. The test's actual need is the `Settings` page. We have changed the test fixture name to `settings`.
3. In the setup part, we create the WordPress instance as earlier, it now refers to the new class that we created.
3. `wordpress.launch` launches the web application (opens browser and goes to the `base_url`). It returns the `Home` object.
4. We login with default credentials using `home.login_with_default_creds()` call. It returns `Dashboard` object.
5. We go to settings by using `left_nav` section of `dashboard`: `dashboard.left_nav.settings`.
5. In the teardown part of fixture, we logout using `top_nav` section of `settings`: `settings.top_nav.logout`.
6. In the test, the argument is changed from `dashboard` to `settings`.
7. `settings.tweak_role_value("editor")` is now  direct call to the settings object.
8. From test and Gui abstraction perspective, this is the most accurate representation of the Gui as well as the most intuitive version of the test automation code.
