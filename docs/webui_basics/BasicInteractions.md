### Basic Interactions with a Gui Element - Setting Text, Clicking and Waits

To interact with a GuiElement, from automation angle it must be in an interactable state. In the usual automation code, a test author writes a lot of waiting related code (and let's not even touch the `time.sleep`.).

Arjuna does a granular automatic waiting of three types:
- Waiting for the presence of an element when it is attempting to identify a GuiElement
- Waiting for the right state (for example, clickability of an GuiElement when you enter text or want to click it)
- Waiting for interaction to succeed (Arjuna, for example, retries click if interaction exception is raised).

Following user options have been added to `project.conf` for this test to work:

```javascript
        userOptions {
	        wp.app.url = "IP address"
	        wp.login.url = ${userOptions.wp.app.url}"/wp-admin"
	        wp.logout.url = ${userOptions.wp.app.url}"/wp-login.php?action=logout"

            wp.admin {
                name = "<username>"
                pwd = "<password>"
            }
        }
```

We will simulate WordPress login. Following are the steps:
1. Enter user name and password.
2. Click Submit button.
3. As mouse actions have not been discussed so far, we will directly go to the logout URL.
4. In the process, WordPress shows some confirmation and success messages.

#### Test Fixture for Example(s) in This Page

Same as Basic locators example.

#### Usage

```python
# arjuna-samples/arjex/test/module/web_ui_basics/check_06_basicinteract_raw.py

@test
def check_wp_login(request, wordpress):
    user = C("wp.admin.name")
    pwd = C("wp.admin.pwd")
    
    # Login
    user_field = wordpress.element(id="user_login")
    user_field.text = user

    pwd_field = wordpress.element(id="user_pass")
    pwd_field.text = pwd

    submit = wordpress.element(id="wp-submit")
    submit.click()

    wordpress.element(classes="welcome-view-site")

    # Logout
    url = C("wp.logout.url")
    wordpress.go_to_url(url)

    confirmation = wordpress.element(link="log out")
    confirmation.click()

    wordpress.element(text="logged out")
```

##### Points to Note
1. We retrieve user name and password from the user options specified in `project.conf`.
2. We identify different elements as discussed earlier.
3. For setting text of an element we can set the value for its `text` property.
4. To click an element, we can call its `click` method.
5. What you will notice is that there is no waiting logic in the test code.
