### Gui Element Locators - Using ID, Name, Tag, Class, Link Text, Partial Link Text

A single node in the DOM of a web UI is represented by a GuiElement object in Arjuna, irrespective of its type. This is unless you need specialized methods which we will see later.

Arjuna supports the locators which are supported by Selenium's By object. Apart from these, there are various abstracted locators which Arjuna provides for easier coding.

For this section, we'll use the login page of WordPress CMS. The elements of interest are the **User Name** field and the **Lost Your Password?** link.

<img src="img/wp_login.png" height="500" width="500">

In the above page, the HTML for the **User Name** field is:

```html
<input type="text" name="log" id="user_login" class="input" value="" size="20">
```

and for **Lost Your Password?** link is:

```html
<a href="/wp-login.php?action=lostpassword" title="Password Lost and Found">Lost your password?</a>
```

#### Test Fixture for Example(s) in This Page

We are going to use a test-level fixture for the examples.

Following user options have been added to `project.conf` for this fixture to work

```javascript
        userOptions {
	        wp.app.url = "IP address"
	        wp.login.url = ${userOptions.wp.app.url}"/wp-admin"
        }
```

Below is the `@for_test` fixture code:

```python
# arjuna-samples/arjex/lib/fixture/test.py

@for_test
def wordpress(request):
    # Setup
    wp_url = C("wp.login.url")
    wordpress = WebApp(base_url=wp_url)
    wordpress.launch()
    
    yield wordpress
    
    # Teadown    
    wordpress.quit()
```

##### Points to Note
1. We retrieve the Login page URL for Wordpress from `Configuration`.
2. We create a `WebApp` instance and supply the above URL as the `base_url` argument. Use a WordPress deployment of choice. For example code creation, a VirtualBox image of Bitnami Wordpress was used.
3. We launch the app.
4. We yield this app object so that it is available in the tests.
5. In the teadown section, we quit the app using `quit` method of the app.

#### Identification using ID, Name, Class Name, Tag Name, Link Text, Partial Link Text

```python
# arjuna-samples/arjex/test/module/web_ui_basics/check_02_locators_basic_locate.py

from arjuna import *

def check_basic_identifiers(request, wordpress):
    # user name field.
    # Html of user name: <input type="text" name="log" id="user_login" class="input" value="" size="20">
    wordpress.element(id="user_login")
    wordpress.element(name="log")
    wordpress.element(tag="input")
    wordpress.element(classes="input")

    # Lost your password link
    # Html of link: <a href="/wp-login.php?action=lostpassword" title="Password Lost and Found">Lost your password?</a>
    # Partial Link text match
    wordpress.element(link="password")
    # Full Link text match
    wordpress.element(flink="Lost your password?")
```

##### Points to Note
1. Launch the WebApp. Use a WordPress deployment of choice. For example code creation, a VirtualBox image of Bitnami Wordpress was used.
2. You can create an element by using `<app object>.element(<locator_type>=<locator_value>)` syntax. For example, `wordpress.element(id="user_login")` will find an element with id.
3. The locator strategy is expressed using locator type names supported by Arjuna. You can pass it as a keyword argument `k=v` format to the the `element` call. Here, we are using the following basic locators, which have one to one mapping to Selenium's equivalent identifiers using By object.
- **`id`** : Wraps By.id
- **`name`** : Wraps By.name
- **`tag`** : Wraps By.tag_name
- **`classes`** : Wraps By.class_name, however it supports compound classes. See Arjuna Locator Extensions page for more information.
- **`link`** : Wraps By.partial_link_text. Note that all content/text matches in Arjuna are partial matches (opposite of Selenium).
- **`flink`** : Wraps By.link_text (short for Full Link)