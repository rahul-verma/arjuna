### Gui Namespace - Externalizing Identifiers

Externalizing of identifiers of `With` based identifiers is built into Arjuna. So, you don't have to go for a completely different model (e.g. Page Factories) in case your purpose is just to externlize your identification in external files.

You can find the example code and files used on this section in [arjuna_app project](https://github.com/rahul-verma/arjuna//tree/master/arjuna-samples/arjex_app).

Here, we will explore a simple example. Let's have a look:

#### The GNS File

Arjuna has a customized externalization format for getting started easily with externalization of identifiers. Such a file looks very similar to an `INI` or `CONFIG` files, but has advanced features which we will discuss in some future sections.

Location for the following file is `arjuna-samples/arjex_app/guiauto/namespace/WordPress.gns`

```INI
[login]
id = user_login

[pwd]
id = user_pass

[submit]
id = wp-submit

[view_site]
classes = welcome-view-site

[logout_confirm]
link = log out

[logout_msg]
text = logged out

[settings]
link = Settings

[role]
id = default_role
```

##### Points to note
1. This file has a `GNS` extension.
2. The file contains various sections marked with a heading `[name]`.
3. The content of the heading is a valid Python name and is the `label` for a visual element in GUI.
4. The section content has the identifier without the `With` reference. For example, `WithType.ID` is mentioned just `id`.
5. The value of an identifier is mentioned as a normal assigment without the the double quotes.
6. All of the `WithType` identifiers (or corresponding `With`'s factory methods) can be be accomodated in the `GNS` file.

#### The Reusable Module Modified to Accomodate GNS

We had earlier created a resuable module for WordPress related functions. Let's see a modified version of it as per the externalization approach:

```python
# arjuna-samples/arjex_app/lib/wp_gns.py

from arjuna import *

def create_wordpress_app():
    url = Arjuna.get_ref_config().get_user_option_value("wp.login.url").as_str()
    wordpress = WebApp(base_url=url)
    wordpress.launch()
    wordpress.externalize(gns_file_name="WordPress.gns")
    return wordpress

def login(wordpress):
    user = wordpress.config.get_user_option_value("wp.admin.name").as_str()
    pwd = wordpress.config.get_user_option_value("wp.admin.pwd").as_str()

    # Login
    wordpress.element("login").text = user
    wordpress.element("pwd").text = pwd
    wordpress.element("submit").click()
    wordpress.element("view_site")

def logout(wordpress):
    url = wordpress.config.get_user_option_value("wp.logout.url").as_str()
    wordpress.go_to_url(url)
    wordpress.element("logout_confirm").click()
    wordpress.element("logout_msg")

    wordpress.quit()


def tweat_role_value_in_settings(wordpress, asserter, value):
    wordpress.element("Settings").click()
    role_select = wordpress.dropdown("role")
    role_select.select_value(value)
    asserter.assert_true(role_select.has_value_selected(value), "Selection of {} as Role".format(value))

```

##### Points to Note
1. The module is structurally very similar to earlier code. Same function signatures are used.
2. `WebApp` is created and launched exactly the same way as earlier. One key change is that we make **`externalize`** call for the `WebApp`. 
3. **`wordpress.externalize(gns_file_name="WordPress.gns")`** invokes the externalization logic and locates the GNS file automatically in the test project's namespace directory: `arjuna-samples/arjex_app/guiauto/namespace`.
4. Other key change is that now the `element` factory call is supplied the `label` from the GNS file. So, `wordpress.element(With.id("user_login")` becomes `wordpress.element("login")`.
5. Labels are treated as **case-insensitive** by Arjuna. 
6. We have implemented an additional method `tweat_role_value_in_settings` to change the user role on settings page to a chosen value. It takes 3 arguments - the web app, the asserter and the value for the role to be selected.
7. Rest of the code is exactly the same. It means you can move to an externalization approach in Arjuna very easily with or without creating a full fledged Page object model like most other implementations.

#### Using the Module in Test Code

```python
# arjuna-samples/arjex_app/tests/modules/test_01_gns.py

from arjuna import *
from arjex_app.lib.wp_gns import *

@for_test
def wordpress(request):
    # Setup
    wordpress = create_wordpress_app()
    login(wordpress)
    yield wordpress

    # Teadown
    logout(wordpress)

@test
def test_with_wp_gns(my, request, wordpress):
    tweat_role_value_in_settings(wordpress, my.asserter, "editor")
```

##### Points to Note
1. In the test fixture, we create the `WebApp` representing WordPress by calling `create_wordpress_app` function from the module that we created. Then, we call the `login` function and yield the `WebApp` object so that test can receive it. In its teardown section (after the `yield`), we call the `logout` function of `wordpress` module.
2. The fixture is mentioned as an argument of the test function.
3. In the test function, we call the tweat_role_value_in_settings, and pass the appropriate 3 arguments expected by the call.


