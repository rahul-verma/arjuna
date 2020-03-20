#### Concise Basic Interactions with a Gui Element - You Can Write Concise Code If You Wish

Code style could be a very personal thing. If you are looking for a concise coding option, you can write the previous code as follows with exact same functionality:

#### Test Fixture for Example(s) in This Page

Same as Basic locators example.

### Usage

```python
# arjuna-samples/arjex/test/module/web_ui_basics/check_07_basicinteract_refined.py

from arjuna import *

@test
def check_wp_login_concise(request, wordpress):
    
    user = C("wp.admin.name")
    pwd = C("wp.admin.pwd")
    
    # Login
    wordpress.element(id="user_login").text = user
    wordpress.element(id="user_pass").text = pwd
    wordpress.element(id="wp-submit").click()
    wordpress.element(classes="welcome-view-site")

    # Logout
    url = C("wp.logout.url")
    wordpress.go_to_url(url)
    wordpress.element(link="log out").click()
    wordpress.element(text="logged out")
```
