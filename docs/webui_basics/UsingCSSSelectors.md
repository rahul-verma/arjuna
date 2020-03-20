### Gui Element Locators - Using CSS Selectors

We use **`selector`** locator for identification using CSS Selector. It is a direct wrapper on By.css_selector in Selenium.

#### Test Fixture for Example(s) in This Page

Same as Basic locators example.

### Usage

```python
# arjuna-samples/arjex/test/module/web_ui_basics/check_04_locators_css_selector.py

from arjuna import *

@test
def check_selector(request, wordpress):

    # Based on any attribute e.g. for
    wordpress.element(selector="*[for = 'user_login']")

    # Based on partial content of an attribute
    wordpress.element(selector="*[for *= '_login']")

    # Based on element type
    wordpress.element(selector="*[type ='password']")

    # Based on compound classes
    wordpress.element(selector=".button.button-large")
```
