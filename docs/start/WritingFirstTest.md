### Writing Your First Test

Writing a basic test in Arjuna is very easy. 

For exploring Arjuna fundamentals, we will consider a very basic web UI test automation case:
1. Open a browser.
2. Go to a URL.
3. Assert the correctness of its title.
4. Quit the browser.

#### Pre-requisites

Selenium WebDriver is the underlying browser automation engine in Arjuna. It needs driver executable for a given browser to be found. 

Arjuna automatically downloads drivers as per the browser version installed on your system. This feature can be switched off, but that's for a later discussion.

Arjuna supports only **Chrome** and **Firefox** as the browsers.

```python
# arjuna-samples/arjex_start/test/module/check_01_simple_test.py

from arjuna import *

@test
def check_go_to_url(request):
    google = WebApp(base_url="https://google.com")
    google.launch()
    request.asserter.assert_equal("Google", google.get_title(), "Page title does not match.")
    google.quit()
```

#### Points to Note
1. Create a test module in `<Project Root Directory>/test/module`. The module name should start with the prefix `check_`
2. In the python test module file, import all names from Arjuna: `from arjuna import *`. Ofcourse, as you become more aware of Arjuna's TPI (tester programming interface), you can do selective imports using Python.
3. Create a test. In Arjuna, a test is a function marked with `@test` decorator. It must start with the prefix `check_`. It should take **one mandatory argument**: `request`.
4. The contents of the test function depend on the test that you want to write. Following are the steps in the above test. We will cover more details on Web UI test automation in a later section. For now, just make do with the high level details.
  - Create a WebApp and provide its `base_url` argument as `https://google.com`.
  - Launch the app using its `.launch()` method. It launches **Chrome**, as it is the **default browser in Arjuna**.
  - We assert the expected title using `request.asserter` object's `assert_equal` method. The actual window title of the browser can be got as `<app object>.title`. The last argument of the assertion method is `msg` string which should be used to give proper message in the context of the automated test where you are using this assertion. You can also pass a `msg` argument to include a message which will be included in the report if this assertion fails.
  - Quit the app using its `quit` method.

#### Running the test
You can run this test by running `arjuna_launcher.py` Python script at the root of the project and passing the `-it` or `--include-tests` command line option:

`python arjuna_launcher.py run-selected -it check_go_to_url`


