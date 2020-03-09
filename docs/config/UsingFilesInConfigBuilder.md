### Configuration Builder - Adding options from a .conf File

`ConfigBuilder` can also load Arjuna options as well user options from `.conf` files. It comes handy when you have a controlled set of configurations which want to create at run-time. It could be also helpful if for some reasons your logic involves clubbing of options from multiple files.

```python
# arjuna-samples/arjex_config/test/module/check_05_builder_file.py
 
from arjuna import *

@test
def check_builder_file_based_options(request):
    cb = request.config.builder
    cb.option("prog.option", "Programmatic")
    cb.from_file("dynamic.conf")
    config = cb.register()

    print(config.prog_option)
    print(config.browser_name)

    print(config.app_url)
    print(config.user)
 ```

##### Points to Note
1. You can load options from any file using `from_file` method of `ConfigBuilder` and providing the file path.
2. If instead of full absolute path, a name or relative file path is provided, Arjuna creates the path in relation to the default configuration directory - `<Project Root>/config`.
3. The above example shows a combination of programmatically added user option in combination with a `.conf` file containing Arjuna options and user options.