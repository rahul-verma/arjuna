### Creating Reusable Module - Separating Reusable Functions

Although not strictly a part of learning Arjuna, it is a good practice to separate reusable functions. Arjuna structurally supports it so it will be a good learning in that direction. Also, this will form the basis of more involved models in later sections.

For this section, it is more about avoiding repeated code across examples.

Here, we are following a traditional style of programming. For more advanced constructs, OOP is the key. We'll explore that in depth in the section on GUI abstractions.

#### The Module Code

```python
# arjuna-samples/arjex_webui_basics/lib/wp.py

from arjuna import *

def create_wordpress_app():
    url = Arjuna.get_ref_config().get_user_option_value("wp.login.url")
    wordpress = WebApp(base_url=url)
    wordpress.launch()
    return wordpress

def login(wordpress):
    user = wordpress.config.get_user_option_value("wp.admin.name")
    pwd = wordpress.config.get_user_option_value("wp.admin.pwd")

    # Login
    wordpress.element(With.id("user_login")).text = user
    wordpress.element(With.id("user_pass")).text = pwd
    wordpress.element(With.id("wp-submit")).click()
    wordpress.element(With.classes("welcome-view-site"))

def logout(wordpress):
    url = wordpress.config.get_user_option_value("wp.logout.url")
    wordpress.go_to_url(url)
    wordpress.element(With.link("log out")).click()
    wordpress.element(With.text("logged out"))

    wordpress.quit()

```

#### Points to Note
1. We are placing this code as in a module inside `lib` directory of your project. When Arjuna loads, it injects the parent directory of your project into PYTHONPATH. It means any packages/modules that you place in your project can be easily imported in your tests. This class can now be imported as `from <your_prj_name>.lib.wp import WordPress`.
2. All the code here is taken from the previous GuiElement interaction example. However, we have arranged it in 3 separate functions.

#### Using the Reusable Functions in Test Code

```python
# arjuna-samples/arjex_webui_basics/tests/modules/check_03_wordpress_app.py

from arjuna import *
from arjex_webui_basics.lib.wp import *

@test
def check_sep_functions(request):
    wordpress = create_wordpress_app()
    login(wordpress)
    logout(wordpress)
```

The above code is basic Python. We are able to make use of the functions that we created. In next secion, we will use this code to create a test fixture.

