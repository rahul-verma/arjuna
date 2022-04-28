.. _guiapp:

The **GuiApp** class
====================

Learning Web UI test automation in Arjuna starts with the concept of **GuiApp** object.

A web application is represented using a **GuiApp** object. To automate your web application, you create an instance of **GuiApp** and call its methods or methods of its objects for automation purpose.

Web automation facilities in Arjuna use Selenium WebDriver as the underlying browser automation library.

**Launching** a Web Application
-------------------------------

.. code-block:: python

   google = GuiApp()
   google.launch(blank_slate=True)
   google.go_to_url("https://google.com")
   google.quit()

1. You can create an object of **GuiApp**. By default, **GuiApp** uses Arjuna's reference **Configuration**. In turn, it uses the corresponding options to launch the underlying automator. You can change this by passing the **Configuration** object using **config** argument of the App constructor.
2. You can launch the **GuiApp**. Here, we pass **blank_slate** as **True** as no base URL is associated as of now with the **GuiApp** (see next section).
3. Here the **GuiApp** uses the reference **Configuration** of Arjuna where default browser is Chrome. So, Chrome is launched as the browser.
4. You can use its **go_to_url** method to go to Google search page.
5. You can quit the app using **quit** method of **GuiApp**.

Associating a App with a **Base URL**
-------------------------------------

You can associate the **GuiApp** with a base URL by providing **url** arg while creating its object. Now the app knows where to go when it is launched. If this represents your situation (which mostly is the case), then it leads to much simpler code as follows:

.. code-block:: python

   google = GuiApp(url="https://google.com")
   google.launch()
   google.quit()

Setting GuiApp **Base URL in Configuration**
--------------------------------------------

During initilization, **GuiApp** automatically looks for the **ArjunaOption.APP_URL** option in the **Configuration** object associated with it. It means you can provide this option in any of the following ways:
    - Modify Reference **Configuration**
        - Add this option in **project.yaml** file.
        - Provide it as a CLI option.
    - Use **ConfigBuilder** to update or create a new **Configuration**. Pass it as argument while instantiating **GuiApp**, for example:
 
 
.. code-block:: python

   cb = Arjuna.get_config().builder
   cb.option(ArjunaOption.APP_URL, "https://google.com")
   config = cb.register()
   
   google = GuiApp(config=config)
   google.launch()
   google.quit()
