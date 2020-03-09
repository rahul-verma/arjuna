### Fundamentals of Configuration in Arjuna

#### Understanding Configuration System of Arjuna
- Arjuna supports tweaking its built in options which are represented by `ArjunaOption` enum. 
- Arjuna also supports user defined options.
- A `Configuration` object represents fixed values for configured settings (Arjuna options as well user defined options).
- A `Configuration` is immutable which means that once created it can not be modified.
- As a part of initialation, Arjuna creates the reference `Configuration` object which combines the following to create the reference :
    - Default settings for Arjuna options
    - Project level settings included in `<Project root directory>/config/project.conf` file.
    - Environment configuration represented by its name passed as `--run-env` switch.
    - Run-time configuration file provided with `--run-conf` switch.
    - CLI options represtedn by Arjuna's named CLI switches (e.g. for logging options)
- You can get the reference configuration by calling `Arjuna.get_config()`.

#### Accesing Reference Configuration

```python
# arjuna-samples/arjex_config/test/module/check_01_config.py
 
from arjuna import *

@test
def check_ref_config_retrieval(request):
    config = Arjuna.get_config()
    print(config.name)

    config = request.config
    print(config.name)
 ```

##### Points to Note
1. We can get reference Configuration object by calling `Arjuna.get_config()` method.
2. Name of reference or any configuration can be got with its `name` property.
3. Within test or test fixture code, we can also get the reference configuration object (if not re-assigned by test author to a non-reference configuration) using `request.config`.

#### Retrieving value of Arjuna options

```python
# arjuna-samples/arjex_config/test/module/check_01_config.py
 
from arjuna import *

@test
def check_config_retrieval(request):
    config = request.config

    print(config.value(ArjunaOption.BROWSER_NAME))

    print(config.value("BROWSER_NAME"))
    print(config.value("BrOwSeR_NaMe"))
    print(config.value("browser.name"))
    print(config.value("Browser.Name"))

    print(config["browser.name"])

    print(config.browser_name)
 ```

##### Points to Note
1. You can retrieve value of an `ArjunaOption` by calling the `value(<Arjuna Option or string>)` method of a `Configuration` object. The argument to this call can be an `ArjunaOption` enum constant or a string representing the option.
2. The option name string is considered by Arjuna as **case-insensitive**. Also, **. (dot)** and **_ (underscore)** are interchangeable. So, following are equivalent arguments:
    - ArjunaOption.BROWSER_NAME
    - BROWSER_NAME
    - BrOwSeR_NaMe
    - browser.name
    - Browser.Name
    - and so on
3. The `Configuration` object also allows for retrieval of a config option using the `. (dot notation)` or `[name] i.e. (dict-like name based retrieval)`.
