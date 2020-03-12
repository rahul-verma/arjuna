### Configuration Builder - Creating Custom Configurations

In Arjuna, you can create your own configurations as well. You can do this by using reference Configuration or any other configuration created by you as the source object.
  
```python
# arjuna-samples/arjex_config/test/module/check_03_create_conf.py
 
from arjuna import *
 
@test
def check_update_config(request):
from arjuna import *

@test
def check_create_config(request):
    cb = request.config.builder
    cb.option(ArjunaOption.BROWSER_NAME, BrowserName.FIREFOX)
    # or
    cb.option("browser.name", BrowserName.FIREFOX)
    # or
    cb["browser_name"] = BrowserName.FIREFOX
    # or
    cb.browser_name = BrowserName.FIREFOX
    config = cb.register()

    google = WebApp(base_url="https://google.com", config=config)
    google.launch()
    request.asserter.assert_equal("Google", google.get_title(), "Page title does not match.")
    google.quit()
```
   
##### Points to Note
1. `Configuration` object's `builder` property creates and returns a `ConfigBuilder` object that uses it as its source configuration.
2. We can tweak an Arjuna option by calling `option` builder method of the `ConfigBuilder`. Here, we are specifying browser name as the target option and firefox as the value. We can change more settings in this manner.  
3. We can also use the `. dot notation` or `[] dict style` for adding/updating options.
4. We call the `register` method of the config creator to update the configuration. If no name is provided, Arjuna creates a unique configuration name for a given test session.
5. The newly created configuration is returned by the `register` call.
5. `WebApp` by default uses the reference Configuration. You can change this by passing the optional keyword argument `config=config` while initializing `WebApp`.
6. All other steps are same as previous code.

### Named Configuration

Sometimes it is useful to provide your own name to the custom configuration that you are creating. Arjuna helps you in creating the configuration in one place and retrieving it in another place. You need not pass the configuration object around for simple needs of this nature.

```python
# arjuna-samples/arjex_config/test/module/check_03_create_conf.py
 
from arjuna import *

@test
def check_named_config(request):
    cb = request.config.builder
    cb.browser_name = BrowserName.FIREFOX
    cb.register("my_config")

    config = Arjuna.get_config("my_config")
    print(config.name)

    config = request.get_config("my_config")
    print(config.name) 

    google = WebApp(base_url="https://google.com", config=config)
    google.launch()
    request.asserter.assert_equal("Google", google.get_title(), "Page title does not match.")
    google.quit()
```

##### Points to Note
1. You can explcitly name a configuration by calling `register` method of `ConfigBuilder` with a name argument.
2. This newly created configuration can be retrieved anywhere by calling `Arjuna.get_config(<name>)` method.
3. Within a test or a test fixture, you can also retrieve it by calling `request.get_config(<name>) method.

### Simpler Builder Methods
 
 Some Arjuna options are so commonly tweaked that Configuration creator provides direct named methods for tweaking them. 

 ```python
 # arjuna-samples/arjex_config/test/module/check_03_create_conf.py
 
 from arjuna import *
 
 @test
 def check_simpler_builder_method(request):
    cb = request.config.builder
    cb.firefox()
    config = cb.register()

    google = WebApp(base_url="https://google.com", config=context.get_config())
    google.launch()
    request.asserter.assert_equal("Google", google.get_title(), "Page title does not match.")
    google.quit()
 ```

Changing browser to Firefox instead of Chrome is one of them. In the above code, we directly call `firefox()` builder method instead of the longer alternatives in previous examples.
