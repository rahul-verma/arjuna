### Getting Started with WebApp

Learning Web UI test automation in Arjuna starts with the concept of `WebApp` object.

A web application is represented using a `WebApp` object. To automate your web application, you create an instance of `WebApp` and call its methods or methods of its objects for automation purpose.

Web automation facilities in Arjuna use Selenium as the underlying browser automation library.

#### Launching a `WebApp`

```python
# arjuna-samples/arjex_webui_basics/tests/modules/check_01_webapp.py

@test
def check_webpp_nobase_url(my, request):
    google = WebApp()
    google.launch(blank_slate=True)
    google.go_to_url("https://google.com")
    my.asserter.assert_equal("Google", google.title, "Page title")
    google.quit()
```

##### Points to Note
1. We create an object of `WebApp`. By default, `WebApp` uses Arjuna's reference `Configuration`. In turn, it uses the corresponding options to launch the underlying automator. You can change this by passing the `Configuration` object using `config` argument of the WebApp constructor.
2. We launch the `WebApp`. We pass `blank_slate` as `True` as no base URL is associated as of now with the `WebApp` (see next section).
3. Here the `WebApp` uses the reference `Configuration` of Arjuna where default browser is Chrome. So, Chrome is launched as the browser.
4. We use its `go_to_url` method to go to Google search page.
5. We use `my.asserter` for asserting the title.
6. We quit the app using `quit` method of `WebApp`.

#### Associating a `WebApp` with a Base URL

We can associated the `WebApp` with a base URL by providing `base_url` arg while creating its object. Now the app knows where to go when it is launched. If this represents your situation (which mostly is the case), then it leads to much simpler code as follows:

```python
# arjuna-samples/arjex_webui_basics/tests/modules/check_01_webapp.py

@test
def check_webpp_nobase_url(my, request):
    google = WebApp(base_url="https://google.com")
    google.launch()
    my.asserter.assert_equal("Google", google.title, "Page title")
    google.quit()
```

During initilization, `WebApp` automatically looks for the `ArjunaOption.AUT_BASE_URL` option in the `Configuration` object associated with it. It means you can provide this option in any of the following ways:
- Modify Reference `Configuration`
  - Add this option in `project.conf` file.
  - Provide it as a CLI option.
 - Use RunContext to update or create a new `Configuration`. Pass it as argument while instantiating `WebApp`. This is what we will for this example:
 
 
```python
# arjuna-samples/arjex_webui_basics/tests/modules/check_01_webapp.py

 @test
def check_webpp_base_url_in_custom_config(my, request):
    context = Arjuna.get_run_context()
    cc = context.config_creator
    cc.arjuna_option(ArjunaOption.AUT_BASE_URL, "https://google.com")
    cc.register()

    google = WebApp(config=context.get_config())
    google.launch()
    my.asserter.assert_equal("Google", google.title, "Page title")
    google.quit()
```
 
 






