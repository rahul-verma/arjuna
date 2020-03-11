### Gui Element Locators - Using XPath

We use **`xpath`** locator for identification using XPath. It is a direct wrapper on By.xpath in Selenium. Following are various samples.

#### Test Fixture for Example(s) in This Page

Below is the `@for_test` fixture code:

```python
# arjuna-samples/arjex_webui_basics/test/module/check_03_locators_xpath.py

@for_test
def wordpress(request):
    # Setup
    wp_url = C("wp.login.url")
    wordpress = WebApp(base_url=wp_url, label="XPath")
    wordpress.launch()
    
    yield wordpress
    
    # Teadown    
    wordpress.quit()
```

##### Points to Note
1. Label is changed to `XPath`.
2. Rest of the code is same as earlier.

### The GNS File

Location for the following file is `arjuna-samples/arjex_app/guiauto/namespace/XPath.yaml`

```YAML
labels:

  lost_pass_text:
    xpath: "//*[text() = 'Lost your password?']"

  lost_pass_text_content:
    xpath: "//*[contains(text(), 'Lost')]"

  lost_pass_title:
    xpath: "//*[@title = 'Password Lost and Found']"

  user_value:
    xpath: "//*[@value = 'Log In']"

  user_attr:
    xpath: "//*[@for = 'user_login']"

  user_attr_content:
    xpath: "//*[contains(@for, '_login')]"

  pass_type:
    xpath: "//*[@type ='password']"
```


### Usage

```python
# arjuna-samples/arjex_webui_basics/test/module/check_03_locators_xpath.py

@test
def check_xpath(request, wordpress):

    # Based on Text
    element = wordpress.lost_pass_text

    # Based on partial text
    element = wordpress.lost_pass_text_content

    # Based on Title
    element = wordpress.lost_pass_title

    # Based on Value
    element = wordpress.user_value

    # Based on any attribute e.g. for
    element = wordpress.user_attr

    # Based on partial content of an attribute
    element = wordpress.user_attr_content

    # Based on element type
    element = wordpress.pass_type
```
