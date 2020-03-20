### Gui Namespace - Externalizing Arjuna's Locator Extensions

All of Arjuna's locator extensions can be externalizd in GNS as well.

- Following are externalized as simple key value pairs:
    - **`text`**
    - **`ftext`**
    - **`title`**
    - **`value`**
    - **`js`**
- Following are externlized with content as a YAML mapping with `name` and `value` keys:
    - **`attr`**
    - **`fattr`**
- **`classes`** is externalized as a single string or a YAML list of strings:
- **`point`** is externlized with content as a YAML mapping with `x` and `y` keys.

#### Test Fixture for Example(s) in This Page

Below is the `@for_test` fixture code:

```python
# arjuna-samples/arjex/test/module/check_05_locators_arjuna_exts.py

@for_test
def wordpress(request):
    # Setup
    wp_url = C("wp.login.url")
    wordpress = WebApp(base_url=wp_url, label="ArjunaExtended")
    wordpress.launch()
    yield wordpress

    # Teadown
    wordpress.quit()
```

##### Points to Note
1. Label is changed to `ArjunaExtended`.
2. Rest of the code is same as earlier.

### The GNS File

Location for the following file is `arjuna-samples/arjex_app/guiauto/namespace/ArjunaExtended.yaml`

```YAML
labels:

  lost_pass_text:
    text: Lost

  lost_pass_ftext:
    ftext: "Lost your password?"

  lost_pass_title:
    title: Password Lost and Found

  user_value:
    value: Log In

  user_attr:
    attr:
      name: for
      value: _login

  user_fattr:
    fattr:
      name: for
      value: user_login

  pass_type:
    type: password

  button_classes_str:
    classes: button button-large

  button_classes_list:
    classes: 
      - button 
      - button-large

  elem_xy:
    point:
      x: 1043
      y: 458

  elem_js:
    js: "return document.getElementById('wp-submit')"
```

### Usage

```python
# arjuna-samples/arjex/test/module/check_05_locators_arjuna_exts.py

@test
def check_arjuna_exts(request, wordpress):

    # Based on partial text
    element = wordpress.gns.lost_pass_text

    # Based on Full Text
    element = wordpress.gns.lost_pass_ftext

    # Based on Title
    element = wordpress.gns.lost_pass_title

    # Based on Value
    element = wordpress.gns.user_value

    # Based on partial match of content of an attribute
    element = wordpress.gns.user_attr

    # Based on full match of an attribute
    element = wordpress.gns.user_fattr

    # Based on element type
    element = wordpress.gns.pass_type

    # Based on compound classes
    element = wordpress.gns.button_classes_str
    element = wordpress.gns.button_classes_list

    # Based on Point (location in terms of X,Y co-ordinates)
    element = wordpress.gns.elem_xy

    # With Javascript
    element = wordpress.gns.elem_js
```
