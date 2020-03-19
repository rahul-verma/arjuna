### Gui Element Locators - Using CSS Selectors

We use **`selector`** locator for identification using CSS Selector. It is a direct wrapper on By.css_selector in Selenium.

#### Test Fixture for Example(s) in This Page

Below is the `@for_test` fixture code:

```python
# arjuna-samples/arjex/test/module/check_04_locators_css_selectors.py

@for_test
def wordpress(request):
    # Setup
    wp_url = C("wp.login.url")
    wordpress = WebApp(base_url=wp_url, label="Selector")
    wordpress.launch()
    
    yield wordpress
    
    # Teadown    
    wordpress.quit()
```

##### Points to Note
1. Label is changed to `Selector`.
2. Rest of the code is same as earlier.

### The GNS File

Location for the following file is `arjuna-samples/arjex_app/guiauto/namespace/Selector.yaml`

```YAML
labels:

  user_attr:
    selector: "*[for = 'user_login']"

  user_attr_content:
    selector: "*[for *= '_login']"

  pass_type:
    selector: "*[type ='password']"

  button_compound_class:
    selector: ".button.button-large"
```

### Usage

```python
# arjuna-samples/arjex/test/module/check_04_locators_css_selectors.py

@test
def check_selector(request, wordpress):

    # Based on any attribute e.g. for
    element = wordpress.gns.user_attr

    # Based on partial content of an attribute
    element = wordpress.gns.user_attr_content

    # Based on element type
    element = wordpress.gns.pass_type

    # Based on compound classes
    element = wordpress.gns.button_compound_class
```
