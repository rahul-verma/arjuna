### Environments and Dynamic Configurations

In today's Agile environments, typically testers run automated tests on multiple environments. These environments could have their own respective properties (e.g. Application URL, user name, password and so on.)

In Arjuna, you can define configurations for environments and use them very easily in your test automation framework.

1. You can define one or more `environment_name.conf` files exactly like a `project.conf` file.
2. Place these files in `<Project Root>/config/env` directory.
3. Arjuna automatically loads these files.

#### Sample Environment configurations

The sample project contains two sample environment configurarions. They contain same options with different values for the purpose of demonstration.

**tenv1.conf**

```javascript
arjunaOptions {
    aut.base.url = "https://tenv1"
}

userOptions {
    user = "tenv1_user" 
    pwd = "tenv1_pwd"
}
```

**tenv2.conf**

```javascript
arjunaOptions {
    aut.base.url = "https://tenv2"
}

userOptions {
    user = "tenv2_user" 
    pwd = "tenv2_pwd"
}
```

#### Progammatically retrieving values from an environment configuration

```python
# arjuna-samples/arjex_config/test/module/check_07_env_config.py

from arjuna import *

@test
def check_env_confs_with_conf(request):

    tenv1 = Arjuna.get_config("tenv1")
    tenv2 = Arjuna.get_config("tenv2")

    print(tenv1.browser_name)
    print(tenv2.browser_name)

    print(tenv1.aut_base_url)
    print(tenv2.aut_base_url)

    print(tenv1.user)
    print(tenv2.user)

    tenv1 = request.get_config("tenv1")
    tenv2 = request.get_config("tenv2")

    print(tenv1.browser_name)
    print(tenv2.browser_name)

    print(tenv1.aut_base_url)
    print(tenv2.aut_base_url)

    print(tenv1.user)
    print(tenv2.user)
```

##### Points To Note
1. You can retrieve an environment config by its name using `Arjuna.get_config` or `request.get_config` call.
2. Now you can inquire the values just like you deal with any configuration in Arjuna.

#### Retrieving Environment configuration options using the `C` Magic function

```python
# arjuna-samples/arjex_config/test/module/check_07_env_config.py

@test
def check_env_confs_with_CFunc(request):
    print(C("tenv1.browser_name"))
    print(C("tenv2.browser_name"))

    print(C("tenv1.aut_base_url"))
    print(C("tenv2.aut_base_url"))

    print(C("tenv1.user"))
    print(C("tenv2.user"))
```

##### Points To Note
1. You can use the configuration query syntax `<confname>.<option>` to retrieve configuration values for an environment. 

#### Making an environment configuration as the default

You can do a session wide update that the reference configuration should utilize configuration values from a given environment config.

You do this by providing `--run-env` CLI switch.

Provide `--run-env tenv2` and run the following test to see the impact:

```python
# arjuna-samples/arjex_config/test/module/check_07_env_config.py

def check_runenv_cli(request):
    '''
        Pass --run-env tenv2 in CLI
    '''

    conf = Arjuna.get_config()
    print(conf.browser_name)
    print(conf.aut_base_url)
    print(conf.user)

    print(C("browser.name"))
    print(C("aut.base.url"))
    print(C("user"))
```

#### Instructing Arjuna to use a Custom Configuration

With today's integration needs, at times you might need to create a configuration outside of Arjuna test project's structure and instruct Arjuna to do a session wide update that the reference configuration should utilize configuration values from a configuration file at a given path.

You do this by providing `--run-conf` CLI switch.

**Sample dynamic.conf** 

```javascript
arjunaOptions {
    aut.base.url = "https://dyn"
}

userOptions {
    user = "dyn_user"
}
```

Provide `--run-conf <path of dynamic.conf>` and run the following test to see the impact:

```python
# arjuna-samples/arjex_config/test/module/check_07_env_config.py

@test
def check_runconf_cli(request):
    conf = Arjuna.get_config()
    print(conf.browser_name)
    print(conf.aut_base_url)
    print(conf.user)

    print(C("browser.name"))
    print(C("aut.base.url"))
    print(C("user"))

```


#### Combining `--run-env` and `--run-conf`

If you pass the switches together:
1. Arjuna first does a reference config update from run-env named conf file.
2. Then it updates the configuration with the one at run-conf path.

Provide `--run-env tenv2 --run-conf <path of dynamic.conf>` and run the following test to see the impact:

```python
# arjuna-samples/arjex_config/test/module/check_07_env_config.py

@test
def check_runenv_runconf_cli(request):
    conf = Arjuna.get_config()
    print(conf.browser_name)
    print(conf.aut_base_url)
    print(conf.user)
    print(conf.pwd)

    print(C("browser.name"))
    print(C("aut.base.url"))
    print(C("user"))
    print(C("pwd"))
```


