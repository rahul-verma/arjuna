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

Below is the `@for_test` fixture code:

```python
# arjuna-samples/arjex/test/module/check_03_locators_xpath.py

@for_test
def wordpress(request):
    # Setup
    wp_url = C("wp.login.url")
    wordpress = WebApp(base_url=wp_url, label="WordPress")
    wordpress.launch()
    
    yield wordpress
    
    # Teadown    
    wordpress.quit()
```

##### Points to Note
1. Label is changed to `WordPress`.
2. Rest of the code is same as earlier.


### The GNS File

Location for the following file is `arjuna-samples/arjex_app/guiauto/namespace/WordPress.yaml`

```YAML
labels:

  user:
    id: user_login

  pwd:
    id: user_pass

  submit:
    id: wp-submit

  view_site:
    classes: welcome-view-site

  logout_confirm:
    link: log out

  logout_msg:
    text: logged out
```

#### Usage

```python
# arjuna-samples/arjex/test/module/check_06_basicinteract_raw.py

@test
def check_wp_login(request, wordpress):
    user = C("wp.admin.name")
    pwd = C("wp.admin.pwd")
    
    # Login
    user_field = wordpress.gns.user
    user_field.text = user

    pwd_field = wordpress.gns.pwd
    pwd_field.text = pwd

    submit = wordpress.gns.submit
    submit.click()

    wordpress.gns.view_site

    # Logout
    url = C("wp.logout.url")
    wordpress.go_to_url(url)

    confirmation = wordpress.gns.logout_confirm
    confirmation.click()

    wordpress.gns.logout_msg
```

##### Points to Note
1. We retrieve user name and password from the user options specified in `project.conf`.
2. We identify different elements as discussed earlier.
3. For setting text of an element we can set the value for its `text` attribute.
4. To click an element, we can call its `click` method.
5. What you will notice is that there is no waiting logic in the test code.
