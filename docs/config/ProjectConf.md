### project.conf - Setting Project Level Configuration Options

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
    request.asserter.assert_equal("Google", google.get_title(), "Page title does not match.")
    google.quit()

```

The code for this example is exactly same as the code that used Chrome for this use case. But instead of launching Chrome, the WebApp launches Firefox browser.
