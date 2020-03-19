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

  user:
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
    template: dropdown
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

'''
This file is a part of Arjuna
Copyright 2015-2020 Rahul Verma

Website: www.RahulVerma.net

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from arjuna import *

class WordPress(WebApp):

    def __init__(self):
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


class WPFullPage(WPBasePage, metaclass=abc.ABCMeta):

    def __init__(self, source_gui):
        super().__init__(source_gui=source_gui)

    @property
    def top_nav(self):
        return TopNav(self)

    @property
    def left_nav(self):
        return LeftNav(self)
```

#### Points to Note
1. `WPBase` is the base class without sections.
2. `WPFullPage` has `top_nav` and `left_nav` sections available as properties.


 **Home Page**

 ```python
 # arjuna-samples/arjex_app_page_widget/lib/gom/pages/home.py
 

from arjuna import *
from enum import Enum, auto
from .base import WPBasePage

class Home(WPBasePage):

    def login(self, user, pwd):
        self.gns.user.text = user
        self.gns.pwd.text = pwd
        self.gns.submit.click()

        from .dashboard import Dashboard
        return Dashboard(self)

    def login_with_default_creds(self):
        user = C("wp.admin.name")
        pwd = C("wp.admin.pwd")

        return self.login(user, pwd)
```

#### Points to Note
1. Inherits from `WPBasePage` (No sections).
2. Rest is same code.

 **Dashboard Page**

 ```python
 # arjuna-samples/arjex_app_page_widget/lib/gom/pages/dashboard.py

from .base import WPFullPage

class Dashboard(WPFullPage):
    pass
```

#### Points to Note
1. Inherits from `WPFullPage` and hence has the `top_nav` and `left_nav` sections.
2. Does not have `go_to_settings` method anymore.

 **Settings Page**

 ```python
 # arjuna-samples/arjex_app_page_widget/lib/gom/pages/settings.py
 
from .base import WPFullPage

class Settings(WPFullPage):

    def tweak_role_value(self, value):
        role_select = self.gns.role
        role_select.select_value(value)
        self.asserter.assert_true(role_select.has_value_selected(value), "Selection of {} as Role".format(value))
        return self
```

#### Points to Note
1. Inherits from `WPFullPage` and hence has the `top_nav` and `left_nav` sections.

**Base Section**

 ```python
 # arjuna-samples/arjex_app_page_widget/lib/gom/pages/sections/base.py
 
import abc
from arjuna import Section

class WPBaseSection(Section, metaclass=abc.ABCMeta):

    def __init__(self, page):
        super().__init__(page, gns_dir="sections")
```

#### Points to Note
1. Inherits from Arjuna's `WSectionidget` class and is implemented as abstract class.
2. Needs to be passed an instance of the parent `Page`.
3. We have placed the widget related GNS files in `sections` sub-directory of `namespace` directory. So, it passes the name of the sub-directory in the call to `__init__` as `gns_dir` keyword argument.


**LeftNav Section**

 ```python
 # arjuna-samples/arjex_app_page_widget/lib/gom/pages/sections/leftnav.py

from arjuna import *
from .base import WPBaseSection

class LeftNav(WPBaseSection):

    def __init__(self, page):
        super().__init__(page)

    @property
    def settings_page(self):
        from arjex.lib.app_page_section.pages.settings import Settings
        self.gns.settings.click()
        return Settings(self)
```

#### Points to Note
1. Inherits from `WPBaseSection`.
2. The `go_to_settings` method is moved from `Dashboard` page to here for accurate representation of Gui.

**TopNav Section**

 ```python
 # arjuna-samples/arjex_app_page_widget/lib/gom/pages/sections/topnav.py

from arjuna import *
from .base import WPBaseSection

class TopNav(WPBaseSection):

    def logout(self):
        url = C("wp.logout.url")
        self.go_to_url(url)

        self.gns.logout_confirm.click()
        self.gns.logout_msg

        from arjex.lib.app_page_section.pages.home import Home
        return Home(self)
```

#### Points to Note
1. Inherits from `WPBaseSection`.
2. The `logout` method is moved from `WPBasePage` page to here for accurate representation of Gui.

#### Using the App-Page-Section Model in Test Code

```python
# arjuna-samples/arjex_app_page_widget/test/module/check_01_app_page_section_model.py

from arjuna import *
from arjex.lib.gom.app import WordPress

@for_test
def settings(request):
    # Setup
    wordpress = WordPress()
    home = wordpress.launch()
    dashboard = home.login_with_default_creds()
    settings = dashboard.left_nav.settings_page
    yield settings

    # Teadown
    settings.top_nav.logout()

@test
def check_with_wp_app_page_section(request, settings):
    settings.tweak_role_value("editor")
```

##### Points to Note
1. With this modularity, we are no more dependent on Dashboard page for logging out. As per the template structure, just like the Gui of WordPress, this method is available in `TopNav` section which in turn is available to a page which is `WPFullPage` (inherits from it).
2. The test's actual need is the `Settings` page. We have changed the test fixture name to `settings`.
3. In the setup part, we create the WordPress instance as earlier, it now refers to the new class that we created.
3. `wordpress.launch` launches the web application (opens browser and goes to the `base_url`). It returns the `Home` object.
4. We login with default credentials using `home.login_with_default_creds()` call. It returns `Dashboard` object.
5. We go to settings by using `left_nav` section of `dashboard`: `dashboard.left_nav.settings_page`.
5. In the teardown part of fixture, we logout using `top_nav` section of `settings`: `settings.top_nav.logout()`.
6. In the test, the argument is changed from `dashboard` to `settings`.
7. `settings.tweak_role_value("editor")` is now  direct call to the settings object.
8. So far, from test and Gui abstraction perspective, this is the most accurate representation of the Gui as well as the most intuitive version of the test automation code. We can do even better with more advanced features of Arjuna discussed elsewhere.
