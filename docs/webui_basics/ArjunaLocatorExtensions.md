### Gui Element Locators - Using Arjuna's Locator Extensions

Arjuna provides various higher level locator strategies in addition to wrapping Selenium's By-style strategies. Following is the list of these extensions:
- **`text`** : Generates Partial Text based XPath
- **`ftext`** : Generates Full Text based XPath
- **`title`** : Generates Title Match CSS Selector
- **`value`** : Generates Value Match CSS Selector
- **`attr`** : Generates Partial Attribute Value Match CSS Selector
- **`fattr`** : Generates Full Attribute Match CSS Selector
- **`classes`** : Supports compound classes (supplied as a single string or as multiple separate strings)
- **`point`** : Runs a JavaScript to find the GuiElement under an XY coordinate
- **`js`** : Runs the supplied JavaScript and returns GuiElement representing the element it returns.

#### Test Fixture for Example(s) in This Page

Same as Basic locators example.

### Usage

```python
# arjuna-samples/arjex/test/module/web_ui_basics/check_05_locators_arjuna_exts.py

from arjuna import *

@test
def check_arjuna_exts(request, wordpress):

    # Based on partial text
    wordpress.element(text="Lost")

    # Based on Full Text
    wordpress.element(ftext="Lost your password?")

    # Based on Title
    wordpress.element(title="Password Lost and Found")

    # Based on Value
    wordpress.element(value="Log In")

    # Based on partial match of content of an attribute
    wordpress.element(attr=Attr("for", "_login"))

    # Based on full match of an attribute
    wordpress.element(fattr=Attr("for", "user_login"))

    # Based on element type
    wordpress.element(type="password")

    # Based on compound classes
    wordpress.element(classes="button button-large")
    wordpress.element(classes=("button", "button-large"))

    # Based on Point (location in terms of X,Y co-ordinates)
    wordpress.element(point=Point(1043, 458))

    # With Javascript
    wordpress.element(js="return document.getElementById('wp-submit')")
```
