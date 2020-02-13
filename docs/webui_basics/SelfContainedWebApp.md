### Creating a Self-Contained App

#### The App Code

```python
# arjuna-samples/arjex_webui_basics/lib/wp.py

from arjuna import *

class WordPress(WebApp):

    def __init__(self):
        url = Arjuna.get_ref_config().get_user_option_value("wp.login.url").as_str()
        super().__init__(base_url=url)
        self.launch()

    def login(self):
        user = self.config.get_user_option_value("wp.admin.name").as_str()
        pwd = self.config.get_user_option_value("wp.admin.pwd").as_str()

        # Login
        self.element(With.id("user_login")).text = user
        self.element(With.id("user_pass")).text = pwd
        self.element(With.id("wp-submit")).click()
        self.element(With.classes("welcome-view-site"))

    def logout(self):
        url = self.config.get_user_option_value("wp.logout.url").as_str()
        self.go_to_url(url)
        self.element(With.link("log out")).click()
        self.element(With.text("logged out"))

        self.quit()
```

#### Points to Note
1. We are placing this class as in a module inside `lib` directory of your project. When Arjuna loads, it injects the parent directory of your project into PYTHONPATH. It means any packages/modules that you place in your project can be easily imported in your tests. This class can now be imported as `from <your_prj_name>.lib.wp import WordPress`.
2. The class inherits from WebApp.
3. In its `__init__` method we do a `super().__init__` call and provide the `base_url`. We launch the app here itself to avoid a separate call.
4. It has two methods `login` and `logout` which represent functionality specific to our app.
5. As app can reference its own attributes, we use `self.launch`, `self.element`, `self.quit` calls.
6. All the code here is taken from the previous GuiElement interaction example.

#### Using the App in Test Code

```python
# arjuna-samples/arjex_webui_basics/tests/modules/test_03_wordpress_app.py

@test
def test_selfcontained_wp(my, request):
    wordpress = WordPress()
    wordpress.login()
    wordpress.logout()
```

The above code is basic Python. We can instantiate the `WordPress` app class that we created and call its methods.

