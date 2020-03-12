### Defining and Handling User Options

Just like Arjuna options, you can define your own options in `project.conf` file as well as programmatically. Rest of the fundamentals remain same as Arjuna options. That's the key point! Arjuna provides you the same facilities for your own defined options that it provides to built-in `ArjunaOption`s.

In Arjuna you can define your own option under `userOptions` section in `<Project root directory>/config/project.conf` file.

```javascript

userOptions {
    target.url = "https://google.com"
}
```

In addition to this we will also define an option `target.title` programmatically.

```python
# arjuna-samples/arjex_config/test/module/check_04_user_options.py

@test
def check_user_options(request):
    '''
        For this test:
        You must add target.url = "https://google.com" to userOptions in project.conf to see the impact.
    '''
    # Just like Arjuna options, C works for user options in reference config
    url = C("target.url")

    cb = request.config.builder
    cb.option("target.title", "Google")
    # or
    cb["target.title"] = "Google"
    # or
    cb.target_title = "Google"
    config = cb.register()

    title = config.target_title
    #or
    title = config["target.title"] # or config.value("target.title") or other variants seen earlier
    url = config.value("target.url") # Ref user options are available in new config as well.

    google = WebApp(base_url=url, config=config)
    google.launch()
    request.asserter.assert_equal(title, google.get_title(), "Page title does not match.")
    google.quit()
```

##### Points to Note
1. Creating a user option and retrieving its value is done in exactly the same manner as Arjuna options.

