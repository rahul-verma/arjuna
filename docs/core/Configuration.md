### Configurations in Arjuna

#### Understanding Configuration System of Arjuna
- Arjuna supports tweaking its built in options which are represented by `ArjunaOption` enum. 
- Arjuna also supports user defined options.
- A `Configuration` object represents fixed values for configured settings (Arjuna options as well user defined options).
- As a part of initialation, Arjuna creates the reference `Configuration` object which combines the following to create the reference :
    - Default settings for Arjuna options
    - Project level settings included in `<Project root directory>/config/project.conf` file.
    - CLI Options for settings (TBD).
- You can get the reference configuration by calling `Arjuna.get_ref_config()`.
- Arjuna's `RunContext` object contains one or more `Configuration`s. By default it contains a configuration which is a deep copy of the reference Configuration.
- `RunContext` can be used to create and update custom configurations.
- You can retrieve the run context from Arjuna facade by making `Arjuna.get_run_context()`.

#### Retrieving value of Arjuna options in Code

```python
# arjuna-samples/arjex_core_features/tests/modules/test_03_tweaking_config.py
 
from arjuna import *

@testBrowserName.CHROME
def test_config_retrieval(my, request):
    config = Arjuna.get_ref_config()

    wait_value = config.get_arjuna_option_value(ArjunaOption.BROWSER_NAME)
    print(wait_value.as_str())

    wait_value = config.get_arjuna_option_value("BROWSER_NAME")
    print(wait_value.as_str())

    wait_value = config.get_arjuna_option_value("BrOwSeR_NaMe")
    print(wait_value.as_str())

    wait_value = config.get_arjuna_option_value("browser.name")
    print(wait_value.as_str())

    wait_value = config.get_arjuna_option_value("Browser.Name")
    print(wait_value.as_str())

    browser = config.browser_name
    print(browser)
 ```

##### Points to Note
1. First, we retrieve the reference config by calling `Arjuna.get_ref_config()`
2. You can retrieve value of an `ArjunaOption` by calling the `get_arjuna_option_value(<Arjuna Option or string>)` method of a `Configuration` object. The argument to this call can be an `ArjunaOption` enum constant or a string representing the option. 
3. The option name string is considered by Arjuna as **case-insensitive**. Also, **. (dot)** and **_ (underscore)** are interchangeable. So, following are equivalent arguments:
        - ArjunaOption.BROWSER_NAME
        - BROWSER_NAME
        - BrOwSeR_NaMe
        - browser.name
        - Browser.Name
        - and so on
4. `get_arjuna_option_value` call always returns a `Value` object which should be converted to an appropriate type before use.
5. The `Configuration` object also has named properties for commonly used Arjuna options. The name of property is same as the lower-case enum constant text, for example, `browser_name`. Such direct named methods return appropriate objects rather than `Value`s. For example, this call returns BrowserName.CHROME enum constant which is the real representation of browser name in Arjuna.

### Project Level Configuration Settings

Many a times, it is useful to change the defaults of Arjuna at project level to avoid writing code every time. It is also a much better way when you need to tweak quite a few settings and you know that those settings are applicable to most of your tests.

In Arjuna you can do this by providing options under `arjunaOptions` section in `<Project root directory>/config/project.conf` file.

```javascript

arjunaOptions {
    browser.name = firefox
}
```

Add the above content to `project.conf` file. We want to tweak `ArjunaOption.BROWSER_NAME`. Correspondingly you can add entry for `BROWSER_NAME` in `arjunaOptions`. For being more intuitive and less mistake prone, Arjuna supports keys in this section as **case-insensitive** and treats **. (dot)** and **_ (underscore)** as interchangeable. This is similar to the behavior of option name string seen in previous section.

