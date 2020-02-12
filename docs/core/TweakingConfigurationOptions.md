### Tweaking Configuration Options

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
  
  
  #### Update Configuration
  
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
    my.asserter.assertEqual("Google", google.ui.main_window.title)
    google.quit()
 ```
   
##### Points to Note
1. `RunContext` is retrieved by calling `Arjuna.get_run_context()`.
2. `context.config_creator` gives a configuration creator.
3. We can tweak an Arjuna option by calling `arjuna_option` builder method of the `config_creator`. Here, we are specifying browser name as the target option and firefox as the value. We can change more settings in this manner.  
4. We call the `register` method of the config creator to update the configuration. As configurations are immutable, it means a new `Configuration` object is created and it replaces the original configuration (in this case the default configuration of the RunContext, a copy of the reference Configuration).
5. `WebApp` by default uses the reference Configuration. You can change this by passing the optional keyword argument `config=context.get_config()` while initializing `WebApp`.
6. All other steps are same as previous code.
   
   
   
   
  
