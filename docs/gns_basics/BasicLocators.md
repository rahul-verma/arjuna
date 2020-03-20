### Gui Namespace - Externalizing ID, Name, Tag, Class, Link Text and Partial Link Text

#### Test Fixture for Example(s) in This Page

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
2. We create a `WebApp` instance and supply the above URL as the `base_url` argument. Use a WordPress deployment of choice. For example code creation, a VirtualBox image of Bitnami Wordpress was used.
3. To instruct Arjuna to pick up a GNS file for a given name, we can provide the `label` argument. Now it will look for `BasicIdentification.yaml` in project's Gui Namespace directory.
3. We launch the app.
4. We yield this app object so that it is available in the tests.
5. In the teadown section, we quit the app using `quit` method of the app.

#### The GNS File

Location for the following file is `arjuna-samples/arjex/guiauto/namespace/BasicIdentification.yaml`

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

#### Usage in code

```python
# arjuna-samples/arjex/test/module/web_ui_basics/check_02_locators_basic.py

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
1. You can directly create an element by using `<app object>.gns.<GNS label>` syntax. For example, `wordpress.gns.user_id` will find an element with the locator information supplied in GNS file for the label `user_id`.
2. The locator strategy is expressed using locator type names supported by Arjuna. These are simple locators and hence are expressed as basic key value pairs, almost equivalent to the way you pass them as keyword arguments in `app.element` calls. Functionality is equivalent as well.