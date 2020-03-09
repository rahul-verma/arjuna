### The Magic `C` Function

```python
# arjuna-samples/arjuna_config/test/module/check_06_Cfunc.py

from arjuna import *

@test
def check_config_retrieval_C(request):
    print(C(ArjunaOption.BROWSER_NAME))
    print(C("browser.name"))
    print(C("BROWSER_NAME"))
```

##### Points to Note
1. Arjuna provides a special function `C` for retrieving values from the reference configuration as it is a very common operation to do on test code.
2. You can pass an `ArjunaOption` enum constant or an option name. The name string has all the flexibility seen in previous example.

#### Configuration Query Format

As Arjuna supports a multi-configuration system, it also provides a special query syntax for retrieving configuration values.

```python
# arjuna-samples/arjuna_config/test/module/check_06_Cfunc.py

from arjuna import *
@test
def check_conf_name_wise_query(request):
    cb = request.config.builder
    cb.browser_name = BrowserName.FIREFOX
    mconf = cb.register("nconf")

    print(C("browser.name"))
    print(C("reference.browser.name"))
    print(C("reference.browser_name"))
    print(C("nconf.browser_name"))
    print(C("nconf.browser.name"))
```

#### Points to Note
1. In the example, we are creating a custom configuration with name `nconf`.
2. `browser.name` refers to the property in reference configuration.
3. You can prefix a configuration name with a configuration name. For example here `reference.browser.name` and `nconf.browser.name` will retrieve `browser.name` from `reference` and `nconf` configurations respectively.
