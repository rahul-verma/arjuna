### Configurations in Arjuna

#### Understanding Configuration System of Arjuna
- Arjuna supports tweaking its built in options which are represented by `ArjunaOption` enum. 
- Arjuna also supports user defined options.
- A `Configuration` object represents fixed values for configured settings (Arjuna options as well user defined options).
- As a part of initialation, Arjuna creates the reference `Configuration` object which combines the following to create the reference :
    - Default settings for Arjuna options
    - Project level settings included in `<Project root directory>/config/project.conf` file.
    - CLI Options for settings (TBD).
- You can get the reference configuration by calling `Arjuna.get_config()`.

#### Retrieving value of Arjuna options in Code

```python
# arjuna-samples/arjex_core_features/test/module/check_02_config.py
 
from arjuna import *

@test
def check_config_retrieval(request):
    config = Arjuna.get_config()

    print(config.value(ArjunaOption.BROWSER_NAME))

    print(config.value("BROWSER_NAME"))
    print(config.value("BrOwSeR_NaMe"))
    print(config.value("browser.name"))
    print(config.value("Browser.Name"))

    print(config["browser.name"])

    print(config.browser_name)
 ```

##### Points to Note
1. First, we retrieve the reference config by calling `Arjuna.get_config()`
2. You can retrieve value of an `ArjunaOption` by calling the `value(<Arjuna Option or string>)` method of a `Configuration` object. The argument to this call can be an `ArjunaOption` enum constant or a string representing the option.
3. The option name string is considered by Arjuna as **case-insensitive**. Also, **. (dot)** and **_ (underscore)** are interchangeable. So, following are equivalent arguments:
    - ArjunaOption.BROWSER_NAME
    - BROWSER_NAME
    - BrOwSeR_NaMe
    - browser.name
    - Browser.Name
    - and so on
4. The `Configuration` object also allows for retrieval of a config option using the `. (dot notation)` or `[name] i.e. (dict-like name based retrieval)`.


#### The `C` function

```python
# arjuna-samples/arjex_core_features/test/module/check_02_config.py

@test
def check_config_retrieval_C(request):
    print(C(ArjunaOption.BROWSER_NAME))
    print(C("browser.name"))
    print(C("BROWSER_NAME"))
```

##### Points to Note
1. Arjuna provides a special function `C` for retrieving values from the reference configuration as it is a very common operation to do on test code.
2. You can pass an `ArjunaOption` enum constant or an option name. The name string has all the flexibility seen in previous example.

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
# arjuna-samples/arjex_core_features/test/module/check_03_tweaking_config.py

@test
def check_project_conf(request):
    google = WebApp(base_url="https://google.com")
    google.launch()
    request.asserter.assert_equal("Google", google.title, "Page title does not match.")
    google.quit()

```

The code for this example is exactly same as the code that used Chrome for this use case. But instead of launching Chrome, the WebApp launches Firefox browser.

#### Change Configuration Settings Programmatically
  
```python
# arjuna-samples/arjex_core_features/test/module/check_02_config.py
 
from arjuna import *
 
@test
def check_update_config(request):
    cc = Arjuna.get_config_creator()
    cc.option(ArjunaOption.BROWSER_NAME, BrowserName.FIREFOX)
    # or
    cc.option("browser.name", BrowserName.FIREFOX)
    # or
    cc["browser_name"] = "Google"
    # or
    cc.browser_name = BrowserName.FIREFOX
    config = cc.register()

    google = WebApp(base_url="https://google.com", config=config)
    google.launch()
    request.asserter.assert_equal("Google", google.title, "Page title does not match.")
    google.quit()
```
   
##### Points to Note
1. `ConfigCreator` is retrieved by calling `Arjuna.get_config_creator()`.
2. We can tweak an Arjuna option by calling `option` builder method of the `ConfigCreator`. Here, we are specifying browser name as the target option and firefox as the value. We can change more settings in this manner.  
3. We can also use the `. dot notation` or `[] dict style` for adding/updating options.
4. We call the `register` method of the config creator to update the configuration. As configurations are immutable, it means a new `Configuration` object is created and it replaces the original configuration (in this case the default configuration of the RunContext, a copy of the reference Configuration).
5. The newly created configuration is returned by the `register` call.
5. `WebApp` by default uses the reference Configuration. You can change this by passing the optional keyword argument `config=config` while initializing `WebApp`.
6. All other steps are same as previous code.

### Simpler Builder Methods
 
 ```python
 # arjuna-samples/arjex_core_features/test/module/check_02_config.py
 
 from arjuna import *
 
 @test
 def check_simpler_builder_method(request):
    cc = Arjuna.get_config_creator()
    cc.firefox()
    config = cc.register()

    google = WebApp(base_url="https://google.com", config=context.get_config())
    google.launch()
    request.asserter.assert_equal("Google", google.title, "Page title does not match.")
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
# arjuna-samples/arjex_core_features/test/module/check_02_config.py

@test
def check_user_options(request):
    # Just like Arjuna options, C works for user options in reference config
    url = C("target.url")

    cc = Arjuna.get_config_creator()
    cc.option("target.title", "Google")
    # or
    cc["target.title"] = "Google"
    # or
    cc.target_title = "Google"
    config = cc.register()

    title = config.target_title
    #or
    title = config["target.title"] # or config.value("target.title") or other variants seen earlier
    url = config.value("target.url") # Ref user options are available in new config as well.

    google = WebApp(base_url=url, config=config)
    google.launch()
    request.asserter.assert_equal(title, google.title, "Page title does not match.")
    google.quit()
```

##### Points to Note
1. Creating a user option and retrieving its value is done in exactly the same manner as Arjuna options.

