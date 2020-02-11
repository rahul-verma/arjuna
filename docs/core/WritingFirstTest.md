### Writing Your First Test

Writing a basic test in Arjuna is very easy. 

You can find the example code used on this page in [arjuna_core_features project](https://github.com/rahul-verma/arjuna//tree/master/arjuna-samples/arjex_core_features/tests/modules).

For exploring Arjuna fundamentals, we will consider a very basic web UI test automation case:
1. Open a browser.
2. Go to a URL.
3. Assert the correctness of its title.
4. Quit the browser.

#### Pre-requisites


Place Selenium **Chromedriver** and **Geckodriver** excutables in the [drivers directory for your OS](ProjectStructure.md).

```python
# test_01_launch_chrome.py

from arjuna import *

@test
def test_launch_chrome(my, request):
    google = WebApp(base_url="https://google.com")
    google.launch()
    my.asserter.assertEqual("Google1", google.ui.main_window.title)
    google.quit()
```

#### Points to Note
1. Create a test module in `<Project Root Directory>/tests/modules`. The module name should start with the prefix `test_`
2. In the python test module file, import all names from Arjuna: `from arjuna import *`. Ofcourse, as you become more aware of Arjuna's TPI (tester programming interface), you can do selective imports using Python.
3. Create a test. In Arjuna, a test is a function marked with `@test` decorator. It must start with the prefix `test_`. It should take two mandatory arguments - `my` and `request`.
4. The contents of the test function depend on the test that you want to write. Following are the steps in the above test. We will cover more details on Web UI test automation in a later section. For now, just make do with the high level details.
  - Create a WebApp and provide its `base_url` argument as `https://google.com`.
  - Launch the app using its `.launch()` method.
  - We assert the expected title using `my.asserter` object's `assertEqual` method. The actual window title of the browser can be got as `<app object>.ui.main_window.title`.
  - Quit the app using its `quit` method.

#### Running the test
You can run this test by running `arjuna_launcher.py` Python script at the root of the project and passing the `-ct` or `--consider-tests` command line option:

`python arjuna_launcher.py run-selected -ct test_launch_chrome`


