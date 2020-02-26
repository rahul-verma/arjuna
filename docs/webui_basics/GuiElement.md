### GuiElement - Identification and Interactions

A single node in the DOM of a web UI is represented by a GuiElement object in Arjuna, irrespective of its type. This is unless you need specialized methods which we will see later.

Arjuna supports the locators which are supported by Selenium's By object. Apart from these, there are various abstracted locators which Arjuna provides for easier coding.

The locator strategy is expressed by using various factory methods of Arjuna's **`With`** class.

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

#### Test Fixture for Examples in This Page

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
# arjuna-samples/arjex_webui_basics/test/module/check_02_guielement.py

@for_test
def wordpress(request):
    # Setup
    wp_url = Arjuna.get_ref_config().user_options.value("wp.login.url")
    wordpress = WebApp(base_url=wp_url)
    wordpress.launch()
    
    yield wordpress
    
    # Teadown    
    wordpress.quit()
```

##### Points to Note
1. We retrieve the Login page URL for Wordpress from `Configuration`.
2. We create a `WebApp` instance and supply the above URL as the `base_url` argument.
3. We launch the app.
4. We yield this app object so that it is available in the tests.
5. In the teadown section, we quit the app.

#### Identification using ID, Name, Class Name, Tag Name, Link Text, Partial Link Text

```python
# arjuna-samples/arjex_webui_basics/test/module/check_02_guielement.py

@test
def check_basic_identifiers(request, wordpress):

    # user name field.
    # Html of user name: <input type="text" name="log" id="user_login" class="input" value="" size="20">
    element = wordpress.element(With.id("user_login"))
    element = wordpress.element(With.name("log"))
    element = wordpress.element(With.tag("input"))
    element = wordpress.element(With.classes("input"))

    # Lost your password link
    # Html of link: <a href="/wp-login.php?action=lostpassword" title="Password Lost and Found">Lost your password?</a>
    # Partial Link text match
    element = wordpress.element(With.link("password"))
    # Full Link text match
    element = wordpress.element(With.flink("Lost your password?"))

    wordpress.quit()
```

##### Points to Note
1. Launch the WebApp. Use a WordPress deployment of choice. For example code creation, a VirtualBox image of Bitnami Wordpress was used.
2. GuiElement identification if done by calling the **`element`** factory method of of `WebApp`.
3. The locator strategy is expressed using factory methods of **`With`** class. Arjuna's `With` object supports all Selenium's `By` identifiers, with slight modifications:
- **`With.id`** : Wraps By.id
- **`With.name`** : Wraps By.name
- **`With.tag`** : Wraps By.tag_name
- **`With.classes`** : Wraps By.class_name, however it supports compound classes. See Locator Extensions section on this page.
- **`With.link`** : Wraps By.partial_link_text. Note that all content/text matches in Arjuna are partial matches (opposite of Selenium).
- **`With.flink`** : Wraps By.link_text (short for Full Link)
4. Quit the app using its `quit` method.

#### Identification using XPath

We use **`With.xpath`** for identification using XPath. It is a direct wrapper on By.xpath in Selenium. Following are various samples.

```python
# arjuna-samples/arjex_webui_basics/test/module/check_02_guielement.py

@test
def check_xpath(request, wordpress):

    # Based on Text
    element = wordpress.element(With.xpath("//*[text() = 'Lost your password?']"))

    # Based on partial text
    element = wordpress.element(With.xpath("//*[contains(text(), 'Lost')]"))

    # Based on Title
    element = wordpress.element(With.xpath("//*[@title = 'Password Lost and Found']"))

    # Based on Value
    element = wordpress.element(With.xpath("//*[@value = 'Log In']"))

    # Based on any attribute e.g. for
    element = wordpress.element(With.xpath("//*[@for = 'user_login']"))

    # Based on partial content of an attribute
    element = wordpress.element(With.xpath("//*[contains(@for, '_login')]"))

    # Based on element type
    element = wordpress.element(With.xpath("//*[@type ='password']"))

    wordpress.quit()
```

#### Identification using CSS Selectors

We use **`With.selector`** for identification using CSS Selector. It is a direct wrapper on By.css_selector in Selenium. Following are various samples.

```python
# arjuna-samples/arjex_webui_basics/test/module/check_02_guielement.py

