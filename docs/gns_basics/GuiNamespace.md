### Gui Namespace - Externalizing Identifiers

After launching a `WebApp`, apart from basic browser operations, most of times an automated test finds and interacts with Gui elements.

Externalizing of identifiers is built into Arjuna and is a MUST to do UI automation with Arjuna. The object which contains identification information and related meta-data of a Gui is referred to as `GuiNamespace (GNS)` in Arjuna.

#### The GNS File

Arjuna uses YAML as the format for externalization of identifiers. Fow now, we will discuss basic usage of the format.

Following is the high level format for simple usage. We will explore practical implementations in the later sections.

```YAML
labels:

  <label1>:
    <locator type>: <locator data>

  <label2>:
    <locator type>: <locator data>

  <labelN>:
    <locator type>: <locator data>
```

##### Points to note
1. This file has a `YAML` extension.
2. All labels are placed under `labels` heading.
3. Each label represents element identification information which can be later referenced by this label.
3. The label should be a valid Arjuna name.
4. In its basic usage format, the section has a key value pair for a given locator type. For example `id: user_login`.
5. Labels are treated as **case-insensitive** by Arjuna.

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