Please note that the contents of `arjunaOptions` follow [HOCON](https://github.com/lightbend/config/blob/master/HOCON.md) syntax. This means that you can write settings in properties syntax, as JSON or as human-readable JSON syntax supported by HOCON.

```python
# arjuna-samples/arjex_core_features/tests/modules/test_03_tweaking_config.py

@test
def test_project_conf(my, request):
    google = WebApp(base_url="https://google.com")
    google.launch()
    my.asserter.assert_equal("Google", google.title, "Page title")
    google.quit()

```

The code for this example is exactly same as the code that used Chrome for this use case. But instead of launching Chrome, the WebApp launches Firefox browser.

#### Change Configuration Settings Programmatically
  
 ```python
 # arjuna-samples/arjex_core_features/tests/modules/test_03_tweaking_config.py
 
 from arjuna import *
 
 @test
def test_update_config(my, request):
    context = Arjuna.get_run_context()
    cc = context.config_creator
    cc.arjuna_option(ArjunaOption.BROWSER_NAME, BrowserName.FIREFOX)
    cc.register()

    google = WebApp(base_url="https://google.com", config=context.get_config())
    google.launch()
    my.asserter.assert_equal("Google", google.title, "Page title")
    google.quit()
 ```
   
##### Points to Note
1. `RunContext` is retrieved by calling `Arjuna.get_run_context()`.
2. `context.config_creator` gives a configuration creator.
3. We can tweak an Arjuna option by calling `arjuna_option` builder method of the `config_creator`. Here, we are specifying browser name as the target option and firefox as the value. We can change more settings in this manner.  
4. We call the `register` method of the config creator to update the configuration. As configurations are immutable, it means a new `Configuration` object is created and it replaces the original configuration (in this case the default configuration of the RunContext, a copy of the reference Configuration).
5. `WebApp` by default uses the reference Configuration. You can change this by passing the optional keyword argument `config=context.get_config()` while initializing `WebApp`.
6. All other steps are same as previous code.

### Simpler Builder Methods
 
 ```python
 # arjuna-samples/arjex_core_features/tests/modules/test_03_tweaking_config.py
 
 from arjuna import *
 
 @test
def test_simpler_builder_method(my, request):
    context = Arjuna.get_run_context()
    cc = context.config_creator
    cc.firefox()
    cc.register()

    google = WebApp(base_url="https://google.com", config=context.get_config())
    google.launch()
    my.asserter.assert_equal("Google", google.title, "Page title")
    google.quit()
 ```

Some Arjuna options are so commonly tweaked that Configuration creator provides direct named methods for tweaking them. Changing browser to Firefox instead of Chrome is one of them. In the above code, we directly call `firefox()` builder method instead of the longer `arjuna_option` call version in previous example.


### User Options

Just like Arjuna options, you can define your own options in `project.conf` file as well as programmatically. Rest of the fundamentals remain same as Arjuna options. That's the key point! Arjuna provides you the same facilities for your own defined options that it provides to built-in `ArjunaOption`s.

In Arjuna you can define your own option under `userOptions` section in `<Project root directory>/config/project.conf` file.

```javascript

userOptions {
    target.url = "https://google.com"
}
```

In addition to this we will also define an option `target.title` programmatically.

```python
# arjuna-samples/arjex_core_features/tests/modules/test_03_tweaking_config.py

@test
def test_user_options(my, request):
    context = Arjuna.get_run_context()
    cc = context.config_creator
    cc.user_option("target.title", "Google")
    cc.register()

    config = context.get_config()

    url = config.get_user_option_value("target.url").as_str()
    title = config.get_user_option_value("target.title").as_str()

    google = WebApp(base_url=url, config=config)
    google.launch()
    my.asserter.assert_equal(title, google.title, "Page Title")
    google.quit()
```

##### Points to Note
1. Creating a user option is same as earlier with the only difference that you need to call the `user_option` builder method of `config_creator`.
2. For retrieving the value, call `get_user_option_value` method of `Configuration`. Like in case of `ArjunaOption`s, the value is returned as `Value` object. Use its methods for appropriate processing.
3. Rest of the code is similar to the basic use case code used so far. It uses the values retrieved from user options in `Configuration`.