@test
def check_xpath(request, wordpress):

    # Based on any attribute e.g. for
    element = wordpress.element(With.selector("*[for = 'user_login']"))

    # Based on partial content of an attribute
    element = wordpress.element(With.selector("*[for *= '_login']"))

    # Based on element type
    element = wordpress.element(With.selector("*[type ='password']"))

    # Based on compound classes
    element = wordpress.element(With.selector(".button.button-large"))

    wordpress.quit()
```

#### Identification using Arjuna's Locator Extensions

Arjuna's `With` object provides various higher level locator strategies in addition to wrapping Selenium's By-style strategies. Following is the list of these extensions:
- **`With.text`** : Generates Partial Text based XPath
- **`With.ftext`** : Generates Full Text based XPath
- **`With.title`** : Generates Title Match CSS Selector
- **`With.value`** : Generates Value Match CSS Selector
- **`With.attr`** : Generates Partial Attribute Value Match CSS Selector
- **`With.fattr`** : Generates Full Attribute Match CSS Selector
- **`With.classes`** : Supports compound classes (supplied as a single string or as multiple separate strings)
- **`With.point`** : Runs a JavaScript to find the GuiElement under an XY coordinate
- **`With.js`** : Runs the supplied JavaScript and returns GuiElement representing the element it returns.
    
Following is the example code:


```python
# arjuna-samples/arjex_webui_basics/test/module/check_02_guielement.py

@test
def check_xpath(request, wordpress):

    # Based on partial text
    element = wordpress.element(With.text("Lost"))

    # Based on Full Text
    element = wordpress.element(With.ftext("Lost your password?"))

    # Based on Title
    element = wordpress.element(With.title("Password Lost and Found"))

    # Based on Value
    element = wordpress.element(With.value("Log In"))

    # Based on partial match of content of an attribute
    element = wordpress.element(With.attr("for", "_login"))

    # Based on full match of an attribute
    element = wordpress.element(With.fattr("for", "user_login"))    

    # Based on element type
    element = wordpress.element(With.type("password"))

    # Based on compound classe
    element = wordpress.element(With.classes("button button-large"))
    element = wordpress.element(With.classes("button", "button-large"))

    # Based on Point (location in terms of X,Y co-ordinates)
    element = wordpress.element(With.point(Screen.xy(1043, 458)))

    # With Javascript
    element = wordpress.element(With.js("return document.getElementById('wp-submit')"))

    wordpress.quit()
```

#### Basic GuiElement Interactions - Setting Text, Clicking and Waits

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

```python
# arjuna-samples/arjex_webui_basics/test/module/check_02_guielement.py

@test
def check_wp_login(request, wordpress):

    user = wordpress.config.user_options.value("wp.admin.name")
    pwd = wordpress.config.user_options.value("wp.admin.pwd")
    
    # Login
    user_field = wordpress.element(With.id("user_login"))
    user_field.text = user

    pwd_field = wordpress.element(With.id("user_pass"))
    pwd_field.text = pwd

    submit = wordpress.element(With.id("wp-submit"))
    submit.click()

    wordpress.element(With.classes("welcome-view-site"))

    # Logout
    url = wordpress.config.user_options.value("wp.logout.url")
    wordpress.go_to_url(url)

    confirmation = wordpress.element(With.link("log out"))
    confirmation.click()

    wordpress.element(With.text("logged out"))
```

##### Points to Note
1. We retrieve user name and password from the user options specified in `project.conf`.
2. We identify different elements as discussed earlier.
3. For setting text of an element we can set the value for its `text` attribute.
4. To click an element, we can call its `click` method.
5. What you will notice is that there is no waiting logic in the test code.

#### Basic GuiElement Interactions - You Can Write Concise Code If You Wish

Code style could be a very personal thing. If you are looking for a conside coding option, you can write the previous code as follows with exact same functionality:

```python
# arjuna-samples/arjex_webui_basics/test/module/check_02_guielement.py

@test
def check_wp_login(request, wordpress):

    user = wordpress.config.user_options.value("wp.admin.name")
    pwd = wordpress.config.user_options.value("wp.admin.pwd")
    
    # Login
    wordpress.element(With.id("user_login")).text = user
    wordpress.element(With.id("user_pass")).text = pwd
    wordpress.element(With.id("wp-submit")).click()
    wordpress.element(With.classes("welcome-view-site"))

    # Logout
    url = wordpress.config.user_options.value("wp.logout.url")
    wordpress.go_to_url(url)
    wordpress.element(With.link("log out")).click()
    wordpress.element(With.text("logged out"))
    
```
