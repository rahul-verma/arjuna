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

#### Identification using ID, Name, Class Name, Tag Name, Link Text, Partial Link Text

```python
# arjuna-samples/arjex_webui_basics/tests/modules/test_02_guielement.py

@test
def test_basic_identifiers(my, request):
    wp_url = Arjuna.get_ref_config().get_user_option_value("wp.login.url").as_str()
    wordpress = WebApp(base_url=wp_url)
    wordpress.launch()

    # user name field.
    # Html of user name: 
    element = wordpress.ui.element(With.id("user_login"))
    element = wordpress.ui.element(With.name("log"))
    element = wordpress.ui.element(With.class_name("input"))
    element = wordpress.ui.element(With.tag_name("input"))

    # Lost your password link
    # Html of link: 
    element = wordpress.ui.element(With.link_text("Lost your password?"))
    element = wordpress.ui.element(With.link_ptext("password"))

    wordpress.quit()
```

##### Points to Note
1. Launch the WebApp. Use a WordPress deployment of choice. For example code creation, a VirtualBox image of Bitnami Wordpress was used.
2. GuiElement identification if done by calling the **`element`** factory method of `ui` object of `WebApp`.
3. The locator strategy is expressed using factory methods of **`With`** class which correspond as follows:
    - **`With.id`** - ID attribute
    - **`With.name`** - Name attribute
    - **`With.class_name`** - One of the class names in class attribute
    - **`With.tag_name`** - Tag Name
    - **`With.link_text`**  - Link Text
    - **`With.link_ptext`** - A part of Link's text
4. Quit the app using its `quit` method.

#### Identification using XPath

We use **`With.xpath`** for identification using XPath. Following are various samples.

```python
# arjuna-samples/arjex_webui_basics/tests/modules/test_02_guielement.py

@test
def test_xpath(my, request):
    wp_url = Arjuna.get_ref_config().get_user_option_value("wp.login.url").as_str()
    wordpress = WebApp(base_url=wp_url)
    wordpress.launch()

    # Based on Text
    element = wordpress.ui.element(With.xpath("//*[text() = 'Lost your password?']"))

    # Based on partial text
    element = wordpress.ui.element(With.xpath("//*[contains(text(), 'Lost')]"))

    # Based on Title
    element = wordpress.ui.element(With.xpath("//*[@title = 'Password Lost and Found']"))

    # Based on Value
    element = wordpress.ui.element(With.xpath("//*[@value = 'Log In']"))

    # Based on any attribute e.g. for
    element = wordpress.ui.element(With.xpath("//*[@for = 'user_login']"))

    # Based on partial content of an attribute
    element = wordpress.ui.element(With.xpath("//*[contains(@for, '_login')]"))

    # Based on element type
    element = wordpress.ui.element(With.xpath("//*[@type ='password']"))

    wordpress.quit()
```

#### Identification using CSS Selectors

We use **`With.css_selector`** for identification using CSS Selector. Following are various samples.

```python
# arjuna-samples/arjex_webui_basics/tests/modules/test_02_guielement.py

@test
def test_xpath(my, request):
    wp_url = Arjuna.get_ref_config().get_user_option_value("wp.login.url").as_str()
    wordpress = WebApp(base_url=wp_url)
    wordpress.launch()
    
    # Based on any attribute e.g. for
    element = wordpress.ui.element(With.css_selector("*[for = 'user_login']"))

    # Based on partial content of an attribute
    element = wordpress.ui.element(With.css_selector("*[for *= '_login']"))

    # Based on element type
    element = wordpress.ui.element(With.css_selector("*[type ='password']"))

    # Based on compound classes
    element = wordpress.ui.element(With.css_selector(".button.button-large"))

    wordpress.quit()
```

#### Identification using Arjuna's Locator Extensions

Arjuna's `With` object provides various higher level locator strategies in addition to wrapping Selenium's By-style strategies. Following is the list of these extensions:
    - **`With.text`** : Generates Text based XPath
    - **`With.ptext`** : Generates Text Content based XPath
    - **`With.title`** : Generates Title Match CSS Selector
    - **`With.value`** : Generates Value Match CSS Selector
    - **`With.attr_value`** : Generates Attribute Value Match CSS Selector
    - **`With.attr_pvalue`** : Generates Attribute Value Content Match CSS Selector
    - **`With.compound_class`** : Generates Compund Class Match CSS Selector (from a string)
    - **`With.class_names`** : Generates Compund Class Match CSS Selector (from multiple strings)
    - **`With.point`** : Runs a JavaScript to find the GuiElement under an XY coordinate
    - **`With.javascript`** : Runs the supplied JavaScript and returns GuiElement representing the element it returns.
    
Following is the example code:


```python
# arjuna-samples/arjex_webui_basics/tests/modules/test_02_guielement.py

@test
def test_xpath(my, request):
    wp_url = Arjuna.get_ref_config().get_user_option_value("wp.login.url").as_str()
    wordpress = WebApp(base_url=wp_url)
    wordpress.launch()
    
    # Based on Text
    element = wordpress.ui.element(With.text("Lost your password?"))

    # Based on partial text
    element = wordpress.ui.element(With.ptext("Lost"))

    # Based on Title
    element = wordpress.ui.element(With.title("Password Lost and Found"))

    # Based on Value
    element = wordpress.ui.element(With.value("Log In"))

    # Based on any attribute e.g. for
    element = wordpress.ui.element(With.attr_value("for", "user_login"))

    # Based on partial content of an attribute
    element = wordpress.ui.element(With.attr_pvalue("for", "_login"))

    # Based on element type
    element = wordpress.ui.element(With.type("password"))

    # Based on compound classe
    element = wordpress.ui.element(With.compound_class("button button-large"))

    # Based on class names
    element = wordpress.ui.element(With.class_names("button", "button-large"))

    # Based on Point (location in terms of X,Y co-ordinates)
    element = wordpress.ui.element(With.point(Screen.xy(1043, 458)))

    # With Javascript
    element = wordpress.ui.element(With.javascript("return document.getElementById('wp-submit')"))


    wordpress.quit()
```
