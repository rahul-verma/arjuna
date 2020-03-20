### Gui Element Locators - Using XPath

We use **`xpath`** locator for identification using XPath. It is a direct wrapper on By.xpath in Selenium. Following are various samples.

#### Test Fixture for Example(s) in This Page

Same as Basic locators example.

### Usage

```python
# arjuna-samples/arjex/test/module/web_ui_basics/check_03_locators_xpath.py

from arjuna import *

@test
def check_xpath(request, wordpress):
    # Based on Text
    wordpress.element(xpath="//*[text() = 'Lost your password?']")

    # Based on partial text
    wordpress.element(xpath="//*[contains(text(), 'Lost')]")

    # Based on Title
    wordpress.element(xpath="//*[@title = 'Password Lost and Found']")

    # Based on Value
    wordpress.element(xpath="//*[@value = 'Log In']")

    # Based on any attribute e.g. for
    wordpress.element(xpath="//*[@for = 'user_login']")

    # Based on partial content of an attribute
    wordpress.element(xpath="//*[contains(@for, '_login')]")

    # Based on element type
    wordpress.element(xpath="//*[@type ='password']")
```
