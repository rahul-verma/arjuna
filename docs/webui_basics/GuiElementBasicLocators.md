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
# arjuna-samples/arjex/test/module/check_02_guielement.py

@for_test
def wordpress(request):
    # Setup
    wp_url = C("wp.login.url")
    wordpress = WebApp(base_url=wp_url, label="BasicIdentification")
    wordpress.launch()
    
    yield wordpress
    
    # Teadown    
    wordpress.quit()
```

##### Points to Note
1. We retrieve the Login page URL for Wordpress from `Configuration`.
2. We create a `WebApp` instance and supply the above URL as the `base_url` argument.
3. To instruct Arjuna to pick up a GNS file for a given name, we can provide the `label` argument. Now it will look for `BasicIdentification.yaml` in project's Gui Namespace directory.
3. We launch the app.
4. We yield this app object so that it is available in the tests.
5. In the teadown section, we quit the app using `quit` method of the app.


### The GNS File

In the last section we had discussed the concept of `GuiNamespace`. For completeness sake, the YAML file is presented below:

Location for the following file is `arjuna-samples/arjex_app/guiauto/namespace/BasicIdentification.yaml`

```YAML
labels:

  user_id:
    id: user_login

  user_name:
    name: log

  user_tag:
    tag: input

  user_class:
    classes: input

  lost_pass_link:
    link: password

  lost_pass_flink:
    flink: "Lost your password?"
```

#### Identification using ID, Name, Class Name, Tag Name, Link Text, Partial Link Text

```python
# arjuna-samples/arjex/test/module/check_02_locators_basic.py

@test
def check_basic_identifiers(request, wordpress):
    # user name field.
    # Html of user name: <input type="text" name="log" id="user_login" class="input" value="" size="20">
    element = wordpress.gns.user_id
    element = wordpress.gns.user_name
    element = wordpress.gns.user_tag
    element = wordpress.gns.user_class

    # Lost your password link
    # Html of link: <a href="/wp-login.php?action=lostpassword" title="Password Lost and Found">Lost your password?</a>
    # Partial Link text match
    element = wordpress.gns.lost_pass_link
    # Full Link text match
    element = wordpress.gns.lost_pass_flink
```

##### Points to Note
1. Launch the WebApp. Use a WordPress deployment of choice. For example code creation, a VirtualBox image of Bitnami Wordpress was used.
2. You can directly create an element by using `<app object>.gns.<GNS label>` syntax. For example, `wordpress.gns.user_id` will find an element with the locator information supplied in GNS file for the label `user_id`.
3. The locator strategy is expressed using locator type names supported by Arjuna. Here, we are using the following basic locators, which have one to one mapping to Selenium's equivalent identifiers using By object.
- **`id`** : Wraps By.id
- **`name`** : Wraps By.name
- **`tag`** : Wraps By.tag_name
- **`classes`** : Wraps By.class_name, however it supports compound classes. See Arjuna Locator Extensions page for more information.
- **`link`** : Wraps By.partial_link_text. Note that all content/text matches in Arjuna are partial matches (opposite of Selenium).
- **`flink`** : Wraps By.link_text (short for Full Link)